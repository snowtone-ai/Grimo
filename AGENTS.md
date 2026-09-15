# Grimo 作業規約

Grimo は smartphone-first の local-first task management PWA です。

## Current architecture

- Full 3D architecture is authoritative.
- Character production direction is Blender → GLB/glTF → PlayCanvas.
- Old PixiJS / 2D / 2.5D implementation is obsolete and must not be resurrected.
- Phase 0 does not implement PlayCanvas, Blender assets, character motion, or touch interaction.
- Preserve Task / Calendar / Google / Gemini / PWA boundaries and existing data compatibility.
- Preserve the four canonical identity assets and the current Grimo app icon byte-for-byte.
- Human Gate remains the final aesthetic acceptance authority for future character work.

## Safety and data

- Read `README.md`, `DESIGN.md`, `tasks.md`, `xp.md`, and the relevant docs before changes.
- Never print, commit, or send `.env*`, credentials, tokens, user data, or secret values.
- Keep `GEMINI_API_KEY` server-only and keep Google scopes read-only unless a later decision explicitly changes them.
- Preserve Dexie migrations, task/calendar semantics, backup recovery, stable source keys, and retry idempotency.
- Do not change Google Cloud or Vercel project settings as part of repository work.

## Git and verification

- Inspect status before editing. Preserve uncommitted user work; never reset, discard, stash, or overwrite it without explicit direction.
- Work on a dedicated `codex/` branch. Do not merge to `main` automatically.
- Use `pnpm`; normal verification is `pnpm verify` plus `pnpm context:check` when available.
- UI changes require real-browser checks of the affected route, including console/runtime errors and mobile-safe layout.
- Keep `tasks.md` focused on current position, next operation, acceptance, unresolved items, branch, and verification.
- Record only reproducible engineering lessons in `xp.md`; record durable architecture/security decisions in `docs/decisions.md`.

<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
