# Shushu v004 — 口B専用候補 v001

2026-10-15。開始HEAD `d5e9882dd644ca35c6944ed9e1c7b4163944890a`、branch `codex/shushu-v004-mouth-b-20261015`。**PC比較用の別名候補を保存。Human mouth=PENDING、原本置換・Motion量産=HOLD。** A前肢は既存HOLDのまま。Human指定「今回はPC比較まで」によりphone未検証。

[比較ギャラリー](index.html) / [生成モデルと現物](model-vs-closed-overview.png) / [閉口の前後](closed-before-after-overview.png) / [原寸切抜き](closed-mouth-crops-native.png) / [最終検証](validation-summary.json)。overviewは縮小、元PNGは640²。native boardと原寸切抜きはレンダー画素を拡縮していない。

## Authority / 保護

AGENTS、Goal√map、Handoff、[v004承認](../production-rig-v004/REVIEW.md)とAUTHORITY、[skin互換/B比較](../production-rig-v004-skin-compat/REVIEW.md)、[口v006](../tripo-mouth-depth-v006/REVIEW.md)、[v003下側口縁](../geometry-v003/lower-mouth-revision/REVIEW.md)、現在のモデル画像を参照。開始時remote main `8e4996c63c6d8fbb41954a2aa5cb5d892e45f01b`、production `0947d03efabbf3df04ed18e0ec6f99cc9efd2727` を照合。一括統合なし。

既存Human PASSの顔全体・外観・座位を保持。生成画像や技術照合をHuman PASSにしない。3枚のユーザー変更PNG、未追跡FBX/GLB、18–27参照等は[開始状態](starting-status.txt)と[3,507入力hash](protected-inputs.json)で保護。Handoff以外を一致させる。原本v004 GLB SHA256 `5fb05e5b7a9cbdb07a64beb5a511d6347c656d85d111ed16eccc533ecfc44cb5` は不変。

## 閉口モデル → 造形 → Texture

1. **最初に画像生成で[閉口モデル](closed-mouth-model-v001.png)を作成**。[入力・完全prompt・hash](closed-model-provenance.json)。鼻下の短い縦線から細いW字へつなぎ、柔らかい上下口縁が接し、口内・舌・ピンク模様を見せない閉口を基準にした。生成画像の目/頭幅/耳などの差分は採用していない。
2. 旧Headの実境界は幅約0.052H、Z≈0.601–0.606の浅いW帯で、下方のピンク/舌の描画と不一致だった。[元形状](source-topology-front-side.png)、[境界](boundary-front-side.png)、[元データ](mouth-source.json)。既存256境界頂点から、閉口Basisを幅約0.086Hの接触W字へ局所修正し、小0.20/中0.55/大1.00へ連続して下縁と顎を動かした。**Texture工程前に[Clay12枚](geometry-clay-states-native.png)を目視**した。
3. MouthInteriorを口縁から奥へ約0.032H続く9層の壁、OralBowlを奥の閉じ面、Tongueを下縁の後ろの独立した丸い形状へ再作成。温かい赤系の口内材質に弱いemission（0.35）を加えた。形状を伴う口内を作り、空洞の奥を透過する構造を解消した。
4. 最後に元UVと確定した閉口形状を対応させ、旧ピンク/舌/口枠を近傍の元クリーム色texelで除去し、実口縁のW線と鼻下の線を描いた。[Texture前後](texture-before-after.png)、[変更マスク](head-texture-changed-mask.png)、[数値](texture-authoring.json)。画像生成結果の全面Texture化はしていない。

Head変更は8,119/34,667頂点、元座標のX約±0.065、Z 0.543–0.624の前面。[全境界/範囲/変位](geometry-authoring.json)。閉口最大変位0.02039H、開口0.04020H。密な局所の頂点数比を顔全体の改変面積とみなさない。Head topology/UV/weight/キー名を保持し、対象外の全Shape座標を完全一致させた。口以外10objectの全shapeと骨rest/親も保持。[保護検証](authored-preservation.json)。

共通開口量は `max(MouthOpen, Tongue*.55, Smile*.18, Joy*.24, Surprise*.65)*(1-MouthClose)`。口縁・口内・舌が同じ量に従いMouthCloseが優先する。**Tongueは0.55開口を伴う専用候補の契約に変更**。既存全表情/旧clip互換を承認したものではない。閉口入口は上下接触モデルで、隠れた口腔面に重なりがある。全状態の防水ソリッド/非縮退を保証していない。

最初のruntime確認で旧口枠の淡い縁が見えたため、antialias色とUV島4texel余白も局所除去した。最終変更は **87,481/4,194,304 texel（約2.086%）**、許容範囲外0、UV変更0。約0.79%だった初期版の失敗画像は `iterations/texture-fringe/` に分離。[Texture工程でShape不変](texture-stage-geometry-invariance.json)。GLBではHead以外11画像の元圧縮バイトと対応材質を復元した（旧MouthInterior画像1本は未参照）。新口内3材質は候補固有。[復元記録](texture-material-restoration.json)：903 numeric accessorは工程前後で完全一致。

## authored / saved / PC local の比較

| 対象 | 根拠と結果 |
|---|---|
| Blender authored | [閉/小/中/大 × Front/Side/3Q 原寸](author-states-native.png)、proof 1/13/25/37f |
| saved GLB | [同12枚](saved-states-native.png)。21状態×14meshで最大位置差9.39e-7H、7 Anchor×169fで最大行列差9.54e-7。[読み戻し](saved-roundtrip.json) |
| PlayCanvas local | [同12枚](runtime-states-native.png)。2.22.2、Chrome/AMD Radeon WebGL2、640² DPR1、既存3mesh局所8-weight adapter共用 |
| runtime数値 | [19状態](runtime-checks.json)：Morph差約1.38e-18、Anchor行列差1.79e-7、console/page error 0 |
| 実GPU出力 | [8状態のHead/口内3mesh](gpu-mouth-readback.json)：位置差最大4.92e-5H、法線角最大0.277°、GL error 0。GPU Morph精度も含み、Skinのみの差と混同しない |
| 連続性 | 101開口サンプルで有限、1%刻み最大移動0.000513H、端点復帰一致。[Front](runtime/closed-open-closed-front.webm) / [Side](runtime/closed-open-closed-side.webm) / [3Q](runtime/closed-open-closed-3q.webm) は実Engine描画 |
| 座位保持 | [同条件の原本/候補 原寸](seated-preservation-native.png)。runtimeにもSeat/閉口優先/Tongue/復帰の3方向PNGを保存 |
| GLB構造 | [validator](glb-validation.json)：error0、既存形式のskinned非root警告14、未使用texture info1。14mesh/67joint、bind高1H/ground offset0。動的外観PASSとは別 |
| phone | 今回未検証。先行原本の実機結果を候補へ転用しない |

Blenderは640²、Cycles24sample、AgX、既存review照明、ortho幅0.56、target(0,-0.02,0.69)、Front(0,-3,0.615)/Side(-3,0,0.615)/3Q(-2,-2.5,0.65)。全身は幅1.14、targetZ0.5。PlayCanvasは同座標のY-up変換、orthoHeight0.28、既存ambient/key/ACES2。renderer間の画素一致は主張しない。原本の閉口はMouthClose1、候補の標準閉口は全口制御0で、どちらも閉口意図。座位の前後は両方MouthClose1。

runtimeの広い陰影/頬の横境界は[原本Front](runtime/before-front.png)にもある。口修正を理由に、目/頬/鼻/頭全体の材質や法線を再設計していない。実画像の比較と数値を別々に判断した。

## GO / HOLD・Human確認

**GO：口専用候補の保存、限定技術検証、PC Evidenceのレビュー提示。HOLD：Human外観承認、原本置換、正式Rig/Motion導入・量産。**

Codexの目視では閉口時のピンクと舌が消え、細いWの閉口に見える。大開口では実口縁・赤い口内・独立舌が見える。小開口はW形の細いすき間が強く、真横は頬に隠れて口内の見える量が少ない。Front可愛さとSide自然さの最終PASSは出さない。

Human確認項目：

1. 最優先：閉口が「ちゃんと閉じた口」か。Wの細さ/幅、鼻下の接続、顎へのつながりが可愛いか。
2. 小開口のW形、中/大の下縁と顎曲線、runtimeで強く見える白い下縁の厚さと口角の陰影、Sideの少ない見え方と3Qの奥行きが自然か。
3. 口内が平坦な黒穴に見えず、舌が下縁より後ろに収まり、閉→開→閉に飛び/色残りがないか。
4. 原寸/全身/座位で目・鼻・頬・耳・頭身・承認済みBody identityを損なっていないか。

A前肢は今回の候補で解消したと扱わない。元v004置換、製品Motion量産、他キャラ変更、外部upload/課金は行っていない。

## 成果 / 再現

`assets/grimo/production/shushu/tripo/geometry-v003/rigging/` の `shushu-v004-mouth-b-v001.blend` が編集元、`-proof.blend` が169f/24fpsの口・座位・閉口優先・復帰の診断。`.glb` は同診断clip1本の別名候補。最終hash/サイズは[validation-summary](validation-summary.json)。

Blender5.2.1、Python3.13+numpy/Pillow/scipy、node、既存PlayCanvas2.22.2/@playwright/test、Chromeを使用。新規導入なし。生成モデルはhash付きで凍結し、生成の再実行をbit同一条件にしない。

```powershell
blender -b --python scripts/blender/inspect-shushu-v004-mouth-b.py
python scripts/3d/inspect-shushu-v004-mouth-b.py
blender -b --python scripts/blender/repair-shushu-v004-mouth-b.py -- --build
blender -b --python scripts/blender/repair-shushu-v004-mouth-b.py -- --render --clay
# 造形を目視してからTexture工程
python scripts/3d/texture-shushu-v004-mouth-b.py
blender -b --python scripts/blender/repair-shushu-v004-mouth-b.py -- --texture
blender -b --python scripts/blender/prove-shushu-v004-mouth-b.py -- --export
python scripts/3d/repack-shushu-v004-mouth-b.py
blender -b --python scripts/blender/prove-shushu-v004-mouth-b.py -- --verify
blender -b --python scripts/blender/prove-shushu-v004-mouth-b.py -- --render
blender -b --python scripts/blender/prove-shushu-v004-mouth-b.py -- --render --saved
blender -b --python scripts/blender/audit-shushu-v004-mouth-b.py -- --audit
blender -b --python scripts/blender/audit-shushu-v004-mouth-b.py -- --render
blender -b --python scripts/blender/audit-shushu-v004-mouth-b.py -- --render --full
blender -b --python scripts/blender/audit-shushu-v004-mouth-b.py -- --render --full --candidate
node scripts/3d/shushu-v004-mouth-b.mjs --validate
node scripts/3d/shushu-v004-mouth-b.mjs --serve
# 別terminal
node scripts/3d/shushu-v004-mouth-b.mjs --capture
node scripts/3d/shushu-v004-mouth-b.mjs --capture --before
node scripts/3d/shushu-v004-mouth-b.mjs --gpu
python scripts/3d/board-shushu-v004-mouth-b.py
python scripts/3d/report-shushu-v004-mouth-b.py
```

Viewer：`http://127.0.0.1:8767/docs/production/shushu/evidence/production-rig-v004-mouth-b/index.html`。再生成は別名候補と今回Evidenceだけを更新する。全体buildや無関係な最適化は行っていない。

保護入力の照合は開始時workspace固有。未追跡のユーザー参照等がないcloneでは、その入力を復元しない限り同じ保護照合は再実行できない。生成モデル・候補・レンダー・数値Evidence自体はこのbranchに保存する。
