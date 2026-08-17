#!/usr/bin/env python3
"""Verify relative links in Markdown files resolve to real files.

Walks every .md file in the repo, extracts [text](target) links, and
checks that any relative (non-http, non-mailto, non-pure-anchor) target
resolves to a real file or directory.

Known, pre-existing broken links are tracked in tools/known_broken_links.txt
(one "relative/path/to/file.md::raw-target" per line) so that CI can fail
only on *newly introduced* breakage instead of the whole legacy backlog.

Usage:
    python3 tools/check_markdown_links.py                 # check, fail on new breaks
    python3 tools/check_markdown_links.py --update-baseline  # regenerate the baseline
"""

import re
import sys
from pathlib import Path
from urllib.parse import unquote

REPO_ROOT = Path(__file__).resolve().parent.parent
BASELINE_FILE = REPO_ROOT / "tools" / "known_broken_links.txt"

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
SKIP_PREFIXES = ("http://", "https://", "mailto:", "#")
SKIP_DIRS = {".git", "node_modules"}


def iter_markdown_files():
    for path in REPO_ROOT.rglob("*.md"):
        if not any(part in SKIP_DIRS for part in path.parts):
            yield path


def strip_code(text: str) -> str:
    text = FENCED_CODE_RE.sub("", text)
    text = INLINE_CODE_RE.sub("", text)
    return text


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
    text = strip_code(md_file.read_text(encoding="utf-8", errors="ignore"))
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


def load_baseline():
    if not BASELINE_FILE.exists():
        return set()
    lines = BASELINE_FILE.read_text(encoding="utf-8").splitlines()
    return {line for line in lines if line and not line.startswith("#")}


def find_all_broken():
    failures = []
    total_files = 0
    for md_file in sorted(iter_markdown_files()):
        total_files += 1
        for raw, resolved in check_file(md_file):
            failures.append((md_file.relative_to(REPO_ROOT), raw, resolved))
    return failures, total_files


def baseline_key(md_file, raw) -> str:
    return f"{md_file}::{raw}"


def update_baseline():
    failures, total_files = find_all_broken()
    keys = sorted({baseline_key(md_file, raw) for md_file, raw, _ in failures})
    header = (
        "# Known, pre-existing broken relative links.\n"
        "# Format: relative/path/to/file.md::raw-link-target\n"
        "# Regenerate with: python3 tools/check_markdown_links.py --update-baseline\n"
        "# CI only fails on links NOT in this file (i.e. newly introduced breakage).\n"
    )
    BASELINE_FILE.write_text(header + "\n".join(keys) + "\n", encoding="utf-8")
    print(f"Wrote {len(keys)} known-broken links to {BASELINE_FILE.relative_to(REPO_ROOT)} "
          f"(from {total_files} Markdown files).")


def main():
    if "--update-baseline" in sys.argv:
        update_baseline()
        return

    baseline = load_baseline()
    failures, total_files = find_all_broken()

    new_failures = []
    known_failures = []
    for md_file, raw, resolved in failures:
        if baseline_key(md_file, raw) in baseline:
            known_failures.append((md_file, raw, resolved))
        else:
            new_failures.append((md_file, raw, resolved))

    if known_failures:
        print(f"{len(known_failures)} known pre-existing broken link(s) (tracked in "
              f"{BASELINE_FILE.relative_to(REPO_ROOT)}, not failing the build):")
        for md_file, raw, resolved in known_failures:
            print(f"  {md_file}: [{raw}] -> {resolved} (missing)")
        print()

    if new_failures:
        print(f"NEW broken relative link(s) found ({len(new_failures)}):\n")
        for md_file, raw, resolved in new_failures:
            print(f"  {md_file}: [{raw}] -> {resolved} (missing)")
        print(f"\nChecked {total_files} Markdown files.")
        print(
            "\nIf this link is intentionally a placeholder/example, or you're "
            "deliberately deferring the fix, add it to "
            f"{BASELINE_FILE.relative_to(REPO_ROOT)} via --update-baseline."
        )
        sys.exit(1)

    print(f"No newly broken relative links across {total_files} Markdown files "
          f"({len(known_failures)} pre-existing, tracked in baseline).")


if __name__ == "__main__":
    main()
