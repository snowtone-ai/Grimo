# PHASE 0 — Repository / Branch Reset

Updated: 2026-09-15 JST

## Current position

Active work is on `codex/phase0-3d-repository-reset`, created from the synchronized `main`. The pre-reset Carol/Pixi state is recoverable through `pre-3d-phase0-20260915`.

## Acceptance state

- [x] Safety reference created before cleanup
- [x] New active branch created from `main`
- [x] Full 3D → Blender → GLB/glTF → PlayCanvas recorded as the current direction
- [x] Task / Calendar / Google / Gemini / PWA foundations preserved
- [x] App icon and four canonical identity images preserved
- [x] Obsolete 2D/2.5D references removed from active assets
- [x] Historical source-pack isolated under `docs/archive/obsolete-2_5d/`
- [x] Install, typecheck, tests, lint, build, and verify completed
- [x] Phase 0 commit created and pushed
- [ ] Human Gate review of this branch

## 2026-09-15 — Full 3D environment bootstrap

- [x] Blender 5.2.1 LTS, headless bpy execution, and official Blender Lab extensions verified
- [x] Official Blender Lab MCP registered and live localhost bridge tested with temporary object create/delete
- [x] PlayCanvas 2.22.2, `@playcanvas/react` 0.11.5, and `sync-ammo` 0.1.2 resolved and imported
- [x] Official PlayCanvas Skills plugin and Editor MCP registration completed
- [x] GLB validator/metrics scripts, Git LFS policy, Sentry opt-in scaffold, and mobile Playwright smoke added
- [x] Chrome DevTools MCP snapshot, network, Lighthouse, and performance trace smoke completed
- [x] Android Platform Tools 37.0.1 verified; Xiaomi 14T Pro is connected as the real-device QA target (`adb devices -l` reports `device`; Pixel 7a-class remains the minimum acceptance baseline)
- [x] KTX-Software 4.4.2 Windows x64 executable installed and directly verified (`ktx`, `toktx`, `ktx2check` all report v4.4.2)
- [x] PlayCanvas Editor project connection completed; Grimo / Untitled is connected and read-only verified

## 2026-09-15 — Frontend production and QA toolchain bootstrap

- [x] Storybook 10.6.0 with `@storybook/nextjs-vite`, MCP, Vitest browser tests, a11y checks, and component manifest configured
- [x] Official Storybook agent skills, Vercel React best-practices, Vercel web-design-guidelines, and local `grimo-frontend` operational skill installed
- [x] Motion 13.3.0 exact-pinned for DOM UI only; no Radix package bulk install and no generic UI library added
- [x] Playwright visual foundation added for Pixel 7a-like viewport and Xiaomi 14T Pro-like viewport; physical Xiaomi QA remains separate
- [x] `frontend:doctor`, Storybook build, interaction/a11y tests, and opt-in visual baseline workflow verified
- [x] Storybook MCP registered as `storybook`; Figma registration was inspected only and not reinstalled

## Next operation

Carol production infrastructure bootstrap is complete. Next operation is the GPT-6 Astra / Medium geometry interpretation session. Do not begin routine Blender blockout until `docs/production/carol/CAROL_GEOMETRY_DECISION.md` is completed.

## 2026-09-16 — Carol production infrastructure

- [x] Repository-scoped documented Codex multi-agent feature disabled
- [x] Carol camera/modeling/state/geometry/review contracts created
- [x] Carol production asset directories created without placeholder binaries
- [x] Blender Gate-render and deterministic review-packet scaffolding created
- [x] Next-session handoff written to root `prompt.md`
- [x] Ingest the authoritative `CAROL_MVP_MOTION_SPEC.md` and approved Carol 3D references; record hashes and authority paths
- [ ] GPT-6 Astra / Medium initial geometry interpretation and Human Gate

## 2026-09-16 — Phase 0 final reconciliation

- [x] Eevee Motion Master is stored under `docs/grimo/knowledge/research/motion-masters/` with the Pikachu Motion Master
- [x] Carol approved 3D authority manifest and Motion Spec are available from their formal paths
- [x] Active state and handoff records no longer report source-ingestion blockage
- [x] Next session handoff targets GPT-6 Astra / Medium geometry interpretation
- [ ] Human Gate review of the reconciled Phase 0 branch

## Unresolved

- Collection remains a planned product surface and is intentionally not implemented in Phase 0.
- Lighthouse CI direct collection passes; the full local autorun can exit after the audit on this Windows host when `chrome-launcher` cannot remove its temporary profile (`EPERM`).
