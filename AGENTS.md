# Grimo — Repository Operating Guide

Grimo is a smartphone-first task-management PWA whose emotional center is four living companion characters: Carol, Jill, Pino, and Shushu. Product success is led by cuteness, appeal, life, attachment, and interaction quality—not technical purity.

## Authority and mutable truth

The repository implements decisions; it is not the highest source of durable product reasoning.

- **ChatGPT Project Memory** holds current reasoning policy.
- **Project Knowledge** holds durable product, experience, and architecture authority; start at `docs/grimo/knowledge/GRIMO_PROJECT_KNOWLEDGE_INDEX.md`.
- **Git and current production state** hold mutable execution truth.

For Carol, `docs/production/carol/CAROL_PRODUCTION_STATE.md` is the single mutable routing truth. Do not infer current state from old prompts, historical documents, or evidence.

## Working rules

- Preserve all local and uncommitted user work. Never reset, clean, overwrite, or discard it without explicit direction.
- Current explicit user decisions and canonical/approved references outrank stale implementation history. Read only the authority relevant to the task.
- Production methods are flexible. Tooling, model choice, topology and rig strategy, testing, workflow order, and intermediate architecture may change when evidence supports a better route.
- Choose the scope and process that best achieve the requested outcome. Avoid unrelated work, but do not stop at a minimum patch when the task requires final-quality convergence. Diagnosis, decomposition, implementation strategy, tooling, iteration, and validation are executor-owned unless an explicit higher authority or external constraint says otherwise.
- Validate proportionally to changed risk. Visible identity, cuteness, naturalness, and companion quality need Human perceptual acceptance.
- Commit and push focused, requested changes; do not alter application behavior, secrets, user data, or unrelated assets.

## Cross-agent live handoff — required (ChatGPT + Codex)

- **One canonical mutable cross-agent handoff:** `docs/production/GRIMO_AI_HANDOFF.md` on the dedicated Git branch **`coord/grimo-ai-handoff`**. Read it **from that branch**, not from the current feature branch or default `main`. This branch is **coordination only**, not a production-code base and must not be merged as a substitute for production.
- On **every Grimo-related user turn / Codex task**, ChatGPT Planner and Codex Executor must **first read the latest remote handoff**, then verify any consequential production facts against actual Git/asset/evidence. Before the response/task ends, **edit and publish that same handoff** even when no production work occurred (update the short latest-interaction field; do not invent a state transition). Keep detailed history in Git, not an accumulating chat log.
- The handoff is a **routing/index and last-known status**, never a replacement for the canonical art, approved project knowledge, character-specific production state, actual Git branch/HEAD, or direct test evidence. Label observations versus decisions versus uncertainties. Never use it to claim Human approval, paid Tripo actions, or successful publishing without proof.
- Coordinate edits with **read-latest → minimal change → optimistic/concurrency-safe commit → push → verify remote HEAD**. If the ref changed, re-read and reconcile; do not force-push or overwrite another agent's update. Codex should use a separate temporary Git worktree for the coordination branch if its active production worktree has local changes. Do not reset/stash/clean user work to update the handoff.
- If the handoff cannot be read or published due to missing tools, access or connectivity, **state HANDOFF_SYNC_BLOCKED** in the user-facing result with the attempted branch/path; never claim it was synced. Do not let coordination updates trigger paid API calls or unrelated refactors.
- Keep updates concise: current production branch and verified revision, current goal and gate, accepted and pending decisions, measured blocker, paid-service credits/trials (observed vs assumed), next owner/action, evidence links, plus actor/date/turn outcome. No credentials, personal information, or giant logs.

<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify in `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
