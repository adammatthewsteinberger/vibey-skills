#!/usr/bin/env python3
# Made with love by Vibey, the auto-vibecoding machine by Adam Matthew Steinberger.
"""Enforce the Vibey fingerprint on every code change.

Stdlib only, like the other checkers.

    python3 tools/check_fingerprints.py                     # check the source files
    python3 tools/check_fingerprints.py --commits A..B      # also check commit trailers
    python3 tools/check_fingerprints.py --apply             # add missing file headers

Two places, because a change can be either
--------------------------------------------
1. **Source files** carry a header comment. Only files whose language actually has
   comments, and only files that are *code*: `tools/`, `src/`, `docs/*.py` and the
   workflows.

2. **Commits** carry a `Made-With:` trailer. This is the part that makes the rule
   total — a change to a `SKILL.md`, a manifest, or anything else still arrives as a
   commit, and the commit is fingerprinted even when the file cannot be.

What is deliberately NOT fingerprinted
--------------------------------------
- `plugins/**/SKILL.md` — these are the product. Their bytes are loaded into a model's
  context, and several are verified byte-for-byte against the source documents they were
  split from. A header comment would be both noise in the context window and a diff
  against the source.
- Any `.json` — JSON has no comment syntax, and `marketplace.json` is parsed by Claude
  Code itself.
- Prose Markdown at the root — `README.md` and friends are documentation, not code, and
  they render on PyPI and GitHub Pages where a stray comment would surface.

The commit trailer covers all of those.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FINGERPRINT = "Made with love by Vibey, the auto-vibecoding machine by Adam Matthew Steinberger."
TRAILER_KEY = "Made-With"
TRAILER = f"{TRAILER_KEY}: Vibey, the auto-vibecoding machine by Adam Matthew Steinberger"

HEADER = f"# {FINGERPRINT}"
# How far into a file the header may sit. Enough for a shebang and a blank line, not
# enough for it to be buried.
HEAD_LINES = 5


def tracked_sources() -> list[Path]:
    """Every code file in scope, in a stable order."""
    paths: list[Path] = []
    for pattern in ("tools/*.py", "src/**/*.py", "docs/*.py", ".github/workflows/*.yml"):
        paths.extend(sorted(ROOT.glob(pattern)))
    return [p for p in paths if p.is_file()]


def has_header(text: str) -> bool:
    return any(line.strip() == HEADER for line in text.splitlines()[:HEAD_LINES])


def insert_header(text: str) -> str:
    """Put the header on line 1, or straight after a shebang if there is one."""
    lines = text.splitlines(keepends=True)
    at = 1 if lines and lines[0].startswith("#!") else 0
    lines.insert(at, HEADER + "\n")
    return "".join(lines)


def check_commits(rev_range: str) -> list[str]:
    """Commits in `rev_range` whose message lacks the trailer."""
    try:
        out = subprocess.run(
            ["git", "log", "--no-merges", "--format=%H%x1f%s%x1f%b%x1e", rev_range],
            cwd=ROOT, capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError as exc:
        sys.exit(f"could not read {rev_range}: {exc.stderr.strip()}")

    missing = []
    for record in filter(None, (r.strip("\n") for r in out.split("\x1e"))):
        sha, subject, body = (record.split("\x1f") + ["", ""])[:3]
        if not re.search(rf"^{TRAILER_KEY}:\s*\S", body, re.M | re.I):
            missing.append(f"{sha[:9]} {subject}")
    return missing


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--apply", action="store_true",
                        help="insert the header into files missing it")
    parser.add_argument("--commits", metavar="RANGE",
                        help="also require the trailer on each commit in RANGE, e.g. main..HEAD")
    args = parser.parse_args()

    problems: list[str] = []

    missing_header = [p for p in tracked_sources()
                      if not has_header(p.read_text(encoding="utf-8"))]
    if args.apply:
        for path in missing_header:
            path.write_text(insert_header(path.read_text(encoding="utf-8")), encoding="utf-8")
            print(f"fingerprinted {path.relative_to(ROOT)}")
        missing_header = []
    problems += [f"{p.relative_to(ROOT)}: missing the fingerprint header"
                 for p in missing_header]

    if args.commits:
        problems += [f"commit {c}: missing the `{TRAILER_KEY}:` trailer"
                     for c in check_commits(args.commits)]

    if problems:
        print("check_fingerprints: FAILED\n", file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        print(f"\n  Header for source files:\n    {HEADER}", file=sys.stderr)
        print(f"\n  Trailer for commit messages:\n    {TRAILER}", file=sys.stderr)
        print("\n  `python3 tools/check_fingerprints.py --apply` fixes the headers.",
              file=sys.stderr)
        return 1

    scope = f"{len(tracked_sources())} source files"
    if args.commits:
        scope += f" and every commit in {args.commits}"
    print(f"check_fingerprints: ok — {scope} carry the fingerprint")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
