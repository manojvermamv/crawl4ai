# Source-adapter architecture

The crawler has one persistence and execution engine with a small, explicit
adapter boundary.  This keeps the default OpenAlgo behaviour stable while
allowing another source to define its own URL rules and hierarchy without
copying the Crawl4AI, checkpoint, or reporting code.

```text
agent / CLI
    |
    v
crawl_source(output, source, start_url, controls)
    |
    +-- adapter registry: openalgo (default) | arxiv | future adapters
    |
    +-- shared OpenVarsityCrawler runner
          +-- Crawl4AI: browser rendering, Markdown, robots, retries
          +-- adapter.discover(): live source graph -> collections/pages
          +-- path policy: adapter.page_relative_path()
          +-- hashes, atomic writes, resume checkpoints, safe pruning
          +-- local-link rewrite and verification
          +-- JSON RunSummary for the calling agent
```

## Responsibilities

`SourceAdapter` is the extension contract.  Each adapter owns:

- start-URL validation and an exact `url_allowed()` scope predicate;
- live discovery of collections and ordered pages;
- source-specific Crawl4AI exclusions; and
- deterministic collection and page paths.

The shared runner owns everything that should behave consistently across
sources: Crawl4AI configuration, robots.txt compliance, retry handling,
depth checks, out-of-order batch mapping, resumable state, content hashes,
atomic JSON, path-safe removal, local links, and verification.  An adapter
must return `DiscoveredCollection` objects and must not write files itself.

The link pass normalizes both original absolute URLs and Crawl4AI-generated
relative filenames against the discovered manifest. This keeps generated
course navigation portable even when the converter adds a title or course
suffix to a relative destination.

Crawl4AI also handles HTML-to-Markdown media conversion.  Charts and other
images are retained as Markdown image links with their source URL/alt text;
the crawler does not download or reinterpret binary assets.  Thus the
Markdown remains portable while image delivery stays with the original site.

The generic manifest uses this shape (the legacy OpenAlgo `courses` /
`chapters` shape is read and upgraded automatically):

```json
{
  "adapter": "openalgo",
  "source_url": "https://openalgo.in/learn",
  "collections": [
    {
      "url": "…",
      "title": "…",
      "relative_path": "courses/001-…",
      "overview": {"url": "…", "relative_path": "…", "content_hash": "…"},
      "pages": [{"url": "…", "relative_path": "…", "content_hash": "…"}]
    }
  ]
}
```

## Current adapters

### OpenAlgo (default)

The adapter discovers the landing page, course cards, and each course's
chapter links on every invocation.  It requires depth 2 because that is the
landing → course → chapter graph.  Content is namespaced under `courses/` and
state under `.openvarsity/`.  Its allow-list rejects the unrelated
`/features`, `/download`, `/blog`, `/faq`, and `/roadmap` sections and all
other hosts (including `docs.openalgo.in`) before a page can be fetched.

### arXiv HTML

The arXiv adapter accepts only canonical `https://arxiv.org/html/...` paper
URLs.  Its exact allow-list recognizes modern identifiers such as
`2608.31041v1` and legacy category identifiers such as `hep-th/9901001v2`.
`/pdf`, `/abs`, `/src`, `export.arxiv.org`, query/fragment variants, and every
other host or path are rejected before Crawl4AI sees them.  It follows only
links that pass the same predicate, so PDF downloads are never crawled.

A single paper is the safe default crawl (`--max-depth 0`, including when the
agent omits `max_depth`). Callers may explicitly raise the depth to follow
links to additional HTML papers. Output is
namespaced under `papers/` and state under `.arxiv/`; each discovered paper is
one collection containing one Markdown page.

```bash
# OpenAlgo remains the default
python crawl_openvarsity.py --output ./open-varsity

# Opt-in arXiv HTML crawl; only this paper at depth zero
python crawl_openvarsity.py \
  --source arxiv \
  --start-url https://arxiv.org/html/2608.31041v1 \
  --max-depth 0 \
  --output ./arxiv-mirror
```

The arXiv page used to design this boundary is a real HTML rendering with
section links and a separate “Download PDF” link; the adapter deliberately
keeps the former and excludes the latter.  Its discussion of sequential,
hierarchical, iterative, coordinated, and adaptive agentic systems is also a
useful design cue: discovery is source-specific, while durable state and
evaluation remain shared and inspectable.

## Adding a future adapter

1. Subclass `SourceAdapter` and register one instance in `ADAPTERS`.
2. Implement URL validation, the exact allow-list, live `discover()`, and
   `page_relative_path()`; do not add source names or page counts to the
   runner.
3. Add offline tests for allowed/rejected URLs, discovery ordering, path
   conventions, and a structured failure case.
4. Run the same CLI/importable function and inspect the adapter's namespaced
   manifest and `RunSummary.verification` fields.

This preserves a single agent-callable interface while keeping source policy
isolated and portable on Windows, Linux, and macOS.  iOS/iPadOS remains a
client platform: invoke the same runner on a supported host and consume its
JSON result and Markdown output remotely.
