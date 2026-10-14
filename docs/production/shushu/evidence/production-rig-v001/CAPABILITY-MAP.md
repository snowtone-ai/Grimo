# Motion-to-Anatomy 対応 — Rig能力と未検証を分離

正本は `docs/production/motion/GRIMO_MOTION_TO_ANATOMY_TRIPO_CONTRACT_DRAFT.md`、この作業の開始HEAD `6b86aa4e3692310fd6d0a3ac44cee308b47e4602`。以下のPASSは小さなRig primitive / 記載した実証poseの技術検証。カードの全Variant、演技、商品state、Human視覚承認をPASSにしない。正本のDRAFTをFINALへ変更しない。S01–S26の基本能力MUST、S27/S28候補OPTIONALを区別する。

| Family | 必須度 | 今回成立したRig能力 | 残るHOLD / 今回の外側 |
|---|---|---|---|
| S01 Living / Warmly at Ease | MUST | blink/gaze/小呼吸/耳/暖かいfaceの独立、Neutral復帰 PASS | 全performanceとHuman温かさ |
| S02 Settle into a Chosen Comfort | MUST | Seat/shift/局所腹臀補正、片保持＋座位割込み PASS | COM/力、実物保持、chosen comfortの演技 |
| S03 Attention / Warm Recognition | MUST | 目→頭を別制御、顔とPaw/胴の分離 PASS | 冠実物、宛先切替のproduct制御 |
| S04 Small Groom / Care for What I Like | MUST | 左右の低い胸腹SelfContact、反対側保持 PASS | 実花束整え、形状/接面適合 |
| S05 Rest / Pleasant Drowsiness / Wake | MUST | Seat＋Rest、半目、低頭、復帰 PASS | Rest＋実花束の全profile、wake演技 |
| S06 Tap / Poke / I Felt That | MUST | 頬L/R・前腹の局所圧、非口元face PASS | 任意頭/胴zone、ACK timing/zone選択 |
| S07 Head Pet / Welcome the Nice Feeling | MUST | 小Head/Neck ACK、半目、head-owned Crown anchor PASS | 冠geometryと重ならない実touch面、全head pet profile |
| S08 Cheek Pet / Enjoy It Here | MUST | 左右頬圧、小頭提示、支持/前肢分離 PASS | 深い多layer圧・任意接点、Human首/頬自然さ |
| S09 Body Pet / Plush Warmth | MUST | 前腹局所圧、胴と保持Pawの所有分離 PASS | 任意胴面・実物保持との全接点合成 |
| S10 Ear-root / Presented-paw Notice | MUST | 耳L/R、小手向き、低Paw提示 PASS | 耳根/pawに沿う任意圧mask、hint演技 |
| S11 Continuous Stroke / Stay with the Good Feeling | MUST | 支持hold＋固定頬/前腹圧＋faceの基礎 PASS | **連続経路へ圧領域を移すRig機能 HOLD**、stroke全profile |
| S12 Back-and-forth Pet / A Clear Little Smile | MUST | 固定局所圧の強度/解放、Smile独立 PASS | **任意経路/反転mask HOLD**、演技/timing |
| S13 High-five / Keep a Little Touch in Mind | MUST | 左右の低いOffer、手方向/支持/回収 PASS | 実相手接点、両保持中の延期と同側競合調停 |
| S14 Invitation / Share My Comfortable Time | MUST | 頭/頬/低Pawの別channel PASS | 提示target可視、冠/花束、全WAIT/ACK |
| S15 Delight / This Feels Really Good | MUST | Joy＋Seat、局所plush/短腕の基礎 PASS | 空Paw選択と全強度演技、Human可愛さ |
| S16 Surprise / Notice, Then Choose What I Like | MUST | Surprise、head/gaze/小口が別制御 PASS | 原因確認/快へのperformance |
| S17 Boundary Hint / Enough for Now | MUST | 軽いDiscomfort、左右瞼、小頭の基礎 PASS | 眠気/保持の全hint合成、Human敵対しない表情 |
| S18 Refusal / Protect My Comfortable Space | MUST | 軽い顔/頭と低保持channelの分離 PASS | 支持内body turn＋実花束保護の全profile、COM |
| S19 Recovery / My Warm Time Continues | MUST | 座位/手/局所の回収、hold-resume、Neutral復帰 PASS | withdrawalの全経路、情動余韻演技 |
| S20 Food Notice / Choose a Taste | MUST | gaze/head/閉口/低保持/軽い不快の基礎 PASS | 実Foodと花束のclearance、拒否未消費state |
| S21 Food Consume / Five Styles | MUST | 小口開閉・短舌・口内・保持面の基礎 PASS | **5styleの実Food接点/残量/大物支持 HOLD**。5style完了と扱わない |
| S22 Food Taste / Savor and Be Delighted | MUST | ためらい/微不快/Smile/Joy/Surprise、Seat合成の基礎 PASS | 味2–5のHuman評価・実Food後処理/演技 |
| S23 Wear / Welcome It without Losing My Shape | MUST | 耳外側/首胸Wear、冠の別owner anchor保存 PASS | 実1Wear交換/解除、表面浮き/顔/腕clearance |
| S24 Afterglow / Close the Action, Keep the Warmth | MUST | 手/表情/視線/局所/支持の独立channel、回収 PASS | 全active poseからの情動保持/部分release演技 |
| S25 Session Entry / My Pleasant Time Is Here | MUST | named channelとAnchor、実証pose/prop world復帰の基礎 PASS | **session/data整合は対象外 HOLD**。consume/transfer完了を姿勢から推定しない |
| S26 Gift / A Little of What I Like, for You | MUST | 両Paw pose、片保持＋反対側接触、fixture解放 PASS | 実Giftの両手grip/片assist/近提示3profile、受理event |
| S27 Rare / A Little Smile Remains | OPTIONAL | 既存Smile/gazeを再利用可能 | 採否とrare performance未決定 |
| S28 Secret Candidate / Bouquet Peek and Welcome | OPTIONAL | 短腕保持・顔の基礎を再利用可能 | 候補花束peek/頬target/極端pose未実証。腕伸長なし |

| Q | 結果と限界 |
|---|---|
| Q01 Face / attention | 左右blink/half/片閉/gaze、5感情、口/舌/頬の独立、閉眼/閉口と競合、保存往復 PASS。Human表情品質 HOLD |
| Q02 Head / neck | 小head yaw/pitch/roll/neck/耳、前肢誤連動解消 PASS。首collarは意図した局所接続追従。深い任意lean/提示・Human首品質 HOLD |
| Q03 Support / weight | 603座位/shift条件、実証589f、固定足底・臀支持 PASS。COM/動的安定・任意FK/Foot向き変更 HOLD |
| Q04 Forelimbs / contact | 左右低Offer/SelfContact/Hold、手方向、反対側分離、根元Corrective PASS。実相手target/全brace/実物両手grip HOLD |
| Q05 Carol fleece | 対象外 N/A。他キャラ不変 |
| Q06 Jill anatomy | 対象外 N/A。他キャラ不変 |
| Q07 Pino anatomy | 対象外 N/A。他キャラ不変 |
| Q08 Shushu anatomy | 大頭/短腕/丸腹/腿/脚足境界、支持、耳、冠/保持の別owner基礎 PASS。Human可愛さ/実花物 HOLD。座位Game Neutral未決定 |
| Q09 Food / mouth | 小口縁/独立短舌/局所口内/閉口競合 PASS。全5styleの物接点・残量・咀嚼/taste合成は HOLD |
| Q10 Wear / motifs | 7 named owner anchorとGLB保存 PASS。実物surface追従/clearance/交換解除 HOLD。通常頭上Wearなし |
| Q11 Session state | pose/face/fixture復帰のRig基礎 PASS。アプリstate/古WAIT/consume/transfer照合は対象外 HOLD |
| Q12 Secret targets | ShushuはOPTIONAL。専用geometry/演技/商品実装は作っていない |
| Q13 Gift / holding | Paw-owned sphere追従→座位割込み→保持復帰→world保持release PASS。実商品3提示profile、両手grip、safe place/受理は HOLD |
| Q14 Composition / continuity | 座位＋喜び、頭傾き＋blink、片保持＋反対接触、割込み/復帰、driver/IK Bake PASS。任意全layer加算、同側reach競合、全performanceのinterrupt policyは HOLD |
| Q15 Spatial / GLB / smartphone | 正面/3Q/左右側面、同条件保存GLB Skin/Morph/Animation/Anchor照合 PASS。背面全変形、PlayCanvas live合成/縦画面/Xiaomi 14T Pro/性能・影は HOLD |

Rig範囲と商品/演技範囲を混ぜない。未検証のMUSTは省略承認ではなくHOLDとして残す。最終採用は[REVIEW](REVIEW.md)と実証画像でHumanが判断する。
