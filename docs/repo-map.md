# Grimo Repository map

This is a **locator**, not a second authority specification or a live progress report.

| Area | Role |
| --- | --- |
| `AGENTS.md` | Automatically read root execution and safety rules |
| `docs/grimo/knowledge/Goal√map.md` | Character production goal/WHY; tools and metrics are means |
| `docs/grimo/knowledge/GRIMO_PROJECT_KNOWLEDGE_INDEX.md` | Single entrypoint to canonical product, character, and workflow specs |
| `docs/grimo/knowledge/product/` | Formal four-screen, reward, inventory and data contracts |
| `DESIGN.md` | Formal application UI/UX design contract |
| `docs/production/Handoff.md` | Last verified cross-session pointer; not live approval |
| `docs/production/<character>/` | Per-character scoped working state, decisions and evidence; verify execution branch |
| `docs/production/motion/` | Working motion drafts, evidence and proposals; status may be DRAFT |
| `assets/grimo/source/` | Canonical identity and approved source inputs; provenance must be preserved |
| `assets/grimo/production/` | Candidate/generated character assets; not automatically canonical |
| `docs/grimo/knowledge/research/` | Measured and inferred references; not product authority |
| `docs/archive/` | Superseded work and historical prompts; not current instructions |
| `src/app/`, `src/components/` | Next.js routes, PWA UI and application shell |
| `src/domain/`, `src/data/`, `src/integrations/` | Domain logic, persistence, external service boundaries |
| `scripts/`, `tests/`, `.github/workflows/` | Tooling, targeted validation and CI |
| `public/` | Shipped browser-visible assets |
| `.agents/skills/`, `.codex/` | Optional task tooling and configuration |

**Branch boundary:** `main` is the shared docs and app base, not necessarily the latest 3D-production state. Feature branches can contain many additional sources, experiments and evidence. Do not merge or rewrite an active branch merely to reorganize it.

**Evidence hygiene:** Keep decision-useful comparisons and provenance. Do not automatically commit repeated disposable renders, browser traces, build logs or temporary experiments. Never delete existing evidence or move active production assets as part of routine cleanup.
