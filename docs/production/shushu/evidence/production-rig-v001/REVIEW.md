# Shushu Production Rig v001 — capability review

2026-10-15。開始branch `codex/grimo-motion-zero-based-design-20261011`、開始HEAD `6b86aa4e3692310fd6d0a3ac44cee308b47e4602`。**測定範囲内のRig能力を検証した別名候補。正式採用・変形の可愛さはHuman HOLD / PENDING。** v006の静的外観Human PASSを、このRigの承認へ拡張しない。

## 成果とAuthority

- [編集可能Rig](../../../../../assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v006-production-rig-v001.blend)：Neutral、独立プロパティ、元骨階層、IK、Morph/Corrective、7 Anchor、内部操作ガイド。
- [編集可能proof](../../../../../assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v006-production-rig-v001-proof.blend)：50代表時点、589f / 24fps。実証用の短い能力系列であり、Motion全編ではない。
- [保存GLB](../../../../../assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v006-production-rig-v001.glb)：Skin/Morphと実証Animation。Blender制約・driverは評価後の通常チャンネルへBake。
- [保持fixture入りGLB](../../../../../assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v006-production-rig-v001-proof.glb)：半径0.030の診断球。商品や花束の承認モデルではない。
- [操作・再現](README.md)、[S01–S28 / Q01–Q15対応](CAPABILITY-MAP.md)、[最終測定値](verification-summary.json)、[資産hash](delivery-manifest.json)。

入力は `shushu-v006-tripo-autorig-v001.glb`、SHA256 `803aeec97cb455a289e28baa9dd8cd281b97d2b54b92048a2e782228172f8932`。[前Gate](../tripo-autorig-v001/REVIEW.md)の骨階層条件付き採用 / Skin HOLDを補修の出発点とした。ローカルGoal√map、Handoff、Canonical、2026-10-14のv006静的Human PASS、Motion-to-Anatomy DRAFTの必須能力を適用。S01–S26は能力MUST、S27/S28はOPTIONAL。演技、timing、座位Game Neutralを決定していない。

## 能力別Gate

ここでのPASSは記載した範囲のCodex測定・保存検証。Human視覚判断、任意の全組合せ、商品機能のPASSを意味しない。

| 能力 | 結果 | 検証範囲・根拠 |
|---|---|---|
| Neutral identity / UV / Texture | 技術PASS、Human HOLD | 元12パーツのtopology/UVループ/Textureバイト一致。眼球のみ奥行きを約0.006戻す。元12 MaterialのGLB意味定義も保持。真のHuman PASS済みv006と4方向比較 |
| 頭 / 首 / 耳 / 顔の所有 | PASS | HeadYaw/PitchでPaw/胴の誤連動0。耳L/R独立。Neckは接続する頭下端・胴上端collarだけ追従し、Pawへ漏れない |
| 左右腕 / 手、脇 | PASS | Arm/ForeArm/Hand各15°単独FKで胴・頭・対側Paw変位0。短い腕の根元を平滑に保持するcurrent-mesh Corrective。指は新設せず元の互換骨を非weight化 |
| 胴 / 骨盤 / 脚 / 足 | PASS、任意FK支持HOLD | 胴と骨盤のFK、左右脚所有。独立FootLift/Side/Forwardで上胴・頭・反対足底へ漏れない。足はworld pin targetで操作する |
| 立位→荷重移動→座位→休息→復帰 | PASS、物理安定HOLD | Seat 0..1を201段階×shift -1/0/1、603条件。両足底の接地とXY固定、臀支持、局所腹容積補正。実証全589fも床貫通検査。COM/力/摩擦solverは未実施 |
| 低い手提示 / 自己接触 | PASS | 左右Offer / SelfContactを立位・座位で検査。末端Pawの胴侵入なし。接続根元の交差をゼロ侵入と誤記しない |
| 保持 / 反対側接触 / 割込み / 解放 | fixture PASS、実物HOLD | 左保持＋右自己接触・頬圧、座位割込み、保持復帰。球はPaw-owned Anchorへ追従し、解放時world transformを維持。保持から最終復帰まで全frameで両Paw/胴との球面距離を検査、最小clearance約0.000902。両Pawのposeは検証、単一実物の両手gripは未検証 |
| 左右瞬き / 半目 / 片閉 / 視線 | PASS、Human HOLD | 左右独立。両閉眼と頭傾き＋視線のray検査で眼面露出0。全閉最後10%で隠れた眼球を頭内へ収納。再開時は視線復帰 |
| 笑顔 / 喜び / 驚き / ためらい / 軽い不快 | 制御・保存PASS、Human HOLD | 各独立のbounded layer。座位＋喜び、頭傾き＋片閉/半目、非口元ACK等を比較。感情の読みやすさ・可愛さはHuman未判定 |
| 口開閉 / 舌 | PASS、Food様式HOLD | 小口と局所口内、短い独立舌。MouthClose優先。閉口＋開口＋舌の競合でも口内露出0を4方向検査。Food5様式・実食品のbite/残量は未実証 |
| 頬L/R / 胴の局所押圧 | PASS（固定領域） | 頬の左右・前腹を全身scaleから分離。支持・対側保持と併用。任意の連続stroke経路へ押圧領域を移すRig機能はHOLD |
| GLB Skin / Morph / Animation / Anchor | 再import PASS | 同じ最終保存GLBを再importし、50時点の全mesh、589f床、7 Anchorとfixture trackを照合。数値はverification-summary。スマホ・アプリでの再合成は未検証 |
| Neutral復帰 | PASS | 全14meshの評価頂点変位0。正面/3Q/左右側面でNeutral復帰画像を照合 |

## 比較画像

- [01 Neutral：Human PASS v006 / Rig / 保存GLB](01-neutral-identity.png)
- [02 支持・正面](02-support-front.png)、[03 支持・左側面](03-support-left.png)
- [04 顔・口](04-face-capabilities.png)、[05 左右Paw・合成](05-paw-composition.png)
- [06 保持・割込み・復帰・解放](06-held-fixture-release.png)、[07 却下した根元と補修](07-rejected-root-vs-repair.png)
- [08 頭回旋と固定した胴/Paw・4方向](08-head-yaw-four-views.png)

`renders/editable`、`renders/approved-static`、`renders/reimport`、`renders/fixture`に原寸640×640の正面/3Q/左右側面を保存。撮影条件は[render-conditions](render-conditions.json)。花柄瞳、口、耳、輪郭、丸い腹/腿、短い手の根元を優先して観察した。Codexの画像観察をHuman PASSと記録しない。

## 補修方法と却下履歴

元65骨を互換用に維持し、既存耳volume内に根を持つEar.L/Rだけを追加。大頭・短腕・丸胴・短脚の比率変更、全身再造形はしていない。頭/Paw/胴/脚の局所weight所有を修正し、足底はworld pin、上腿の関節位置は実際の腿rootへ合わせた。小weightの下限を1e-4に揃えて正規化し、GLB往復での微小weight省略を編集元へ反映した。

v003の457 Shape Keys / 285f proofは読み取り専用の参照。顔の**評価後変位場**だけを現在の表面へ三角形barycentric補間した。評価vertex数の安定を確認したが、評価triangulationの不変を主張しない。旧shape絶対座標の無条件コピーなし。腹/臀/腕のCorrectiveは現meshの評価姿勢とinverse LBSから局所作成。眼球の奥行き基準は、v006位置を保持したlowpoly参照。lowpoly自体に独立のHuman PASSはないため、比較板にはHuman PASS済み高密度v006を使用した。

初期の座位足貫通、足targetの滑り、上胴への脚weight漏れ、保持Paw根元の扇状fold、全閉時の瞳露出を却下して修正した。`iterations/06`は根元FAIL、`iterations/07`は保存往復の微小weight欠落、`iterations/08`は閉口時の口内露出の却下記録。Blender exportで消えた画像参照は、元12画像とMaterial定義を保った再packingで補修。修復後の最終GLBで検証し、Textureなしexportを成果PASSにしていない。

## 残るHOLDと実用上の範囲

1. HumanによるNeutral保持・半目/全閉・感情・閉口・座位/保持時の可愛さと自然さ。静的v006 PASSは維持するが、本Rigは正式採用HOLD。
2. 支持保証は指定Seat/WeightShiftと実証系列。任意FK、大きな骨盤移動、Foot target回転、同側で複数reach目的を足す操作、範囲外のhead/affect合成は別QA。骨は編集可能でも、その任意姿勢をPASSにしない。
3. 頬左右と前腹の固定押圧領域以外の連続stroke経路・深い多領域同時押圧は未対応。実球の支持力、COM、摩擦、衝突physicsは未計算。
4. 実花束/冠/Wear/Gift/Food、単一物の両手grip、5食べ方、顔・接点遮蔽とitem clearanceはHOLD。Anchorは所有と保存能力の根拠であり、item適合の承認ではない。通常頭上Wearを新設していない。
5. glTFにvisibility trackを載せていないため、fixture proof GLBの球は系列全体に表示される。キャラ単体GLBには球を含めない。releaseはworld transform維持の診断で、贈与/consume/sessionの完了eventではない。
6. GLBには67 joints、14mesh、101,053三角形、最大6 weight influences（JOINTS_1使用）。Blender制御はBake済みだが、PlayCanvasでのlive合成・縦画面・Xiaomi 14T Pro・負荷・影は未検証。PWA実装は対象外。

[保護入力最終照合](preservation-final.json)で原本、歴代候補、旧proof、他キャラ、開始時ユーザー差分、Goal mapを照合。更新は本候補・再現script・Evidenceと重要Handoffのみ。Tripo再実行/外部upload/課金は行っていない。
