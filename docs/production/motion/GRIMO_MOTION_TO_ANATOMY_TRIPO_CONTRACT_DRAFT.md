# Grimo — Motion-to-Anatomy / Rig Capability / Tripo Production Contract DRAFT

**Date:** 2026-10-11

**Status:** PHASE_4_COMPLETE / DRAFT / HUMAN_REVIEW_PENDING

**Scope:** 身体能力の設計のみ。Tripo Ready、Rig適合、変形・知覚・実機PASSを意味しない。

**Input HEAD:** `818feba8715d69ac8767482067fa95000c207953`

**Branch:** `codex/grimo-motion-zero-based-design-20261011`

## A. Executive Decision / Production Goal

**Canonicalの可愛さを保った身体で、全130 Family / 408 Variant profilesを成立させるための能力契約。** 生成モデルを「完成時の見た目」だけで採用せず、顔・頭・短肢・支持・接点・固有付属部の構造を先に評価する。Tripoを第一制作手段として評価し、不足する制御・局所構造・演技はBlenderで補う。モデル全体の再生成は、Identityと必須能力を同時に保つ修復が困難な場合に限定する。

優先順は **Identity/可愛さ → 必須Motionの身体構造 → 生命感/触れ合い/表情 → 変形の安定と自然さ → 制作効率 → モバイル性能**。性能のために顔を小さく、腕を長く、尾を細くする判断はしない。成立しない演技を可能と断定せず、実測とHuman判定に戻す。

今回作成するのは本書だけ。画像編集、課金、Credits使用、Tripo/Blender実行、3D/Rig/Animation生成、アプリ変更、Phase 5監査は行わない。Phase 1–3の演技提案はDRAFTのまま。COMPLETEは本書の設計coverageの完成を指す。

## B. Authority / Motion Inputs / Constraints

### B1. 正本と読み取った範囲

| 入力 | 使用範囲 / 優先関係 |
|---|---|
| [Knowledge Index](../../grimo/knowledge/GRIMO_PROJECT_KNOWLEDGE_INDEX.md)、[North Star](../../grimo/knowledge/GRIMO_PRODUCT_NORTH_STAR_AND_MINIMUM_REQUIREMENTS.md)、[Experience Spec](../../grimo/knowledge/GRIMO_CHARACTER_EXPERIENCE_SPEC.md) | 可愛さ、局所因果、主体性、WAIT、静止、余韻、Human知覚、スマホ。実機はXiaomi 14T Pro、Pixel 7a-classはUNVERIFIED_TARGET |
| [Production Architecture](../../grimo/knowledge/GRIMO_CHARACTER_PRODUCTION_ARCHITECTURE.md) §§3–16 | Full-Spatial + View-Weighted Polish、独立制御、連続した身体、方法の自由。別メッシュ/骨数を固定しない |
| [Product Feature](../../grimo/knowledge/product/GRIMO_PRODUCT_FEATURE_SPEC.md) §§5,10–14,21、[Data Model](../../grimo/knowledge/product/GRIMO_DATA_MODEL_SPEC.md) §§5.4,8–9,21–24 | Food5様式/5好き度、1Wear、所有/activation、Giftと消費の事実境界。身体都合で商品仕様を改訂しない |
| [Carol FINAL](../../grimo/knowledge/character-production/carol/CAROL_MVP_MOTION_SPEC.md) §§7–25,27.1 | 46 Family/156 profile、7 Signature、locked content、既承認タイミング/trigger/cooldown/activationを参照継承。8 fleece用途、12 face presets、10 ear statesは能力用途であり骨/Shape Keyの個数ではない |
| [Carol Production State](../carol/CAROL_PRODUCTION_STATE.md)、[visible authority](../../../assets/grimo/source/carol/approved-3d/authority.json) | 現ブランチのNormal候補はHuman review pending。保存済みSkin/Normalを本書で置換・認定しない。旧制作方法を義務化しない |
| [Phase 0 Evidence Pack](GRIMO_MOTION_EVIDENCE_PACK_DRAFT.md) A–D、[Phase 1 Identity](GRIMO_FOUR_CHARACTER_EXPERIENCE_IDENTITY_DRAFT.md) B–E,H、[Phase 2 Direction](GRIMO_FOUR_CHARACTER_BEHAVIOR_PERFORMANCE_DIRECTION_DRAFT.md) B–F,J | 観察/推論/提案を区別。Carolは安心を預ける、Jillは共有、Pinoは結果を見る、Shushuは選んだ快を保つという演技候補を能力へ翻訳 |
| [Phase 3 Architecture](GRIMO_FOUR_CHARACTER_MOTION_ARCHITECTURE_DRAFT.md) E–H全カード、I–K、M–O | 全130行の正本。408 profileの列挙、Variant差、支持/商品/割り込み、Carol原ID alias、Q01–Q13、未決定事項 |
| [Zero-Based Plan](GRIMO_FOUR_CHARACTER_MOTION_ZERO_BASED_PLAN_20261011.md) Phase 4 | 工程の目的。旧Phase 0停止/モデル配分/週量制約は今回の明示Phase 4指示で置換 |
| [Body-only Register](../../grimo/knowledge/character-production/GRIMO_BODY_ONLY_MULTIVIEW_ASSET_REGISTER.md)、[Generation Pose DRAFT](../../grimo/knowledge/character-production/GRIMO_TRIPO_GENERATION_POSE_CONTRACT_DRAFT.md) §§0–8 | 15 selected images registered; Carol Back intentionally omitted by Human decision; image-facing left/right, technical Preflight pending, and Generation/Rest/Neutral separation.古い耳解釈/座位指定/数値試験案を確定値にしない |

直接見たCanonicalは [Carol](../../../assets/grimo/source/carol/carol-Identity-canonical.png)、[Jill](../../../assets/grimo/source/jill/jill-Identity-canonical.png)、[Pino](../../../assets/grimo/source/pino/pino-Identity-canonical.png)、[Shushu](../../../assets/grimo/source/shushu/shushu-Identity-canonical.png)。登録済みBody-only 15枚も直接確認した。これは本書の入力観察であり、Humanの2D選定を取り消す判定や技術Preflight PASSではない。Project Memoryは未取得で、推測した内容をAuthorityへ追加しない。

最新明示Human決定とCanonical、承認済み個体外見/体験/FINAL、補助資料、実装履歴の順で扱う。Carolの古いdelay表現はFINAL §23により **body-owned / macro positional lag = zero**。Jill桃色頭部付属はhorn-like、飛行必須化なし。Pino/Shushu座位Game Neutralは未決定。

### B2. 二軸ラベル

- **MUST:** 正式仕様/必須Motionの成立に必要な能力。未承認の具体演技をFINALへ昇格する意味ではない。
- **SHOULD:** 必須能力をより可愛く自然に実現する局所corrective、選択的な補助表現等。
- **OPTIONAL:** 未承認拡張/Secret候補/将来能力。一般能力と共有する部分はMUSTを維持。
- **UNKNOWN:** 実形状、可動域、Studio適合、到達、性能、Human知覚の未検証事実。MUSTの要求にもUNKNOWNの達成状態が併存する。

工程タグは **G=生成時に必要な形状/接続/面**、**R=Rig制作時に追加可能な骨/weights/morph/補正**、**M=Motion制作時に追加可能なclip/制御/演技/イベント**、**T=要実物検証**。GはTripoに完成した制御を要求しない。分離/局所再構築で原形を保てるG欠陥は修復候補、主要体積や根元を推測し直すG欠陥は再生成候補（I/Q）。全Tは現状UNKNOWN。根拠のない最終骨数/角度/Shape Key数/ポリゴン/FPS/メモリ上限は定めない。

## C. Complete Motion-to-Capability Matrix

### C0. 行の読み方 / 408 profileの扱い

各行はPhase 3同IDカードを正本とする。Carolの原FINAL IDはPhase 3 M1で双方向対応する。以下はCatalogの再生成ではなく、造形と可動性への差分契約。

**全130行にQ01,Q02,Q03,Q14,Q15 + 個体Q05/06/07/08を継承適用。** 表のQ欄はPhase 3見出しの重点Qを保持し、必要な追加Qを含む。頭/顔を使わない姿勢調整でも、現在の顔/注意と支持を壊さない基礎能力を免除しない。各QのG/R/M/Tと検査T01–T15はD。従って各行の部位/独立、支持/変形、G、R/M、リスク/検査、Variant差を併せて読むと9項目を追跡できる。

Vは入力カードの列挙数。各行の基本能力は**そのFamilyの全Vへ適用**。「差なし」は身体能力の追加なしで、初回/慣れ/眠気/満足/無応答等をQ01/Q14の選択・強度・hold・解放で表せることを意味する。演技差を消す指示ではない。特定profileだけが部位/到達/支持/propを追加する場合は最終列に列挙する。左右/gesture/履歴/5好き度との合成をVへ乗算しない。

MUST行でも具体profileの演技はDRAFT。OPTIONAL行のためにCanonicalを変更したり専用形状を必須生成しない。全行の実際の可動/達成状態はUNKNOWN。


### C1. Carol

| Motion ID / Family | V | 要求 | 重点Q | 部位 / 独立制御 | 変形・接触・支持 | G: 造形条件 | R/M: 後付け能力 | 極限リスク / T検査 | Variant限定の追加要求 |
|---|---:|---|---|---|---|---|---|---|---|
| C01 Living Baseline / Intentional Stillness | 4 | MUST | Q01,Q02,Q03 | 眼/瞼・呼吸を耳/蹄から分離 | 蹄接地、局所呼吸 | 顔面容積/下胴/蹄実面 | 独立blink/呼吸/quiet hold | 全身scale・眼潰れ;T01,T03,T05 | 眠気はhalf-lid、開眼/関心はgaze保持。新構造なし |
| C02 Soft Check-in | 3 | MUST | Q01,Q02,Q10 | 視線→頭→近耳を個別 | 胴/蹄固定 | 顔/首/耳根の連続 | gaze/head/耳mask | 眼と頭同時固定・首露出;T01,T02 | 別対象→相手でgaze切替。差なし |
| C03 Want-affection Prelude | 3 | MUST | Q01,Q02,Q05 | 頬/低頭/開口を選択 | 蹄内で前傾停止 | 頬面と顔周辺羊毛の余地 | 提示target/開口/WAIT | 顔とtarget遮蔽;T02,T05,T14 | 羊毛開口profileだけopening制御 |
| C04 Fleece Nestle / Self-comfort | 3 | MUST | Q01,Q02,Q05 | 頭を胴羊毛から独立 | 顔近傍局所圧縮、蹄固定 | 顔受けの余地/奥面 | nestle補正/顔開口 | 首穴・顎羊毛誤所有;T02,T05 | 片側名残は同側corrective |
| C05 Quiet Content Hold | 3 | MUST | Q01,Q02,Q10 | 瞼/口の快と視線解放を分離 | 現在lean/蹄支持保持 | 表情面と首接続 | affect hold/局所ACK | フリーズ・一斉Neutral;T01,T14 | 触れた側だけ頭/局所形状残留 |
| C06 Gentle Curiosity Inspect | 3 | MUST | Q01,Q02,Q03 | 視線/頭/一耳/小胴を分離 | 近い対象時だけ支持内shift | 首/下胴の可動余地 | 注意target/支持補正 | 羊毛に眼埋没・前方転倒;T02,T03 | 近い対象はCOM、驚きは眼/口評価追加 |
| C07 Grounded Hoof Adjustment | 3 | MUST | Q03,Q04,Q05 | 一蹄と残る支持を分離 | 移荷重→置く→局所下羊毛回復 | 四肢根/3分割蹄/足底 | 接地lock/支持phase | 蹄滑り・下羊毛貫通;T03,T04,T05 | 前側/片側/lean戻りの支持集合を切替 |
| C08 Forehead / Head-top Preferred Pet | 5 | MUST | Q01,Q02,Q05 | 額/頭・瞼・近耳 | 低頭、蹄残す | 額軟部/首/開口 | 額圧縮/低頭corrective | 眼圧壊・額羊毛遮蔽;T01,T02,T05 | 心地よい低頭が最深、眠い受容はblink独立 |
| C09 Cheek Preferred Lean-in | 5 | MUST | Q01,Q02,Q03,Q05 | 頬L/R・頭・小胴 | 同側contact、非接触側/蹄保持 | 頬厚/首/胴の接続 | 頬圧縮/接点追従/COM | 首折れ・両側lean加算;T02,T03,T05 | 浅い胴commitのみ胴参加、頬だけ版は顔で完結 |
| C10 Front-fleece Pet / Soft Compression | 4 | MUST | Q01,Q05,Q10 | 実触点/隣接羊毛と顔 | 前面局所圧縮、macro固定 | 立体羊毛面/装備と皮膚の区別 | 局所mask/回復/anchor | shell滑り・Wear浮き;T05,T10 | 面を移る受けはmask経路更新 |
| C11 Ear-root Touch Response | 4 | MUST | Q01,Q02,Q05 | 耳根L/R/同側耳・顔 | 根元の小受け、対耳/蹄固定 | 耳厚/根元接続 | 耳独立/根補正/保護 | 耳穴・耳先過大振り;T02,T05 | 過密前の保護は耳方向/顔hint |
| C12 Tap / Poke Local Notice | 4 | MUST | Q01,Q02,Q05 | zoneごとの局所と顔 | 当たった面のみACK | semantic面/硬軟境界 | zone mask/評価/解放 | rootパルス・偽触点;T05,T14 | 保護版は柔らかいnoticeと異なるface、差なし |
| C13 Continuous Stroke Comfort Build | 4 | MUST | Q01,Q02,Q03,Q05 | 経路面/顔/頭/小胴 | 深まりを止め支持hold | 連続した触面/首余地 | 経路mask/COM/途中release | 経路全身追従・足滑り;T03,T05,T14 | 十分holdは胴commit上限内、満足後は局所のみ |
| C14 Back-and-forth Pet / Melt-with-Saturation | 4 | MUST | Q01,Q02,Q05 | 局所反転/表情/一度の頭寄り | 蹄固定、押圧回復 | 往復可能な実面 | 反転ACK/飽和/hold | 雲周期揺れ・左右押圧累積;T05,T14 | 過密hintのみ境界face。差なし |
| C15 Side / Back Fleece Neutral Acknowledge | 3 | MUST | Q01,Q02,Q05 | 側/露出背面と近耳/頭 | 局所面のみ受け、全身旋回不要 | 側背羊毛の実体/所属 | 露出zone/同側glance | 背面架空hit・カメラ依存shell;T05,T15 | 露出背面版は背面Gが必要 |
| C16 Sensitive Hoof / Rear-lower Response | 3 | MUST | Q01,Q03,Q04 | 触れた蹄/後下部と顔 | 残る蹄へ移荷重/微退避 | 支持面/後下部境界 | sensitive/offer文脈mask | 足浮き・C40誤拒否;T03,T04,T14 | 軽保護/反復hintは支持移行追加 |
| C17 Boundary Hint | 4 | MUST | Q01,Q02 | 同側瞼/口/耳・小頭 | 支持停止、触面に余地 | 表情/耳根/首 | hint face/頭offset | 敵対顔・目縮小;T01,T02 | 敏感面は元zone引継ぎ、休息は眠気共存 |
| C18 Clear Refusal | 3 | MUST | Q01,Q02,Q03,Q04 | 頭と前蹄保護を分離 | 小back/down、支持保存 | 首/前肢根/低い胴 | withdraw/蹄protect/安全遷移 | 後退で足滑り・頭羊毛貫通;T02,T03,T04 | 敏感部を守るprofileだけ前蹄制御 |
| C19 Withdrawal + Mild Residue | 3 | MUST | Q01,Q02,Q03,Q05 | 頭/胴turn/羊毛開口/一耳 | 支持内withdraw、局所opening縮小 | 顔開口/首/側外面 | 部分turn/nestle補正 | 顔消失・羊毛が盾として滑る;T02,T05 | 浅いnestleはopening、部分turnは側外面 |
| C20 Recovery / Re-engagement | 3 | MUST | Q01,Q02,Q03,Q05 | 顔/頭/耳と支持回復 | 圧縮解放→楽な支持 | 回復先の同一身体面 | 強度別recover/現在face保持 | happy snap・押圧残留;T05,T14 | 新touch合流のみ新zone局所ACK |
| C21 Affection Invitation + WAIT | 4 | MUST | Q01,Q02,Q03,Q05 | 頬L/R/額/開口・目/耳 | 自重支持で提示、WAIT | 各提示実面/顔とtarget余地 | target/hold/低頭corrective | target隠れ・指を支柱化;T02,T03,T05 | 4profile=頬L/頬R/低額/opening、各面を検査 |
| C22 Accepted Invitation ACK | 3 | MUST | Q01,Q02,Q05 | 提示面ACKとface payoff | 接点保持、蹄安定 | 実offer面/局所厚 | fast局所/快face/hold | 接触前success・開口閉鎖;T05,T14 | 撫で深まりだけ頭commit追加 |
| C23 Second-turn Offer | 3 | MUST | Q01,Q02,Q03,Q05 | 旧面と新面の提示を分離 | 旧圧縮を解き支持内side移行 | 反対頬/額/opening | 次target/片側補正 | 両頬同時過圧・顔隠れ;T02,T05,T14 | 反対頬/額/openingの3到達を個別 |
| C24 Social Completion / Shared Warmth | 3 | MUST | Q01,Q02,Q03 | 提示姿勢と期待faceを分離 | 荷重順に戻し温かさ保持 | 支持/首/表情面 | offer close/afterglow | 無応答で罰顔・強制Neutral;T03,T14 | 二turnは最終側から戻し、無応答success偽装なし |
| C25 Food Notice / Orient / Presentation Wait | 3 | MUST | Q01,Q02,Q09 | Food視線/頭/口期待/耳 | 届く位置で待機、蹄固定 | 口前余地/首接続 | food target/anticipation | 羊毛/容器が顔を隠す;T01,T09 | 眠気noticeは目覚めと受領準備を分離 |
| C26 Food Receive / Consume Style | 5 | MUST | Q01,Q02,Q03,Q04,Q09 | 口/頭/必要前蹄・非口元顔 | bite接点、残量、brace/外部支え | 小口縁/必要内部/短肢実面 | 5style/保持mask/口とACK分離 | 平面口・大物支持不成立;T04,T09,T14 | 5様式の追加能力はL1の全5行を必須適用 |
| C27 Preference 1 | 3 | MUST | Q01,Q02,Q09 | 口を受領させず顔/頭/耳 | 未消費、蹄固定 | 口閉状態/首可動 | 拒否face/食品撤去settle | 食べたふり・吐出;T01,T09 | 新/既知/再提示は強度差、差なし |
| C28 Preference 2 | 3 | MUST | Q01,Q02,Q09 | 食後口処理と微妙face | 消費済み支持hold | 口元/瞼変形面 | taste2/口処理後評価 | 笑顔morphと咀嚼競合;T01,T09,T14 | 再評価は小口処理追加、口大scale不要 |
| C29 Preference 3 | 3 | MUST | Q01,Q02,Q09 | 口/瞼/視線解放 | 食後普通満足、接地 | Canonical表情面 | taste3/眠気/次target | 無表情停止・眼潰れ;T01,T09 | 眠い充足はhalf-lid、差なし |
| C30 Preference 4 | 4 | MUST | Q01,Q02,Q03,Q05,Q09 | 顔/頭/一耳/小胴羊毛 | 好きの支持hold | 首/胴/局所羊毛 | taste4/小COM/shape回復 | shell lag・足浮き;T03,T05 | 小預けだけ胴、長め満足はhold |
| C31 Preference 5 | 4 | MUST | Q01,Q02,Q03,Q05,Q09 | 顔/頭/胴/選択耳 | 食後peak接地、羊毛macro追従 | 表情/首/胴接続 | taste5/hero補正/afterglow | 笑顔眼崩れ・全身膨張;T01,T03,T05 | 小胴喜びだけ胴参加、深い余韻はhold |
| C32 Warm Content Afterglow | 4 | MUST | Q01,Q02,Q03,Q05,Q09 | body settleと顔/目の余韻 | 現在支持と頬方向保持 | 局所面/首継続性 | 情動保持/shape解放 | 口元/押圧同時reset;T05,T14 | Food満足はconsume状態Q09も継承 |
| C33 Neutral Return / Active-pose Settle | 3 | MUST | Q01,Q02,Q03,Q05,Q10 | 親行為部位/感情を別解放 | 支持を伴うsettle | 首/支持関節/羊毛面 | 現在pose blend/回復 | 全身snap・足滑り;T03,T14 | 支持版だけCOM/蹄、頭版は下半身固定 |
| C34 Session Entry / Return / Background Resume | 4 | MUST | Q01,Q02,Q03,Q11 | 顔/現在支持/商品prop | 最初の可視poseで成立 | 全外面/安定接点 | resume reconciliation/ACK | 古いWAIT・prop二重表示;T11,T14 | 背景/余韻復帰は現在商品状態とaffect保持 |
| C35 Dream-like Long Moving Hold | 3 | MUST | Q01,Q02,Q03,Q05 | 瞼/小呼吸/一耳・頭 | 低い休息、蹄安定 | 首低頭/顔開口 | drowsy hold/局所wake | 眠気で顔消失・低頭首穴;T01,T02,T05 | 深いholdは低頭corrective、wakeはACK重畳 |
| C36 Bounded Dreamy Self-expression Phrase | 3 | MUST | Q01,Q02,Q03,Q05 | 頭/耳/小胴の二拍 | 支持内arc、羊毛位置直追従 | 首/胴/耳根 | 私的phrase/途中redirect | 周期ダンス・足浮き;T03,T05,T14 | 頭と小胴版だけ胴、途中相手へはgaze切替 |
| C37 Moon / Star Motif Recognition | 4 | MUST | Q01,Q02,Q05,Q09,Q10 | 月/星anchorと近接面/顔 | モチーフはowner、蹄固定 | 装飾取付面/羊毛体積 | named anchors/物と身体ACK分離 | モチーフ浮遊・表情遮蔽;T05,T10 | 特別Food後accentは入力を偽装せずQ09状態保持 |
| C38 Deeper Cheek Press | 3 | MUST | Q01,Q02,Q03,Q05 | 同側頬/頭/小胴 | 深いleanを自重で停止 | 頬厚/首/局所羊毛余地 | 深圧縮corrective/COM/回復 | 首折れ・眼押壊・蹄浮き;T02,T03,T05 | 支持を足す受容だけ胴参加、hold深さ固定 |
| C39 Face-in-Fleece Peek | 3 | MUST | Q01,Q02,Q05 | 頭/顔先行peek/耳/開口 | 局所opening、胴蹄macro固定 | 顔を収める空間/内側面 | peek/開口corrective/可視clamp | 顔消失・顎羊毛連れ;T02,T05 | 片側peekだけ非対称、招待版はQ14 target |
| C40 Rare Low-Forehoof Reciprocal Ritual / High-five | 2 | MUST | Q01,Q03,Q04,Q05 | 片前蹄/残る3蹄/顔/耳 | 移荷重→低蹄WAIT→戻す | 短肢根/3分割蹄面/下羊毛隙間 | 蹄独立/支持lock/target ACK | 足浮き・羊毛に蹄隠れ;T03,T04,T05 | 長め温かさはhold差。通常軽交流の能力共有、rare条件はEで保護 |
| C41 Delayed Affection Look-back | 3 | MUST | Q01,Q02 | 視線のみ/必要小頭/一耳 | 胴蹄固定 | 眼と首の独立可動面 | look-back/新入力cancel | 首回し過大・常時催促;T01,T02,T14 | 目だけ版はhead固定、小頭版のみhead |
| C42 Medium Hero Delight | 3 | MUST | Q01,Q02,Q03,Q05 | 嬉しい顔/頭/小胴/選択耳 | 接地sigh、局所/任意broad shape | 顔/首/胴羊毛連続 | hero corrective/shape echo/回復 | global scale・浮遊・眼崩れ;T01,T03,T05 | 小胴sighのみ胴、broad shapeはOPTIONAL実装 |
| C43 Secret | 3 | MUST | Q01,Q02,Q03,Q05,Q12 | 目/頭/頬or額とballを分離 | nudge/軌跡/支持/WAIT | 頬額の実接点/羊毛余地 | prop接触/軌跡/安全exit | ball浮き・顔遮蔽・口把持捏造;T02,T12 | 額/頬接点を別試験、二turnは接点再取得 |
| C44 Secret | 3 | MUST | Q01,Q02,Q05,Q12 | 目/頭/左右前pocketとstar | owner面のreveal、蹄固定 | front局所体積/星の出入口余地 | L/R/front marker/可視target | 星貫通・羊毛全体追従;T05,T12 | 3profileは3pocketを個別検査 |
| C45 Secret | 3 | MUST | Q01,Q02,Q05,Q12 | 頭/顔/開口/同側ACK | 局所隠れ/自重WAIT | 顔収容空間/触れる開口面 | hide/peek/side swap/exit | 無反応消失・shell滑り;T05,T12,T14 | side swapだけ左右corrective間遷移 |
| C46 Gift | 3 | MUST | Q01,Q02,Q03,Q04,Q05,Q13 | 顔/羊毛reveal/頬push/低蹄 | Gift提示/保持→transfer、支持 | reveal余地/頬面/低蹄面 | 3提示接点/解放marker/ACK mask | 保持偽装・羊毛/蹄貫通;T04,T13 | 羊毛reveal/頬push/rare蹄assistを別接点として検査 |

### C2. Jill

| Motion ID / Family | V | 要求 | 重点Q | 部位 / 独立制御 | 変形・接触・支持 | G: 造形条件 | R/M: 後付け能力 | 極限リスク / T検査 | Variant限定の追加要求 |
|---|---:|---|---|---|---|---|---|---|---|
| J01 Living / Private Contentment | 3 | MUST | Q01,Q02,Q03,Q06 | 顔/胸呼吸と翼/葉/尾を分離 | 下半身接地、翼根/尾安定 | 胸/顔/翼葉尾の実根元 | blink/小呼吸/quiet hold | 翼常時往復・葉浮き;T01,T03,T06 | 遊び後も翼recoveryと顔の満足を分離、差なし |
| J02 Attention / Shareable Check | 3 | MUST | Q01,Q02,Q06 | 目→頭/胸、翼を独立停止 | 下半身/翼/尾固定 | 首/胸/顔可動余地 | 対象/相手targetの切替 | 葉が顔を覆う・頭胸一体;T02,T06 | 共有版だけ胸が対話方向へ |
| J03 Private Stretch / Wing Care | 3 | MUST | Q01,Q03,Q04,Q06 | 胸・前肢L/R・翼L/R・葉 | 安定支持上の伸び/軽self-contact | 翼根/膜/腕根と葉の境界 | 胸伸び/片翼fold/局所care | 翼腕葉融合・首反り;T04,T06 | 片翼置直しは片翼制御、身繕いは届く面だけ |
| J04 Grounded Weight Reposition | 2 | MUST | Q03,Q04,Q06 | 一足/下胴と尾根元 | 残る足へ移荷重、尾支柱なし | 独立足/下胴/太尾根 | foot lock/COM/尾連続follow | 足滑り・尾が本体を押上げ;T03,T06 | 私的/共有姿勢から現在の支持へ。差なし |
| J05 Rest / Drowsy Wake | 3 | MUST | Q01,Q02,Q03,Q06 | 瞼/頭/胸/前肢と翼尾 | 低休息支持、眠気ACK | 首低頭/翼休息余地 | drowsy/soft wake/保持mask | 葉首穴・翼顔貫通;T02,T06 | 起床だけ目/注意を開き支持維持 |
| J06 Head Touch / Bright Receipt | 3 | MUST | Q01,Q02,Q06 | 頭軟部/同側face、角固定 | 小受け、脚/翼停止 | 頭軟部と硬いhorn境界 | 頭ACK/顔/胸soften | 角を耳化/圧縮・眼崩れ;T01,T02,T06 | slow版は受けhold、tap/pokeは短notice |
| J07 Cheek Touch / Turn to Share | 4 | MUST | Q01,Q02,Q03,Q06 | 頬L/R/顔と胸を分離 | 頬接点、胸対話方向、脚保持 | 頬厚/首葉/胸余地 | 頬corrective/胸向き/side解放 | 葉が頬/眼を隠す;T02,T03,T06 | 顔胸共有版だけ胸、満足小holdは局所 |
| J08 Chest / Body Touch | 3 | MUST | Q01,Q03,Q04,Q06 | 胸実面/顔/低前肢 | 局所受け、支持上hold | 胸軟部/腹plates/腕根 | 胸ACK/前肢解放/face | plates伸び・葉waveで代行;T03,T04,T06 | body notice/穏やかpet/小受容、差なし |
| J09 Appendage-root Notice / Protection | 3 | MUST | Q01,Q03,Q06 | 片翼根/尾根と反対付属 | 根元ACK→楽なfold/小尾調整 | 根元体積/翼膜境界/尾連続 | root-local ACK/片翼閉/保護 | 根潰れ・翼膜を皮膚扱い;T06 | 翼根notice/尾根noticeは別owner、hintは閉方向 |
| J10 Continuous Stroke / Shared Ease | 3 | MUST | Q01,Q02,Q03,Q06 | 経路局所/顔/頭/胸 | 支持hold、翼を休める | 実触面/首/胸/翼余地 | 経路mask/胸小開き/解放 | 指を翼周期に転写;T06,T14 | 快育ちのみ胸参加増、満足版は局所 |
| J11 Back-and-forth Pet / Playful Settle | 3 | MUST | Q01,Q02,Q06 | 反転局所/faceと胸 | 翼前肢止め、支持hold | 頬/頭と胸軟部 | 反転ACK/快/過密hint | 羽ばたき同期・角変形;T06,T14 | 速い過密の区切りのみhint face |
| J12 High-five / One Reply Is Plenty | 4 | MUST | Q01,Q03,Q04,Q06 | 片前肢・胸・顔・選択翼 | 脚支持で低paw WAIT→戻し | 腕根/提示面/胸翼clearance | paw独立/接地/target/payoff | 足浮き・翼前肢face貫通;T03,T04,T06 | 無応答版は荷重順で閉じる、翼参加は選択的 |
| J13 Invitation / Open a Shared Moment | 3 | MUST | Q01,Q02,Q03,Q04,Q06 | 胸/前肢offerと頬頭/翼 | 顔とtargetを見せ支持WAIT | 首/腕根/胸/頬面 | 複数提示面/WAIT/ACK | stretch holdに見える・翼遮蔽;T02,T04,T06 | 遊び版は低paw空間、頬/頭版はface接触面 |
| J14 Delight / Joy Opens Outward | 3 | MUST | Q01,Q03,Q04,Q06 | 顔→胸→低前肢→翼葉 | 支持上peak、尾根追従 | 胸腕翼の別根/葉体積 | 強度別胸/翼mask/尾follow | 胸拡大・翼根潰れ・浮遊;T03,T06 | 翼添う/大喜び版のみ翼/葉参加増 |
| J15 Surprise / Curious Reassessment | 3 | MUST | Q01,Q02,Q03,Q06 | 意外face/頭/胸と翼 | 原因確認で支持停止 | 顔と葉首の可動余地 | surprise/target/胸hold | 恐怖の翼大展開・眼縮小;T01,T02,T06 | 共有版だけ胸を開き、既知版は小評価 |
| J16 Boundary Hint / Make Some Room | 2 | MUST | Q01,Q03,Q04,Q06 | 顔/胸閉じ/必要前肢翼 | 支持固定、余地回復 | 胸腕翼の内側余地 | hint/局所owner保護 | 畳む翼が腕/顔を貫通;T04,T06 | 割込hintは現在翼/保持状態継承 |
| J17 Refusal / Grounded Withdrawal | 3 | MUST | Q01,Q03,Q04,Q06 | 頭/前肢/翼・小胴turn | 支持内withdraw、保持保存 | 首/内側翼/腕/側外面 | withdraw/保護mask/COM | 翼根潰れ・尾払い;T02,T03,T06 | 胸面/付属根保護はそれぞれownerを閉じる |
| J18 Recovery / Ready to Enjoy Again | 2 | MUST | Q01,Q03,Q06 | 胸/翼解放と顔暖かさ | 支持/尾根安定 | 戻り経路の胸翼余地 | recover/情動保持 | 急happy flip・翼snap;T06,T14 | withdrawalからは現在turnを解く |
| J19 Food Notice / Pre-consume Choice | 3 | MUST | Q01,Q02,Q09 | Food目/頭/口と胸前肢 | 受領前支持停止、拒否未消費 | 口前/前肢/翼余地 | notice/未受領拒否mask | 拒否を食後表情化・顔Food隠れ;T09 | 好き度1版は口を受領させず前肢閉じる |
| J20 Food Consume / Five Styles | 5 | MUST | Q01,Q02,Q03,Q04,Q09 | 口/頭/保持前肢と翼/顔 | Food接点/brace、胸安定 | 口縁/内部/短腕/翼root余地 | 5style/口保持/非口元ACK | 翼食物把持捏造・平面口;T04,T06,T09 | 5様式の差はL1全行、翼は食後まで休む |
| J21 Food Taste / Shared Happiness | 4 | MUST | Q01,Q03,Q06,Q09 | taste face/胸/選択翼葉 | 食後支持peak/尾follow | 口face/胸翼接続 | taste2–5/胸翼mask | 毎味翼peak・咀嚼競合;T01,T06,T09 | 2胸収まり/3小満足/4胸共有/5翼参加を別評価 |
| J22 Wear Recognition / Equip / Enjoy | 3 | MUST | Q01,Q02,Q06,Q10 | 目/頭胸とWear anchor | 1Wear、根元所属維持 | 安全頭中央/首胸面 | owner anchor/交換/解除 | 角葉翼にWear衝突;T06,T10 | 初/交換/解除はattach状態のみ差 |
| J23 Afterglow / Private or Shared Settle | 3 | MUST | Q01,Q03,Q06 | 胸/前肢/翼葉とface余韻 | 下半身/尾根固定 | 回復経路の付属接続 | settle/affect hold/視線release | 翼葉同時snap・強制Neutral;T06,T14 | 共有/私的/非peakは情動と宛先差 |
| J24 Session Entry / Current Joy | 3 | MUST | Q01,Q03,Q06,Q11 | 現在顔/胸/翼/prop | 初可視poseで支持成立 | 全外面/安定接点 | entry/resume状態整合 | 古WAIT・翼pop・商品完了偽装;T11,T14 | 背景復帰のみ無効接触解放/商品照合 |
| J25 Gift / Bring You Into My Joy | 3 | MUST | Q01,Q03,Q04,Q06,Q13 | 顔/保持前肢/胸と翼 | 低Gift提示、翼停止、脚支持 | 短腕/胸前/接点余地 | 保持target/transfer/非保持ACK | Gift胸翼貫通・足浮き;T04,T06,T13 | 胸前版はface遮蔽、片assist版は対側支持/保持 |
| J26 Rare / The Smile I Held Back | 2 | OPTIONAL | Q01,Q03,Q06 | face/胸と片翼小参加 | 下半身安定、尾所属 | 既存胸翼構造を共用 | rare phrase/翼開きかけ | 痙攣・新offerと誤読;T06,T14 | 翼版だけ小翼追加、専用生成形状不要 |
| J27 Secret Candidate / Wing-shelter Peek | 2 | OPTIONAL | Q01,Q03,Q04,Q06,Q12 | 片翼/顔・反対翼/腕を分離 | 支持WAIT、部分顔/target露出 | 通常翼体積/根元余地のみ必須 | 候補翼横peek/side切替 | 翼顔/腕貫通・全顔消失;T06,T12 | 側替え版だけ左右経路。候補不成立で翼を拡大しない |

### C3. Pino

| Motion ID / Family | V | 要求 | 重点Q | 部位 / 独立制御 | 変形・接触・支持 | G: 造形条件 | R/M: 後付け能力 | 極限リスク / T検査 | Variant限定の追加要求 |
|---|---:|---|---|---|---|---|---|---|---|
| P01 Living / Interested or Satisfied Quiet | 3 | MUST | Q01,Q02,Q03,Q07 | 顔/目/前肢配置と呼吸/尾 | 足/下半身支持、尾停止 | 丸い胴/短肢/両眼 | quiet hold/blink/注意release | balloon呼吸・尾常振り;T01,T03,T07 | 対象/納得/次思考は注意状態差 |
| P02 Attention / Focus and Release | 3 | MUST | Q01,Q02,Q07 | 目/頭と停止前肢 | 支持/尾静止、見るhold | 顔首/手元可視余地 | gaze/self-target/頭小turn | 腹が接点隠す・空追跡;T02,T07 | 身体面版のみ実self-target |
| P03 Paw Set / Press / Look | 3 | MUST | Q01,Q03,Q04,Q07 | 片前肢/接点/視線と対側支持 | 置く→軽荷重→解放/観察 | 丸paw実面/腕腹境界/短肢到達余地 | paw局所圧縮/独立pose/結果gaze | paw腹融合・到達不可・隠れ変形;T03,T04,T07 | 向き変更版は接触面方向、既知版は短縮。第一候補の代替はG |
| P04 Thick-tail Inspection / A Small Turn | 2 | OPTIONAL | Q01,Q03,Q07 | 胴小turn/尾連続/頭目 | 足支持、尾は従属重量 | 単一太尾の自由区間/根元 | tail follow/露出target | 尾を前巻き・把持・支柱化;T03,T07 | 両profileとも実露出時のみ、専用尾延長なし |
| P05 Grounded Posture Rebalance | 2 | MUST | Q03,Q04,Q07 | 足/下胴と前肢/尾 | 移荷重/置直し→尾収まり | 短脚/腹/太尾根の境界 | foot lock/COM/尾連続settle | 尾胴融合・転がるbody;T03,T07 | 試行戻りは現在pawを安全回収 |
| P06 Rest / Let the Experiment End / Wake | 3 | MUST | Q01,Q02,Q03,Q07 | 目/頭/前肢休むと尾/足 | 低休息支持、局所wake | 低頭首/腹脚余地 | drowsy/soft wake/ACK mask | 大頭で前転・尾浮遊;T02,T03,T07 | 起床でも未完関心は選択、差なし |
| P07 Tap / Poke / What Changed Here | 4 | MUST | Q01,Q02,Q07 | 局所面/同側faceと手元 | 下半身/尾固定 | 頭頬胴/根元実面 | zone ACK/評価/短release | 全身bounce・左右消失;T07,T14 | 保護版だけboundary face、差なし |
| P08 Head Pet / Choose the Nice Feeling | 3 | MUST | Q01,Q02,Q04,Q07 | 頭/目faceと前肢解放 | 支持保持、集中を休める | 首/眼/内寄り腕余地 | 頭pet/顔快/手元保留 | 頭ACKが保持pawを崩す;T01,T02,T14 | 集中合間版は前肢作業を安全保留 |
| P09 Cheek Pet / A Little More This Way | 3 | MUST | Q01,Q02,Q03,Q04,Q07 | 頬L/R/頭/前肢休む | 小contact seeking、足尾安定 | 頬厚/首/腕腹境界 | 頬補正/小lean/旧側解放 | 頬眼壊れ・顔腹埋没;T02,T03,T07 | 小さく寄る版だけhead/COM増 |
| P10 Body Pet / Rounded Ease | 3 | MUST | Q01,Q03,Q04,Q07 | 実胴面/顔と前肢 | 局所受け、支持上丸さ維持 | 胴軟部/腹腕区別 | body局所mask/腕休み | 腹ゴム・中空bounce;T03,T07 | 試行後は前肢回収を共存 |
| P11 Ear / Tail-root / Forepaw Context Notice | 3 | MUST | Q01,Q02,Q04,Q07 | 耳根/尾根/前pawと対側 | 使用面を守り支持維持 | 各根元/短paw実体 | owner別ACK/offer文脈 | 尾drag・self-contactをuser化;T04,T07,T14 | 根元版は耳or尾、試行版はpaw、保護版は安全戻し |
| P12 Continuous Stroke / Discover Then Enjoy | 3 | MUST | Q01,Q02,Q03,Q04,Q07 | 経路局所/頭顔/腕構え | 支持hold/尾停止 | 連続実触面/首余地 | 経路ACK/快/作業解放 | 毎stroke再試行・尾周期;T07,T14 | 眠い満足はhalf-lid、差なし |
| P13 Back-and-forth Pet / Notice the Change, Settle | 3 | MUST | Q01,Q02,Q04,Q07 | 反転局所/顔・頭と腕尾 | 一度開く→支持hold | 顔軟部/首 | 反転ACK/快/hint | 腕尾交互パタパタ;T07,T14 | 十分区切りはhint faceのみ |
| P14 High-five / Touch, Look, Smile | 4 | MUST | Q01,Q03,Q04,Q07 | 片paw/目/顔と対支持 | 低target WAIT、触面観察→戻す | 短腕/丸paw面/腹clearance | paw独立/target/gaze/支持lock | 足浮き・paw腹埋没;T03,T04,T07 | 無応答版は観察successなし、他は強度/確認差 |
| P15 Invitation / Open an Unfinished Discovery or Pet | 3 | MUST | Q01,Q02,Q04,Q07 | paw空間or頬頭とface | 支持WAIT、元手元を安全保留 | 短腕/頭頬面/首 | 複数target/作業pause/ACK | 手元を顔が隠す・腹貫通;T02,T04,T07 | 前肢試行版だけ手元target、頬/頭版は顔面 |
| P16 Delight / I Found Something Nice | 3 | MUST | Q01,Q03,Q04,Q07 | face/内寄り前肢/胴と尾 | 支持上の小意欲/尾settle | 腕腹/丸胴/単一尾根 | 強度別喜び/尾follow | jump・空気balloon;T03,T07 | 大納得版のみ胴尾の参加増 |
| P17 Surprise / Try a Different Way | 3 | MUST | Q01,Q02,Q04,Q07 | 操作側paw/頭目と非操作側 | 試行停止→一度変更、足尾支持 | 短paw可視面/首 | 結果評価/別試行/安全停止 | 繰返し試行・支持/比較面動揺;T04,T07 | 試行結果版は一度別操作、外部版はtarget確認 |
| P18 Boundary Hint / Keep My Working Space | 2 | MUST | Q01,Q03,Q04,Q07 | 顔/使用paw/頭と尾下胴 | 作業域へ収める、支持停止 | 腕腹/首余地 | hint/作業mask | 払う手・保持破壊;T04,T07,T14 | 集中割込版は手元安全保留 |
| P19 Refusal / Reclaim a Little Space | 3 | MUST | Q01,Q03,Q04,Q07 | 顔頭/前肢/小turn | 支持/prop保持でwithdraw | 首/腕腹/側外面 | withdraw/保持mask/COM | 尾払い・物落ち・足滑り;T03,T07 | 前肢作業保護版だけ手元保持 |
| P20 Recovery / Curiosity Returns | 2 | MUST | Q01,Q02,Q03,Q04,Q07 | 顔/頭/前肢と支持 | 保護を解き自力回復 | 戻り経路の顔腕余地 | recover/条件有効性/現在face | 壊れた接点の復元偽装;T07,T14 | 元関心版は実target残存、touch版はACK合流 |
| P21 Food Notice / Examine, Accept or Refuse | 3 | MUST | Q01,Q02,Q04,Q09 | 目頭/必要paw/口を分離 | 受領前停止、拒否未消費 | 口前/短腕保持余地 | notice/保持準備/拒否 | touchしただけでconsume・顔物遮蔽;T04,T09 | 好き度1のみ受領口なし/保持解放 |
| P22 Food Consume / Five Styles | 5 | MUST | Q01,Q02,Q03,Q04,Q09 | 口/頭/内寄り前肢・非口元顔 | 保持/残量/持直し、足尾支持 | 小口縁内部/短paw/腕腹境界 | 5style/保持mask/safe node | 尾把持・腹物貫通・平面口;T04,T07,T09 | L1全5様式、飲む外部提示候補を分離 |
| P23 Food Taste / Evaluate and Be Pleased | 4 | MUST | Q01,Q03,Q04,Q07,Q09 | taste顔/前肢/胴と尾 | 食後支持peak→尾settle | 口顔/腕腹/尾根 | taste2–5/強度mask | 評価を前肢作業だけにする;T01,T07,T09 | 2再評価/3paw休/4小快/5胴尾参加 |
| P24 Wear / Check the New Feeling | 3 | MUST | Q01,Q02,Q04,Q07,Q10 | 視線/届くpawとWear | 1Wear owner維持、足尾支持 | 頭上/首胸面/試行clearance | anchor/交換/解除/短確認 | Wear試行paw貫通・頭上掴み;T04,T10 | 頭上はpaw確認不要、首胸のみ届く場合確認 |
| P25 Afterglow / Keep the Result, Let Go | 3 | MUST | Q01,Q03,Q04,Q07 | 操作paw/頭胴/尾と情動 | 現在支持へ、尾settle | 腕腹/首/尾連続 | 行為解放/affect hold | 一斉Neutral・結果を見せ続け;T07,T14 | 非peak版は残るaffectを消さない |
| P26 Session Entry / Already Doing My Thing | 3 | MUST | Q01,Q03,Q04,Q07,Q11 | 現在目頭/手元と支持/prop | 初可視poseから成立 | 全外面/短肢接点 | entry/resume/商品整合 | 毎回手の初発見・古WAIT;T11,T14 | 背景復帰は残存target/商品確認 |
| P27 Gift / I Chose This for You | 3 | MUST | Q01,Q03,Q04,Q07,Q13 | 両or片paw/顔と支持 | 低Gift提示→解放transfer | 短腕/丸paw保持面/腹余地 | 2paw/片assist/transfer marker | Gift腹顔貫通・尾補助手化;T04,T13 | 両paw版は脚支持、片assistは対側用途保護 |
| P28 Rare / A Little Knowing Wink | 2 | OPTIONAL | Q01,Q02,Q07 | 片瞼/他眼/口と頭 | 全身支持静止、両眼復帰 | 両眼の完全な面/眼窩 | 片wink/復帰/注意redirect | 片眼欠落・眼形崩れ;T01,T07 | 発見後/共有後は宛先差、追加構造なし |
| P29 Secret Candidate / Roll, Stop, Try Together | 2 | OPTIONAL | Q01,Q03,Q04,Q07,Q12 | 片paw/目/prop軌跡と対支持 | 押す→止まる→WAIT/exit | 通常paw/支持を共用 | 候補prop接触/軌跡/一度別push | 物瞬間移動・尾で回収;T04,T12 | 試し方変更版のみ二つ目接点経路、候補専用生成なし |

### C4. Shushu

| Motion ID / Family | V | 要求 | 重点Q | 部位 / 独立制御 | 変形・接触・支持 | G: 造形条件 | R/M: 後付け能力 | 極限リスク / T検査 | Variant限定の追加要求 |
|---|---:|---|---|---|---|---|---|---|---|
| S01 Living / Warmly at Ease | 3 | MUST | Q01,Q02,Q03,Q08 | 顔/小呼吸/短前肢と小耳 | 胴短肢支持安定 | 大頭/丸胴/短肢の境界 | quiet/blink/呼吸/face | 全身scale・足腹融合;T01,T03,T08 | 相手へ開く版はgaze宛先差 |
| S02 Settle into a Chosen Comfort | 3 | MUST | Q01,Q03,Q04,Q08,Q13 | 下胴荷重/片paw/顔 | 支持内settle/局所plush | 腹腿脚足裏/腕腹の区別 | 荷重corrective/片paw配置 | 腹に脚潰す・座位固定;T03,T04,T08 | 片荷重版はCOM、保持物版は保持maskQ13 |
| S03 Attention / Warm Recognition | 3 | MUST | Q01,Q02,Q08 | 目/頭/口と胴/保持paw | 既存快/支持保持 | 首/頬/頭と冠接点 | target/暖かいface/小turn | 冠浮き・大頭首折れ;T02,T08 | 好き対象→相手はgaze切替 |
| S04 Small Groom / Care for What I Like | 3 | MUST | Q01,Q03,Q04,Q08,Q13 | 片paw/対象gazeと対保持 | 届く胸腹care/花束直す | 短腕/胸腹実面/花束attach余地 | self-contact/保持補正 | 頭上伸長・花束無条件出現;T04,T08 | 実花束整え版のみbouquet保持制御Q13 |
| S05 Rest / Pleasant Drowsiness / Wake | 3 | MUST | Q01,Q02,Q03,Q04,Q08 | 頭/瞼/前肢と花束/支持 | 低休息/局所wake、物保持 | 首低頭/腹腿足境界 | drowsy/soft wake/保持mask | 眠さで物落ち・脚潰れ;T02,T08 | 眠いholdでも保持が必要なら維持 |
| S06 Tap / Poke / I Felt That | 3 | MUST | Q01,Q02,Q08 | 実触面/同側faceと胴paw | 局所受け、選んだ居方保持 | 頬頭胴軟部/硬い装飾分離 | zone ACK/快/hint | ACK遅延・全身bounce;T08,T14 | 過密区切りのみhint face |
| S07 Head Pet / Welcome the Nice Feeling | 3 | MUST | Q01,Q02,Q08,Q10 | 実頭面/faceと冠/前肢 | 頭小開き、支持保持 | 頭冠別所有/非重複touch面 | 頭ACK/owner anchor/低頭補正 | 頭圧縮で冠浮き・眼崩れ;T01,T02,T10 | 眠い受容はhalf-lid、差なし |
| S08 Cheek Pet / Enjoy It Here | 4 | MUST | Q01,Q02,Q03,Q08 | 頬L/R/顔と前肢解放 | 選んだ荷重のまま接点 | 頬厚/首/腕腹余地 | 頬補正/小提示/side解放 | 首穴・前肢腹貫通;T02,T03,T08 | 好み頬提示のみhead/target追加 |
| S09 Body Pet / Plush Warmth | 3 | MUST | Q01,Q03,Q04,Q08,Q13 | 胴実面/顔/空pawと保持paw | 局所plush、腹腿脚維持 | 胴軟部/腕腹/短脚境界 | body mask/保持mask | 腹腿一体潰れ・物落ち;T03,T08 | 保持物共存版だけ保持Q13、通常は物不要 |
| S10 Ear-root / Presented-paw Notice | 3 | MUST | Q01,Q02,Q04,Q08 | 小耳根or提示paw/同側face | 支持/保持pawを保存 | 耳厚根/丸paw実面 | 耳root/paw ACK/保護 | 耳拡大・保持物投げ;T04,T08 | 耳根/提示pawは別owner、hintは安全戻し |
| S11 Continuous Stroke / Stay with the Good Feeling | 3 | MUST | Q01,Q02,Q03,Q04,Q08 | 経路局所/face/空paw | 荷重hold、冠安定 | 連続軟面/腹脚境界 | 経路ACK/plush/hold | 全身沈み・ACKを味わい後へ;T08,T14 | 眠い満足は瞼差、差なし |
| S12 Back-and-forth Pet / A Clear Little Smile | 3 | MUST | Q01,Q02,Q08 | 反転局所/明るいfaceと胴paw | 既存居方hold | 顔軟部/首 | 反転ACK/快/hint | 指とbody左右同期;T08,T14 | 十分区切りだけhint/解放 |
| S13 High-five / Keep a Little Touch in Mind | 4 | MUST | Q01,Q03,Q04,Q08 | 空いた片paw/顔と保持/支持 | 安全荷重→低paw WAIT→戻す | 短腕/丸paw面/腹余地 | paw独立/target ACK/保持mask | 足浮き・花束落ち・腹埋没;T03,T04,T08 | 無応答は安全閉、両手保持中は後でoffer |
| S14 Invitation / Share My Comfortable Time | 3 | MUST | Q01,Q02,Q03,Q04,Q08 | 頬/頭/空pawと胴/保持 | 好き姿勢のままWAIT | 首/提示面/腕腹余地 | 複数target/保持mask/ACK | 冠/花束が顔/接点隠す;T02,T04,T08 | 低paw版だけpaw/支持、頬頭版は顔提示 |
| S15 Delight / This Feels Really Good | 3 | MUST | Q01,Q03,Q04,Q08 | 明快face/空pawと胴局所 | 支持上小快/plush回復 | 顔/短腕/腹脚実体 | 強度別喜び/局所corrective | 全身elastic・holding破壊;T01,T03,T08 | 前肢添う版は空pawのみ、大好きを長hold |
| S16 Surprise / Notice, Then Choose What I Like | 3 | MUST | Q01,Q02,Q08 | 意外face/頭と安定胴paw | 原因確認、居方保持 | 眼口/首の可動面 | surprise/target/暖かさ | 老人顔・角度過大;T01,T02 | 嬉しい意外版は満足へ、差なし |
| S17 Boundary Hint / Enough for Now | 2 | MUST | Q01,Q02,Q04,Q08 | 同側顔/前肢楽方向と胴 | 支持保持、保護物維持 | 顔/首/短腕余地 | hint/眠気や保持共存 | 閉眼品定め・保持破壊;T01,T08 | 休息/保持版だけ既存mask継承 |
| S18 Refusal / Protect My Comfortable Space | 3 | MUST | Q01,Q03,Q04,Q08,Q13 | 顔頭/前肢/小turnと保持 | 支持上withdraw、花束固定 | 首/腕腹/側外面 | withdraw/保持mask/COM | 花束盾・腹脚潰れ;T03,T08 | 保持前肢保護版はprop保持Q13 |
| S19 Recovery / My Warm Time Continues | 2 | MUST | Q01,Q03,Q04,Q08 | 顔/前肢回復と居方 | 刺激なしで自力recover | 戻る首腕/支持面 | recover/affect hold | 謝罪待ち・happy snap;T08,T14 | withdrawal版は現在turn解放 |
| S20 Food Notice / Choose a Taste | 3 | MUST | Q01,Q02,Q04,Q09 | Food目頭/口/必要短paw | 受領前停止、拒否未消費 | 口前/短腕/花束clearance | notice/保持準備/拒否 | Food花束混線・口届かない;T04,T09 | 好き度1版のみ受領口なし、支持冠保存 |
| S21 Food Consume / Five Styles | 5 | MUST | Q01,Q02,Q03,Q04,Q08,Q09 | 口/頭/短前肢と非口元顔 | bite/保持/外部提示、短脚支持 | 小口縁内部/腕腹/腹腿脚 | 5style/保持mask/口ACK分離 | 両手花束とFood同時・平面口;T04,T08,T09 | L1全5様式、事前に花束保持競合を解く |
| S22 Food Taste / Savor and Be Delighted | 4 | MUST | Q01,Q03,Q04,Q08,Q09 | taste顔/短空pawと胴/冠 | 食後支持/居方hold | 眼口/短腕/腹脚 | taste2–5/局所plush/hold | 快のため脚潰れ・顔物遮蔽;T01,T08,T09 | 2微妙/3満足/4小paw/5意外→明快喜び |
| S23 Wear / Welcome It without Losing My Shape | 3 | MUST | Q01,Q02,Q08,Q10 | 顔/頭とWear/花冠 | 1Wear/冠owner/支持保持 | 耳外側/首胸/冠別接続 | anchor/交換/解除/実surface ACK | 冠を浮かせる・顔/短腕干渉;T08,T10 | 頭上Wear専用仕様なし、初/交換/解除差のみ |
| S24 Afterglow / Close the Action, Keep the Warmth | 3 | MUST | Q01,Q03,Q04,Q08 | 前肢/顔の閉じと情動/胴 | 現在荷重の局所plush回復 | 腹腿足/腕腹/首接続 | 行為解放/affect/視線release | 全身Neutral・短脚潰れ;T08,T14 | 共有/自己快/非peakは顔宛先/affect差 |
| S25 Session Entry / My Pleasant Time Is Here | 3 | MUST | Q01,Q03,Q04,Q08,Q11 | 現在face/保持pawと支持 | 初可視poseで保持成立 | 全外面/短肢保持面 | entry/resume/商品整合 | 古WAIT・Food/Gift偽完了;T11,T14 | 眠気背景復帰は目と商品状態を別復帰 |
| S26 Gift / A Little of What I Like, for You | 3 | MUST | Q01,Q03,Q04,Q08,Q13 | 両or空片paw/顔と保持 | 低Gift WAIT→transfer、短脚支持 | 短腕/低保持面/腹clearance | 両保持/片assist/近提示/transfer | 花束Gift同時衝突・顔物隠れ;T04,T08,T13 | 両paw/空片assist/支持優先近提示の保持集合を別試験 |
| S27 Rare / A Little Smile Remains | 2 | OPTIONAL | Q01,Q02,Q08 | 口/目の思い返しと前肢 | 居方支持保持 | 既存顔面共用 | rare smile/gaze/入力合流 | 恒常閉眼・意味ない頷き;T01,T14 | 共有/感触思返しはgaze差、新生成不要 |
| S28 Secret Candidate / Bouquet Peek and Welcome | 2 | OPTIONAL | Q01,Q03,Q04,Q08,Q12 | 花束保持/顔peekと冠/支持 | 短腕届く顔下、部分頬target | 通常短腕/顔とprop余地のみ必須 | 候補bouquet保持/peek/安全戻し | 両手支持不可・顔全隠れ;T04,T08,T12 | 片頬版のみside opening、候補のため腕伸長なし |

## D. Common Anatomy / Rig Capability

### D1. Capability contract（各行のTはUNKNOWN）

Q01–Q13はPhase 3 Nを保持し詳細化。Q14（合成/解放）とQ15（空間/受渡し/実行）を追加する。**Gは生成直後に評価する形状能力、R/Mは後付け候補であり特定方式の決定ではない。**

| Q / 要求区分 | G: 生成で得る形状 | R: Rigで補える制御 | M: Motionで補える表現 | T: 未検証の受入方法 |
|---|---|---|---|---|
| Q01 Face / attention — MUST | 両眼の位置/大きさ/眼窩、瞼が閉じられる受け面、Canonical口縁/頬の局所厚。小顔を平面textureだけで閉じ込めない | gazeと頭、左右瞼、口と頬L/Rを分離。bounded gaze/close-target convergence、blink/half-lid/片閉/口開閉/小笑顔/期待/安心/驚き/不満。bone/morph/局所materialの組合せ候補 | 原因の評価→表情hold→余韻、blinkとaffect調停、bite中の非口元ACK。人間眉/巨大口を追加しない | T01: Neutral/開閉眼/片閉→両開/近遠視線/各感情/口処理と同側ACKをFront/3⁄4で比較。眼形/配置/幼さを保ち口面が裂けない |
| Q02 Head / neck — MUST | 頭/頬/胴の意味境界、首の連続体積、傾ける内側余地。首を長く露出して解決しない | head yaw/pitch/roll/低頭/leanと胴の独立、首/頬corrective（SHOULD）。耳等は各ownerに従属 | 視線先行or手元先行の選択、頬/額提示、現在姿勢からの方向変更 | T02: 頭左右/低頭/傾き/深頬→release/side変更を段階的に試す。可動終端はIdentityと接点/首境界から決める。角度UNKNOWN |
| Q03 Support / weight — MUST | 足底/蹄の厚み、短肢/腹/下胴の区別、支持し得る接地面、主要体積と尾根の一貫性 | 支持と操作肢のmask、接地lock/IK候補、体幹/骨盤の小shift、荷重corrective。見かけの重心と支持の整合を示し物理solver成功を仮定しない | 移荷重→肢解放→再接地、安全なmoving hold、active-pose settle | T03: 支持面/足接点を表示し片肢/両前肢操作/低休息/戻し。残る支持内で重さが読め、指や尾を未承認支柱にしない。動的安定はUNKNOWN |
| Q04 Forelimbs / contact — MUST | 短前肢の自然な根、腹と自由区間の境界、実蹄/paw面。指/手掌の新設や伸長なし | 前肢L/R独立、接面方向/局所受け、対側保持/支持の保存。必要なcorrective（SHOULD） | 低High-five、self-care、bounded brace、保持/解放、届く面を選ぶ | T04: 左右単独提示/低target/両保持/自己面到達/回収。短さを維持して顔と接面が見えるか。腕腹貫通/足浮きはFAIL |
| Q05 Carol fleece — MUST、broad residualはOPTIONAL | 頭-owned/胴-owned/尾-owned体積、顔開口/内側面、四肢と耳根の余地。雲球列や独立浮遊shellを身体の代りにしない | owner weights/接続補正、FINALの8用途（E）、局所圧縮/開口とmacro transformを分離。head/torso位置追従zero lag | 現触点/隣接小shape/任意hero shape/解放。macro遅れを使わずSHOULDの小authored回復 | T05: 首/頬/peek/低蹄/深lean/装備を owner表示で観察。押圧を解いた後に位置滑り/浮雲/全体scaleがない |
| Q06 Jill anatomy — MUST、候補翼peekはOPTIONAL | 胸/腕/翼根L/R/葉根/horn/太尾の所有と自由区間。翼膜の実面/厚み感、葉の立体輪郭、Canonical marking | 胸と前肢/翼の独立、左右翼fold/open、膜/root補正、葉の局所follow/stop、連続tail root曲げ。hornは硬い頭所属、耳bone化なし | 胸先行→選択翼葉尾、翼を動かさないhold、低paw、根元ACK | T06: 片/両翼開閉×胸/paw/頭/物/装備。根潰れ/膜裏面消失/葉が顔を塞ぐ/尾に体重代行させる状態を検出。飛行は未要求 |
| Q07 Pino anatomy — MUST、尾inspection/rare winkはOPTIONAL | 丸頭胴/内寄り短腕/短脚/単一厚尾/両眼。尾自由区間と根元、paw面/足裏 | 独立短paw/腹corrective、尾rootから連続bend/follow、両眼基礎制御。wink自体は候補で、両眼生成はMUST | 片側試す→見る→止める、自己/他者touch区別、重量の尾settle | T07: 手元可視性/押す戻す/腹腕干渉/太尾連続性、両眼復帰。尾の把持/前巻き/balloonを前提にしない |
| Q08 Shushu anatomy — MUST、bouquet SecretはOPTIONAL | 大頭/丸胴、短腕/腹/腿/脚/足裏の区別、小耳根。花冠/花束は独立所有、身体に焼き込まない | 荷重局所plush/回復、短paw独立/保持、脚腹corrective/低姿勢、小耳独立、冠head anchor/束holding anchor | 自分の快の居方→顔歓迎→前肢休む。花束なしの全core、保持競合を先に解く | T08: 低休息/座る能力/片肢/両保持/冠/花束on-off。腹脚を一塊に潰さず短さを保つ。座位Neutralは承認しない |
| Q09 Food / mouth — MUST | 口縁/閉口/開口の立体連続、必要な内部の受け、口前と短肢保持の余地。舌は必要な小露出の追加余地を評価、長舌必須なし | 口開閉/小咀嚼相当/小舐め/飲む接点、保持mask/口marker/残量・safe node、非口元face分離。局所内部/短舌はBlender追加候補 | L1の5style、好き度1未消費/2–5食後、残量/接点/consume事実を別扱い | T09: 一口/複数口/舐め/飲む/大物×顔ACK/取消。接点・保持・残量が見え、小口で成立。口平面/食物瞬間消失だけはFAIL |
| Q10 Wear / motifs — MUST | owner表面/厚みと取付余地。独立アクセサリを身体へ融合しない | head/耳根/胸等のnamed anchor、変形面追従候補、局所corrective（SHOULD）。surface所属を保つ | 1Wear、交換/解除、物のACKと皮膚ACK区別、Carol月星再装着 | T10: neutral/lean/peek/翼/paw/Food/Giftで各anchor。顔/主要輪郭/接面を守りずれ/浮き/二重物がない |
| Q11 Session state — MUST | 初可視姿勢で隠れない実接点、露出外面の一貫性 | 現在pose/face/propを復元できるchannel、無効touchを解くrestoration | Entry/背景復帰、古WAIT解放、consume/transfer事実を姿勢から推測せず照合 | T11: 食前/食後/提示/受理/眠気/余韻で離脱復帰。古接点や消費/贈与の偽完了なし |
| Q12 Secret targets — Carol MUST、他3候補OPTIONAL | Carol顔/頬額/pocket空間。候補他3は通常身体を共用、専用変形比率を生成必須にしない | body-owned target/prop marker、setup/WAIT/主turn/side/exitの分離、可視clamp | owned/activation/cooldown/ordinary touch exit、候補の採否前は実装しない | T12: C43–45各接点/2turn/外れ/無応答/終了、J27/P29/S28候補の極端pose。顔/target/支持を同時に見せられない候補は再設計へ |
| Q13 Gift / holding — MUST | bounded Giftの支持可能面/短肢余地、Carol reveal/頬push/蹄面。花束等の既存保持面も関連検査 | holding/assist/transfer marker、保持と非保持face/ACK分離。安全な置き場は候補で実座標UNKNOWN | 本人意図→提示→WAIT→受理/transfer→余韻、未受理保存仕様はRへ。通常保持への再利用はGiftを発生させる意味ではない | T13: 各提示profile×他保持物/Touch/離脱。手と物の関係、解放/受理を可視化。二重grant/消失で衝突解決なし |
| Q14 Channel composition / continuity — MUST（追加） | 押す面/口/保持面/支持面が区別可能、共用面の競合が分かる形 | gaze/face/head/局所/保持/支持のmask、骨とmorph組合せの補正、競合時の制約。driver/constraint等のexport非対応依存を残さない設計候補 | ACK/主行為/余韻を独立、今poseからblend、release kill/reset、safe node、反復/眠気強度。正確な実装方式は未決定 | T14: C0共通の反対側touch/同時受理touch/release/peak中touch/bite中ACK/WAIT別zone/無応答。局所が読め、支持/保持/口を壊さない |
| Q15 Spatial / GLB / smartphone — MUST（追加） | Front Hero/3⁄4/側/後/低姿勢でcoherent。可動面の厚み、隠れ領域の機能を持つ | export可能なskinning/morph/attachment/animation候補、座標/scale/axis整理、boundsと表面所有 | runtime組合せ/anchor再評価、読みやすい演技量、4匹の個別性能調整 | T15: 同じassetのGLB再読込→PlayCanvas→縦画面/Xiaomi 14T Proで顔/ACK/接面/影/負荷。Pixel 7a-classは別の未検証target |

T01–T15は「検査条件のID」であり、今回実施した3D試験ではない。T01–T13を後続でまず段階的にpose/変形評価し、T14で合成、T15で受渡し/実機を評価する。Rest単体のPASSで必要動作をPASSにしない。外見と身体が正常な生成結果にRigがない段階ではR/Mを欠陥と誤分類しない。

### D2. Capability → Family逆引き

全Familyの基礎Q01,Q02,Q03,Q14,Q15、Carol全46のQ05、Jill全27のQ06、Pino全29のQ07、Shushu全28のQ08が先に適用される。以下はC表の追加/重点要求。Q13を通常保持に用いる行では、保持独立能力を再利用しGiftイベントを付与しない。

| Q | 重点/追加Family |
|---|---|
| Q01 | C01,C02,C03,C04,C05,C06,C08,C09,C10,C11,C12,C13,C14,C15,C16,C17,C18,C19,C20,C21,C22,C23,C24,C25,C26,C27,C28,C29,C30,C31,C32,C33,C34,C35,C36,C37,C38,C39,C40,C41,C42,C43,C44,C45,C46,J01,J02,J03,J05,J06,J07,J08,J09,J10,J11,J12,J13,J14,J15,J16,J17,J18,J19,J20,J21,J22,J23,J24,J25,J26,J27,P01,P02,P03,P04,P06,P07,P08,P09,P10,P11,P12,P13,P14,P15,P16,P17,P18,P19,P20,P21,P22,P23,P24,P25,P26,P27,P28,P29,S01,S02,S03,S04,S05,S06,S07,S08,S09,S10,S11,S12,S13,S14,S15,S16,S17,S18,S19,S20,S21,S22,S23,S24,S25,S26,S27,S28 |
| Q02 | C01,C02,C03,C04,C05,C06,C08,C09,C11,C12,C13,C14,C15,C17,C18,C19,C20,C21,C22,C23,C24,C25,C26,C27,C28,C29,C30,C31,C32,C33,C34,C35,C36,C37,C38,C39,C41,C42,C43,C44,C45,C46,J01,J02,J05,J06,J07,J10,J11,J13,J15,J19,J20,J22,P01,P02,P06,P07,P08,P09,P11,P12,P13,P15,P17,P20,P21,P22,P24,P28,S01,S03,S05,S06,S07,S08,S10,S11,S12,S14,S16,S17,S20,S21,S23,S27 |
| Q03 | C01,C06,C07,C09,C13,C16,C18,C19,C20,C21,C23,C24,C26,C30,C31,C32,C33,C34,C35,C36,C38,C40,C42,C43,C46,J01,J03,J04,J05,J07,J08,J09,J10,J12,J13,J14,J15,J16,J17,J18,J20,J21,J23,J24,J25,J26,J27,P01,P03,P04,P05,P06,P09,P10,P12,P14,P16,P18,P19,P20,P22,P23,P25,P26,P27,P29,S01,S02,S04,S05,S08,S09,S11,S13,S14,S15,S18,S19,S21,S22,S24,S25,S26,S28 |
| Q04 | C07,C16,C18,C26,C40,C46,J03,J04,J08,J12,J13,J14,J16,J17,J20,J25,J27,P03,P05,P08,P09,P10,P11,P12,P13,P14,P15,P16,P17,P18,P19,P20,P21,P22,P23,P24,P25,P26,P27,P29,S02,S04,S05,S09,S10,S11,S13,S14,S15,S17,S18,S19,S20,S21,S22,S24,S25,S26,S28 |
| Q05 | C03,C04,C07,C08,C09,C10,C11,C12,C13,C14,C15,C19,C20,C21,C22,C23,C30,C31,C32,C33,C35,C36,C37,C38,C39,C40,C42,C43,C44,C45,C46 |
| Q06 | J01,J02,J03,J04,J05,J06,J07,J08,J09,J10,J11,J12,J13,J14,J15,J16,J17,J18,J21,J22,J23,J24,J25,J26,J27 |
| Q07 | P01,P02,P03,P04,P05,P06,P07,P08,P09,P10,P11,P12,P13,P14,P15,P16,P17,P18,P19,P20,P23,P24,P25,P26,P27,P28,P29 |
| Q08 | S01,S02,S03,S04,S05,S06,S07,S08,S09,S10,S11,S12,S13,S14,S15,S16,S17,S18,S19,S21,S22,S23,S24,S25,S26,S27,S28 |
| Q09 | C25,C26,C27,C28,C29,C30,C31,C32,C37,J19,J20,J21,P21,P22,P23,S20,S21,S22 |
| Q10 | C02,C05,C10,C33,C37,J22,P24,S07,S23 |
| Q11 | C34,J24,P26,S25 |
| Q12 | C43,C44,C45,J27,P29,S28 |
| Q13 | C46,J25,P27,S02,S04,S09,S18,S26 |
| Q14 | 全130（継承） |
| Q15 | 全130（継承） |

## E. Carol Anatomy / Rig Contract

**MUST / G:** 羊らしい低い四足支持、小顔とCanonical眼、耳厚/根元、重い短蹄、自然な後部の絞りを保つ。蹄の3分割は見える形状の分節であり「3本の独立指」や新しい掌ではない。後足の実底面と前後脚根を区別する。Body-only Frontで隠れる後方支持を、正面の蹄だけで代用しない。

**所有:** 顔/顎/耳はhead、頭周囲の羊毛はhead-owned、下顔のcollarはneck/torsoに属し**jaw/chinには羊毛を新設しない**（STATEのHuman semantic）。胴羊毛はtorso-owned。見える尾は独立した根付きfluffy tuftで、胴の雲に溶かさずtail-owned。首を曲げる時は隣接owner境界で連続形を補正する。**macro positional lag = zero**を頭/胴/尾の位置所有に適用し、tail自身の独立可動と羊毛shell遅れを混同しない。既存3D資産の現状態から今回の新設計適合を推定しない。

| 能力 / 優先 | Gで必要 / Rで追加 / Mで表現 | 実物限界 / 検査 |
|---|---|---|
| 頬L/R / 深頬 — MUST | 頬自体の厚みと顔羊毛境界、Rで局所頬corrective/首/胴COM、Mで受け→必要lean→止める→解放 | C09/C38の同側頬と眼が崩れず、自分の蹄で支えられる深さT02/03/05。可動域UNKNOWN |
| Fleece 8用途 — MUST（利用可能性）、broad実使用OPTIONAL | FINAL §23の **cheek-L / cheek-R / forehead-front / front-stroke / side-back / face opening / broad hero shape echo / broad post-action settle** を対応面に割当。Rでmask/morph/骨局所等。8個のShape Keyを強制しない | 片側を押して他側/胴macroが滑らない。heroと直接touchが競合時は局所ACKを保ちbroadを抑えるT05/14 |
| Face-in-Fleece / Hide-and-Peek — MUST | Gで顔の入る立体余地/開口内側/目・頬を出せる面。Rでhead/開口/首補正、Mで意思→隠れ→peekとowned loopを別 | C39は通常Signature、C45はowned interactive。顔完全消失を長い無反応にしない。局所openingだけで不成立なら開口地域の再構築/再生成を判定 |
| 耳L/R / 顔 — MUST | 小顔眼/口/頬、実耳根。RでFINALの12顔presetと10耳stateを表現できる組合せ、Mで選択的近耳参加 | 12/10はsemantic stateの件数で骨/morph数ではない。顔の羊毛開口とear-root anchorの合成T01/02/05/10 |
| Low forehoof — MUST | 羊毛下の実短脚/蹄、支持時と提示時の自由区間。Rで片前蹄と後支持、Mで移荷重/低提示/ACK/回収 | C40の2profile、C16のsensitiveとofferを区別。**通常の軽い前蹄交流が可能な身体能力**も同じ構造で用意するが、発動/頻度を新仕様化しない |
| Cloud Sigh — MUST、shape echoはOPTIONAL | 顔/頭/小胴が独立、Rで支持された胸胴開き/局所補正、Mで呼吸をほどくようなphrase | C42/食後C31。全身scale/ジャンプ/羊毛浮遊を用いず、peakとhold/recoveryに顔が残る |
| Food / Moon Ball / Star / Gift / Wear — MUST | 口前、頬額nudge面、front-fleece pocket/reveal余地、低蹄assist面、モチーフ取付面。接点は後付け | C26/C43/C44/C46全接点とC37/T10。蹄で保持不可なら頬/reveal/外部提示を候補比較し、承認済みprofileの削除はHumanへ |

**C40保護:** FINALのrare Layer 2、trigger（high socialSeeking / recent successful invitation）、hard cooldown **90–240s**、user tap only、単発低蹄/非chain、WAIT無応答soft releaseを継承する。これは既承認参照値で新たな角度/頻度設計ではない。通常軽交流の呼び出しはHuman未決定（U06/H2）。身体の能力を用意することと通常化の承認を分け、Family/profile件数を増やさない。

## F. Jill Anatomy / Rig Contract

**MUST / G:** 大きい幼い顔、春緑、短肢/丸い胸胴、horn-like桃色頭付属、頭/首葉、翼L/R、太く根付きの尾と葉状稜線、Canonical cloverを保つ。頭葉/首葉/胴側の境界をownerとして区別し、葉を全て頭の固定飾りや単なるtextureにしない。硬いhornを通常耳として揉む/折る/軟化する解決はしない。

| 能力 / 優先 | G / R / M契約 | 実物限界 / 検査 |
|---|---|---|
| 胸先行の喜び — MUST | Gで胸/前肢の別根と首連続。Rで胸小起こし/腕独立、Mで胸から必要翼葉尾へ選択伝播 | J03/J08/J12–14/J21。胸の上昇が脚伸長や全身上下bounceにならないT03/06 |
| 左右翼fold/open — MUST | Gで二つの根と膜/枠の実面、自由輪郭。Rで根rotation/局所膜補正、Mで片/両翼参加と休むhold | fold時の葉/腕/胸、open時の顔/画面端。膜を開くと穴/紙裏面消失がない。翼の生物学的関節数はUNKNOWN |
| 葉/身体花 — MUST所属、自然follow SHOULD | Gで頭/首葉の輪郭/厚み感/基部。Rでowner追従と必要地域の小follow、Mで収まり/停止 | 葉先個々にboneを必須化しない。身体にある花はCanonicalとの取付分類をして戻す。離れた花/蝶を常設化しない |
| 太尾root/連続変形 — MUST | Gで骨盤の太い接続と自由区間、稜線の立体輪郭。Rでrootから連続bend/重量follow、Mで小settle | 腹/足/翼/葉との干渉T06、尾が支持脚を代行しない。曲率や遅れ量UNKNOWN |
| 低High-five/保持 — MUST | Gで短paw面/腕腹・腕翼の余地。Rで片paw/胸/支持の分離、MでJ12低WAIT/payoff/回収 | 足支持の具体形態はUNKNOWN。二足で全要求が成立するか実形状で判定。尾/翼支柱や長腕で救済しない |
| Wing-shelter Peek — OPTIONAL | 通常翼構造を使うR/M候補。顔横に小部分を隠して返す、左右経路 | J27。翼で全顔を覆う能力/飛行/翼把持は必須でない。通常fold/openが合格して候補peekが不成立なら候補の可愛さ/採否をHumanへ |

**SHOULD:** 翼膜の曲面と枠/root補正、胸/腕の局所correctiveを少数の意味ある地域で設計する。不要な再生成より、正常形状を保った翼rig再配置/weight修正を先に判定する。葉に埋もれた翼根が3Dで失われていれば造形修復規模を再評価する。

## G. Pino Anatomy / Rig Contract

**MUST / G:** 丸い大頭/低いcompact胴、内寄りの短前肢、短い足、耳/頭tuft、**単一の幅広く厚い尾**が後骨盤から連続する。尾rootと胴は接続し、自由尾と脚/脇腹は融合しない。厚みは各断面で連続し風船のように独立球へ膨れない。両眼は生成必須、Canonicalのwinkは表情資源。

| 能力 / 優先 | G / R / M契約 | 実物限界 / 検査 |
|---|---|---|
| 内寄り前肢L/R — MUST | Gで左右root/自由輪郭/腹との余地。Rで左右paw独立、Mで一方を止めてもう一方を試す | P03/P11/P14/P15/P17。前肢先とその変化を本人の目/Front Heroの両方から認識できるかT04/07 |
| 小試行と観察 — MUST能力、P03具体案DRAFT | 置く/軽荷重/上げる面、Rで丸paw局所受け/回復、Mで「変える→見る→止める」 | P03第一候補は床/低支持面へ届くことがUNKNOWN。接面の小方向変更、届く身体面の軽押し→解放を見る、非対称の手合わせ→隙間を見る等は代替P。腕を延ばさず、結果/快が見える案をHuman比較 |
| 重い太尾 — MUST | Gでroot/free segment、Rで連続bend/owner root/重みfollow、Mで胴後のsettle | 尾を第三の手/前巻き/常設支柱にしない。P04は実露出を見られる時のOPTIONAL拡張でcoreの成立に使わない |
| 両眼とwink — MUST基礎 / P28 OPTIONAL | Gで両眼面/窩、Rで左右瞼独立、Mでrare片閉→両眼復帰 | 閉じた目をtexture線だけとして固着させない。視線/笑顔/片閉の組合せで他眼appeal保持T01 |
| 低paw遊び/Food/Gift — MUST | 短paw接面と腹前余地、Rで保持/brace/接地mask、Mでtargetと結果gaze | P14/P22/P27。両前肢保持時は足支持、保持不可サイズはbounded提示へ。尾把持による成立は不可 |
| 低休息/支持変更 — MUST、座位Neutral UNKNOWN | 下胴/脚/足底を区別、Rで局所荷重/低頭/支持corrective、MでP05/P06 | reclineのCanonicalやbody-only立位からNeutralを自動決定しない。丸胴転がし/脚伸長なし |

**SHOULD:** 腹と腕の接近で丸さを維持するcorrective、太尾断面を潰さない局所補正、手元を見たまま頭touch ACKを返すface mask。P03が不成立でもまず演技/対象面を比較し、必須前肢/接触能力自体が欠落している時だけ造形の再生成候補にする。

## H. Shushu Anatomy / Rig Contract

**MUST / G:** 大きい幼い頭、桃色小耳/眼周辺/短paw、丸いplush胴、短い腿/脚/足と足裏。腹から足を「同じ球の突起」として作らず、低姿勢で重みを受ける下胴/腿/足の役割を残す。花冠はhead-ownedアクセサリ、花束は保持物で別owner。どちらも身体texture/腹の固定塊へ焼き込まない。

| 能力 / 優先 | G / R / M契約 | 実物限界 / 検査 |
|---|---|---|
| 低く落ち着く/座る能力 — MUST、Game Neutral選択UNKNOWN | Gで腹/腿/脚/足底と後下胴、Rで支持/屈曲/局所corrective、Mで低rest/settle | 深い座位を通常必須姿勢にしない。生成立位/低squatから低姿勢へ移す際に短脚の長さと足裏位置が保てるかT08 |
| Plush local compression — MUST | Gで局所厚と荷重面、Rで触点/荷重形状と回復、MでS02/S09/S15/S24 | 胴全体scale、腹と脚を潰すmochi、無限弾性で表現しない。回復遅れはshapeであり冠/身体位置の浮遊ではない |
| 短前肢L/R / low High-five — MUST | Gで根元/自由paw/腹境界、Rで片肢と保持/支持分離、Mで低WAIT/ACK/休む | S13の即ACK後hold、両手保持なら後に誘う。手を長く/人間掌にせず顔とtargetを露出T04/08 |
| 頬/頭の歓迎 — MUST | Gで頬厚/首/冠非重複面、Rで小提示/圧縮/顔独立、Mで居方を保った明瞭快 | S07/S08/S14。Carol深全身leanの速度違いにしない。冠/束の下でも同側面と顔を見せる |
| 花冠と花束 — MUST所有、Bouquet Peek OPTIONAL | Gで身体側取付面のみ。Rでhead冠/保持束/手からの解放/安全置き場、Mで実在時だけ持直し | 束なしS01–27 coreが成立。S04の束整え、S09保持共存、S28候補の全保持/遮蔽を試す。花束初期所有/出現/退出はHuman未決定 |
| Food/Gift/Wearの競合 — MUST | Gで口前/短腕/首胸/耳外側余地、Rで保持mask/anchor、Mで安全な事前状態切替 | 両手束＋両手Food/Giftを同時要求しない。目の前で物を消して解決しない。頭上Wearは専用交換仕様なしに使わない |

**SHOULD:** 足裏/padはCanonicalから素材/必要な局所凹凸を再現し、立位画像で見えないからと脛前へ移さない。冠/束offでも丸さと通常Motionが魅力的かを確認し、装飾だけに可愛さを依存させない。

## I. Mesh / Part / Deformation Requirements

### I1. 接続・分離の契約

**独立して動く部位＝必ず別メッシュではない。** 関節を跨いだ適切な変形領域/weightsがあれば同一meshでも独立制御できる。別meshでも所属/根元/接点が破綻すればFAIL。次の分類は完成能力を要求し、Tripoの特定出力構造を断定しない。

| 領域 | 一体化/接続を許す条件 | 独立制御 / 形状と材質 | Blender修正可能な欠陥 | 再生成/入力差戻し候補 |
|---|---|---|---|---|
| 眼/瞼/顔 | 同mesh/別眼どちらも可。眼形/窩/瞼受けが連続 | gaze、瞼L/R、頬/口を分離。highlight/色は材質候補、窩/開閉に必要な面は形状 | UV/色、eye材質、局所retopo/瞼/窩の補正 | 大きさ/配置/顔容積が多方向でoff-model、片眼と顔構造が失われて再構築規模が大きい |
| 口/鼻口元 | 顔と接続、口内部別part可 | 開閉/咀嚼/舐め/飲む受領面は立体能力。鼻色/赤みは材質でよい | 小内部/短舌/口縁retopo、morph/weight修正 | 黒い口絵だけでmuzzle/顔比率が成立しない、開口追加がIdentityを変える |
| 頭/首/胴 | 自然な連続mesh可、隠れ接合可 | headと胴独立、首bendで奥側にも面 | loop追加/weights/地域corrective/隠れ接合修復 | 頭胴が誤体積で一塊、首回転余地のため比率改変が必要 |
| 耳/horn/tuft | root接続、耳同mesh可 | Carol/Pino/Shushu耳L/R、小tuft所属。Jill hornは頭付属で耳の軟変形を要求しない | root補強/厚み/weights/局所接合 | 主要付属欠落/根位置違い/Identity輪郭が各viewで別構造 |
| 肩/前肢/蹄paw | root接続、自由区間は胴に融合させない | 左右と支持/操作を分離。蹄3分割/丸paw外形は立体、細色/pad色は材質候補 | 小web除去/局所分離/retopo/weights | 自由肢が腹に全面融合、短肢を再発明しないと回復不能、根の位置/数誤認 |
| 腹/腿/脚/足 | 軟部は連続可、各支持機能を識別 | 足底厚/短脚・腿の体積は形状、pad/色は材質＋必要局所 relief | 内股web除去/局所retopo/足裏素材/corrective | Shushu等の腹腿脚が板状一体で低姿勢を作れない、長脚化が必須 |
| Carol fleece | head/torso/tail地域の連続volume可、制作上別mesh可 | lobe外形/開口/顔余地は形状、細雲色/soft shadingは材質。body-owned zero lag | owner weights/局所retopo/接合/corrective | 独立浮雲列/滑るshellに依存、顔収容/蹄余地が全体比率改変なしに作れない |
| Jill翼root/膜/枠 | root接続、膜/枠同mesh可 | 左右wing/root独立、膜実面と厚み感/裏面、枠輪郭は形状 | 膜retopo/薄面厚み/裏面/weights/root correctives | 翼が葉/腕へ全面融合、二root/主要膜輪郭が不明/欠落 |
| Jill葉/稜線 | 基部の所属を保ち一部一体可 | シルエット葉は形状、葉脈/色は材質。地域単位follow候補 | 局所分離/根補強/材質/clover復元 | 葉を消すと頭首体積そのもの欠落、翼との境界再発明が必要 |
| Jill/Pino太尾 | root接続、尾と胴同mesh可 | rootから自由部へ連続bend、重量断面。尾形状はtexture代用不可 | 根/断面retopo、脚との小web除去/weight | 尾が脚/胴の塊に埋没して単一経路/断面を復元できない、切断浮尾 |
| 冠/束/月星/Wear | 身体ownerと装飾の物体所有を分離 | detach/交換/解放できる可視物は別asset/part候補。独立mesh義務より所有が要点 | 身体を復元可能な小融合の分離、anchor追加/アクセサリ独自制作 | bouquetが腹や手全体を置換、装飾除去で顔/胴が欠落。Body-only再入力を検討 |
| Food/Gift/Secret props | 身体と別所有。接触時も身体へ永久結合しない | 接点面/保持/軌跡は形状と制御、残量素材等は候補 | bounded prop/接点/marker/clip制作 | propだけの不適合で正常な全身を再生成しない。身体側reach/顔形状の欠落は別判定 |

### I2. 修復単位と再生成判断

1. **入力だけの不整合:** view/slot/pose対応が矛盾する場合、先に入力を照合する。Creditsを使って矛盾した身体を引き当てない。
2. **正常形状＋制御欠如:** bone/weights/morph/clip/anchor欠如、Auto Rig誤認はR/Mの修正。形状が正常なら自動Rig失敗だけで再生成しない。
3. **Identity内で戻せる局所欠陥:** 小web、薄膜、mouth内部、局所loops、素材/UV/markingはC/Dの補正候補。補正後に関連Tと組合せT14を再検査する。
4. **主要構造欠落/広域融合/多方向Identity破綻:** Canonicalから多部位を発明し直す必要、必須可動に比率変更が必要、修復が大規模になるなら入力修正→再生成を比較。Blender地域再構築がより確実なら採用できる。費用/工数の固定閾値はUNKNOWN。
5. **候補演技だけ不成立:** 既存MUST能力が正常ならJ27/P04/P28/P29/S27/S28やP03第一案の採否/代替を戻す。未承認候補のために必須Identityを壊して再生成しない。
6. **承認済みMotionがIdentityと両立しない:** 実物証拠を添えHumanへ。FINALを黙って削る/比率を伸ばす/成功と呼ぶことを禁止する。

「生成時必須」は最初のTripo出力を無修正採用する義務ではない。局所修復後にG条件が満たせるなら身体を保持する。生成姿勢を綺麗に見せるだけの腕の隙間は、R変形時のclearanceを保証しない。

## J. Critical Pose Stress Matrix

以下は**将来の検査指示**。今回pose/rig/clipは作成していない。「最大」は数値角度の限界でなく、その演技で最も厳しい組合せ/位相を指す。T01–T15はD節の検査条件。全行で、開始→到達→接触/保持→解除→現在姿勢への復帰を、Front Hero・左右3/4・側面・必要な背面/低い視点で確認する。support欄は成立させるべき荷重経路であり、実モデルでのPASSではない。

### J1. Carol

| 検査姿勢 / Motion ID | 能力 | 支持点 | 最大リスク部位 | 自己干渉 | 顔/接点の遮蔽 | Identity破綻 | 生成後の検査 | 修正/代替 |
|---|---|---|---|---|---|---|---|---|
| Neutral / C01,C07,C33 | Q01–03,05; 呼吸と接地分離 | 基準の4蹄、移行中の残存支持 | 頭胴fleece・脚root | 前fleece↔蹄 | 口/前蹄が雲に埋まる | 雲を滑る別shellにする | T02,03,05,14; 接地保持のweight shift | owner/weights/接合修正。比率不良はGへ |
| 深い頬寄せ / C09,C38 | head/neck＋頬L/R局所圧縮 | 荷重を残す蹄 | 頬・首・collar | 頬↔torso fleece/耳 | 近側眼/接触頬 | 顎に羊毛、眼間隔・muzzle変化 | T01–03,05; 左右、圧縮→回復 | 首/頬correctiveと到達域調整。深さと可愛さはHuman |
| 片前蹄High-five / C40 | 低いL/R提示、接触中の顔ACK | 残る3蹄と胴荷重 | 肩・蹄後部絞り | 蹄↔前fleece/胸 | 提示面/反対眼 | 脚長化、掌/指追加 | T03–05,14; touch解除・無応答帰還 | 局所clearance/支持移行、targetを低く近く。rare契約固定 |
| Food / C25,C26,C27–32 | 5styleの口/頬、支持と受領 | 接地蹄、必要な前蹄assist時は残存支持 | 口縁・前fleece | Food↔鼻/雲/蹄 | 噛む接点・眼 | 大口化/顎fleece | T01,03–05,09,14; 拒否/各味/cancel | item位置/size、内部/clip補正。受領形状欠落はG判定 |
| Gift / C46 | fleece reveal/頬push/rare hoof assist | 接地、assist時残る3蹄 | 前fleece開口・頬・肩 | Gift↔fleece/Wear/蹄 | reveal前後の物体/顔 | 浮雲/物体瞬間出現 | T03–05,10,13,14; 全3profileと移管 | owner/prop経路/局所開口。広域収容欠落はG判定 |
| 低い休息 / C01,C04,C35 | head低下、body-owned soft settle | 蹄/低姿勢の接触面を実物で確認 | 脚root・腹fleece・首 | 腹↔蹄/地面、耳↔雲 | 顔が胸雲に沈む | 体積崩壊/脚消失 | T02,03,05; 降下→長hold→復帰 | 局所圧縮/pose修正。横臥等を新必須にしない |
| Face-in-Fleece Peek / C39 | 顔包み・局所隙間・耳/眼 | 接地蹄 | head/torso境界・顔余地 | 顔↔雲の閉鎖面 | peek時の両眼/口 | 顎羊毛/頭を雲から切断 | T01,02,05,14; 左右/開閉/interrupt | ownership/局所corrective。顔余地が作れなければG再評価 |
| Cloud Sigh等 / C35,C36,C41,C42 | 呼気とfleece局所、moving hold/遅いlook-back/hero | 蹄支持を継続 | 胸/首・fleece連続性 | 雲↔雲/脚/耳 | sigh口/振返り眼 | macro lag、呼吸で全身ゴム化 | T01–03,05,14; hold/releaseと重層 | 身体追従zero lag＋局所変形。遅い感情は演技側 |
| Moon Ball / C43 | 額/片頬nudge、二turn | 接地蹄・小荷重移動 | 額/頬/球接点 | 球↔鼻/雲/地面 | nudge接点と眼 | 口で運ぶ/球が身体化 | T01–03,05,12; 二turn、解放/終了 | 球軌跡/target/局所頬。額頬の方式を維持 |
| Star Peek・HidePeek / C44,C45 | L/R/front pocket、peek/side swap | 接地蹄 | 雲pocket/顔首 | 星↔雲/顔、顔↔雲 | 顔/星/覗き口 | 浮雲化・過度隠し | T01,02,05,12,14; C44全3位置/C45最大2turn・1side swap | pocket/顔可視調整。HidePeekへpropを追加しない |
| Wear併用 / C02,C05,C37,C38–40,C43–46 | head/ear-root/front-fleece anchorと可動 | 当該演技の支持 | anchorowner・首/雲 | 月星/Wear↔眼/耳/蹄/Food/Gift | 顔・Signature接点 | 身体所有と装飾所有の混同 | T05,09,10,12–15; 装脱/各極端姿勢 | anchor/asset位置/重なり修正。Canon比率は維持 |

### J2. Jill

| 検査姿勢 / Motion ID | 能力 | 支持点 | 最大リスク部位 | 自己干渉 | 顔/接点の遮蔽 | Identity破綻 | 生成後の検査 | 修正/代替 |
|---|---|---|---|---|---|---|---|---|
| Neutral / J01,J04,J23 | 胸呼吸・足支持・翼/尾root follow | 接地足、weight shift後の支持 | 胸・翼root・尾root | 葉↔翼/胸/尾↔脚 | 胸の表情/前肢 | hornが耳、胸clover欠落 | T02,03,06,14; 全view | root/材質/weights。入力左右照合を先行 |
| 深い頬寄せ / J07,J10,J11 | headneck・頬・胸からの応答 | 接地足、近づく荷重 | 首葉・頭付属・翼root | horn/葉↔翼/頬 | 翼が眼/頬を覆う | 細首/顔比率変化 | T01–03,06; 左右lean/release | leafowner/首corrective・近いtarget |
| High-five / J12 | 片前肢低提示、胸と独立 | 残る支持肢/足と胴。具体足配置UNKNOWN | 肩↔胸/翼root | 前肢↔翼膜/胸 | 提示面/顔 | 長腕化/浮足 | T03,04,06,14; L/R・ACK | 支持移行/翼reserve/target調整 |
| Food / J19–21 | 口5style・受領・翼reserve | 足支持、assistの残存支持 | 口/胸/肩 | Food↔前肢/胸葉/翼 | 口接点・眼 | 大口/胸から手が生える | T01,03,04,06,09; 味/5style | prop経路/口内部/翼mask調整 |
| Gift / J25 | 低提示/胸前/片前肢assist | 足と残る肢、両前肢提示の安定 | 胸・肩・翼root | Gift↔clover/葉/翼/Wear | 品物と胸起点表現 | 支持を尾へ預ける | T03,04,06,10,13; 3profile | bounded prop/低提示/root補正 |
| 低い休息 / J05 | head低下・胸settle・翼収納 | 足/低い接触面は実物確認、尾を支持化しない | 胸/翼根/尾根 | 翼↔地面/脚/葉 | 顔・収納後の眼 | 翼折れ・胸潰れ | T02,03,06; rest/wake | 折畳み/厚み/局所corrective。Restを生成poseに固定しない |
| Signature / J03,J14,J23,J26 | 胸→顔→翼の順序、左右wing/leaf | 接地足 | 膜/枠・翼root・胸 | 翼↔horn/前肢/互い | 喜びの顔が翼に隠れる | 膜伸び・飛行追加 | T01–03,06,14; open/close/interrupt | 膜retopo/rootcorrective/clip順序。J26のみOPTIONAL |
| Secret極端 / J27 | wing-shelter peek・一側替え | 接地足、前肢は支持/助けを分離 | 翼root/顔前膜 | 膜↔眼/鼻/肩 | peek窓の顔 | 翼を硬板/顔改変 | T01–04,06,12; 無応答出口 | OPTIONAL。窓/軌跡改善、不成立なら候補差戻し |
| Wear併用 / J22,J12,J14,J20,J25 | 頭中央/首胸anchor、wing reserve | 当該支持 | 首胸anchor・翼root | Wear↔horn/翼/葉/Food/Gift | 顔・胸/clover | 翼/尾/葉へ装備root追加 | T06,09,10,13–15; 装脱＋open | anchor/asset修正。wingrootの身体構造不足はG判定 |

### J3. Pino

| 検査姿勢 / Motion ID | 能力 | 支持点 | 最大リスク部位 | 自己干渉 | 顔/接点の遮蔽 | Identity破綻 | 生成後の検査 | 修正/代替 |
|---|---|---|---|---|---|---|---|---|
| Neutral / P01,P05,P25 | compact body・足・内寄りpaw/太尾 | 接地足、低い支持面は確認。尾支持なし | 腹paw・尾root | paw↔腹、尾↔脚 | 前肢が腹に消える | 長脚/balloon尾 | T02,03,07; weight shift全view | 腹paw境界/尾rootweights、比例不良はG |
| 深い頬寄せ / P09,P12,P13 | headneck・頬・視線分離 | 足/検証済み低い支持面 | 首・頬・耳 | 頬↔肩/腹/耳 | 近眼と頬接点 | 単眼化・muzzle変化 | T01–03,07; 左右/両眼 | 眼瞼/首/局所頬補正 |
| High-five / P14 | inward pawを低く提示、look→smile | 残る支持、足/胴荷重 | 肩・腹paw隙間 | paw↔腹/顔 | 小paw提示面 | 腕伸長/指/掌 | T01,03,04,07,14; L/R | 低近target/肩weights/腹corrective |
| Food / P21–23 | 5style口、片/両paw受領 | 足と安定胴、保持中の足支持 | 口/腹/肩 | Food↔鼻/paw/腹 | 噛み/観察眼 | 口大型化/手長化 | T01,03,04,07,09; itemと各味 | item位置/サイズ/口内部・clip修正 |
| Gift / P27 | 両paw低提示/片assist/親しい確認省略 | 足/低い支持面を検証、尾支持なし | 内寄りpaw/胸腹 | Gift↔paw/腹/Wear | 視線/品物の選択 | grasp指/尾把持追加 | T03,04,07,10,13; 全3profile | 小物/保持anchor/低い提示。支持欠如はG/R切分け |
| 低い休息 / P06 | 腹局所settle、短肢/尾の重さ、wake | 足または検証済み低い接触面 | 腹・脚/尾root | 腹↔足、尾↔地面/脚 | 顔/両眼 | 胴潰れ・尾切断 | T02,03,07; descent/recovery | 腹/脚corrective・太尾連続bend |
| Signature / P03,P16,P17 | paw set/press/lift/look、原因→結果→顔 | 足＋試すpaw以外の支持 | 短い肩paw/腹 | paw↔腹/target | 試行接点と眼 | 腕を伸ばして第一案に合わせる | T01,03,04,07,14; 第一案と同reach内代替 | 局所修正/target移動。第一案のみ不成立なら別の可愛い探索案へ |
| Secret・尾/wink / P04,P28,P29 | 太尾を見る/片瞼wink/prop roll-stop-retry | 足支持、尾は操作器具にしない | 首尾連鎖/眼瞼/paw | 尾↔脚、prop↔paw | 反対眼/試行接点 | 片眼を省略/把持尾 | T01–04,07,12; 各OPTIONAL profile | 候補差戻し可。必須両眼/尾root/短肢は保持 |
| Wear併用 / P24,P03,P14,P22,P27 | 頭/首胸anchor、workface/pawを解放 | 当該支持 | 耳/首/前腹 | Wear↔paw/食物/Gift/耳 | 両眼・作業接点 | 尾/limb装備化 | T07,09,10,13–15; 試行＋装脱 | anchor/asset/重なり、作業域を守る |

### J4. Shushu

| 検査姿勢 / Motion ID | 能力 | 支持点 | 最大リスク部位 | 自己干渉 | 顔/接点の遮蔽 | Identity破綻 | 生成後の検査 | 修正/代替 |
|---|---|---|---|---|---|---|---|---|
| Neutral / S01,S02,S24 | plush局所・短肢/足、花なし成立 | 接地足/検証済み低支持面。Neutral未決定 | 腹/腿/足境界 | 腹↔脚、束↔腹 | 顔/前paw | 立位長脚化/座位固定 | T02,03,08,14; 花有/無、姿勢移行 | 腹脚retopo/pose候補QA、HumanがNeutral選定 |
| 深い頬寄せ / S08,S11,S12 | 頬L/R・headneck・plush局所 | 足/低支持面と胴荷重 | 首/頬/耳・冠root | 頬↔胸/束、冠↔耳 | 眼/頬接点 | 顔扁平化・冠身体化 | T01–03,08; 左右/花有無 | 局所頬/首/冠asset修正 |
| High-five / S13 | 短い片paw低提示、残る温かさ | 足/低支持面と残る肢、尾に依存しない | 肩/腹paw | paw↔束/腹/頬 | 小paw提示面 | 長腕/浮足/束瞬間消失 | T03,04,08,13,14; L/Rと束競合 | 低近target/保持物退避状態、肩/腹corrective |
| Food / S20–22 | 5style口・頬、束と別受領 | 足/検証済み低姿勢支持 | 口/短肩/腹 | Food↔束/鼻/paw | 口接点/眼 | 口大型化/脚延長 | T01,03,04,08,09,13; 束有無/各味 | item/保持順序/内部修正。束なし通常能力も検査 |
| Gift / S26 | 両paw低提示/空いたpaw/近い支持優先 | 足/低支持面、保持中の荷重 | 腹・両paw・束root | Gift↔束/Wear/腹 | 提示品/顔 | 三本目の手/束融合 | T03,04,08,10,13; 各3profile | put-down等の候補状態をHuman選択、clip/anchor補正 |
| 低い休息 / S02,S05 | 座る/低くsettle対応、足裏区別・回復 | 腹/臀等を使う場合は実物で接触確認、足の役割も追跡 | 腹/腿/短脚/足 | 腹↔脚/地面、束↔足 | 顔が腹/束へ埋まる | 腹脚足の一枚板化 | T02,03,08; 座位候補→起きる、足裏 | 局所retopo/体積corrective。広域融合はG差戻し |
| Signature / S02,S04,S09,S15,S27 | 選んだ快適さ・groom・局所plush | 接地/低支持、groom片paw時残存支持 | plush/短肩/耳 | paw↔頬/冠/束 | 顔喜び/触れる点 | 全身ゴム化/花必須化 | T01–04,08,13,14; 花なしを含む | 地域圧縮/保持mask/演技。S27だけOPTIONAL |
| Secret極端 / S28 | bouquet-under peek/片頬開放 | 足/低支持面＋束を保持する肢 | 両paw/顔前の束 | 花↔眼/頬/冠 | peek窓の眼 | 束と顔が一体/長腕化 | T01–04,08,12,13; 二profile/退出 | OPTIONAL。束asset/窓/近い位置。候補差戻し可 |
| Wear併用 / S23,S08,S13,S21,S26 | earouter/首胸anchor、冠と束の所有分離 | 当該支持 | 耳/冠/胸anchor | Wear↔冠/束/Food/Gift | 顔/頬/paw | 無断headtop装備/冠消去 | T08–10,13–15; 冠/束有無と装脱 | asset/anchor/state修正。headtop交換は専用仕様待ち |

## K. Face / Touch / Contact / Support Requirements

### K1. 顔の能力と制御の分担

- **MUST / G:** 眼の大きさ・形・間隔・顔への収まり、鼻口元の体積、口縁/開閉余地、頬の量、左右の可視構造をCanonicalに合わせる。閉じた口の絵から巨大な口を追加する方針は不可。後方/奥眼/側面も立体として成立する。
- **MUST / R:** gazeをhead回転から分離し、眼と瞼L/R、口/頬、耳/付属、body/limbを独立に組み合わせる。瞬き/半閉眼/閉眼、嬉しさ・安心・期待・驚き・不満を既存の小さな顔で出す。人間眉/長指/大歯列を表情の必須構造にしない。
- **MUST / M:** 表情の立上り/保持/解放とhead/bodyの因果を組む。口使用中のconsumeとTouch ACKは同一mouth channelを奪い合わず、眼・頬・耳・headの小さな応答へ振替えられる。食べるclipを瞬断して完了/消費を偽装しない。
- **SHOULD / R/M:** 非対称の微表情、眼球/瞼の接触補正、表情の奥行き可読性。P28の「wink演技」採用はOPTIONALだが、両眼/瞼L/R能力はMUST。Carol FINALの顔12state/耳10stateは演技集合であり、同数のMorph/Boneを指定しない。
- **UNKNOWN / T01,T14,T15:** 必要開口、眼窩/瞼方式、内部/舌の実装、極限域での顔可読性、消費中ACKの見え方。通常表情＋blink＋gaze＋head傾き＋接触圧縮を同時に試し、単独表情の成功だけでPASSにしない。

### K2. 接点は変形するowner上の意味領域

| 接点群 | Gで守るもの | R/Mで追加するもの | 禁止する解決 / 要実物検証 |
|---|---|---|---|
| 頭頂/額/頬L/R | 顔を隠さない面、首/頬の体積 | owner追従のsemantic region、頬局所圧縮、head向きと安全なrelease | 世界座標固定のmarkerだけで接触判定しない。T01,02,14で左右/近い視点 |
| 胴/胸/Carol front-fleece | 接触可能な身体面と所属 | 地域follow/局所soft response、胸感情と接触mask分離 | Carol macro lag禁止、Jill胸を前肢の伸縮部にしない。T05/06/08 |
| 耳root/付属root/尾root | 正しい根元と自由領域 | ownerと保護/境界応答、耳L/R/尾連続follow | Jill hornを耳rigへ誤分類しない。Pino尾を掴む装置にしない。T02,06,07 |
| 蹄/paw提示面 | 3分割蹄/丸pawの小さな接触面 | L/R target、提示/hold/ACK/release、足接地との排他 | 掌/指/腕伸長を追加しない。画面上touchは力センサの物理押圧ではない。T03,04,14 |
| Food mouth/assist | 口/鼻/paw余地、prop別所有 | 受領・bite/lick/drink接点、残量/移動、taste/release | body anchorへ固定したitemで食べたと見なさない。T09 |
| Gift/Secret/Wear | 身体ownerの面とclearance | graspでなく安全な低保持、移管/解放、pocket/anchor | propと身体の永久融合禁止、消失を解除の代わりにしない。T10,12,13 |

接触面はhard/softを分ける。蹄/propの形を圧縮で変えて接点をごまかさず、頬/fleece/plushはownerを保つ局所変形とする。足ロック/target拘束/IK/FK/補正Morphは**候補方式**であり、現在のRigへ搭載済みではない。離れたtargetへ無限追従せず、届く範囲への誘導/境界応答/解除を設計する。左右のtargetは対応する肢/頬で受け、急なside swap時は接点解除→荷重/向き変更→再提示を可能にする。

### K3. 支持と重層

**MUST:** 片前肢提示の前に荷重を移し、残る支持点とbodyがつながる。両前肢保持時は足/検証された低姿勢支持で全身を保つ。足の接地保持、関節のvolume、低姿勢への入出、tail重量の連続性をT03で検査する。Carolの4蹄/片蹄提示時3蹄を除き、画像だけで支持面/重心の実数を確定しない。Jill/Pinoの尾を新しい支えにせず、Shushuの座位もNeutral固定にしない。

**MUST:** Q14は全Familyに適用する。Living＋表情、Touch＋体重移動、Wear＋Signature、Food＋小ACK、Gift＋保持競合、Secret＋通常入力、foreground復帰を、現在姿勢からつなぐ。支持/owner/口/手の役割を再計算する位相と、安全にclipを中断できる位相を分ける。毎回Neutralへsnap、足滑り、prop teleport、形状が戻らない圧縮は禁止。連続撫での快感増加/飽和は演技/状態の変化であり、Morphを無制限に積み足さない。境界/拒否/回復も同じ身体能力で、痛み/罰の新しい演出を追加しない。

**UNKNOWN:** 可動域、reach envelope、安定支持姿勢、許容圧縮、接触中の画面可視領域、blend envelope。実物で許容域と失敗域を記録し、Canonicalと必須演技が両立しない場合はHumanへ戻す。

## L. Food / Wear / Secret / Gift Dependencies

### L1. Food 5 stylesと消費契約

共通FamilyはC26/J20/P22/S21。C25/J19/P21/S20のnotice/choiceから入り、C27–32/J21/P23/S22のtaste/afterglowへつなぐ。方法が違ってもinventory transactionを演技のbite回数から独立させる。

| style | G条件 | R/M能力 / 接点 | 生成後必須確認 |
|---|---|---|---|
| SMALL_ONE_BITE | 小口/鼻口元を保ち一口の接点面 | 近い受領→bite→口内/残物終了→taste。paw assistは個体に応じる | 顔/口の大きさ、物体が鼻/頬を通らない、消費一回 |
| MULTI_BITE | 閉開反復で崩れない口縁/頬 | 複数bite、残量と手/口の経路、途中のTouch ACK/中断 | 各biteでも在庫はitem一個分、途中退避/復帰で二重消費なし |
| LICK | 鼻口周辺と舐める面の余地 | 小さい口/舌または許容される接触表現、item保持と短い接触 | 既存顔のまま「舐め」が読めるかUNKNOWN。舌の長さ/数を固定しない |
| DRINK | mouth/受領面と容器等のclearance | 口との持続接点、顔傾き、必要なら小assist。容器/液体方式は未確定 | 鼻が埋まらず、飲む行為と残量/終了が読める |
| LARGE_EAT | 口を巨大化せず大きい物へ接近する余地 | bounded item、近いbite位置、保持/食べ進め/残物表現 | 短い肢・支持・顔可読性と両立。item寸法/具体方法は実物決定 |

Taste **1はpre-consume拒否、在庫不変**。Taste **2–5はconsume後、在庫−1**。multi-biteでも−1は一個分。拒否/受領/消費確定/中断/再開に意味的eventを持たせるが、確定nodeを今固定しない。Food中に口を使うACKを上書きしない。clipだけで在庫/Collectionの成否を判断しない。T09/T14で5style×個体、拒否とtaste段階、holding競合、復帰を確認する。Moon MacaronはCarolの既存SMALL_ONE_BITE→favorite反応→motif accentを保持し、食物とWearのanchorを混同しない。

### L2. Wear / Motif

**MUST:** 一度に1 Wear、永久所有と装着状態は別。C02/C05/C33/C37、J22/P24/S23を中心にnotice/equip/joy/remove/current-pose settleを支える。C節で追加したQ10は能力上の依存であり、Phase 3の演技採用を昇格させない。

| 個体 | 安全anchor候補（既存契約内） | 可動と除外領域 |
|---|---|---|
| Carol | head / ear-root / front-fleece。Dream Star Broochはfleece_front | head-owned/torso-ownedを跨ぐ固定結合を避ける。耳・頬・C39pocket・C40蹄・C46revealを検査 |
| Jill | 頭中央 / 首胸 | horn/首の向き/胸感情、翼open/closeを確保。翼/尾/葉は装備先にしない |
| Pino | 頭 / 首胸 | 両眼、短いpaw、試行workfaceを解放。肢/尾に装備しない |
| Shushu | earouter / 首胸 | 冠/束と別所有。headtopは専用の冠交換仕様が承認されるまで通常anchorにしない |

ownerへ追従するanchor、装備assetの自前の位置/形、衝突reserve、表示/非表示/交換時の自然な継ぎ目をR/Mで追加できる。材質だけで大きな装飾体積を代用しない。正常な身体を、単一Wearの寸法不適合だけで再生成しない。Wear外した身体でもCanonicalの可愛さを満たす。T10/T14は単独equipだけでなくJ節の重要Motion併用を含む。

### L3. Secret / Gift / 花束

- **Carol SecretはFINAL保持:** C43 Moon Ballは所有済み、BOTH、cooldown 60–120s、額/頬nudge。C44 Star Peekは所有済み、BOTH、cooldown 75–150s、L/R/front pocket。C45 HidePeekは所有済み、BOTH、cooldown 90–180s、最大2turn/1side swap、propなし。これらは能力/形状条件だけでなくWAIT・解放・通常入力への出口も必要。数値は既存FINALの契約値であり可動域の新規推定ではない。
- **J27/P29/S28はOPTIONAL候補:** 翼窓/roll-stop/束peekの成立証拠とHuman採否待ち。未成立を理由に翼/短肢/顔を改変しない。P04/P28/J26/S27の拡張も同様。C40 rareはE節どおり保持。
- **Gift共通:** C46/J25/P27/S26は別物体の保持→可視提示→移管が身体から追跡できること。移管確認の後でCollection/所有/eventを確定する。itemを身体に埋め込んだまま「贈った」としない。no-response時の保存/再提示/timeoutや確定nodeはUNKNOWN。
- **C46:** AUTO_ONLY、ultra-low、fleece reveal/cheek push/rare low hoof assistの3profileを支える。付与時点未確定。C43等の所有条件と混同しない。
- **Shushuの束:** head-owned花冠と保持物の花束は別。S02/S04/S09/S18等で既存束を保持/退避する能力をQ13で扱うが、Gift発生を追加する意味ではない。Food/High-five/Giftで手が足りない場合は「安全に置いて後で取る」「一方の手を空ける低い保持」「一旦外部presentationへ移す」の**候補**を比較し、Humanが操作契約を決める。body比例を伸ばす/第三の肢/束teleportは禁止。
- **UNKNOWN:** 持てるitemの寸法/重さ表現/数、両paw保持の到達域、束の退避先と所有event、Gift no-response、候補Secretの採否。T09/T12/T13/T14で検証し、状態契約未決定とmesh欠陥を分ける。

## M. Generation Pose / Rig Rest / Game Neutral

| 姿勢 | 目的 / 誰が決めるか | 要求 | 今の確定範囲 / 未決定 |
|---|---|---|---|
| Tripo Generation Pose | 画像から身体構造を読むための入力姿勢 | 各viewが同じ身体/姿勢で、顔/両肢/翼root/尾root/接合が分かる。隙間とCanonical比率を両立 | 登録2D参照とpose DRAFTあり。Tripo slot/生成適合は未検証。腕を開く量等の旧数値は仮説 |
| Rig Rest Pose | bind/weights/関節軸/変形を設計する技術姿勢 | 肩/首/脚/翼/尾のownerとbend経路を確保。mesh/skin/bind transformの整合 | 技術担当が生成モデルから決める。Generation姿勢と異なってよい。変更時は形状/weights/export再確認 |
| Game Neutral Pose | 日常に自然に生きる姿勢 | 個体らしい支持/呼吸/顔、現在姿勢からinteractionへ入れる | CanonicalはIdentity基準。Pino/ShushuのCanonical座位/低姿勢をそのまま唯一Neutralに固定しない。Human視覚判断待ち |

三姿勢の一致はMUSTではない。生成姿勢で綺麗な隙間があることはRig時の可動保証ではなく、Restを変えるだけでも広域融合は治らない。Game姿勢へ移したときに首/腹/短脚/翼/太尾が成立するかが受入条件。既存pose DRAFTの角度/開き幅/座標は検証前の制作案としてのみ扱い、骨数/関節限界/本タスクの確定契約へ転用しない。

Body-only 2DのHuman受入は「入力画像としての受入」。Canonicalを置換せず、現在のTripo Preflight完了や3D/Rig/NeutralのHuman承認を含まない。登録済み15枚とCarolのBack不使用方針は、O節および§Tの2026-10-11更新で扱う。

## N. Tripo-First / Blender-Fallback Production Strategy

### N1. 工程別の投入物と出口

Tripoの現在の機能/対応Rig/価格/プラン制限は本タスクで確認していない。下表は「期待する出力/検査」であり、機能提供の事実表ではない。現在値を使った選定/購入/生成は行わず、Studioで観測する項目を固定する。

| 工程 | 欲しいもの / 次へ渡す条件 | 不足時の判断 |
|---|---|---|
| 1. Multi-view 3D generation | Oの入力slot/pose照合後、顔/短肢/接合/固有付属を保ったbody mesh/texture候補 | slot機能・必要枚数・camera解釈はUNKNOWN。入力矛盾を直す前に反復生成しない |
| 2. Shape / Identity evaluation | Canonicalとのfront/side/back/3/4比較、G要件とJの変形余地のscreening | off-model/広域融合は入力/生成へ。未Rigの見た目検査だけで可動PASSにしない |
| 3. Topology / Mesh correction | owner領域、口/眼/首/肩/腹/翼/尾の変形可能な面と接合 | topology品質はUNKNOWN。局所retopo/分離/厚み/UV/材質をC/Dで補正、主要構造欠落はI2 |
| 4. Auto Rig | 非標準体型の頭/胴/左右肢と、必要ならwing/tail等のroot、skin/bind/weightsの候補 | 対応生物型/付属部/morphはUNKNOWN。誤認はまずRigを修正/独自制作。正常meshを捨てない |
| 5. Preset Motion | 原形を保った小weight shift/呼吸/settle等の利用候補 | 対象Rig/retarget/clip編集可否UNKNOWN。名前が類似してもQ能力/支持/owner未達なら不採用 |
| 6. Text-to-Motion | 具体target/支持/表現順序を満たす動作候補 | 非標準短肢/蹄/翼/雲/propへの適合UNKNOWN。単発clipでContact/WAIT/解除を満たすと仮定しない |
| 7. Blender補正/追加 | C:出力の局所形状/Rig/clip修正。D:個体表情/接触corrective/prop/不足Rig/独自演技 | 任意のrig方式。owner/Canonicalを守る。主要比率まで作り直す場合はHumanと再生成比較 |
| 8. GLB/glTF Export | skin/morph/material/clip/node/propの必要情報を、Pの実行環境で再現 | constraints/driver等の作者側依存を必要に応じbake/移植。export成功だけでruntime同等としない |
| 9. PlayCanvas / Smartphone QA | J/Tの受入、商品/入力/重層/復帰、顔可読性、実機負荷 | 可愛い顔/固有付属/必須能力を守ってmeasure→修正。未実装/未実測をPASSにしない |

Tripoに最初に期待するのは**Canonicalに沿う立体の身体と、後工程で変形できる接続/面**。Auto Rigは骨格/skinの出発点候補。全130行の実装、全408演技、Contact transaction、個体らしい表情、owner-aware局所fleece/wing/plush、ゲームの割り込みは独自設計を要する可能性が高い。これは能力契約からの推論で、現在のTripoの不可/可の断定ではない。

### N2. 能力から制作ルートへの暫定分類

**A=Preset候補、B=Text-to-Motion候補、C=Tripo出力のBlender修正、D=Codex＋Blender独自制作、?=Studio適合確認。** A/B/C/Dは排他的でなく、shape→Rig→clipの段階で併用できる。下表とC/Dの逆引きで全Familyにルートを引ける。**全A/Bは?付き、未採用**。

| 能力 / 対象Family | 暫定ルート | 候補で済まない個体要件 / 最小の確認 |
|---|---|---|
| Q01 顔 / 全130の継承 | C/D + ? | 眼瞼/視線/小口/頬/感情の独立性、非対称、身体との併用。顔Rig/morph/出力clip対応を確認 |
| Q02 headneck / 全130 | A?/B?→C/D | 汎用turnは小注意の候補だけ。低額/深頬/短首/顔可視に適合するか |
| Q03 支持 / 全130 | A?/B?→C/D | 小weight shift/rest候補。非標準支持肢、footlock/低姿勢/両手保持を自動保証しない |
| Q04 forelimb / C07,C16,C18,C26,C40,C46ほかD逆引き | B?→C/D | 低target/短肢/蹄paw/片肢支持。標準human high-five clipの置換採用不可 |
| Q05 Carol fleece / C01–C46 | C/D + ? | owner zero lag、顔opening/頬圧縮/pocket、局所/broad用途を独自構築候補 |
| Q06 Jill wings/胸/葉/尾 / J01–J27 | C/D、限定B? | wingrootと膜、胸始動/顔窓/葉所属。wing/tailをAuto Rigが認識するか実見 |
| Q07 Pino compact/尾 / P01–P29 | C/D、限定B? | 内寄り短paw、腹との隙間、太尾連続bend、両眼。P03第一案と代替のreachを検査 |
| Q08 Shushu plush/脚/花 / S01–S28 | C/D、限定B? | 腹腿足区別、局所圧縮/低姿勢、冠/束の別所有。支持/短肢を保つか |
| Q09 Food / C25–32,J19–21,P21–23,S20–22 | B?→C/D | 5styleの接点/残量/口ACK/在庫確定はclip名から推定不可。prop相互作用の出力方式確認 |
| Q10 Wear / C02,C05,C10,C33,C37,J22,P24,S07,S23 | C/D + ? | owner anchor、装脱/current-pose、Signature可動/1Wear。attachment/node/exportを確認 |
| Q11 session / C34,J24,P26,S25 | D + ? | 現在姿勢/状態/prop復帰。一般入場clipでは状態整合を保証しない |
| Q12 Secret / C43–45,J27,P29,S28 | B?→C/D | nudge/peek/roll/WAIT/side/退出、prop所有。J/P/S候補はOPTIONAL |
| Q13 Gift/保持 / C46,J25,P27,S26 + S02,S04,S09,S18の保持再利用 | C/D、限定B? | 移管event、低保持、束競合/解放。補助保持とGift演技を区別 |
| Q14 重層/割り込み / 全130 | C/D + ? | 顔/口/支持/propのphase、mask/現在姿勢、安全復帰。複数clip/追加表情のexportと実行可否 |
| Q15 fullspatial/export/mobile / 全130 | C/D + ? | 360°立体/非Hero、skin/morph/material/clip/axis/実機。Studioプレビューと同等か |

### N3. 次回Studioで必要な最小観測

1. UI上のmulti-view入力枚数/slot名/実camera向き/pose条件。画像側のleft/rightとcamera側を別記録し、Jill Rightのcamera slotとCarolの3視点入力対応を確認する。
2. 生成出力のmesh分割/接合/topology/裏面/口眼内部/texture、download形式と再編集可能性。
3. Auto Rigが4体の体型/付属をどう分類し、実際のroot/chain/weights/bindをどう出すか。翼/太尾/短肢/fleeceは部分ごとに確認する。
4. Preset/Text-to-Motionの実際の利用条件、target指定/prop/clip編集/retarget/複数clip出力。A/Bを採るなら該当Tの証拠が必要。
5. GLB/glTFにskin/morph/素材/animation/nodeをどこまで保持できるか。制約/価格/Credits/plan/再試行費はその時点の表示から記録。
6. 入力不足と生成の失敗、shape正常とAuto Rigの失敗、任意clipの不成立を別々に記録し、同じ問題への無目的な再生成を避ける。

上記は次工程の確認仕様であり、今回Studio操作/課金/生成を許可する指示ではない。現行機能・費用を前提にした数値予算/回数を本書で発明しない。

## O. 3D Input & Multiview Preflight Checklist

### O1. 登録と本書での直接観察

**Historical Phase 4 observation:** この節の画像状態・Jill right・Carol Backに関する記述はPhase 4時点の記録。現在の入力選定は§Tの2026-10-11 Post-Phase-4 updateが優先する。

画像のリンクは**現在の既存asset**。canvas/背景/向き/姿勢のscreeningは本タスクの観察に限り、画像の再編集や既存Registerの改訂はしていない。各個体のfront/left/right/backは画像側の名称である。

| 個体 | 入力 | 登録状態 | 直接観察 / Motionへの影響 | Preflight判定 |
|---|---|---|---|---|
| Carol | [Front](../../../assets/grimo/source/carol/tripo-generation-pose/carol_bodyonly_front.png), [Left](../../../assets/grimo/source/carol/tripo-generation-pose/carol_bodyonly_left.png), [Right](../../../assets/grimo/source/carol/tripo-generation-pose/carol_bodyonly_right.png) | 3/4、2D受入済み。Back未登録 | 正面/側面の雲・短い蹄は読める。後方接合/尾/後蹄/背面fleeceの同一性は3枚だけで確定不可。C07,C15,C16,C40,C46とFull-Spatialに影響 | TRIPO_PREFLIGHT_PENDING。Backは入力解決待ち、3枚で投入できるかもUNKNOWN |
| Jill | [Front](../../../assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png), [Left](../../../assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png), [Right](../../../assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png), [Back](../../../assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png) | 4/4、2D受入済み | **right名の画像もscreen-leftを向き、leftと同方向に見える。** RegisterのOpposite/right解釈との矛盾。front胸cloverは可視参照から欠ける。wing/root/horn/葉/尾の復元を妨げ得る | TRIPO_PREFLIGHT_PENDING、slot対応は**HOLD**。ファイル名を根拠にOppositeへ投入しない |
| Pino | [Front](../../../assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png), [Left](../../../assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png), [Right](../../../assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png), [Back](../../../assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png) | 4/4、2D受入済み | 立位入力とCanonicalの低い姿勢で見える脚長/腹pawの関係が違う。長脚化とは断定しない。足裏、内寄りpaw/尾rootの隠れ面は不確定 | TRIPO_PREFLIGHT_PENDING。P03/P14/P22/P27とrestの短肢reachを検査 |
| Shushu | [Front](../../../assets/grimo/source/shushu/tripo-generation-pose/shushu_bodyonly_front.png), [Left](../../../assets/grimo/source/shushu/tripo-generation-pose/shushu_bodyonly_left.png), [Right](../../../assets/grimo/source/shushu/tripo-generation-pose/shushu_bodyonly_right.png), [Back](../../../assets/grimo/source/shushu/tripo-generation-pose/shushu_bodyonly_back.png) | 4/4、2D受入済み | 花なし身体は読めるが、立位入力から腹/腿/足裏/低い座り方を断定不可。Canonicalのplush/短肢/花所有の再現が必要 | TRIPO_PREFLIGHT_PENDING。S02/S05/S13/S21/S26の低姿勢/保持検査 |

全体でfrontの開いた前肢と側面の下がった前肢は、projection差か姿勢差かをslot照合時に確認する。2D観察だけで正確な関節角/同一poseの合否を決めない。canvasサイズ/余白も異なるため、原assetは保持したままStudioでのscale/center/camera対応を検証する。見えない足裏/内部は「存在しない」と推定しない。左右の名前と画面上の向きが一致していてもTripo cameraの意味は別確認。

### O2. Preflight完了に必要なチェック

- **Authority:** CanonicalとBody-onlyの用途を分ける。最新Register/Carol State/承認済みvisible参照を同一時点で照合。Normal review pendingを最終受入と誤読しない。
- **slot:** view画像の実向き、Tripo slot/camera向き、前後/左右の対応を記録。Jill Rightは2026-10-11の新しいscreen-right原本へ差し替え済み。実slot/camera対応はStudioで確認する。Carolは三視点対応を確認し、非対応ならHOLD。
- **同一個体/pose:** 頭/胴/肢の比率、眼/口/耳またはhorn/翼葉/尾/蹄、支持、露出した接合、marking、背景/scale/cropを照合。見え方と実pose差を区別する。
- **body-only:** 冠/束/prop/通常Wearがbodyと融合していないか、除去跡で身体が欠落していないか。別asset候補の所有を確認。
- **critical anatomy:** 首/頬、短肢root/腹の隙間、支持面、口/眼、Carol faceopening/下雲/尾、Jill wingroot/膜/葉/太尾、Pino内paw/太尾、Shushu腹腿足をG条件でscreening。
- **出力検査計画:** C/D/J/Tと検査視点、再生成vs局所修正判定を添える。費用/入力対応/出力Rig等UNKNOWNをStudioの現行表示で解決する。入力受入が揃うまでTripo Readyと呼ばない。

### O3. 追加/修正参照の提案（未作成・未承認; Phase 4 snapshot, current Carol decision superseded by §T)

| 提案 | 目的 / 影響Motion | 追加が必要になる条件 |
|---|---|---|
| Carol Backの正式登録候補 | 後蹄/尾root/背面fleeceとowner、C07/C15/C16/C40/C46・Q15 | 既存Register未登録を解決。正しい既存参照の有無とHuman受入、または限られたviewでの根拠ある生成方針を決める |
| Jill真のOppositeの照合/修正候補 | 左右wingroot/膜/前肢/葉/尾、J03/J07/J12/J14/J20/J25/J27 | rightが同方向という矛盾を解消する資料がない場合。鏡像作成を自動の解決にしない |
| 口/鼻口元の近い複数view | 全4体のFood5style、顔T01とC43額頬nudge | 出力が平面口/内部欠如で局所修復の形を決められない場合。口を大きくする参照ではない |
| Jill wingroot/収納/裏面の斜め参照 | J03/J05/J12/J14/J25/J27 | 既存viewでroot/膜/葉の区別が曖昧で誤融合の原因になる場合 |
| Pino/Shushuの足裏・腹短肢/低い支持参照 | P03/P05/P06/P14/P22/P27、S02/S05/S13/S21/S26 | 既存Canonical/入力/生成物で短脚/足裏と低姿勢支持を判定できない場合。新しい長脚/Neutral仕様を発明しない |
| Carol顔opening/尾の斜め、花冠/束の別所有参照 | C38/C39/C44–46、S04/S21/S26/S28 | ownerや解除後の身体を既存参照から復元できない場合。既存承認参照を優先 |

追加参照は必要条件と対象を限定した提案。全てを無条件に生成するタスクへ拡張しない。画像側のHuman受入とStudio技術Preflightの両方が必要で、今回いずれも新規PASSは出していない。

## P. Smartphone / GLB / PlayCanvas Requirements

### P1. データと実行の契約

| 領域 | MUST / 候補方式 | 要実物検証 |
|---|---|---|
| 全身/座標 | frontだけでなく3/4/側/背/低姿勢の外面、node/skin/bindの一貫性。制作座標とruntime座標を対応表で管理 | 旧pose DRAFTのaxis表記をPlayCanvasへ直輸入しない。forward/up/handedness/units/root scale、L/R、contact anchorを既知poseで照合 |
| 骨格/skin | head/body/肢/翼/尾のownerと変形をskinで表せる候補。必要chain/rootだけを設計 | Auto Rig出力、短肢/首/wingroot/tailroot、joint order/weights、clipの実行/retarget |
| 顔/局所soft | bones/morph/materialの組合せ候補。瞼/眼/口/頬/fleece/plushを独立に重層 | 同時morphの形/normal/shading、gaze/eye素材、blend処理、GLB経由の再現性 |
| 作者側制約 | IK/driver/constraint/correctiveは制作方式の候補。exportに残らない依存はclipへbakeまたはruntime相当制御 | Blender見た目≠GLB動作の可能性。拘束/評価順/非linear補正/shape animationが保持されるか |
| node/物体 | Wear/Food/Secret/Gift/花の独立所有、意味anchorとclip/event対応 | slot/node命名、装脱/移管/残量、親切替/scale、root owner。データモデルのevent実装は本タスク外 |
| material/texture | Canonical色/輪郭、眼/marking、膜裏、雲/plushのsoft shadingと接点の読みやすさ | alpha/裏面/normal/色域/light、素材切替、outlines等の方式は未確定 |
| clip/blend | 片肢支持/face/body分離、現在姿勢からの遷移、口ACK排他、WAIT/release位相 | runtime mask/clip同期、resume、物体と骨/morphの時刻整合。全130能力の再生経路は後工程 |

骨/Shape Keyの名称・数、angle limit、clip長、最終mesh密度/texture寸法、compression方式は実モデルから決める。Carol FINALの演技時間/trigger等の既存値は保持し、runtimeの都合で変更しない。PlayCanvasの具体API/コードは今回設計しない。

### P2. スマホの可読性と負荷

**MUST:** Front Heroで眼/小口/頬/低い蹄paw提示面を読み取れる。3/4/傾き/低姿勢/装飾重なりでも近眼/接点/Signatureが消えない。距離・画面比率・接触UIの見え方は実画面で確認する。Heroだけの平面化で奥面を隠さず、Full-SpatialとView-Weighted Polishを両立する。

**MUST:** bones＋顔morph＋局所soft＋複数clip＋Wear/propの同時実行、入力中/低休息/復帰を実機で測る。Xiaomi 14T Proが利用可能な実機、Pixel 7a-classはUNVERIFIED_TARGET。FPS/メモリ/骨数/総poly上限の保証は現在UNKNOWN。ロード/切替/描画/skin/morph/animation/inputのどこに負荷があるか観測し、見た目のQAと並べる。

**SHOULD:** measureに応じ、見えない補助制御のbake、局所変形の整理、素材/meshの整理、texture/compression、必要ならLOD等を比較する。Identity/両眼/短肢/付属root/必須接点を削って性能を満たす方針は不可。方式を変えた後は同じJの顔/支持/接点とT14/T15で差を確認する。最適化は実モデルが出た後の選択であり今回のasset変更ではない。

## Q. Failure Modes and Recovery Decisions

以下18件が重点failure register。Detectは将来の検査、PreventはG/R/M契約。**再生成必要かは条件分岐**であり実物なしにYes/Noを断定しない。Humanは可愛い/自然/Identityの受入、仕様変更、候補採否を決める。技術的局所修正はexecutorが進め、外見を変える修復の承認をHumanから推測しない。

| ID / 失敗 | 発生条件 | 検出 | 予防 | 再生成判断 | Blender補正 | Human判断 |
|---|---|---|---|---|---|---|
| F01 可愛いが頭が動かない | 首余地/loop/skin不足、頭胴の一塊 | T02/Jの低頭・左右深頬・解除 | 首/顔胴境界G、headneck独立R | 主要頭胴体積/首を発明し直すなら候補 | 正常shapeならloops/weights/首corrective/rig | 新しい首比率が必要、必須域と可愛さの衝突 |
| F02 笑顔で眼口崩壊 | 表情の同時加算/眼瞼/口縁不適合 | T01/T14、笑顔＋blink＋gaze＋食後 | 顔体積G、地域mask/補正 | 多viewの顔構造がoff-modelなら候補 | morph/weights/眼瞼/口縁修正 | 感情可読性と顔Identityの受入 |
| F03 High-fiveで足が浮く | 片肢提示前の荷重移行欠如/過reach | T03/T04、L/R/無応答/戻り | 残存支持/低近target/足lock | 支持肢root/足底欠落で回復困難時のみ | clip/足lock/COM/肩weights | Canon比率でも成立しない演技の変更 |
| F04 頬寄せで首頭胴破綻 | neck折れ/頬→body引きずり/隙間 | T02/J深頬、側/低視点 | 連続neck/owner/頬局所 | 主要接合誤形/比率改変必須なら候補 | 接合retopo/weights/地域corrective | 深さと可愛さ/自然さの受入 |
| F05 Carol雲の浮遊/滑走/伸縮 | shell lag/owner誤り/全身scale | T05、C38–46と呼吸/移動同時 | head/torso/tailowner、macro lag zero | 原形が浮雲列で顔/肢余地なしなら候補 | ownerweights/接合/局所soft/素材 | FINAL/Canonicalと雲の生きた質感受入 |
| F06 Jill翼root潰れ/顔肢貫通 | root融合/膜無厚/肩wing weights共用 | T06/Jopen/収納/High-five/Secret | 左右root/膜/枠と肩独立、reserve | root/翼輪郭不明・広域融合なら候補 | 膜retopo/裏面/weights/rootcorrective/clip | 翼/胸のIdentity、顔窓、Secret採否 |
| F07 Pino尾胴の不適切融合 | 尾root/自由部と脚がweb/塊 | T07、back/side＋bodyshift/tailbend | 太い連続尾rootと別自由領域 | 尾経路/体積の大規模復元なら候補 | 小web除去/rootretopo/skin | 尾の厚み/重さ/輪郭受入 |
| F08 Pino短pawで代表試行不可 | target遠すぎ/腹遮蔽/肩可動不足 | T04/T07、P03第一案と近域代替 | inwardpaw独立、低近workface | 第一案だけ不成立なら再生成しない。必須独立肢の広域融合なら候補 | target/試し方/肩/腹corrective | 第一案vs別の可愛い探索演技 |
| F09 Shushu腹脚足が一塊で座位潰れ | 腿/短脚/足裏が曖昧なmesh | T08、低settle/座位候補/起きる・足裏 | 腹/腿/足の体積区別、局所plush | 一枚板/長脚化なしに復元不能なら候補 | 局所retopo/weights/腹脚corrective | 座り方/Neutral未固定、plush可愛さ |
| F10 Food口構造不足 | 黒い口絵/内部なし/必要開口不成立 | T01/T09、全5style | 小口縁/受領面G、口ACK分離 | 内部追加が顔Identityを変えるなら候補 | 局所内部/口縁/舌候補/clip/prop位置 | 小口のまま食べ/舐め/飲みが読めるか |
| F11 Giftと保持物衝突 | 束/食物/Wear同時、空きpaw不明 | T13/T14、S26等全profile/中断 | 所有/保持/退避state、boundedprop | 正常身体＋状態問題なら不要 | prop/anchor/clip/局所clearance | 束退避/再取得、no-response/移管仕様 |
| F12 Wearが顔署名関節を妨げる | 禁止anchor/大asset/owner跨ぎ | T10とJWear併用 | 安全anchor/1Wear/可動reserve | 装飾だけ不適合なら不要。身体root異常は別判断 | asset寸法/anchor/skin修正 | 装備外見、冠交換など新規仕様 |
| F13 Auto Rigが非標準体型誤認 | 短肢/蹄/翼/太尾をstandardへ誤配 | joint/weights/bind実見→T02–08 | 出力chain/rootを部位単位検査 | Rig失敗単独では不要 | Rig/weights再構築、付属/face追加 | 方式変更より、結果のIdentity/生命感受入 |
| F14 frontとsideが一致しない | slot/同pose/scale/左右矛盾、復元誤解 | O照合→全view同mesh/顔輪郭 | Jill right HOLD、Canon/入力比率照合 | 入力不整合解決後、広域比率誤形なら候補 | 小局所/材質なら補正 | 正しいOpposite/Back/補助参照の受入 |
| F15 生成時分離がRig時破綻 | 隙間だけ正常、内面/loops/weightsなし | T04–08、肢/翼/尾/雲変形 | 自由領域と接合面G、動的clearance | 主要自由領域欠落なら候補 | 局所retopo/分離/weights/corrective | 変形しても連続した身体/可愛さ |
| F16 front可愛いが3/4低姿勢で不自然 | Hero専用平面/奥眼不足/裏面欠如 | T15/J、非Hero全view/低休息 | Full-Spatial、奥側/足底/接合G | 顔/体積の多viewoff-modelなら候補 | 局所奥面/素材/posecorrective | 全方向IdentityとFrontの魅力両立 |
| F17 必須MotionにCanon比率改変が必要 | 短肢/頬/翼等で限界、代替/補正尽きる | J/T該当、正常shapevs演技の証拠 | 形状よりtarget/支持/局所方式を先に比較 | 必須構造の誤生成なら入力修正→候補。Canon自体変更は自動判断不可 | 局所修復/演技解釈の比較まで | 必須仕様とIdentityの衝突を正式判断、無断削除/改変不可 |
| F18 morph/bones等がモバイル過負荷 | 重層/素材/skin/morph/propで負荷集中 | T15実機、単独vs組合せ・resume | 実測と必要能力に応じ構造整理 | 負荷だけで全身再生成しない。非効率mesh全体なら方式比較 | bake/制御/mesh素材/texture/LOD候補 | 最適化後の顔/付属/生命感を受入、根拠なきFPS保証なし |

## R. Unknowns / Human Decisions

### R1. UNKNOWN register

UNKNOWNは設計漏れでなく、決定者/必要証拠/次工程を指定して閉じる。Phase 3 O1–O6の未決定を引き継ぎ、Carol FINALとの照合を維持する。

| ID | 未決定事項 | 決める根拠 / 担当 |
|---|---|---|
| U01 | 実可動域/到達/接触圧縮/支持/低姿勢の安全域 | 生成mesh＋仮RigでJ/T01–08・14の成功/失敗域。技術担当＋Human知覚 |
| U02 | mesh分割/topology/骨/morph/材質の方式と数 | G screen/変形/export/負荷から技術担当。演技state数を構造数に転用しない |
| U03 | Tripo現行slot/対応枚数/Auto Rig/付属/morph/clip/Text-to-Motion/export | N3をStudio実機で観測。価格/Credits/plan/再試行費も現行表示確認までUNKNOWN |
| U04 | Carol BackとJill真のOpposite/slot矛盾、同pose/canvas対応 | Oの既存参照/登録経緯/Studio camera照合。必要なら限定追加参照とHuman受入 |
| U05 | 4体のGame Neutral、Generation→Rest→Neutralの移行 | CanonicalとJrest/Idle/短肢支持、花あり/なしを比較。Shushu座位固定なし |
| U06 | Carol通常軽前蹄交流の頻度/発動/rareとの関係 | Human。低蹄能力は準備、C40 FINAL rare trigger/cooldown/入力は保持 |
| U07 | P03第一案/別探索、J27/P04/P28/P29/S27/S28等の候補採否 | 個体らしい因果、短肢/翼/両眼/束と両立するJ/T証拠＋Human |
| U08 | Jill/Shushu特別Food/Wear、候補Secretの正式item/条件 | Phase 3のproposalは非FINAL。商品/データAuthorityとHuman、通常5Food/1Wear能力は先に必要 |
| U09 | Gift保持物寸法/束退避/移管node/no-response再提示/保存/時刻、C46付与時点 | 既存仕様で確定した所有/event順を保ち、未決定だけHuman/商品設計。clipは勝手に確定しない |
| U10 | GLB/runtimeでのbones/morph/素材/作者constraintの等価性 | P1のroundtrip/PlayCanvas再生、T14/T15。具体API/方式/性能値は後工程 |
| U11 | 画面距離/接点可読域/実機負荷/性能目標/Pixel級受入 | Xiaomi実機と未検証targetのQA、T15。根拠のない骨/poly/FPS/メモリ上限を固定しない |
| U12 | 完成mesh/Rig/演技/修復後IdentityのHuman受入 | 各gateの全view/Jclip/実画面証拠。現在PHASE_4_COMPLETEから推定不可 |

### R2. Humanが判断する範囲

- **H1:** Canonicalと承認済みvisible参照を守った顔/シルエット/可愛さ、3/4/低姿勢/表情/局所圧縮/身体の連続性、個体らしい生命感の受入。
- **H2:** C40の通常軽交流の運用、P03第一案と代替、Jill/Pino/ShushuのRare/Secret/特別itemの採否。Carol FINAL既承認項目は変更提案がなければ維持。
- **H3:** 4体のGame Neutral/休息姿勢、入力Back/Oppositeや追加参照の正式受入。2D選定と3D/Rig知覚受入は別。
- **H4:** Gift no-response/付与時点/花束退避・再取得/移管など未決定の体験と商品契約。
- **H5:** 必須MotionとCanonicalが両立しない証拠が出た場合の仕様判断、外見を変える大規模修復/再生成の比較、モバイル最適化後の魅力受入。

技術担当は具体実装/分割/骨格/retopo/clip/検査方式/局所修正の選択を進める。Human待ちを理由に設計coverageを省かず、Humanの選定を技術PASSへ代用しない。本書では未承認演技や未検証モデルの承認を求めず、次の検査で判断可能な証拠を定義する。

## S. Tripo Generation Handoff / Acceptance Gates

### S1. 次工程に渡す入力

1. BのCanonical/最新visible Authority/Carol FINAL/商品・データ正本と、本書CのID→能力/Variant差、Dの逆引き、Jのstress、Qのfailure判定。
2. 既存Body-only Register/15枚とGeneration Pose DRAFT。OのCarolの3視点入力対応UNKNOWN/Jill Right差し替え/同pose/slot/canvas/足裏等の不確定を明示する。
3. N3のStudio観測票に必要な項目、A/B/C/D/?の未採用候補、U/Hの未決定一覧。生成担当が独自に「Tripo Ready」と推定しない。
4. 各出力について、入力/slot/設定/出力識別、修正内容、該当Motion/Q/T、検査画像/clip/実画面、技術結果とHuman結果を分けて記録する。証拠保存の具体ファイルは次タスクで決め、本タスクで補助成果物を増やさない。

### S2. 受入gate（今回いずれも未実施）

| Gate | 次へ進む条件 | HOLD/FAIL時 |
|---|---|---|
| G0 入力/Studio Preflight | Canonical/補助参照/slot/左右前後/同poseの照合。Carol 3視点対応の確認とJill Rightのslot照合。機能/出力/費用条件を観測し、必要なHuman入力受入を得る | 入力/現行機能UNKNOWNを解消。登録枚数だけで生成受入にしない |
| G1 生成shape/Identity | 全viewで顔/比率/短肢/付属root/口/眼/自由領域のG条件をscreen。HumanがIdentity/可愛さを評価 | Q/Iの局所修復vs入力修正/再生成。Human review pendingをPASSにしない |
| G2 topology/Rig能力 | Jの9カテゴリ以上/個体を試すための独立制御、支持、局所面/根/接合が揃う。T01–08の実結果と不成立域を記録 | 正常形状ならR/C/D修復。主要構造欠落ならG1へ、Canonとの衝突はH5 |
| G3 Motion/接触stress | C全130の必須能力＋profile限定差を実物で照合、T14の組合せ/左右/入出/解放。OPTIONALは採否を分離 | clip/target/corrective/支持修正。候補不成立で必須Identity改変不可 |
| G4 商品/所有/状態 | T09–13、Food5style/5tasteと消費、1Wear、Secret/WAIT/出口、Gift移管/束競合、foreground復帰が一致 | 実装/商品未決定と形状失敗を区別。必要Human仕様判断へ |
| G5 export/runtime/スマホ | T15、GLB/PlayCanvasで作者側の顔/支持/局所変形/物体/clip同等、非Hero可読性、実機負荷測定 | export/bake/素材/重層/構造最適化と再QA。数値性能は実測から |
| G6 知覚最終受入 | 各個体がCanonicalの魅力とらしい因果/触れ合い/生命感を保ち、必須能力とQA証拠が揃いHumanが承認 | 技術PASS単独で完成にしない。未承認候補は本番契約へ昇格しない |

gateは責任/証拠の境界であり、順序を硬直させる制作方法ではない。shape修復とRig検査の反復やC/D選択を許すが、入力矛盾/Identity FAILを後段の成功で覆い隠さない。今回の成果は**設計handoff完成**で、G0–G6はPENDING/UNKNOWN。

### S3. Phase 4 coverage / 完了判定

| 個体 | Family | profiles | MUST能力対象 | OPTIONAL能力対象 |
|---|---:|---:|---:|---:|
| Carol | 46 | 156 | 46 / 156 | 0 / 0 |
| Jill | 27 | 81 | 25 / 77 | J26/J27: 2 / 4 |
| Pino | 29 | 86 | 26 / 80 | P04/P28/P29: 3 / 6 |
| Shushu | 28 | 85 | 26 / 81 | S27/S28: 2 / 4 |
| **合計** | **130** | **408** | **123 / 394** | **7 / 14** |

MUST/OPTIONALは採用能力の要求区分。Jill/Pino/Shushuの具体演技はDRAFTであり、MUST行数は正式演技承認の件数ではない。OPTIONALでも両眼/短肢/翼root/支持/通常顔等の共通MUSTを削らない。

重点監査を実施済み。Phase 3の全ID/各V/重点QとCの130行を機械照合し、欠落/重複/V不一致/元の重点Q欠落は0。個体別46/156・27/81・29/86・28/85、合計130/408が一致した。全408profileの列挙をFamily共通能力と最終列/Lの追加差に照合し、D逆引きも一致した。G/R/M/T分離、Jの全4体9カテゴリ以上/計38検査姿勢、18failure、pose分離、入力HOLD/未知、Carol FINAL保護を確認した。表の列数不整合/既存参照リンク切れは0。変更対象は本書だけで、正式資料/画像/3D/アプリの変更なし。**coverageは設計の対応完了であり、408profileの実物成立証明ではない。**

**PHASE_4_COMPLETE / DRAFT / HUMAN_REVIEW_PENDING。** 次は明示された別タスクでG0のTripo Preflightを行う。本タスクは本書の重点監査・commit/push後に停止し、モデル/Rig/clip生成やPhase 5へ進まない。


## T. Post-Phase-4 Human Decision / Input Update (2026-10-11)

This update records current input decisions after Phase 4. The direct observations in O1 above remain the Phase 4 snapshot. Where that historical snapshot or any earlier handoff text describes Carol Back or Jill Right as unresolved current work, this section supersedes that interpretation. The Phase 4 Motion/Anatomy/Rig Capability contract and its historical observations are unchanged.

1. **Jill Right replaced:** The former Right image faced screen-left like Left. It is excluded from the current set (old SHA-256 `f745cbd01b8224b45354e9c3f1621b4668f51cc00df3cfc9287deda415ef019a`). New original `ChatGPT 画像 2026年10月11日 18_08_13.png` (1145×1374; SHA-256 `9572b69c0bbbe66eda9ef2e1011f8f0e040126b3d84cec10446da47a9233c9dc`) is registered as `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png` and faces screen-right. Jill's selected input is updated; camera-slot interpretation and technical preflight remain unverified.
2. **Carol Back intentionally omitted:** Human decided not to create or use a Carol Back image after repeated generated candidates failed lower-body taper, hoof-shape, and three-dimensional-connection quality. Use approved Front, Left, and Right as the planned Tripo inputs if supported. This decision does not claim accurate reconstruction of unseen rear anatomy.
3. **Studio support unknown:** Current Tripo support for three-view input and its camera-slot mapping have not been checked. If three views are unsupported or a required slot prevents this input plan, hold and decide the next input method separately. No Tripo operation or Credits use occurred in this update.
4. **Readiness:** All 15 registered images remain `BODY_ONLY_REFERENCE_ACCEPTED`; technical Tripo preflight remains `PENDING`. This update does not declare Tripo Ready or Rig Ready.
