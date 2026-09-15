# Grimo — AGENTS.md

**ステータス:** リポジトリ運用の正式規約  
**基準:** smartphone-first PWA / Full 3D / Blender → GLB/glTF → PlayCanvas

## 1. 権威順位

競合時は次を優先する。

1. 現在のユーザー明示指示
2. 承認済みcanonical identity / 3D production reference
3. UI/UX・Audio・Hapticsは `DESIGN.md`
4. 現行Product / Data / Motion / 3D Production仕様
5. `docs/decisions.md` → `docs/state.md` → `tasks.md` → 現在のcode/tests
6. 外部調査
7. archive / legacy

旧PixiJS / 2D / 2.5D architectureは廃止済み。古いfileから復活させない。

## 2. Product固定前提

メイン画面：

```text
Task
Calendar
Grimo
Collection
```

Character基盤：

```text
Blender → GLB/glTF → PlayCanvas → smartphone PWA
```

Carolを最初のvertical sliceとし、合格後にJill / Pino / Shushuへ展開する。

companion viewは原則front-facing。side/backはproduction reference用途。

現在のGrimo app iconは正式採用品。明示指示なしに再生成・recolor・crop・rename・replaceしない。

## 3. 作業前確認

大きな変更前に最低限、`README.md`、`DESIGN.md`、`tasks.md`、`xp.md`、`docs/state.md`、`docs/decisions.md`、関連spec、変更対象fileを読む。archiveから現在仕様を推測しない。

## 4. UI / UX / Audio

`DESIGN.md` を正式規約とする。

アプリ全体は、ポケポケの観察可能なUI/UX grammarを可能な限り高精度で再現する。対象は情報階層、淡いblue-white neumorphism、spacing、typography、icon、button depth、押下感、transition、micro-interaction、sound、haptics、Collection、reward pacing。

ただしname / character / image / icon / audio / effectはGrimo独自とし、Pokémon asset・logo・無許諾font・抽出soundを使用しない。

意味のあるinteractionは一体で設計する。

```text
visual + motion + sound + optional haptic + result/loading feedback
```

## 5. Character Quality

canonical identityを技術都合より優先する。

禁止：

- 1枚絵全体を変形characterとして使う
- whole-body bob / scaleを生命感に使う
- physicsへhero pose決定を任せる
- 弱いactingをVFX / audioで隠す
- 全channel常時motion
- 同じpersonality animationを4体へretarget

Primary actingはsound / VFXなしでも成立させる。最終visual acceptanceはHuman Gate。

## 6. Runtime責務

```text
React / Next.js
  route, DOM UI, app state, settings, accessibility

PlayCanvas
  3D rendering, animation, camera, hit volume

TypeScript behavior
  gesture, state, attention, cooldown, repetition,
  selection, interruption

Data
  Task / Calendar / Collection / reward persistence / migration
```

rendererにroutingやtask persistenceを持たせない。React stateでper-frame 3D transformを駆動しない。

## 7. 既存system保持

専用migrationまでは、Task / Calendar semantics、Dexie migration / backward compatibility、stable source key / idempotency、Google read-only boundary、Gemini server-only secret、PWA / service worker、app icon、4体のidentity canonicalを保持する。

通常のrepo作業でGoogle Cloud / Vercel settingsを変更しない。

## 8. Secret / User Data

`.env.local`、credential、OAuth token、`GEMINI_API_KEY`、private user dataをprint・commit・upload・公開しない。`GEMINI_API_KEY` はserver-only、`.env.local` はGit ignoreを維持する。

## 9. Git

編集前：

```bash
git status
git branch --show-current
```

未commitのユーザー作業を保護する。明示指示なしにdiscard / reset / overwrite / stashしない。専用 `codex/` branchで作業し、許可なしに `main` へauto-mergeしない。

## 10. 検証

`pnpm` を使用する。適用可能なら以下を実行する。

```text
pnpm typecheck
pnpm test
pnpm lint
pnpm build
pnpm verify
pnpm context:check
```

visible UI変更ではreal-browser mobile checkも行い、route、console/runtime/network error、safe-area、keyboard、touch target、pressed/released state、audio/mute、reduced motion、必要に応じてPixel 7a級performanceを確認する。

3Dのautomated metricは証拠であり、最終合否はHuman Gate。

## 11. Documentation

- `tasks.md`: 現在地 / 次作業 / acceptance / blocker / branch / verification
- `xp.md`: 再現可能なengineering lessonのみ
- `docs/decisions.md`: 長期decision
- `docs/state.md`: 現在のproduction fact

obsolete historyをcurrent truthとして扱わない。

## 12. 停止条件

canonical identity失敗、Task/Calendar compatibility破壊、user dataを危険にするmigration、browser/PWA regression、secret handling不明、`DESIGN.md`から重大逸脱、未承認quality lossが必要、Human Gate不合格のいずれかでは、問題を隠さず停止して報告する。

<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->
