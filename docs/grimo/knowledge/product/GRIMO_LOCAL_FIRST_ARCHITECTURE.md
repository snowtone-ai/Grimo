# Grimo Local-first Backend Architecture — Initial Shushu Release

**Status:** Human-approved deployment/data decisions + engineering architecture contract (2026-10-17)  
**Scope:** Shushu-only first usable release, future Jill/Pino content. This file selects storage/implementation constraints; product reward, companion and appearance rules remain governed by their own authorities.
**Authority:** latest explicit Human decisions > product/data feature specifications > this implementation architecture > legacy implementation. Read `AGENTS.md`, `Goal√map.md` and the relevant specs before implementation.

## 1. Release decisions and boundary

- Grimo is a **new application**, not a migration/rebrand of task-plant/Grimoire. No legacy user data import, cross-app migration or preservation of legacy feature semantics is required.
- Personal/family, **non-commercial**; each family member uses an independent installation/profile. **No device sync, shared task database, account, cloud database, server-backed collection or login for core use**. Do not silently add Dexie Cloud, Firebase, Supabase or authentication.
- Existing Vercel project **`grimo`** is the deployment target (observed project ID `prj_krUcsYiiziGcR0YIQzPXWGtPLlXJ`). Project settings, linked Git branch, environment and deployment health were **not verified** due to permission errors. No new project, domain or environment change without a concrete need.
- Initial release ships **Shushu alone**. Jill and Pino remain future-enabled content/character IDs, not required runtime bundles or placeholders disguised as working. Carol is retired; do not restore.
- Data belongs to the browser **origin + browser profile + installation storage**. Same URL in another browser/device does not share state. Users may manually transfer Grimo backups; that is **file restore**, not sync.
- Remote integrations (e.g. optional Google Calendar, Gemini) are separate, gated functionality; core Task/Calendar/Grimo/Collection never depend on them. Do not store server secrets in client storage.

## 2. Dependency and application topology

```text
Next.js/React UI (Task, Calendar, Grimo, Collection)
         ↓ application/domain services (pure rules)
Task commands ─┬─> single Dexie transaction ─> local IndexedDB
               └─> durable RewardEvent ledger ─> RewardResult/inventory/collection
                                         ↓ projections / notifications
                            UI chest and PlayCanvas Shushu experience

Serwist: offline app shell + versioned asset cache, NOT the user-data database
Vercel: deploy/download application and assets, NOT the source of user state
```

Separations: `src/domain/` owns rules, IDs, catalog and reward selection; `src/data/` owns Dexie schema/repositories/transactions and Grimo backups; `src/app/` + components own screens; PlayCanvas owns short-lived rendering/motion with a narrow event interface. Never mutate inventory directly in React or 3D code. All UI methods share the same command path. Database access runs client-side only; keep Next.js server rendering safe. Use existing stack, no framework/database swap.

## 3. A fresh, isolated and versioned database

Create a **new database name `GrimoLocalV1`** starting at **Dexie schema version 1**. Existing `TaskManagerDB` (old `src/data/db/grimo-db.ts`) is a *legacy implementation detail*, **not** the new Grimo database. Do not automatically open, copy, reset or delete it. Likewise, obsolete `src/data/backup/legacy-grimoire.ts` is not a Grimo backup contract; deactivate its reachable paths after caller audit, rather than broad destructive deletion. A new DB name alone is not sufficient: convert the app's active repositories to the new DB.

Logical ownership (separate tables/indexes where actual queries and atomic writes justify them):
- `tasks` (stable task ID, due date/time, recurrence, creation metadata); `taskCompletions` (stable `taskId+occurrenceLocalDate` composite uniqueness; repeated tasks keep history, nonrepeating tasks have one lifetime grant).
- `rewardEvents` (unique domain event ID, cause, source/occurrence key, processing state); `rewardResults` (one immutable result per event; chest revealed/auto-open metadata).
- `inventory` (Food quantity or permanent ownership), `collection` (ever-discovered metadata), `reactionDiscoveries` (item × character), `equippedWear` (per-character slot), `duplicateExchanges` (one exchange per source result).
- `userGrimoState` (active/owned characters, last login reward day), `rewardSettings` (e.g. auto chest open); `interactionSessions` only if justified for gift limits and exactly-once.
- Keep item/character **definitions and catalog versioned in source-controlled static content**, not duplicated as user-owned records. Catalog may include future unavailable Jill/Pino content but must not roll rewards unusable with the Shushu-only release. Do not over-index; add only indexes needed for core lookups and uniqueness.
- No long-term affinity/hunger/penalty/XP/currency fields. `CharacterRuntimeState` is transient in-memory except explicitly approved short afterglow.
- Future Grimo upgrades MUST preserve **Grimo** data with monotonic Dexie schema versions, upgrade tests and backup compatibility. “No old-app migration” does **not** authorize destructive changes to Grimo after actual use.

## 4. Atomic commands, recurrence and idempotency

- Registration command: persist task **and** `TASK_CREATED:<taskId>` event in one short `rw` Dexie transaction. Editing a task is not a new registration. External Calendar imports get stable source identity and must not duplicate events when replayed.
- Completion command: persist occurrence completion **and** `TASK_COMPLETED:<taskId>:<occurrenceDateKey>` in one transaction. A one-off task uses a stable one-time occurrence key, not an arbitrary click time. Recurring tasks earn at most once per eligible local occurrence; toggling undone→done again MUST NOT farm the same occurrence. Completion status may be toggled without deleting historically granted rewards.
- Daily visit: `DAILY_LOGIN:<localYYYY-MM-DD>` exactly once per local day **on actual app opening** (no remote authentication). Gift: a unique `INTERACTION_GIFT:<sessionId>` only after actual eligible interaction, no per-frame lottery.
- Stable unique keys enforced by IndexedDB indexes/primary keys, not only preflight checks, so overlapping tabs/concurrent clicks cannot double-award. Roll the outcome once and persist `RewardResult` with its event atomically with inventory/collection. Use finite-duration Dexie transactions and avoid network, animation, arbitrary asynchronous work, or long user prompts inside them.
- The user's action must not disappear if content is temporarily unavailable. A durable event may remain `PENDING`; a later deterministic retry resolves it exactly once. **Never show an empty chest or invent a reward**. Validate each enabled catalog/action has at least one eligible item before shipping. A completed domain command is not contingent on successful visual animation.
- Reward outcomes follow `GRIMO_PRODUCT_FEATURE_SPEC.md`: daily Food, create Food/Wear, complete Food/Wear/Special/Secret Motion, interaction Gift separate; rarity 70/20/6/3/1 with three-star reserved/re-roll, no zero-result reward; Food only consumable; duplicate permanent item → one discovered Food chosen by user (persist `PENDING` exchange safely). Task splitting is allowed.
- Render/UI can replay a *saved* pending/unrevealed reward after a crash without re-rolling or duplicating inventory. Do not use random values or UI mount events as idempotency keys.
- Date calculation uses a deliberate **local calendar date** contract, with one source of truth for Task/Calendar and rewards. Test midnight, daylight-saving/timezone change, multi-tab operation and recurring daily/weekly/monthly occurrences. Device clock changes are an explicit local-only limitation, not an excuse for a server.

## 5. Backup, restore and user-data safety

- Ship **Grimo-only** versioned JSON export/import with `app: "grimo"`, `backupFormatVersion`, `exportedAt`, catalog/schema metadata and complete user-owned tables. No inherited `app: "grimoire"` backup API or silent legacy import.
- Export must be consistent across all relevant tables; safe download with intelligible file name. Restore parses/validates **before** modifying data: format/schema version, structural types, ID uniqueness, catalog references, event→result/exchange integrity, nonnegative Food quantities, size/resource limits and unsupported future versions. Unexpected or malformed payload → no changes.
- Initial restore policy: **replace current local Grimo dataset**, never implicit merge across different installations. Clearly preview impact and require explicit confirmation. Offer/save a safety backup before any replacement and check that the user can retain it; perform replacement in one transaction, roll back entirely on failure. Separate “delete all local data” must require explicit confirmation.
- Explain that uninstalling PWA, changing origin/browser/profile, clearing site data or storage eviction may lose state; installing on another device does not synchronize. Exports held by users are not automatically backed up. A lightweight export reminder is acceptable; no background/auto-cloud backup claims.
- Optionally offer `navigator.storage.persist()` after an understandable user action, handling denial gracefully. Browser persistence reduces eviction risk but never protects against deliberate deletion/device loss. Handle `QuotaExceededError`, permission/storage denial and no-IndexedDB mode with explicit user-visible recovery paths; avoid claiming unconditional durability.

## 6. PWA, assets, performance and Vercel

- Persist **user state exclusively in IndexedDB**; Serwist handles network/application/asset responses. Do not precache all high-volume 3D assets or embed GLB as JS. Load Shushu GLB/flower/paw textures only when visiting Grimo, cache versioned immutable asset URLs subject to real storage/eviction behavior and fallback when asset unavailable.
- Production-ready Shushu candidate and its custom loader live on a separate production branch; **do not merge that whole branch**, historical diagnosis or all heavy assets into main. Select only approved manifest/hash + runtime dependencies and verify no Git LFS *pointer text* is being served as a GLB. The ~62.6 MB Shushu geometry candidate plus equipment needs an actual phone memory/network budget, not optimistic PC extrapolation.
- Offline Task/Calendar and accessible Collection state are non-negotiable; Shushu works offline only after assets have been cached successfully, otherwise show a meaningful non-destructive fallback. Avoid breaking Task/Calendar when 3D fails.
- Existing Vercel `grimo` project should receive **production only after** CI, Preview smoke, real Xiaomi/target-phone checks, Human Shushu experience GO and backup restore checks. Confirm actual Vercel project→repo/branch settings and limits before relying on them; connector access is currently insufficient.
- No extra paid services, sync services, new database hosted service, automatic credential provisioning, production deployment, or destructive repository cleanup as part of data-layer tasks.

## 7. Ordered implementation and merge gates

**Gate A — design (now):** docs-only architecture authority + explicit correction of cross-device-sync clause in logical data spec. Merge separately after checking diff/authority consistency; no app behavior or asset change. Publish this to main *before* starting Codex data work.

**Gate B — next Codex task, bounded foundation:** new isolated `GrimoLocalV1` Dexie v1 + types and active Task/Calendar repository wiring; use stable per-occurrence completion IDs and create/complete reward-event envelopes transactionally (PENDING only; no reward generation yet); ensure no legacy data imports and retain task/calendar basic behavior. Add focused fake-indexeddb/node tests for clean install, double click/re-completion, recurring dates, concurrent operations, old database isolation and transaction failure. **Do not** build full reward engine, complex UI, 3D or Vercel deployment in this task. Merge once tests + CI + inspection establish no Task/Calendar regression.

**Gate C — Shushu Grimo route:** bring only approved v004 runtime/appearance references to actual lazy-loaded PlayCanvas `/grimo` with lifecycle, quality/fallback and phone evidence. Preserve existing approved body/paw/flower. Approval of image ≠ mobile-runtime GO. Merge only after phone validation and targeted performance/lifecycle checks.

**Gate D — rewarding vertical slice:** complete daily/create/complete engine and seeded legitimate Shushu catalog, persistent chest open/replay, inventory/Collection projections; test exactly-once, duplicate exchange, restart and offline; then add Collection UI.

**Gate E — companion:** living idle/touch/intent and reward-to-character bridge; Food/Wear/Special/Secret Motion/Gift with independently demonstrated motions. Each independent Human gate; no visual downgrades to clear technical tests.

**Gate F — release:** all four usable screens, recurring tasks, restore/export, working rewards/Collection/Shushu, offline/no-network, real phone memory/load/cooling checks, Vercel Preview and Human product GO. Then ship through the existing Vercel project; Jill/Pino later on isolated character branches.

**Integration rule:** main receives small verified app/document changes via focused PRs. Never merge the long-running full Shushu/Jill/Pino production branches wholesale. For production-changing code, tests/CI and scoped review precede merge; avoid exposing a half-finished experience as production. The exact deploy hook/branch is to be verified, not assumed.

## 8. Adversarial minimum QA

1. Rapid double tap + simultaneous tabs → one event/reward per identity, no lost task.
2. Kill/relaunch before chest reveal → same persisted reward and quantity, no re-roll.
3. Complete→undo→complete; and tomorrow's daily recurrence → exact per-occurrence grant.
4. Invalid/corrupt/truncated/oversized/newer backup → reject *before* write; failed restore leaves prior snapshot intact.
5. Restore of valid backup with no online connection → exact tasks/inventory/discoveries/reward history.
6. 3D load fail/offline uncached → Task/Calendar/Collection remain usable.
7. Storage quota exceeded and Vercel serving LFS pointer rather than GLB → visible error/fallback, no silent corrupt state.
8. Jill/Pino future catalog added → no accidental grant or forced download in Shushu-only release.
9. No runtime auth/sync/cloud calls or hidden charges; explicit owner-controlled backups.

**Distinction:** This document sets future implementation choices. It does *not* claim the backend/rewards are already built, the phone passes, or Vercel production is live.
