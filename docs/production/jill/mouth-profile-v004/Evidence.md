# Jill v004 — 口〜顎の横顔を顔曲面へ統合

2026-10-16。Human指定の最後の局所修正を実装し、**修正後の4K BaseColor用Pre-Texture Technical GO候補を保存**。Human最終visual GOは代行しない。Tripo upload/課金/正式Texture生成は未実施。

## 今回のHuman指示 / Authority

Humanは赤線の口縁〜顎が横から「ペラペラ粘土を貼り付けている」ように見える点をFAILとし、顔曲面へなじませ独立パーツ感を消すこと、正面/3Qの可愛さを維持することを指定。「あとはこの修正だけで、Tripoテクスチャフェーズに進む」を今回の形状修正範囲とする。他の瞼/翼/葉の追加修正を必須化していない。全poseや正式Textureを承認したと解釈もしない。

添付原物を [human-redline-face-review.jpg](human-redline-face-review.jpg) として保存。SHA-256 `44a085ce26207bda32d253531ec5a012c3336cb1c3f6bcc1f13bcb7f567edc17`。これは修正指示の参照で、v004の承認画像ではない。

開始 `9c25c6bf86da6ffcced4439ea2456d112befe98c` / clean。branch `codex/jill-mouth-profile-v004-20261016`、既存専用worktreeを再利用。main `73617ce2d3c724c86aed82dfc2a09cd220e5d194` を再fetchしAGENTS/Goal√map/Handoffを再確認。v003正本/Evidence、v002、元checkoutのShushu変更は保護。[事前方針](Plan.md)。

G3の局所顔面とMorph接続→G2の自然な開閉口→G1の可愛さ/本人性→G0の愛着。技術数値のために別の顔へ変えない。

## 原因と修正

v002由来の追加口面は顔本体とは別の浅い解析曲面だった。外周が実際の丸い顎から浮き、閉口では元の露出肌を35mm後退させるMorphも重なり、板状の口下が目立っていた。単なる奥への移動では閉口時に元の口穴のギザギザが露出するため、その案は採用しなかった。

顔本体の口周囲3,055サンプルから左右対称な曲率をfitし（周囲skin fit RMSE 1.182mm）、追加口外肌の奥行きを顔曲面へ合わせた。口内/舌/歯も口縁に連続する奥行きへ整合。元の口周囲179頂点はY方向だけ局所fairingし、露出肌52頂点の閉口時後退を除いた。外周は肌へ埋まり、内側は0.5mmの穏やかな口縁とする。

**全21 key（Basis含む）のX/Zは完全保持**。口周囲以外の座標、polygon頂点順/材質所有、3層UV、weights/groups、130 bones rest/parent、drivers、39ch、16 anchorは一致。全体remesh、眼/瞼/鼻/翼/葉/Rig再制作なし。今回の意図的なY変更があるため「元Basis全頂点差0」とは主張しない。変更は各key 1,948頂点、最大Y差はBasis 25.836mm、閉口key 60.836mm（旧35mm後退を除いた分を含む）。[対象ID・全値](repair-report.json) / [保持契約](preservation-proof.json)。

## 実レンダー確認

- [横顔の主要3状態、左v003/右v004](side-key-poses.jpg)
- [横顔6状態の比較](side-before-after.jpg)
- [正面・3Qの修正前後](front-3q-before-after.jpg)
- [反対側の横顔・3Q](opposite-side-before-after.jpg)
- [v004の全顔面レビュー](face-review.jpg)

neutral、close .5/1、open 1、blink .5/1とneutral復帰を同条件のWorkbench実レンダーで保存して開いた。反対側はneutral/close .5/1/open 1を比較。横の独立した板状突出がなくなり、口下〜顎が丸い輪郭につながる。正面/3Qは目・鼻・顔幅・口の幅/高さを保ち、笑い口のまま下顎の貼付け感を除いた。可愛さの最終判定はHumanに残す。

[画像差分](render-review.json)の8/255超の差分bboxは口周囲に限定。顔全体をpixel一致とは言わない。neutral復帰はfront/side/3Qのpixel完全一致、評価頂点差0。[復帰proof](recovery-proof.json)。旧305frame、全Motion/mobileを重複実行していない。

## UV / Textureへの影響

UV0 `Jill_Texture_UV0_v003`、UV1 `v002_Previous_Active_Preserved`、UV2 `v002_Source_UV_Preserved` は名前/順序/全loop座標がv003と完全一致。23paint ownerも一致。編集polygon topologyは同じだが、曲面変更によりBlenderの自動対角線による三角形16行が変わったため、UV交差も再測定した。

[exact audit](after-uv-audit.json): 61,321三角形/2,203島、正面積overlap 0、意図的共有0、UV縮退0。既存Geometry縮退1枚は不変。4Kの最小島間23.894px、tile端20.144px。1K HOLD、2Kは余白のみPASS・細部未実証、4K基準、8Kは測定上候補という解像度条件は継続。

[密度/伸びの全値](uv-geometry-audit.json)は1K/2K/4K/8Kで保存。口外肌/口内/舌のanisotropy p95は1.516/1.271/1.375、4K密度medianは約1176/1199/1210px/m。口外肌の極小sliverに最大44.676の伸びが残る（同領域の面積比0.0213%）。既定の同系肌色充填で扱い、ここへ細密図柄/Normalを描く品質は保証しない。見た目を崩して数値だけを下げない。

閉口で新しく維持する元肌にも開口模様を印刷しないため、既存ownerとは別に [局所host肌mask](mouth-host-fill-mask.png) / [polygonと画素数](mouth-host-fill-mask.json) を保存。UV/材質は変えていない。`sanitize-jill-mouth-return-v004.py input.png output.png fills.json` はv003の瞼/口外肌/口腔/舌/歯の明示充填に加え、このhost肌を同じ承認肌色で充填する。4K固定。`mouth-host-skin` と `mouth-skin` のRGB一致が必須。今回の [試験色](synthetic-fills.json) は診断専用で正式配色ではない。[充填試験](protected-fill.log)。

## 保存・FBX/GLB・Morph

[transfer-proof](transfer-proof.json): 修正後neutralからclay FBX/GLBを再作成。診断画像付き合成返却をfresh importし、画像だけを修正Rigへ戻し、packed blend保存/再読込、Rig GLB export/fresh importを確認。両形式decode画素差0。GLB位置差0、UV差2.98e-8、FBX位置差1.744e-7m、UV差0。Rig再importは位置差最大3.073e-7m。130骨/20 Morph、TEXCOORD_0/1/2、baseColor texCoord=0を保持。

さらに [posed GLB proof](posed-glb-proof.json) でfresh Rig GLBのclose .5/1、open 1を元Rig評価面と照合。全3状態で位置差最大3.073e-7m、UV差2.98e-8。39ch solverをglTFへ移した証明ではない。

保存返却Rigの [GLB閉口](renders/returned-glb-closed.png) / [FBX閉口](renders/returned-fbx-closed.png) を実renderし開いた。診断owner色でパーツが別色に見えるのは試験用で、正式肌色は同色充填する。入力候補へ診断画像を含めていない。

## 引渡し

[投入候補README](../../../../assets/grimo/production/jill/tripo/mouth-profile-v004/README.md) / [SHA・絶対パス](Manifest.json) / [停止条件](TripoHandoff.md) / [remote照合](RemoteReceipt.json)。旧v003の入力ファイルを今回の修正版として使わない。

Humanは今回の口修正を最後の形状修正と指定しているため、他の旧課題を新たな形状作業へ拡張しない。修正版のHuman visual GOはPENDING。実Tripo UI/料金/Original UV選択可否/返却はUNKNOWN、upload/課金/正式Textureは今回未実施。実返却で形状/UV/ownerが変われば既定の停止条件に従う。
