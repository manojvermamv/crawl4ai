# Open Varsity Markdown crawler

This is a portable, agent-callable mirror for the OpenAlgo **Open Varsity** learning catalogue.  It uses [Crawl4AI](https://github.com/unclecode/crawl4ai) for JavaScript rendering, robots.txt checks, retries, and HTML-to-Markdown conversion.

It discovers the live hierarchy on every run:

1. `https://openalgo.in/learn` discovers course cards.
2. Each live course page discovers its ordered chapter links.
3. Only those discovered chapter pages are converted and written.

No course name, course slug, chapter name, chapter count, or page list is configured in the code. Links to other site sections and other subdomains never enter the output scope.

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
  "courses_discovered": 0,
  "chapters_discovered": 0,
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
from crawl_openvarsity import crawl_openvarsity

summary = await crawl_openvarsity("./open-varsity")
```

## Regression tests

The tests run entirely offline—no browser, network, or existing mirror is required:

```bash
python -m unittest discover -s tests -v
```

They cover scope leakage, ordering, future label variations, out-of-order Crawl4AI batches, update/no-op behavior, safe pruning, local-link/image handling, and structured errors for invalid agent inputs.

The included [cross-platform CI workflow](.github/workflows/cross-platform.yml)
runs this suite on current Windows, Linux, and macOS runners for every push or
pull request. It does not claim native iOS support; iOS uses the remote-runner
pattern described above.

## Output and updates

Every course has the same layout, in live landing-page order:

```text
open-varsity/
  courses/
    001-course-title/
      000-course-overview.md
      001-chapter-title.md
      002-chapter-title.md
  .openvarsity/
    manifest.json
    crawl-state.json
    latest-run.json
```

`manifest.json` is the previous successful source-of-truth. The next run always performs discovery again, writes only pages whose Crawl4AI Markdown hash changed, reports additions/removals, and safely prunes managed files for removed chapters. `crawl-state.json` is checkpointed after discovery and after every converted page, so an interrupted job has durable progress and its next invocation can continue without losing completed work.

The report's `verification` section checks that the live-discovered counts equal the manifest counts, every discovered course/chapter Markdown file exists, and every path follows the course/chapter naming convention. It also emits two live chapter URLs for an agent to spot-check against the generated Markdown.
