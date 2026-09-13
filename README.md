# Grimo

**Grimo** is a mobile-first, local-first task management PWA built around high-quality interaction with four original Grimo characters: Carol, Jill, Pino, and Shushu.

Core concept: **「グリモと触れ合いたすぎて逆にタスク管理ができなくなるタスク管理アプリ」**.

## Current foundation

- Next.js App Router + React + TypeScript
- Dexie / IndexedDB local persistence
- PixiJS 8 layered 2.5D character runtime (planned vertical slice starts with one character)
- Google Identity Services + Gmail/Calendar read-only integrations
- Server-only Gemini proxy for structured task extraction
- Serwist PWA foundation
- Playwright-ready QA structure

Main routes:

- `/tasks` — タスク
- `/grimo` — グリモ
- `/calendar` — カレンダー
- `/settings` — 設定
- `/` — startup preference launch gate

Read `AGENTS.md`, `tasks.md`, and `docs/decisions.md` before implementation work.
