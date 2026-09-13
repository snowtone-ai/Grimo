# Long-lived decisions

## 2026-09-13 — New repository
The product and repository name are **Grimo**. The product is rebuilt in `snowtone-ai/Grimo` rather than continuing to modify the old `snowtone-ai/grimoire` repository.

The old repository remains a read-only behavioral reference for Task/Calendar persistence, backup, Google integrations, and security boundaries. Its old UI/gamification are not the design source of truth.

## 2026-09-13 — Main information architecture
Primary bottom navigation is **タスク / グリモ / カレンダー**. Inventory/Items belongs under Grimo rather than as a fourth peer destination. Settings is secondary navigation.

`/` is a launch gate. A local preference selects `/tasks` or `/grimo`; default is `/tasks`.

## 2026-09-13 — Character runtime
React owns route/UI/app state/viewport host. PixiJS 8 owns layered character rendering, pointer hit, secondary motion, particles, and the render loop. Gesture/reaction/affinity/cooldown logic remains renderer-independent TypeScript.

Full 3D, Blender/Three.js mainline, Live2D and Spine are not the formal runtime.

## 2026-09-13 — Data compatibility
Task semantics, recurrence, streak behavior, Calendar import source-key idempotency, and the legacy `TaskManagerDB` tables are initially preserved. New Grimo data tables are deferred until the vertical slice validates their actual needs.

Legacy Grimoire JSON backups are importable without deleting current records. New Grimo backup format will be versioned separately once Grimo-specific state exists.

## 2026-09-13 — External integrations
Google access remains browser OAuth token flow with read-only Gmail and Calendar scopes; access tokens are memory-only. Gemini key remains server-only behind fixed-purpose, validated requests. Secrets are not committed.

## 2026-09-13 — Agent quota policy
For Plus usage, Sol Medium is the integration/default reasoning tier, Luna High handles scoped routine work, Terra Medium handles broader multi-file exploration, and Sol High is an escalation. Repeated subagent status polling and duplicated work are prohibited.
