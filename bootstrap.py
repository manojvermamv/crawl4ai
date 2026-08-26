#!/usr/bin/env python3
"""Create the local runtime and browser used by the Open Varsity crawler.

This standard-library-only bootstrap runs on Windows, Linux, and macOS. It
avoids shell activation commands, whose syntax differs between operating systems.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import venv
from pathlib import Path


def virtualenv_python(venv_dir: Path, is_windows: bool | None = None) -> Path:
    """Return the interpreter location for the requested operating system."""
    is_windows = os.name == "nt" if is_windows is None else is_windows
    return venv_dir / ("Scripts/python.exe" if is_windows else "bin/python")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install the portable Open Varsity crawler runtime.")
    parser.add_argument("--venv", type=Path, default=Path(".venv"), help="Virtual-environment directory (default: .venv).")
    parser.add_argument("--skip-browser", action="store_true", help="Install Python packages only; useful on a remote runner with browsers preinstalled.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    venv_dir = args.venv.resolve()
    python = virtualenv_python(venv_dir)
    if not python.exists():
        venv.EnvBuilder(with_pip=True).create(venv_dir)

    subprocess.run([str(python), "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([str(python), "-m", "pip", "install", "-r", str(Path(__file__).with_name("requirements.txt"))], check=True)
    if not args.skip_browser:
        # Playwright chooses the correct Chromium build for Windows, Linux, or
        # macOS. On a minimal Linux host, crawl4ai-doctor reports any missing
        # operating-system libraries after this step.
        subprocess.run([str(python), "-m", "playwright", "install", "chromium"], check=True)

    print(f"Runtime ready: {python}")
    print(f"Run: {python} crawl_openvarsity.py --output open-varsity")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
