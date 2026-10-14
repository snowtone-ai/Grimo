# v002 capability gates — S01–S26 / Q01–Q15

**判定の対象は測定したRig能力。Human=PENDING、正式item/商品実装/スマホ=HOLD。** PASSは下記witness・control domain内のみ。実Motionの完成やDRAFT演技の正式化を意味しない。未測定はPASSに含めない。

原典: [Motion-to-Anatomy DRAFT](../../../motion/GRIMO_MOTION_TO_ANATOMY_TRIPO_CONTRACT_DRAFT.md) のS01–S26、Q01–Q15、H/J4/L1。旧[ v001 map](../production-rig-v001/CAPABILITY-MAP.md)と実assetから再点検。最新Human/古い仮説・他キャラ共通との区別は[AUTHORITY](AUTHORITY.md)。判定の根拠は[REVIEW](REVIEW.md)と保存JSON/実render。

## S capabilities

全行のRig PASSは、可愛さHuman最終承認と、行の「残HOLD」を含まない。

| S | Rig能力 / 測定したwitness | Rig gate | 残HOLD |
|---|---|---|---|
| S01 Living | breath/左右blink/quiet、頭と胴paw分離、Neutral復帰 | PASS | Living演技・可愛さ |
| S02 Comfort | Seat連続・左右荷重・片paw・hold、足pin・腹臀補正 | PASS bounded | 物理COM、任意FK/片足支持、座り方Human |
| S03 Attention | head/gaze/faceと保持/支持分離 | PASS | target選択・気持ちの演技 |
| S04 Groom | self-L/R、反対側hold、同側優先順位 | PASS bounded | 実花束表面/整え動作・頭上reach |
| S05 Rest/Wake | seat-rest/低頭半目/閉眼、割込み復帰保持 | PASS | 眠気/覚醒の時間設計・Human |
| S06 Tap/Poke | 頬左右/腹の局所押圧、頭/腕への漏れ検査 | PASS | 入力ACKのlatency・event実装 |
| S07 Head Pet | 額stroke、頭ownerと冠anchor、低頭閉眼保護 | PASS bounded | 任意冠/装飾の接触域・実物clearance |
| S08 Cheek Pet | 頬L/R stroke、head turnと片hold、同側分離 | PASS bounded | 頬外の任意軌跡・好みの演技 |
| S09 Body Pet | 腹stroke/pressure、Seat/保持を保護 | PASS bounded | 裏面/腿/足の追加domain・実束 |
| S10 Ear/Paw Notice | 左右耳/低Offer/Wrist独立、保持pawの競合解決 | PASS bounded | 任意耳根圧縮場・実触hit mapping |
| S11 Continuous Stroke | 4局所domain×21点、押圧中心移動、support/hold/低頭共存 | PASS bounded | domain越境・任意面の追従 |
| S12 Back-and-forth | 腹経路の往復/反転、pressure解放と復帰 | PASS bounded | 入力速度/飽和/情動state実装 |
| S13 High-five | 低Offer、対側hold、同側Hold優先、safe return | PASS bounded | 両手占有中の予約/WAIT契約 |
| S14 Invitation | 顔・頭・低paw・保持の独立合成 | PASS bounded | target選択/応答/WAIT演技 |
| S15 Delight | joy/Smileとplush/support/保持、明瞭な最大閉眼joy | PASS | 喜び強度の魅力Human |
| S16 Surprise | surprise/gaze/headと胴支持分離 | PASS | cause→choiceの演技 |
| S17 Boundary | hesitate/discomfortと口close/hold/support独立 | PASS | 境界の意味/タイミング・Human |
| S18 Refusal | head/turn、顔、保持と独立回復 | PASS bounded | COM/大withdrawal・実花束退避 |
| S19 Recovery | interrupt-return、action解放と保持/affect、Neutral差分0 | PASS bounded | 任意状態からのevent復帰 |
| S20 Food Notice | gaze/小口/保持準備/close優先、口ACK分離 | PASS bounded | 受領前拒否・在庫不変の実装 |
| S21 Five Foods | 開閉反復、舌、傾き接点、片/両hold＋口の独立proxy | PASS contact-domain | 5style実item本体/残量/飲料/large reach/可読性 |
| S22 Taste | mouth reserveのままblink/頬ACK、食後joy/支持 | PASS bounded | Taste2–5の演技・消費契約 |
| S23 Wear | Crown/earouter/chestの独立owner・7 Anchor保存照合 | PASS anchor | 1Wear交換、実item干渉、headtop仕様 |
| S24 Afterglow | 局所解放・face/支持/保持を別に復帰 | PASS bounded | 全Motionのaffect維持・感情Human |
| S25 Session | 既存姿勢/propでinterrupt→resume、anchor出力復帰 | PASS bounded | foreground/data/所有stateの復元実装 |
| S26 Gift | 固定spanの一つの両手rigid item、単手/対側assist、解放world維持 | PASS fixed proxy | 実Gift/束/物理移管・任意寸法/regrasp |

## Q cross-check

| Q | Rig結果・出典 | Scope / 残HOLD |
|---|---|---|
| Q01 Face | 左右独立、半目/閉眼/口/舌/喜び・低頭/荷重/極端ray、五方向顔比較 | 共通原理。Shushuの可愛さHuman PENDING |
| Q02 Head/Neck | v001 isolation/FK継承、低頭＋左右荷重＋blink | 共通原理。検査したbounded角度外HOLD |
| Q03 Support | 継承603条件＋v002中間243条件＋proof全frame、footlock/復帰 | 共通原理。物理COM/force/friction/任意FK HOLD |
| Q04 Forelimb | 左右独立、低Offer/Self/Hold、残余優先、固定span両保持 | 共通原理。item寸法/握り直しは実物fit |
| Q05 Fleece | N/A | Carol固有。本taskで検証せず |
| Q06 Wings | N/A | Jill固有。本taskで検証せず |
| Q07 Compact tail | N/A | Pino固有。本taskで検証せず |
| Q08 Shushu plush | 腹/腿/脚/足の局所Seat補正、4 stroke域、冠/保持別owner | Shushu固有。実冠/束の見た目・干渉HOLD |
| Q09 Food | 5style接点の最小witnessと口優先、proxy外部所有 | 共通原理。実Food5style・在庫・残量HOLD |
| Q10 Wear | owner Anchor、頭/耳/胸変換とGLB保存 | 共通原理。実Wear/交換/解除HOLD |
| Q11 Session | proofで支持/保持/口/affectの割込みと復帰 | 共通原理。PWA/データ復帰HOLD |
| Q12 Secret | 既存能力の保持のみ | S28はOPTIONAL/候補。Secret全演技は非対象 |
| Q13 Gift/Hold | 単手sphere＋一つの固定span両手proxy・解放保存 | 共通原理。正式item/transfer契約HOLD |
| Q14 Composition | 座位×顔、低頭×blink、保持×対側接触、同側競合、stroke反転、極端/復帰 | 共通原理。全組合せや任意clip合成は未保証 |
| Q15 Spatial/Export | 正面/両3Q/両側面、GLB数値・属性・画像比較、孤立runtime結果はREVIEW参照 | 共通原理。PlayCanvas 2.22.2標準loaderのJOINTS_1/WEIGHTS_1未対応により完全Skin適合HOLD。スマホ/性能/商品runtime HOLD |

v001の67 joints・14mesh・101,053 triangles、元12 Texture/UV/Materialを保持。無根拠な骨追加、他キャラ改修、全Motion、PWA改修、Wiki書込みなし。座位や表情の改善はCodexの比較観察であり、Human確定PASS/FAILを捏造しない。
