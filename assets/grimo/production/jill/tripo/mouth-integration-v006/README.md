# Jill v006 — integrated local mouth candidate

**2026-10-18 Human口外観GO。モデル全体の完全完成は未達。** 鼻下の不要cream帯・追加外皮の重なりを局所的に解消した候補。元v005/v004は不変保持。

- `jill-textured-rig-v006.blend` — Texture packed、neutral保存、130骨/39ch/20Morph/16anchor。
- `jill-textured-rig-v006.glb` — static shipping候補。drivers/authoring UIはglTF仕様上含まれない。直接Morphを動かす実装では、開口/smileへ閉口ゲートを同様に適用する必要がある。
- `jill-review-bounded-v006.glb` — 13代表状態のbaked QA clip。全Motionライブラリではない。

static GLBの口を直接操作する場合は、[mouth-controller.mjs](../../../../../../scripts/3d/jill-mouth-v006/mouth-controller.mjs) の `createJillMouthController(entity)` を一度生成し、`set({mouth_close, mouth_open, 'smile.L', 'smile.R'})` を呼ぶ。省略入力は0、各入力は0〜1。閉口を優先する。別animation trackが同じ4weightを書く場合は、そのtrackを止めるかanimation評価後に口制御を適用する。15同時入力と連続開閉・復帰をstatic GLBの実PlayCanvasで検証済み。

[原因・局所Geometry/UV/driver差分・actual render/runtime・未解決点](../../../../../../docs/production/jill/mouth-integration-v006/Evidence.md) / [比較](../../../../../../docs/production/jill/mouth-integration-v006/mouth-detail.jpg)。

Texture画像そのものはv005とバイト一致。外部ファイル再リンクは不要。局所面は元の専用口UV島を再利用しており、全Geometry/全UV不変のimage-only派生ではない。
