# Long-lived decisions / historical decision log

**Current status:** Entries dated before 2026-09-23 are historical decisions.
They remain useful provenance unless explicitly superseded below, but they must
not override active Project Knowledge or current mutable production state.

## 2026-09-23 — Goal-Backward production system

Current durable routing:

- Product Goal / quality: `GRIMO_PRODUCT_NORTH_STAR_AND_MINIMUM_REQUIREMENTS.md`
- Experience: `GRIMO_CHARACTER_EXPERIENCE_SPEC.md`
- Architecture: `GRIMO_CHARACTER_PRODUCTION_ARCHITECTURE.md`
- Workflow: `GRIMO_PRODUCTION_OPERATING_SYSTEM.md`
- Mutable Carol state: `docs/production/carol/CAROL_PRODUCTION_STATE.md`

The prior “Full 3D is authoritative” wording is superseded by
**Front-Optimized 3D-First Living Character Architecture as a falsifiable
baseline hypothesis**. Prior geometry-first gate ordering, mandatory static
perfection before representative motion/runtime, and fixed model-routing rules
are superseded.

Technical Hygiene is subordinate to Experience and Functional consequences.
Two bounded failures on essentially the same blocker trigger Architecture Review
before attempt 3.

---

## Historical entries

## 2026-09-15 — Full 3D production baseline

Grimo's authoritative character architecture is Full 3D. Blender is the centered production tool, GLB/glTF is the interchange and shipping format, and PlayCanvas is the planned browser runtime. Phase 0 is repository cleanup only; it does not begin 3D implementation.

Old PixiJS, 2D, and 2.5D implementation is obsolete. Historical material is isolated under `docs/archive/obsolete-2_5d/` and is not a current source of truth.

## 2026-09-15 — Preserve independent foundations

Task and Calendar behavior, Dexie/IndexedDB compatibility, legacy backup recovery, Google read-only integrations, server-only Gemini handling, PWA behavior, the four canonical identity images, and the current app icon remain independent of the character runtime reset.

## 2026-09-15 — Product information architecture

Primary navigation remains Tasks / Grimo / Calendar. Settings is secondary navigation. Collection is a planned surface and is not implemented as part of Phase 0.

## 2026-09-15 — Data and security boundaries

The initial database preserves the existing `TaskManagerDB` tables and migrations. No reward, collection, or character database is added in Phase 0. Google access remains browser OAuth with read-only Gmail and Calendar scopes; access tokens remain memory-only. `GEMINI_API_KEY` remains server-only behind the existing fixed-purpose API route. Secrets are never committed.

## 2026-09-15 — Human acceptance

Future character identity and interaction work requires a full-screen Chrome Human Gate. Automated checks support but do not replace human aesthetic acceptance.

## 2026-09-15 — Reproducible 3D toolchain

The 3D environment uses exact-pinned Blender 5.2.1 LTS, official Blender Lab MCP, PlayCanvas 2.22.2, `@playcanvas/react` 0.11.5, `sync-ammo` 0.1.2, glTF Transform 4.5.0, and Khronos `gltf-validator` 2.0.0-dev.3.10. The official PlayCanvas Skills plugin is installed through the current Codex marketplace integration. Editor MCP is an inspection/preview/QA surface and does not replace Git, Blender, GLB, or TypeScript as source of truth.

The GLB pipeline is asset-optional until Carol exists: CI validates all committed `.glb`/`.gltf` assets when present and otherwise exits successfully. KTX-Software 4.4.2 is selected as the stable Windows texture-tool baseline; no source texture is converted during bootstrap. Automatic upgrades of Blender, rig extensions, PlayCanvas, physics, or MCP are prohibited; upgrades require a branch, automated checks, visual regression, Human Gate, and deliberate merge.

## 2026-09-13 — Repository origin

The product is rebuilt in `snowtone-ai/Grimo` rather than continuing to modify the old `snowtone-ai/grimoire` repository. The old repository remains a read-only behavioral reference for Task/Calendar persistence, backup, Google integrations, and security boundaries; its old UI and gamification are not design authority.

## 2026-09-15 — Frontend production and QA toolchain

Storybook 10.6.0 with `@storybook/nextjs-vite` is the isolated component surface; Playwright is the screen-level browser and visual surface. Storybook MCP is localhost-only and registered as `storybook`. Vitest browser mode is the Storybook interaction/a11y gate. A small Windows path compatibility transform is kept inside the Vitest project because Storybook's generated file-URL execution guard otherwise skips every story on this host.

Motion 13.3.0 is exact-pinned and permitted only for DOM/React UI motion. Radix is not a design system for Grimo: install only a directly-needed primitive, exact-pin it, and author all appearance in Grimo CSS/Tailwind. MUI, Chakra, Ant Design, Bootstrap, Mantine, and a full shadcn/ui library are prohibited. Local Storybook plus Playwright is preferred over Chromatic until team/PR snapshot requirements justify a hosted service.

## 2026-09-16 — Carol interpretation gate before modeling

Carol's first 3D production milestone is an evidence-based geometry interpretation recorded in `docs/production/carol/CAROL_GEOMETRY_DECISION.md`. GPT-6 Astra / Medium owns that interpretation and critical face/identity decisions; Sol Medium owns subsequent non-trivial Blender production. Routine modeling must not start before the decision is complete. The repository-scoped documented `multi_agent` feature is disabled for this write-heavy Carol workflow. Missing references and measurements remain explicit blockers rather than being guessed.
