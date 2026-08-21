# vibey-skills

> **47 Claude Code plugins. 210 Agent Skills.** Long-form, source-cited practitioner
> references for the parts of software engineering an agent is most likely to get
> confidently wrong — security, compliance, Azure, identity automation (Okta),
> DevSecOps, AI/ML, data engineering, frontend, mobile, desktop, smart TV, game development, UI/UX design, systems programming, embedded and IoT, blockchain, quantum computing, penetration testing, architecture, quality
> engineering, process, and technical writing. Install as a marketplace or from PyPI.

Formerly **vibe-engineering-skills** — see [NOTICE.md](https://github.com/adammatthewsteinberger/vibey-skills/blob/main/NOTICE.md).

[![PyPI](https://img.shields.io/pypi/v/vibey-skills.svg)](https://pypi.org/project/vibey-skills/)
[![Downloads](https://img.shields.io/pypi/dm/vibey-skills.svg)](https://pypi.org/project/vibey-skills/)
[![CI](https://github.com/adammatthewsteinberger/vibey-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/adammatthewsteinberger/vibey-skills/actions/workflows/ci.yml)
[![Docs](https://github.com/adammatthewsteinberger/vibey-skills/actions/workflows/docs.yml/badge.svg)](https://adammatthewsteinberger.github.io/vibey-skills/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/adammatthewsteinberger/vibey-skills/blob/main/LICENSE)

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
/plugin marketplace add adammatthewsteinberger/vibey-skills
/plugin install security-principles@vibey-skills
/plugin                                    # browse everything
```

**From PyPI** — same skills, any agent that reads `SKILL.md`:

```bash
uvx vibey-skills list                      # try it without installing
uvx vibey-skills install --all             # copy all 210 skills into ~/.claude/skills
uvx vibey-skills install security-principles azure-cloud-infra
```

Or install the CLI permanently with `uv tool install vibey-skills` /
`pip install vibey-skills` (Python 3.10+); `vibey-skills` is then on your PATH
(`vibe-skills` still works as a deprecated alias).

```console
$ vibey-skills list
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

`vibey-skills marketplace` prints the packaged manifest path for `/plugin marketplace add`;
`--dest`, `--link`, `--dry-run`, and `--force` are covered in the
[Usage docs](https://adammatthewsteinberger.github.io/vibey-skills/usage/).

### Migrating from vibe-engineering-skills

2.0.0 renames the project; the 18 plugins and 71 skills are unchanged.

| | 1.x (`vibe-engineering-skills`) | 2.0.0 (`vibey-skills`) |
|---|---|---|
| PyPI package | `pip install vibe-engineering-skills` | `pip install vibey-skills` |
| Python import | `import vibe_engineering_skills` | `import vibey_skills` |
| CLI | `vibe-engineering-skills`, `vibe-skills` | `vibey-skills` (`vibe-skills` kept as a deprecated alias; the long form is gone) |
| Marketplace | `/plugin marketplace add TheViziusGroup/vibe-engineering-skills` | `/plugin marketplace add adammatthewsteinberger/vibey-skills` |
| Plugin install | `<plugin>@vibe-engineering-skills` | `<plugin>@vibey-skills` |
| Docs | theviziusgroup.github.io/vibe-engineering-skills | [adammatthewsteinberger.github.io/vibey-skills](https://adammatthewsteinberger.github.io/vibey-skills/) |

Uninstall the old package (`pip uninstall vibe-engineering-skills` / `uv tool uninstall
vibe-engineering-skills`) and re-add the marketplace under its new name; skills already
copied into `~/.claude/skills` need no change.

## Plugins

Generated from `plugins/*/` and `.claude-plugin/marketplace.json`; every plugin has its
own `README.md` with the full skill list and trigger descriptions.

| Plugin | Version | Category | Skills | Covers |
|---|---|---|---|---|
| [agile-delivery](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/agile-delivery) | 0.1.0 | engineering-process | 3 | Security-First Scrum, delivery velocity, engineering metrics |
| [ai-and-data](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/ai-and-data) | 0.2.0 | ai | 4 | Data engineering, AI/ML landscape, RAG & agents, LLM cost optimization & compression |
| [ai-chatbot-strategy](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/ai-chatbot-strategy) | 0.1.0 | ai | 4 | Chatbot fundamentals, RAG for business, build/deploy, ROI |
| [algorithms-deep-dive](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/algorithms-deep-dive) | 0.1.0 | computer-science | 5 | Choosing structures, the machine model (cache/branches/SIMD), hash tables, trees & the B-tree/LSM divide, sorting, searching, graphs, strings, DP, probabilistic & streaming structures, vector search, concurrency, measurement |
| [assembly-programming](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/assembly-programming) | 0.1.0 | systems-programming | 4 | x86-64/AArch64/RISC-V, ABIs, toolchains, disassembly, performance, SIMD, systems & constant-time asm, inline asm |
| [azure-cloud-infra](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/azure-cloud-infra) | 0.2.0 | cloud-infrastructure | 3 | Azure RBAC, Kubernetes IaC, Azure service catalog |
| [cloud-computing](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/cloud-computing) | 0.1.0 | cloud-infrastructure | 5 | Service/deployment models, provider landscape, primitives, Well-Architected trade-offs, 2025 outage lessons, FinOps, shared responsibility, EU Data Act sovereignty, observability, migration, multi-cloud, AI workloads |
| [compliance-frameworks](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/compliance-frameworks) | 0.1.0 | security | 5 | NIST 800-171, PCI-DSS v4, SOC 2, CMMC/CUI, OWASP SAMM |
| [cryptocurrency-development](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/cryptocurrency-development) | 0.1.0 | blockchain | 4 | Protocol layer, clients, EIPs, EVM, Solidity, contract architecture, ERC standards, DeFi/MEV, testing, security, L2s, cross-chain, deployment |
| [design-patterns](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/design-patterns) | 0.1.0 | engineering-process | 5 | What a pattern is, the GoF audit, functional & data-oriented alternatives, DI, hexagonal/DDD/microservices, saga/outbox/CQRS/event sourcing, resilience & concurrency, LLM & agentic patterns, over-application anti-patterns |
| [desktop-apps-macos-linux](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/desktop-apps-macos-linux) | 0.1.0 | frontend | 5 | macOS & Linux architecture, SwiftUI/AppKit, GTK4/Qt6, Electron/Tauri/Flutter, Wayland/X11, native idioms, notarization/Flatpak/Snap, sandboxing |
| [devsecops-cicd](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/devsecops-cicd) | 0.2.0 | devops | 4 | DevSecOps pipelines, Bitbucket/Azure, CI/CD field guide, GitHub/Atlassian |
| [diy-kit-dev](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/diy-kit-dev) | 0.1.0 | embedded | 5 | Board choice, Raspberry Pi/Arduino/ESP32/Pico lineups, power, electronics fundamentals, sensors & actuators, Arduino/MicroPython/ESP-IDF, soldering & physical build, hardware debugging, home automation, enclosures, prototype→product |
| [ecommerce-development](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/ecommerce-development) | 0.2.0 | commerce | 4 | Payments architecture, auth/capture/settlement, idempotency & webhooks, Stripe/Adyen/PayPal, rails (cards/ACH/SEPA/BNPL/instant), SCA/3DS, fraud & chargebacks, PCI DSS, subscriptions, marketplaces, tax, Shopify/headless, checkout, agentic commerce |
| [embedded-iot-controls](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/embedded-iot-controls) | 0.1.0 | embedded | 5 | MCU silicon & peripherals, bare-metal/RTOS/embedded Linux, real-time patterns, OT/PLC/OPC UA, control theory, BLE/Thread/Matter/LoRaWAN/MQTT, OTA & fleet, CRA/IEC 62443, functional safety |
| [engineering-process](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/engineering-process) | 0.1.0 | engineering-process | 4 | Requirements, SDLC, process engineering, research methodology |
| [frontend-design](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/frontend-design) | 0.1.0 | frontend | 3 | Graphic/UX/UI design, Next.js patterns, performance optimization |
| [fundamental-physics](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/fundamental-physics) | 0.1.0 | physics | 5 | QM postulates & formalism, solved systems, QFT & renormalization, the Standard Model, special & general relativity, black holes & thermodynamics, gravitational waves, FLRW/ΛCDM cosmology, stellar structure, compact objects, dark matter, the measurement problem, QM/GR incompatibility |
| [low-code-no-code](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/low-code-no-code) | 0.1.0 | low-code | 5 | Taxonomy, Scratch/LEGO/micro:bit, n8n/Zapier/Make/Power Automate, AI app generation, iPaaS, ETL, app builders, RPA, when to write code instead, governance & shadow IT, licensing traps, security, escape hatches |
| [machine-learning](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/machine-learning) | 0.1.0 | ai | 4 | Framing, data & leakage, classical ML, deep learning, architectures, PyTorch/JAX, distributed training, fine-tuning/LoRA, evaluation, serving (vLLM/SGLang), MLOps, hardware |
| [math-science-programming](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/math-science-programming) | 0.1.0 | scientific-computing | 5 | Floating point, conditioning & stability, BLAS/LAPACK, MATLAB/NumPy/Julia/R/Fortran, symbolic computation, linear algebra, ODEs/PDEs, optimization, statistics, GPU & parallelism, verification & reproducibility |
| [media-engineering](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/media-engineering) | 0.1.0 | media | 5 | Digital media fundamentals, containers & muxing, audio/video codecs, DAWs & plugin formats, colour & timecode, LUFS loudness, transcoding & ABR packaging, HLS/DASH/CMAF/WebRTC/MoQ, DRM, captions, podcast infra & dynamic ad insertion, rights identifiers, AI generation & licensing |
| [mobile-development](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/mobile-development) | 0.1.0 | frontend | 5 | React Native New Architecture, native iOS/Android, mobile UI/UX & patterns, Azure hosting/Intune/CI-CD, mobile security & MFA |
| [network-engineering](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/network-engineering) | 0.1.0 | cloud-infrastructure | 2 | Network fundamentals, modern stack (eBPF, Cilium, AKS) |
| [okta-api-reference](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/okta-api-reference) | 0.1.0 | cloud-infrastructure | 3 | Okta core Management API & Python SDK, Identity Governance (OIG) API surface, MCP server landscape for Okta core and IGA automation |
| [okta-workflows](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/okta-workflows) | 0.1.0 | cloud-infrastructure | 9 | Okta Workflows field guide for identity source-of-truth → Okta sync: branching, loops, Tables, hooks/streaming, Okta & Entra connectors, execution limits, error handling, flopack deployment — quirks, caps & verified workarounds |
| [os-development-kernel-shell](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/os-development-kernel-shell) | 0.1.0 | systems-programming | 5 | Kernel architecture, kernel C/Rust, concurrency, syscalls/ABI, eBPF, boot & init, containers, debugging/tracing, hardening, shell semantics, defensive scripting |
| [package-manager-development](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/package-manager-development) | 0.1.0 | systems-programming | 5 | Versioning, manifests, resolvers (PubGrub/SAT/MVS), lockfiles, registries, install layouts, publishing/OIDC/Sigstore, supply chain, workspaces, ecosystem comparison |
| [penetration-testing](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/penetration-testing) | 0.1.0 | security | 4 | Authorization & law (CFAA, RoE, bug bounty), scoping, methodology (PTES/WSTG/NIST 800-115/ATT&CK), recon, web/network/AD/cloud/API/mobile/wireless/OT testing, social engineering, red/purple teaming, AI-system testing, reporting, disclosure & certs |
| [programming-language-development](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/programming-language-development) | 0.1.0 | systems-programming | 5 | Language design, parsing, type systems, IRs (SSA/CPS/MLIR), optimization, backends (LLVM/Cranelift/Wasm), runtimes & GC, interpreters/JITs, diagnostics, IDE support, evolution |
| [quality-engineering](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/quality-engineering) | 0.2.0 | engineering-process | 3 | Python testing, test strategy, debugging & observability |
| [quantum-computing](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/quantum-computing) | 0.1.0 | emerging-tech | 5 | Foundations, capabilities & limits, algorithm canon, NISQ noise, error correction, hardware modalities, Qiskit/Cirq/PennyLane/CUDA-Q, resource estimation, advantage claims, PQC migration |
| [robotics-software](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/robotics-software) | 0.1.0 | robotics | 5 | Robot stack, ROS 2 & DDS, perception & sensor fusion, state estimation & SLAM, motion planning, PID→MPC & whole-body control, manipulation, RL/imitation/VLA models, sim-to-real, real-time & safety, ISO 10218:2025, DO-178C |
| [rocket-science](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/rocket-science) | 0.1.0 | aerospace | 5 | Rocket equation & staging, nozzle thermodynamics & isentropic flow, combustion chamber & c*, turbomachinery & engine cycles, regenerative cooling, propellants, orbital mechanics & patched conics, ascent trajectory, aero loads, tank structures, guidance & TVC, reentry heating, failure physics |
| [security-first-dev](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/security-first-dev) | 0.1.0 | security | 3 | Security-First Scrum, codebase modernization, cybersecurity implementation |
| [security-principles](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/security-principles) | 0.2.0 | security | 4 | Cybersecurity principles, threat modeling, AI-era security, AI safety |
| [signal-processing](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/signal-processing) | 0.1.0 | scientific-computing | 5 | Sampling & aliasing, quantization, FFT & windowing traps, FIR/IIR filter design, convolution, multirate, adaptive filtering, spectral analysis, audio & speech, RF/SDR, images & video, fixed-point & real-time, classical vs. learned |
| [smart-tv-app-development](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/smart-tv-app-development) | 0.1.0 | frontend | 4 | Roku/Tizen/webOS/Android TV/Fire OS/tvOS, 10-foot UI, focus & remote input, HLS/DASH playback, DRM, constrained-device performance, deep linking, CTV ads, certification |
| [social-media-engineering](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/social-media-engineering) | 0.1.0 | social | 5 | Platform APIs & pricing shocks, ActivityPub & AT Protocol, feed/timeline fan-out, social graphs, ranking, notifications, moderation at scale, spam & abuse, DSA/OSA/age assurance, media handling, experimentation, privacy & deletion, developer presence |
| [software-architecture](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/software-architecture) | 0.2.0 | engineering-process | 3 | Production architecture, architecture patterns, software design |
| [theory-of-computation](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/theory-of-computation) | 0.1.0 | computer-science | 5 | Automata & the Chomsky hierarchy, regex & ReDoS, parsing & grammar classes, halting & Rice's theorem, complexity classes, NP-hardness escape hatches, SAT/SMT, fine-grained complexity, space & streaming, FLP/CAP, Curry–Howard, randomization |
| [ui-ux-design-principles](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/ui-ux-design-principles) | 0.1.0 | frontend | 5 | Perception & cognition, heuristics, IA & navigation, interaction per form factor, layout, visual design, design tokens, HIG/Material/Fluent, WCAG 2.2/EAA/APCA, UX writing, research, dark patterns, AI-era UI |
| [vibey-bootstrap](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/vibey-bootstrap) | 0.3.0 | cloud-infrastructure | 4 | The [vibey-bootstrap](https://github.com/adammatthewsteinberger/vibey-bootstrap) library (v4.0.0, formerly `azure-bootstrap`): 4-phase bootstrap, v2 primitives, ten logging transports, subpackages, v3 DB/email/HTTP/AKS/governance/scaffold, TypeScript integration |
| [video-game-development](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/video-game-development) | 0.1.0 | game-development | 5 | Engines, game loop, ECS, rendering, physics, animation, audio, gameplay AI, netcode (rollback/prediction), pipelines, frame budgets, game feel, shipping, production & business |
| [web-browser-development](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/web-browser-development) | 0.1.0 | systems-programming | 5 | Engine landscape, process model & sandboxing, networking, HTML/DOM, CSS, layout/paint/compositing, JS integration, security model, privacy, extensions, standards & interop |
| [web-scraping](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/web-scraping) | 0.1.0 | data-engineering | 5 | CFAA & the hiQ line, contract/ToS exposure, DMCA §1201, copyright & GDPR, EU AI Act, robots.txt & the crawl-permission layer, tool ladder (requests/curl_cffi/Scrapy/Playwright), parsing, bot detection, scale & data quality, AI/RAG corpora, running a site |
| [writing-craft](https://github.com/adammatthewsteinberger/vibey-skills/tree/main/plugins/writing-craft) | 0.1.0 | content | 5 | White papers, prose mechanics, technical prose, narrative, legal briefs |

Browse every skill's full text on the
[Skills reference](https://adammatthewsteinberger.github.io/vibey-skills/reference/).

## How it works

```
.claude-plugin/marketplace.json         Marketplace manifest — the entry point Claude Code reads
plugins/<plugin>/.claude-plugin/plugin.json   Plugin manifest
plugins/<plugin>/README.md              Plugin overview + skill list
plugins/<plugin>/skills/<skill>/SKILL.md      One skill: YAML frontmatter (name, trigger) + the reference
src/vibey_skills/                       Python package + `vibey-skills` CLI (stdlib only)
tools/validate_manifests.py             Manifest and skill-frontmatter validator
tools/check_links.py                    Hermetic link checker (README is also the PyPI long description)
```

CI validates every manifest and frontmatter, checks that the built wheel carries every
`SKILL.md`, smoke-tests `vibey-skills install --all` from the wheel, and builds the docs
site with `mkdocs build --strict` so a dead link on any of the 71 generated pages fails
the build.

## Docs & links

- **[Documentation site](https://adammatthewsteinberger.github.io/vibey-skills/)** — [Installation](https://adammatthewsteinberger.github.io/vibey-skills/installation/) · [Usage](https://adammatthewsteinberger.github.io/vibey-skills/usage/) · [Skills reference](https://adammatthewsteinberger.github.io/vibey-skills/reference/) (one page per plugin and per skill)
- **[PyPI](https://pypi.org/project/vibey-skills/)** · **[Releases](https://github.com/adammatthewsteinberger/vibey-skills/releases)** · **[Issues](https://github.com/adammatthewsteinberger/vibey-skills/issues)**
- **[CONTRIBUTING.md](https://github.com/adammatthewsteinberger/vibey-skills/blob/main/CONTRIBUTING.md)** · **[SECURITY.md](https://github.com/adammatthewsteinberger/vibey-skills/blob/main/SECURITY.md)** · **[CODE_OF_CONDUCT.md](https://github.com/adammatthewsteinberger/vibey-skills/blob/main/CODE_OF_CONDUCT.md)** · **[CLAUDE.md](https://github.com/adammatthewsteinberger/vibey-skills/blob/main/CLAUDE.md)** (conventions and the `SKILL.md` format)
- Claude Code docs: [Plugins](https://code.claude.com/docs/en/plugins) · [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces) · [Agent Skills](https://code.claude.com/docs/en/skills)

## Related projects

Part of the same open-source family — MIT, on PyPI:

- **[engineering-influence-skills](https://github.com/adammatthewsteinberger/engineering-influence-skills)** — companion plugin: a 14-phase content-engineering pipeline for long-form writing
- **[claudeloop](https://github.com/adammatthewsteinberger/claudeloop)** · **[codexloop](https://github.com/adammatthewsteinberger/codexloop)** · **[cursorloop](https://github.com/adammatthewsteinberger/cursorloop)** · **[agyloop](https://github.com/adammatthewsteinberger/agyloop)** — autonomous coding-session runners with the same contract, different vendor
- **[vibey](https://github.com/adammatthewsteinberger/vibey)** — six-phase queue conductor over the loop runners
- **[vibey-bootstrap](https://github.com/adammatthewsteinberger/vibey-bootstrap)** — the Azure Functions cross-cutting layer the `vibey-bootstrap` plugin documents (formerly `azure-bootstrap`)
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
[CONTRIBUTING.md](https://github.com/adammatthewsteinberger/vibey-skills/blob/main/CONTRIBUTING.md)
and [CLAUDE.md](https://github.com/adammatthewsteinberger/vibey-skills/blob/main/CLAUDE.md).

## License & attribution

[MIT](https://github.com/adammatthewsteinberger/vibey-skills/blob/main/LICENSE) © 2026 The Vizius Group and Adam Matthew Steinberger.
Contributions are accepted under the same license.

vibey-skills was originally developed as `TheViziusGroup/vibe-engineering-skills` by Adam
Matthew Steinberger while at The Vizius Group, and is republished here with the permission of
The Vizius Group — see [NOTICE.md](https://github.com/adammatthewsteinberger/vibey-skills/blob/main/NOTICE.md).

---

Built by [Adam Matthew Steinberger](https://hire.adam.matthewsteinberger.com) · [more open source](https://hire.adam.matthewsteinberger.com/open-source)
