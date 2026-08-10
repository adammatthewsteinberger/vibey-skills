# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this repo is

This is a **Claude Code plugin marketplace**: 18 plugins composed of 71 Agent Skills,
published to PyPI as `vibe-engineering-skills` under the MIT license. Apart from a small
packaging CLI there is no application code — the deliverable is the Markdown and JSON that
define the plugins. "Correctness" means valid manifests and accurate, well-triggered skill
content.

## Source of truth

- [.claude-plugin/marketplace.json](.claude-plugin/marketplace.json) — the marketplace
  manifest Claude Code reads when this repo is added with `/plugin marketplace add`. Each
  entry's `source` points at a directory under `plugins/`.
- [plugins/](plugins/) — the authoritative plugin sources. Edit skills here.

`plugins/` must stay at the repository root: Claude Code requires
`.claude-plugin/marketplace.json` at the root with `source: ./plugins/<name>`. The Python
wheel force-includes that same tree instead of duplicating it, so there is exactly one copy
of every skill file.

## Plugin structure

```
plugins/<plugin-name>/
  .claude-plugin/plugin.json    Manifest: name, version, description, author
  README.md                     Human overview + bullet list of skills
  skills/<skill-name>/SKILL.md  One skill per directory
```

### plugin.json

```json
{
  "name": "agile-delivery",
  "version": "0.1.0",
  "description": "Agile Delivery: …",
  "author": { "name": "vibe-engineering-skills contributors" }
}
```

`name` must match both the directory name and the `name`/`source` in
`.claude-plugin/marketplace.json`.

### SKILL.md

YAML frontmatter then Markdown body:

```markdown
---
name: delivery-velocity
description: Use when … Triggers on … Also triggers on …
---

# Delivery Velocity

<body>
```

- `name` (required) matches the skill directory name (kebab-case).
- `description` (required) is the trigger. Write it as "Use when …" plus concrete trigger
  phrases — this is the only thing Claude sees when deciding whether to load the skill, so
  be specific about the tasks, tools, and terms that should activate it.
- Keep the body self-contained and evidence-grounded; cite sources where claims are made.

## Conventions

- `author` is always `{ "name": "vibe-engineering-skills contributors" }`, in both
  `plugin.json` and each `marketplace.json` entry. Tracked files carry no personal names and
  no email addresses — attribution lives in the Git history.
- Skills are general-purpose. Never add content that documents a specific organization's
  internal systems, hostnames, ticket IDs, or personnel; that belongs in a private
  marketplace, not this public one.
- Versioning is per-plugin semver in `plugin.json`. Most plugins are `0.1.0`; revised ones
  are `0.2.0`.
- The package version in `pyproject.toml` (single-sourced from
  `src/vibe_engineering_skills/__init__.py:__version__`) must equal `marketplace.json`'s
  `metadata.version`. The validator enforces this.
- Plugin and skill names are kebab-case and must be unique within the marketplace.

## When you change a plugin

1. Edit the skill(s) under `plugins/<name>/skills/<skill>/SKILL.md`.
2. Bump `version` in `plugins/<name>/.claude-plugin/plugin.json`.
3. Mirror `version`, `description`, and `category` into the matching entry in
   `.claude-plugin/marketplace.json`.
4. Update `plugins/<name>/README.md` and the plugin table in the root
   [README.md](README.md) if the skill list or summary changed.
5. Run the validator — it must exit 0:
   ```bash
   python3 tools/validate_manifests.py
   ```

Keep `.claude-plugin/marketplace.json` and the per-plugin `plugin.json` files in sync —
a mismatch in `name` or `source` will break installation.

## Releasing

`.github/workflows/ci.yml` runs the validator, `uv build`, and `uvx twine check dist/*` on
every push and pull request. Pushing a `v*` tag triggers `.github/workflows/release.yml`,
which builds and publishes to PyPI via Trusted Publishing (OIDC) — no API token is stored
anywhere. Bump the version in `src/vibe_engineering_skills/__init__.py` and
`marketplace.json`'s `metadata.version` together, then tag.
