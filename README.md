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

The repository reset does not implement the 3D runtime, Blender assets, character motion, or touch interaction. The current `/grimo` route is intentionally a neutral placeholder until the Phase 1 foundation work begins.

## Development

```text
pnpm install
pnpm verify
```

The reproducible 3D environment and diagnostics are documented in [`docs/setup/3D_TOOLCHAIN.md`](docs/setup/3D_TOOLCHAIN.md). Useful checks are:

```text
pnpm 3d:doctor
pnpm 3d:playcanvas
pnpm 3d:validate:ci
pnpm qa:browser:smoke
```

Read `AGENTS.md`, `DESIGN.md`, `tasks.md`, and the relevant `docs/` files before implementation work.
