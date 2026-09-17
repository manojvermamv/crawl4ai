#!/usr/bin/env python3
"""Agent-callable, adapter-based crawler for OpenAlgo and arXiv HTML sources.

The OpenAlgo adapter deliberately discovers the catalogue on every run.  It
never embeds course names, course slugs, chapter names, or chapter counts.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
import re
import tempfile
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, Iterable
from urllib.parse import urljoin, urlsplit, urlunsplit

# Keep Crawl4AI's database, robots cache, and logs beside this portable script
# unless a host explicitly provides a shared base directory.  This must precede
# the Crawl4AI import because the library reads it at import time.
os.environ.setdefault("CRAWL4_AI_BASE_DIRECTORY", str(Path(__file__).resolve().parent / ".crawl4ai-runtime"))

from bs4 import BeautifulSoup, Tag
from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig


DEFAULT_START_URL = "https://openalgo.in/learn"
STATE_FILE_NAME = "crawl-state.json"
MANIFEST_FILE_NAME = "manifest.json"
REPORT_FILE_NAME = "latest-run.json"


def canonical_url(url: str) -> str:
    """Drop fragments/query strings so one content page has one identity."""
    parsed = urlsplit(url)
    path = parsed.path.rstrip("/") or "/"
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, "", ""))


def validate_request(
    start_url: str,
    max_depth: int,
    retries: int,
    concurrency: int,
    adapter: SourceAdapter | None = None,
) -> None:
    """Validate shared crawl controls plus the selected adapter's URL scope."""
    selected = adapter or ADAPTERS["openalgo"]
    selected.validate_start_url(start_url)
    if max_depth < selected.minimum_depth():
        raise ValueError(f"max_depth must be at least {selected.minimum_depth()} for the {selected.name} adapter")
    if retries < 0:
        raise ValueError("retries must be zero or greater")
    if concurrency < 1:
        raise ValueError("concurrency must be at least 1")


def slugify(value: str, fallback: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value[:96] or fallback


def markdown_value(result: Any) -> str:
    """Support Crawl4AI's string and MarkdownGenerationResult return shapes."""
    markdown = getattr(result, "markdown", "")
    for attribute in ("fit_markdown", "raw_markdown", "markdown"):
        value = getattr(markdown, attribute, None)
        if isinstance(value, str) and value.strip():
            return value.strip() + "\n"
    return str(markdown).strip() + "\n"


def page_html(result: Any) -> str:
    return str(getattr(result, "cleaned_html", None) or getattr(result, "html", ""))


def page_title(html: str, fallback: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    heading = soup.find("h1")
    title = heading.get_text(" ", strip=True) if heading else ""
    if not title and soup.title:
        title = soup.title.get_text(" ", strip=True).split("|")[0].strip()
    return title or fallback


def content_root(html: str) -> Tag | BeautifulSoup:
    soup = BeautifulSoup(html, "html.parser")
    return soup.find("main") or soup.find("article") or soup.body or soup


def is_internal_content_url(url: str, origin: str) -> bool:
    parsed = urlsplit(url)
    return parsed.scheme in {"http", "https"} and parsed.netloc.lower() == urlsplit(origin).netloc.lower()


def anchor_context(anchor: Tag) -> str:
    pieces: list[str] = [anchor.get_text(" ", strip=True)]
    parent: Tag | None = anchor.parent if isinstance(anchor.parent, Tag) else None
    for _ in range(3):
        if not parent:
            break
        # A main/body container contains text from unrelated cards and must not
        # make a navigation link look like a course or chapter link.
        if parent.name in {"main", "body"}:
            break
        pieces.append(parent.get_text(" ", strip=True))
        parent = parent.parent if isinstance(parent.parent, Tag) else None
    return " ".join(pieces).lower()


def unique_urls(urls: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for url in urls:
        url = canonical_url(url)
        if url not in seen:
            seen.add(url)
            result.append(url)
    return result


def discover_course_urls(html: str, base_url: str) -> list[str]:
    """Find course-card links, without depending on names or URL slugs.

    Course cards carry both a chapter count and a course call-to-action.  The
    second selector is a deliberately broader fallback for harmless site-markup
    changes; candidates are subsequently validated as course pages.
    """
    root = content_root(html)
    strict: list[str] = []
    broad: list[str] = []
    for anchor in root.find_all("a", href=True):
        absolute = canonical_url(urljoin(base_url, str(anchor["href"])))
        if absolute == canonical_url(base_url) or not is_internal_content_url(absolute, base_url):
            continue
        label = anchor.get_text(" ", strip=True).lower()
        context = anchor_context(anchor)
        if "chapter" in context and "course" in context:
            broad.append(absolute)
            # On the current catalogue each card is an anchor containing its
            # own count and CTA.  Requiring both on the anchor itself avoids
            # leaking nearby editorial/navigation links into the crawl.
            if "chapter" in label and re.search(r"start|begin|explore|view|open", label):
                strict.append(absolute)
    return unique_urls(strict or broad)


def discover_chapter_urls(html: str, course_url: str, landing_url: str) -> list[str]:
    """Return chapters in their rendered reading order from a course page."""
    root = content_root(html)
    course = canonical_url(course_url)
    landing = canonical_url(landing_url)
    numbered: list[str] = []
    chapter_area: list[str] = []
    for anchor in root.find_all("a", href=True):
        absolute = canonical_url(urljoin(course_url, str(anchor["href"])))
        if absolute in {course, landing} or not is_internal_content_url(absolute, course_url):
            continue
        text = anchor.get_text(" ", strip=True)
        context = anchor_context(anchor)
        if re.search(r"(?:^|\b)(?:chapter\s*)?\d{1,3}(?:\b|\s)", text, re.I):
            numbered.append(absolute)
        elif "chapter" in context:
            chapter_area.append(absolute)
    # Numbered links are strongest and preserve course navigation order.  The
    # fallback supports a future course whose chapter labels stop using numbers.
    return unique_urls(numbered or chapter_area)


@dataclass
class PageRecord:
    url: str
    title: str
    relative_path: str
    content_hash: str
    kind: str = "page"


@dataclass
class DiscoveredPage:
    """A page returned by a source adapter before output-path assignment."""

    url: str
    title: str
    markdown: str
    kind: str = "page"


@dataclass
class DiscoveredCollection:
    """A source-native collection with one optional overview and ordered pages."""

    url: str
    title: str
    overview: DiscoveredPage | None
    pages: list[DiscoveredPage]


FetchPage = Callable[[Any, str, int], Awaitable[Any | None]]
FetchPages = Callable[[Any, list[str], int], Awaitable[dict[str, Any]]]


class SourceAdapter(ABC):
    """Pluggable source contract used by the shared crawl/persist engine.

    An adapter owns URL scope and live hierarchy discovery.  The runner owns
    Crawl4AI execution, checkpointing, change detection, path safety, and JSON
    reporting.  Adding a source therefore does not require changing persistence
    or the agent-facing interface.
    """

    name: str
    default_start_url: str | None
    output_dir_name: str
    meta_dir_name: str
    default_max_depth: int = 0

    @abstractmethod
    def validate_start_url(self, start_url: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def url_allowed(self, url: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def discover(
        self,
        app: "OpenVarsityCrawler",
        crawler: AsyncWebCrawler,
        start_url: str,
        max_depth: int,
    ) -> list[DiscoveredCollection]:
        raise NotImplementedError

    def crawl_excluded_tags(self) -> list[str]:
        return ["nav", "footer"]

    def crawl_excluded_selector(self) -> str | None:
        return "header.sticky"

    def minimum_depth(self) -> int:
        """Smallest useful depth for this source's discovery strategy."""
        return 0

    def collection_folder(self, index: int, title: str) -> str:
        return f"{index:03d}-{slugify(title, 'collection')}"

    @abstractmethod
    def page_relative_path(
        self,
        collection_index: int,
        collection: DiscoveredCollection,
        page_index: int,
        page: DiscoveredPage,
        folder: str,
    ) -> str:
        raise NotImplementedError


class OpenAlgoAdapter(SourceAdapter):
    name = "openalgo"
    default_start_url = DEFAULT_START_URL
    output_dir_name = "courses"
    meta_dir_name = ".openvarsity"
    default_max_depth = 2
    excluded_path_prefixes = ("/features", "/download", "/blog", "/faq", "/roadmap")

    def validate_start_url(self, start_url: str) -> None:
        if canonical_url(start_url) != DEFAULT_START_URL:
            raise ValueError(f"start_url must be {DEFAULT_START_URL} for the openalgo adapter")

    def url_allowed(self, url: str) -> bool:
        if not is_internal_content_url(url, DEFAULT_START_URL):
            return False
        path = (urlsplit(url).path.rstrip("/") or "/").lower()
        return not any(path == prefix or path.startswith(prefix + "/") for prefix in self.excluded_path_prefixes)

    def minimum_depth(self) -> int:
        # The catalogue is discovered as landing → course → chapter.
        return 2

    def collection_folder(self, index: int, title: str) -> str:
        return f"{index:03d}-{slugify(title, 'course')}"

    async def discover(
        self,
        app: "OpenVarsityCrawler",
        crawler: AsyncWebCrawler,
        start_url: str,
        max_depth: int,
    ) -> list[DiscoveredCollection]:
        landing = await app.fetch(crawler, start_url, depth=0)
        if landing is None:
            raise RuntimeError("The Open Varsity landing page could not be fetched.")
        candidate_courses = [
            url for url in discover_course_urls(page_html(landing), start_url) if self.url_allowed(url)
        ]
        if not candidate_courses:
            raise RuntimeError("No course links were discovered from the Open Varsity landing page.")
        course_results = await app.fetch_many(crawler, candidate_courses, depth=1)
        discovered: list[DiscoveredCollection] = []
        for course_url in candidate_courses:
            course_result = course_results.get(course_url)
            if course_result is None:
                continue
            course_html = page_html(course_result)
            chapters = [
                url for url in discover_chapter_urls(course_html, course_url, start_url) if self.url_allowed(url)
            ]
            if not chapters:
                app.summary.skipped.append({"url": course_url, "reason": "not_a_course_page"})
                continue
            overview = DiscoveredPage(course_url, page_title(course_html, course_url), markdown_value(course_result), "overview")
            pending = await app.fetch_many(crawler, chapters, depth=2)
            pages: list[DiscoveredPage] = []
            for chapter_index, chapter_url in enumerate(chapters, 1):
                result = pending.get(chapter_url)
                if result is None:
                    continue
                html = page_html(result)
                pages.append(DiscoveredPage(chapter_url, page_title(html, f"Chapter {chapter_index}"), markdown_value(result), "chapter"))
            discovered.append(DiscoveredCollection(course_url, overview.title, overview, pages))
        return discovered

    def page_relative_path(
        self,
        collection_index: int,
        collection: DiscoveredCollection,
        page_index: int,
        page: DiscoveredPage,
        folder: str,
    ) -> str:
        if page.kind == "overview":
            filename = "000-course-overview.md"
        else:
            filename = f"{page_index:03d}-{slugify(page.title, 'chapter')}.md"
        return f"{self.output_dir_name}/{folder}/{filename}"


# arXiv supports both modern identifiers (YYMM.NNNNN) and legacy
# category/7-digit identifiers (for example hep-th/9901001).
ARXIV_HTML_PATH = re.compile(
    r"^/html/(?:\d{4}\.\d{4,5}|[A-Za-z][A-Za-z0-9.-]*/\d{7})(?:v\d+)?$"
)


def is_arxiv_html_url(url: str) -> bool:
    parsed = urlsplit(url)
    return parsed.scheme in {"http", "https"} and parsed.netloc.lower() == "arxiv.org" and bool(ARXIV_HTML_PATH.fullmatch(parsed.path))


def discover_arxiv_html_urls(html: str, base_url: str) -> list[str]:
    root = content_root(html)
    return unique_urls(
        canonical_url(urljoin(base_url, str(anchor["href"])))
        for anchor in root.find_all("a", href=True)
        if is_arxiv_html_url(canonical_url(urljoin(base_url, str(anchor["href"]))))
    )


class ArxivHtmlAdapter(SourceAdapter):
    name = "arxiv"
    default_start_url = None
    output_dir_name = "papers"
    meta_dir_name = ".arxiv"
    default_max_depth = 0

    def validate_start_url(self, start_url: str) -> None:
        if not is_arxiv_html_url(start_url):
            raise ValueError("arxiv adapter accepts only an arxiv.org/html/<paper-id>[vN] URL; PDF/abs/source URLs are excluded")

    def url_allowed(self, url: str) -> bool:
        return is_arxiv_html_url(url)

    def minimum_depth(self) -> int:
        # A single paper is a complete crawl. Explicitly increasing depth lets
        # callers follow links to other HTML papers when desired.
        return 0

    def collection_folder(self, index: int, title: str) -> str:
        return f"{index:03d}-{slugify(title, 'paper')}"

    def crawl_excluded_tags(self) -> list[str]:
        return ["header", "nav", "footer", "aside", "script", "style"]

    def crawl_excluded_selector(self) -> str | None:
        # arXiv's page shell contains a report-issue dialog, announcement
        # banner, and fixed action buttons outside the paper document. Keep
        # the document/figures while excluding those UI-only nodes.
        return "dialog, .announcement-banner, .ds-announcement, .fixed-buttons-container"

    async def discover(
        self,
        app: "OpenVarsityCrawler",
        crawler: AsyncWebCrawler,
        start_url: str,
        max_depth: int,
    ) -> list[DiscoveredCollection]:
        queue: list[tuple[str, int]] = [(canonical_url(start_url), 0)]
        seen: set[str] = set()
        collections: list[DiscoveredCollection] = []
        while queue:
            url, depth = queue.pop(0)
            if url in seen or depth > max_depth or not self.url_allowed(url):
                if depth > max_depth:
                    app.summary.skipped.append({"url": url, "reason": "max_depth"})
                continue
            seen.add(url)
            result = await app.fetch(crawler, url, depth)
            if result is None:
                continue
            html = page_html(result)
            title = page_title(html, url)
            page = DiscoveredPage(url, title, markdown_value(result), "paper")
            collections.append(DiscoveredCollection(url, title, None, [page]))
            for child in discover_arxiv_html_urls(html, url):
                if child not in seen:
                    queue.append((child, depth + 1))
        return collections

    def page_relative_path(
        self,
        collection_index: int,
        collection: DiscoveredCollection,
        page_index: int,
        page: DiscoveredPage,
        folder: str,
    ) -> str:
        return f"{self.output_dir_name}/{folder}/{page_index:03d}-{slugify(page.title, 'paper')}.md"


ADAPTERS: dict[str, SourceAdapter] = {
    "openalgo": OpenAlgoAdapter(),
    "arxiv": ArxivHtmlAdapter(),
}


def get_adapter(name: str) -> SourceAdapter:
    try:
        return ADAPTERS[name.lower()]
    except KeyError as exc:
        raise ValueError(f"unknown source adapter {name!r}; choose one of {', '.join(sorted(ADAPTERS))}") from exc


def manifest_collections(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    """Read the generic schema and the pre-adapter OpenAlgo schema."""
    if isinstance(manifest.get("collections"), list):
        return [collection for collection in manifest["collections"] if isinstance(collection, dict)]
    # Existing OpenAlgo mirrors used courses/chapters. Keep them upgradable.
    return [
        {
            **course,
            "pages": course.get("pages", course.get("chapters", [])),
        }
        for course in manifest.get("courses", [])
        if isinstance(course, dict)
    ]


def collection_pages(collection: dict[str, Any]) -> list[dict[str, Any]]:
    pages = collection.get("pages", collection.get("chapters", []))
    if not isinstance(pages, list):
        pages = []
    overview = collection.get("overview")
    return ([overview] if isinstance(overview, dict) else []) + [page for page in pages if isinstance(page, dict)]


@dataclass
class CourseRecord:
    url: str
    title: str
    relative_path: str
    overview: PageRecord
    chapters: list[PageRecord]


@dataclass
class RunSummary:
    started_at: str
    completed_at: str | None = None
    status: str = "running"
    source_url: str = DEFAULT_START_URL
    courses_discovered: int = 0
    chapters_discovered: int = 0
    pages_fetched: int = 0
    pages_written: int = 0
    pages_unchanged: int = 0
    pages_resumed: int = 0
    pages_new: list[str] = field(default_factory=list)
    pages_changed: list[str] = field(default_factory=list)
    pages_removed: list[str] = field(default_factory=list)
    courses_new: list[str] = field(default_factory=list)
    courses_changed: list[str] = field(default_factory=list)
    courses_removed: list[str] = field(default_factory=list)
    chapters_new: list[str] = field(default_factory=list)
    chapters_changed: list[str] = field(default_factory=list)
    chapters_removed: list[str] = field(default_factory=list)
    skipped: list[dict[str, str]] = field(default_factory=list)
    errors: list[dict[str, str]] = field(default_factory=list)
    verification: dict[str, Any] = field(default_factory=dict)
    # Adapter-neutral fields are appended so the historical positional
    # constructor order remains compatible for existing OpenAlgo callers.
    adapter: str = "openalgo"
    collections_discovered: int = 0
    pages_discovered: int = 0
    collections_new: list[str] = field(default_factory=list)
    collections_changed: list[str] = field(default_factory=list)
    collections_removed: list[str] = field(default_factory=list)
    papers_discovered: int = 0
    papers_new: list[str] = field(default_factory=list)
    papers_changed: list[str] = field(default_factory=list)
    papers_removed: list[str] = field(default_factory=list)
    courses_changed: list[str] = field(default_factory=list)


class OpenVarsityCrawler:
    def __init__(
        self,
        output_dir: Path,
        start_url: str = DEFAULT_START_URL,
        max_depth: int = 2,
        retries: int = 3,
        concurrency: int = 8,
        adapter: SourceAdapter | None = None,
    ) -> None:
        self.adapter = adapter or ADAPTERS["openalgo"]
        validate_request(start_url, max_depth, retries, concurrency, self.adapter)
        self.output_dir = output_dir.resolve()
        self.content_dir = self.output_dir / self.adapter.output_dir_name
        self.meta_dir = self.output_dir / self.adapter.meta_dir_name
        self.start_url = canonical_url(start_url)
        self.max_depth = max_depth
        self.retries = retries
        self.concurrency = max(1, concurrency)
        self.summary = RunSummary(started_at=self.now(), adapter=self.adapter.name, source_url=self.start_url)
        self.state: dict[str, Any] = {}

    @staticmethod
    def now() -> str:
        return datetime.now(timezone.utc).isoformat()

    def load_json(self, path: Path, default: Any) -> Any:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return default
        except (json.JSONDecodeError, OSError) as exc:
            self.summary.errors.append({"url": str(path), "error": f"state unreadable: {exc}"})
            return default

    def atomic_json(self, path: Path, value: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
            json.dump(value, handle, indent=2, sort_keys=True)
            handle.write("\n")
            temp_path = Path(handle.name)
        temp_path.replace(path)

    def checkpoint(self) -> None:
        self.atomic_json(self.meta_dir / STATE_FILE_NAME, self.state)
        self.atomic_json(self.meta_dir / REPORT_FILE_NAME, asdict(self.summary))

    def run_config(self) -> CrawlerRunConfig:
        return CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            check_robots_txt=True,
            page_timeout=60_000,
            max_retries=self.retries,
            semaphore_count=self.concurrency,
            word_count_threshold=1,
            # Keep content headers (they carry chapter H1s), while excluding
            # only the site-wide chrome and footer.
            excluded_tags=self.adapter.crawl_excluded_tags(),
            excluded_selector=self.adapter.crawl_excluded_selector(),
            url_matcher=self.adapter.url_allowed,
            verbose=False,
            log_console=False,
        )

    def accepted_result(self, result: Any, url: str, depth: int) -> Any | None:
        if depth > self.max_depth:
            self.summary.skipped.append({"url": url, "reason": "max_depth"})
            return None
        self.summary.pages_fetched += 1
        if not getattr(result, "success", False):
            reason = getattr(result, "error_message", None) or f"HTTP {getattr(result, 'status_code', 'unknown')}"
            if getattr(result, "status_code", None) == 403:
                self.summary.skipped.append({"url": url, "reason": f"robots_or_access_denied: {reason}"})
            else:
                self.summary.errors.append({"url": url, "error": str(reason)})
            return None
        return result

    async def fetch(self, crawler: AsyncWebCrawler, url: str, depth: int) -> Any | None:
        if depth > self.max_depth:
            self.summary.skipped.append({"url": url, "reason": "max_depth"})
            return None
        try:
            result = await crawler.arun(url=url, config=self.run_config())
        except Exception as exc:  # Crawl4AI/browser failures are retryable only inside its runner.
            self.summary.errors.append({"url": url, "error": str(exc)})
            return None
        return self.accepted_result(result, url, depth)

    async def fetch_many(self, crawler: AsyncWebCrawler, urls: list[str], depth: int) -> dict[str, Any]:
        """Fetch a bounded same-depth batch while retaining URL-level errors."""
        eligible = [url for url in urls if depth <= self.max_depth]
        for url in urls:
            if depth > self.max_depth:
                self.summary.skipped.append({"url": url, "reason": "max_depth"})
        if not eligible:
            return {}
        try:
            results = await crawler.arun_many(eligible, config=self.run_config())
        except Exception as exc:
            for url in eligible:
                self.summary.errors.append({"url": url, "error": str(exc)})
            return {}
        by_url: dict[str, Any] = {}
        returned: set[str] = set()
        # arun_many completes out of order.  Associate each result with the URL
        # Crawl4AI reports, never with its position in the submitted list.
        for result in results:
            result_url = canonical_url(str(getattr(result, "url", "")))
            if result_url not in eligible:
                self.summary.errors.append({"url": result_url or "unknown", "error": "unexpected URL returned by Crawl4AI"})
                continue
            returned.add(result_url)
            accepted = self.accepted_result(result, result_url, depth)
            if accepted is not None:
                by_url[result_url] = accepted
        for url in eligible:
            if url not in returned:
                self.summary.errors.append({"url": url, "error": "Crawl4AI returned no result"})
        return by_url

    def page_record(self, url: str, title: str, relative_path: str, markdown: str, kind: str = "page") -> PageRecord:
        return PageRecord(
            url=canonical_url(url),
            title=title,
            relative_path=relative_path,
            content_hash=hashlib.sha256(markdown.encode("utf-8")).hexdigest(),
            kind=kind,
        )

    def write_page(self, record: PageRecord, markdown: str, prior_pages: dict[str, dict[str, Any]]) -> bool:
        prior = prior_pages.get(record.url)
        destination = self.output_dir / record.relative_path
        if prior and prior.get("content_hash") == record.content_hash and destination.exists():
            self.summary.pages_unchanged += 1
            return False
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(markdown, encoding="utf-8")
        self.summary.pages_written += 1
        if prior:
            self.summary.pages_changed.append(record.url)
            if record.kind == "chapter":
                self.summary.chapters_changed.append(record.url)
            elif record.kind == "paper":
                self.summary.papers_changed.append(record.url)
            elif record.kind == "overview":
                self.summary.collections_changed.append(record.url)
                if self.adapter.name == "openalgo":
                    self.summary.courses_changed.append(record.url)
        else:
            self.summary.pages_new.append(record.url)
            if record.kind == "chapter":
                self.summary.chapters_new.append(record.url)
        return True

    def prune_removed(self, old_manifest: dict[str, Any], manifest: dict[str, Any]) -> None:
        old_collections = {collection["url"]: collection for collection in manifest_collections(old_manifest)}
        new_collections = {collection["url"]: collection for collection in manifest_collections(manifest)}
        for url in old_collections:
            if url not in new_collections:
                self.summary.collections_removed.append(url)
                if self.adapter.name == "openalgo":
                    self.summary.courses_removed.append(url)
                elif self.adapter.name == "arxiv":
                    self.summary.papers_removed.append(url)
        old_pages = {
            page["url"]: page
            for collection in manifest_collections(old_manifest)
            for page in collection_pages(collection)
            if page
        }
        new_pages = {
            page["url"]: page
            for collection in manifest_collections(manifest)
            for page in collection_pages(collection)
            if page
        }
        for url, page in old_pages.items():
            replacement = new_pages.get(url)
            if replacement is None or replacement["relative_path"] != page["relative_path"]:
                candidate = (self.output_dir / page["relative_path"]).resolve()
                if candidate.is_relative_to(self.content_dir) and candidate.exists():
                    candidate.unlink()
                if replacement is None:
                    self.summary.pages_removed.append(url)
                    if self.adapter.name == "openalgo" and page["relative_path"].rsplit("/", 1)[-1] != "000-course-overview.md":
                        self.summary.chapters_removed.append(url)
        # Empty folders are only removed beneath this crawler's dedicated root.
        if self.content_dir.exists():
            for folder in sorted(self.content_dir.rglob("*"), reverse=True):
                if folder.is_dir() and not any(folder.iterdir()):
                    folder.rmdir()

    @staticmethod
    def normalized_for_link_check(markdown: str) -> str:
        """Ignore only Markdown link destinations when comparing live/output text."""
        without_targets = re.sub(r"\]\([^)]*\)", "]", markdown)
        return re.sub(r"\s+", " ", without_targets).strip()

    def verify(self, manifest: dict[str, Any], spot_checks: dict[str, str]) -> None:
        collections = manifest_collections(manifest)
        page_paths = [page["relative_path"] for collection in collections for page in collection_pages(collection)]
        expected_paths: list[str] = []
        for collection_index, collection in enumerate(collections, 1):
            folder = self.adapter.collection_folder(collection_index, collection["title"])
            discovered = DiscoveredCollection(collection["url"], collection["title"], None, [])
            if collection.get("overview"):
                page = collection["overview"]
                discovered_page = DiscoveredPage(page["url"], page["title"], "", page.get("kind", "overview"))
                expected_paths.append(self.adapter.page_relative_path(collection_index, discovered, 0, discovered_page, folder))
            for page_index, page in enumerate(collection.get("pages", collection.get("chapters", [])), 1):
                discovered_page = DiscoveredPage(page["url"], page["title"], "", page.get("kind", "page"))
                expected_paths.append(self.adapter.page_relative_path(collection_index, discovered, page_index, discovered_page, folder))
        spot_results = []
        page_lookup = {
            page["url"]: page
            for collection in collections
            for page in collection_pages(collection)
        }
        for url, live_markdown in spot_checks.items():
            page = page_lookup[url]
            output_markdown = (self.output_dir / page["relative_path"]).read_text(encoding="utf-8")
            spot_results.append(
                {
                    "url": url,
                    "content_matches_live_ignoring_local_link_targets": (
                        self.normalized_for_link_check(live_markdown)
                        == self.normalized_for_link_check(output_markdown)
                    ),
                    "title_present": f"# {page['title']}" in output_markdown,
                }
            )
        chapter_count = sum(
            1
            for collection in collections
            for page in collection.get("pages", collection.get("chapters", []))
            if page.get("kind", "chapter") == "chapter"
        )
        self.summary.verification = {
            "collection_count_matches_manifest": len(collections) == self.summary.collections_discovered,
            "page_count_matches_manifest": len(page_paths) == self.summary.pages_discovered,
            "course_count_matches_manifest": len(collections) == self.summary.courses_discovered if self.adapter.name == "openalgo" else None,
            "chapter_count_matches_manifest": self.summary.chapters_discovered == chapter_count if self.adapter.name == "openalgo" else None,
            "paper_count_matches_manifest": len(collections) == self.summary.papers_discovered if self.adapter.name == "arxiv" else None,
            "all_markdown_files_exist": all((self.output_dir / path).is_file() for path in page_paths),
            "consistent_file_naming": page_paths == expected_paths,
            "spot_checks": spot_results,
        }

    def rewrite_internal_links(self, manifest: dict[str, Any]) -> int:
        """Turn links between discovered Markdown pages into portable relatives.

        Crawl4AI remains responsible for HTML-to-Markdown conversion. This small
        post-processing step only changes links whose destinations are also in
        this mirror; external/source links stay intact.
        """
        url_paths = {
            page["url"]: page["relative_path"]
            for collection in manifest_collections(manifest)
            for page in collection_pages(collection)
        }
        changed_files = 0
        link_pattern = re.compile(r"\]\((https?://[^\s)]+)(\s+\"[^)]*\")?\)")
        for source_relative in url_paths.values():
            source = self.output_dir / source_relative
            if not source.exists():
                continue
            original = source.read_text(encoding="utf-8")

            def replacement(match: re.Match[str]) -> str:
                raw_url, title = match.group(1), match.group(2) or ""
                parsed = urlsplit(raw_url)
                target_relative = url_paths.get(canonical_url(raw_url))
                if target_relative is None:
                    return match.group(0)
                relative = Path(os.path.relpath(self.output_dir / target_relative, source.parent)).as_posix()
                return f"]({relative}{'#' + parsed.fragment if parsed.fragment else ''}{title})"

            rewritten = link_pattern.sub(replacement, original)
            if rewritten != original:
                source.write_text(rewritten, encoding="utf-8")
                changed_files += 1
        return changed_files

    def materialize_page(
        self,
        collection_index: int,
        collection: DiscoveredCollection,
        page_index: int,
        page: DiscoveredPage,
        folder: str,
        old_pages: dict[str, dict[str, Any]],
        resume_completed: dict[str, dict[str, Any]],
        spot_checks: dict[str, str],
    ) -> PageRecord | None:
        relative_path = self.adapter.page_relative_path(collection_index, collection, page_index, page, folder)
        current = self.page_record(page.url, page.title, relative_path, page.markdown, page.kind)
        if page.kind != "overview" and len(spot_checks) < 2:
            spot_checks[current.url] = page.markdown
        saved = resume_completed.get(current.url)
        if (
            saved
            and saved.get("content_hash") == current.content_hash
            and saved.get("relative_path") == relative_path
            and (self.output_dir / relative_path).is_file()
        ):
            self.summary.pages_resumed += 1
            self.summary.skipped.append({"url": current.url, "reason": "resumed_from_checkpoint"})
            return current
        self.write_page(current, page.markdown, old_pages)
        self.state["completed"][current.url] = asdict(current)
        self.checkpoint()
        return current

    async def run(self) -> RunSummary:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.content_dir.mkdir(parents=True, exist_ok=True)
        old_manifest = self.load_json(self.meta_dir / MANIFEST_FILE_NAME, {"collections": []})
        old_pages = {
            page["url"]: page
            for collection in manifest_collections(old_manifest)
            for page in collection_pages(collection)
            if page
        }
        previous_state = self.load_json(self.meta_dir / STATE_FILE_NAME, {})
        saved_completed = previous_state.get("completed", {})
        resume_completed = saved_completed if previous_state.get("status") == "running" and isinstance(saved_completed, dict) else {}
        self.state = {
            "status": "running",
            "started_at": self.now(),
            "source_url": self.start_url,
            "adapter": self.adapter.name,
            "completed": resume_completed,
        }
        self.checkpoint()

        browser = BrowserConfig(headless=True, verbose=False)
        manifest_entries: list[dict[str, Any]] = []
        spot_checks: dict[str, str] = {}
        try:
            async with AsyncWebCrawler(config=browser) as crawler:
                discovered = await self.adapter.discover(self, crawler, self.start_url, self.max_depth)
                self.summary.collections_discovered = len(discovered)
                self.summary.pages_discovered = sum(len(collection.pages) + (1 if collection.overview else 0) for collection in discovered)
                if self.adapter.name == "openalgo":
                    self.summary.courses_discovered = len(discovered)
                    self.summary.chapters_discovered = sum(sum(page.kind == "chapter" for page in collection.pages) for collection in discovered)
                elif self.adapter.name == "arxiv":
                    self.summary.papers_discovered = len(discovered)
                self.state["discovered"] = {
                    "collections": [
                        {
                            "url": collection.url,
                            "title": collection.title,
                            "page_urls": [page.url for page in collection.pages],
                        }
                        for collection in discovered
                    ]
                }
                self.checkpoint()

                old_collection_urls = {collection["url"] for collection in manifest_collections(old_manifest)}
                for collection_index, collection in enumerate(discovered, 1):
                    folder = self.adapter.collection_folder(collection_index, collection.title)
                    if collection.url not in old_collection_urls:
                        self.summary.collections_new.append(collection.url)
                        if self.adapter.name == "openalgo":
                            self.summary.courses_new.append(collection.url)
                        elif self.adapter.name == "arxiv":
                            self.summary.papers_new.append(collection.url)
                    entry: dict[str, Any] = {
                        "url": collection.url,
                        "title": collection.title,
                        "relative_path": f"{self.adapter.output_dir_name}/{folder}",
                        "overview": None,
                        "pages": [],
                    }
                    if collection.overview:
                        page = collection.overview
                        record = self.materialize_page(collection_index, collection, 0, page, folder, old_pages, resume_completed, spot_checks)
                        if record:
                            entry["overview"] = asdict(record)
                    for page_index, page in enumerate(collection.pages, 1):
                        record = self.materialize_page(collection_index, collection, page_index, page, folder, old_pages, resume_completed, spot_checks)
                        if record:
                            entry["pages"].append(asdict(record))
                    manifest_entries.append(entry)

            manifest = {
                "adapter": self.adapter.name,
                "source_url": self.start_url,
                "generated_at": self.now(),
                "collections": manifest_entries,
            }
            self.prune_removed(old_manifest, manifest)
            rewritten_files = self.rewrite_internal_links(manifest)
            self.verify(manifest, spot_checks)
            self.summary.verification["files_with_local_link_rewrites"] = rewritten_files
            self.atomic_json(self.meta_dir / MANIFEST_FILE_NAME, manifest)
            self.summary.status = "success" if not self.summary.errors else "partial_success"
        except Exception as exc:
            self.summary.status = "failed"
            self.summary.errors.append({"url": self.start_url, "error": str(exc)})
        finally:
            self.state["status"] = self.summary.status
            self.state["finished_at"] = self.now()
            self.summary.completed_at = self.now()
            self.checkpoint()
        return self.summary


# Generic name for new integrations; the historical class name remains for
# callers that already import it.
SourceCrawler = OpenVarsityCrawler


async def crawl_openvarsity(
    output_dir: str | Path,
    start_url: str = DEFAULT_START_URL,
    max_depth: int = 2,
    retries: int = 3,
    concurrency: int = 8,
) -> dict[str, Any]:
    """Backward-compatible OpenAlgo entry point (the default adapter)."""
    return await crawl_source(output_dir, "openalgo", start_url, max_depth, retries, concurrency)


async def crawl_source(
    output_dir: str | Path,
    source: str = "openalgo",
    start_url: str | None = None,
    max_depth: int | None = None,
    retries: int = 3,
    concurrency: int = 8,
) -> dict[str, Any]:
    """Run any registered source adapter and return a JSON-serialisable summary."""
    resolved_source = source.lower()
    try:
        adapter = get_adapter(resolved_source)
        resolved_url = start_url or adapter.default_start_url
        if not resolved_url:
            raise ValueError("start_url is required for the arxiv adapter (use an arxiv.org/html/<paper-id>[vN] URL)")
        resolved_depth = adapter.default_max_depth if max_depth is None else max_depth
        summary = await OpenVarsityCrawler(
            Path(output_dir), resolved_url, resolved_depth, retries, concurrency, adapter
        ).run()
        return asdict(summary)
    except Exception as exc:
        now = datetime.now(timezone.utc).isoformat()
        return asdict(
            RunSummary(
                started_at=now,
                completed_at=now,
                status="failed",
                adapter=resolved_source,
                source_url=canonical_url(start_url) if start_url else "",
                errors=[{"url": canonical_url(start_url) if start_url else "", "error": str(exc)}],
            )
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Crawl a registered learning/research source into structured Markdown.")
    # Do not use argparse choices here: an unknown adapter must still produce
    # the same structured JSON failure that every other agent input receives.
    parser.add_argument(
        "--source",
        default="openalgo",
        help=f"Source adapter (default: openalgo; available: {', '.join(sorted(ADAPTERS))}).",
    )
    parser.add_argument("--output", type=Path, required=True, help="Directory to receive the selected adapter's content and state.")
    parser.add_argument("--start-url", default=None, help="Source URL. Required for arxiv; defaults to Open Varsity for openalgo.")
    parser.add_argument("--max-depth", type=int, default=None, help="Maximum discovery depth (OpenAlgo defaults to 2; arXiv defaults to 0).")
    parser.add_argument("--retries", type=int, default=3, help="Crawl4AI transient/anti-bot retry rounds per page.")
    parser.add_argument("--concurrency", type=int, default=8, help="Maximum simultaneous chapter fetches.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = asyncio.run(crawl_source(args.output, args.source, args.start_url, args.max_depth, args.retries, args.concurrency))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["status"] in {"success", "partial_success"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
