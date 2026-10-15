# Shushu v004 — PlayCanvas compatibility / measured runtime Gate

2026-10-15。**v004のHuman外観PASSは維持。Motion量産・本番runtimeはHOLD。** 原本SHA256 `5fb05e5b7a9cbdb07a64beb5a511d6347c656d85d111ed16eccc533ecfc44cb5` は不変。外観PASSをスマホ・任意Pose・実アイテムの承認に拡張しない。

## 見る証拠

- [Front](comparison-front.png)、[Side](comparison-side.png)、[3Q / 入り・座位・休息・復帰](comparison-3q.png)。実画像を開いて確認済み。
- [原本の実時間再生](stock-seat-return.webm)、[候補の実時間再生](four-seat-return.webm)、[原本動画の1秒間隔抜粋](playback-contact-sheet.png)。動画はcanvas.captureStream(24)で約7.2秒記録。時間補間・描き直しなし。抜粋も開いて確認。
- [原本計測・91姿勢](stock-runtime.json)、[候補計測](four-runtime.json)、[8 Weight CPU参照の条件](full8-runtime.json)、[画像差](image-differences.json)、[最終照合](verification.json)。

左列はHuman承認済みv004 Evidenceからの実画像。BlenderはAgX/Cycles・複数灯・接地影、ViewerはACES2・ambient .65・directional 1・影なし。カメラも完全登録していないため**異Engine間の画素一致や外観PASSを主張しない**。半目＋保持f549の左列は近い座位保持の参照で、同一表情のauthor renderではない。原本・候補・CPU参照の3列は同一Viewer条件。

確認範囲では顔・目・短肢・座位→立位は維持され、Texture消失・大きな破裂は見えない。一方、頬/顎/腹・前肢付け根の陰影が承認画像より硬く、耳や足のTextureの継ぎ目も強く出る。8 Weight参照でも材質の見え方はBlenderと異なる。照明条件とnormal/material整合の切り分けが必要。原本の造形を直して解決しない。Runtime外観のHuman判定は未取得。

## Skin / Morph / Anchor

対象はplaycanvas **2.22.2**、14 mesh、101,053 tri、67 joints、12 embedded images、315 morph targets、821f/24fpsの診断Action。実際にcontainerをロードし、render entity上のanimで再生。Head/LeftForeArmの行列と時間が実フレームで変化し、全14 mesh/12 Texture/7 Anchorを取得。frame時刻は **f/24**（先頭keyは1/24秒、duration 34.208332秒）。

installed `framework/parsers/glb/gltf-accessor.js`のsemantic mapと`glb-parser.js`のfilter、および実vertex formatはJOINTS_0/WEIGHTS_0各4成分のみ。追加属性を取り込まないことを確認。

| Mesh | 追加Weightのある頂点 | 最大欠落Weight合計 |
|---|---:|---:|
| Paw L | 15 / 1,681 | 1.4543% |
| Paw R | 8 / 1,716 | 2.1814% |
| Torso | 334 / 5,621 | 8.8008% |

`skin.js`は合計Weightを同次座標wへも渡す。したがって単純なraw xyz差を画面変位と解釈できない。`maxStock`はshader内の正規化前world xyz差、`maxFour`/`stockRasterError`は同次除算後の上位4正規化位置と全Weight位置の差。後者がSkin欠落の幾何比較。**91姿勢の最大0.0175131 H、座位f79のTorso最大0.0161679 H**。H=Neutral身長1.0。Neutral/復帰f169は約6.7e-8 H以下。半目＋保持f549はPaw L 0.00235357、R 0.00368133、Torso 0.0161679 H。全91姿勢の法線方向差最大5.13771°。単一視点の平均画素差でこの局所差を合格にしない。

CPU参照は追加Weightを持つ3 meshのみ、元GLBのsparseを展開したMorph位置/法線、PlayCanvasが再生した関節world行列、inverse bind、全8枠Weightを加算し、同じPlayCanvas materialで描く。残り11 meshは標準GPU経路。これは**静止した診断参照**であり、8 Weight対応EngineやBlenderとの独立完全一致を証明しない。CPU参照では再生ボタンを無効化。Skin差の計算は全91 witness、画像は9姿勢×3視点×3経路。

MorphはGLB sampler値との最大差1.12e-16。QuaternionはEngineがnormalized linear、glTF参照はslerpであるため、4 witnessでworld matrixに最大0.000402629、Anchorに0.000285566の差がある。[補間切り分け](interpolation-comparison.json)ではEngine方式で91姿勢のmatrix最大1.029e-6、Anchor最大1.192e-7、missing 0。[outlier](transform-outliers.json)。**限定binding PASS / strict glTF補間同等は差あり / 全Skin互換はHOLD**。次Clipの粗いrotation key削減はこの差を拡大し得る。

## 費用 / 実測条件

[内訳](asset-costs.json)はcategory内でbufferViewを重複除外し、sparse indices/valuesを含む。category間は共有する可能性があるため単純合計はファイルサイズに一致しない。

| 項目 | bytes | 方針への意味 |
|---|---:|---|
| GLB全体 | 29,691,796 | 約29.69 MB、28.32 MiB |
| Base属性/index | 3,705,698 | tri削減を最初に行う根拠なし |
| Morph | 18,744,535 | 最大費用。correctiveを一括削除しない |
| Animation | 3,247,876 | 診断Action。製品演技としての同梱不要 |
| Texture | 3,690,306 | 画像圧縮サイズとGPU費用は別 |
| inverse bind | 4,288 | 67関節を減らす効果はここでは小さい |

Windows / Ryzen 5 7430U / RAM約16.5GB / AMD Radeon D3D11 ANGLE / headed Chromium、WebGL2、canvas **640×640、DPR設定1**、shadow/物理/PWAなし、localhost、各300 frame・60 frame warmup。Desktop renderer詳細は[環境記録](transform-investigation.json)。

原本・候補はともに約60fps / rAF平均約16.67ms、P95約17–18ms、平均約18 draw calls（14主要drawにMorph処理等が加わる）。厳密値は各runtime.json。これはvsyncを含むrAF間隔で、GPU処理時間ではない。release engineのupdateTime=0は未計測なので最終記録ではnull。CPU/GPU詳細時間はUNKNOWN。

最終観測は原本load-ready **631.3ms** / 最初の表示 **1,919ms**、候補595.7ms / 1,088.8ms。runtime.jsonの`loadedMs`/`firstFrameMs`を保存。単発localhost観測で、後者には診断用の原本再fetch・sparse展開・参照初期化も含む。実ネットワーク初回表示、production load分解、decode/upload/compile個別時間はUNKNOWN。実行順とOS/browser cacheが違うので原本と候補の差を速度改善と解釈しない。

Engine推定VRAMは約 **76.15 MB / 72.62 MiB**（Texture 72.42MB、VB 3.13MB、IB .61MB等）。12 basecolor画像だけでmip込み70.78MB。GPU driver overhead、browser、CPU decoded画像/Morph、実機総RAMを含まない。JPEG/PNGを小さくしても同解像度の展開GPU費用はほぼ減らない。

## 最大1候補の結果 / 軽量化方針

唯一の別名候補は[4 Weight正規化probe](shushu-v004-runtime-4w-probe.glb)。上位4が最大であることをassertして正規化し、追加属性参照を外す。未使用secondary bufferは残して影響を隔離。変更はW0内6,556 bytesだけ。画像/UV/法線/Morph/Action/骨/rest等の他BIN bytesは一致、JSON差は追加2属性参照だけ。validator error 0 / inherited warning 14。

**不採用。** 29,691,264 bytesで532 bytes（0.0018%）しか減らず、欠落した関節寄与は戻らない。原本との画像差はごく小さく、速度/VRAM改善なし。正規化だけを互換解決としてMotion量産に入れない。候補を本番assetへ差し替えていない。

| 手法 | 今回の判断 / 次に比較する条件 |
|---|---|
| 821f診断Action | Evidence/QAに保持。本番の常時同梱は不要。3.25MBは除去可能なaccessor予算の上限見積りで、削除済み製品assetの実測ではない |
| Clip遅延ロード | rig/rest/skin/Morph名・順序・pathを固定し、standing/seated/表情/占有状態の開始・終端・interrupt契約を備えた個別Clipを必要時load。単純に`animations=[]`にしてもBINは減らない |
| Morph | Face・Seat・保持correctiveを保護。必要能力と依存するcorrectiveの対応表を作ってから、未使用targetの限定除去やlossless疎化を将来比較。315個の一括間引きは禁止 |
| Draco | installed parserに拡張あり。base geometryの転送費候補だがdecoder別配備・decode時間とnormal/UV/skin/shapeの同等確認が必要。今回は未変換、315 Morphの全費用が消えると見積らない |
| Meshopt | installed parserに対応なし。本番候補にしない |
| KTX2/Basis | installed `KHR_texture_basisu`経路＋decoder配備が必要。GPU費が大きいHead/Torsoから将来比較。ETC1Sはサイズ重視、UASTCは顔/目/微妙な色境界の品質重視候補。今回未変換・採用なし |
| Texture resize/atlas | 顔/目の解像・UVを損なうため一括適用しない。draw callも少数なのでatlas先行の根拠なし |
| 4 Weight再配分 / 再bake | 正規化のみは無効。承認形状を保つpose-aware correctiveへの転送、または局所8-influence対応のどちらかを別の限定Gateで判断。今回Engine/PWA/rigは改変しない |

## Clip / 制御 / 立位と座位 / 次Gate

- 同一rest rig・同一Mesh/Morph辞書で立位Seat=0と座位Seat=1を共存。座位をGame Neutralに確定しない。rootや全身scaleで支持/顔を合わせない。
- Seat/Rest/WeightShiftと顔・gaze・耳を分離。保持中はoccupied pawをOffer/SelfContactより優先し、解放後だけ再開。局所correctiveはSeat/shift/両手占有に依存するため、その入力又は対応するbaked trackをClipと一緒に供給。Blender driverはGLBで自動実行されない。
- 7 Anchorのname/path/親/単位を固定。Hold.L/Rは手の追随点であり、mesh表面の追加Weight欠落を治さない。itemのspan、接触法線、把持・handoff・releaseの世界座標連続、Wear重複等を実物で確認。
- Clipには入り/settle/hold/return、立位・座位境界、足/臀の支持相、割込み出口、局所Morphの所有を定義。原本diagnostic timingを製品仕様へ昇格しない。
- **GO:** 最小Viewer・再現手順・限定binding計測・次の互換修復設計。**HOLD:** Motion量産、本番asset採用、8 Weight等価なSkin/normal、runtime外観Human判定、スマホ性能、実item/物理臀支持。先に狭い互換性解決→同じ3視点/遷移の再比較→実機測定→Human判定。

Authority: 最新main `8e4996c63c6d8fbb41954a2aa5cb5d892e45f01b`のAGENTS/Goalと制作branchのGoal・Motion-to-Anatomy・v004実物/Evidence。開始HEAD `ef9a86077eed138ee91644eaee4d9652d73c6493`、承認記録2件を含むremote `56558a1f72ad1df33595b6283d868cd2828ebb80`へ安全にFF。4,422入力hashを照合し、許可されたremote REVIEW/Handoff同期以外は保護。[保護照合](verification.json)。全build・全体テストなし、PWA/approved asset/他キャラ/ユーザー画像差分の編集なし。

## 再現 / スマホ（未実施）

```powershell
node scripts/3d/shushu-v004-runtime-audit.mjs --serve
# 別ターミナル
node scripts/3d/capture-shushu-v004-runtime.mjs
& 'C:/Users/chidj/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' scripts/3d/report-shushu-v004-runtime.py
node scripts/3d/verify-shushu-v004-runtime.mjs
```

2026-10-15の`adb devices -l`は0台。**Xiaomi 14T Pro実測UNKNOWN / Pixel 7a-class UNKNOWN**。USB debuggingを許可した端末で `adb devices -l` → `adb reverse tcp:8766 tcp:8766` → Chromeで `http://127.0.0.1:8766/docs/production/shushu/evidence/production-rig-v004-runtime/runtime.html`。外部公開や追加費用不要。

1. Chrome/OS/機種/RAM/電源/温度/省電力/画面Hz・描画解像度/DPRを記録。原本stockと`?mode=four`を同条件で比較。`full8`は静止参照だけ。
2. キャッシュ無効coldとwarmを区別。load-ready、表示までのwall time、Chrome remote DevTools Network/Performanceでtransfer/decode/compileの観測可能な区間を保存。localhost USB転送を実回線速度と混同しない。
3. frame 1/31/79/103/121/169/237/549/533をFront/Side/3Qで保存。座位・復帰・半目・保持の顔/輪郭/足/前肢/Anchor追随を確認。DevTools consoleで`qa.state()`、`qa.summary()`を取得。
4. まず`Measure 300 frames`。その後5分以上連続playで温度とrAF P50/P95・drop、draw calls、推定VRAM、context lossを再測定。foreground復帰も確認。GPU実時間は対応profilerを使い、rAFと区別。端末の安定性/発熱/知覚に基づくbudgetを決め、未測定欄はUNKNOWNのまま残す。

ディスク空き0で最初のfetch自動maintenanceが失敗したが、ref更新を確認し以後はauto-maintenanceを無効化してFF。既存資産の削除なし。今回のfailed temporary pack強制削除は自動承認レビューに拒否され、実行されていない。成果の保存/検証/commit/pushは別途Gitで照合する。
