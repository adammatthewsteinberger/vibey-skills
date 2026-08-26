# .github

This document explains the automation that lives in this directory: what runs, why it
runs, what it is and is not trusted to do, and how to change it safely. It is written for
whoever next touches a workflow file — a maintainer, a contributor, or an agent — not for
users of the marketplace itself (that's the root
[README.md](https://github.com/adammatthewsteinberger/vibey-skills/blob/main/README.md)).

## Delivery model

Work moves `feature/* -> develop -> main`. A `feature/*` branch is squash-merged into
`develop`; `develop` is rebase-merged into `main`, which is the only method consistent
with the `required_linear_history` rule both branch rulesets enforce. Every push to
`develop` publishes a `<release>.dev<run_number>` build to TestPyPI; every push to `main`
publishes the exact version in `src/vibey_skills/__init__.py` to PyPI, after the same
TestPyPI-then-verify gate. A `v*` tag additionally attaches build artifacts to a GitHub
Release. Two weekly trains carry ordinary work through without a human in the loop: a
merge train squash-merges ready pull requests into `develop`, and a promotion opens (and,
once its checks pass, rebase-merges) the pull request that carries `develop` into `main`
when the two differ. Full detail, including why `develop` used to fall behind `main` and
how that's fixed, is in
[CLAUDE.md](https://github.com/adammatthewsteinberger/vibey-skills/blob/main/CLAUDE.md).

## Workflow inventory

Five workflows are hand-authored because they are specific to this repository's product or
its release pattern: `CI` (manifest and skill-frontmatter validation, packaging, the
wheel-completeness assertion), `Release` (the TestPyPI/PyPI publish pipeline and
`develop`'s realignment onto `main`), `Release artifacts` (attaches the sdist/wheel to
whatever GitHub Release `github-release.yml` creates — vibey-gh's own template has no
way to attach files), `Docs` (the mkdocs Material site, deployed to GitHub Pages), and
`Currency research` (a scheduled agent that audits dated claims in skill content against
the live web). Ten more are managed by `vibey-gh install` (pinned exactly, via
`[install] pin_version = true`) from its own templates and regenerated verbatim whenever
that command runs: `provenance.yml` (job name **Provenance**), `codeql.yml` (job name
**Analyze Python**), `pr-automation.yml` (publishes the **PR automation / gate** check),
`merge-train.yml`, `promote-to-main.yml`, `branch-intake.yml`,
`automation-bootstrap.yml`, `github-release.yml`, `repository-profile.yml`, and
`conventional-commits.yml`. `Provenance`, `Analyze Python`, and `PR automation / gate`
are required status checks on both branch rulesets, alongside the hand-authored `Validate
manifests and build` and `Build docs (strict)`.

Not every template `vibey-gh` ships is adopted. `api-drift.yml` is excluded permanently:
it is vibey-gh's own self-test (`pip install .` then `import vibey_gh.surfaces`), which
only works when the adopting repository's own package *is* `vibey-gh` — false here by
design, since runtime `dependencies` are deliberately empty. `conventional-commits.yml`
had the identical defect through vibey-gh 1.16.0 and was excluded for the same reason;
fixed upstream in 1.27.0 (the same self-hosting detection `provenance.yml` already used)
and re-adopted here.
`documentation.yml` is not yet adopted pending further configuration.
`release-surfaces.yml` is excluded because it would contest ownership of GitHub Pages with
`docs.yml`, which already publishes the marketplace's real documentation site.
`release-repair.yml` is excluded because it would spend an AI call diagnosing
`github-release.yml`'s expected failures (below) as if each were a real one.

`github-release.yml` is installed and required on this repository. Through vibey-gh
1.26.0 it failed on most pushes to `main`, since it had no way to skip a push that
carried no version bump and most of this repository's promotions are exactly that —
fixed upstream in 1.27.0, where that case is now a clean no-op rather than an error. See
[.vibey-gh.toml](https://github.com/adammatthewsteinberger/vibey-skills/blob/main/.vibey-gh.toml)'s
`[install]` comment for the full history. `release.yml`'s own tag-triggered release job
still creates a correct, artifact-carrying release independently of this workflow.

## Exact-head PR automation

`vibey-gh`'s design principle is that only evidence produced against a pull request's
*exact current head commit* counts — a check that ran against an earlier commit, or a
review approving an earlier commit, is stale the moment the branch moves. The merge train
applies this mechanically: readiness is not a draft, no merge conflicts, every check green,
and no outstanding changes-requested review, evaluated fresh each run rather than cached
from a prior pass. A pull request held back only by the review requirement is labeled and
its owner is mentioned once, so a real contribution does not sit unnoticed; a draft or a
red build gets neither, because that is the contributor's own next step, not something
worth paging anyone about.

## AI trust boundary

The one workflow that runs an AI agent with write access, `Currency research`, is scoped
tightly: it may only edit skill content for dated claims, must attach its research sources
in the pull request body, and is explicitly forbidden from merging, closing, changing
repository settings, or pushing to `develop` or `main` directly — it can only open a pull
request into `develop`, which the ordinary review and merge-train path then evaluates like
any other contribution. It also carries the fingerprint trailer, same as a human commit.

## Credentials and settings

`ANTHROPIC_API_KEY` and `AUTOMERGE_TOKEN` are configured as repository secrets.
`AUTOMERGE_TOKEN` exists because a branch ruleset that requires an approving review cannot
be satisfied by the default `GITHUB_TOKEN`, and because a push authenticated as
`github-actions[bot]` does not trigger further workflows — a release chain downstream of an
automated merge would silently stop. Settings -> Actions -> General must allow Actions to
create and approve pull requests, or the merge train and the promotion cannot open theirs.

## Permanent-branch safety

`develop` and `main` are permanent branches, protected by rulesets that both trainings
respect: they may advance, but neither this automation nor a human is expected to delete or
force-push them. `develop` is realigned onto `main` after every release by fast-forward
only — the job checks the two trees are byte-identical first, so it can never discard work,
and never back-merges by hand.

## Failure recovery

`automation-bootstrap.yml` exists for the case the privileged automation itself is broken:
an admin-only, manually dispatched recovery merge, gated on an open non-draft pull request
against `develop`, an exact head match, changes confined to workflow/template/automation
paths, and every non-gate check green. Outside that narrow path, a failed required check
blocks the merge train exactly as intended, and the fix is the ordinary one — push a new
commit and let the checks run again against the new head.

**The exact-head review can fail for a reason that has nothing to do with the PR**:
`pr-automation.yml`'s own gate messaging distinguishes this case by design — "Scans passed
for this exact head, but the exact-head review returned no verdict... This is an
infrastructure or operator failure rather than a defect in the pull request. Check the
review job log for API credit balance, credentials, or model availability, then rerun." A
review job that shows `is_error: true` with `num_turns: 1`, `total_cost_usd: 0`, and empty
`modelUsage` in its result JSON failed before the model ran at all — most often exhausted
`ANTHROPIC_API_KEY` credits. The ordinary fix is `gh run rerun <run-id> --failed` once
credits are restored.

If a merge genuinely can't wait for that, the fallback is a manual, human-equivalent
review posted in the same shape `gate` itself posts, so the check-run contract stays
identical whether the review ran automatically or was done by hand:

```bash
gh api "repos/<owner>/<repo>/check-runs" --method POST \
  -f name='PR automation / gate' -f head_sha="<exact head SHA>" \
  -f status=completed -f conclusion=success \
  -f "output[title]=PR automation: manual review (API credits exhausted)" \
  -f "output[summary]=Reviewed by hand in place of the exact-head review, which failed with is_error and zero cost/turns (credit exhaustion, not a PR defect). <one-line verdict>."
```
Only ever do this after actually reading the diff — it substitutes for the review, not for
having one.

## Changing workflows

The four hand-authored workflows are edited directly; their `name:` fields are load-bearing
(`CI` and `Release` are watched by name elsewhere) and must not change casually. The six
`vibey-gh`-managed workflows are edited by changing `.vibey-gh.toml`'s `[install]`
`workflows` list or the relevant config table, then running `vibey-gh install` — a manual
edit to one of these files is reported as "out of date" by `vibey-gh check` and overwritten
on the next `install`. Adding a new managed template is a one-line config change followed
by `vibey-gh install`; removing one requires deleting the generated file by hand, since
`install` never deletes.

---

Made with ❤️ by [Vibey](https://adammatthewsteinberger.github.io/vibey/), Developed by [Adam Matthew Steinberger](https://hire.adam.matthewsteinberger.com/) ([@adammatthewsteinberger](https://github.com/adammatthewsteinberger/)).
