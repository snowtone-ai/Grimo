# Grimo — AGENTS.md

Grimo is a smartphone-first PWA with a Full 3D character pipeline:
`Blender → GLB/glTF → PlayCanvas → Next.js/React`.

## Authority

Resolve conflicts in this order:

1. Current explicit user instruction
2. Canonical identity and approved production authority
3. Task-specific current specification
4. Current code and tests
5. Archive / legacy

Do not revive archived PixiJS, 2D, or 2.5D architecture. Carol is the first
vertical slice; preserve the four canonical identities and the approved Grimo
icon unless the user explicitly changes them. The companion view is normally
front-facing. Visual identity and motion quality require a Human Gate.

## Lean reading policy

Default: read this file, files named by the user, and files directly changed by
the task. Read additional specifications only when the task needs them (for
example `DESIGN.md` for UI/UX, a character production contract for geometry,
the motion spec for motion, the data model for persistence, or setup docs for
toolchain work). Do not routinely read `tasks.md`, `xp.md`, `docs/state.md`,
`docs/decisions.md`, or archive material. Archive is for explicit history work.

## Safety and boundaries

- Preserve Task/Calendar semantics, Dexie migrations/backward compatibility,
  stable source keys/idempotency, Google read-only boundaries, PWA behavior,
  server-only Gemini secrets, and user work.
- Never print, commit, upload, or expose `.env.local`, credentials, OAuth
  tokens, `GEMINI_API_KEY`, or private user data.
- Keep React responsible for routes, DOM UI, app state, settings, and
  accessibility; keep PlayCanvas responsible for 3D rendering, animation,
  cameras, and hit volumes. Do not put persistence or routing in the renderer.
- Do not discard, reset, overwrite unrelated work, or auto-merge `main`.

## AI Handoff / Execution

- The default substantial-reasoning route is `ChatGPT Planner → Codex Luna / Low`:
  ChatGPT reads the latest pushed GitHub state, completes investigation and
  planning, and produces a concrete Luna execution prompt. ChatGPT does not
  edit the repository.
- Tracked changes include targeted validation when needed, `commit`, and
  `push`, unless the user explicitly prohibits push, security or unresolved
  failure blocks it, a Human Gate is required first, or the remote is
  unavailable. Do not treat commit-only or unpushed local state as the
  session handoff boundary.
- Sol/Terra are exception-only for local iterative reasoning, unobservable
  local state, a failed clearly specified Luna task requiring non-trivial
  reasoning, or an explicit user request. Automatic escalation is forbidden.

Use the short final handoff report: branch, commit, pushed status, validation,
and next handoff (`CHATGPT_PLANNER`, `CODEX_LUNA`, `CODEX_ASTRA`, or `HUMAN`).

## Current truth and phase routing

- `docs/production/carol/CAROL_PRODUCTION_STATE.md` is the single mutable
  Carol execution truth. Stale prompts, memory snapshots, maps, contracts, or
  repository-local Skills must not override it.
- The latest pushed GitHub state is the ChatGPT↔Codex handoff boundary.
- Before any materially new production phase or task class, ChatGPT Planner
  must audit the latest pushed GitHub state and the actual Codex environment,
  including current state/evidence, relevant contracts, `.codex/config.toml`,
  available repository Skills, and applicable `codex mcp/plugin/features`
  inventory commands. It must evaluate phase relevance, quality gain,
  context/token cost, noise, side effects, reproducibility, and built-in
  alternatives, then choose the minimum sufficient toolset.
- Toolset optimization and project-scoped configuration must happen before
  substantive phase execution. Planner must issue a dedicated Luna
  configuration prompt first; if reload/restart is required, stop and resume
  planning only after reload. Re-audit at every phase transition; no fixed
  permanent phase tool list exists.
- Repository-local `.agents/skills/` is intentionally not production truth or
  a required routing layer. Use current task authority and actual framework or
  tool documentation instead.

## Assumption Expansion / Unseen-Option Search

ChatGPT Planner must not treat user-listed options or assumptions as the limit
of the search space. Before an important design, technical, or workflow choice,
it must compare relevant unseen options, including simpler or higher-quality
methods, lower-token approaches, ways to remove an assumption, built-in
alternatives to external tools, approaches that reduce later work, and ways to
eliminate failure modes at their root. Respect explicit constraints, keep the
search scoped, and do not stop merely because another option exists. Prefer
current GitHub truth and verifiable evidence. Apply this rule to Mandatory
Phase Tool Preflight: seek the best quality, token efficiency, and reliability
for the actual problem space rather than choosing only among visible options.

## Targeted verification

Verification is change-based. Do not run tests merely because a task is
complete, and do not run `pnpm verify` by default. Never repeat a passing check
unless relevant files changed afterward; do not broaden a passing targeted
check without a concrete unresolved risk. “Just in case”, “best practice”, or
“Definition of Done” is not a reason for full validation.

| Change | Default check |
| --- | --- |
| Markdown, image reference, or prompt only | None; optionally `git diff --check` |
| Small TypeScript, CSS, or config change | At most one relevant check: `pnpm typecheck`, changed-file lint, or relevant test |
| Bug fix | One relevant regression test only when reproducible and useful |
| UI change | Targeted browser/component check only when the changed behavior needs it |
| Changed/exported GLB | Once: `pnpm 3d:validate -- <changed-file.glb>` |
| Dependency, framework, or build-config upgrade | Full checks are allowed as a rare high-blast-radius exception |

Do not start Storybook, Playwright, Lighthouse, Blender, PlayCanvas, Chrome
DevTools, or physical-device QA unless the task, release gate, Human Gate, or a
concrete regression risk requires it. Do not inspect output unrelated to the
changed scope. Specialized QA is opt-in. GitHub Actions owns full PR CI; local
agents should run only targeted checks and investigate CI failures when they
occur.

## Models

Reserve Astra for high-value geometry, identity, and architecture reasoning.
Astra must not perform routine validation, command execution, test-failure
triage, or repository-wide scans. Luna handles deterministic clerical work and
targeted checks; GitHub CI handles automated regression. Automatic escalation
is forbidden. Keep `.codex/config.toml` `multi_agent = false`.

<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify in `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
