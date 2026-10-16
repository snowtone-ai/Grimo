# Grimo — Complete Three-Character Motion Architecture DRAFT

**Date:** 2026-10-11
**Status:** PHASE_3_COMPLETE / DRAFT / HUMAN_REVIEW_PENDING
**Scope:** Jill / Pino / Shushuの全Motion Family、演技、接続、身体能力要求。Phase 4の詳細Anatomy/Rig設計・実制作は未実行。
**Source revision:** `fd91fe527cceaa62df116cb6ebc43d078d0650cd`
**Branch:** `codex/grimo-motion-zero-based-design-20261011`

COMPLETEは文書設計の完了。Phase 1・2と本書の新提案はHuman未承認であり、FINAL、Human知覚PASS、実機PASS、DESIGN_READY、TRIPO_READYを意味しない。正確な秒数・角度・変形量・通常座位・制作方式は未決定。台詞のような説明は動機の比喩であり、音声やUI追加仕様ではない。

## A. Motion Design North Star

**触れ合って可愛く癒され、その子が自分から関わってくれたことを嬉しく感じ、また会いたくなる。** 個性はこの体験を豊かにするためにある。Pinoを探究の演技だけ、Shushuを静止だけに閉じ込めない。3匹とも撫で、頬寄せ、遊び、はっきりした喜び、ハイタッチを楽しめる。差は、認識から何を選び、どこに満足を残すかに置く。

最新Human追記に従い、ピカブイの可愛い交流を共通の体験テーマとして取り入れる。ハイタッチは「前肢提示→WAIT→触点ACK→嬉しい応答→満足」の共通遊び。頬/頭の差し出し、撫でに気持ちよく応じるhold、少し後からもう一度こちらを見る好意も共通の楽しさに含める。既存資料の「原理だけ」という説明を、共通テーマを禁止する意味では採用しない。具体的な身体演技は3匹に合わせて設計する。

本人の意思は **Intent → Action/Choice → Outcome** で見えること。目の前の入力または自分の関心に気付き、何かを選び、その結果で顔・姿勢・次の注意が変わる。音・FX・説明なしでも因果を読める構造を優先する。毎回大きな反応を要求せず、十分に届いた後の小さい受容も魅力として扱う。

## B. Authority / Design Decisions

### B1. Source register

| Key | 正本・入力と使用範囲 |
|---|---|
| NORTH | [Product North Star](../../grimo/knowledge/GRIMO_PRODUCT_NORTH_STAR_AND_MINIMUM_REQUIREMENTS.md) §§1–11。可愛さ→癒し→愛着、局所因果、罰なし、Human判定 |
| EXP | [Experience Spec](../../grimo/knowledge/GRIMO_CHARACTER_EXPERIENCE_SPEC.md) §§2–11。注意、Touch、Agency、WAIT、余韻、3匹の身体表現 |
| ARCH / OPS | [Production Architecture](../../grimo/knowledge/GRIMO_CHARACTER_PRODUCTION_ARCHITECTURE.md) §§3–8 / [Operating System](../../grimo/knowledge/GRIMO_PRODUCTION_OPERATING_SYSTEM.md) §2。Canonical優先、Full-Spatial + View-Weighted Polish、方法は未固定 |
| PRODUCT | [Product Feature Spec](../../grimo/knowledge/product/GRIMO_PRODUCT_FEATURE_SPEC.md) §§5,10–18,21。Food・Wear・Special・Secret・Gift・Collection・親密度なし |
| DATA | [Data Model Spec](../../grimo/knowledge/product/GRIMO_DATA_MODEL_SPEC.md) §§5.4,8–9,21–24。consume確定、装備交換、Secret activation、Giftの渡す→Collection/所有記録の境界 |
| IDENTITY | [Phase 1](GRIMO_FOUR_CHARACTER_EXPERIENCE_IDENTITY_DRAFT.md) B–E,H。3匹の人格候補、外見保護 |
| DIRECTION | [Phase 2](GRIMO_FOUR_CHARACTER_BEHAVIOR_PERFORMANCE_DIRECTION_DRAFT.md) B–J。代表演技・入力/支持/接続の候補 |
| PACK / PLAN | [Evidence Pack](GRIMO_MOTION_EVIDENCE_PACK_DRAFT.md) A–D / [Zero-Based Plan](GRIMO_FOUR_CHARACTER_MOTION_ZERO_BASED_PLAN_20261011.md) Phase 3。観察・推論・提案の分離、今回の工程境界 |
| E-M / P-M | [Eevee Master](../../grimo/knowledge/research/motion-masters/EEVEE_MOTION_MASTER_INVENTORY.md) MF-051–054 / [Pikachu Master](../../grimo/knowledge/research/motion-masters/PIKACHU_MOTION_MASTER_INVENTORY.md) MF-021–022。既存観察記録のoffer/WAIT/contact/payoff。新規動画解析ではない |
| VIEWS | [Body-only register](../../grimo/knowledge/character-production/GRIMO_BODY_ONLY_MULTIVIEW_ASSET_REGISTER.md) §1。派生画像はCanonicalを置換しない。Jill頭部の桃色付属はhorn-likeとして保護 |

3枚のCanonical PNGも確認した。小顔と羊毛、Jillの葉/翼/太い尾、Pinoの丸さ/内寄り前肢/厚い尾、Shushuの短肢/花冠/花束が演技の境界。画像周辺の蝶・雲・水泡・花を常設propsや入力対象として新設しない。ChatGPT Project Memoryは取得しておらず、内容を推測しない。

### B2. Labels and precedence

**A:** 既承認要件・今回の明示Human指示。**O/T:** 既存研究の可視観察/時間推定。**I:** 意図等の解釈。**P:** 本書の具体演技提案。**U:** 未承認/未検証。各catalogの演技・variant名は全てP。身体能力は全てUを伴う。O/TからRig方式・内部scheduler・心理的効果を断定しない。
今回の明示指示がPhase 1・2文書の「Gate 1承認前はPhase 3へ進まない」という古い実行停止条件に優先する。**設計を進める許可と人格の最終承認は別**。旧モデル配分・残量制約は使用せず、サブエージェント、アプリ実装、Blender/Tripo、動画再解析、Web調査は行わない。

### B3. Family / variant accounting

Familyは意味のある行為単位。左右、速度、Food品目、割り込み分岐を別Familyにして件数を増やさない。**V**は本書で列挙する基本performance profile数。左右/現在姿勢/gesture/履歴の条件合成を乗算しない。Foodのstyle5とtaste4も20個の専用clipへ展開しない。variantは制作済みclipではない。

本文のprofile名はPの制作候補名である。既存profileの資産や意味を置換する命令ではなく、FINALに別の具体指定があればそちらを保持する。Jill/Pino/Shushuは独立した行為から作り、未決定Secret候補も別記して集計する。SpecialのFood/Wear構成、横断接続、Gesture条件は重複Familyに数えない。

## C. Shared Motion Semantics

### C1. Family cardの23項目と共通契約

各Familyは、見出しの **ID / 名前 / Category / Priority / V / Capability** と、「設計」「演技」「運用」の記述、以下の共通契約を併せて読む。省略した項目を空欄や自由裁量にしない。個別カードが共通契約を精密化する。

| 要求項目 | 追跡先 |
|---|---|
| 1–3 ID/Character/Category/Priority | F–Hの見出し。J=Jill、P=Pino、S=Shushu。必=要件coverageに必要、拡=拡張提案、保=既承認contentを保護、候=未承認content候補。全新演技はDRAFT |
| 4–7 Purpose/Trigger/Motivation/Emotion | 各「設計」。本人の欲求と変化を示す |
| 8–14 Attention/Face/Primary/Secondary/Stillness/Sequence/Timing | 各「演技」。矢印は時系列で、等時間の段階ではない。局所ACKの即時性と演技の間は別 |
| 15–17 Variants/History/Interruption | 各「運用」＋K。列挙profileと今の姿勢を組み合わせ、初回を繰り返さない |
| 18 Props/Audio/FX | Food/Gift/prop Secretのみ明記物が必須。Wearは装着物が必要。その他は外部props不要。全Familyの音/FXは補助、意味成立の必須条件にしない |
| 19 Readability | 各「設計」の意思→各「演技」の結果。Lの無説明監査。成功はその変化が見えること |
| 20 Identity Restrictions | B2と各個体の冒頭。全員:長い指/新しい眉/巨大な口/Canonical比率変更/一枚絵全身warp不可 |
| 21 Dependencies | 各見出しのQ番号→Nの要求面/独立部位/支持/干渉/未検証事項 |
| 22 Acceptance | 下記category scenario＋各カードの運用分岐。将来の確認条件であり実演要求/実施証拠ではない |
| 23 Authority/Evidence/Proposal/Unknown | B1/B2、contentはJ、提案衝突はO |

**全FamilyのHistory:** 同じ完全chainを連続させず、直前に満たされた欲求は確認/振幅/誘いを減らせる。局所ACKと可愛い基本受容は減らさない。希少演技のために通常の魅力を取り上げない。直前のzone/side/offer/感情/未完行為を引き継ぐ。一時的な慣れは親密度/XPではない。

**全FamilyのInterruption:** 新触点ACKはすぐ返す。主行為は今の姿勢から接続し、強制Neutralや古い入力queueを使わない。接触release時は押圧形状/有効offerを解く。支持移行、bite、Gift transferは安全な区切りを守り、顔/非口元/非保持部でACKする。保護中の入力が既に解放されていれば後から大きく再演しない。画面離脱は現実時間の演技を裏で完走する根拠にしない。
**全FamilyのTiming:** 認識は遅らせず、動機を選ぶ間、動作が終わる減速、結果を味わうholdを分ける。新しい秒数/角度/thresholdは作らない。Catalogの「短い/広い」は演技の相対関係。

| Category | 将来のAcceptance Scenario |
|---|---|
| A Life / B Attention | 30秒無入力、初回/満足後/眠気。静止に入った理由と次に見る対象が読める。音/FXなし |
| C Touch | 頭・頬L/R・身体でtap/poke/slow/continuous/back-and-forth、途中release/side change、弱い反復10回。実在触点と因果、快/過密の分離 |
| D Emotion / L Rare | 原因ありの小/大喜び、無害な驚き、満足後の再touch。ストレッチ/ランダム動作/常時winkに見えない |
| E Social / High-five | offer前→WAIT→target応答/別zone応答/無応答/途中cancel/再接触。接触後に喜び、自由な不参加、支持が読める |
| F Boundary | 穏やかな反復と過密pokeを比較。hint/拒否/距離/解放後回復、謝罪や追加touchなしで回復する |
| G Food | style5×好き度1–5を意味として網羅。1未消費、2–5食後評価。bite中の頭touch/品目取消/保持物の可視性 |
| H Wear | 各安全anchorで装着/交換/解除、lean/喜び/Touch中。1個装備、目/モチーフ保護、旧物と新物の混同なし |
| I Content / J Gift | 所有/発動権限あり/なし、target応答/外れ/無応答、保持中touch、exit/transfer境界。UIなしでも提示意図を読める |
| K After / Entry | 喜び→別touch、拒否→解放、Food→hold、復帰。現在の姿勢/気持ちが連続し、未完消費/報酬を偽装しない |

### C2. Touch zone map

| 個体 | 有効面 / 限定面 | 条件と禁止 |
|---|---|---|
| Jill | headの軟部、cheek L/R、chest/body、appendage_root（翼根元/尾根元の実在面）、提示forepaw | 頭のhorn-like付属を耳として揉まない。翼膜/葉先/尾先を多数の遊びzoneにしない。根元は短いACKと保護、引っ張り入力なし。前肢提示時だけ接点を交流targetとして扱う |
| Pino | head、cheek L/R、chest/body、forepaw（自発試行/ハイタッチ時）、ear_root/tail_rootの限定ACK | 太い尾を「掴める道具」にしない。耳/尾の物理dragなし。自分の床/身体接触とユーザーtouchを区別。両眼を持ち、winkは状態差 |
| Shushu | headの花冠非重複面、cheek L/R、chest/body、ear_root、提示forepaw | 花冠/花束は皮膚の代替zoneにしない。保持物/支持前肢をtapのために投げない。小耳を拡大してtouch面を稼がない |

3匹の最小zone構成はPRODUCT §5・身体から導いたP/U。眼・口内・装飾particlesは全員除外。screen-leftと解剖学Lは別。実際の面からsideを得て、中央はcentralのまま。受理された複数touchには局所ACKを返すが、左右へ同時に大きく倒れない。対応入力数は製品判断を拡張しない。
### C3. 可愛い共通遊びの採用台帳

| Theme | 根拠 / 採用範囲 | Jill / Pino / Shushu |
|---|---|---|
| 頬/頭を差し出して撫でを受け取る | EXP §§5–6 A、PACK C4–5 O/I |  / J13 / P15 / S14。Pinoも甘えられ、Shushuも歓迎する |
| 気持ちよいmoving hold | EXP §§2–3 A、PACK B3–4 O/I |  / J06–11,J23 / P08–13,P25 / S07–12,S24。誰も常時動く必要はない |
| 小さな接触→はっきり嬉しい顔→好意の余韻 | PACK B7,B11、EXP §§7–8 |  / J14,J26 / P16,P28 / S15,S27。稀少演技だけを可愛くしない |
| High-five | E-M MF-051–053、P-M MF-021–022のO/T:提示と接触payoff。今回Human指示A:共通の可愛い遊びにする。具体演技P | J12 / P14 / S13。全員に身体面との交流を設計。各個体の支持と接点を実物で検証 |

E-M MF-054の別反応は意味未解決。拒否や失敗の証拠として採用しない。ハイタッチに力センサー、実手追跡、タイミング点数、成功報酬、新アイテムunlockを追加しない。既存tap/pokeで提示面に応答する意味設計。掌を頭の高さへ上げる人間的動作は必須でなく、低い「ちょん」でも、offer→接触→嬉しさが明瞭なら成立する。

## D. Complete Motion Coverage Map

| Coverage | Jill | Pino | Shushu |
|---|---|---|---|
| A Living/呼吸/まばたき/姿勢/休息/眠気/起床 | J01,J03–05 | P01,P03–06 | S01–02,S04–05 |
| B 注目/確認/視線保持・解放/自己身体 | J02,J15,J24 | P02–04,P17,P26 | S03–04,S16,S25 |
| C tap/poke/slow/continuous/back-and-forth/固有面 | J06–11 | P07–13 | S06–12 |
| D 喜び/安心/好奇心/驚き/甘え/遊び/満足 | J03,J12–15,J21,J26 | P03–04,P14–17,P23,P28 | S02–04,S13–16,S22,S27 |
| E 自発offer/WAIT/応答/無応答/自己活動へ | J12–13 | P14–15 | S13–14 |
| F hint/refusal/withdrawal/recovery | J09,J16–18 | P11,P18–20 | S10,S17–19 |
| G Food/style5/好き度1–5/保持中入力 | J19–21 | P21–23 | S20–22 |
| H Wear/認識/装着/交換/解除/Identity | J22 | P24 | S23 |
| I Special/Secret/所有/発動/完了 | J19–22,J27＋§J3 | P21–24,P29＋§J3 | S20–23,S28＋§J3 |
| J Gift/自発意図/提示/受領/余韻 | J25 | P27 | S26 |
| K 接続/同時touch/release/afterglow/WAIT解除 | J18,J23–25＋K | P20,P25–27＋K | S19,S24–26＋K |
| L Signature/意外性/rare | J03,J12–14,J26–27 | P03–04,P14–17,P28–29 | S02,S13–15,S27–28 |

呼吸/まばたきはLife Family内の独立channel、Emotionは原因のあるFamily内の評価、TransitionsはKの横断契約。名前の数だけclipを増やさない。以下catalogにあるFamily全てがNへ紐付く。未決定contentは候補として設計し、現行製品に採用したことにはしない。

## F. Jill Motion Catalog

**楽しさを共有する。** 私的に楽しい行為と、相手へ向けて応答を受ける行為を分ける。胸/上半身が喜びの中心、翼/葉/尾は意味を補う。翼を全反応で開かず、尾根元は身体所属と重さを保つ。horn-like頭部を柔らかい耳に変えない。下半身の安定した支持形態はUで、尾を支柱にする前提を置かない。共通契約はC、全演技P/U、product ruleはA。

### J01 Living / Private Contentment — A / 必 / V3 / Q01,Q02,Q03,Q06

- **設計:** もう楽しい気持ちを持って過ごしている。快→穏やかな充足。常時相手を待たない。
- **演技:** 胸の構えが休む→顔が今の気分を残す→視線releaseとblink→小呼吸。翼を楽な形に止め、下半身/尾根元は安定。葉は主動作の小recoveryだけ。
- **運用:** V=開眼の楽しさ/遊び後の休息/関心を保つ静止。直後の大演技を抑え、touchはlocalから。A scenarioで元気を翼の常時往復にしない。

### J02 Attention / Shareable Check — B / 必 / V3 / Q01,Q02,Q06

- **設計:** 対象を確かめ、ときには相手にも向けたい。関心→確認/共有への入口。
- **演技:** 目が実在対象へ→頭/胸が必要分だけ向く→分かった時に顔を相手へ少し開く→対象または休息へ。翼/下半身は止め、機械的な交互lookなし。
- **運用:** V=対象確認/相手の短い確認/対象から共有へ。既知なら確認を短縮、新touchはその面ACK。B scenarioで「何を見ていたか」が残る。

### J03 Private Stretch / Wing Care — A,D / 必 / V3 / Q01,Q03,Q04,Q06

- **設計:** 自分の身体を心地よく使い、整えたい。くつろぎ→私的な楽しさ。
- **演技:** 胸を少し起こす→低い前肢をほどく/片翼を楽に整える→顔に快→支持を残して一度止める→翼/葉が収まる。届く部位だけ前肢で軽く整え、葉を引き抜かない。
- **運用:** V=胸の伸び/片翼の置き直し/届く身体面の身繕い。共有したい時だけJ13へ。無入力でも完結、反復は別の休息へ。A/D scenarioでstretch自体と招待を区別。

### J04 Grounded Weight Reposition — A,K / 必 / V2 / Q03,Q04,Q06

- **設計:** 動いた上半身を自分の足で楽に支える。活動→安定。
- **演技:** 動かす支持面を顔/胸が小さく意識→残る足へ荷重→一足/下胴の配置を整える→尾根元が身体に従い→胸が休む。飛行、尾で突っ張る動作なし。
- **運用:** V=私的姿勢の調整/共有姿勢からの戻し。支持移行中は局所ACKを返し主反応を待つ。A/K scenarioで翼や尾が重量を代行しない。

### J05 Rest / Drowsy Wake — A / 必 / V3 / Q01,Q02,Q03,Q06

- **設計:** 遊びを終えて休みたい。快→眠気、touch→眠さの中で気付き。
- **演技:** 胸/前肢を楽にする→目が細まり頭が休む→翼/尾の安定を残すhold→touch位置の受け→目が短く相手を確かめ、起きるか休み続ける。大きい羽ばたきで覚醒しない。
- **運用:** V=休息入口/眠いhold/やわらかい起床。再touchで必ず完全覚醒せず、Foodには明確なnotice。A/C scenarioで鈍い入力と区別。

### J06 Head Touch / Bright Receipt — C / 必 / V3 / Q01,Q02,Q06

- **設計:** 頭への触れ合いを嬉しい出来事として受ける。気付き→好意。
- **演技:** 軟部の実触点を頭で小さく受ける→同側目/口が評価→顔を相手へ→胸が僅かにほどける→hold。角は凹ませず、翼・脚は静か。
- **運用:** V=tap・poke notice/slow petの受容/慣れた小受容。poke過密だけJ16、releaseでJ23。C scenarioで速いACKと胸の喜びの時間を分ける。

### J07 Cheek Touch / Turn to Share — C / 必 / V4 / Q01,Q02,Q03,Q06

- **設計:** 頬の気持ちよさを受け、嬉しさを相手にも向ける。快→共有した好意。
- **演技:** 同側頬の局所受け→目/顔が快を示す→頬を少し開き、胸を対話方向へ整える→顔の温かいhold。支持/反対翼は止める。
- **運用:** V=短いnotice/頬のslow受容/顔と胸の共有/満足の小hold。L/R保持、新sideは旧commitを解く。C scenarioで接点を胸の喜びに消さない。

### J08 Chest / Body Touch — C / 必 / V3 / Q01,Q03,Q06

- **設計:** 胸/胴の感触を受け、相手との近い遊びを喜ぶ。
- **演技:** 実面の小さい受け→顔が触点を確認→胸の緊張が解ける→必要なら前肢を低く開く→胴の支持位置を保ったhold。葉のwaveで触点を代行しない。
- **運用:** V=短いbody notice/穏やかなbody pet/楽しい小受容。continuousはJ10、過密はJ16。Wear面に当たった場合は胸への皮膚touchを偽装しない。C/H scenario。

### J09 Appendage-root Notice / Protection — C,F / 必 / V3 / Q01,Q03,Q06

- **設計:** 翼/尾根元への接触を認識し、快なら受け、動く余地が必要なら守る。
- **演技:** 実根元の小ACK→目/頭がその側へ→翼を楽な閉じ方にする/尾根元の向きを小さく整える→顔を温かく残す。反対付属/下半身は静か、引っ張られて伸びない。
- **運用:** V=翼根元notice/尾根元notice/余地を守るhint。根元の左右/appendage種は条件。releaseでJ18/J23、rough継続でJ17。C/F scenarioで翼膜が皮膚のように潰れない。

### J10 Continuous Stroke / Shared Ease — C / 必 / V3 / Q01,Q02,Q03,Q06

- **設計:** 続く撫でを嬉しく受け、楽しさを静かな共有へ育てる。
- **演技:** 経路の実触点を更新→顔の快→胸の小さい開き→前肢/翼は必要分だけ休む→満足したmoving hold。頭/胸を指の経路で振り回さない。
- **運用:** V=快が育つ/静かに十分/既に満足した小受容。入力連続は一行為、release/side changeは今の深さからJ23。C scenarioで活発さと落ち着きを両立。

### J11 Back-and-forth Pet / Playful Settle — C / 必 / V3 / Q01,Q02,Q06

- **設計:** 往復の感触を可愛い遊びとして受け、十分なら休む。
- **演技:** 反転の局所受け→顔が少し面白がる→胸の小さい嬉しさ→翼/前肢を止めて楽しむhold→静かなsettle。指と同周期の羽ばたきなし。
- **運用:** V=軽い遊び/満ちた受容/速い過密への区切り。弱い反復を拒否理由にせず、rough時だけJ16。C scenarioで笑顔とboundaryの因果を読む。

### J12 High-five / One Reply Is Plenty — E,C / 必 / V4 / Q01,Q03,Q04,Q06

- **設計:** 相手と前肢をちょんと合わせたい。私的な楽しさ→期待→返事の喜び。
- **演技:** 安定支持を確認→目を相手へ、片前肢の面を見せる→胸の開きを止めてWAIT→target tapの手先ACK→前肢が一度身へ寄り、胸/顔が嬉しく開く→翼は必要な小参加→前肢を休める。
- **運用:** V=一往復/小さい返事/慣れた柔らかい返事/無応答の自己完結。再touchは小ACKで満足、掌chainを要求しない。別zoneも返事として歓迎し、target成功とは混同しない。E scenario。

### J13 Invitation / Open a Shared Moment — E / 必 / V3 / Q01,Q02,Q03,Q04,Q06

- **設計:** 楽しかった自分の時間に相手の分を空けたい。私的快→共有の期待。
- **演技:** J03等の楽しさ→顔の宛先を相手へ変える→低い前肢/胸の開きを小さい提示に収める、または撫で面を見せる→WAIT→局所ACK→返事に胸/顔が喜ぶ→休む。翼はWAITで止める。
- **運用:** V=遊びへの招待/頬の甘え/頭の甘え。無応答は自分の快へ収め、J01/J03へ。頭touchでも十分嬉しい。直後の再offer抑制。E scenarioで見せ芸・指示待ちを除く。

### J14 Delight / Joy Opens Outward — D / 必 / V3 / Q01,Q03,Q04,Q06

- **設計:** 嬉しい返事/出来事を共有したい。快→明確な喜び→共有満足。
- **演技:** 顔に「届いた」→胸が支持上で起きる→低い前肢が開く→翼/葉が少し後から補う→peakで相手への顔を止める→胸/前肢を休める。尾は身体に従う重さ、飛び上がりなし。
- **運用:** V=顔と胸の小喜び/翼が添う喜び/大きい嬉しさから静かな共有。反復は振幅を増やさず、touchで喜びを残したまま局所へ。D scenarioはFXなし。

### J15 Surprise / Curious Reassessment — B,D / 必 / V3 / Q01,Q02,Q03,Q06

- **設計:** 不意の変化を確かめ、無害なら楽しさに変えたい。
- **演技:** 目/口の短い意外さ→頭が原因へ→胸は支持を保ち一度止まる→理解した顔→小さく相手に開くか対象へ戻る。翼を恐怖の大展開にしない。
- **運用:** V=小驚きから確認/面白い変化を共有/既知の変化へ短反応。対象消失で終了、新touchは局所ACK。B/D scenarioで驚きだけの乱発を除く。

### J16 Boundary Hint / Make Some Room — F / 必 / V2 / Q01,Q03,Q06

- **設計:** 接触が詰まったので自分から動ける余地がほしい。快→小戸惑い。
- **演技:** 触点側の顔が区切り→胸の開きを小さく閉じる→必要な前肢/翼を自分の範囲へ→下半身は安定。怒った羽ばたきや大きい尾振りなし。
- **運用:** V=身体の過密/交流を割り込まれ続けたhint。releaseならJ18、継続ならJ17。無応答をhint原因にしない。F scenario。

### J17 Refusal / Grounded Withdrawal — F / 必 / V3 / Q01,Q03,Q04,Q06

- **設計:** 今の刺激を明確に終え、自分の余地を取り戻す。
- **演技:** 頭/顔が触点を避ける→前肢/翼を内側の楽な位置へ→必要なら支持内の小turn→目で相手を認識しつつ刺激面を離す→自分の快を整える。叩く/尾で払う動作なし。
- **運用:** V=頭のoffer終了/胸面の保護/付属根元の余地。解放でJ18、別zone ACKと元の境界を両立。F scenarioで悲嘆・罪悪感なし。

### J18 Recovery / Ready to Enjoy Again — F,K / 必 / V2 / Q01,Q03,Q06

- **設計:** 余地が戻り、自分の楽しさと交流を再び保てる。
- **演技:** 保護した姿勢を小さく解く→胸/翼を楽に収める→顔が暖かく戻る→短い相手確認→私的な休息。すぐ再inviteしない。
- **運用:** V=hintから回復/withdrawalから回復。user無入力で成立、穏やかなtouchは合流可。F/K scenarioで急なhappy flipを除く。

### J19 Food Notice / Pre-consume Choice — G / 必 / V3 / Q01,Q02,Q09

- **設計:** Foodを見て、食べたいか選ぶ。関心→期待/穏やかな拒否。
- **演技:** 目→頭がFoodへ→好きなら胸に小期待、受領位置で待つ。好き度1は口を受領させず頭/前肢を少し閉じ、相手への好意は残す。支持/翼は安定。
- **運用:** V=通常notice/好きFoodへの期待/好き度1未消費拒否。撤去でJ23、2–5はJ20へ。既知Foodは初見驚きを省く。G scenarioで食前拒否を食後嫌いと分ける。

### J20 Food Consume / Five Styles — G / 必 / V5 / Q01,Q02,Q03,Q04,Q09

- **設計:** 食べる選択を口/必要な前肢で実行し、味を確かめる。
- **演技:** 頭とFood接点を整える→style主動作→胸を安定させ口の処理→翼/尾は休む→味を見る小停止。食べながら毎口翼を開かない。
- **運用:** V=一口/複数口/なめる/飲む/大きい物。J1の個体scriptへ。bite中touchは非口元ACK、safe nodeから切替、consume事実保持。G scenario。

### J21 Food Taste / Shared Happiness — G,D / 必 / V4 / Q01,Q03,Q06,Q09

- **設計:** 食べた味を自分で評価し、好きなら嬉しさを相手へ開く。
- **演技:** 味の小停止→2:口元の微妙さと胸の小収まり、3:普通の満足、4:胸/顔を相手へ明るく、5:胸から翼まで選択参加し長い共有hold→落ち着く。2も吐出/責め顔なし。
- **運用:** V=好き度2/3/4/5。消費済み、毎回初発見にしない。大きい喜び中touchでlocalを返しpeak再演を足さない。G/D scenarioで4段階の結果を読む。

### J22 Wear Recognition / Equip / Enjoy — H / 必 / V3 / Q01,Q02,Q06,Q10

- **設計:** 自分に着いた物を認識し、相手と小さく喜びたい。
- **演技:** 物を見る→頭中央/首胸の安全anchorへの装着を受ける→目/胸がその位置を確かめる→顔を相手へ明るく→胸が休む。角/葉/翼根元を隠さず、見えない頭上を無理に覗かない。
- **運用:** V=初装着の気付き/交換の違い確認/解除の収まり。1個所有装着、旧物を二重表示しない。touch中は保持anchorを崩さず局所ACK。H scenarioは翼開閉との干渉も確認。

### J23 Afterglow / Private or Shared Settle — K / 必 / V3 / Q01,Q03,Q06

- **設計:** 共有できた嬉しさや私的快を、休んだ身体へ残す。
- **演技:** 胸/前肢が止まる→翼/葉が小さく収まる→顔の温かさと目の短dwell→視線release。下半身/尾根元は安定、毎回Neutralへ揃えない。
- **運用:** V=共有の温かさ/私的快の完結/感情peakのないsettle。新touchは今の顔から。未完offerは閉じ、J26は別のrare思い返し。K scenario。

### J24 Session Entry / Current Joy — B,K / 必 / V3 / Q01,Q03,Q06,Q11

- **設計:** いまのJillの時間から相手を迎える。休息/関心→認識。
- **演技:** 既に安定した支持/翼の姿勢→顔が現在の快を保つ→必要なcheck-in→胸の小settle。毎回飛び込む/羽ばたく歓迎なし。
- **運用:** V=新session/短い再入場/背景復帰。古いWAITや入力は解き、Food/Gift事実保持。B/K scenarioで不在を寂しさへ変換しない。

### J25 Gift / Bring You Into My Joy — J / 必 / V3 / Q01,Q03,Q04,Q06,Q13

- **設計:** 自分が嬉しいと感じた贈与を、相手との出来事にしたい。
- **演技:** bounded Giftを準備する視線→顔が相手へ→前肢/胸前で見える提示→翼は静か、WAIT→受理を前肢の局所変化/顔で受ける→transfer→胸の喜び→温かい完了。
- **運用:** V=低い前肢提示/胸前の提示/支持を優先する片前肢assist。品目/発生率は追加せずAUTO product eligibility。無応答も好意を保ち、保持中touchは非保持部ACK。J scenario/J4。

### J26 Rare / The Smile I Held Back — L,D / 拡 / V2 / Q01,Q03,Q06

- **設計:** 返事を受けた後、抑えていた嬉しさが自分から少し漏れる。共有満足→小さい遊び心。
- **演技:** J23で落ち着く→顔がもう一度明るく→胸に小さい一拍、翼を開きかけて楽に収める→相手に温かい顔を残す。新offer/拍手待ちなし。
- **運用:** V=顔・胸だけの思い返し/翼が一瞬添う思い返し。全sessionで必ず発生させず、touchはその嬉しさへ合流。L scenarioでWAIT失敗や痙攣に見えないこと。

### J27 Secret Candidate / Wing-shelter Peek — I,L / 候 / V2 / Q01,Q03,Q04,Q06,Q12

- **設計:** 小さい翼のかげから顔を覗かせ、相手と可愛い再会を遊ぶ。私的遊び→期待→返事の喜び。新unlock/アイテムは未採用。
- **演技:** 顔が相手を確かめる→片翼を安全範囲で顔の横へ、部分だけ隠す→目/翼端targetを見せWAIT→有効tapを翼根元を壊さず受ける→顔を開き胸が喜ぶ→翼を楽に戻す。翼で顔全体を覆う能力は必須にしない。
- **運用:** V=片翼のpeek/一度側を替えるpeek。発動方式P=BOTH候補、回数/所有条件U。翼可動とスマホ遮蔽U、不可なら無理に翼を拡大せず候補を戻す。I/L scenarioでJ12と「隠れ→再会」の意味を分ける。

## G. Pino Motion Catalog

**発見し、確かめる。** 動かした部位と、結果を見て止まる時間を分ける。ユーザーは結果に参加でき、Pinoも好きな撫でや遊びを自分から求める。太い尾は重い身体に従い、第三の手/常設支柱にしない。両眼がありwinkを常態化しない。手合わせだけを人格の記号にせず、P03の片前肢の置き方を第一候補にする。水/泡/音なしでも成立。全演技P/U、product ruleはA。

### P01 Living / Interested or Satisfied Quiet — A / 必 / V3 / Q01,Q02,Q03,Q07

- **設計:** 自分の関心を持ち、分かった後は休める。関心/満足→安定した日常。
- **演技:** 前肢を内寄りの楽な配置→目が今の対象へ/自然にrelease→口元に穏やかな快→blink/小呼吸。下半身は重く支持し、尾を常時揺らさない。
- **運用:** V=対象を見る静止/納得した休息/次を考える短hold。試行を連発せず、touchはその面ACK。A scenarioで休むことも自立と読める。

### P02 Attention / Focus and Release — B / 必 / V3 / Q01,Q02,Q07

- **設計:** 気になった実在の面/対象を選び、確かめたい。散漫でなく焦点を持つ。
- **演技:** 目が対象を拾う→頭が必要分近づく/向く→前肢は動かさず結果を見る→納得して視線を解く。支持・尾は静か。新刺激を全部追わない。
- **運用:** V=身体面への関心/外部対象確認/相手への親しい確認。既知対象は短く、新touchは局所ACKから注意を更新。B scenarioで何もない空間の追跡を除く。

### P03 Paw Set / Press / Look — A,D,L / 必 / V3 / Q01,Q03,Q04,Q07

- **設計:** 前肢の置き方と受けた感触を、自分で試して確かめたい。関心→小発見→納得。手揉みを避ける代表Signature候補。
- **演技:** 片前肢を低い見える支持面へ置く→他の支持は安定→軽く荷重し、接点を目で見る→荷重を解いて前肢を僅かに上げる→丸い先端/置いた位置を見て止まる→目/口が納得してほどけ、別の置き方を一度試すか休む。床の魔法反応や全身bounceなし。
- **運用:** V=置いて戻りを見る/向きを変えて一度確かめる/既知の感触を短く味わう。局所圧縮の可視量/到達はU、隠れた変形だけでは成立扱いにしない。頭touchは手元を保留、条件が変われば試行を閉じる。A/D scenario。

### P04 Thick-tail Inspection / A Small Turn — B,L / 拡 / V2 / Q01,Q03,Q07

- **設計:** 自分の向きを変えた結果、見える尾の位置も変わったことを確かめたい。
- **演技:** 支持内で小turn→身体に属する尾が遅れて収まる→目/頭が実際に露出した側面を一度見る→納得して前肢と顔が休む。尾を前へ巻く/掴む能力は要求しない。
- **運用:** V=turn後の確認/既知の尾位置を短く確認。露出/顔の可読性が成立時のみ候補、通常Touchを尾視認に依存させない。新touchで中止可。B/L scenarioで理由のない尾追いを除く。

### P05 Grounded Posture Rebalance — A,K / 必 / V2 / Q03,Q04,Q07

- **設計:** 試行中の自分の重みを楽に整える。活動→安定。
- **演技:** 残る支持に重みを保つ→足/下胴を小さく置き直す→前肢を内寄りへ→尾が主身体に従って収まる→顔が満足。座位を固定せず、胴を丸いballとして転がさない。
- **運用:** V=試行からの戻し/休息の小調整。荷重移行中ACKは顔/局所、主反応は安全な位置から。A/K scenarioで尾と胴の融合を除く。

### P06 Rest / Let the Experiment End / Wake — A / 必 / V3 / Q01,Q02,Q03,Q07

- **設計:** 十分確かめたので休む。納得→眠気、touch→眠い好意。
- **演技:** 次の試みを始めず前肢を休む→目の集中がほどける→頭を支持内の楽な位置へ→静かなhold→touch側で受ける→短く目を向け、起きるか休む。尾/足は崩れない。
- **運用:** V=休息入口/眠いhold/好意を持つ起床。未完の関心は残せるが無限試行なし。A/C scenarioで「活発だから眠らない」を避ける。

### P07 Tap / Poke / What Changed Here — C / 必 / V4 / Q01,Q02,Q07

- **設計:** 当たった場所を確かめ、小さい接触を面白く/嬉しく受け取る。
- **演技:** 実触点の局所ACK→同側目/顔の評価→必要な頭/前肢だけ確認→好意/小関心の終点。下半身/尾は止め、全身を弾ませない。
- **運用:** V=柔らかいnotice/嬉しいnotice/意外さの確認/過密の局所保護。zoneでP08–11へ、短いrelease後に長い試行を起動しない。C scenarioで毎回初発見の乳児性なし。

### P08 Head Pet / Choose the Nice Feeling — C / 必 / V3 / Q01,Q02,Q07

- **設計:** 頭の気持ちよい撫でを、自分から選んで受ける。関心→快→満足。
- **演技:** 頭触点の小受け→目が相手/触点を確認→頭を楽な角度へ少し開く→前肢の構えが解ける→快のhold。尾/支持は静か。前肢の仕事を無理に継続しない。
- **運用:** V=確認から快/集中の合間の受容/満足済みの小受容。releaseでP25、roughはP18。C scenarioで独立性を撫で拒否に変えない。

### P09 Cheek Pet / A Little More This Way — C / 必 / V3 / Q01,Q02,Q03,Q07

- **設計:** 好きな頬の感触を確かめ、気に入れば少し近さを足したい。
- **演技:** 同側頬ACK→目/口が快→頭が小さく接点へ→内寄り前肢が楽にほどける→結果を味わい止まる。支持/尾は保つ。
- **運用:** V=短い確認/気に入った頬の受容/自分から小さく寄る。L/R、side changeは旧commitを解き新側へ。C scenarioで好意が結果検分だけに消えない。

### P10 Body Pet / Rounded Ease — C / 必 / V3 / Q01,Q03,Q07

- **設計:** 胴の柔らかい感触を受け、集中を解いて気持ちよく過ごしたい。
- **演技:** 実面の小受け→顔が位置を確認→前肢を楽に収める→胴の荷重は支持上に残す→顔の満足。腹全体のゴム変形/空気ballの弾みなし。
- **運用:** V=body notice/穏やかなpet/試行後のくつろぎ。continuousはP12、Wear面との区別はP24。C scenarioで触点と全体の丸さを両立。

### P11 Ear / Tail-root / Forepaw Context Notice — C,F / 必 / V3 / Q01,Q02,Q04,Q07

- **設計:** 自分の可動部に届いた接触を認識し、今使っている面を守るか交流するか選ぶ。
- **演技:** 実根元/前肢面の局所受け→顔が同側へ→必要なら部位を楽な向きへ→意図を持つ小hold。尾/耳を引っ張らず、反対前肢/支持は保つ。
- **運用:** V=根元へのnotice/試行中前肢の受け/余地を守る。P14/P15のoffer targetは遊びACK、敏感部判定で潰さない。releaseでP20/P25。C/F scenarioで自己接触とuser入力を混同しない。

### P12 Continuous Stroke / Discover Then Enjoy — C / 必 / V3 / Q01,Q02,Q03,Q07

- **設計:** 最初に感触を確かめたら、もう調べ直さず楽しめる。関心→快→安心。
- **演技:** 経路の局所受け→顔の確認→前肢/頭の構えがほどける→一定の快い姿勢→支持と尾を残すmoving hold。毎strokeで新実験を開始しない。
- **運用:** V=確認して深まる/慣れた快/眠い満足。releaseは現在深さから、別side ACKを保持。C scenarioで連続撫でを作業にしない。

### P13 Back-and-forth Pet / Notice the Change, Settle — C / 必 / V3 / Q01,Q02,Q07

- **設計:** 往復の違いを一度面白がり、その後は快として受ける。
- **演技:** 反転の実触点ACK→目/口の小意外さ→頭が一度楽に開く→指の反転を追うのをやめ満足hold。前肢/尾の交互パタパタなし。
- **運用:** V=短い変化確認/気持ちよい往復/十分を示す区切り。遅い反復は受容、roughだけP18。C scenarioで試す癖より可愛い快が先に読める。

### P14 High-five / Touch, Look, Smile — E,C / 必 / V4 / Q01,Q03,Q04,Q07

- **設計:** 相手との接触を試し、その違いを面白がり喜ぶ。関心/遊び心→期待→好意ある発見。
- **演技:** 安定した支持→片前肢の面を低く見せる→目が接点と相手を結ぶWAIT→target tapで前肢ACK→目が触れた面を短く確かめる→顔を相手へ明るく→前肢を自分の楽な配置へ。尾は胸/胴に従う小settle。
- **運用:** V=初めのちょん/慣れた返事/満足後の小返事/無応答の完結。接点検分を長くして笑顔を遅らせない。別zone touchも歓迎、target成功は偽装しない。E scenarioで拍手待ちなし。

### P15 Invitation / Open an Unfinished Discovery or Pet — E / 必 / V3 / Q01,Q02,Q04,Q07

- **設計:** 気に入った試みの途中、または好きな感触へ相手を招きたい。
- **演技:** 手元の結果を見る→片前肢の空間を開き/好きな頬を見せる→顔を相手へ→WAIT→有効面ACK→結果を見る短い間と嬉しい顔→続きを選ぶ/満足して終える。下半身は安定。
- **運用:** V=前肢試行を開く/気に入った頬の甘え/頭petの申し出。無応答なら自分の試行/休息へ、返事の正解gestureなし。E scenarioでP14との目的差を読む。

### P16 Delight / I Found Something Nice — D / 必 / V3 / Q01,Q03,Q04,Q07

- **設計:** 面白い結果/触れ合いが分かり、嬉しい。納得→小/大喜び→満足。
- **演技:** 結果を見る停止→顔が明るい→内寄り前肢が一度身へ寄る/ほどける→支持上の胴に小さい意欲→尾が遅れて収まる→顔が温かく休む。ジャンプ/balloon bounceなし。
- **運用:** V=小発見の喜び/相手参加の喜び/大きい納得の喜び。毎回同結果で大喜びしないが好きな接触には常に好意。touchは現在の快へ合流。D scenarioでFX依存なし。

### P17 Surprise / Try a Different Way — B,D / 必 / V3 / Q01,Q02,Q04,Q07

- **設計:** 予想と違う結果を確かめ直し、納得する。意外→関心→別選択/終了。
- **演技:** 動かした部位を止める→目/口の小「おや」→変わった面へ目/頭→一度だけ別の動かし方/対象確認→満足してほどく。非操作側/支持/尾は比較基準として静か。
- **運用:** V=試行結果の意外/user接触の意外/外部対象の無害な驚き。新touchでACK、元条件消失なら実験を閉じる。B/D scenarioで驚き芸/無限再試行を除く。

### P18 Boundary Hint / Keep My Working Space — F / 必 / V2 / Q01,Q03,Q04,Q07

- **設計:** 今の感触/試行を保つ余地がほしい。快/集中→小戸惑い。
- **演技:** 触点側の顔に区切り→使う前肢/頭を自分の範囲へ小さく収める→目は相手を一度認識し元対象へ。尾/下半身は静か。払う手つきなし。
- **運用:** V=同面の過密/集中を割り込まれ続けるhint。優しいpetを自立の理由で拒否しない。解放でP20、継続でP19。F scenario。

### P19 Refusal / Reclaim a Little Space — F / 必 / V3 / Q01,Q03,Q04,Q07

- **設計:** 今の刺激から離れ、自分の関心を守る。戸惑い→明確な境界。
- **演技:** 顔/頭が触点を外す→前肢を安全な作業域へ→必要な小turnで面を離す→相手は認識しながら温かさを失わない。尾で払わず、支持/prop保持を守る。
- **運用:** V=頭petの終了/前肢作業域の保護/body過密からの小withdrawal。解放からP20、別面は局所ACK。F scenarioで挑発/勝ち誇りなし。

### P20 Recovery / Curiosity Returns — F,K / 必 / V2 / Q01,Q02,Q03,Q07

- **設計:** 余地が戻り、自分の関心または気持ちよい交流に戻れる。
- **演技:** 保護した面を楽にする→前肢/頭の緊張が解ける→目/口が温かく→元対象が残れば短く確認→試行/休息を選ぶ。謝罪待ちなし。
- **運用:** V=元の関心へ/好きなtouchと合流。条件が変わった実験を復元しない。user無入力で回復可。F/K scenarioで人格をneutral resetしない。

### P21 Food Notice / Examine, Accept or Refuse — G / 必 / V3 / Q01,Q02,Q04,Q09

- **設計:** Foodの見える形を確かめ、食べるか自分で選ぶ。関心→期待/小拒否。
- **演技:** 目/頭がFoodへ→必要なら届く前肢で保持姿勢→受領前に止まる。1は口を受領させず前肢/頭を楽に引き、相手には好意。食べ物を玩具として投げない。
- **運用:** V=初見の確認/既知の期待/好き度1未消費拒否。2–5はP22、撤去でP25。反復の初見探究は省く。G scenarioで触っただけの消費を偽装しない。

### P22 Food Consume / Five Styles — G / 必 / V5 / Q01,Q02,Q03,Q04,Q09

- **設計:** 受けたFoodを扱い、口で食べ、味を確かめる。
- **演技:** 内寄り前肢/口の接点を整える→style主動作→必要な保持のみ続け、支持/尾は静か→味を見る間。食べるために長い指や尾の把持を追加しない。
- **運用:** V=一口/複数口/なめる/飲む/大きい物。J1の個体script。bite中頭touchは局所ACK、前肢保持維持、safe nodeで主切替。G scenarioで残量と手/口の因果を確認。

### P23 Food Taste / Evaluate and Be Pleased — G,D / 必 / V4 / Q01,Q03,Q04,Q07,Q09

- **設計:** 味の結果を自分で確かめ、好きなら嬉しさが身体に出る。
- **演技:** 味を見る停止→2:口元の微妙さと短い再評価、3:納得し前肢が休む、4:目/顔の喜びと内寄り前肢の小快、5:意外に嬉しい顔から胴/尾の支持された喜び→長い満足。2は吐かない。
- **運用:** V=好き度2/3/4/5。4/5もユーザーへ好意を見せ、検分だけで終えない。消費事実保持、新touchは現在の味/快と共存。G/D scenario。

### P24 Wear / Check the New Feeling — H / 必 / V3 / Q01,Q02,Q04,Q07,Q10

- **設計:** 装着した物の違いを確かめ、気に入った自分で落ち着く。
- **演技:** 視線が提示物→頭上/首胸anchor装着→届く位置は目/前肢が一度確認、頭上は無理に掴まない→顔の納得/喜び→内寄り前肢を休む。尾や手足にWearを付けない。
- **運用:** V=初装着の確認/交換の違い/解除の収まり。1個装備、pull/取り外し遊び機能なし。touchは局所ACK、実anchorと可視面を保持。H scenarioでP03/P14との干渉を確認。

### P25 Afterglow / Keep the Result, Let Go — K / 必 / V3 / Q01,Q03,Q04,Q07

- **設計:** 分かった面白さや受け取った好意を残し、行為自体は終えられる。
- **演技:** 操作前肢が休む→頭/胴が楽な支持へ→尾の小settle→顔に満足→目は相手/結果から自然にrelease。毎回完成した芸を見せ続けない。
- **運用:** V=納得の余韻/相手参加の温かさ/感情peakのないsettle。touchで快保持、未完の結果だけ再開可。K scenarioで操作と気持ちの終了を分ける。

### P26 Session Entry / Already Doing My Thing — B,K / 必 / V3 / Q01,Q03,Q04,Q07,Q11

- **設計:** 自分の関心/休息の続きからユーザーを認識する。
- **演技:** 支持された内寄り前肢/頭の姿勢→目がいまの対象を持つ→短い相手確認と温かい口元→現在の行為へ。新sessionで毎回自分の手を発見しない。
- **運用:** V=関心ありの新session/短い再入場/休息から背景復帰。旧touch/WAITを破棄、Food/Gift事実保持。B/K scenarioで自立と無視を区別。

### P27 Gift / I Chose This for You — J / 必 / V3 / Q01,Q03,Q04,Q07,Q13

- **設計:** 確かめたものを自分から相手へ渡したい。関心→贈る好意→満足。
- **演技:** bounded Giftを短く見る→顔が相手へ→内寄り前肢から提示位置へ→目を物/相手に結びWAIT→受理ACK→前肢の保持を解きtransfer→相手への嬉しい顔。渡す前に延々実験しない。
- **運用:** V=両前肢の低い提示/片前肢assist/確認を省いた親しい提示。新品目/抽選条件なし。保持中touchは非保持部ACK、無応答の気持ちを罰にしない。J scenario/J4。

### P28 Rare / A Little Knowing Wink — L,D / 拡 / V2 / Q01,Q02,Q07

- **設計:** 気に入った結果/触れ合いの後、自分でもちょっと嬉しくなる。満足→遊び心。
- **演技:** 納得した顔→相手を短く見る→片眼の小winkと口元の喜び→両眼が自然に戻る→自分の快へ。全身を揺らさず、他眼/顔のappealを保持。
- **運用:** V=発見後のwink/共有後のwink。通常にも可愛い笑顔を保ち、winkを好意の唯一条件にしない。新touchで自然に両眼の注意へ。L scenarioで常時片眼や人間的勝ち誇りなし。

### P29 Secret Candidate / Roll, Stop, Try Together — I,L / 候 / V2 / Q01,Q03,Q04,Q07,Q12

- **設計:** bounded丸いpropの転がりを試し、相手が変えた結果も楽しむ。関心→予想外/納得→共有快。
- **演技:** prop出現を目で認識→片前肢で小さく転がす→他の支持は残し軌跡を見る→止まったpropを見せWAIT→target tapで動いた結果へ目→一度だけ別の押し方/返し→満足してexit。尾で拾わない。
- **運用:** V=一往復の確認/一度試し方を変える。prop品目/新unlockは未採用、発動P=BOTH候補。無応答は自分で小試行を閉じる、外れに罰なし。I scenarioで現実の動く対象と因果を確認。

## H. Shushu Motion Catalog

**好きな時間を味わう。** 自分で選んだ前肢/荷重の居場所を残し、顔を明確に温かく開いて相手を迎える。ACKを遅らせず、好きな感触には目/口/短い前肢のはっきりした喜びを許す。短脚・小耳・丸い身体・花冠/花束の所属を保持。座位はUで、花束なしでも日常と甘えが成立。達観した大人/無反応のぬいぐるみにしない。全演技P/U、product ruleはA。

### S01 Living / Warmly at Ease — A / 必 / V3 / Q01,Q02,Q03,Q08

- **設計:** 自分の心地よい時間を過ごしている。充足→静かな満足。
- **演技:** 胴/短肢の荷重を安定→前肢は楽な配置→顔に小さい快→目を休める/短く相手へ→blink/小呼吸。小耳は注意時のみ参加し、全身scale呼吸なし。
- **運用:** V=開眼の快/満足したhold/相手へ温かく開いた静止。touchは実面ACK、毎回熟考待ちなし。A scenarioで静止に入る選択が見える。

### S02 Settle into a Chosen Comfort — A,L / 必 / V3 / Q01,Q03,Q04,Q08

- **設計:** この居方/感触がいいと自分で選びたい。中立→好きな快。代表Signature候補。
- **演技:** 支持内で荷重を小さく整える→片前肢を腹前の届く面/楽な位置へ→局所plushが収まる→目/口がはっきり満足→前肢と胴をそのまま残す。短脚を腹へ潰さない。
- **運用:** V=前肢の居場所/片側荷重の快/保持物がある時の居方。座位必須なし。touchは姿勢を保ちS07–09へ、離脱も気持ちは失わない。A/L scenarioで単なる下がるbodyを除く。

### S03 Attention / Warm Recognition — B / 必 / V3 / Q01,Q02,Q08

- **設計:** 好きな時間を保ちながら、実在の変化や相手に気付く。快→関心/歓迎。
- **演技:** 目が対象へ→頭が必要分だけ向く→口元が温かく開く→確認したら自分の手元/居方へ。胴・支持前肢・花冠は安定、冷たい一瞥なし。
- **運用:** V=相手認識/対象確認/好きな対象から相手へ。視線を逸らす前に認識を読ませ、touchでlocalへ。B scenarioで遅い入力や品定めに見えない。

### S04 Small Groom / Care for What I Like — A,B / 必 / V3 / Q01,Q03,Q04,Q08

- **設計:** いまの身体の感触/実在する花束を心地よく整えたい。
- **演技:** 対象を目で選ぶ→片前肢が届く胸/腹面を一度整える、または花束保持を小さく直す→対象を見て満足→前肢を休む。反対支持/花冠は止め、頭上へ腕を伸ばさない。
- **運用:** V=胸面の小care/前肢の置き直し/存在する花束の整え。花束を無条件出現させない。touchは局所ACK、保持が必要なら継続。A/B scenarioで清潔維持の義務や掻き続けなし。

### S05 Rest / Pleasant Drowsiness / Wake — A / 必 / V3 / Q01,Q02,Q03,Q08

- **設計:** 好きな時間を十分味わって休む。満足→眠気、touch→眠い好意。
- **演技:** 前肢/頭を楽な位置へ→顔の温かさのまままぶたが緩む→短肢支持を残すhold→touch面の小受け→目が相手を確かめ、眠さを保つ/起きる。花束を落として眠さを説明しない。
- **運用:** V=休息入口/眠いhold/柔らかい起床。毎回完全覚醒の笑顔にresetしない。A/C scenarioでACKが読める。

### S06 Tap / Poke / I Felt That — C / 必 / V3 / Q01,Q02,Q08

- **設計:** 小さい接触を明確に受け取り、自分の快と両立する。
- **演技:** 実触点の局所受け→同側目/口の評価→顔が温かく開く→胴/前肢の居方はそのまま。大きい動作を待って認識を遅らせない。
- **運用:** V=柔らかいnotice/嬉しいnotice/過密への区切り。zoneでS07–10へ、短いreleaseに後追い全身反応なし。C scenarioで無反応の置物を除く。

### S07 Head Pet / Welcome the Nice Feeling — C / 必 / V3 / Q01,Q02,Q08,Q10

- **設計:** 花冠のない実頭面に届いた撫でを、自分の時間へ歓迎する。
- **演技:** 頭の実面ACK→目/口が嬉しい→頭を楽に開く→前肢の構えを解く→胴/支持を残してhold。花冠は頭所有、頭頂を凹ませて花冠を浮かせない。
- **運用:** V=短い受容/明確なslow快/眠い受容。花冠に当たったら皮膚petと混同しない。releaseはS24、roughはS17。C/H scenario。

### S08 Cheek Pet / Enjoy It Here — C / 必 / V4 / Q01,Q02,Q03,Q08

- **設計:** 自分の快を保ったまま、気持ちよい頬touchを選び受ける。
- **演技:** 同側頬ACK→目/口がはっきり喜ぶ→顔を接点側へ少し開く→不要な前肢の構えを低く解く→選んだ胴/荷重で満足hold。
- **運用:** V=短い歓迎/顔の明確な快/好みの頬を小提示/満足済みの受容。L/R、新sideも即ACK。release後は前肢を楽に閉じ温かさを残す。C scenarioで冷淡さなし。

### S09 Body Pet / Plush Warmth — C / 必 / V3 / Q01,Q03,Q04,Q08

- **設計:** 胴に届いた柔らかい感触を味わいたい。
- **演技:** 触点の小局所受け→顔が同側へ暖かく→前肢を楽な位置へ→胴の選んだ荷重を保って快いhold。腹/腿/短脚を一体に潰さず、全身mochi変形なし。
- **運用:** V=body notice/穏やかなpet/保持物と共存するpet。花束保持前肢は残す。continuousはS11、Wear面は実面を区別。C scenarioで身体の重さと接点を読む。

### S10 Ear-root / Presented-paw Notice — C,F / 必 / V3 / Q01,Q02,Q04,Q08

- **設計:** 小耳の根元/前肢への接触を受け、今の用途に合わせて受容/保護する。
- **演技:** 実面の小ACK→同側顔の評価→耳根の小向き/前肢の楽な配置→温かい口元を残す。小耳を大きく跳ねさせず、保持/支持前肢を投げない。
- **運用:** V=耳根notice/提示前肢の受容/余地を守るhint。S13のtargetは可愛い遊びACK、通常の過密と区別。releaseでS19/S24。C/F scenario。

### S11 Continuous Stroke / Stay with the Good Feeling — C / 必 / V3 / Q01,Q02,Q03,Q08

- **設計:** 好きな感触を急がず味わい、一緒の時間にする。
- **演技:** 経路の実面ACK→顔の快が明瞭→前肢/荷重が楽にほどける→選んだ姿勢でmoving hold→満足ならそれ以上増幅しない。下半身/花冠は静か。
- **運用:** V=快が深まる/十分を味わう/眠い満足。弱い反復は歓迎、roughだけboundary。releaseで押圧を解き快を保つ。C scenarioで認識を「味わう間」に遅延させない。

### S12 Back-and-forth Pet / A Clear Little Smile — C / 必 / V3 / Q01,Q02,Q08

- **設計:** 往復の心地よさにも、小さくはっきり喜びたい。
- **演技:** 反転触点ACK→目/口の嬉しい評価→顔を楽に開く→胴/前肢はその居方で味わうhold。指と一緒にbodyを左右振りしない。
- **運用:** V=小さい遊び快/満ちた受容/十分の穏やかな区切り。解放でS24、rough継続だけS17。C scenarioで笑顔が希少反応に閉じ込められていないこと。

### S13 High-five / Keep a Little Touch in Mind — E,C / 必 / V4 / Q01,Q03,Q04,Q08

- **設計:** 自分が好きな小さい触れ合いを、相手と味わいたい。快→期待→温かい満足。
- **演技:** 支持/保持を安全に確保→顔が相手へ嬉しく→空いた片前肢の面を低く提示→WAIT→target tapの局所ACK→目/口がはっきり明るく、短い前肢が小さく受ける→一瞬その感じを残す→楽な位置に休む。
- **運用:** V=柔らかい一往復/好きがはっきり出る返事/慣れた小返事/無応答の完結。気付きは即時、味わうholdはACK後。両手が保持中は後で誘い、物を落とさない。E scenarioで達観/遅延なし。

### S14 Invitation / Share My Comfortable Time — E / 必 / V3 / Q01,Q02,Q03,Q04,Q08

- **設計:** 好きな居方/感触に相手を迎えたい。自己快→歓迎の期待。
- **演技:** S02の満足した姿勢→顔を相手へ明るく→頬/頭/空いた前肢の面を開く→胴はそのままWAIT→local ACK→明確な嬉しさ→自分で前肢/顔を楽に収める。
- **運用:** V=頬petの招待/頭petの招待/好きな時間の低い前肢offer。無応答は自己快へ、失望なし。別zoneも温かく受け、再offerを連発しない。E scenarioでS13と目的差を読む。

### S15 Delight / This Feels Really Good — D / 必 / V3 / Q01,Q03,Q04,Q08

- **設計:** 好きな感触/共有がとても嬉しい。評価→意外にはっきりした喜び→深い満足。
- **演技:** 目/口が明るい→短い空いた前肢が一度ほどける→胴は支持上で小さく快を受ける→局所plushが収まる→温かいhold。小耳の参加は補助、跳躍や全身elasticなし。
- **運用:** V=顔中心の快/前肢が添う喜び/大きい好きを長く味わう。通常の笑顔も残す。touchで今の快とACKを両立。

### S16 Surprise / Notice, Then Choose What I Like — B,D / 必 / V3 / Q01,Q02,Q08

- **設計:** 不意の違いを確かめ、自分に心地よい次を選ぶ。
- **演技:** 目/口の短い意外さ→顔が原因側へ→胴/前肢の居方は安定→無害なら顔が柔らかく→元の快を続ける/新しい快へ開く。反応の遅さで穏やかさを示さない。
- **運用:** V=触点の意外/対象変化の確認/嬉しい意外から満足。新touchは局所ACK、対象消失で終了。B/D scenarioで老人の達観/鈍感を除く。

### S17 Boundary Hint / Enough for Now — F / 必 / V2 / Q01,Q02,Q08

- **設計:** 今の触れ方は十分なので、自分の心地よい余地を保ちたい。
- **演技:** 触点側の顔が穏やかに区切り→開いた顔/前肢を楽な向きへ戻す→口元の温かさは保持。胴/支持を止め、細目の品定めにしない。
- **運用:** V=同面の過密/休息や保持を守るhint。前肢を単に休めたことは拒否でない。継続S18、release S19。F scenarioで罪悪感なし。

### S18 Refusal / Protect My Comfortable Space — F / 必 / V3 / Q01,Q03,Q04,Q08

- **設計:** 今の刺激を終え、好きな時間を守る。
- **演技:** 顔/頭が触面を外す→必要な小turn/前肢の保護→胴/保持物は安全なまま→相手を認識しつつ触面の余地を取り直す。花束を盾として振らない。
- **運用:** V=頭・頬のoffer終了/body余地/保持前肢の保護。解放でS19、新zoneはlocal ACK。全面背向けや冷たい長い無視なし。F scenario。

### S19 Recovery / My Warm Time Continues — F,K / 必 / V2 / Q01,Q03,Q08

- **設計:** 余地が戻ったので自分の快へ穏やかに戻れる。
- **演技:** 保護を解く→前肢/顔を楽に整える→目/口が温かく戻る→元の居方を味わう。再びユーザーに向くかは選べるが認識は消さない。
- **運用:** V=hint後の回復/withdrawal後の回復。user無入力で成立、穏やかなtouchは合流。F/K scenarioで謝罪/慰め待ちなし。

### S20 Food Notice / Choose a Taste — G / 必 / V3 / Q01,Q02,Q04,Q09

- **設計:** Foodを確かめ、食べたいか選ぶ。関心→期待/小拒否。
- **演技:** 目/頭がFoodへ→短い前肢は必要な保持のみ→好きなら口元に期待、受領位置で待つ。1は口を受領させず顔を穏やかに外し、相手への温かさを戻す。支持/花冠は安定。
- **運用:** V=通常notice/好きFoodの期待/好き度1未消費拒否。2–5はS21、撤去でS24。既知Foodを毎回審査しない。G scenarioで嫌いFoodへの拒否が冷淡にならないこと。

### S21 Food Consume / Five Styles — G / 必 / V5 / Q01,Q02,Q03,Q04,Q08,Q09

- **設計:** 好きな時間の中でFoodを受け、口で食べ、味を見る。
- **演技:** Foodと口/短い前肢の接点を整える→style主動作→胴/保持は安定→味を見る小停止。頭と前肢が離れて食物を浮かせない。花束両手保持と食物両手保持を同時に要求しない。
- **運用:** V=一口/複数口/なめる/飲む/大きい物。J1の個体script。bite中ACKは非口元、safe nodeで切替。G scenarioで摂食と遅い味わいを分ける。

### S22 Food Taste / Savor and Be Delighted — G,D / 必 / V4 / Q01,Q03,Q04,Q08,Q09

- **設計:** 自分の好きな味を確かめ、はっきりした満足として味わう。
- **演技:** 味の小停止→2:微妙な口元から自分で収める、3:普通の温かい満足、4:目/口と短い前肢の小喜び、5:小さい意外顔→明瞭な喜び→選んだ居方で長い味わい。支持/花冠は安定。
- **運用:** V=好き度2/3/4/5。食後2も消費済み、罰や吐出なし。反復は確認短縮、好きの温かさを維持。touchは味の快と共存。G/D scenario。

### S23 Wear / Welcome It without Losing My Shape — H / 必 / V3 / Q01,Q02,Q08,Q10

- **設計:** 着いた物を認識し、自分の好きな見た目/感触に落ち着きたい。
- **演技:** 提示物へ目→耳外側付近/首胸anchor装着→顔の短確認→温かい満足→前肢/胴は楽に保つ。花冠を持ち上げて頭上Wearの場所を作らない。
- **運用:** V=初装着の気付き/交換の違い/解除の収まり。1個Wear、花冠はIdentity、頭上使用は別専用仕様が必要。touchはactual surface ACK。H scenarioで花束/冠/短肢と干渉しない。

### S24 Afterglow / Close the Action, Keep the Warmth — K / 必 / V3 / Q01,Q03,Q04,Q08

- **設計:** もう十分味わったので行為を閉じ、温かさは残す。
- **演技:** 開いた前肢/顔を楽な居場所へ→胴の局所plushが荷重に従い収まる→目/口に好意→手元/自己快へ注意release。相手へ冷たい背向けを挟まない。
- **運用:** V=共有した快/自分の快/peakのないsettle。新touchはその温かさからACK。

### S25 Session Entry / My Pleasant Time Is Here — B,K / 必 / V3 / Q01,Q03,Q04,Q08,Q11

- **設計:** 今の満足/休息の中へ相手を迎える。
- **演技:** 支持/前肢/保持物の整った姿勢→目が今の注意を持つ→顔の温かい相手認識→必要な小settle。毎回無表情から歓迎に切り替える仕様にしない。
- **運用:** V=新session/短い再入場/眠気から背景復帰。古いoffer/touchは解き、Food/Gift事実保持。B/K scenarioで不在への不満なし。

### S26 Gift / A Little of What I Like, for You — J / 必 / V3 / Q01,Q03,Q04,Q08,Q13

- **設計:** 自分が気に入ったものを相手に渡したい。自己快→贈る好意→温かい充足。
- **演技:** bounded Giftを大切に準備→顔が相手へ→短い前肢で安全な低い提示→保持を止めWAIT→受理ACK→保持を解きtransfer→嬉しい顔と居方を残す。手を伸長せず、既存花束を必ず贈ると決めない。
- **運用:** V=両前肢の低い提示/空いた片前肢assist/支持優先の近い提示。品目/抽選率U、product条件維持。両手保持衝突は安全な置き場が必要で、物の消失で解決しない。J scenario/J4。

### S27 Rare / A Little Smile Remains — L,D / 拡 / V2 / Q01,Q02,Q08

- **設計:** 触れ合いの後にも、その感じを自分からもう一度嬉しく思う。
- **演技:** S24で落ち着く→口元がふと明るい→目が相手へ短く温かく開く→前肢は居場所を保つ→自分の快を続ける。恒常的な閉眼や意味不明な頷きなし。
- **運用:** V=共有後の思い返し/好きな感触の思い返し。通常笑顔をrareへ移さず、新touchで今の嬉しさへ合流。

### S28 Secret Candidate / Bouquet Peek and Welcome — I,L / 候 / V2 / Q01,Q03,Q04,Q08,Q12

- **設計:** 実在する花束越しに相手を覗き、好きな時間へ迎える可愛い遊び。
- **演技:** 花束を見て満足→短い前肢で届く範囲の顔下へ少し提示→目/片頬と花束を同時に残すWAIT→visible cheek/開口tapの局所ACK→顔を温かく開く→花束を安全な保持へ戻し余韻。花冠を外して花束代わりにしない。
- **運用:** V=花束下から小peek/片頬を開くpeek。花束のasset/保持開始・退出、所有/発動P=BOTH候補は未承認。両手の支持と遮蔽U、無応答は自分で花束を味わい閉じる。I scenarioでS14の通常甘えとinteractive themeを分ける。

## I. Character-Specific Performance Variants and Selection

### I1. 同じ入力で何が変わるか

| Situation | Jill | Pino | Shushu |
|---|---|---|---|
| 頬slow pet | J07。頬の快を胸/顔の共有へ開く | P09。気に入った感触を確かめ、前肢の集中を解く | S08。選んだ胴/前肢の居方を保ち、嬉しい顔を開く |
| High-five contact | J12。返事の宛先へ顔/胸が開き、一往復で満足 | P14。接点の違いを一瞬見て、相手へ嬉しい顔 | S13。即ACK後に好きな感じを短く保ち、前肢を休む |
| 同じpetを10回 | J06/J10。毎回大きい翼peakを足さず共有満足 | P08/P12。既知の感触を再発見せず楽しむ | S07/S11。好きの顔を残して同じ快を味わう |
| 無応答WAIT | J13。前から楽しかった私的快へ戻る | P15。残っている試行を自分で続ける/休む | S14。前から好きだった居方へ顔を戻す |
| 喜び途中に反対頬touch | 胸/翼の広がりを小さくして新sideを向く | 手元を安全に保留し、新触点を受ける | 胴/保持を残して顔を新sideへ開く |

初回profileは意思を確かめる段階を広めに、慣れたprofileは確認を省いて快を早く見せる。眠いprofileもACKは明確。強いprofileは参加部位と結果holdが増え、小さいprofileは顔/触点だけでも十分可愛い。違いを振幅/速度/左右mirrorだけに還元しない。

profile選択は、**今の欲求がまだあるか→支持/保持が可能か→この面/gestureをどう感じるか→直前に同じ意味を完了したか**の順で考える。family cooldown中でも通常の好意とlocal ACKは返す。反復が続いたらfamilyを無理に替えて驚きを増やさず、満足した受容を続ける選択も正しい。

### I2. 代表演技の代替比較

| 対象 | 比較した候補 | 本書の推奨 / 理由 / 未確定 |
|---|---|---|
| Pinoの自発試行 | Phase 2の手合わせ・離す / P03片前肢の置く・押す・上げて見る / P04小turn後の尾確認 | **P03を日常の第一候補P**。片側行為→結果を見る停止が明瞭で拍手/手揉みを避けやすい。前肢先端/視線/接点が見えることはU。手合わせは非対称の一試行として保留可能、独立Familyには数えない。P04は視認条件がある拡張で、coreの代替にはしない |
| Jillの招待 | 伸びの姿勢をそのまま長く保つ / J13で顔の宛先と前肢の空間を変える / J12片前肢のHigh-five | **J13とJ12を目的で使い分けるP**。伸びを止めるだけではstretch holdに見えるため、顔を相手へ・応答後の胸の喜びを必ず持つ。High-fiveは接触面が明確だが常用の招待をそれだけにしない |
| Shushuの静けさ | 熟考後の遅い笑顔 / S02の自己姿勢＋S06即ACK / S15のはっきりした好き | **自己快＋即ACK＋明瞭な喜びP**。温かさを速度差で説明せず、接触前の居方と接触後の完結で本人らしい違いを作る。小顔/手元の可視性U |

これらは期待する可読性の比較であり、実演で最適と証明した選択ではない。Humanが手合わせを最も可愛いと感じれば、Identityを保った演技候補として選べる。現在の候補を守るために癒し/可愛さを犠牲にしない。

## J. Touch / Food / Wear / Special / Secret / Gift Integration

### J0. Gesture × zone composition

tapは短い一接触のnotice、pokeは局所に留まる押し/繰り返しの評価、slow petは穏やかな面移動の快、continuous strokeは現在の経路と快の深まり、back-and-forthは方向反転を受ける快/飽和として区別する。tap/pokeは同Family内でも、短い気付きと留まった面の受けを演じ分ける。新しい力センサーは要求しない。

| Character / zone | Tap / Poke | Slow Pet | Continuous Stroke | Back-and-Forth |
|---|---|---|---|---|
| Jill head / cheek / chest-body | J06/J07/J08で局所notice | 各J06/J07/J08で快 | J10＋実面ACK | J11＋実面ACK |
| Pino head / cheek / chest-body | P07→P08/P09/P10 | 各P08/P09/P10 | P12＋実面ACK | P13＋実面ACK |
| Shushu head / cheek / chest-body | S06→S07/S08/S09 | 各S07/S08/S09 | S11＋実面ACK | S12＋実面ACK |
| 他3匹の付属根元 / 提示前肢 | J09/P11/S10。offer中はJ12/P14/S13のACK | 根元は低い受容、提示面は交流を閉じず快を受ける | 局所面を保ち小受容。支持/保持競合ならhint | 反転ごとの全身追従なし。rough過密だけFへ |

同じgestureでも触面の材質/用途を保ち、前肢提示中のtapは遊び、支持前肢へのpokeは保護が必要になり得る。口内/目や非露出面を新zoneに追加しない。ここは演技routingのPであり実装の入力分類/閾値を決める仕様ではない。

### J1. Five eating styles — 全3匹の接点と時間

PRODUCT §10.4の5分類を全員で設計する。**一つのitem使用で複数口食べても消費は基本1個**。好き度1はstyleに入らず未消費、2–5は食べる確定からDATA §21に従う。演技の途中にエラー/取消があっても、食べていない物を減らす/食べた物を再表示する設計にはしない。確定safe nodeの実装位置はU。

共通時系列は **notice→受領面/保持を整える→style→味の短い評価→好き度→個体の余韻**。各styleの主行為は次のとおり。

| Style | Jill J20 | Pino P22 | Shushu S21 |
|---|---|---|---|
| SMALL_ONE_BITE | Foodを見て小期待→口で一口→胸は安定→処理後に顔が味を見る。喜びの翼は食後 | 前肢assistが必要な時だけ保持→口で受領→前肢を低く収め→目/口が結果を見る | 短前肢/口の届く位置で受ける→一口→保持が不要になれば楽に休む→味を見る。花束との保持衝突を先に解く |
| MULTI_BITE | 必要な前肢保持を安定→口/頭の小biteを区切る→最後に胸/顔が評価。翼は保持を妨げない | 内寄り前肢で保持→食べた部分/残量を一度見る→持ち直して次bite→最後に納得。毎口「初発見」なし | 短前肢の届く範囲で保持→小bite→口の処理→次bite。十分食べてから長い味わい、食べる途中に全身沈みを足さない |
| LICK | 舐める面に口を向ける→短い口動作→胸/翼は止める→最後の顔評価 | 前肢で面を整え、口で舐める→一度面を確認→必要分継続→終了。器用な指回しなし | 安全な保持/提示面に口を合わせる→小さい口動作→好きな味を見る間。短腕を伸ばさない |
| DRINK | 必要な支えを確保→口の受領→胸は安定したまま飲む→口を解き評価。大きい首反りなし | 内寄り前肢が届く容器を支える、不可なら外部提示→口の接点を保つ→飲む→安全に戻して評価 | 短前肢の保持/外部提示を成立させる→口の接点→小さい飲み動作→物を安定させてから味わう。容器を腹へ貫通させない |
| LARGE_EAT | 必要な前肢brace→口の到達→小biteと処理→最後に支えを解き評価。翼を食物把持にしない | 両前肢/外部提示で安定→口が届く部分を選ぶ→bite後に残りを見て持ち直す→終了。尾で掴まない | 短前肢で届くboundedサイズまたは外部提示→口の到達→小bite→propを安全に戻す→満足。顔や腕を拡大して食べない |

飲むための容器/舐める面/大物の支えはitemごとのprop contractで必要。ここで新Food品目や容器の永久所有を正式採用しない。数値サイズ・舌/口の露出範囲・外部提示の接触方式はQ09のU。限界があればbounded propサイズ/提示を調整し、Canonicalの口/腕を拡大して解決しない。

好き度2は「食べた後の微妙さ」、3は普通の満足、4は嬉しい好き、5は明確な大喜びと長い余韻。喜びの結果はJ21/P23/S22にある。5を常にジャンプ、2を敵対的拒否にしない。

### J2. Wear staging and ownership

装着前の視線確認→旧Wearがあれば安全に外す→新Wearを指定anchorへ→その場所の認識→本人らしい快/関心→余韻。解除は現在の支持を保ち、旧物への小noticeから行為を閉じる。任意screen位置へ置く/二つ同時に着ける/取り付け直後に揺れ続ける演技は作らない。

| 個体 | 正式な位置候補 / performance composition | 保護部位と干渉 |
|---|---|---|
| Jill | horn/leaf非干渉の頭中央、首/胸。J22 | 翼・尾・葉先には付けない。胸の開き/前肢/翼根元のclearance |
| Pino | 頭上、首/胸。P24 | 太い尾/手足/試行接点を避ける。P03/P14で物が前肢へ貫通しない |
| Shushu | 耳外側付近、首/胸。S23 | 花冠はCanonicalの所属。頭上Wearは原則不可、交換専用仕様なしに冠を外さない。花束保持/顔/短腕のclearance |
3匹は「新しい装着感をどう受け取るか」を個体の一つのFamilyにまとめた。安全anchorの位置は造形確認でU、表の候補を実測済み座標としない。

### J3. Special and Secret protection / proposals

| Content | Status / motion routing / ownership |
|---|---|
| Jill / Pino / Shushu Special | 正式な具体品目は今回参照Authorityで未決定。FoodならJ19–21/P21–23/S20–22＋固有余韻、WearならJ22/P24/S23、Secretなら承認された個別Familyへ。対象Grimo限定、消費はFood型だけ。新しいSpecial名/個数/レア度/好き度を勝手に決めない |
| J27 / P29 / S28 | **P/U** 原創Secret候補。interactive performance/prop/exitは設計済み。採用、名称、itemId、所有/発動方式、cooldownはHuman未決定。未承認のまま解放/実装しない |
| 共通High-five | J12/P14/S13。日常交流テーマP。新Secret商品/アンロック条件にはしない。 |

Secretは「遊びを所有」する。propがある場合はsetup→visible target→WAIT→main turn→必要な次turn→settle/afterglow→removeまでを一つの体験として追跡。普通のTouchは認識するがゲーム成功と偽装しない。間違い/late/無応答を失点にせず、再提示または自然な終了。所有なし/activation権限なしは演技を開始しない。candidateのBOTHは提案でありPRODUCTのUSER_ONLY/AUTO_ONLY選択自由を奪わない。

### J4. Gift event boundary

全員 **本人の準備→気付いてほしい顔→物の提示→WAIT→受理/transfer→身体の余韻→Collection/owned記録**。Foodの受領とGiftの贈与は向きが逆。品目・超低確率・session判定・永久所有・通常宝箱別枠を変えない。贈る意思はUIや発光より前に読めること。

DATA §24は「渡す→Collection作成→owned→RewardEvent」を規定し、FINAL はaccept/transferを持つ。一方、**WAIT中の無応答/離脱の具体終了時間、未受理Giftを再提示する保存方式**はこれらの参照節では未確定。ここではgrantを早める/没収する/無限保持する新ルールを作らない。推奨Pは提示を安全に閉じ、既存商品状態と整合する再提示機会を持つこと。O5でHuman/下流設計対象に残す。受領済みGiftは永久所有を保ち、演技中断で取り消さない。

## K. Transitions / Interruption / Afterglow

### K1. 切替時に残すこと、解くこと

| Current → event | 即時ACK / 主行為の接続 | 保持 / 終了 |
|---|---|---|
| Idle/意味あるhold → touch | 実触点側の短ACK→今の顔から評価→必要な頭/胸だけ参加 | 支持/快/眠さを保持、正面Neutral待機を省く |
| 頬lean → 反対側 | 新面ACK→旧面のcommitを解く→支持内で新側へ | 温かい顔を保つ。旧面の圧縮と新面の圧縮を同時に過大にしない |
| 継続stroke → release/cancel | 当時の深さで局所押圧を解く→頭/胴を自重支持へ→余韻 | 押され続ける形を終了、快は継続。無効inputを再playしない |
| WAIT → target tap | 提示面ACK→そのFamilyのpayoff | 有効offerの目的を保持、接触前に成功を出さない |
| WAIT → 別zone touch | 別面ACK→そのtouchを嬉しい交流として受ける→元offerを閉じる/小さく保つ | 別zoneをtarget成功とはしない。正解を要求しない |
| WAIT → 無応答 | 提示を安全に解く→個別の自己活動/満足へ | 希望の顔を失望へ反転させず、再offerを連発しない |
| 喜びpeak → touch | 非競合の触点/顔ACK→残りの大動作を小さくredirect | 快/支持/prop保持。最初から最大喜びを足さない |
| Pino試行 → 頭touch | 頭ACK→手元を安全な位置で止める→嬉しい顔 | 未完の関心。条件変化後に同じ接点/結果を復元したふりをしない |
| Food bite → touch | 非口元local/顔ACK→bite/保持のsafe node後に主切替 | Food/口接点、消費確定の事実。旧inputを後追いしない |
| Gift transfer → touch/離脱 | 非保持部ACK→transferを破壊しない区切り→現在の状態へ | 受理/所有事実。物の瞬間移動/二重grantなし |
| Boundary → release | 局所保護を解く→支持/顔の温かさを自力回復 | 刺激からの距離の理由。謝罪/入力を回復条件にしない |
| 眠気 → touch/Food | touchは眠いACK、Foodは対象認識→安全に頭を整える | 眠気を消し飛ばさない。口へ無理に物を押し込まない |
| Wear中 → 他行為 | anchor所有を維持し、必要channelだけ主行為へ | 1Wear/顔可視性、既存装飾。物を消して可動を稼がない |
| 背景/画面復帰 | 無効触点/offerを解く→保存された商品事実と経過を整合→Entry | 罰なし。裏で実時間animation/報酬完走を仮定しない |

**同時接触:** 受理された各面にACKする。主姿勢は支持/保持/現在の意思に基づく一つの選択とし、左右のmacro leanを加算しない。一方を捨てたことを無反応に見せず、頭/顔/局所面で認識を返す。入力の受理数や優先ルールそのものは新しく固定しない。

### K2. Channel ownership / safe interruption

gaze/headは現在の注意対象、faceは評価/感情、口と保持前肢はFood/Giftの接点、下半身/蹄は支持、固有付属は選択的補助、Wearは所有部位anchorが担当。新Familyへ移る時、全部を同時に明け渡さない。食べる口に笑顔の大きい口動作を重ねない。支持移行中に足を装飾的に動かさない。

**どの姿勢で局所ACK可能か/どの安全な接点で主切替できるか**をQ03/Q09/Q13で下流へ渡す。ACKが可視でない長いprotected windowは設計上の問題として戻す。
### K3. 3–5分の連続体験 trace（時刻を固定しない）

1. 無入力でそれぞれの生活がある。Jillは私的な快、Pinoは短い試行後の観察、Shushuは選んだ居方。代表Signatureを全てこの区間に出す義務はない。
2. 左頬slow pet。全員にlocal ACKと可愛い快。Jillは共有、Pinoは気に入った感触、Shushuは自己快への歓迎へ。
3. 右側へ変更/早期release。旧commitと新ACKが連続。頭/胴は現在姿勢から収まり、表情を一度消さない。
4. 同じ優しいpetを反復。既知の快を小さく楽しむ。入力が過密/roughの場合のみhint→拒否→withdrawal。解放後は全員自分で回復。
5. 自発invite/High-fiveの機会。応答なら触点から喜び、無応答ならその前からの快へ。通常の可愛い反応をrareまで待たせない。
6. Foodを一つ提示。好き度1なら未消費、2–5ならstyle→評価→余韻。bite中の頭touchにもACK。Wearがあればanchorを保つ。
7. 満足した無入力時間。既に完了した試行/誘いを初回として再演せず、顔/姿勢/次の注意に前の出来事が残る。Giftはproduct eligibilityが成立した時だけ、traceの定例報酬にしない。

これは将来の受容scenarioであり、今の3Dや実機でPASSした記録ではない。

## L. Visual Readability Design Audit

**一巡の文書監査。** 全A–L coverage、23項目の参照構造、重要Familyの時系列、身体要求を確認した。以下は設計上の成立条件/未解決リスク。動く姿・可愛さ・実機のPASSではない。
| Question /重点対象 | 文書上の根拠 / 対処 | 未検証・失敗条件 |
|---|---|---|
| 意思が説明なしに読める構造か | J12–13、P03/P14–15、S02/S13–14に見る→選ぶ面→止まる→結果の顔を明示 | offer前の動機や接点が隠れると不足。単一poseで人格を判定しない |
| Touchと反応の因果 | C2 zone map、全Touchに面/side ACK、K1でside/release/同時接触を分けた | 大きい喜びに局所が消える、中央macroへ潰れる、ACKが見えない長い保護はFAIL |
| stretch/random motionではないか | JillのJ03私的careとJ13共有への宛先を別設計。P03行為→観察→納得 | Jillの胸を開いて止めるだけ/Pinoの操作と結果が見分けられない場合は演技修正 |
| 静止が無反応ではないか | 全Lifeに入る選択/顔/注意release、Shushu即ACK、WAITに提示面と期待 | 静止に入る動作/対象が見えず、ただ低速/閉眼なら不足 |
| 感情は顔・身体・時間にあるか | 顔→小胴→安らぎ、J14胸の喜び、P16結果→喜び、S15好き→短前肢→満足 | 音/FXを外すと嬉しさが分からない場合は意味未成立 |
| 全3組の差 | I1: Jill返事/Pino結果/Shushu居方。共通遊びでもOutcomeが異なる | 同clipの速度/表情だけなら未達。Sは接触前後の胴/前肢、J/Pは最後の視線対象を比べる |
| 重み・支持・接触に矛盾がないか | 全カードの止める支持、Q03/Q04、Food/Gift safe node | 手を上げる時の荷重、短肢到達、実際の可動域はU。尾を支柱にして成立扱いにしない |
| 反復・割り込みで人格が消えないか | 全カード運用＋K。既知の確認短縮、快保持、未完だけ再開 | 10回petで同chain/無理由の拒否/古いtouchの遅延再生ならFAIL |
| smartphoneで意味が見えそうか | 顔と提示面を同時に残す、低前肢でも見える面、重要primaryはfront可読 | 蹄の羊毛遮蔽、P03小接点、S13/S28前肢/花束遮蔽、J27翼の顔隠しは高リスクU。カメラorbitで救わない |
| Canonicalを変えていないか | 長腕/巨大口/人間眉を要求せず、horn-like/厚い尾/花冠/羊毛所有を保護 | ポーズ実現のため比率/所属/幼さが変われば候補を戻す。見た目のHuman判定が必要 |
| 商品coverage/locked content | Jで消費/所有/装備/activation、個体別contentの保持 | DRAFT Secretを既存商品扱い、High-fiveを新unlockへ変換、Gift時点の推測採用は不可 |

**優先して見直す条件:** ①P03接点/戻りが読めないなら見える置き方へ戻す、手合わせを唯一解にしない。②J13がstretchに見えるなら顔の宛先/応答後の変化を強める。③S01が同じ静けさなら接触前の選択と終了後の姿勢を再評価。④High-fiveが身体上成立しないなら低い提示面/支持を見直す。魅力を落とすと分かっている代替を「技術的に楽」で採用しない。

## N. 3D Capability Dependency Index

**これはPhase 4への要求索引であり、詳細Anatomy/Rig設計ではない。** 共通の基礎能力Q01（顔/注意）、Q02（頭）、Q03（支持）と各身体所有Q06–Q08は該当個体の全Familyに適用する。見出しのQは特に負荷がかかる能力を示す。例えばQ09は食前/摂食だけでなくFood結果と消費状態の引継ぎまで適用。下表からFamily群へ、カードからQへ双方向に辿れる。

| Capability / Family links | 必要な独立部位・変形/接触/支持 | 造形・視認・干渉 / Unknown |
|---|---|---|
| **Q01 Face / evaluation / attention** — 全Family、特にJ06–15,J21 / P03,P07–17,P23,P28 / S06–16,S22 | 両眼/まぶた、視線、口元/頬の小評価。touch側の顔と他側、blinkと感情、咀嚼口と非口元ACKの独立。必要な軟部の局所受け | Canonical眼形/placement/幼さを保持。小顔で認識/快/微妙/期待が読める範囲U。新しい眉/巨大口を前提にしない。winkの閉眼側/両眼復帰が必要 |
| **Q02 Head / neck / gaze relation** — J02,J05–07,J10–13,J15,J19–22 / P02,P06–09,P12–15,P17,P21–24 / S03–08,S11–14,S16,S20–23 | 目だけの注目、頭の必要分turn/lean、頬L/R/額の接触面提示、releaseの向き変更。目と頭のleadを分離 | 首露出/顔の羊毛や葉への埋没、花冠/頭Wear干渉、3/4での顔の連続。可動range/接点追従U。screen-leftをanatomical Lに固定しない |
| **Q03 Support / weight / quiet body** — 全Family、特にJ03–05,J12–14,J17,J20,J25 / P03–06,P14,P16,P19,P22,P27,P29 / S02,S05,S13,S15,S18,S21,S26 | 接地支持の保存、片肢解放時の荷重移行、胴の小圧縮/leanとstable hold、active-pose settle。動かす支持と止める支持を分離 | tail支柱を仮定しない。Pino/Shushu座位、Jill通常支持はU。転倒/foot sliding/short-leg collapseが極端姿勢リスク |
| **Q04 Forelimbs / hoof-paw surfaces** — J03–04,J12–14,J17,J20,J25,J27 / P03,P05,P11,P14–19,P21–27,P29 / S02,S04,S09–10,S13–15,S18,S20–26,S28 | 一前肢提示・対側の支持/保持、接触面の向き、前肢を休む/戻す、bounded prop保持/brace。左右独立、届く自己面、P03片側操作と結果観察 | 短い比率のまま到達/前肢先の可視性が必要。長い指/人間手首/腕伸長を足さない。手を出せる姿勢の支持はU。hoofはpadを新設せず実蹄面 |
| **Q06 Jill chest / wings / leaves / tail** — 全Jill、特にJ03,J07–14,J17,J21–23,J25–27 | 胸/前肢の主喜びと片/両翼の選択参加、翼根元接触/閉じる、葉/花の局所follow/settle、尾根元と太い尾の重量追従。horn-like頭部は固有anatomy | 翼と腕/葉/胸Wearのclearance、翼の顔遮蔽、葉根元所属、clover等canonical marking保持。翼膜/角の材質を軟部ACKで改変しない。飛行能力は未要求 |
| **Q07 Pino rounded body / thick tail** — 全Pino、特にP03–05,P09–16,P22–29 | 内寄り前肢の独立、前肢先の接触/形状回復、丸い胴と支持肢の分離、太い尾のbody-follow delay、両眼と単発wink | tail/胴/足の融合、self-contact到達、前肢が腹に埋まる姿勢、P03の前肢先の見え方U。尾の前巻き/把持/独立balloonは要求しない |
| **Q08 Shushu plush / short limbs / flowers** — 全Shushu、特にS02,S04,S08–15,S21–28 | 局所荷重compression/settle、短前肢を休む/提示する、短脚/腹/腿/足裏の区別、小耳の独立、花冠の頭所属/実花束の保持 | sit/低姿勢で腹脚を潰さない。花束とFood/Gift/前肢提示の同時保持、冠/頭/耳Wear干渉、花束peekでの目/頬遮蔽U。花束なしでもcore演技成立 |
| **Q09 Mouth / Food / style5** — J19–21 / P21–23 / S20–22、§J1 | 口/頭の受領接点、咀嚼相当の小動作、舐める面/飲む面、残量/複数bite、前肢brace、pre-consume拒否、消費確定/評価引継ぎ、bite中非口元ACK | 舌/口の可視range、容器/大物のbounded寸法、顔を隠さない保持、safe node U。口の大scale/食物瞬間消失だけで摂食を代行しない |
| **Q10 Wear / motifs / owned anchors** — J22 / P24 / S07,S23、§J2 | ownerに属するanchor、装着/交換/解除、顔/目/重要モチーフ保護、衣装面と身体touch区別、1装備状態 | 各候補anchorの実座標/clearance U。Jill角/葉/翼、Pino試行面、Shushu冠/花束を守る。物を浮かせて干渉解消しない |
| **Q11 Session / visible current state** — J24/P26/S25 | 初めの可視poseで支持/現在感情が成立、背景復帰時の無効接触/WAIT解放、商品/受領事実と姿勢の整合 | 見えない間の連続animationを要求しない。復帰の接点/未完prop整合U。カメラで破綻面を隠す構築不可 |
| **Q13 Gift presentation / transfer** — J25/P27/S26 | 本人の意図を示す注意、bounded prop保持/提示、受理ACK、保持解放とtransfer、非保持部touch、owned/Collection境界 | 物を出す/置く/しまう具体位置、短肢のreach、花束との保持衝突、無応答/離脱時の再提示U。gift品目/発生率を造形から新設しない |
| **Q12 Interactive Secret / targets / props** — J27 / P29 / S28 | setup/target面/WAIT/応答/exit、body接点とprop軌跡/遮蔽、側替え、受領のない通常touch、propの安全remove | 3候補のprops/activation/clearanceはU。特定preset/solver適合の決定はしない |
**カメラ横断要求:** frontの小顔/触点/前肢提示を同時に読めること。3/4・turn・lean・低頭・propの接近で露出する面は空間的に成立すること。耳/翼/尾がframeに収まるだけでなく、目/口の意味が小さくならないこと。旧Eevee16:9比率を3匹の固定値へ転用しない。上表の能力が不足なら、意味を保つ姿勢/提示/演技を再設計し、Canonical改変を前提にしない。

## O. Unresolved Questions / Human Decisions

| ID | Concrete decision / 推奨案 | 保護する条件 / U |
|---|---|---|
| O2 Experience Identity / signature preference | Phase 1・2の3核と、本書の具体演技をDRAFTとして判断。PinoはP03第一候補、Jill J13、Shushu S02＋即ACK | 新人格を承認済みにしない。手合わせがHumanに最も可愛ければ候補に戻せる。文書だけで知覚PASS不可 |
| O3 Body/normal pose limits | 全Motionに必要な独立部位/面/支持をNから逆算して次工程で設計 | Pino/Shushu座位、Jill支持、短肢到達、口、Peek、rig方式はU。ボーン数/関節角/shape構成未確定 |
| O4 New Special/Secret content | J27/P29/S28は原創候補。Specialの個別品目は正式決定を入力待ちにする。性能/可愛さが分かる範囲で採否 | 新itemId/rarity/獲得条件/所有/activationを正式追加しない。候補を採用しなくても通常の触れ合いの魅力を維持 |
| O5 Unanswered Gift / interrupted item boundary | GiftのWAIT無応答/画面離脱、Foodconsume確定safe node、花束と複数保持の整合を下流で定義 | DATAの渡す→記録、食べる確定→消費、永久所有、罰なしを保持。再提示の保存/消失/取得を推測実装しない |
| O6 Smartphone readability / appeal | 顔/ACK/接点が読める姿勢を優先。重要primaryは音/FX/外部propsなしでも核が成立 | 実物/スマホ/最終Human知覚は未実施。Xiaomi 14T Proが現行実機truth、Pixel 7a-classはUNVERIFIED_TARGET |

これらは今の文書設計を止めるための質問ではなく、DRAFT承認/次工程で判断できる具体的な境界。Humanが求める可愛さを失う取捨選択は技術判断だけで確定しない。

## P. Phase 4 Handoff / Completion Ledger

| Character | 本書Family | 基本variant profile | 内訳 / 採用状態 |
|---|---:|---:|---|
| Jill | **27** | **81** | 日常/商品対応26 / 79（J26拡張を含む）＋未承認Secret候補1 / 2 |
| Pino | **29** | **86** | 日常/商品対応28 / 84（P04/P28拡張を含む）＋未承認Secret候補1 / 2 |
| Shushu | **28** | **85** | 日常/商品対応27 / 83（S27拡張を含む）＋未承認Secret候補1 / 2 |
| Total | **84** | **252** | 左右/gesture/品目/接続の条件合成を乗算しない。制作済みclip数/正式商品数ではない |
**次工程への入力:** F–Hの演技/variant、Dのcoverage、Iの代替比較、Jの商品/接点、Kの連続性、NのQ01–Q13、OのHuman/U。これらから「全Motionに必要な身体能力」を逆算する。生成pose、rig rest pose、通常ゲームposeは別として扱う。

**Phase 4で解くこと:** 顔/頭/付属/前肢/支持の独立性、局所変形、接点と保持、Wear/装飾干渉、極端poseの破綻、front/3/4の可視性を能力契約にまとめ、未達時に意味/可愛さを保つ代替を明示する。Tripo生成前に要求が欠けないことを目指す。具体bone数、rig方式、weight paint、shape key、Tripo/preset適合、credit、生成はPhase 3では未決定/未実行。
