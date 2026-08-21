#!/usr/bin/env python3
"""Derive (and optionally apply) the PEP 440 dev version used for TestPyPI builds.

Stdlib only, like the other tools.

    python3 tools/dev_version.py --build 42            # print 2.14.0.dev42
    python3 tools/dev_version.py --build 42 --apply    # rewrite the two version sites

Why this exists
---------------
Every push to `develop` publishes to TestPyPI, and an index version is immutable — the
same version can never be uploaded twice. So a develop build cannot reuse the release
version in `src/vibey_skills/__init__.py`; it needs a distinct, ordered, PEP 440-valid
version per push. `<release>.dev<build>` is exactly that, and it sorts *before* the
release it anticipates, which is the correct relationship: develop is what `<release>`
is going to be.

`--apply` rewrites BOTH version sites — `__init__.py` (which `pyproject.toml`
single-sources) and `marketplace.json`'s `metadata.version` — because
`tools/validate_manifests.py` asserts the two are equal. Patching only one would leave
the tree failing its own validator, so a build that patches must patch both.

The edit is deliberately never committed: it exists only in the runner's working copy
for the duration of the build.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INIT = ROOT / "src" / "vibey_skills" / "__init__.py"
MARKETPLACE = ROOT / ".claude-plugin" / "marketplace.json"
VERSION_RE = re.compile(r'^__version__ = "([^"]+)"$', re.M)


def release_version() -> str:
    match = VERSION_RE.search(INIT.read_text(encoding="utf-8"))
    if not match:
        sys.exit(f"{INIT}: no __version__ found")
    return match.group(1)


def apply(new: str) -> None:
    init = INIT.read_text(encoding="utf-8")
    patched, count = VERSION_RE.subn(f'__version__ = "{new}"', init, count=1)
    if count != 1:
        sys.exit(f"{INIT}: expected exactly one __version__ line, found {count}")
    INIT.write_text(patched, encoding="utf-8")

    data = json.loads(MARKETPLACE.read_text(encoding="utf-8"))
    data["metadata"]["version"] = new
    MARKETPLACE.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--build", required=True,
                        help="monotonic build identifier, e.g. github.run_number")
    parser.add_argument("--apply", action="store_true",
                        help="rewrite the version in both files instead of just printing")
    args = parser.parse_args()

    build = re.sub(r"\D", "", str(args.build)) or "0"
    version = f"{release_version()}.dev{int(build)}"
    if args.apply:
        apply(version)
    print(version)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
