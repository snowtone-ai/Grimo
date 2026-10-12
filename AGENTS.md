# Grimo — AGENTS.md

## Required on every Grimo task/turn
**Codex and ChatGPT: fetch and read these 3 files from GitHub branch `coord/grimo-ai-handoff` before working:**
1. `AGENTS.md` — operating rules.
2. `docs/grimo/knowledge/Goal√map.md` — ゴール√マップ (WHY).
3. `docs/production/Handoff.md` — current state.

Codex reads local AGENTS automatically; then fetch the **3 remote files**. ChatGPT fetches all 3 via GitHub each Grimo turn. Do not reuse memory, previous turns, `main` or feature-branch copies. Verify actual production HEAD separately. Failure: report `CONTEXT_SYNC_BLOCKED` and missing path. Coordination branch is not for production code.

## Division / limits
AGENTS = startup/safety ≤2,500 chars. Goal√map = durable goals/WHY ≤5,000. Handoff = current facts/next action ≤4,000. ChatGPT→Codex prompt = task delta (goal/problem/authority/constraints/acceptance) ≤1,500. Count Unicode characters including markup/whitespace; link detail rather than duplicating.

## Authority
Latest explicit Human decisions and canonical/approved references outrank summaries. Higher user-visible goals outweigh lower technical proxies; Human visual FAIL overrides technical PASS. Safety/data integrity/authorization always apply. ChatGPT specifies outcome and gates; Codex chooses methods and targeted tests. Preserve user work, secrets, approved assets, Task/Calendar data and compatibility. No destructive reset, force-push, paid service or unrelated changes without consent. Use relevant specs only; no legacy 2D.

## Coordination
Update Handoff briefly for new facts or last interaction, not history. Re-fetch, reconcile concurrent changes, commit safely, verify remote HEAD; otherwise report `HANDOFF_SYNC_BLOCKED`. Goal√map changes only with material goal decisions. No full build for docs-only edits.

<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify in `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
