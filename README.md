# vibe-engineering-skills

> **18 Claude Code plugins. 71 Agent Skills.** Long-form, source-cited practitioner
> references for the parts of software engineering an agent is most likely to get
> confidently wrong — security, compliance, Azure, identity automation (Okta),
> DevSecOps, AI/ML, data engineering, frontend, mobile, architecture, quality
> engineering, process, and technical writing. Install as a marketplace or from PyPI.

[![PyPI](https://img.shields.io/pypi/v/vibe-engineering-skills.svg)](https://pypi.org/project/vibe-engineering-skills/)
[![Downloads](https://img.shields.io/pypi/dm/vibe-engineering-skills.svg)](https://pypi.org/project/vibe-engineering-skills/)
[![CI](https://github.com/TheViziusGroup/vibe-engineering-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/TheViziusGroup/vibe-engineering-skills/actions/workflows/ci.yml)
[![Docs](https://github.com/TheViziusGroup/vibe-engineering-skills/actions/workflows/docs.yml/badge.svg)](https://theviziusgroup.github.io/vibe-engineering-skills/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/TheViziusGroup/vibe-engineering-skills/blob/main/LICENSE)

## Why

"Vibe engineering" is the disciplined counterpart to vibe coding: keep the agent
fast *and* correct. These skills are the reference layer for that.

- **Each skill is a document, not a prompt snippet.** A `SKILL.md` is a long-form,
  source-cited reference (STRIDE → MITRE ATT&CK, NIST 800-171 control families,
  Okta Workflows record caps, React Native New Architecture) written so a model can
  act on it. Claude loads it automatically when a task matches the trigger description.
- **One source of truth.** `plugins/` is the marketplace tree Claude Code reads; the
  PyPI wheel maps that same tree in at build time. There is exactly one copy of every skill.
- **Zero runtime dependencies.** `uvx` runs the CLI with no resolution step. Skills
  install into `~/.claude/skills`, which any harness that reads `SKILL.md` can use.
- **Nothing overwritten.** `install` skips skill directories that already exist and
  tells you which; `--force` is explicit.

## Quick start

**In Claude Code** — add the marketplace, then install the plugins you want:

```bash
/plugin marketplace add TheViziusGroup/vibe-engineering-skills
/plugin install security-principles@vibe-engineering-skills
/plugin                                    # browse everything
```

**From PyPI** — same skills, any agent that reads `SKILL.md`:

```bash
uvx vibe-engineering-skills list           # try it without installing
uvx vibe-engineering-skills install --all  # copy all 71 skills into ~/.claude/skills
uvx vibe-engineering-skills install security-principles azure-cloud-infra
```

Or install the CLI permanently with `uv tool install vibe-engineering-skills` /
`pip install vibe-engineering-skills` (Python 3.10+); both `vibe-skills` and
`vibe-engineering-skills` are then on your PATH.

```console
$ vibe-skills list
agile-delivery  (0.1.0, engineering-process, 3 skills)
  - delivery-velocity
  - engineering-metrics
  - security-first-agile

ai-and-data  (0.2.0, ai, 4 skills)
  - ai-ml-landscape
  - data-engineering
  - llm-cost-optimization
  - rag-and-agents
…
```

`vibe-skills marketplace` prints the packaged manifest path for `/plugin marketplace add`;
`--dest`, `--link`, `--dry-run`, and `--force` are covered in the
[Usage docs](https://theviziusgroup.github.io/vibe-engineering-skills/usage/).

## Plugins

Generated from `plugins/*/` and `.claude-plugin/marketplace.json`; every plugin has its
own `README.md` with the full skill list and trigger descriptions.

| Plugin | Version | Category | Skills | Covers |
|---|---|---|---|---|
| [agile-delivery](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/agile-delivery) | 0.1.0 | engineering-process | 3 | Security-First Scrum, delivery velocity, engineering metrics |
| [ai-and-data](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/ai-and-data) | 0.2.0 | ai | 4 | Data engineering, AI/ML landscape, RAG & agents, LLM cost optimization & compression |
| [ai-chatbot-strategy](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/ai-chatbot-strategy) | 0.1.0 | ai | 4 | Chatbot fundamentals, RAG for business, build/deploy, ROI |
| [azure-bootstrap](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/azure-bootstrap) | 0.2.0 | cloud-infrastructure | 4 | The [azure-bootstrap](https://github.com/adammatthewsteinberger/azure-bootstrap) library (v3): 4-phase bootstrap, v2 primitives, ten logging transports, subpackages, v3 DB/email/HTTP/AKS/governance/scaffold, TypeScript integration |
| [azure-cloud-infra](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/azure-cloud-infra) | 0.2.0 | cloud-infrastructure | 3 | Azure RBAC, Kubernetes IaC, Azure service catalog |
| [compliance-frameworks](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/compliance-frameworks) | 0.1.0 | security | 5 | NIST 800-171, PCI-DSS v4, SOC 2, CMMC/CUI, OWASP SAMM |
| [devsecops-cicd](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/devsecops-cicd) | 0.2.0 | devops | 4 | DevSecOps pipelines, Bitbucket/Azure, CI/CD field guide, GitHub/Atlassian |
| [engineering-process](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/engineering-process) | 0.1.0 | engineering-process | 4 | Requirements, SDLC, process engineering, research methodology |
| [frontend-design](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/frontend-design) | 0.1.0 | frontend | 3 | Graphic/UX/UI design, Next.js patterns, performance optimization |
| [mobile-development](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/mobile-development) | 0.1.0 | frontend | 5 | React Native New Architecture, native iOS/Android, mobile UI/UX & patterns, Azure hosting/Intune/CI-CD, mobile security & MFA |
| [network-engineering](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/network-engineering) | 0.1.0 | cloud-infrastructure | 2 | Network fundamentals, modern stack (eBPF, Cilium, AKS) |
| [okta-api-reference](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/okta-api-reference) | 0.1.0 | cloud-infrastructure | 3 | Okta core Management API & Python SDK, Identity Governance (OIG) API surface, MCP server landscape for Okta core and IGA automation |
| [okta-workflows](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/okta-workflows) | 0.1.0 | cloud-infrastructure | 9 | Okta Workflows field guide for identity source-of-truth → Okta sync: branching, loops, Tables, hooks/streaming, Okta & Entra connectors, execution limits, error handling, flopack deployment — quirks, caps & verified workarounds |
| [quality-engineering](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/quality-engineering) | 0.2.0 | engineering-process | 3 | Python testing, test strategy, debugging & observability |
| [security-first-dev](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/security-first-dev) | 0.1.0 | security | 3 | Security-First Scrum, codebase modernization, cybersecurity implementation |
| [security-principles](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/security-principles) | 0.2.0 | security | 4 | Cybersecurity principles, threat modeling, AI-era security, AI safety |
| [software-architecture](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/software-architecture) | 0.2.0 | engineering-process | 3 | Production architecture, architecture patterns, software design |
| [writing-craft](https://github.com/TheViziusGroup/vibe-engineering-skills/tree/main/plugins/writing-craft) | 0.1.0 | content | 5 | White papers, prose mechanics, technical prose, narrative, legal briefs |

Browse every skill's full text on the
[Skills reference](https://theviziusgroup.github.io/vibe-engineering-skills/reference/).

## How it works

```
.claude-plugin/marketplace.json         Marketplace manifest — the entry point Claude Code reads
plugins/<plugin>/.claude-plugin/plugin.json   Plugin manifest
plugins/<plugin>/README.md              Plugin overview + skill list
plugins/<plugin>/skills/<skill>/SKILL.md      One skill: YAML frontmatter (name, trigger) + the reference
src/vibe_engineering_skills/            Python package + `vibe-skills` CLI (stdlib only)
tools/validate_manifests.py             Manifest and skill-frontmatter validator
tools/check_links.py                    Hermetic link checker (README is also the PyPI long description)
```

CI validates every manifest and frontmatter, checks that the built wheel carries every
`SKILL.md`, smoke-tests `vibe-skills install --all` from the wheel, and builds the docs
site with `mkdocs build --strict` so a dead link on any of the 71 generated pages fails
the build.

## Docs & links

- **[Documentation site](https://theviziusgroup.github.io/vibe-engineering-skills/)** — [Installation](https://theviziusgroup.github.io/vibe-engineering-skills/installation/) · [Usage](https://theviziusgroup.github.io/vibe-engineering-skills/usage/) · [Skills reference](https://theviziusgroup.github.io/vibe-engineering-skills/reference/) (one page per plugin and per skill)
- **[PyPI](https://pypi.org/project/vibe-engineering-skills/)** · **[Releases](https://github.com/TheViziusGroup/vibe-engineering-skills/releases)** · **[Issues](https://github.com/TheViziusGroup/vibe-engineering-skills/issues)**
- **[CONTRIBUTING.md](https://github.com/TheViziusGroup/vibe-engineering-skills/blob/main/CONTRIBUTING.md)** · **[SECURITY.md](https://github.com/TheViziusGroup/vibe-engineering-skills/blob/main/SECURITY.md)** · **[CODE_OF_CONDUCT.md](https://github.com/TheViziusGroup/vibe-engineering-skills/blob/main/CODE_OF_CONDUCT.md)** · **[CLAUDE.md](https://github.com/TheViziusGroup/vibe-engineering-skills/blob/main/CLAUDE.md)** (conventions and the `SKILL.md` format)
- Claude Code docs: [Plugins](https://code.claude.com/docs/en/plugins) · [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) · [Agent Skills](https://code.claude.com/docs/en/skills)

## Related projects

Part of the same open-source family — MIT, on PyPI:

- **[content-pipeline-skills](https://github.com/adammatthewsteinberger/content-pipeline-skills)** — companion plugin: a 14-phase content-engineering pipeline for long-form writing
- **[claudeloop](https://github.com/adammatthewsteinberger/claudeloop)** · **[codexloop](https://github.com/adammatthewsteinberger/codexloop)** · **[cursorloop](https://github.com/adammatthewsteinberger/cursorloop)** · **[agyloop](https://github.com/adammatthewsteinberger/agyloop)** — autonomous coding-session runners with the same contract, different vendor
- **[vibey](https://github.com/adammatthewsteinberger/vibey)** — six-phase queue conductor over the loop runners
- **[azure-bootstrap](https://github.com/adammatthewsteinberger/azure-bootstrap)** — the Azure Functions cross-cutting layer the `azure-bootstrap` plugin documents
- **[homebrew-tap](https://github.com/adammatthewsteinberger/homebrew-tap)** — `brew tap adammatthewsteinberger/tap`
- **[clippy-pet](https://github.com/adammatthewsteinberger/clippy-pet)** — the fun one

## Contributing

Nearly every contribution is Markdown (skill content) or JSON (manifests). To add or
change a plugin: edit under `plugins/<name>/`, bump `version` in its `plugin.json`,
mirror `version` / `description` / `category` into `marketplace.json`, update the table
above if the skill count or summary changed, then:

```bash
python3 tools/validate_manifests.py
python3 tools/check_links.py
pip install -e ".[docs]" && mkdocs build --strict
```

Branch from `develop`; PRs need green CI. Full workflow and the `SKILL.md` format:
[CONTRIBUTING.md](https://github.com/TheViziusGroup/vibe-engineering-skills/blob/main/CONTRIBUTING.md)
and [CLAUDE.md](https://github.com/TheViziusGroup/vibe-engineering-skills/blob/main/CLAUDE.md).

## License

[MIT](https://github.com/TheViziusGroup/vibe-engineering-skills/blob/main/LICENSE) © 2026 The Vizius Group.
Contributions are accepted under the same license.

---

Built by [Adam Matthew Steinberger](https://hire.adam.matthewsteinberger.com) · [more open source](https://hire.adam.matthewsteinberger.com/open-source)
