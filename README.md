# Grimo

Grimo is a smartphone-first, local-first task management PWA built around four original characters: Carol, Jill, Pino, and Shushu.

## Main screens

- `/tasks` — Tasks
- `/calendar` — Calendar
- `/grimo` — Grimo
- Collection is a planned product surface; it is not implemented in Phase 0.

The existing Task, Calendar, Dexie/IndexedDB, Google read-only integrations, server-only Gemini boundary, and Serwist PWA foundation are preserved.

## Character architecture

The authoritative production direction is:

```text
Full 3D → Blender → GLB/glTF → PlayCanvas
```

`main` contains the stable Phase-0 application foundation. Current character-production artifacts and status may live on separate feature branches; verify the active execution branch and evidence rather than treating `main` as the latest production result.

## Development

```text
pnpm install
pnpm dev
```

For a lightweight local check, use `pnpm check:fast`. `pnpm check:full` and
the compatibility alias `pnpm verify` are intended for PR, release, or
troubleshooting validation, not as the default development command.

The reproducible 3D environment and diagnostics are documented in [`docs/setup/3D_TOOLCHAIN.md`](docs/setup/3D_TOOLCHAIN.md). The following are opt-in specialized checks, not a default checklist:

```text
pnpm 3d:doctor
pnpm 3d:playcanvas
pnpm 3d:validate:ci
pnpm qa:browser:smoke
```

## Project context

- [`AGENTS.md`](AGENTS.md) — local Codex rules and safety boundaries
- [Production Goal√map](docs/grimo/knowledge/Goal%E2%88%9Amap.md) — character production WHY, not the overall product loop
- [Knowledge index](docs/grimo/knowledge/GRIMO_PROJECT_KNOWLEDGE_INDEX.md) — canonical product, experience, technical and app specifications
- [Handoff](docs/production/Handoff.md) — last-known pointer only; check the actual execution branch
- [Repository map](docs/repo-map.md) — source, assets, evidence and history

Read only documents relevant to the current task. Historical Phase-0 prompts and task logs are in [`docs/archive/phase0/`](docs/archive/phase0/).
