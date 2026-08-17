#!/usr/bin/env python3
"""Verify relative links in Markdown files resolve to real files.

Walks every .md file in the repo, extracts [text](target) links, and
checks that any relative (non-http, non-mailto, non-pure-anchor) target
resolves to a real file or directory. Exits non-zero and prints every
broken link found.
"""

import re
import sys
from pathlib import Path
from urllib.parse import unquote

REPO_ROOT = Path(__file__).resolve().parent.parent
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "#")
SKIP_DIRS = {".git", "node_modules"}


def iter_markdown_files():
    for path in REPO_ROOT.rglob("*.md"):
        if not any(part in SKIP_DIRS for part in path.parts):
            yield path


def extract_target(raw: str) -> str:
    target = raw.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    # Drop an optional "title" after the URL, e.g. (path "title")
    target = target.split(" ", 1)[0]
    # Drop an in-file anchor
    target = target.split("#", 1)[0]
    return unquote(target)


def check_file(md_file: Path):
    broken = []
    text = md_file.read_text(encoding="utf-8", errors="ignore")
    for match in LINK_RE.finditer(text):
        raw = match.group(1)
        if raw.strip().startswith(SKIP_PREFIXES):
            continue
        target = extract_target(raw)
        if not target:
            continue
        resolved = (md_file.parent / target).resolve()
        if not resolved.exists():
            broken.append((raw, resolved))
    return broken


def main():
    total_links_checked = 0
    failures = []
    for md_file in sorted(iter_markdown_files()):
        broken = check_file(md_file)
        total_links_checked += 1
        for raw, resolved in broken:
            failures.append((md_file.relative_to(REPO_ROOT), raw, resolved))

    if failures:
        print(f"Broken relative links found ({len(failures)}):\n")
        for md_file, raw, resolved in failures:
            print(f"  {md_file}: [{raw}] -> {resolved} (missing)")
        print(f"\nChecked {total_links_checked} Markdown files.")
        sys.exit(1)

    print(f"All relative links resolved OK across {total_links_checked} Markdown files.")


if __name__ == "__main__":
    main()
