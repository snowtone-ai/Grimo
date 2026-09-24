# Carol face / ear authority match v001

正式 Normal Front / Side、Skin Front / Side、Ear Module、canonical identity を基準に、顔と耳を再構成した Human review 候補。旧 F2 の局所移動・旧 Ear v002 の維持を前提とせず、顔の断面と耳の立体を作り直した。**Human perceptual acceptance は未実施。正式 authority の昇格ではない。**

- Branch: `codex/carol-face-ear-authority-match-v001`
- Exact source: `656d6510b6ca81205cca1fced46d176f10d7aca7` / `codex/carol-face-ear-production-v003`
- Asset: `assets/grimo/production/carol/blender/carol-face-ear-authority-match-v001.blend`
- Final asset commit: `git log -1 --format=%H -- assets/grimo/production/carol/blender/carol-face-ear-authority-match-v001.blend`
- Active references: `assets/grimo/source/carol/approved-3d/authority.json`。全 manifest hash を保存後検証。資料の改変なし。

## Human review

1. [human-review.png](human-review.png) — 新版の顔 Front / 3Q / Side と耳。
2. [face-front-comparison.png](face-front-comparison.png)、[face-side-comparison.png](face-side-comparison.png) — 正式 Normal / Skin、旧版、新版、固定登録 overlay。
3. [face-spatial-review.png](face-spatial-review.png) — 同じ立体の Front / 3Q / Side / Top。3Q と Top は派生診断。
4. [ear-four-view-comparison.png](ear-four-view-comparison.png)、[ear-contour-overlay.png](ear-contour-overlay.png) — Module 4 方向および Front / Top 輪郭差。
5. [ear-side-camera-diagnostic.png](ear-side-camera-diagnostic.png) — Module Side のカメラ解釈。厳密な直交 Side と混同しない。
6. [attached-three-view.png](attached-three-view.png) — 共通の絶対カメラで、頭・耳と既存胴体の関係を比較。
7. [authority-measurements.png](authority-measurements.png)、[measurements.json](measurements.json) — 測定点、登録座標、耳断面、資料 hash。[renders/](renders/) に合成前の新版 PNG。

全レンダーは保存された単一の neutral 3D 形状を Blender Cycles で描画。顔の比較は共通カメラ・照明・倍率。正式画像には明記した平行移動と等方スケールのみを適用。レンダーの形状を画像加工で変更していない。耳の定性比較パネルは余白を切り、等方倍率で表示。定量 overlay は旧版／新版とも root を基準に固定した module 座標を使用する。

## 再造形

- **頭部**: 15 本の高さ断面で顔幅・正中前端・側面中心・後端を指定。低い頬の張り、短い口元、顎の丸み、額から頭頂への推移を再構成。既存の連続 chassis topology を使い、HEAD の全 351 制御頂点と短い接続帯を更新。胴体の制御頂点 379 以降は完全保持。
- **目と眼窩**: 眼窩を斜めに回り込む面に変更し、顔面へ raycast した曲面上に目と薄い瞼を構築。正面開口 0.137 × 0.149 H、中心間 0.324 H を維持し、中心 Z を 0.412 H に設定。側面の眼球 X 幅は約 0.082 → 0.130 H。中心の浮き 0.018 H、縁 0.0015 H。正式 Front の眼内色・金色・星・ハイライトを曲面 UV に配置し `.blend` に pack。平面 billboard ではない。
- **鼻・口・頬**: 鼻幅 0.039 H / 中心 Z 0.378 H を維持し、前後厚を短縮して新しい顔面へ接続。口幅 0.091 H の閉じた二重弧と人中を再構成。クリーム色と柔らかい頬色を頭部から接続帯へ連続させた。
- **耳**: Module Front と Top の raster 断面から 95 × 24 の閉じた shell を再構築。上辺の落ち方、下辺の膨らみ、Top の前後厚、丸い末端を独立制御。内耳は同じメッシュに含まれる浅い凹面と色領域。root `(0.386, ±0.235, 0.579) H`、後方 sweep 35°、局所全長 0.413 H。左右は鏡像。旧 provisional test shape keys は新しい形状に引き継いでいない。
- **範囲**: 変更した形状オブジェクトは chassis、両目、両瞼、鼻、口、人中、両耳の 10 個。胴体・脚・蹄・尾の再設計なし。比較用 studio 照明と scene provenance も更新。fleece、rig 完成、runtime は今回の成果に含まれない。

## 数値比較と解釈

| 固定登録での指標 | 旧版 | 新版 |
| --- | ---: | ---: |
| Skin Front 可視輪郭 MAE、18 samples | 17.75 px | 2.54 px |
| Skin Side 前面輪郭 MAE、11 samples | 59.49 px | 3.21 px |
| Normal Side 前面輪郭 MAE、9 samples | 40.33 px | 3.62 px |
| Ear Front silhouette IoU | 0.610 | 0.966 |
| Ear Top silhouette IoU | 0.730 | 0.961 |

詳細は [fit-metrics.json](fit-metrics.json)。輪郭値は選択したフィッティング点の誤差で、画像全体の一致度や独立した検証スコアではない。手動の画素境界には約 ±3 px の不確かさがある。耳の IoU は外形のみを評価し、内耳・質感・かわいさの評価を含まない。

登録は Normal Front `1011 px/H, origin 646, ground 1162`、Normal Side `916, 144, 998`、Skin Front `994, 626.5, 1075`、Skin Side `1160, 82, 945`。Normal Front の顔は胴体中心より約 20 px 右にあり、顔中心で対称化した。Skin Side は鼻・目・顎を合わせた **face-local** 登録であり、既存の全身登録を成立したことにはしていない。

## 残差・判断が必要な点

- Skin Side の頭頂は、この顔登録では約 Z 0.657 H、Skin Front は約 0.698 H。目と鼻と顎を固定した単一立体では完全には一致しない。Front の頭頂と幅を優先している。
- 3Q では回り込む眼窩のため、目が Front より横に広く見える。瞼の縁、顎から頬への陰影、後頭部から首への流れは Human による立体的な自然さの確認が必要。
- Ear Module Side はカメラが未較正。Front / Top に整合する立体の厳密な直交 Side は sheet と一致しない。俯角 14.7°・roll 11° の比較も併記したが、これはカメラの解釈であり、Side の完全一致や authority の変更ではない。内耳の縁・末端の厚み・attached Side の root 位置にも差が残る。
- 色・陰影は資料の描画と完全一致ではない。眼内の星と主要ハイライトは正式画像に由来する固定 pigment。動的な視線や照明応答の完成品ではない。
- 完成 fleece を含めた最終 Hero appearance／耳 clearance は未確認。今回の head-only と既存胴体への attachment の review に限定する。

## 検証・再生成

[validation.json](validation.json) に保存・再読込、対象外 snapshot、胴体制御点保持、authority hash、packed pigment、PNG decode / hash を記録。頭部 chassis と両耳は finite、外向き、nonmanifold edge 0、非隣接三角形の自己交差 0。中立形状の検証であり、変形・rig・runtime の合格を意味しない。

Python は Pillow / NumPy / SciPy、Blender は 5.2.1 を使用。repo root で順に実行する。

```powershell
python scripts/blender/carol-authority-match-evidence-v001.py --measure
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' -b --python scripts/blender/build-carol-authority-match-v001.py
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' -b --python scripts/blender/build-carol-authority-match-v001.py -- source
python scripts/blender/carol-authority-match-evidence-v001.py --compose
```

既存 `build-carol-ear-production-v002.py` の snapshot / manifold check / render helper のみ再利用。009 donor は不使用。生成中の atlas と中間レンダーは OS temp、提出物は上記 asset と本 evidence directory。

## 次の handoff

**HUMAN — Face / Ear authority-match review**。正式 Front / Side と新版の顔の同一性、3Q の目・頬・顎、耳の内面・厚み・attached root を判定する。承認後にその結果を次の制作判断へ渡す。今回の数値改善だけで authority 承認や runtime 移行を決定しない。
