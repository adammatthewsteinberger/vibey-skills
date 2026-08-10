# Usage

Two console scripts are installed and are interchangeable: `vibe-engineering-skills` and the
shorter `vibe-skills`.

## Listing

```bash
vibe-skills list                       # every plugin, its skills, and trigger descriptions
vibe-skills list --plugin azure-cloud-infra
vibe-skills list --json                # machine-readable
```

## Installing

```bash
vibe-skills install --all                        # all 71 skills
vibe-skills install security-principles azure-cloud-infra
vibe-skills install --all --dest ./.claude/skills
vibe-skills install --all --dry-run              # print the plan, touch nothing
vibe-skills install --all --link                 # symlink instead of copy
```

## Conflicts and updates

`install` uses `cp -n` semantics: a destination that already exists is **skipped**, and the
skipped names are printed at the end. This is deliberate — the alternative silently destroys
a skill you edited locally.

```console
$ vibe-skills install --all
vibe-skills: copied 71 skill(s) into /Users/you/.claude/skills

$ vibe-skills install --all
vibe-skills: 71 skill(s) already present, skipped: agile-delivery, ...
vibe-skills: re-run with --force to overwrite
```

To update after a release, overwrite explicitly:

```bash
vibe-skills install --all --force
```

`--link` symlinks instead of copying, so skills track the installed package version and a
`uv tool upgrade` updates them in place.

## Locating the packaged files

```bash
vibe-skills path          # the packaged plugins/ root
vibe-skills marketplace   # the packaged marketplace.json, for /plugin marketplace add
```

## Programmatic use

```python
from vibe_engineering_skills import iter_skills, plugins_root

for skill in iter_skills():
    print(skill.plugin, skill.name, skill.path)
```
