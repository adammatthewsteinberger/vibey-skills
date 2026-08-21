# Usage

The console script is `vibey-skills`. `vibe-skills` — the short alias from the
`vibe-engineering-skills` era — still works but prints a one-line deprecation warning and
will be removed in a future release.

## Listing

```bash
vibey-skills list                       # every plugin, its skills, and trigger descriptions
vibey-skills list --plugin azure-cloud-infra
vibey-skills list --json                # machine-readable
```

## Installing

```bash
vibey-skills install --all                        # all 457 skills
vibey-skills install security-principles azure-cloud-infra
vibey-skills install --all --dest ./.claude/skills
vibey-skills install --all --dry-run              # print the plan, touch nothing
vibey-skills install --all --link                 # symlink instead of copy
```

## Conflicts and updates

`install` uses `cp -n` semantics: a destination that already exists is **skipped**, and the
skipped names are printed at the end. This is deliberate — the alternative silently destroys
a skill you edited locally.

```console
$ vibey-skills install --all
vibey-skills: copied 457 skill(s) into /Users/you/.claude/skills

$ vibey-skills install --all
vibey-skills: 457 skill(s) already present, skipped: agile-delivery, ...
vibey-skills: re-run with --force to overwrite
```

To update after a release, overwrite explicitly:

```bash
vibey-skills install --all --force
```

`--link` symlinks instead of copying, so skills track the installed package version and a
`uv tool upgrade` updates them in place.

## Locating the packaged files

```bash
vibey-skills path          # the packaged plugins/ root
vibey-skills marketplace   # the packaged marketplace.json, for /plugin marketplace add
```

## Programmatic use

```python
from vibey_skills import iter_skills, plugins_root

for skill in iter_skills():
    print(skill.plugin, skill.name, skill.path)
```
