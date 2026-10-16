# Jill v005 — 4K Texture移植レビュー候補 / 外観HOLD

2026-10-17。Human v004形状GOを継承。**新Textureの正式外観GOは未取得。**

- `jill-textured-rig-v005.blend`: v004のGeometry・全UV・130骨・39ch・20 Morph・16 anchor・23 ownerを保持し、4K BaseColorをpackedした編集正本候補。
- `jill-textured-rig-v005.glb`: 同blendからの静的Rig export。UV0を23材質へ明示。Skin/Morph/anchorあり。
- `jill-textured-review-bounded-v005.glb`: 5.875秒の限定確認clip付き。全Motionライブラリ・39ch runtime solverではない。
- `jill-basecolor-v005.png`: owner/host mask補修後4K画像。配色はレビュー用の暫定サンプルでありRGB承認を意味しない。
- `jill-basecolor-resampled-v005.png`: 元JPEGを三角形対応で正本UVへ転写した補修前画像。
- `source/tripo-return-original.glb` / `source/original-basecolor-0.jpg`: 返却原本と無変換抽出JPEG。再保存禁止。SHAはManifestに記録。

[比較・残課題・再現手順](../../../../../../docs/production/jill/texture-return-v005/Evidence.md) / [SHA Manifest](../../../../../../docs/production/jill/texture-return-v005/Manifest.json)。正式外観HOLDの主因は、全閉眼の立体縁・外眼角の隙間、Canonicalクローバー不在と位置判断、角の桃色境界・肌の連続性。診断paletteは採用していない。
