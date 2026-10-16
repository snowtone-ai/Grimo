# Shushu v004 Motion Ready候補 v003

**2026-10-17 / 技術・Runtimeは以下の検証範囲でPASS、最終Human外観GO待ち。原本置換・Motion量産はHOLD。** 初回候補をそのまま採用せず、SelfContact先端が自分の面から離れる欠陥を再検出し、実メッシュへの接触fitまで修正した。W形と鼻下紐除去を維持する別名候補。Human未承認をPASSへ読み替えない。

候補は `shushu-v004-motion-gate-v003.blend` / `-proof.blend` / `.glb`。GLB SHA256 **`11dc599c13d14db8c6ddd68068059738cf4ec6ac81c7ff706530eff65578c892`**、60,850,552 bytes。branch `codex/shushu-v004-motion-ready-v003-20261016`。開始HEAD `a4a90851c1ff85e584671f7c3decd7561e2baea1`、確認済みmain `73617ce2d3c724c86aed82dfc2a09cd220e5d194`。main一括統合なし。

## 判断する画像と連続動作

- [顔：v002 → Blender → 保存GLB → PC → Xiaomi](compare-face.png)、[頭頂の旧突起領域](compare-crown.png)、[前肢before/after](compare-arms.png)。縮小一覧であり、`author/`・`saved/`・`desktop/`・`phone/` の640×640原寸が判断元。
- [初回v003の棄却とSelfContact再修正](compare-selfcontact-iteration.png)、[同姿勢の4経路比較](compare-pipeline.png)、[承認済みv004の体型・座位との比較](compare-approved-body.png)。承認画像と今回では照明・camera枠が異なるためpixel一致を主張しない。
- Xiaomi連続録画：[口 Front](phone/mouth-front.webm) / [口 3Q](phone/mouth-3q.webm)、[左右前肢 3Q](phone/arm-3q.webm) / [反対3Q](phone/arm-3qR.webm)、[真の座位と復帰 Side](phone/seat-return-side.webm)、[顔＋保持・割込み・復帰 3Q](phone/composition-3q.webm) / [反対3Q](phone/composition-3qR.webm)。4抜粋×Front/Side/左右3Qを全件保持。
- Blender連続：[mouth](author-mouth.mp4) / [arm](author-arm.mp4) / [seat-return](author-seat-return.mp4) / [composition](author-composition.mp4)。保存GLB再読込にも同じ4 MP4、PCにも同じ16 WebMがある。全40動画の実デコード更新を[監査](encoded-video-audit.json)した。抜粋は診断用、量産Motionではない。
- [native Android画面の例](phone/seat-face-hold-3qR-android.png)。4 native PNGは、canvas撮影後も同pose時刻を維持しrender counterが進んだことを[135件ledger](phone/capture-ledger.json)で確認。nonce付き再読込・visibility・frame/24・PNG hashでstaleを排除した。

## 技術Gate

| 対象 | 結果と根拠 | 判断の限界 |
|---|---|---|
| FACE-01/02 | W全44 key座標を保持した局所深度補間、外側Cavity凹みを退役。101開口で有限・局所反転0。[保護・開口](preservation-and-aperture.json)、[lit/unlit/wire](phone-face-diagnostic/capture-ledger.json) | 残る広い陰影・小開口の可愛さ・下唇の自然さはHuman確認。Head再構築で法線も再計算されるため、域外位置不変を陰影不変へ拡張しない |
| CROWN-02 | 多層の折り返し面を局所diskへ再構築。局所open/nonmanifold 0。[topology](crown-topology-audit.json)、[移送](crown-retopo-applied.json) | 耳・顔Identityの最終外観はHuman |
| ARM形状・接触 | 264状態/左右プローブで体積proxy 0.982347–1.000001、確認inside 0、root接続sample最少20。[probes](paw-space-probes.json)。全SelfContact先端gap 左0.00328H / 右0.00255H | 体積proxy・距離は柔らかい接触のHuman PASSではない。肩の意図した重なりは遠位侵入と区別 |
| 実三角形 | 51姿勢×左右＝102件、Head/Torsoとの遠位triangle crossing 0。[実面監査](contact-surface-audit.json) | 最近傍法線の負値は隠さない。残った4例はHead AABB外で、ray parityでもinside 0。全制御空間や物理衝突の証明ではない |
| 保存・7 Anchor | 14mesh/51姿勢の保存位置差最大9.39e-7H、7 Anchor全1149frameの行列差最大8.94e-7。[再読込](saved-roundtrip.json) | Anchorは座標契約。実物ごとの接触・解放・支持QAは別 |
| 保持fixture | radius .030H、表面前方 .031Hの既存契約。全保持の最小clearance約0.000324H、span約0.33662H、partial blendのgap誤差最大1.28e-5H | 任意小物の形状や重量に対する保証ではない |
| 座位・Neutral | 対象外Shape/UV/Texture/weight、骨rest/親を保持。Paw BasisとSeat 0/0.5/1の中立位置差 <1e-6H。承認済みrump支持のbody経路を継承し、座位/復帰を再撮影 | crouchを座位へ読み替えていない。新しい物理COM・mass simulationの証明は行わない |

口retopo、38頂点の頭頂修正、CPU法線更新を前提の正解とはしなかった。[原因・不採用案・方式転換](METHOD.md)に記載。原本6ファイルは実LFS object hashまたは未変更pointerと照合した。[保護記録](protected-source-hashes.json)。元checkoutのユーザー変更PNG、未追跡モデル・参照18–27、他キャラには触れていない。

## Runtime Gate

製品用の[loader/controller](../../../../../../assets/grimo/production/shushu/runtime/shushu-v004-loader-v003.mjs)と[deformation module](../../../../../../assets/grimo/production/shushu/runtime/shushu-v004-deformation-v003.mjs)を直接使用。Blender driver、診断frame番号、DOM、診断Viewer専用修復には依存しない。Torso全8-weight GPU skin、2 Pawの現在面NORMAL更新、Purpose/Wrist/Seat補間、実表面に追従するHold anchorを同じ経路で提供する。

- 7姿勢で診断経路と製品loaderのPNG完全一致。[結果](phone/production-loader.json)。2回のload/disposeで元表示が完全復帰、GPU bufferは48→48、二重disposeも安全。[lifecycle](phone/production-loader-lifecycle.json)。
- raw入力26姿勢を[照合](phone-purpose-controls/purpose-controls.json)。うち16姿勢は中立clip上の独立入力から再現し、位置差最大1.23e-6H・法線成分差4.52e-6・7 Anchor差1.03e-6H。baked clipと同じ入力だけの偽陽性を避け、誤ったApplication event名もこのテストで修正した。
- [84 mesh GPU readback](gpu-comparison.json)：GL error 0、raw位置差最大 PC 5.28e-4H / phone 2.10e-4H。GPU Morph値を受け取ったskin-only差は最大8.12e-8H、法線差最大0.04270°。raw誤差はGPU Morph精度を含む。CPU法線stream一致を実GPU面曲率の全一致とは主張しない。
- 旧・新の法線計算を同じ36姿勢で比較し位置・法線差0。[parity](phone-normal-parity/normal-parity.json)。全Head CPU法線更新は行わない。
- GLB validatorはerror 0、既存構造のskinned mesh non-root warning 14、unused texture info 1。[report](glb-validation.json)。任意4-weight Viewerで同品質になる保証はない。

**制御契約の変更：** 前肢は単一Spine2 carrier＋左右438個の通常Shapeを使う。旧arm FK clipをそのまま再生する互換性は提供しない。body/face poseと対応するSeatは呼出側が管理し、連続Purpose・割込みではControllerを使う。baked endpointのcrossfadeだけでは中点の体積補正が抜ける。未検証の任意FK・全制御組合せ・任意小物はHOLD。Grimo全画面への採用や原本置換とは分ける。

## Xiaomi 14T Pro / 300秒比較

同端末2407FPN8ER / Android16 / Chrome155 / Mali-G720 Immortalis MC12、同じUSB・visible/WakeLock・640 canvas・3Q・共通993-frame loop。新候補では診断mesh/deformer/containerを破棄し製品経路1体だけを更新した。[比較データ](performance-comparison.json)、[実モデル14描画の確認](phone/production-perf-probe.json)。

| 指標 | v002 再計測 | v003 製品経路 |
|---|---:|---:|
| 時間 / rAF samples | 300秒 / 18,119 | 300秒 / 18,110 |
| rAF P50 / P95 / P99 | 16.6 / 16.7 / 16.7ms | 16.6 / 16.7 / 16.7ms |
| rAF最大 / 25ms超 | 33.2ms / 1回 | 33.1ms / 1回 |
| 法線CPU P50 / P95 | 5.5 / 6.3ms | 3.9 / 4.3ms |
| Purpose補間CPU P50 / P95 | 対象外 | 0.5 / 0.7ms |
| context loss | 0 | 0 |
| battery開始→終了 | 29.6→30.5℃ | 31.7→32.1℃ |

旧報告のCPU P50 5.2msと、今回同じ記録系で測った5.5msを区別する。法線とPurposeの各P50の和をtotal P50とは扱わない。開始温度が異なる単回・順次測定なので、発熱低減の因果比較はしない。thermalは`Current temperatures from HAL`を使い、過去の`Cached temperatures`を現在値にしない。終了時Current HAL CPU/GPU 42.795℃、Thermal Status 0。新候補の計測中には描画確認PNGと読取probeを1回ずつ採取し、その負荷も含む。

**GPU時間はUNKNOWN。** [計時拡張](phone-gpu-time/gpu-time.json)は非対応。rAFをGPU時間へ読み替えない。GLBは約60.85MBで、USB localhostのload/first-frame値をモバイル回線でのdownload時間へ拡張しない。raw device/performance/progress/environmentを保持した。

## Human Gate / 残課題

[残項目](residual-defects.json)はHuman PENDING。閉/小/中/大と連続口、3Q耳根、両肘の中間～限界、Offer/Wrist/SelfContact/Hold、座位・復帰、顔＋保持・割込みの可愛さ、短肢の柔らかさ、肩と頬下の自然な接触をHumanが最終判定する。Agentの局所画像判定・技術PASSはHuman承認ではない。今回の検証範囲で既知の技術欠陥OPENは残していないが、範囲外をPASSとはしない。

Human GO前は原本置換・Motion量産HOLD。Humanが欠陥を指摘した場合は該当GateをHOLDへ戻し、その箇所から改善する。再現は [REPRODUCE.md](REPRODUCE.md)、納品hashと証拠対応は [delivery-manifest.json](delivery-manifest.json)。
