# Shushu v004 — A/B Motion Ready Gate / 2026-10-15

**最終判定: HOLD。Motion Ready未到達。原本置換・Motion量産を開始しない。**

鼻下のオレンジの紐は実体とTextureの両方を局所除去した。前肢の乱れた陰影は評価面法線で改善した。新しい口周辺面と頭頂の局所補正も別名候補に保存したが、Xiaomi実表示では口周辺のくぼみ・凹凸と3Qの微小突起が残る。「しわ・僅かなくぼみ・動いたときの微小な飛び出しを全て綺麗に」の完了条件は満たしていない。技術数値をHuman外観PASSに置き換えない。

## Authority / 保護

- 開始HEAD `a35f645858f806edb162bd521f1b85f7871481f4`、作業branch `codex/shushu-v004-motion-ready-gate-20261015`。取得した最新 `origin/main` は `8e4996c63c6d8fbb41954a2aa5cb5d892e45f01b`。一括統合なし。
- [v004の承認範囲](../production-rig-v004/REVIEW.md)、[Aの旧原因・8互換](../production-rig-v004-skin-compat/REVIEW.md)、[mouth B v001](../production-rig-v004-mouth-b/REVIEW.md)を継承。顔全体・Identity・既存座位のHuman PASSを拡張しない。
- 今回のユーザー指示はスマホを含む。旧Handoffの「今回はPCまで／phone対象外」は今回の対象範囲には適用しない。
- 原本 `shushu-v006-production-rig-v004.glb` SHA256 `5fb05e5b7a9cbdb07a64beb5a511d6347c656d85d111ed16eccc533ecfc44cb5`。原本と旧候補は未置換。
- 開始時5,251ファイルのhashは [protected-inputs.json](protected-inputs.json)、終了照合は [protected-inputs-check.json](protected-inputs-check.json)。既存ユーザー変更3PNG、18–27参照、未追跡モデル、他キャラはこのコミットの対象外。Handoffは状態更新として区別する。

## 候補と変更範囲

最終比較対象は `assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v004-motion-gate-v002.blend` / `-proof.blend` / `.glb`。ファイルhashと数値は [measured-summary.json](final-v002/measured-summary.json)。これは診断候補であり、production Motionではない。

1. **鼻下の紐の原因と除去。** Nose meshがz=.6062011まで垂れる実体と、Head Textureの独立したphiltrum着色の2要因だった。先にNoseのz<.632の細い部分を切除・局所cap化し、鼻本体の座標と全既存Shape座標を保持。次に閉/小/中/大の開口構造を確認し、最後に縦線の着色416texelを除去した。Wの着色coverageはこの段階で同一。[原因](mouth-cause-and-removal.json)、[Nose手術](nose-local-surgery.json)、[Texture比較](texture-before-after.png)。
2. **口周辺の面。** 元W境界256点と外側境界362点を固定し、局所31,067triを6,054triのannulusへ作り直した。閉口XZは調和写像、開口XZは制約付き三角分割。口縁側の接線と外側3層の深度を拘束した。鼻・目・頬外側の座標を動かして帳尻を合わせていない。[面の定義](muzzle-retopo-plan.json)、[全ShapeのW/外境界保持](final-v002/authored-preservation.json)。
3. **Textureは面と開口を決めた後。** Headの既存使用UVと重ならない256px領域へ局所口UVを配置し、周囲の既存色とW口縁を整合させた。口内・舌をTextureで描いていない。元の圧縮画像11本は元バイトを維持し、Head画像だけ変更。[局所UV/着色](muzzle-texture-authoring.json)、[元画像復元・数値accessor不変](final-v002/texture-material-restoration.json)。
4. **頭頂。** rayで特定したHeadの38頂点に、局所曲面からのZ補正を同じ量で全Shapeへ適用。最大0.01229994H。正面の尖りは減ったが、3Qの耳付け根付近の微小突起は残る。[特定](crown-ray-inspection.json)、[範囲](crown-local-authoring.json)。耳の形状を変更して隠していない。
5. **前肢A。** 8-weight位置経路を維持し、現在のMorph＋全8ウェイト変形面から角度加重法線を計算、UV分割位置をrest 1e-6で対応させて2つのPawのNORMALだけ更新する。既存のposition、weight、corrective、骨・接触制御は同一。2つのclone materialのnormalVSでworld法線を使用。[実装](surface-normals.mjs)。全面再Rigなし。

v001は上記1＋5の中間候補。rootの `author/ saved/ desktop/ phone/` と旧hashはv001に対応する。**最終v002のEvidenceは `final-v002/` に限定**する。v001のphone性能値をv002の結果として使わない。

## 実表示の比較

- [閉/小/中/大 × authored / saved / PC / phone](final-v002/compare-mouth-front.png)
- [旧mouth B → 紐除去v001 → 面修正v002、Front/Side/3Q](final-v002/compare-mouth-views.png)
- [実機の口周辺拡大](final-v002/compare-face-detail.png)、[正面の頭頂比較](final-v002/compare-crown.png)
- [前肢4姿勢の法線before、Blender、saved、PC、phone](final-v002/compare-forelimb.png)

全PNGは原寸640×640。静止BlenderはCycles 16 samplesでノイズがあり、Runtimeは既存のPlayCanvas照明。明暗差だけで面が直ったと判断しない。**Blenderでは軽く見える凹凸がphoneでは強く出る**こと自体を残欠陥として扱う。

動画:

- [Blender authored 前肢](final-v002/author-arm-3q.mp4)、[saved GLBをBlenderで再読込した前肢](final-v002/saved-arm-3q.mp4)
- [Blender authored 開閉口](final-v002/author-mouth-front.mp4)、[saved GLB 開閉口](final-v002/saved-mouth-front.mp4)
- [PC 前肢3Q](final-v002/desktop/arm-3q.webm)、[phone 前肢3Q](final-v002/phone/arm-3q.webm)
- [PC 開閉口Front](final-v002/desktop/mouth-front.webm)、[phone 開閉口Front](final-v002/phone/mouth-front.webm)
- PC/phone各フォルダにmouth / arm / seat-returnのFront/Side/3Q、計9動画ずつ保存。

Blender動画はEevee 384×384、前肢477–557の81連続frame、口825–897の73連続frameを24fpsで符号化。生成補間なし。PNG列は同じ `author-video/` / `saved-video/` にある。PC/phone動画は実canvasをMediaRecorderで保存し、各診断frameを描いてから次へ進む。host待機を含むため実時間の製品Motion速度やfps benchmarkではない。持続描画性能は別のperformance.jsonで測る。

共通timeline: 24fps、993f。1–821は既存proof、825閉口、837小=.2、849中=.55、861大=1、897閉復帰、909以降座位口、969閉口優先、981舌、993中立復帰。Aは477 offer、493 wrist、509/517 self左右、533 hold、549 seat-hold。15状態×Front/Side/3Qと505–541の3f刻み列をPC/phoneで保存。座位の意図的なblink/表情を修正欠陥と混同しない。

## 検証結果と限界

- authored→saved GLB→Blenderの固定対応比較: 最大位置差9.38773e-7H、993fのanchor最大行列差1.93715e-6。全14meshと比較対象frameを検査。[roundtrip](final-v002/saved-roundtrip.json)。
- GLB validator: error 0、既存と同種のskinned mesh non-root warning 14、unused texture info 1。[詳細](final-v002/glb-validation.json)。警告を消すための骨階層変更は行っていない。
- Wは全Shapeで元境界座標を保持。他13mesh、骨rest/親、口内3mesh、前肢全Shapeを保持。Head外側の元weight、UV、surface topologyは [局所属性監査](final-v002/head-local-attributes.json)。Headの局所面・局所UV・新頂点weight・法線は変更範囲であり、Head全体不変とは主張しない。
- 口の101段階で有限・反転・退化を検査。[aperture-sweep](final-v002/aperture-sweep.json)。これは全身collision検査でも可愛さPASSでもない。
- Aの評価面と旧export法線の差は大きい。frame533のP95は左104.49°→2.59°、右99.92°→3.27°に改善。ただし一部seam/退化近傍では最大差が大きく、最近傍対応にも曖昧さがある。**全法線一致・全ポーズの潰れ解消とは言わない。** [比較値](paw-normal-comparison.json)。
- 実GPU transform feedbackは `final-v002/{desktop,phone}/gpu-*.json`。corrected PawのnormalOracleは評価面NORMAL stream。skinOnlyNormalDegは補正後の比較契約に合わないためnull。positionのraw誤差と、GPU Morph値を受け取ったskin-only誤差を区別する。
- Aの改善はこのviewerのlocal8＋NORMAL companion経路に依存する。GLB単体を任意の4-weight viewerへ渡して同品質になる保証はない。製品Runtimeへの統合承認は未実施。
- 実機はUSB接続Xiaomi 14T Pro / 2407FPN8ER / Android16 / Chrome155 / Mali-G720 Immortalis MC12。ADB reverseと既存Shushu tabを再利用。他アプリ・他tabの操作は行っていない。途中消灯で止まった時点の未確認画像は採用せず、ユーザーのロック解除後に測り直した。
- 5分の実機持続描画、CPU normal処理時間、rAF、context loss、端末開始/終了温度情報は [phone/performance](final-v002/phone/performance.json)、[device-start](final-v002/phone/device-start.json)、[device-end](final-v002/phone/device-end.json)。PCは [desktop/performance](final-v002/desktop/performance.json)。**GPU時間はUNKNOWN。rAFをGPU時間に置換しない。** PCは同時のBlender処理がある環境で、専有性能値ではない。

最終v002実測: phone 300秒/17,667 samples、rAF P50=16.6ms・P95/P99=16.7ms、最大99.7ms、25ms超106回、context loss 0。Paw法線CPU P50=5.2ms・P95=6.3ms・最大35.7ms。PC headlessの30秒/900 samplesはP50=33.3ms・P95=33.4msであり、PCを60fps PASSとはしない。42件のGPU captureはGL error 0、raw position最大2.72705e-4H、GPU Morph値を用いたskin-only位置差最大1.31911e-7H、normal差最大0.031493°。Runtimeの15状態で例外0、morph差最大2.78e-17、anchor差最大1.79e-7。性能・位置精度・外観の判断を混同しない。

## 残欠陥 / 次Gate

[residual-defects.json](final-v002/residual-defects.json)に画像座標と再現frameを固定した。

| 項目 | 現在の判断 | 次に必要なこと |
|---|---|---|
| 鼻下のオレンジ縦線/紐 | 技術的に除去、Human局所PENDING | W形と鼻下の自然な接触をHumanが確認 |
| 口周辺のしわ・微小なくぼみ | **OPEN / HOLD** | PC/phone照明で見える境界深度・接線を形状から再調整。Textureや照明で隠さない |
| 3Q耳付け根付近の微小突起 | **OPEN / HOLD** | 残るsurfaceのobject/triangleを再特定し、承認済み耳形状を保つ局所修正 |
| 前肢A | 陰影改善の候補、全Motion許容は未確定 | 問題姿勢・連続動画で体積/交差/接触をHumanが判定。数値だけでPASSにしない |
| 可愛さ・Identity・座位 | 既存承認範囲は継承、新候補の局所Human PENDING | Frontの可愛さ、Side自然さ、頭頂、W/口内/舌、座位・保持中の外観を比較 |
| Motion量産 | **HOLD** | 上記OPEN解消と局所Human確認後にのみ開始 |

頭部全体を評価面法線へ置換する追加試験は、凹凸解消に結びつかずphone CPU負担も増えたため不採用。`final-v002/phone-face-smoke/` はその**不採用試験**で、最終RuntimeはPaw 2meshのみ補正。rootの `face-*-review/`、`muzzle-retopo*-review/`、`final-local-review/`、`final-surface-review/`、`tangent-review/` は途中案であり、最終候補やHuman承認と混同しない。`phone-isolated-head.png` は描画停止中のstale captureだったため最終Evidenceから除外した。

## 再現

repo rootのPowerShell。既存viewerが起動中なら同じportを再起動しない。

記録環境: Blender 5.2.1、Python 3.13（NumPy/SciPy/triangle/Pillow）、Node 24、PlayCanvas 2.22.2、ADB、FFmpeg。既存依存とviewerを再利用した。

```powershell
node scripts/3d/shushu-v004-motion-gate.mjs --v002 --validate
node scripts/3d/shushu-v004-motion-gate.mjs --v002 --serve
adb devices -l
adb reverse tcp:8768 tcp:8768
adb forward tcp:9223 localabstract:chrome_devtools_remote
# Phone Chromeの既存Shushu tabを開き、画面を点灯・ロック解除する。
node scripts/3d/capture-shushu-v004-motion-gate.mjs --phone --v002 --measure
node scripts/3d/capture-shushu-v004-motion-gate.mjs --v002
blender -b -t 4 --python-exit-code 1 --python scripts/blender/shushu-v004-motion-gate.py -- --v002 --verify
blender -b -t 4 --python-exit-code 1 --python scripts/blender/audit-shushu-v004-motion-gate.py -- --v002
py -3.13 scripts/3d/summarize-shushu-v004-motion-gate.py
```

Viewer: `http://127.0.0.1:8768/docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v002/runtime.html`。`?sourceNormals=1`でPawの法線補正だけを外す。静止画像再描画はmain Blender scriptの `--render --face-only [--saved]`、連続frameは `--video [--saved]`。再生成は既存の別名候補だけを対象にし、原本へ保存しない。
