# Long-lived decisions

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

## 2026-09-13 — Repository origin

The product is rebuilt in `snowtone-ai/Grimo` rather than continuing to modify the old `snowtone-ai/grimoire` repository. The old repository remains a read-only behavioral reference for Task/Calendar persistence, backup, Google integrations, and security boundaries; its old UI and gamification are not design authority.
