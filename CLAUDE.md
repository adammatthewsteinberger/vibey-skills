# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this repo is

This is a **Claude Code plugin marketplace**: 61 plugins composed of 280 Agent Skills,
published to PyPI as `vibey-skills` under the MIT license. Apart from a small
packaging CLI there is no application code — the deliverable is the Markdown and JSON that
define the plugins. "Correctness" means valid manifests and accurate, well-triggered skill
content.

## Source of truth

- [.claude-plugin/marketplace.json](https://github.com/adammatthewsteinberger/vibey-skills/blob/main/.claude-plugin/marketplace.json) — the marketplace
  manifest Claude Code reads when this repo is added with `/plugin marketplace add`. Each
  entry's `source` points at a directory under `plugins/`.
- [plugins/](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins) — the authoritative plugin sources. Edit skills here.

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
  "author": { "name": "Adam Matthew Steinberger", "email": "adam@matthewsteinberger.com" }
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

- `author` is always `{ "name": "Adam Matthew Steinberger", "email":
  "adam@matthewsteinberger.com" }`, in both
  `plugin.json` and each `marketplace.json` entry, and the same identity is used for
  `authors`/`maintainers` in `pyproject.toml`. The MIT copyright in `LICENSE` is held
  jointly by **The Vizius Group** (where the project was originally developed as
  `vibe-engineering-skills`) and **Adam Matthew Steinberger**; `NOTICE.md` records the
  republication. Do not remove either line.
- Skills are general-purpose. Never add content that documents a specific organization's
  internal systems, hostnames, ticket IDs, or personnel; that belongs in a private
  marketplace, not this public one.
- Versioning is per-plugin semver in `plugin.json`. Most plugins are `0.1.0`; revised ones
  are `0.2.0`.
- The package version in `pyproject.toml` (single-sourced from
  `src/vibey_skills/__init__.py:__version__`) must equal `marketplace.json`'s
  `metadata.version`. The validator enforces this.
- Plugin and skill names are kebab-case and must be unique within the marketplace.

## When you change a plugin

1. Edit the skill(s) under `plugins/<name>/skills/<skill>/SKILL.md`.
2. Bump `version` in `plugins/<name>/.claude-plugin/plugin.json`.
3. Mirror `version`, `description`, and `category` into the matching entry in
   `.claude-plugin/marketplace.json`.
4. Update `plugins/<name>/README.md` and the plugin table in the root
   [README.md](https://github.com/adammatthewsteinberger/vibey-skills/blob/main/README.md) if the skill list or summary changed.
5. Run both checkers — each must exit 0:
   ```bash
   python3 tools/validate_manifests.py
   python3 tools/check_links.py
   ```

Keep `.claude-plugin/marketplace.json` and the per-plugin `plugin.json` files in sync —
a mismatch in `name` or `source` will break installation.

## Documentation links: absolute at the root, relative under `docs/`

This is a hard rule, not a style preference, because three renderers resolve links against
three different base URLs:

| Surface | Base | Relative links |
|---|---|---|
| GitHub repo view | the repo root | work |
| PyPI project page | `https://pypi.org/project/vibey-skills/` | **break** |
| Pages site | `https://adammatthewsteinberger.github.io/vibey-skills/` | work only inside `docs/` |

- **Root Markdown** (`README.md`, `CONTRIBUTING.md`, `CLAUDE.md`, `SECURITY.md`,
  `CODE_OF_CONDUCT.md`) must use **absolute** `https://github.com/…/blob/main/…` URLs —
  `blob` for files, `tree` for directories. 1.0.0 shipped
  `](.claude-plugin/marketplace.json)`, which renders fine on GitHub and 404s on PyPI.
- **Files under `docs/`** must use **relative** links so `mkdocs build --strict` can verify
  them and the Pages site stays self-contained.

`tools/check_links.py` enforces both directions and runs in CI. It is hermetic — no HTTP —
because a link checker that needs the network gets switched off the first time CI flakes.

## Documentation site

`mkdocs.yml` builds a Material site published to
<https://adammatthewsteinberger.github.io/vibey-skills/> by
`.github/workflows/docs.yml`.

The skills reference is **generated**, not written: `docs/gen_reference.py` synthesises a page
per plugin and per skill from `plugins/**` at build time, exactly as the wheel maps that same
tree in via hatchling `force-include`. Never add a skill page to `docs/` by hand — edit the
`SKILL.md` it comes from. Adding a plugin or skill needs no `mkdocs.yml` change; the nav is
generated too.

```bash
pip install -e ".[docs]"
mkdocs serve
mkdocs build --strict   # what CI runs; warnings are errors
```

`docs.yml` also triggers on `plugins/**`, since a skill edit changes the site even when
nothing under `docs/` was touched.

## Releasing

`.github/workflows/ci.yml` runs both checkers, `uv build`, `uvx twine check dist/*`, a
wheel-completeness assertion, a wheel smoke test, and `mkdocs build --strict` on every push
and pull request.

Pushing a `v*` tag triggers `.github/workflows/release.yml`, which builds, then publishes in
this order:

1. **TestPyPI** — separate instance, separate trusted publisher.
2. **Verify** — installs that exact version from TestPyPI and asserts all 280 skills land.
3. **PyPI** — only if the verify step passed.
4. **GitHub Release** — sdist and wheel attached.

TestPyPI comes first because a PyPI version number is immutable: it can never be reused, even
after a yank, so the only chance to catch a bad artifact is before it is uploaded.

Both publishes use Trusted Publishing (OIDC) — no API token is stored anywhere. Bump the
version in `src/vibey_skills/__init__.py` and `marketplace.json`'s
`metadata.version` together (CI asserts they match, and that the tag matches both), then tag.
