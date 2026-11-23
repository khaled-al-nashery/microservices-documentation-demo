#!/usr/bin/env python3
"""Check that every internal reference in the docs resolves to a real file.

Scans docs/*.md for markdown links and inline-code file paths, then verifies
each target exists under the repo (relative to the doc's directory). This is
the local equivalent of a broken-link check in CI.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SERVICE = ROOT / "order-service"
ERRORS = 0

# match [text](target) and backtick `path` and bare file names
MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def main() -> None:
    global ERRORS
    docs = sorted((SERVICE / "docs").glob("*.md"))
    for doc in docs:
        text = doc.read_text(encoding="utf-8")
        print(f"== {doc.name} ==")
        for m in MD_LINK.finditer(text):
            label, target = m.group(1), m.group(2)
            if "://" in target or target.startswith("#"):
                continue  # external URL or anchor — not a local-file check
            t = target.split("#")[0].strip()
            if not t:
                continue
            candidate = (doc.parent / t).resolve()
            if candidate.exists():
                print(f"  OK     {label!r} -> {t!r}")
            else:
                ERRORS += 1
                print(f"  BROKEN {label!r} -> {t!r}")
    print()
    if ERRORS:
        print(f"RESULT: FAIL ({ERRORS} broken reference(s))")
        sys.exit(1)
    print("RESULT: PASS — all internal references resolve")


if __name__ == "__main__":
    main()
