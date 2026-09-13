# Data model foundation

The initial database intentionally preserves the old `TaskManagerDB` v1-v4 schema and does **not** add speculative Grimo tables yet.

Current stores:
- `tasks`
- `streaks`
- `plantState` (legacy compatibility only)
- `drops` (legacy compatibility only)

New reward/inventory/affinity stores are added only after the first character vertical slice validates the actual product loop. Any new reward grant mechanism must have a stable source identity so retry/replay cannot double-grant.
