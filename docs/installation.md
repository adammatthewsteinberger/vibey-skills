# Installation

## As a Claude Code marketplace

The native route. Claude Code reads the marketplace manifest and manages plugins for you.

```bash
# From the Git remote
/plugin marketplace add TheViziusGroup/vibe-engineering-skills

# ...or from a local clone
/plugin marketplace add /path/to/vibe-engineering-skills

# Browse, then install what you want
/plugin
/plugin install security-principles@vibe-engineering-skills
```

## From PyPI

The same skills ship as a Python package with **no runtime dependencies**, so `uvx` can run
it without a resolution step. Useful when you want the skills in a harness other than
Claude Code, or you would rather not clone.

```bash
# Run without installing
uvx vibe-engineering-skills install --all

# ...or install the CLI persistently
uv tool install vibe-engineering-skills
pip install vibe-engineering-skills
```

Requires Python 3.10 or newer.

## Where skills get installed

`install` copies each skill directory to `~/.claude/skills/<skill-name>/` by default,
creating the directory if it does not exist. Override with `--dest`:

```bash
vibe-skills install --all --dest ./.claude/skills   # project-local instead of user-global
```

Existing directories are **skipped, never overwritten** — see
[Usage](usage.md#conflicts-and-updates).
