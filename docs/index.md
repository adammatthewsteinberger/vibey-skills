# vibe-engineering-skills

**18 plugins. 71 Agent Skills.** Evidence-grounded practitioner references for the parts of
software engineering an agent is most likely to get confidently wrong: security, compliance,
cloud infrastructure, identity automation, DevSecOps, AI/ML, data engineering, frontend,
mobile, architecture, quality engineering, process, and technical writing.

"Vibe engineering" is the disciplined counterpart to vibe coding — keeping an agent fast
*and* correct. These skills are the reference layer for that: each one is a long-form,
source-cited document rather than a prompt snippet, written so a model can act on it.

## Two ways to install

=== "Claude Code marketplace"

    ```bash
    /plugin marketplace add TheViziusGroup/vibe-engineering-skills
    /plugin install security-principles@vibe-engineering-skills
    ```

=== "PyPI (any agent)"

    ```bash
    uvx vibe-engineering-skills install --all
    ```

    Copies every skill into `~/.claude/skills`, which also works for any other harness
    that reads `SKILL.md`.

See [Installation](installation.md) for both routes in full, [Usage](usage.md) for the CLI,
and the [Skills reference](reference/index.md) for all 71 skills.

## What makes a skill here different

- **Sourced.** Claims cite the standard, vendor doc, or paper they come from.
- **Trigger-engineered.** A skill's `description` is the only thing a model sees when
  deciding whether to load it, so each one names the concrete tasks and terms that should
  activate it.
- **Self-contained.** No skill assumes another has been loaded.

## License

MIT. See [LICENSE](https://github.com/TheViziusGroup/vibe-engineering-skills/blob/main/LICENSE).
