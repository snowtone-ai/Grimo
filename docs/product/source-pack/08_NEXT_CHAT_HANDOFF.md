# New Chat Handoff — Grimo

新しいチャットで最初に読む。

## Current truth

- Project: Grimoire PWA の4体グリモ触れ合い機能
- Characters: Carol / Jill / Pino / Shushu
- Development path: **PixiJS 8系 2.5D layered runtime**
- Canonical images: Project Sourcesに追加済み
- 4 × 8 development reference images: **32/32 generated**
- Environment setup: **complete**
- Pre-development questionnaire: **answered**
- Human review gates: allowed and required
- Implementation: not yet confirmed complete
- Reference clip collection: not yet confirmed complete

## Do not restart planning from zero

以下は既に決定済み:
- full 3Dを本線にしない
- Live2D/Spineを本線にしない
- PixiJS character runtime
- Reactはhost/UI
- canonical fidelity優先
- human final QA
- AI/Codexが実装・QA・数値調整を主担当

新チャットで再び「2Dか3Dか」をゼロから聞かない。  
新しい証拠で覆す必要がある場合だけ、明示的に理由を示して再提案する。

## First recommended task

まだreference clipsが未収集なら:

1. Let's Go 5本
2. Pokémon-Amie 5本

だけ先に集め、`04_INTERACTION_MOTION_BIBLE.md`へ具体例を追加する。

その後、最初の1体を縦にprototypeする。

## Prototype acceptance

最初の1体で証明すべきこと:
- asset/layer pipeline
- touch zone
- tap/pet/hold
- facial preset
- primary motion
- secondary motion
- reaction settle
- random/repetition memory
- capture / visual QA
- human Gate 1–3

これが通るまで4体並列化しない。

## Context hygiene

新しいチャットでは、必要以上に過去資料を読み込まない。

通常:
1. `00_SOURCE_INDEX.md`
2. `01_CURRENT_STATE.md`
3. 対象タスクに必要なBible/Architecture
4. 対象キャラcanonical
5. 対象キャラの必要な補助画像のみ

で開始する。

Carol 3D / Muu / Blender / Three.js legacy packを自動で混ぜない。
