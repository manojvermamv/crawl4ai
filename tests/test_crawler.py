"""Offline regression tests for crawler behaviour an agent or end user relies on."""

from __future__ import annotations

import asyncio
import json
import subprocess
import sys
import tempfile
import unittest
from dataclasses import asdict
from pathlib import Path
from types import SimpleNamespace

from bootstrap import virtualenv_python
from crawl_openvarsity import (
    CourseRecord,
    OpenVarsityCrawler,
    PageRecord,
    canonical_url,
    crawl_openvarsity,
    discover_chapter_urls,
    discover_course_urls,
    markdown_value,
)


class DiscoveryScenariosTest(unittest.TestCase):
    def test_course_cards_preserve_order_and_exclude_navigation_external_and_mission_links(self) -> None:
        html = """
        <main>
          <a href='/learn/mission'>Our mission</a>
          <a href='/features'>Features</a>
          <a href='https://docs.openalgo.in'>Docs</a>
          <a href='/first'><h2>First</h2><p>18 chapters</p><span>Start the course</span></a>
          <a href='/second'><h2>Second</h2><p>4 chapters</p><span>Start the course</span></a>
        </main>
        """
        self.assertEqual(
            discover_course_urls(html, "https://openalgo.in/learn"),
            ["https://openalgo.in/first", "https://openalgo.in/second"],
        )

    def test_course_discovery_has_a_markup_change_fallback(self) -> None:
        html = """
        <main>
          <section><p>12 chapters in this course</p><a href='/changed-card'>Read now</a></section>
        </main>
        """
        self.assertEqual(discover_course_urls(html, "https://openalgo.in/learn"), ["https://openalgo.in/changed-card"])

    def test_chapter_discovery_excludes_course_landing_duplicates_and_unrelated_links(self) -> None:
        html = """
        <main>
          <a href='/first'>Course overview</a>
          <a href='/first/one'>01 First chapter</a>
          <a href='/first/two'>Chapter 02 Second chapter</a>
          <a href='/blog'>Blog</a>
          <a href='/first/one'>01 First chapter</a>
        </main>
        """
        self.assertEqual(
            discover_chapter_urls(html, "https://openalgo.in/first", "https://openalgo.in/learn"),
            ["https://openalgo.in/first/one", "https://openalgo.in/first/two"],
        )

    def test_chapter_discovery_handles_future_non_numbered_chapter_labels(self) -> None:
        html = """
        <main><section><h2>Course chapters</h2>
          <a href='/first/intro'>Introduction</a><a href='/first/next'>Next lesson</a>
        </section></main>
        """
        self.assertEqual(
            discover_chapter_urls(html, "https://openalgo.in/first", "https://openalgo.in/learn"),
            ["https://openalgo.in/first/intro", "https://openalgo.in/first/next"],
        )

    def test_url_identity_drops_fragments_queries_and_trailing_slashes(self) -> None:
        self.assertEqual(canonical_url("HTTPS://OpenAlgo.in/stocks/?from=x#chapter-1"), "https://openalgo.in/stocks")

    def test_crawl4ai_markdown_result_variants_are_supported(self) -> None:
        result = SimpleNamespace(markdown=SimpleNamespace(fit_markdown="# A page"))
        self.assertEqual(markdown_value(result), "# A page\n")

    def test_bootstrap_uses_the_correct_virtualenv_interpreter_on_windows_and_unix(self) -> None:
        self.assertEqual(virtualenv_python(Path("runtime"), is_windows=True).as_posix(), "runtime/Scripts/python.exe")
        self.assertEqual(virtualenv_python(Path("runtime"), is_windows=False).as_posix(), "runtime/bin/python")


class FakeCrawler:
    def __init__(self, results: list[SimpleNamespace]) -> None:
        self.results = results

    async def arun_many(self, urls: list[str], config: object) -> list[SimpleNamespace]:
        # Crawl4AI can return completed results in a different order than input.
        return self.results


class PersistenceAndAgentScenariosTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.app = OpenVarsityCrawler(self.root)

    def tearDown(self) -> None:
        self.temp.cleanup()

    @staticmethod
    def record(url: str, relative_path: str, markdown: str = "# page\n") -> PageRecord:
        return PageRecord(url=url, title="Page", relative_path=relative_path, content_hash="hash-" + markdown)

    def manifest(self, overview: PageRecord, chapters: list[PageRecord]) -> dict[str, object]:
        return {
            "courses": [
                asdict(CourseRecord("https://openalgo.in/course", "Course", "courses/001-course", overview, chapters))
            ]
        }

    def test_batch_fetch_maps_out_of_order_results_by_returned_url(self) -> None:
        first = "https://openalgo.in/first"
        second = "https://openalgo.in/second"
        fake = FakeCrawler([SimpleNamespace(url=second, success=True), SimpleNamespace(url=first, success=True)])
        mapped = asyncio.run(self.app.fetch_many(fake, [first, second], depth=2))
        self.assertEqual(list(mapped), [second, first])
        self.assertEqual(self.app.summary.pages_fetched, 2)

    def test_unchanged_page_is_not_rewritten(self) -> None:
        record = self.record("https://openalgo.in/course/one", "courses/001-course/001-page.md")
        self.assertTrue(self.app.write_page(record, "# page\n", {}))
        self.assertFalse(self.app.write_page(record, "# page\n", {record.url: asdict(record)}))
        self.assertEqual(self.app.summary.pages_written, 1)
        self.assertEqual(self.app.summary.pages_unchanged, 1)

    def test_known_internal_links_become_local_but_images_and_external_links_remain_remote(self) -> None:
        overview = self.record("https://openalgo.in/course", "courses/001-course/000-course-overview.md")
        chapter = self.record("https://openalgo.in/course/one", "courses/001-course/001-page.md")
        source = self.root / overview.relative_path
        source.parent.mkdir(parents=True)
        source.write_text(
            "[chapter](https://openalgo.in/course/one#part)\n"
            "[external](https://example.org/page)\n"
            "![chart](https://openalgo.in/course/images/chart.png)\n",
            encoding="utf-8",
        )
        (self.root / chapter.relative_path).write_text("# Page\n", encoding="utf-8")
        self.assertEqual(self.app.rewrite_internal_links(self.manifest(overview, [chapter])), 1)
        converted = source.read_text(encoding="utf-8")
        self.assertIn("](001-page.md#part)", converted)
        self.assertIn("https://example.org/page", converted)
        self.assertIn("https://openalgo.in/course/images/chart.png", converted)

    def test_pruning_only_removes_managed_content(self) -> None:
        overview = self.record("https://openalgo.in/course", "courses/001-course/000-course-overview.md")
        chapter = self.record("https://openalgo.in/course/one", "courses/001-course/001-page.md")
        for record in (overview, chapter):
            target = self.root / record.relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("managed", encoding="utf-8")
        unrelated = self.root / "unrelated.md"
        unrelated.write_text("keep", encoding="utf-8")
        self.app.prune_removed(self.manifest(overview, [chapter]), {"courses": []})
        self.assertFalse((self.root / chapter.relative_path).exists())
        self.assertTrue(unrelated.exists())
        self.assertIn(chapter.url, self.app.summary.chapters_removed)

    def test_agent_invalid_request_returns_a_structured_failure_not_a_traceback(self) -> None:
        summary = asyncio.run(crawl_openvarsity(self.root, max_depth=1))
        self.assertEqual(summary["status"], "failed")
        self.assertIn("max_depth", summary["errors"][0]["error"])

    def test_agent_cannot_redirect_the_crawler_to_another_subdomain_or_site_section(self) -> None:
        summary = asyncio.run(crawl_openvarsity(self.root, start_url="https://docs.openalgo.in/"))
        self.assertEqual(summary["status"], "failed")
        self.assertIn("start_url", summary["errors"][0]["error"])

    def test_cli_invalid_request_has_json_only_stdout_and_a_nonzero_exit_code(self) -> None:
        script = Path(__file__).parents[1] / "crawl_openvarsity.py"
        completed = subprocess.run(
            [sys.executable, str(script), "--output", str(self.root / "out"), "--max-depth", "1"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(completed.stderr, "")
        payload = json.loads(completed.stdout)
        self.assertEqual(payload["status"], "failed")
