# Grimo Project — Current State

更新: 2026-09-13 JST

## 現在地

**Pre-development specification phase は完了。実装開始前の状態。**

ユーザー確認済みの完了事項:

- [x] 開発方式を決定
- [x] 4体の canonical 画像を `grimo` Project の情報源へ追加
- [x] 4体 × 8種類 = **32枚の開発用画像を生成**
- [x] 開発環境導入
- [x] 事前質問リスト回答
- [x] 人間レビューを挟むことを許可
- [x] AI-native / Codex主導開発を基本方針として維持

## 4体 × 8画像

各キャラについて完了済み:

1. `01-rig-neutral.png`
2. `02-opposite-3q.png`
3. `03-occlusion-parts-sheet.png`
4. `04-expression-sheet.png`
5. `05-facial-components-sheet.png`
6. `06-reaction-keyposes.png`
7. `07-layer-separation-sheet.png`
8. `08-touch-map-reference.png`

これらは **canonicalを置き換えるものではない**。  
canonicalはidentityの唯一の正式基準。32枚は実装・補完・Rig/Layer/Reactionの参考資料。

## 未完了 / 次に扱うもの

このsource pack作成時点で完了したと明示されていないため、以下は未確認扱い:

- Pokémon等のreference clip収集
- Motion Bibleへのreference clip転記
- 1体目の縦スライスprototype
- PixiJS character runtimeの本実装
- 実機でのTouch/Performance QA
- 4体完成

## 次の推奨フェーズ

1. reference clipを最小10件収集
2. 最初の1体だけで end-to-end prototype
3. Asset → Idle → Touch → Reaction → QA → Human Gate を通す
4. Architectureを固定
5. 残り3体へ横展開

### prototypeの考え方
最初から4体並列実装しない。  
1体で「生命感・interaction・QA loop」が成立することを証明してから横展開する。

## 完了の定義

コードが動くことではなく、

- canonical identityを保つ
- 触った場所へ局所的に反応する
- 表情・身体・secondary motionが因果的につながる
- idleに自発性がある
- 反応後にsettle/afterglowがある
- 同じ操作を繰り返しても機械的に見えない
- 4体で明確にキャラ差がある
- スマホで直接触って気持ちよい
- ユーザーが最終承認する

までを完成とする。
