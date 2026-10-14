# Shushu Production Rig v002

v001を継承する別名の編集可能Rig候補。全Motion・商品実装・Human最終承認の代行ではない。最終Gateと数値は[REVIEW](REVIEW.md)、S01–S26/Q01–Q15は[CAPABILITY-MAP](CAPABILITY-MAP.md)、原典と判断の分類は[AUTHORITY](AUTHORITY.md)を参照。

## Assets / reproduction

- 編集元: `assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v006-production-rig-v002.blend`
- 編集可能な最小proof: 同名 `-proof.blend`。custom controls / drivers / constraintsを残す。
- 通常Skin/Morph/Animation/7 Anchor出力: 同名 `.glb`。controlsを実行するコードではなく、能力を示すbaked clip。
- 単手fixture: `-proof.glb`。両手rigid itemとFood接点: `-contacts.glb`。診断proxyであり、正式itemではない。
- `scripts/blender/build-shushu-production-rig-v002.py` は不変のv001から制作。`prove-shushu-production-rig-v002.py` はv001の読取専用sampling/UV・weight対応手法を継承。`scripts/3d/report-shushu-production-rig-v002.py` は元Textureの完全保持と比較板を作成。

Blender 5.2.1 LTS / normalized height ≈1 / Z-up、exportはglTF Y-up。CLI例: `blender -b --factory-startup --python-exit-code 1 --python scripts/blender/prove-shushu-production-rig-v002.py -- --proof`。出力後 `report... --textures`、`prove... --roundtrip` / `--contact-roundtrip`、`report... --boards`。v001側のファイルは編集しない。

## Controls and ownership

既存のSeat、WeightShift、頭/首/耳、左右gaze/blink、Smile/Rest/Joy/Surprise/Hesitate/Discomfort、口開閉/舌/頬/腹、左右Hold/SelfContact/Offer/Wrist/Footを維持。floatの通常入力を0へ戻すとNeutral。`GripFit.*`と`GripOffset.*`は計算用driver出力であり、手入力しない。

座位はv001の足world pin・腹臀Correctiveを維持し、8個の中間Seat補正で腹下端〜腿の局所的な折れを緩和する。同位置UV seamを一群として評価し、元mesh/UVを結合・作り直ししない。足裏と上胴の範囲を保護。直接FKやfoot target rotation、片足の支持を任意に外すことは保証範囲外。

同側reachは **Hold > SelfContact > Offer** の残余量でターゲット・肩/IK・対応paw Correctiveを一緒に解決する。Hold中のOfferを実行し終えたとは扱わない。商品側の予約/後送りは別責務。両手Holdには固定span proxy用の小さな遠位接面補正が追加される。Seat×WeightShiftの3×9 gridを補間し、itemのscaleでずれを隠さない。異なるitem寸法・自由なWrist/regraspは再fitが必要。

左右Blinkの半開を緩め、Restの瞼量を0.40へ、Joy最大を明瞭な閉眼笑顔へ調整。閉眼の元の終点と、Neutralの花柄瞳・口・顔・体型は保持。途中の好み・可愛さはHuman PENDING。

連続strokeは`StrokeZone` 0額 / 1頬L / 2頬R / 3腹、`StrokeU/V` −1…1、`StrokePressure` 0…1。各領域の3×3局所morphをbilinear補間し、押圧の中心が経路に従う。頭の眼/瞼/鼻口付近、胴の腿/足を除外。ownerのskinに直接追従し、支持や保持を解除しない。領域を選んだ後に動かす。Zone自体の連続cross-fade、任意の裏面/装飾/眼/口を横断するstrokeは未対応。実接触hitからU/Vへのmappingは商品実装の責務。

## Proxies / boundaries

両手itemは一つのmeshに固定幅の2個の半径0.030 handleと細いshaftを持つ。実itemがrepositoryに無いため、固定spanでの同時保持→座位→割込み→再開→解放の能力を測る。圧力、摩擦、物理COMや任意寸法の把持を証明するものではない。

Foodは外部所有の半径0.006の球状接点probe。SMALL_ONE_BITE、MULTI_BITEの開閉反復/対側ACK、LICKの舌接点、DRINKの頭傾き、LARGE_EATの両手保持と口の独立性を最小witnessで検査する。Head/Tongue/OralBowl/Noseの合成面に対し、口の外側から最初の接点を探し、閉口と舌の後退を含む途中frameも検査する。大きいFood本体・容器・残量・液体・咀嚼の読みやすさ、実itemの保持/口への経路はHOLD。probeを口ownerへ永久parentせず、明示した外部軌跡を記録する。消費/在庫/受領/拒否は実装しない。

Blender proofは非活動proxyを非表示にする。glTFにはこのvisibility trackを移さないため、proxy GLBには診断物が全区間で表示される。正式Rig GLBにはproxyを含めない。解放は直前のworld matrixを保つfixture規約であり、落下物理ではない。

最小proofは81時点/961 frame/24 fps。PlayCanvas 2.22.2の孤立受入はloading/clip/morph/7 Anchor/12 TextureがPASS。完全Skin・runtime外観はHOLDで、標準loaderが追加weightを省く303頂点と、実renderの陰影差をREVIEWへ保存した。受入用`runtime.html`は`node scripts/3d/serve-shushu-production-rig-v002.mjs`でlocalhost:8765から開く。PWAのコードやstateを使用しない。

## Human review

[座位正面](01-seat-front.png)、[座位側面](02-seat-side.png)、[顔の前後比較](03-face-before-after.png)、[五方向の合成](04-five-view-composition.png)、[独立・反転・復帰](05-composition-return.png)、[proxy接点](06-proxy-contact.png)、[Blender/再import GLB](07-blender-glb.png)。全て実assetを固定条件でrenderした未加工画像。crops/resizesと文字入れ以外の画像編集なし。

`iterations/01`は腿の体積を減らしすぎた全体場、`02`は腹下端の突起が残った試行（再renderした一部と前試行の画像を含むため一つの完成状態ではない）、`03`はUV seam裂けと初回proxy接点ずれ、`04`はproxyの軸とFood位置の誤りの棄却記録。いずれも最終候補ではない。専門資料はBlender公式のrelative shape keys / glTF exportだけを局所適用し、身体の全面再造形、追加骨、外部有料生成は行っていない。

単位内の数値PASSは可愛さの承認ではない。Humanのv006静的PASS、v002 RigのHuman判断、商品/スマホ受入を分ける。
