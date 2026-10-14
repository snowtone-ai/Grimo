# Shushu v003 — eye-outline Texture candidate v002

2026-10-14 / Codex visual review: **対象箇所の外観 PASS / Human Gate PENDING**。

添付の黒線は、ピンク目囲みの上〜外周に並走する淡い帯と、鼻側〜下側の白っぽい二重境界を示す。囲まれたピンク面全体の除去ではない。保存候補を実際に確認し、今回の二重境界が解消し、不自然な切れ込み・輪郭欠け・新しい白縁・継ぎ目・ぼかし跡がなく、瞳と笑顔の可愛さが維持されていると判断した。最終のHuman判断は未受領。

## Authority・開始基準

- 実行branch: `codex/grimo-motion-zero-based-design-20261011`、開始HEAD `cfc10d459c09f1e781b544c9d56b59a00c7aa16f`。ローカルGoal√map、Handoff、最新正式Geometry Evidenceを照合。Handoffを現在値・承認の代用にしていない。
- 元GLB: `shushu-geometry-v003-tripo.glb.glb`、実LFS SHA256 `338ad5f8c67906917579ddbb804a4f7f51d8fec6c42328bb545adc87c1bf077b`。
- 開始候補v001: 口のみ修正済み、SHA256 `8d4420d5e8baae6c1cd3d0c4b215d89af5ee157be1c1a3e54df4721d5a5eac09`。
- 独立候補v002: [保存GLB](../../../../../assets/grimo/production/shushu/tripo/geometry-v003/texture-cleanup/shushu-geometry-v003-tripo-texture-candidate-v002.glb)、SHA256 `d9bfbac01404c39a22fe14306a4d225c7b8efde34b3402cca0e9e9933d40b4d7`。元GLB・v001を上書きしていない。
- Canonical Identity・承認済みBody-only front/left/rightを参照。[前回の口修正/診断](../tripo-texture-v003/REVIEW.md)と[最新正式Geometry](../geometry-v003/lower-mouth-revision/REVIEW.md)は保持。

## 画像による確認

- [承認済み正面 → v001 → v002](00-authority-before-candidate.png)
- [正面・左右3/4・左右側面：before / saved candidate / difference×4](01-five-angle-before-candidate-difference.png)
- [承認済み左右側面との比較](02-approved-sides-before-candidate.png)
- [局所マスク位置](03-local-mask-overlay.png)、[両目の3倍拡大](04-eye-closeups.png)
- [Humanの黒線](human-annotation.png)、[Headだけの診断](head-only-diagnostic.png)
- 原寸の再読込レンダーは `renders/`。`before`は元GLBではなく**口修正を保持したv001**。図中の「source GLB」はこの開始候補を指す。

全5角度の原寸と拡大画像を実際に開き、Body-onlyと比較した。ピンク目囲み本体、濃いまぶた/目の輪郭、花柄の瞳、ハイライト、チーク、笑顔・舌を維持。意匠としての白い毛の描線とチークの白い点は除去対象にしていない。[視覚判断と閲覧画像hash](visual-review.json)。

## 原因と最小修正

12メッシュ・12個別TextureのうちHeadに目の濃い描画と二重境界が焼き込まれている。独立したEye_L/Rと重なるため、すべてを単純な「別レイヤー」として消せない。Head-onlyにも同じ帯があり、flat Head診断と合わせ、今回の帯がHead Texture編集で改善できることを確認。重なりの全原因やGeometryの良否までは断定していない。

鼻と瞳ハイライトで黒線を未加工の正面へ対応付け、左右別に不要帯の両側を追った細いマスクを作った。上部/外側の処理範囲はマスクから算出。既存のUV投影・Head最前面ray確認を再利用。built-in image_genは局所のピンク/クリーム修正材料を一度だけ生成し、全生成画像をモデルへ貼り直していない。[生成記録](IMAGEGEN.md)。

画面座標で修正材料をサンプルし、隣接する既存色と合わせた。濃い元画素/濃い生成色は保護し、チークとの下側接続は画面y620〜650の局所重みでつないだ。全体ぼかしはない。補間用の隣接2 atlas texelだけ追加し、対象Head PNGの画素だけ変更。`repair-config.json`/`projection-masks.json`は最終の輪郭、`applied-projection-map.json`は適用可能なtexel、`textures/changed-texels.png`は実際に変更したtexelを記録。

## 対象別検証

[構造/画素検証](candidate-validation.json)、[同一描画条件/保護入力検証](review-manifest.json)。

| 確認 | 結果 |
|---|---|
| v001に対するHead変更 | 128,907 / 4,194,304 texel = **3.0734%** |
| 選択範囲外のHead画素 | 変更0、lossless PNGを維持 |
| 他11枚のTexture | 全payloadがbyte一致、Eye_L/R・口内を含む |
| メッシュ/UV/材質設定 | JSON各subtree一致、元BIN prefix全byte一致 |
| 口修正のtexelとの交差 | 0、v001の修正保持 |
| 正面の口/下側顔 | y670以降の変更0 |
| 正面の対象目領域外 | 変更0（マスクbbox+6pxによるrender確認。厳密なatlas範囲外0とは別） |
| 瞳内部のrender比較 | 左右の記録済み内部矩形とも変更0 |
| 保護入力 | 758ファイルhash一致、変更0 |
| 5角度のcamera/描画条件 | 同一、保存v002 SHAとrender元SHA一致 |

広めの瞳矩形には背景も入り、左のクリーム背景(381,619)にRGB各1階調の変更が1画素あった。瞳内部の変化ではなく、右の広い矩形と左右の実際の内部矩形は変更0。Eye画像自体もbyte一致。この追加確認を隠さず記録した。

正式Blender Geometry・Shape Keys・285f Motion proof・他キャラ・既存ユーザー差分を保護し、全体build/test・サブエージェントを使用していない。元GLB・v001・正式Rig資産の置換、外部Tripo操作、課金、mainマージなし。今回の保存は静的Tripo候補であり、正式Rig採用を意味しない。

## 不採用試作と残る判定

`rejected-trial-01`〜`09`に実GLBの試作render/検証を保持。01は外周マスク不足と白い切れ込み、02は隣接色処理の白い点/下端、03は右外周の帯/鼻側の楔、04–05はマスク間の切れ込みと外周の不自然さ、06は左外周の残り、07–08は左上部の小さな色片、09は下側チークとの接続を理由に採用しなかった。最終v002は局所材料の直接サンプル、両側の境界マスク/接続箇所修正、下側だけの重み調整で再保存・再読込したもの。

Codexは**今回の対象箇所に不自然さを認めず、可愛さを維持した候補として外観PASS**と判断する。Human GateはPENDING。可愛さの客観的100%保証や正式Geometry/Rig/Motion/runtime完成の判定ではない。先行正式Geometryの下側口縁〜顎とFront承認も引き続き別途PENDING。

## 再現

既存scriptsにconfig指定だけを追加。デフォルトの前回口修正は保持。Nodeはsharp、Blenderは5.2.1 LTS、比較boardはPython/Pillow/numpyを使用。

```powershell
blender --background --python scripts/blender/review-shushu-tripo-texture-v003.py -- --eye-config docs/production/shushu/evidence/tripo-eye-outline-v002/repair-config.json --projection
Copy-Item -LiteralPath docs/production/shushu/evidence/tripo-eye-outline-v002/textures/imagegen-local-repair-projection.png -Destination .git/shushu-eye-material-replay.png
node scripts/3d/patch-shushu-tripo-texture-v003.cjs .git/shushu-eye-material-replay.png docs/production/shushu/evidence/tripo-eye-outline-v002/repair-config.json
blender --background --python scripts/blender/review-shushu-tripo-texture-v003.py -- --eye-config docs/production/shushu/evidence/tripo-eye-outline-v002/repair-config.json --render --asset assets/grimo/production/shushu/tripo/geometry-v003/texture-cleanup/shushu-geometry-v003-tripo-texture-candidate-v002.glb
python scripts/blender/review-shushu-tripo-texture-v003.py --eye-config docs/production/shushu/evidence/tripo-eye-outline-v002/repair-config.json --boards
```

生成済み材料は別のローカルpathへコピーしてからpatch引数に渡す（Evidence内の同名input/outputへの自己copyを避ける）。再生成の技術reportは外観未判定へ戻るので、保存モデルを再度目視してから別途visual-reviewを記録する。
