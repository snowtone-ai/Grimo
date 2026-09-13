# Grimo 作業規約

スマホ向けlocal-first task management PWA「Grimo」。正式character runtimeは **PixiJS 8 layered 2.5D**。旧Full 3D / Blender / Three.js / Live2D / Spineを本線へ戻さない。

## 開始・情報源

1. `AGENTS.md`、`tasks.md`、`xp.md` を読む。必要時だけ `docs/state.md`、`docs/decisions.md`、`docs/repo-map.md`、対象コード、`docs/product/source-pack/` を読む。
2. 優先順位: 現在のユーザー指示 > canonical画像 > 回答済み事前質問 > current docs > 実コード/実行結果 > 旧Grimoire repo > legacy。
3. 完了済みの本文・調査を理由なく再取得しない。

## 自律実行・確認境界

目的が明確な調査・編集・検証は自律実行する。確認は、新規費用、秘密情報の外部送信、不可逆なデータ破壊、公開範囲/認証/権限の重大な不明点だけ。追加コストは承認なしに発生させない。`.env*`、credential、token、利用者データをcommit/ログ/公開しない。

## Git

作業前に状態を確認。未コミット差分をreset/discard/stash/checkout/上書き/削除しない。原則mainへ直接編集せず安全なbranch/worktreeを使い、意図した変更だけcommitする。安全に競合を分離できない場合だけ確認する。

## 旧repo移植境界

`snowtone-ai/grimoire` はread-only reference。Task/Calendarの安定domain、IndexedDB互換、backup、Google/Gemini security boundaryは選択移植する。旧UI、植物、Book、旧reward/gamification、dark-fantasy visual、旧Carol 3Dはコピーしない。

## データ・API

- DB/task/backup変更は既存データ保持、重複、migration再実行、rollback/recoveryを確認。自動削除・曖昧な自動統合なし。
- Calendar source keyはstable/unique。retry/replayで二重登録しない。
- 日付はlocal calendar semantics、timestampはISO。
- Google scopeは理由なく拡大しない。現行 `gmail.readonly` / `calendar.readonly`。
- Gemini keyはserver-only。固定用途、入力検証、有限timeout、recoverable error、retry冪等性を維持。

## Engineering

標準機能 → 良質な既存実装 → 既存依存 → 必要な新規依存。将来だけを理由に抽象化・基盤・依存を増やさず、責務が実際に分かれる時だけ分割。performanceは主要操作を測ってから変更。

React = route/UI/app state/viewport host。PixiJS = character rendering/hit/secondary/particles/render loop。renderer外TS = gesture/reaction/affinity/cooldown。

## UI / UX

- UI/UX参照はPokémon Trading Card Game Pocket、触れ合い参照はPokémon Let's Go。原理を抽象化し、コピーしない。
- 1画面1主要目的/主要action。mobile safe area、片手操作、keyboard、semantic、contrast、loading/empty/success/error、reduced motionを扱う。
- 高品質な既存primitiveは優先するがGrimo固有visual/character experienceは必要なら自作。旧 `border-radius:0` / dark-fantasy styleは継承しない。
- UI変更は実Browserで主要経路と必要なconsole/network/runtimeを確認し、コード読解だけで完了にしない。

## Grimo品質

優先: canonical identity > touch causality/local reaction > character uniqueness > face/attention > timing/weight/settle > secondary > runtime stability > VFX > feature quantity。

Reaction: input → contact ack → anticipation → local body → face/gaze → main motion → secondary → optional VFX/SFX/haptic → overshoot → settle → afterglow → idle/attention。

4体を並列実装せず、まず1体vertical sliceをHuman Gateまで通す。

## モデル / subagent（Plus節約）

- **Sol Medium**: Main、設計、統合、milestone review、高blast-radius変更。default。
- **Luna High**: scope明確なroutine coding、tests、log確認、rename等。
- **Terra Medium**: 複数領域探索、中規模実装、Lunaで再修正が増えた時。
- **Sol High**: architecture/security/migration/難debug、またはMediumで実際に失敗した時だけ。
- xhigh/max/ultra/Astraをdefaultにしない。
- workerには完結タスク+受入条件を渡し、milestone完了/block時だけ報告。反復status polling禁止。既存workerを再利用し、重複作業を並列化しない。
- subagent利用自体を目的にしない。小作業はMainが直接処理。

## 実行・検証

pnpmのみ。開発 `pnpm dev`。通常 `pnpm verify`（typecheck→lint→test→build）。context `pnpm context:check`。検証量はrisk比例、成功済み同一検証を反復しない。CIは `.github/workflows/ci.yml` をmerge gateとする。

## 記録

- `tasks.md`: 現在地、次操作、受入条件、未解決、branch、verificationのみ。
- `xp.md`: 実作業で再現確認できた経験則のみ。
- `docs/state.md`: productionの現在事実のみ。
- `docs/decisions.md`: architecture/DB/auth/hosting/security/migration等の長期判断。
- `docs/repo-map.md`: 現在の責務/入口。理由はdecisionsへ。

最終報告は「変更」「検証」「残る問題」を短く伝える。
