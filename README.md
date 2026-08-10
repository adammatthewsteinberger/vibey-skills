# vibe-engineering-skills

A [Claude Code plugin marketplace](https://docs.claude.com/en/docs/claude-code/plugins) of **18 plugins** and **71 skills** spanning security, compliance, cloud infrastructure, identity automation, DevSecOps, AI/ML, data engineering, frontend, mobile, software architecture, quality engineering, engineering process, and technical writing.

Each plugin bundles a set of [Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) — model-invoked instructions that Claude loads automatically when a task matches the skill's trigger description.

## Install as a marketplace

Add this repository as a marketplace, then install the plugins you want:

```bash
# Add the marketplace (from a local clone)
/plugin marketplace add /path/to/vibe-engineering-skills

# …or directly from the Git remote
/plugin marketplace add TheViziusGroup/vibe-engineering-skills

# Browse and install
/plugin
```

Once added, `/plugin install <name>@vibe-engineering-skills` installs any single plugin (for example `/plugin install security-principles@vibe-engineering-skills`).

The marketplace manifest lives at [.claude-plugin/marketplace.json](https://github.com/TheViziusGroup/vibe-engineering-skills/blob/main/.claude-plugin/marketplace.json); each plugin's source lives under [plugins/](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins).

## Install from PyPI

The same skills ship as a Python package, so you can install them into `~/.claude/skills`
without cloning:

```bash
# Try it without installing
uvx --from vibe-engineering-skills vibe-skills list

# Install every skill into ~/.claude/skills
uvx --from vibe-engineering-skills vibe-skills install --all

# …or just one plugin's skills
uvx --from vibe-engineering-skills vibe-skills install security-principles

# Or install the CLI permanently
pip install vibe-engineering-skills
vibe-skills list
```

Existing skill directories are never overwritten — `install` skips them and tells you which,
so re-run with `--force` if you actually want to replace them. `vibe-skills marketplace`
prints the path to the packaged manifest for `/plugin marketplace add`.

## Plugins

| Plugin | Version | Category | Skills | Covers |
|---|---|---|---|---|
| [agile-delivery](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/agile-delivery) | 0.1.0 | engineering-process | 3 | Security-First Scrum, delivery velocity, engineering metrics |
| [ai-and-data](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/ai-and-data) | 0.2.0 | ai | 4 | Data engineering, AI/ML landscape, RAG & agents, LLM cost optimization & compression |
| [ai-chatbot-strategy](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/ai-chatbot-strategy) | 0.1.0 | ai | 4 | Chatbot fundamentals, RAG for business, build/deploy, ROI |
| [azure-bootstrap](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/azure-bootstrap) | 0.2.0 | cloud-infrastructure | 4 | azure-bootstrap library (v3.0.0): v1 bootstrap, v2 primitives, ten logging transports, subpackages, v3 DB/email/HTTP/AKS/governance/scaffold, TypeScript integration |
| [azure-cloud-infra](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/azure-cloud-infra) | 0.2.0 | cloud-infrastructure | 3 | Azure RBAC, Kubernetes IaC, Azure service catalog |
| [compliance-frameworks](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/compliance-frameworks) | 0.1.0 | security | 5 | NIST 800-171, PCI-DSS v4, SOC 2, CMMC/CUI, OWASP SAMM |
| [devsecops-cicd](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/devsecops-cicd) | 0.2.0 | devops | 4 | DevSecOps pipelines, Bitbucket/Azure, CI/CD field guide, GitHub/Atlassian |
| [engineering-process](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/engineering-process) | 0.1.0 | engineering-process | 4 | Requirements, SDLC, process engineering, research methodology |
| [frontend-design](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/frontend-design) | 0.1.0 | frontend | 3 | Graphic/UX/UI design, Next.js patterns, performance optimization |
| [mobile-development](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/mobile-development) | 0.1.0 | frontend | 5 | React Native New Architecture, native iOS/Android, mobile UI/UX & patterns, Azure hosting/Intune/CI-CD, mobile security & MFA |
| [network-engineering](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/network-engineering) | 0.1.0 | cloud-infrastructure | 2 | Network fundamentals, modern stack (eBPF, Cilium, AKS) |
| [okta-api-reference](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/okta-api-reference) | 0.1.0 | cloud-infrastructure | 3 | Okta core Management API & Python SDK, Identity Governance (OIG) API surface, and the MCP server landscape for Okta core and IGA automation |
| [okta-workflows](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/okta-workflows) | 0.1.0 | cloud-infrastructure | 9 | Okta Workflows field guide for identity source-of-truth → Okta sync: branching, loops, Tables, hooks/streaming, Okta & Entra connectors, execution limits, error handling, flopack deployment — quirks, caps & verified workarounds |
| [quality-engineering](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/quality-engineering) | 0.2.0 | engineering-process | 3 | Python testing, test strategy, debugging & observability |
| [security-first-dev](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/security-first-dev) | 0.1.0 | security | 3 | Security-First Scrum, codebase modernization, cybersecurity implementation |
| [security-principles](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/security-principles) | 0.2.0 | security | 4 | Cybersecurity principles, threat modeling, AI-era security, AI safety |
| [software-architecture](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/software-architecture) | 0.2.0 | engineering-process | 3 | Production architecture, architecture patterns, software design |
| [writing-craft](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/writing-craft) | 0.1.0 | content | 5 | White papers, prose mechanics, technical prose, narrative, legal briefs |

See each plugin's `README.md` for its full skill list and trigger descriptions.

## Repository layout

```
.claude-plugin/marketplace.json   Marketplace manifest (the entry point Claude Code reads)
plugins/                          Authoritative plugin sources, one directory per plugin
  <plugin>/.claude-plugin/plugin.json   Plugin manifest
  <plugin>/README.md                    Plugin overview + skill list
  <plugin>/skills/<skill>/SKILL.md      Individual skill definition
src/vibe_engineering_skills/       Python package + `vibe-skills` CLI
tools/validate_manifests.py        Manifest and skill-frontmatter validator
README.md / CLAUDE.md             This guide + Claude Code conventions
.cursor/rules/claude.mdc          Cursor rules (aliases CLAUDE.md)
```

`plugins/` is the source of truth for the marketplace. The Python package maps that same
tree into the wheel rather than duplicating it, so there is exactly one copy of every skill.

## Authoring

To add or change a plugin:

1. Edit the plugin under `plugins/<name>/` — update `skills/<skill>/SKILL.md`, the plugin
   `README.md`, and bump `version` in `.claude-plugin/plugin.json`.
2. Mirror the `version`, `description`, and `category` into the matching entry in
   [.claude-plugin/marketplace.json](https://github.com/TheViziusGroup/vibe-engineering-skills/blob/main/.claude-plugin/marketplace.json).
3. Update the table in this README if the plugin's skill count or summary changes.
4. Run `python3 tools/validate_manifests.py`.

See [CONTRIBUTING.md](https://github.com/TheViziusGroup/vibe-engineering-skills/blob/main/CONTRIBUTING.md) for the full workflow and [CLAUDE.md](https://github.com/TheViziusGroup/vibe-engineering-skills/blob/main/CLAUDE.md) for
conventions and the SKILL.md format.

## License

[MIT](https://github.com/TheViziusGroup/vibe-engineering-skills/blob/main/LICENSE) © 2026 The Vizius Group.

Contributions are accepted under the same license — see [CONTRIBUTING.md](https://github.com/TheViziusGroup/vibe-engineering-skills/blob/main/CONTRIBUTING.md).
