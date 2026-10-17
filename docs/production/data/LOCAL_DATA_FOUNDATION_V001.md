# Local data foundation v001

2026-10-18. Base: main `8b9d736` (#7/#8/#9). Branch: `codex/grimo-local-data-foundation-v001`; unmerged, no deployment.

## Contract

- `GrimoLocalV1`, Dexie v1: tasks, taskCompletions, rewardEvents, streaks.
- Atomic task + `TASK_CREATED:<taskId>`; retries reuse command ID. Calendar source IDs survive replay/deletion.
- Atomic completion + `TASK_COMPLETED:<taskId>:<localDate|ONE_OFF>`. Undo retains events. IndexedDB keys enforce cross-tab uniqueness. PENDING only, unprocessed, no result.
- Task/day and Calendar/month use date indexes + recurrence candidates; live queries reflect other tabs. Legacy DB never opened/migrated/deleted; old backup entry points fail closed.

## Verification

- Node 24, frozen lockfile; `pnpm check:full`: typecheck, lint, 17 tests, production build.
- Tests: retries, undo/recomplete, daily/weekly/monthly dates, Calendar replay, batch/quota rollback, two connections, midnight/DST/timezone, legacy isolation.
- Chromium: simultaneous tabs, double submit, reload, live Task/Calendar; 2 tasks / 1 completion / 3 PENDING events. Injected quota failures surfaced and rolled back.
- Browser + production-app restart PASS: 1 task / 1 completion / 2 events retained; offline undo/recomplete adds none.

Gate B technical: GO. Feature pushes do not trigger GitHub Actions; local CI-equivalent checks passed. Release HOLD: rewards, Collection, backup/restore, Shushu/runtime/phone and Human release gates remain separate.
