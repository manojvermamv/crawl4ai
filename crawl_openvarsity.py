#!/usr/bin/env python3
"""Agent-callable crawler for the OpenAlgo Open Varsity learning catalogue.

The program deliberately discovers the catalogue on every run.  It never embeds
course names, course slugs, chapter names, or chapter counts.
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
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable
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


def validate_request(start_url: str, max_depth: int, retries: int, concurrency: int) -> None:
    """Keep the public interface inside the single supported learning scope."""
    if canonical_url(start_url) != DEFAULT_START_URL:
        raise ValueError(f"start_url must be {DEFAULT_START_URL}")
    if max_depth < 2:
        raise ValueError("max_depth must be at least 2 for landing → course → chapter discovery")
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
    courses_removed: list[str] = field(default_factory=list)
    chapters_new: list[str] = field(default_factory=list)
    chapters_changed: list[str] = field(default_factory=list)
    chapters_removed: list[str] = field(default_factory=list)
    skipped: list[dict[str, str]] = field(default_factory=list)
    errors: list[dict[str, str]] = field(default_factory=list)
    verification: dict[str, Any] = field(default_factory=dict)


class OpenVarsityCrawler:
    def __init__(
        self,
        output_dir: Path,
        start_url: str = DEFAULT_START_URL,
        max_depth: int = 2,
        retries: int = 3,
        concurrency: int = 8,
    ) -> None:
        validate_request(start_url, max_depth, retries, concurrency)
        self.output_dir = output_dir.resolve()
        self.content_dir = self.output_dir / "courses"
        self.meta_dir = self.output_dir / ".openvarsity"
        self.start_url = canonical_url(start_url)
        self.max_depth = max_depth
        self.retries = retries
        self.concurrency = max(1, concurrency)
        self.summary = RunSummary(started_at=self.now(), source_url=self.start_url)
        self.state: dict[str, Any] = {}

    @staticmethod
    def now() -> str:
        return datetime.now(UTC).isoformat()

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
            excluded_tags=["nav", "footer"],
            excluded_selector="header.sticky",
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

    def page_record(self, url: str, title: str, relative_path: str, markdown: str) -> PageRecord:
        return PageRecord(
            url=canonical_url(url),
            title=title,
            relative_path=relative_path,
            content_hash=hashlib.sha256(markdown.encode("utf-8")).hexdigest(),
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
        else:
            self.summary.pages_new.append(record.url)
        return True

    def prune_removed(self, old_manifest: dict[str, Any], manifest: dict[str, Any]) -> None:
        old_courses = {course["url"]: course for course in old_manifest.get("courses", [])}
        new_courses = {course["url"]: course for course in manifest.get("courses", [])}
        for url, course in old_courses.items():
            if url not in new_courses:
                self.summary.courses_removed.append(url)
        old_pages = {
            page["url"]: page
            for course in old_manifest.get("courses", [])
            for page in [course.get("overview", {})] + course.get("chapters", [])
            if page
        }
        new_pages = {
            page["url"]: page
            for course in manifest.get("courses", [])
            for page in [course.get("overview", {})] + course.get("chapters", [])
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
                    if page["relative_path"].rsplit("/", 1)[-1] != "000-course-overview.md":
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
        courses = manifest.get("courses", [])
        chapter_paths = [page["relative_path"] for course in courses for page in course["chapters"]]
        all_paths = [course["overview"]["relative_path"] for course in courses] + chapter_paths
        expected_paths = [
            f"courses/{index:03d}-{slugify(course['title'], 'course')}/{chapter_index:03d}-{slugify(page['title'], 'chapter')}.md"
            for index, course in enumerate(courses, 1)
            for chapter_index, page in enumerate(course["chapters"], 1)
        ]
        spot_results = []
        page_lookup = {
            page["url"]: page
            for course in courses
            for page in [course["overview"]] + course["chapters"]
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
        self.summary.verification = {
            "course_count_matches_manifest": len(courses) == self.summary.courses_discovered,
            "chapter_count_matches_manifest": len(chapter_paths) == self.summary.chapters_discovered,
            "all_markdown_files_exist": all((self.output_dir / path).is_file() for path in all_paths),
            "consistent_file_naming": chapter_paths == expected_paths,
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
            for course in manifest["courses"]
            for page in [course["overview"]] + course["chapters"]
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

    async def run(self) -> RunSummary:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.content_dir.mkdir(parents=True, exist_ok=True)
        old_manifest = self.load_json(self.meta_dir / MANIFEST_FILE_NAME, {"courses": []})
        old_pages = {
            page["url"]: page
            for course in old_manifest.get("courses", [])
            for page in [course.get("overview", {})] + course.get("chapters", [])
            if page
        }
        previous_state = self.load_json(self.meta_dir / STATE_FILE_NAME, {})
        resume_completed = previous_state.get("completed", {}) if previous_state.get("status") == "running" else {}
        self.state = {"status": "running", "started_at": self.now(), "source_url": self.start_url, "completed": resume_completed}
        self.checkpoint()

        browser = BrowserConfig(headless=True, verbose=False)
        manifest_courses: list[CourseRecord] = []
        spot_checks: dict[str, str] = {}
        try:
            async with AsyncWebCrawler(config=browser) as crawler:
                landing = await self.fetch(crawler, self.start_url, depth=0)
                if landing is None:
                    raise RuntimeError("The Open Varsity landing page could not be fetched.")
                candidate_courses = discover_course_urls(page_html(landing), self.start_url)
                if not candidate_courses:
                    raise RuntimeError("No course links were discovered from the Open Varsity landing page.")

                # Course page validation prevents header/footer/unrelated landing links
                # from entering the content tree.
                discovered_courses: list[tuple[str, str, list[str], str]] = []
                course_results = await self.fetch_many(crawler, candidate_courses, depth=1)
                for course_url in candidate_courses:
                    course_result = course_results.get(course_url)
                    if course_result is None:
                        continue
                    course_html = page_html(course_result)
                    chapters = discover_chapter_urls(course_html, course_url, self.start_url)
                    if not chapters:
                        self.summary.skipped.append({"url": course_url, "reason": "not_a_course_page"})
                        continue
                    discovered_courses.append((course_url, page_title(course_html, course_url), chapters, markdown_value(course_result)))

                self.summary.courses_discovered = len(discovered_courses)
                self.summary.chapters_discovered = sum(len(chapters) for _, _, chapters, _ in discovered_courses)
                self.state["discovered"] = {
                    "courses": [
                        {"url": url, "title": title, "chapter_urls": chapters}
                        for url, title, chapters, _ in discovered_courses
                    ]
                }
                self.checkpoint()

                old_course_urls = {course["url"] for course in old_manifest.get("courses", [])}
                for course_index, (course_url, course_title, chapter_urls, course_markdown) in enumerate(discovered_courses, 1):
                    course_folder = f"{course_index:03d}-{slugify(course_title, 'course')}"
                    if course_url not in old_course_urls:
                        self.summary.courses_new.append(course_url)
                    # Course pages are first-class discovered content, saved at a
                    # stable index path before their chapter files.
                    overview = self.page_record(
                        course_url,
                        course_title,
                        f"courses/{course_folder}/000-course-overview.md",
                        course_markdown,
                    )
                    self.write_page(overview, course_markdown, old_pages)
                    self.state["completed"][course_url] = asdict(overview)
                    self.checkpoint()
                    chapter_records: list[PageRecord] = []
                    pending_chapters: list[str] = []
                    for chapter_index, chapter_url in enumerate(chapter_urls, 1):
                        saved = resume_completed.get(chapter_url)
                        expected_prefix = f"courses/{course_folder}/{chapter_index:03d}-"
                        if saved and str(saved.get("relative_path", "")).startswith(expected_prefix) and (self.output_dir / saved["relative_path"]).is_file():
                            record = PageRecord(**saved)
                            chapter_records.append(record)
                            self.summary.pages_resumed += 1
                            self.summary.skipped.append({"url": chapter_url, "reason": "resumed_from_checkpoint"})
                            continue
                        pending_chapters.append(chapter_url)
                    chapter_results = await self.fetch_many(crawler, pending_chapters, depth=2)
                    for chapter_index, chapter_url in enumerate(chapter_urls, 1):
                        if any(record.url == chapter_url for record in chapter_records):
                            continue
                        result = chapter_results.get(chapter_url)
                        if result is None:
                            continue
                        markdown = markdown_value(result)
                        html = page_html(result)
                        title = page_title(html, f"Chapter {chapter_index}")
                        relative_path = f"courses/{course_folder}/{chapter_index:03d}-{slugify(title, 'chapter')}.md"
                        record = self.page_record(chapter_url, title, relative_path, markdown)
                        if course_index <= 2 and chapter_index == 1:
                            spot_checks[record.url] = markdown
                        changed = self.write_page(record, markdown, old_pages)
                        if changed:
                            if record.url in old_pages:
                                self.summary.chapters_changed.append(record.url)
                            else:
                                self.summary.chapters_new.append(record.url)
                        chapter_records.append(record)
                        self.state["completed"][chapter_url] = asdict(record)
                        self.checkpoint()
                    manifest_courses.append(
                        CourseRecord(course_url, course_title, f"courses/{course_folder}", overview, chapter_records)
                    )

            manifest = {
                "source_url": self.start_url,
                "generated_at": self.now(),
                "courses": [asdict(course) for course in manifest_courses],
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


async def crawl_openvarsity(
    output_dir: str | Path,
    start_url: str = DEFAULT_START_URL,
    max_depth: int = 2,
    retries: int = 3,
    concurrency: int = 8,
) -> dict[str, Any]:
    """Importable, JSON-serialisable entry point for an AI agent or scheduler."""
    try:
        summary = await OpenVarsityCrawler(Path(output_dir), start_url, max_depth, retries, concurrency).run()
        return asdict(summary)
    except Exception as exc:
        now = datetime.now(UTC).isoformat()
        return asdict(
            RunSummary(
                started_at=now,
                completed_at=now,
                status="failed",
                source_url=canonical_url(start_url),
                errors=[{"url": canonical_url(start_url), "error": str(exc)}],
            )
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mirror OpenAlgo's live Open Varsity catalogue as Markdown.")
    parser.add_argument("--output", type=Path, required=True, help="Directory to receive courses/ and .openvarsity/ state.")
    parser.add_argument("--start-url", default=DEFAULT_START_URL, help="Open Varsity landing page URL.")
    parser.add_argument("--max-depth", type=int, default=2, help="Maximum discovery depth; 2 covers landing, course, chapter.")
    parser.add_argument("--retries", type=int, default=3, help="Crawl4AI transient/anti-bot retry rounds per page.")
    parser.add_argument("--concurrency", type=int, default=8, help="Maximum simultaneous chapter fetches.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary = asyncio.run(crawl_openvarsity(args.output, args.start_url, args.max_depth, args.retries, args.concurrency))
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["status"] in {"success", "partial_success"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
