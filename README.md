# Open Varsity Markdown crawler

This is a portable, agent-callable mirror for the OpenAlgo **Open Varsity** learning catalogue.  It uses [Crawl4AI](https://github.com/unclecode/crawl4ai) for JavaScript rendering, robots.txt checks, retries, and HTML-to-Markdown conversion.

It discovers the live hierarchy on every run:

1. `https://openalgo.in/learn` discovers course cards.
2. Each live course page discovers its ordered chapter links.
3. Only those discovered chapter pages are converted and written.

No course name, course slug, chapter name, chapter count, or page list is configured in the code. Links to other site sections and other subdomains never enter the output scope.

The runner is adapter-based. OpenAlgo is the default; an opt-in arXiv adapter
crawls only `arxiv.org/html/...` pages (never `/pdf`, `/abs`, `/src`, another
host, or an unrelated path). See the [adapter architecture](ARCHITECTURE.md)
for the extension contract and manifest schema.

## Setup and run

### Windows, Linux, and macOS

Use the platform-neutral bootstrap command; it creates a virtual environment,
installs Python dependencies, and downloads the correct Playwright Chromium.

```bash
python bootstrap.py
```

On Windows, use `py -3 bootstrap.py` if `python` is not on `PATH`. Then run the
command printed by the bootstrap, for example:

```text
# Windows PowerShell
.\.venv\Scripts\python.exe crawl_openvarsity.py --output open-varsity

# Linux/macOS
.venv/bin/python crawl_openvarsity.py --output open-varsity
```

To crawl an arXiv HTML rendering, provide its `/html/` URL explicitly. The
arXiv adapter defaults to depth zero (that paper only); increasing the depth
follows only linked arXiv HTML papers:

```bash
# PowerShell
.\.venv\Scripts\python.exe crawl_openvarsity.py --source arxiv --start-url https://arxiv.org/html/2608.31041v1 --max-depth 0 --output arxiv-mirror

# Linux/macOS
.venv/bin/python crawl_openvarsity.py \
  --source arxiv \
  --start-url https://arxiv.org/html/2608.31041v1 \
  --max-depth 0 \
  --output arxiv-mirror
```

Python 3.10 or newer is required. On a minimal Linux server, run
`.venv/bin/crawl4ai-doctor` after bootstrap and install any OS libraries it
reports; Crawl4AI documents this diagnostic and its Linux setup notes in its
[installation guide](https://docs.crawl4ai.com/core/installation/).

### Manual setup

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
crawl4ai-setup
python crawl_openvarsity.py --output ./open-varsity
```

### iOS / iPadOS

Native iOS is not a supported crawler host: Crawl4AI requires Python plus a
Playwright-managed Chromium browser, which iOS does not provide. Use an iOS
agent as a client of a Windows, Linux, or macOS runner instead—for example, by
having the agent invoke this same CLI over a preconfigured remote command or
automation. The runner returns the same JSON summary and writes the same
portable Markdown output, which the iOS client can read or sync. Do not attempt
to install this crawler directly on an iPhone or iPad.

The command writes its only machine-readable result to stdout as JSON. A zero exit status means the run completed (or completed with page-level errors reported as `partial_success`).

```json
{
  "status": "success",
  "adapter": "openalgo",
  "collections_discovered": 0,
  "pages_discovered": 0,
  "collections_changed": [],
  "courses_discovered": 0,
  "courses_changed": [],
  "chapters_discovered": 0,
  "papers_discovered": 0,
  "papers_changed": [],
  "courses_new": [],
  "chapters_new": [],
  "chapters_changed": [],
  "chapters_removed": [],
  "skipped": [],
  "errors": [],
  "verification": {}
}
```

For Python callers, use the importable async function:

```python
from crawl_openvarsity import crawl_openvarsity, crawl_source

summary = await crawl_openvarsity("./open-varsity")

# Any registered adapter uses the same structured interface.
summary = await crawl_source(
    "./arxiv-mirror",
    source="arxiv",
    start_url="https://arxiv.org/html/2608.31041v1",
    max_depth=0,
)
```

## Regression tests

The tests run entirely offline—no browser, network, or existing mirror is required:

```bash
python -m unittest discover -s tests -v
```

They cover OpenAlgo scope leakage, arXiv HTML-only scope, ordering, future
label variations, out-of-order Crawl4AI batches, update/no-op behavior,
safe pruning, local-link/image handling, and structured errors for invalid
agent inputs.

The included [cross-platform CI workflow](.github/workflows/cross-platform.yml)
runs this suite on current Windows, Linux, and macOS runners for every push or
pull request. It does not claim native iOS support; iOS uses the remote-runner
pattern described above.

## Output and updates

Each adapter has one consistent layout, in live discovery order:

```text
open-varsity/
  courses/                         # OpenAlgo adapter
    001-course-title/
      000-course-overview.md
      001-chapter-title.md
      002-chapter-title.md
  .openvarsity/                     # adapter state and reports
    manifest.json
    crawl-state.json
    latest-run.json

arxiv-mirror/
  papers/                           # arXiv adapter
    001-paper-title/
      001-paper-title.md
  .arxiv/
    manifest.json
    crawl-state.json
    latest-run.json
```

`manifest.json` is the previous successful source-of-truth. The next run always performs discovery again, writes only pages whose Crawl4AI Markdown hash changed, reports additions/removals, and safely prunes managed files for removed collections/pages. `crawl-state.json` is checkpointed after discovery and after every converted page, so an interrupted job has durable progress and its next invocation can continue without losing completed work. Existing OpenAlgo manifests using `courses` and `chapters` are upgraded automatically.

The report's `verification` section checks that live-discovered counts equal
manifest counts, every Markdown file exists, and every path follows the
adapter's naming convention. It also emits spot-check results against live
converted Markdown. `RunSummary` includes generic collection/page changes plus
OpenAlgo-compatible course/chapter aliases and arXiv paper aliases, so an
agent can decide success, partial success, or failure without parsing logs.
