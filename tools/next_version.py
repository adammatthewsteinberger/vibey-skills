#!/usr/bin/env python3
# Made with love by Vibey, the auto-vibecoding machine by Adam Matthew Steinberger.
"""Decide the next package version from what actually changed since the last release.

Stdlib only, like the other tools.

    python3 tools/next_version.py                  # print the version to release, or "none"
    python3 tools/next_version.py --apply          # write it to both version sites
    python3 tools/next_version.py --since origin/main --explain

Why this has to be automatic
----------------------------
The PyPI publish uses `skip-existing`, so a promotion whose version was not bumped is a
green run that releases nothing — silently. Nothing warns you. For the weekly train to be
autonomous rather than merely unattended, the bump has to be derived, not remembered.

The rule follows what is actually in the wheel
----------------------------------------------
`pyproject.toml` force-includes `plugins/` and `.claude-plugin/marketplace.json` alongside
`src/`. So:

  plugins/ or the marketplace manifest changed  -> MINOR. New or revised skills are the
                                                   product; every release in this repo's
                                                   history that shipped skills was a minor.
  only src/ changed                             -> PATCH. A CLI fix, no content change.
  neither                                       -> NONE. Docs, workflows and tooling do
                                                   not reach an installed user, so there
                                                   is nothing to release and a version
                                                   bump would be noise.

`none` is a legitimate, common answer. The promotion still happens; it just does not
publish, which is correct rather than a failure.

The guard that stops double bumps
---------------------------------
If the working version already differs from the released one, somebody bumped it by hand
in a pull request — the usual case for a deliberate release — and this reports `none` so
the promotion uses their number rather than adding another on top.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INIT = ROOT / "src" / "vibey_skills" / "__init__.py"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
VERSION_RE = re.compile(r'^__version__ = "([^"]+)"$', re.M)

# Paths whose contents reach an installed user, most significant first.
CONTENT_PATHS = ("plugins/", ".claude-plugin/marketplace.json")
CODE_PATHS = ("src/",)


def git(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"git {' '.join(args)}: {result.stderr.strip()}")
    return result.stdout


def current_version() -> str:
    match = VERSION_RE.search(INIT.read_text(encoding="utf-8"))
    if not match:
        sys.exit(f"{INIT}: no __version__ found")
    return match.group(1)


def released_version(ref: str) -> str | None:
    result = subprocess.run(["git", "show", f"{ref}:src/vibey_skills/__init__.py"],
                            cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        return None
    match = VERSION_RE.search(result.stdout)
    return match.group(1) if match else None


def bump(version: str, level: str) -> str:
    major, minor, patch = (int(p) for p in version.split(".")[:3])
    if level == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def decide(since: str) -> tuple[str | None, str]:
    """Return (new_version_or_None, human explanation)."""
    released = released_version(since)
    if released is None:
        return None, f"cannot read a version at {since}; refusing to guess"

    working = current_version()
    if working != released:
        return None, (f"already at {working} while {since} is {released} — "
                      "a deliberate bump is in place, leaving it alone")

    changed = [line for line in git("diff", "--name-only", since, "HEAD").splitlines() if line]
    if not changed:
        return None, f"no changes since {since}"

    if any(f.startswith(p) for f in changed for p in CONTENT_PATHS):
        return bump(working, "minor"), "packaged skills or the marketplace manifest changed"
    if any(f.startswith(p) for f in changed for p in CODE_PATHS):
        return bump(working, "patch"), "only the CLI changed"
    return None, (f"{len(changed)} file(s) changed but none reach an installed user "
                  "(docs, workflows, tooling) — nothing to release")


def apply(new: str) -> None:
    init = INIT.read_text(encoding="utf-8")
    patched, count = VERSION_RE.subn(f'__version__ = "{new}"', init, count=1)
    if count != 1:
        sys.exit(f"{INIT}: expected one __version__ line, found {count}")
    INIT.write_text(patched, encoding="utf-8")

    data = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    data["metadata"]["version"] = new
    MARKETPLACE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--since", default="origin/main",
                        help="the ref holding the last released version (default: origin/main)")
    parser.add_argument("--apply", action="store_true", help="write the new version")
    parser.add_argument("--explain", action="store_true", help="print the reasoning to stderr")
    args = parser.parse_args()

    new, why = decide(args.since)
    if args.explain or not new:
        print(f"next_version: {why}", file=sys.stderr)
    if not new:
        print("none")
        return 0
    if args.apply:
        apply(new)
    print(new)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
