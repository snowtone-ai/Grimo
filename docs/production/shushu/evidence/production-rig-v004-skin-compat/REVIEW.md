# Shushu v004 — Skin compatibility / Xiaomi 14T Pro / local A・B HOLD

2026-10-15。**総合判定 HOLD。原本置換・Motion量産は禁止。** 既存Human PASSはレビュー済み外観・座位に限定する。同日追加Human Reviewで前肢Aと口BはHOLD。Skin互換数値と実機再生の成立を外観PASSへ拡張しない。

開始HEAD `0947d03efabbf3df04ed18e0ec6f99cc9efd2727`、制作元branch `codex/grimo-motion-zero-based-design-20261011`。専用branch `codex/shushu-v004-skin-compat-20261015`。取得・照合した最新main `8e4996c63c6d8fbb41954a2aa5cb5d892e45f01b`。main一括統合なし。AGENTS、Goal√map、Handoff、[承認時v004](../production-rig-v004/REVIEW.md)、[先行runtime HOLD](../production-rig-v004-runtime/REVIEW.md)を参照。

承認済みGLB SHA256 `5fb05e5b7a9cbdb07a64beb5a511d6347c656d85d111ed16eccc533ecfc44cb5`、29,691,796 bytes。原本、制作/proof Blender、顔・体型・rest・Morph・Texture/UV・7 Anchorは変更していない。旧Evidenceも保持。今回の変更は別名候補、独立診断Viewer、測定・Evidence・Handoffのみ。

## 2方式の比較と選択

| 方式 | 8-weight参照との差：最大位置 / 最大法線 | 実装・負荷 | 判定 |
|---|---|---|---|
| 標準PlayCanvas 2.22.2（比較元） | 0.0177415344H / 5.2118803° | JOINTS_1/WEIGHTS_1欠落。ラスタ位置は上位4個の正規化と同等 | 不適合 |
| 候補1：姿勢横断4-influence最適化 | 0.00530314035H / 3.37692727° | 357頂点、91 witness＋90中間の181姿勢で位置と法線残差を最適化。元の非零jointの全4個以下supportを非負・総和1で探索。実行時追加shaderなし | 精度不足、不採用 |
| 候補2：対象3meshの局所8-influence | 理論計算：0H / 浮動小数誤差約0.0000021° | Paw L/R・Torsoだけ2属性＋skinVS。元の8個をそのまま使用。追加VB 288,576 bytes、追加geometry drawなし | **Skin互換の限定技術成立。外観A/BはHOLD** |

Hは承認済みNeutral身長約1。比較は全821整数フレーム＋全半フレーム、計1,641時点。以前の91姿勢のみの0.0175131H / 5.14°と今回の最大値の差は検証密度による。[stock](desktop-stock-audit.json)、[optimized](desktop-optimized-audit.json)、[local8実機](phone-local8-audit.json)、[最適化条件・変更バイト](optimization.json)。候補1は別名[GLB](shushu-v004-optimized4.glb)、SHA256 `f844a02a521428c7d0128bf3fd2b8984d4b42ab212bb58e280347876f96b15dd`。変更はJ0/W0データと追加属性参照の除去に限定し、予期しないBIN変更0。

最小有効方式として候補2を独立Viewerに試作した。[compat.mjs](compat.mjs) は元GLBを読み、3meshの既存属性を完全コピーしてTEXCOORD6/7へ追加joint/weightを載せ、複製materialのskinVSで4＋4を加算する。restやweightsの再設計なし。対象VB全体9,018頂点へ属性を足すため、357頂点だけの追加計算ではない。draw分割は増やさない。WebGL2 / PlayCanvas 2.22.2に限定。WebGPU、他バージョン、未収録の任意姿勢は未検証。

## 実際のGPU出力・Morph・Anchor・Neutral

Xiaomi実GPUのmaterial vertex shaderをtransform feedbackで読み、91 witness＋7半フレーム、98時点×3mesh＝294回をCPU全8-weight参照と比較。GL error 0、欠落capture 0。GPU Morphのローカル位置/法線も採取して同じ入力をCPUへ与えると、**Skinだけの最大差は位置0.000000129571H、法線0.0000185684°**。CPUのfloat Morph計算から比較した全差は0.000130056H / 0.398470°。この残差はGPU Morph表現等も含み、Skin一致と混同しない。GPUの時間計測ではない。

91姿勢で保存GLB channelに対するjoint等の最大行列要素差0.000001028996、7 Anchor 0.000000119210、315 Morphの最大weight差約1.11e-16、欠落node 0。回転は実装のnlerpと照合。局所8候補はchannelを書き換えない。f549からf821へ戻したjoint・全7 Anchor・Morphはf1と差0。34.208332秒clipを8周期ずらした同じ姿勢もjoint差0、Morph差約2.13e-13でloopを確認。[追加実機検証](phone-focused-checks.json)。これはAnchorのbindingと復帰の成立であり、実item接触や全姿勢の自然さの承認ではない。

Front/Side/3Qの原寸640² canvas、座位→復帰の実再生動画は `phone-{stock,full8,local8}-lit-*.png` と `phone-*-seat-return.webm`。full8は元8個をCPUで計算し、対象3meshだけ参照表示する診断専用。full8のCPU処理は性能比較へ混ぜていない。

実機候補とCPU全8参照の125組をpixel比較。Lit 57組の最悪平均RGB絶対差は0.002361/255、当該画像の最大channel差51/255・8超の画素28/409,600。normal/unlit/腕の列もvalidation-summaryへ保存。輪郭等で残差があるためpixel完全一致とは記載しない。小さな相対差でも、両方に共通するA/Bの欠陥を外観PASSにはできない。

## A：前肢の潰れ — Skin互換だけでは修復できない

[5経路の同一姿勢比較](A-five-paths.png)は、編集可能v004 proof Blender、保存GLBのBlender再読込、標準PlayCanvas、CPU全8-weight参照、局所8候補を並べた。f477 Offer、493 Wrist、509/517 SelfContact、533 Hold両側、549座位合成と、f505–541を3フレーム間隔でSide/3Q保存。Blenderは同じカメラ位置・画角だがCyclesとWebGLで照明/色管理が異なるため、両renderer間のpixel一致は主張しない。

**観測：** f533/549の腕付け根〜曲げ部はPlayCanvas標準だけでなく全8参照・局所8でも不自然な凹凸と陰影が残る。編集Blenderと保存GLBのBlender表示では同じ強い陰影の潰れは現れない。f533の有効キーは `Corrective.Hold100.Seat0` と `Corrective.RigidGrip_0_0.0`、f549は `Corrective.Hold100.Seat1` 等。単純な追加Weight欠落だけの不具合ではない。

**幾何と法線を分離：** 元8-weight計算の腕頂点位置は、7姿勢でBlender評価面と最大0.00000143509H、保存GLBのBlender評価面とも最大0.00000148398H。Neutralの法線差は最大約0.0223°（保存再読込約0.0389°）だが、屈曲ではBlender評価法線と最大179.0469°、f533左腕の95パーセンタイル104.4921°になる。[元数値・照合方法](local-defects-numeric.json)、[CPU参照面](surface-oracle.json)、`blender-{author,saved}/normals-*.npz`。Neutral最近傍対応でUV分割頂点も含めて評価した。

[Lit / 照明なしTexture / world normal比較](A-lighting-normal-separation.png)では、色だけにすると強い凹凸陰影が消え、normal表示には乱れが残る。したがって主要な見かけの潰れは、**既存correctiveを含む保存Morph法線＋skin法線変形経路が、Blenderの変形後評価法線を再現していない問題**に局在する。normalの色を照明強度やroughnessで隠してPASSにしない。既存Rig/weight/correctiveで作った評価形状そのものの局所品質もHuman未承認であり、位置一致を体積品質PASSにはしない。どのキーの法線生成/合成を直すかの最終処方は未確定。

Skinだけを修復してもAが残るため、ここで**A HOLD**。原本、corrective、法線、Rigは編集しなかった。次の専用修正範囲はまずPaw L/Rのcorrective Morph法線書き出し・合成とskin法線の扱いを調査し、現行Blender評価面・閉じたNeutral・顔/体型/rest/UVを保持してSide/3Qと全中間で再判定すること。再Rigや全面decimateを解決策として扱わない。

原寸：`blender-author/f*-{side,3q}.png`、`blender-saved/f*-{side,3q}.png`、`phone-*-arm-*-{side,3q}.png`。実再生動画：[候補Side](phone-local8-arm-side.webm) / [候補3Q](phone-local8-arm-3q.webm) / [8参照Side](phone-full8-arm-side.webm) / [標準Side](phone-stock-arm-side.webm)。Blenderの比較動画は `blender-*-arm-*-sampled8fps.mp4`（3フレーム間隔＝8fpsの実レンダー列、補間生成なし。24fps連続レンダーとは記載しない）。

## B：閉口のピンク開口模様と実体の不整合

[閉口→小→中→大の比較](B-closed-to-open.png)。閉口f333、混合小開口f345、中f349、大f357をBlender・保存GLB・実機各方式でFront/Side/3Q保存。f345は純粋なMouthOpen単独試験ではなく、HeadのMouthOpen約0.4＋MouthClose約0.5、Smile等が合成された既存clip中間。f349はOpen/Cavity約0.6、f357は約1。active Shape Keyは各Blenderのinventoryに記録。

**原因：** Head baseColorにピンクの開口/舌に見える模様が焼き込まれ、MouthCloseは形状を閉じてもTextureを切り替えない。Headは追加Weight欠落の3meshに含まれず、8-weight対応でこの印刷模様は消えない。開口時はHeadのMouthOpen / Corrective.MouthCavity、既存MouthInteriorの帯、独立OralBowl/Tongueが合成され、印刷された開口に実開口が重なる。閉口で口内partを診断上だけ非表示にした[Head模様確認](phone-local8-mouth-head-only-333.png)でもピンクは残る。大開口の同条件は[こちら](phone-local8-mouth-head-only-357.png)。表示の一時切替後は復元、資産変更なし。

Headの[埋込み原画像](ShushuStatic_Head-original-basecolor.png)と[MouthInterior原画像](ShushuStatic_MouthInterior-original-basecolor.jpg)を**圧縮バイトそのまま**抽出し、材質bindingとhashをlocal-defects-numericに保存。色管理を通したTexture再出力は原画像の証拠に採用しない。

[過去のtripo-mouth-depth-v006 REVIEW](../tripo-mouth-depth-v006/REVIEW.md)にも、開口/舌が主にHead Textureの描画、独立MouthInteriorは浅い上縁の帯、完全な立体口腔ではないという記録がある。その後の静的Human PASSは歴史として保持するが、今回の閉口/動作欠陥の承認にはならない。**B HOLD。口・Texture・UV・Morphは変更なし。**

次は別の専用修正タスクで、Headの口の局所Textureと実開口輪郭、MouthInterior/OralBowl/Tongue、MouthClose/Openの整合だけを扱う。閉口に開口模様が残らないこと、小〜大開口で「模様に穴」を見せないこと、Side/3Qの口縁/奥行き、Neutral復帰をHuman再確認する。顔全体、瞳、チーク、承認済み体型・座位を無断変更しない。実動画：[候補Side](phone-local8-mouth-side.webm) / [候補3Q](phone-local8-mouth-3q.webm) / [8参照3Q](phone-full8-mouth-3q.webm)。

## Xiaomi 14T Pro 実機Gate

`adb devices -l`で `6TNNJZKBGIFM89FA device product:rothko_jp model:2407FPN8ER` を確認し、marketname Xiaomi 14T Pro。Android16、Chrome155.0.8059.41、60Hz設定、WebGL2 / ARM Mali-G720-Immortalis MC12。`adb reverse tcp:8766 tcp:8766`、Chromeの実端末tabへ接続。ADBによるChrome起動は自動承認レビューにblocked by policyで拒否されたため、Humanが手動で開き「開いた」と回答。その後のロード・再生・capture・計測は実端末で完了した。

既存Viewer由来の照明/材質/orthographic cameraを共用。640×640 physical render pixels、DPR1、CSSのみ端末幅へ縮小、shadowなし、USB充電中、画面前面。原本標準→候補の順に各5分。端末リフレッシュ上限付近のrAFでありGPU性能限界の測定ではない。背景の別アプリ/私用tabは操作しなかった。

| 実測 | 原本＋標準Skin | 原本＋局所8候補 |
|---|---:|---:|
| Cold asset-ready / first frame | 1404.3 / 2567.8 ms | 1750.9 / 3164.9 ms |
| Warm asset-ready / first frame | 488.6 / 922.4 ms | 1067.5 / 1847.3 ms |
| 5分実観測時間 / rAFサンプル | 303.125 s / 18,271 | 303.197 s / 18,271 |
| rAF間隔 P50 / P95 / P99 | 16.6 / 16.7 / 16.7 ms | 16.6 / 16.7 / 16.7 ms |
| 最大 / >25ms jank | 16.8 ms / 0回 | 33.1 ms / 1回 |
| >33.34ms / context loss | 0 / 0 | 0 / 0 |
| app draw calls平均（Morph pass含む） | 20.875 | 20.866 |
| 追加実測60frameのindexed draw / triangles | 16 / 101,057 | 16 / 101,057 |
| 推定GPU allocation（tex+VB+IB+UB） | 76,151,494 bytes | 76,440,070 bytes |
| 終了時JS heap推定 used / total | 約177 / 199 MB | 約177 / 199 MB |
| battery/skin HAL開始→終了 | 31.3→31.7°C | 31.7→31.9°C |
| HAL GPUセンサ開始→終了 | 47.964→41.632°C | 42.205→41.903°C |

ColdはChrome cache clear＋cache disabled、Warmはcache有効でprime後に再ロード。Warmのresource transferSize=0を確認。各1回で分布ではない。asset-readyとfirst frameを分けて保存。診断Viewerは参照照合用GLB再fetch・Morph展開も行うため、これは製品アプリのロード予測ではない。候補初期化は追加コストがあり、Warmも約0.9秒遅いfirst frameを記録した。

GLB本体は101,053 triangles。上記101,057は実GL drawElementsでfixture等も含めた値。5分ログの `app.stats.frame.triangles` は0を返す未対応counterで、描画0と解釈しない。追加60frameは同じアニメーション冒頭を両モードで実測した。GPU allocationはEngine管理の見積もりでdriver/framebuffer/全RAMは含まない。JS heapはChromeの粗い推定。`dumpsys meminfo com.android.chrome` 生ログも保管したが、共有Chromeプロセス分を候補専用RAMとみなさない。

温度は `Current temperatures from HAL` とbattery dumpを使用し、thermalserviceの古いcached値と混同しない。採取したHALはstatus0、再生後半にフレーム劣化/警告/context lossは観測なし。ただしUSB充電・順序・周囲条件が固定されておらず、温度差を候補だけの因果として主張しない。GPU/CPU等のセンサが同値で返る端末実装であり、ダイ温度の独立計測ではない。

**GPU frame time / GPU headroom = UNKNOWN**。端末にEXT_disjoint_timer_query_webgl2がなく、rAF約60fpsからGPU余力を推定しない。5分前面再生・限定タッチの成立は確認したが、A/B外観Gate、製品解像度/影/実item、長時間バッテリー、WebGPU、別アプリへの実バックグラウンド復帰は未検証。Page frozen→activeの復帰は確認したがOS app切替の代わりとはしない。

タッチはChrome CDPの実端末trusted touchイベント。400ms間隔の追加6tapで両モードともPlay/Pauseが6/6反転。pointer event→次rAFの生値はphone-focused-checks、touch-to-photonはUNKNOWN。最初のstock連続tap列にはclick反転しないtapがあったため、その列も消さずperformance.jsonに保持し、追加確認と区別する。

生ログ：[標準のcold/warm・5分・温度・メモリ](phone-stock-performance.json)、[候補](phone-local8-performance.json)、[draw/touch/loop/Neutral追加確認](phone-focused-checks.json)。実機UI画面：[標準](phone-stock-android-screen.png) / [候補](phone-local8-android-screen.png)。原寸canvas PNGは640²の実readback。viewport外CDP screenshotのタイル不整合があった初期撮影は採用せず、現在の全PNGは正しいcanvasから再取得済み。

## 再現

repoでPlayCanvas 2.22.2と既存Playwright、Python/numpy/Pillow、Blender5.2、adb、ffmpegを使用。新規導入・課金なし。

```powershell
git switch codex/shushu-v004-skin-compat-20261015
node scripts/3d/shushu-v004-skin-compat.mjs --serve
# 別terminal。端末のChromeで下記URLを開く。
adb devices -l
adb reverse tcp:8766 tcp:8766
adb forward tcp:9223 localabstract:chrome_devtools_remote
# http://127.0.0.1:8766/docs/production/shushu/evidence/production-rig-v004-skin-compat/runtime.html?mode=local8
node scripts/3d/capture-shushu-v004-skin-compat.mjs fit stock
python -B scripts/3d/optimize-shushu-v004-skin.py
node scripts/3d/capture-shushu-v004-skin-compat.mjs audit stock
node scripts/3d/capture-shushu-v004-skin-compat.mjs audit optimized
node scripts/3d/capture-shushu-v004-skin-compat.mjs audit local8 --mobile
node scripts/3d/capture-shushu-v004-skin-compat.mjs capture local8 --mobile
node scripts/3d/capture-shushu-v004-skin-compat.mjs defects local8 --mobile
# capture/defectsをstockとfull8でも実行。性能測定へCPU full8を使用しない。
node scripts/3d/measure-shushu-v004-phone.mjs stock 300
node scripts/3d/measure-shushu-v004-phone.mjs local8 300
node scripts/3d/diagnose-shushu-v004-phone.mjs
```

Blenderは別プロセスのfactory sceneで `--python scripts/blender/diagnose-shushu-v004-local-defects.py -- --kind author` と `--kind saved`。さらに両方へ `--normals-only` を付けて評価面/法線を抽出。Blend/GLBのsaveはしない。次に `python -B scripts/3d/summarize-shushu-v004-defects.py`、`python -B scripts/3d/board-shushu-v004-skin-compat.py`。後者の動画は実レンダーの8fps列。Pythonはnumpy/Pillowのある環境を指定する。

## Human確認と次Gate

- A：Offer/Wrist/SelfContact/Hold/座位合成と中間のSide/3Qで、腕の丸み・曲げ部分・付け根・左右のつながりを確認。Blenderだけの見え方をruntimeへ拡張しない。
- B：閉口でピンクの開口が残らず、小〜大開口のTextureと実体、口縁/口内/舌が連続して見えることを専用修正後に再確認。
- 既存レビュー済み顔・体型・座位の承認範囲は保持。A/Bの両局所Human再判定までMotion量産はHOLD。
- 局所8候補は互換試作として保持するが、今回の資産置換・製品導入は行わない。全体buildや無関係なテストは実施せず、必要なrenderer/asset/端末検証に限定。

初期4,527入力hashは[protected-inputs.json](protected-inputs.json)、終了照合は[validation-summary.json](validation-summary.json)。Handoffは今回の状態更新として区別し、承認済み資産・初期ユーザー差分・他キャラに今回からの変更を加えていない。
