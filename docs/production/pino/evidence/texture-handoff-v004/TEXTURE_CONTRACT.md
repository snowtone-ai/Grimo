# Pino C Texture Handoff v004 — UV / Material / Return contract

Human Pre-Texture Gate=PENDING。Texture GO=NO。2026-10-16。UV契約は候補資産間の対応を固定するもので、外観承認ではない。

## 渡すもの

| 用途 | ファイル | 内容 |
|---|---|---|
| Tripoへの入力候補 | `pino-c-v004-tripo-input.glb` | Neutralの4mesh / 5使用材質、50,763三角形。Skin / Morph / animation / 画像Textureなし。Tripo操作は未実施。 |
| 編集正本 | `pino-c-texture-handoff-v004.blend` | Neutral保存。70骨、LBS4、従来の顔制御とv004のPose補正。画像Textureなし。 |
| Rig付き可搬レビュー | `pino-c-v004-rigged-review.glb` | 同一Basis・UV、Skin / Morph POSITION・NORMAL、対応ID。animationなし。Tripo入力にこれを選ばない。 |
| 逆対応 | `pino-c-v004-return-map.npz` | mesh indexごとのposition、corner_vertex、uv、polygon_sizes、material_id。index→名前・key名はdelivery-contract.json。 |

元FBXを置換する新Geometry Masterではない。元FBX / 元GLB / v001〜v003はそのまま残す。

## UVと所有

`PinoUV_v003`を全4meshでそのまま維持する。Basis座標・面順・corner順・UV座標・材質の面所有・元corner normalのSHAはv003と一致。共通0–1 atlasの50,763三角形で正面積UV重複0、ゼロ面積UV0。Atlasを各mesh別に0–1へ再packしない。UV島は細かい。数値検査はTripoのペイント品質・島間padding・十分なtexel densityを保証しない。

| 使用材質 | 所有 | 戻すときの注意 |
|---|---|---|
| `Pino_Skin` | 主体の皮膚・毛・尾・鼻口周辺 | 皮膚へ開眼や開口の固定色を焼かない。顔、頬、白腹、尾の色分けはCanonical / 承認Body-onlyに従う。 |
| `Pino_Eye_L` / `Pino_Eye_R` | 主体内の独立した左右眼surface | v004では眼面を弧へ縮めて閉眼線にする。左右を混ぜず、閉眼時の色伸びも確認する。 |
| `Pino_LidSkin` | 左右の既存外付け瞼 | v004の新閉眼候補では常にBasis内へ退避。旧keyは履歴として残すが新Squintと混用しない。不可視面のTripo塗りは保証されない。 |
| `Pino_OralInterior` | 可動内張り | 頭の材質slotにも残るが頭の面割当は0。口内の暗色は内張りへ。閉口・開口制御と同期。 |

Tripoに未露出の内側、埋没瞼、尾の内殻が着色されるとは限らない。皮膚色/口内色は既存slotの編集で補完する。3重尾殻は消さず同じ色設計を保つ。削除・結合・retopology・UV再packをTexture後の通常修正に含めない。

## Textureを戻す手順

1. この入力GLBとfile-manifestのSHAを記録して渡す。Tripoの出力は別donorとして保存し、Blendの既存geometry / rig / shape key / vertex group / normal bankを置換しない。
2. 出力が入力の面・UVを維持した場合は、その画像を既存slotへ接続する。まず所有ごとに確認し、NPZのcorner UVと入力の`TEXCOORD_0`を比較する。glTFはVが反転するため、Blender側は`(u,1-v)`。単なる頂点数一致を対応の証拠にしない。
3. 出力が新UVまたは新meshになった場合、donorの見た目を既存UVへ再投影/bakeする。受け側はこのBlendのNeutral複製と共通atlas。Skin・左右眼・口内を分けて対応し、近接する眼と皮膚、尾の重なった殻を横断してnearest転写しない。ray距離・cageと隠れ面は実物で決める。Bakeの方法やTripoの保持動作は今回未実行・UNKNOWN。
4. 画像だけを編集正本へ戻し、同じ閉眼/口/接触/休息/尾probeを再描画する。輪郭の変化は画像転写の問題かPoseの問題かを切り分ける。元Blendへdonorのarmature / rest pose / vertex orderを移植しない。
5. donorが対応不能な造形を返した場合は受入HOLD。元の制作資産を温存したままTextureの転写・再制作を検討する。新mesh採用を暗黙の解決にしない。

`_PINO_VERTEX_ID`は各編集meshの頂点index、`_PINO_CORNER_ID`はcorner index。GLBのUV/normal seamによる頂点分割後も両方で対応する。両属性はTripoが保持する保証はなく、保持されなかった場合は入力とNPZを対応正本にする。

## Rig / Morph / Normal

支持骨のUpLeg起点を体内上方へ移し、Leg起点を合わせた。70骨の名前・親階層は維持するが、v001/v003の脚のlocal keyframeをそのまま使う互換性はない。必要ならworld目標からretargetする。旧IK制約を除去し、probeは伸長なしの解析2骨解と足の姿勢固定。全Motionへの一般化は未実装。

`scripts/blender/pino-texture-handoff-v004.py`の`body_state()`がPoseと対応補正を同時設定する。contactは0/.5/1、restは0/.25/.5/.75/1、tailは-1/0/1の組で使う。probe-controls.jsonに世界Skin差分とMorph値、runtime-controls.jsonにglTF local骨行列を保存。Morphだけを単独で上げない。contactの逆Skin補正はbind空間で最大約103mmあり、任意Pose用の汎用補正ではない。

BlenderのFREE custom normalはArmatureだけでは変形に追従しない。`refresh_preview_normals()`をPose/key編集後に呼ぶ。保存BlendはNeutralのpreviewを保持するが、手で骨を動かすだけではpreview法線を更新しない。export時はNODES previewを無効にし、元corner normalと各`PinoDN_*`をGLBのNORMAL targetへ格納する。PlayCanvasではNORMAL MorphとSkinが実行される。Blender標準glTF importだけではMorph法線を結線しないため、付属reimport scriptのbridgeを使う。

後工程でPose補正を変えたら同じUVのままnormal bankを再計算する。法線場・補正Poseの移植なしに別エンジンへ渡した品質はUNKNOWN。
