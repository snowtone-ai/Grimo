# Grimo — Handoff (last verified pointer; NOT live state)

**Checked:** 2026-10-16 / ChatGPT. **Canonical:** `main:docs/production/Handoff.md`. Main is the shared rules/knowledge base, **not** proof of the newest 3D state. For actual NOW, inspect the relevant feature branch remote HEAD, editable assets, production State, evidence, and Codex-local dirty changes. Human approval cannot be inferred from file names, dates or technical PASS.

## Shared foundation verified
- `main:AGENTS.md` was updated at [`da479113`](https://github.com/snowtone-ai/Grimo/commit/da4791135414a94951ed2d9ab51ca28da9ebcec8) to require GOAL-first, identity protection, targeted evidence, cause separation and minimal sufficient work. Next.js auto-generated rules were retained.
- 2026-10-15 [shared-reference sync](https://github.com/snowtone-ai/Grimo/blob/main/docs/grimo/knowledge/character-production/SHARED_REFERENCE_SYNC_20261015.md) registered 15 Body-only PNGs and their hash manifest on main, shared Canonicals and other reusable knowledge. This **does not** confer Tripo preflight, 3D, Rig, Motion or Human acceptance.
- [Project Knowledge Router](https://github.com/snowtone-ai/Grimo/blob/main/docs/grimo/knowledge/GRIMO_PROJECT_KNOWLEDGE_ROUTER.md) is the stable entrypoint; Goal√map is the WHY. Former `coord/grimo-ai-handoff` and old `GRIMO_AI_HANDOFF.md` are history, not active coordination.

## Character execution routing (status requires recheck)
- **Carol:** `docs/production/carol/CAROL_PRODUCTION_STATE.md` on the **active Carol feature branch** and `assets/grimo/source/carol/approved-3d/authority.json`. Main's old bootstrap State is not today's production status.
- **Jill:** identify the selected Rig/Geometry branch among active `codex/jill-*` work; inspect actual rig, deforming renders, motion failures and scoped Human gate. Do not infer GO from branch labels.
- **Pino:** identify the selected `codex/pino-*` branch; verify tail/short-arm/support rigs and evidence, including whether Motion references gained Human approval.
- **Shushu:** investigate `codex/shushu-*` candidate branches and their real evidence. The older v002/v003 Human FAIL/PENDING records are **historical**, not a current v004 quality verdict.

## Current operational gates
User-visible Identity, cuteness, expression and natural support/contact require actual comparable renders and Human review. Geometry/Rig/GLB tests validate only their demonstrated scope; unverified runtime/credit/UI claims remain UNKNOWN. Keep accepted assets, other characters, source binaries and uncommitted work intact. No blind branch merges/rebases and no unapproved chargeable Tripo actions.

**Update:** Only after material progress, Human decision, blocker or owner transition. Read latest, reconcile competing changes, commit/push safely, verify remote HEAD. Otherwise leave unchanged; if required update fails, report `HANDOFF_SYNC_BLOCKED`.

## Shushu branch verification — 2026-10-17 / Codex
`codex/shushu-v004-motion-ready-v003-20261016`、開始HEAD `a4a90851`。main pointer `73617ce2`を照合、一括統合なし。別名v003の口/頭頂/前肢を修正し、初回SelfContactも再修正。[候補・原寸/連続動作・再現・残項目](shushu/evidence/production-rig-v004-motion-ready/final-v003/REVIEW.md)。技術/Runtimeは記載範囲でPASS、**最終Human外観GO待ち**。Blender→再読込GLB→PlayCanvas→Xiaomiを最終hashで照合。実機300秒：rAF P95/P99 16.7ms、25ms超1回、context loss 0、法線CPU P50 3.9ms（旧再計測5.5）、Purpose 0.5ms。開始温度差あり、GPU時間UNKNOWN。通常Morph＋製品controller経路を納品、旧arm FKの無変更互換・全任意制御はHOLD。W/鼻下紐除去・承認body/座位・原本・ユーザー差分を保護。原本置換/量産HOLD。次はHumanが顔・短肢体積・肩/頬下接触・連続復帰を判定し、指摘箇所から改善。
