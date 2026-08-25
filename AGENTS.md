# AGENTS.md

Guidance for Codex when working in this repository.

## What this repo is

This is a **Codex plugin marketplace**: 127 plugins composed of 644 Agent Skills,
published to PyPI as `vibey-skills` under the MIT license. Apart from a small
packaging CLI there is no application code — the deliverable is the Markdown and JSON that
define the plugins. "Correctness" means valid manifests and accurate, well-triggered skill
content.

## Source of truth

- [.claude-plugin/marketplace.json](https://github.com/adammatthewsteinberger/vibey-skills/blob/main/.claude-plugin/marketplace.json) — the marketplace
  manifest Codex reads when this repo is added with `/plugin marketplace add`. Each
  entry's `source` points at a directory under `plugins/`.
- [plugins/](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins) — the authoritative plugin sources. Edit skills here.

`plugins/` must stay at the repository root: Codex requires
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
  phrases — this is the only thing Codex sees when deciding whether to load the skill, so
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

- **Root Markdown** (`README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `SECURITY.md`,
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

## Scheduled currency research

`.github/workflows/currency-research.yml` runs weekly (Mondays, 06:17 UTC) and on
`workflow_dispatch`. It audits a rotating slice of the marketplace for stale dated claims —
versioned specifics, regulatory thresholds, market figures — researches them against the live
web, and opens a pull request against `develop` only when something actually changed. A run
that finds nothing writes its record to the job summary and opens nothing.

`tools/select_currency_batch.py` picks the slice. It is deterministic on the ISO week, so a
run reproduces locally:

```bash
python3 tools/select_currency_batch.py --week 34        # that week's briefing
python3 tools/select_currency_batch.py --plugins a,b    # an explicit set
```

**The method is not in the YAML.** It lives in the `currency-research` plugin in this
marketplace, which the workflow installs via the action's `plugin_marketplaces` / `plugins`
inputs — the repo's own deliverable tells the agent how to do the job, so improving the method
is an ordinary skill edit rather than a workflow change.

Two things must be configured for it to run, and neither is in the repository:

- the `ANTHROPIC_API_KEY` repository secret — the job exits with a notice if it is absent
  rather than failing every week;
- Settings → Actions → General → **Allow GitHub Actions to create and approve pull requests**,
  without which the default `GITHUB_TOKEN` cannot open the PR.

## Release tooling lives in a package, not in this repository

`vibey-gh` (on PyPI, no dependencies) provides the fingerprint check, the derived version
bump, the merge train, and branch realignment. This repository used to carry its own copy
of all of that — `tools/check_fingerprints.py`, `tools/next_version.py`,
`tools/dev_version.py` and a 170-line merge-train workflow, about 530 lines. They are
gone; the behaviour is unchanged.

```bash
pip install "vibey-gh==1.16.0"
vibey-gh install          # hooks + the merge-train workflow, and points core.hooksPath
vibey-gh check            # are the fingerprints intact?
vibey-gh version --since origin/main --explain
```

Everything project-specific is in `.vibey-gh.toml`: which files carry headers, which hold
the version, which paths count as content versus code, and who the merge train trusts.

`[install] workflows` manages `merge-train.yml`, `promote-to-main.yml`,
`provenance.yml`, `branch-intake.yml`, `automation-bootstrap.yml`, `codeql.yml`,
`pr-automation.yml`, `github-release.yml`, and `repository-profile.yml`.
`provenance.yml`'s job is named **Provenance** and is a REQUIRED status check on both
rulesets — it replaced a hand-written "Check fingerprints" step that used to live inside
ci.yml's **Validate manifests and build** job. `codeql.yml`'s job is named
**Analyze Python** and is also a REQUIRED status check on both rulesets, replacing CodeQL
**default setup** (Settings -> Code security), which is now switched off. Default setup
scanned both the `python` and `actions` languages; the template scans `python` only, so
GitHub Actions workflow scanning has no coverage until vibey-gh's template adds it.
`pr-automation.yml` publishes **PR automation / gate**, also a REQUIRED status check on
both rulesets, configured with `[pr_automation] scan_workflows = ["CI", "Provenance",
"CodeQL", "Docs"]` — the default additionally names `"API drift (Cloud Agents OpenAPI)"`,
vibey-gh's own self-test, which is not installed here.

`github-release.yml` is installed and REQUIRED knowing it fails on most pushes to
`main`: it has no way to skip a push that carries no version bump, and per `[version]`
above, most of this repository's own promotions are exactly that — docs- or
tooling-only. `vibey_gh.github_release.publish()` raises "refusing to move existing tag"
whenever the version file is unchanged, because the tag for that version already exists
at an earlier SHA. There is no config knob for this and no way to guard it from this
side of the trigger: a workflow run's overall `conclusion` is `success` once any job in
it succeeds, so nothing this repository's own `Release` workflow does can make
`github-release.yml`'s `workflow_run` trigger see anything other than `success`. Filed
upstream; accepted here because it is not a required check, and because
[.github/workflows/release-artifacts.yml](https://github.com/adammatthewsteinberger/vibey-skills/blob/main/.github/workflows/release-artifacts.yml)
(hand-authored) plus the unchanged `github-release` job inside `release.yml` still
produce a correct, artifact-carrying release on an actual version bump regardless of
whether this workflow succeeds.

`repository-profile.yml` is configured with a real `[repository_profile] description`
and `topics` — its defaults are generic release-automation boilerplate that would
overwrite this repository's actual GitHub description — and
`delete_branch_on_merge = false`, since `develop` heads the next promotion PR and must
survive a merge.

Not (yet) installed: `documentation.yml` (the documentation contract isn't satisfied),
and `release-surfaces.yml` (would contest Pages ownership with docs.yml).
`release-repair.yml` is excluded because it would spend an AI call diagnosing
`github-release.yml`'s expected failures as if each were a real one.

Two templates are deliberately excluded **permanently**, both for the same underlying
reason: a step that does `pip install .` (or checks out and installs this repo's own
default branch) expecting that to make the `vibey-gh` CLI itself available. It never
does — this repo's runtime `dependencies` are deliberately `[]`, so that install only
ever yields `vibey-skills`.
- `api-drift.yml` — asserts `vibey_gh.surfaces` parity on whatever it installed; the
  import fails outright.
- `conventional-commits.yml` — its "Check out trusted normalizer" step installs this
  repo's default branch, then calls a `vibey-gh` CLI that was never actually installed.
  Confirmed failing on PR #48 with "vibey-gh: command not found" inside the msg-filter.
  Not a required check, so this was silent rather than blocking — worse, since it can
  never actually normalize a commit message.

`vibey-gh install` fully regenerates every file in this list from its template, including
the `pip install` line inside it — which is **unpinned**, unlike the hand-authored
ci.yml/release.yml. A hand-edit to pin it would immediately be flagged as "out of date" by
`vibey-gh check`, so these workflows cannot be pinned the way Stage 1 pinned ci.yml and
release.yml. A future vibey-gh release can still change behavior under `provenance.yml`,
`merge-train.yml`, or `promote-to-main.yml` without warning; upgrading `vibey-gh` in
`pyproject.toml`'s `[dev]` extra and re-running `vibey-gh install` deliberately, then
re-verifying `vibey-gh check --ci`, is the only way to catch that before it reaches CI.

## The fingerprint

**Every code change carries it. This is mandatory and CI enforces it.**

```
# Made with ❤️ by [Vibey](https://adammatthewsteinberger.github.io/vibey/), Developed by [Adam Matthew Steinberger](https://hire.adam.matthewsteinberger.com/) ([@adammatthewsteinberger](https://github.com/adammatthewsteinberger/)).

Made-With: Made with ❤️ by [Vibey](https://adammatthewsteinberger.github.io/vibey/), Developed by [Adam Matthew Steinberger](https://hire.adam.matthewsteinberger.com/) ([@adammatthewsteinberger](https://github.com/adammatthewsteinberger/)).
```

Two places, because a change can be either:

- **Source files** carry the header comment — `tools/`, `src/`, `docs/*.py` and
  `.github/workflows/*.yml`. `vibey-gh check --apply` adds it to anything missing it.
- **Every commit** carries the `Made-With:` trailer. This is what makes the rule total:
  a change to a `SKILL.md` or a JSON manifest still arrives as a commit, and the commit
  is fingerprinted even when the file cannot be.

Install the tooling and its hooks once per clone, so the trailer is added for you and a
push without the fingerprints is refused:

```bash
pip install "vibey-gh==1.16.0"
vibey-gh install
```

`vibey-gh check` runs in CI on every push and pull request; on a pull request it also
checks the trailer on each commit the branch adds.

**What is deliberately not fingerprinted**, and why the trailer exists to cover it:

- `plugins/**/SKILL.md` — the product. Their bytes are loaded into a model's context and
  many are verified byte-for-byte against the source documents they were split from, so a
  header would be both context noise and a diff against the source.
- Any `.json` — no comment syntax, and `marketplace.json` is parsed by Claude Code itself.
- Prose Markdown at the root — documentation, rendered on PyPI and GitHub Pages.

## Branching and publishing

```
feature/*  --PR-->  develop  --PR-->  main
                      |                 |
                   TestPyPI           PyPI
```

- **Work happens on `feature/*` branches**, never directly on `develop`. Open a pull
  request into `develop`.
- **Every push to `develop` publishes to TestPyPI** as `<release>.dev<run_number>` — see
  `vibey-gh version --dev`. An index version is immutable, so a develop build cannot reuse
  the release version; the dev suffix makes each push distinct and sorts it before the
  release it anticipates. The patch is applied in the runner only and never committed.
- **Every push to `main` publishes directly to PyPI** as the exact version in
  `src/vibey_skills/__init__.py`. Most pushes to
  main carry no version bump, so the publish skips a version PyPI already holds rather
  than failing.
- **A `v*` tag** additionally attaches the artifacts to a GitHub Release.

- **`feature/* -> develop` is squash-merged**, always and only. develop's ruleset sets
  `allowed_merge_methods: ["squash"]`, so a feature branch arrives on develop as one
  commit.
- **`develop -> main` is rebase-merged**, always and only. Every commit from develop is
  preserved and replayed onto the front of main's history with new SHAs and new
  timestamps. This is the only method consistent with the `required_linear_history` rule
  both rulesets enforce — a merge commit violates it, which is why merges to main used to
  need an admin bypass.
- **Two weekly trains** carry the work through, both on Monday, after the currency audit
  at 06:17:
  - `merge-train.yml` (07:17) reviews every open pull request into develop and
    squash-merges the ready ones. "Ready" is mechanical — not a draft, no conflicts,
    checks green, no changes requested; anything else is skipped with the reason recorded.
  - `promote-to-main.yml` (08:17) runs `vibey-gh promote`, which compares develop and
    main **by content** and, if they
    differ, opens the promotion pull request, waits for its checks and rebase-merges it.
    That push publishes to PyPI.
- **`develop` is realigned to `main`** by `vibey-gh realign`, in `release.yml`'s
  `sync-develop` job, after each
  publish. Rebase gives main rewritten SHAs, so develop can never be fast-forwarded onto
  it; the job realigns only when the two trees are **identical**, so it can never discard
  work. Do not realign by hand.

### Version bumps are derived, not remembered

`vibey-gh version` decides the release version from what actually changed since
`main`, and the promotion applies it:

| what changed | bump |
|---|---|
| `plugins/` or the marketplace manifest | **minor** — new or revised skills are the product |
| only `src/` | **patch** — a CLI fix |
| only docs, workflows, tooling | **none** — nothing reaches an installed user |
| version already differs from `main` | **none** — a deliberate bump is in place; never double-bump |

This has to be automatic. The PyPI upload uses `skip-existing`, so a promotion whose
version nobody bumped is a green run that publishes nothing, silently, with no warning.

### Why `develop` used to fall behind

A `develop -> main` pull request leaves exactly one commit on `main` that `develop` does
not have: the merge commit itself. GitHub's merge button has no fast-forward option, so
`develop` ended up permanently one commit behind after every release, every following
pull request reported *"head branch is not up to date"*, and the fix each time was a
manual back-merge.

The `sync-develop` job in `.github/workflows/release.yml` removes that step: after a
successful publish from `main` it fast-forwards `develop` onto `main`. `develop`'s tip is
always an ancestor of the merge commit, so this is a fast-forward — no merge, no new
commit, nothing to resolve. **Do not back-merge `main` into `develop` by hand**; if the
job reports it could not fast-forward, that means `develop` has genuinely new commits and
they belong in a pull request.

## Releasing

`.github/workflows/ci.yml` runs both checkers, `uv build`, `uvx twine check dist/*`, a
wheel-completeness assertion, a wheel smoke test, and `mkdocs build --strict` on every push
and pull request.

Pushing a `v*` tag triggers `.github/workflows/release.yml`, which builds once, publishes
directly to PyPI, and attaches the same sdist and wheel to a GitHub Release. Develop remains
the isolated TestPyPI lane and verifies its uniquely versioned development artifact there;
main and tags do not depend on a second registry.

Both publishes use Trusted Publishing (OIDC) — no API token is stored anywhere. Bump the
version in `src/vibey_skills/__init__.py` and `marketplace.json`'s
`metadata.version` together (CI asserts they match, and that the tag matches both), then tag.
