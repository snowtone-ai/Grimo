# Shushu Production Rig v003 — Human指摘対応候補

2026-10-15 / Codex。開始branch `codex/grimo-motion-zero-based-design-20261011`、開始HEAD `93a8d2480c44e90a9c6a6d693c0fd34f9f4487cb`。v002から別名で制作した編集Rig・proof・2 GLB。**短脚と足の厚み、指定2姿勢の眼は改善。ただし座位の足首稜線・腹下のつながりが残り、総合外観はHOLD。Human合格・正式採用はPENDING。** 技術PASSを外観PASSへ読み替えない。

## 成果と確認入口

- [編集Rig](../../../../../assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v006-production-rig-v003.blend) / [保存GLB](../../../../../assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v006-production-rig-v003.glb)
- [編集可能な81姿勢proof](../../../../../assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v006-production-rig-v003-proof.blend) / [診断fixture付きproof GLB](../../../../../assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v006-production-rig-v003-proof.glb)
- [参照→v002→v003の足・側面](03-reference-feet-left.png)、[同・正面](03-reference-feet-front.png)、[v002/v003の全座位段階・左3Q](02-v002-v003-3q-L.png)
- [指定2姿勢の眼・正面](04-eye-detail-front.png)、[左3Q](04-eye-detail-3q-L.png)、[右3Q](04-eye-detail-3q-R.png)
- [各段階の実際の目視所見](VISUAL-OBSERVATIONS.md)、[権威と保護範囲](AUTHORITY.md)、[再現手順・制御](README.md)、[4成果のhash](delivery-manifest.json)

## 元の足構造と問題初出

同一照明・正投影カメラで **静的v006→lowpoly→Auto Rig→v001→v002** のNeutralを4方向で追跡した。[正面](00-lineage-front.png) / [側面](00-lineage-left.png) / [左3Q](00-lineage-3q-L.png) / [右3Q](00-lineage-3q-R.png)。各段階の入力path/hashは [lineage.json](lineage.json)。原寸を実際に開いて比較し、静的v006由来の短い腿・丸い足の立体感はNeutralで追跡できる。

[表面対応](lineage-comparison.json)では、元v006の下半身表面への片方向最近傍差はlowpoly 0、Auto Rig ≤1.640e-6、v001/v002 ≤2.646e-6（モデル全高約1の座標系）。v001→v002は0。これは保存された表面サンプルの対応であり、体積や双方向Hausdorff距離の証明ではない。見た目でも足を削って薄くした工程はNeutralには見当たらない。

既存Auto Rig診断GLBの `seat-entry` / `seat-attempt` を同じ4カメラで再描画した。原寸 [seat-attempt側面](renders/autorig-probe/seat-attempt-left.png)を開き、足上部が潰れ、足先が裾状へ広がる変形を確認。**保存資料で最初に確認できる動的崩れはAuto Rig変形probe**。静的v006には正解の座位がないため、静的本人の不良とは解釈しない。

v001/v002では、膝IKのpole angle ±π/2が膝を前方でなく股の内側へ曲げていた。[v002骨位置](v002-support-diagnostic.json)。例としてfull seatの左膝は x≈.0466、y≈.0407へ入り、短い腿を股へ巻き込む。足上部の複数骨weightと線形Skinの縮み、既存座位補正の組合せが足首の細い折れと腹下の不連続に寄与していた。

## v003の局所修正

既存Rest骨・骨長は不変。膝IKのpole angleを左 −.0872665、右 −.174533へ調整し、元の短い膝が前方（−Y）へ曲がるようにした。midの膝は x≈±.133、y≈−.0496。[変更記録](knee-plane-repair.json)。人体・動物種の標準角度を採用したという主張ではなく、この本人の短い足と支持から設計した。

元の足の低い体積（Rest z<.095）を既存Foot骨へまとめ、その上をz=.145まで既存weightへ移行。Torsoの976頂点だけweightが変化し、Basis・脚長・足の元形状・UV・Textureは変えていない。上半身や他メッシュのweightは不変。旧SeatVolume/SeatFlow 12補正を、Seat 9段階×荷重3段階の26局所補正へ置換した。Quaternionによる回転体積の保持、境界座標をまとめた局所緩和、広い臀支持場を、通常の線形Skinで再現するMorphとして保存。個々の足頂点を床へ潰す方法ではない。[生成記録](support-authoring.json)。

眼は `seat-lowhead` と `seat-shift-L` 付近の制御合成だけに補正を追加した。主因は眼球全体の大変形というより、Blink/HalfBlink/JoyLids合成で開口が花形の瞳を切り潰すことだった。LowHeadではEyeメッシュ自体の補正量は0で、Headの眼周囲・LidWallを調整。ShiftLでは眼の小さな変形と開口を補正。既存キー座標を改変せず、頭姿勢・口・頬を保持し、全閉眼へ向かうと補正を切る。[眼の生成記録](eye-authoring.json) / [81姿勢の対象外回帰](v002-regression.json)。

## 実際に開いて行った外観評価

本体は立位→左右shift→entry .25→mid .5→.75→full→rest→mid復帰→立位復帰、および指定2姿勢を、正面・左側面・左右3Qで描画。`view-*.png` 全12板（各4方向640px原寸）を実際に開いた。[側面の全遷移](01-transition-left.png) / [正面](01-transition-front.png) / [左3Q](01-transition-3q-L.png) / [右3Q](01-transition-3q-R.png)。各段階の腿・膝・足首・足裏・臀・腹、重量感・可愛さの個別所見は [目視記録表](VISUAL-OBSERVATIONS.md)に保存。

足先の厚み・丸み・短脚は維持し、内股へ折れる膝と細い足首は改善した。full seatでは臀下面が床へ下がり、支持を読みやすくした。一方、**mid〜full/restの側面・両3Qで足首上に斜めの稜線が残り、腹下から腿への境界と股中央の暗部も硬い。自然な体重支持と柔らかな可愛さが完成したとは判定しない。座位外観HOLD。** 復帰では開始時の足・腹・顔へ戻り、補正残りは見えない。

顔拡大は768²、正面・左右3Qを実際に開いた。指定2姿勢では、下がった瞼による尖り・横潰れが緩和され、花形の瞳と眼の丸みが読みやすい。ただし眼を開く方向に変わるため、その表情の魅力・半目/Joyらしさを新たにHuman承認済みとはしない。**眼はCodex改善候補 / Human PENDING**。

[他の顔・正面](05-face-regression-front.png)、[左3Q](05-face-regression-3q-L.png)、[右3Q](05-face-regression-3q-R.png)を開き、Neutral・半目・閉眼・seat-rest・seat-joyにv002からの外観変化を認めなかった。既存閉眼の白い細い帯などを含め、今回の対象外の顔を再設計していない。この比較は既存表情全体の新規外観PASSではない。

保存GLBも4方向×7姿勢を描画し、原寸のmid側面・full左3Qと [保存前後7姿勢比較](06-saved-glb.png)を開いた。編集Rigと同様に足の厚み・眼の改善と残る稜線が見える。保存によって外観HOLDが解消したという扱いはしない。画像の加工は板への配置・ラベル・crop/resizeだけ。[描画条件](render-conditions.json)。

## 保存・重点回帰の結果

| 検証 | 結果と限界 |
|---|---|
| 原本/本人性 | [inheritance](inheritance.json): 全14メッシュのBasis差0、UV/面一致、残した既存キー座標差0。Rest骨一致、制御名保持。Neutral最大差2.581e-8。 |
| 眼以外の顔/手/耳等 | 81姿勢中、指定2姿勢以外の全非Torso評価頂点差0。キーを残すだけでなく評価結果を比較。任意の未検証合成すべてを保証するものではない。 |
| 支持と足体積 | [405条件](support-regression.json): Seat 81段階×荷重5段階。元の低い足体積の最大変位4.956e-7、−.001以下の頂点0。full seatの後方支持域min z=.000333〜.000500。復帰最大差2.581e-8。数値的支持は外観合格ではない。 |
| 既存Rig能力 | [603条件/独立制御・足・FK・接点・閉眼閉口](capability-numeric.json)、[追加243支持条件/4域stroke/優先制御](v002-capability.json)、[両手grip](grip-audit.json)、[閉眼合成のray確認](composed-face-occlusion.json)を再実行。各監査完走。任意FK接地・実item/物理COMの証明なし。 |
| proofと焼出し | 24fps、81 witness / 961フレーム。Skin/Morph/Anchorを通常チャンネルへ焼出し。保存前後の最大頂点差7.110e-7。[焼出し照合](bake-verification.json) / [時系列](proof-timeline.json)。Draftの動作タイミングを採用したものではない。 |
| 保存GLB往復 | [再読込](glb-roundtrip.json): 81×14メッシュ、最大世界頂点差9.965e-7、Rest対応差3.629e-7。全961フレーム床min≥−4.124e-7、−.001以下0。Skin 67 joints、Morph・clipあり。 |
| Anchor/fixture | [7 Anchor×961f](anchor-roundtrip.json)の行列差≤1.610e-6。[診断fixture 961f](fixture-roundtrip.json)≤1.014e-6。fixtureは承認済み実itemではない。v002のcontacts GLBは不変で、v003の実item追従は今回新規検証していない。 |
| Texture/UV/材質 | 元の12画像バイト一致、元UV集合/材質意味一致、外部bufferなし。[GLB属性](glb-attributes.json)。元画像byteを再梱包し、その前後で全数値accessor hash一致。[数値不変](numeric-repack-invariance.json) / [画像材質復元](texture-material-restoration.json)。 |
| glTF構文 | [両GLB検証](schema-validation.json): errors=0。各14件の `NODE_SKINNED_MESH_NON_ROOT` 警告、未使用UVのinfoあり。親transformでskinned meshを動かす意味は制限があり、保存往復とは別にruntimeで適合が必要。 |
| 原本保護 | [保護入力照合](protected-input-verification.json)。開始時3588入力をhash照合し、許可されたHandoff同期以外の変更0。開始時および作業中に現れたユーザーの画像・新規FBX/GLBはstage対象外。 |

## 未達と引継ぎ

最優先の座位外観は改善したが未達。残る足首稜線、腹下・股から腿への硬い折れ、臀へ体重を預ける柔らかさを外観HOLDとして残す。[棄却試行と理由](iterations/README.md)には、腿weightの別案が外観と床侵入を悪化させたことも保存した。根拠なく脚長や元の足形を変えてPASSへ寄せない。

v003のPlayCanvas/スマホ/PWA統合は今回行っていない。v002で確認された追加Skin weight未対応と陰影差のruntime HOLDを解決済みとはしない。v003もJOINTS_1/WEIGHTS_1を含み、意味のあるweightは最大5本（glTF属性枠は最大8）。実Food/Gift/束/Wear、任意stroke面、物理重量/COM、任意未検証合成と全Motion完成はHOLD。

原本、v001/v002、旧geometry-v003 proof、他キャラ、既存ユーザー差分は保存。Tripo/課金/PWA変更なし。Human静的v006 PASSは維持し、v003 Rig/座位/表情/runtimeの承認へ拡張しない。
