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

<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify in `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
