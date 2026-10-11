# Grimo — Motion Evidence Pack DRAFT

**Date:** 2026-10-11

**Status:** PHASE_0_EVIDENCE_COMPRESSION / DRAFT — 新しいMotion承認仕様ではない

**Scope:** Carol / Jill / Pino / Shushu。Phase 1 Astra / Highへの根拠圧縮のみ。
**Source revision:** `e775f1aeb139c27f4cae39479a9260d1c7be4743`（設計ブランチでの参照開始HEAD）。この文書は同revisionの資料を抽出し、動画再解析・外部主張の再検証は行っていない。

## Source navigation / evidence labels

リンクは本ファイルからの相対パス。節番号・見出し・Family ID・動画内時刻を併記する。出典の区別を維持する：

- **A — Approved / authority:** 現行正式仕様・明示Human決定。実装済み/PASSの意味ではない。
- **O — Observation / measured:** 原資料の `[V1]` に記録された可視事実・計測。今回はその記録の抽出であり、新規直接観察ではない。
- **T — Temporal inference:** 原資料の `[V2]`。近接frameからの時間的推定。
- **I — Interpretation:** 原資料の `[I]` や研究のD。意図、原因、空間的要件等の解釈。内部アルゴリズムの証明ではない。
- **X — External claim:** 研究が開発者・公式・心理学資料等に帰属させる主張。原資料のA/B表記を保持するが、本Phaseでは一次ページ未再検証。
- **P — Proposal:** 原資料の `[G]` / E、推奨数値、歴史的Grimo案。別の正式仕様に採用が確認できる場合だけAを併記。
- **U — Unresolved:** 未確認・未測定・未承認。空欄を推測で埋めない。

| Key | Source / role |
|---|---|
| PLAN | [Six-phase plan](GRIMO_FOUR_CHARACTER_MOTION_ZERO_BASED_PLAN_20261011.md) §§0–4 — 今回の境界、最終Goal、次段階のHuman Gates |
| INDEX | [Knowledge Index](../../grimo/knowledge/GRIMO_PROJECT_KNOWLEDGE_INDEX.md) — Authority入口 |
| NORTH | [Product North Star](../../grimo/knowledge/GRIMO_PRODUCT_NORTH_STAR_AND_MINIMUM_REQUIREMENTS.md) — 最高位の製品品質要件 |
| EXP | [Character Experience Spec](../../grimo/knowledge/GRIMO_CHARACTER_EXPERIENCE_SPEC.md) — 4匹の正式体験仕様 |
| ARCH | [Production Architecture](../../grimo/knowledge/GRIMO_CHARACTER_PRODUCTION_ARCHITECTURE.md) — 空間・可動能力の要件 |
| OPS | [Production Operating System](../../grimo/knowledge/GRIMO_PRODUCTION_OPERATING_SYSTEM.md) — Authorityと制作方法の分離 |
| CAROL | [Carol FINAL Motion Spec](../../grimo/knowledge/character-production/carol/CAROL_MVP_MOTION_SPEC.md) — Carolのみの既承認契約 |
| STATE | [Carol Production State](../carol/CAROL_PRODUCTION_STATE.md) — mutable実行routing |
| LIVING | [Living Companion Research](../../grimo/knowledge/research/GRIMO_LIVING_COMPANION_EXPERIENCE_RESEARCH.md) — 開発者資料・観察・解釈・歴史的提案が混在 |
| E-AN | [Eevee Video Analysis](../../grimo/knowledge/research/GRIMO_PARTNER_EEVEE_VIDEO_MOTION_ANALYSIS.md) — 5本の詳細観察 |
| P-AN | [Pikachu Video Analysis](../../grimo/knowledge/research/GRIMO_PARTNER_PIKACHU_VIDEO_MOTION_ANALYSIS.md) — V01/V02/V03/V05の詳細観察 |
| E-M | [Eevee Master Inventory](../../grimo/knowledge/research/motion-masters/EEVEE_MOTION_MASTER_INVENTORY.md) — 11本の既存Inventory正規化 |
| P-M | [Pikachu Master Inventory](../../grimo/knowledge/research/motion-masters/PIKACHU_MOTION_MASTER_INVENTORY.md) — 6本の既存Inventory正規化 |
| ANATOMY | [Motion Anatomy Evidence](../../grimo/knowledge/research/GRIMO_PARTNER_EXPERIENCE_MOTION_ANATOMY_EVIDENCE.md) — historical research-only抽出 |
| CAMERA | [Camera Full Source](../../grimo/knowledge/research/camera-framing/GRIMO_PARTNER_EEVEE_CAMERA_FRAMING_ANALYSIS_FULL_SOURCE.md) — Eevee実測とCarol提案の分離が必要 |
| POSE | [Generation Pose DRAFT](../../grimo/knowledge/character-production/GRIMO_TRIPO_GENERATION_POSE_CONTRACT_DRAFT.md) — 入力姿勢仮説 |
| VIEWS | [Body-only Multiview Register](../../grimo/knowledge/character-production/GRIMO_BODY_ONLY_MULTIVIEW_ASSET_REGISTER.md) — 2D選択・provenance・未完了事項 |

**Corpus警告:** E-ANのE03=嫌がる部位、E04=ノリノリ、E05=頬すりすり。E-MではそれぞれV05/V11/V06。E-M V03は進化の石。CAMERAのVideo 02はclose framingとして扱う。資料間で番号だけを照合しない。Masterは独立した追加実測ではなく既存Inventoryの集約であり、詳細分析と件数を足して新しい標本数にしない。

## A. Authority & Conflict Register

### A1. Precedence / approved ledger

現行明示Human決定とNORTH/4匹のCanonical Identityを優先し、承認済み見た目・EXP・ARCHの能力要件を維持する。Supporting geometry、研究Evidence、制作都合、歴史的文書はそれらを上書きしない。PLANは一時ロードマップであり新しいFINALではない（CAROL §0、OPS §2、INDEX）。ChatGPT Project MemoryはAGENTS上のreasoning policyだが、本作業では未取得であり内容を補完しない。

| Item | Status / handling | Trace |
|---|---|---|
| Canonical Identity優先 | **A**。4匹の元Identityが最終外見Authority。Body-onlyは派生入力。Neutralのシルエット、目・顔、比率、色、固有付属部、幼さ・柔らかさを保護。新しい姿勢やrig都合で変えない | NORTH §4; POSE §0; VIEWS §1 |
| Carol visible/supporting authority | **A**。Canonical → approved Normal Front/Side → supporting Skin等の関係を維持。[authority.json](../../../assets/grimo/source/carol/approved-3d/authority.json) が参照先を記録。Body-onlyでNormal/Skinを置換しない | CAROL §0; INDEX Carol; STATE |
| 4匹のdirection | **A**。Carol=attention-seeking+relaxed、Jill=attention-seeking+energetic、Pino=energetic+independent、Shushu=relaxed+independent。方向性は保持するが形容詞/速さだけでIdentityを完成としない | NORTH §5; EXP §9; PLAN Phase 1 |
| 共通体験 | **A**。局所因果、視線、主体性、WAIT、境界、静止、余韻、割り込み、履歴・反復抑制。共通runtime semanticsは許容、個性の共有は禁止 | EXP §§1–8; NORTH §§6–9 |
| Carol FINAL保護 | **A**。46 Families=42 built-in+4 unlockable、156 variant profiles。既承認coverageは将来監査対象であり黙って削除しない。件数は4匹の最適解/生成目標ではない | CAROL §§1,32; PLAN Phases 1,3 |
| Carol locked content | **A**。Dream Moon Macaron / Dream Star Brooch、Moon Ball Play / Star Peek / Fleece Hide-and-Peek、Dream Keepsake Presentationを保護。変更案はHuman reviewへ明示 | CAROL §§1,13–15 |
| Positive-only care | **A**。無入力/不在に罰、親密度低下、罪悪感、敵対的報復を導入しない。拒否・距離・回復は許容 | NORTH §9; EXP §5; CAROL §§9–10 |
| Acceptance | **A**。Identity/cuteness/naturalnessはHumanが判定。技術PASSは体験PASSではない。Xiaomi 14T Proが実機QA、Pixel 7a-classは未検証target | NORTH §§10–11; EXP §11 |

### A2. Conflict / unresolved ledger

| Collision / uncertainty | Disposition for next design | Trace |
|---|---|---|
| Carolの古い「restrained delay / delayed softness / delayed secondary」 | **解決済み優先規則:** 2026-09-24の**body-owned fleece / default macro positional lag = zero**を適用。局所圧縮・開口・小さいauthored shape recoveryは許容。位置/回転のshell遅れ、独立cloud lobe spring、浮遊、常時揺れは不可。Shape recoveryとmacro transform lagを混同しない | CAROL §§17,22–24; NORTH §5 / EXP §9 / ARCH §8の旧表現; STATE planning inputs |
| 旧FINALをゼロベースで再設計する意味 | **A/U**。Carol契約を勝手に改訂する権限ではない。Jill/Pino/ShushuへCarolのcatalogを雛形にしない。独立Identityを先に作り、後段でCarol coverageを照合。改訂が必要なら承認事項との差分を提案として提示 | PLAN Phases 1,3,5 |
| Generation Pose = Rest Pose = Game Neutralという誤同一視 | **P/U**。入力形状を読みやすくする姿勢、rigの基準姿勢、体験上の通常姿勢を分離。POSEの角度/clearanceは実測ではない。Pino/Shushu座位Game NeutralはPLAN上まだ候補 | POSE §§0,2–7; PLAN §1 |
| 旧制作方式・budget・数値 | **P**。LIVINGのruntime/制作推奨、CAROL冒頭のruntime baseline hypothesis、CAMERAのCarol「Final contract」という見出しを新しい技術決定に昇格しない。Full-Spatial+View-Weighted Polishは現行能力要件。mesh/rig/骨数/solver/手順は未確定 | ARCH §§0,2,11,21; OPS §§2,13; ANATOMY authority boundary |
| Tripo適合性 | **U**。Studio 3D/auto-rig/preset/eligible Text-to-Motionを優先評価し、不足はCodex/Blenderで修復/制作するという**Aの方針**。4匹に使えること、品質、StudioとAPIの同等性は未検証。POSEの外部Help/slot記述はXであり最新能力の保証ではない。credit使用は明示Human承認が必要 | PLAN §0, Phase 4; POSE §§7–9 |
| 2D selection vs production readiness | **A/U**。VIEWSには現在選定された15画像を登録済み。Carol BackはHuman判断で不使用、全画像TRIPO_PREFLIGHT_PENDING。Jillの桃色頭部付属は最新Human解釈でhorn-like。左右名はimage-facing方向であり解剖学/Studio slotと異なる。clover等のmaterial QAは未完 | VIEWS §§1–3,6; INDEX; POSE §8 |
| Carol実行状態の古い「Current state」見出し | **A/U**。STATE内の2026-10-10更新と保存checkpointを区別。v001はHuman visual review待ち、Skin v004 default promotionは耳・Motion・runtime PASSではない。このbranchのSTATE snapshotを他branchの最新結果で推測更新しない | STATE「Normal semantic v001」「Normal/Fleece planning inputs」「Current state — 2026-09-29」 |
| Eevee分析が「Pikachu corpus absent」と記す | 文書自身の5本corpus限界。今回P-AN/P-Mは別に存在する。E-AN §25の欠落をプロジェクト全体の欠落と誤読しない | E-AN §§0,25; P-AN §2; P-M §1 |
| 外部開発者証言の参照形式 | **X/U**。LIVINGはrendered citation IDで開発者/心理学主張を記録している。本Packはその帰属を報告するのみ。一次出典URL・原文未再確認の主張をO/Aへ昇格しない | LIVING「開発者側から見た『可愛さ』の作り方」「証拠強度と残る不確実性」 |

## B. Living Companion Principles

下記は研究をコピー指示へ変えるものではない。ピカブイの姿勢・時刻・ハイタッチ演技を流用せず、原理とGrimoの正式要件を接続する。

1. **注意が存在する。** 見る/逸らす/戻る、目と頭の選択的参加が相手への向き合い方を作る。**O:** 表情や頭の変化は観察可能。**I/U:** 正確な眼球追従、procedural gaze、ターゲット推定は弱い。**A:** 常時凝視を避け、注意の継続と自然なreleaseを支える。
2. **主体は入力前からいる。** **O:** 相棒からのoffer、無接触時の小さな自発phrase。**I:** 「欲求を持っている」ように知覚される。**A:** invitationとWAITをfirst-classな体験にし、ユーザーが応答しなくても責めない。
3. **静止にも意味がある。** **O:** 全身をほぼ止めた長いholdでも顔・耳など限定channelが変わる。**I:** 動作量と意図の強さは別。**A:** moving hold、無入力のquiet life、必要channelだけ動くcorrelated asynchrony。固定周期やrandom twitchを生命感の代替にしない。
4. **触れ合いは一発triggerではなく時間的因果。** **O/T:** 持続pet中の段階的快、警告から回避、食後pause、social contact後の素早いACKは異なる時間構造。**I:** accumulationやevaluationに見えるが内部threshold不明。**A:** zone/side/gesture/速度/継続/履歴/現在状態を保持し、柔らかい演技と素早い局所ACKを両立。
5. **触点と身体が互いに関わる。** **O:** Eeveeの頬rubで深いbow/rebound。**I:** contact seekingと解釈できるが、動いている間の接触維持は未確認。**A:** Grimoでは触れた側が消えない局所因果・接触anchor整合を要求。参考映像の左右が中央macroへ収束する弱点も引き継がない。
6. **左右差には理由がある。** **O:** 片耳、片前肢、左右非同期のphrase。**I:** 注意/支持/触点に結びついた非対称性が説得力を作る。**A:** random offsetを増やすより意味・weight・side ownershipを優先。screen-leftをrig Lへ無条件変換しない。
7. **感情は強度と時間を持つ。** **O:** 顔による先行評価、小さな反応のchannel節約、大きな感情で参加部位が増える。leadはFamilyにより違う。**A:** anticipation→action→hold/follow-through→settle→afterglowを意味に応じて扱う。全反応に全段階・全channelを強制しない。
8. **拒否は関係の言語。** **O:** warning/protestとwithdrawal、向きや顔に残る負の状態。**I:** boundaryが独立した相手の知覚を支える。**A:** Grimoはhint→mild refusal→withdrawal→recovery、罰や敵対表現を避ける。Pikachuの強い怒り演技は採用指示ではない。
9. **WAITは応答可能な意図の保持。** **O:** offerしてユーザーcontactを待ち、ACK後に次turn/完了。**U:** 完全無応答時timeoutの自然分布は不足。**A:** 姿勢を忙しく動かさずに生きた期待を伝え、ignored時のreleaseも考慮する。
10. **割り込みは連続した相手を保つ。** **O（Master記録）:** doze→touch wake/recovery。**U:** 正の反応途中で指を離す際の全branch、内部blendは確認できない。**A:** 現在姿勢/感情からredirect、forced neutral・clip queue spamを避ける。安全な支持/咀嚼/prop transferの保護とACKの両立は後段の課題。
11. **動作が終わっても感情は終わらない。** **O:** content hold、displeased idle、再入場後の背/側面状態。**I:** 内部記憶の具体方式は不明。**A:** body settleとemotion settleを分け、次の反応に連続性を残す。
12. **反復抑制は件数より文脈。** **O/T:** ピカブイでも似たpositive/negative句が反復しcanned感の余地がある。同一clipの証明はできない。**A:** Familyとperformance両方で初期状態・side・強度・settle・余韻・historyを扱う。反復時は常に増幅する必要がない。
13. **関係性が続く。** **X:** LIVINGは公式の直接touch、絆、high-five/gift、開発者の相棒別専任designer・生物/重量観察を報告。**I:** 同じ相棒と行為の結果が続く閉ループがattachmentを支える。**P:** 研究のmemory項目やutility schedulerは一案。**A:** Grimoは内部状態の継続と4匹固有のactingが必要であり、罰を伴うaffinity modelや研究の実装レシピは自動採用しない。

## C. Evidence Traceability Matrix

Familyは参考側の索引でありGrimoの新catalogではない。数値は参考映像内の例、Grimoの固定timing contractではない。E-AN/P-ANは30fps、1frame≈33.3ms。visible hand/contactと内部入力受理は同一ではない。

| Principle | Evidence section / representative event | Family / limit | Current requirement |
|---|---|---|---|
| 1 注意・視線 | E-AN §§4.6,5,25; P-AN §§5,16.3 | E-M §5 MF-011はhand-oriented **candidate**（V01 02:49.50–02:51.70）。眼球saccade/追従solver未確定 | EXP §4 |
| 2 主体性 | P-AN §§1.3,24：V05≈0.4–4.4s、cursor前のaffection phrase; E-AN §8.4 E01≈98.633–99.7s自発paw action | P-M §12、E-M §§11–12。無入力=内部motiveの証明ではない | EXP §6 |
| 3 静止・非同期 | E-AN §§1.1–1.2,8.5：E01≈128.3–150+s; P-AN §§1.5,4.10–4.11 | E-M MF-007/019、P-M MF-001/029、両Master Stillness節。breathing周期未確立 | EXP §§2–3,6 |
| 4 触れ合いの時間構造 | E-AN §§8.1,8.3,24：E01 09.833→11.367s快表情、≈77.63→78.53s食後反応; P-AN §24 V01≈63–66s段階的快 | E-M MF-027/028/029/057; P-M MF-006/007/035。1.53sは入力latencyではない。pause=咀嚼の証明ではない | EXP §§3,5 |
| 5 接触へのcommit / side | E-AN §§8.12–8.13：E05≈20.12–22.6s、65.9–68.4s; §§16.2–16.3,25 | E-M MF-032/033; P-M MF-009。接触維持・sideの内部利用はU。Opposite-sideでも中央反応する弱点 | EXP §5; CAROL §§7,21,30 Gate F |
| 6 非対称 / channel節約 | E-AN §8.10：E04≈0.6s片耳→face→反対耳→≈2.933s両paw参加→≈3.5s終了; ANATOMY §3 E1-A | E-M MF-005/006; P-M §22。常時全身/常時tail wagは導かない | EXP §§3,7–8 |
| 7 感情の時間phrase | E-AN §8.2：E01≈55.80s顔→≈56.97s耳peak; P-AN §§1.8–1.9,24 V02≈48.5–49.20s compression→expansion→VFX | P-M MF-016。参考の怒り/技をコピーしない。face-firstは全Family固定ではない | EXP §§3,7–8 |
| 8 boundary | E-AN §§1.6,8.8–8.9：E03≈9.667–11.13s protest、20.80–22.33s withdrawal; P-AN §24 V02≈14.7–16.47s顔警告→身体 | E-M MF-039–046; P-M MF-014/015/017/018。selection/hysteresisの内部方式はI/U | NORTH §9; EXP §5 |
| 9 offer / WAIT / turn | E-AN §§8.6,24 E02 34.400→≈34.467s contact→happy face; P-AN §24 V03≈20.7→22.07s WAIT、≈22.10s eyelid change | E-M MF-051/052/053; P-M MF-021/022。時刻は各source体系。無応答timeout未確認 | EXP §6; CAROL §9 |
| 10 interruption | P-M §§4,19 MF-033 touch-interrupted doze→wake/recovery; E-AN §25 items 29–30はearly release/contact continuity不足 | wake例から全reactionのinterrupt graphを推定しない | EXP §7; CAROL §20 |
| 11 afterglow / continuity | E-AN §8.12≈21.28–22.4s第二content hold; P-AN §§1.2,1.7,24 V05≈102–105s、V02≈54–67s背/側面 | E-M MF-076、P-M MF-038/039/017。affect persistenceは見えるが保存方式不明 | EXP §§1–2,7; CAROL §17 |
| 12 variation / repetition | E-AN §§13,16.1–16.6; P-AN §1.10; E-M §28、P-M §25 | cross-video類似は共有clipの証明ではない。E-M 77 / P-M 47 Familiesはcorpus taxonomy、最適制作件数ではない | EXP §3; CAROL §§18–19,30 Gate I |
| 13 関係の継続 / 固有acting | LIVING「直接触ること…」「感動は…agency…」「『絆』が別画面…」「開発者側…」「証拠強度…」 | 外部主張A/B=本Pack X。統合モデルD=I、motion-personality bible等E=P。効果の因果寄与率は未測定 | NORTH §§1,5,9; EXP §§1,9,11 |

## D. Anatomy / Camera / Production Implications

### D1. Capability and physical unknowns — 技術方式は決めない

- **独立可動と連続した身体:** ARCH §§4,6,11のAは、目/瞼/顔/頭/固有付属部/前肢/支持/COMを必要に応じて独立制御し、turn/leanで露出する面が破綻しないこと。ANATOMY §3 E1-Aの前肢深度とpad向き、E2のprofile→front/occlusion変化、E3のdeep bowはO。それをGrimoのcapabilityへ翻訳するのはIであり、特定rig/bone数を導かない。
- **支持と重量:** ANATOMY §§9–10、P-M §23は上半身表現中も支持が静かに残る例。大きい感情=跳躍とは限らず、足がcropされたframeで接地を断定しない。Carolのshort limb/heavy hoofはA。安全な頭/体幹角度、支持移行、forward/lateral COM量、tail根元露出、deformation clearanceはU（ANATOMY §12）。
- **接触・props:** bodyが触点へ寄るとzone/anchorも整合する必要がある。食物の消失だけではbite/chew/swallow、gift消失だけではtransfer方式は分からない（P-M §34）。眼/口/接触可動範囲、深いlean時のanchor、Wear遮蔽、prop sizeは実物検証が必要（CAROL §§24–25,32）。
- **Carol:** Aはfleeceのbody-owned macro positionとlocal shape deformationの分離、tiny face/eye appeal、heavy support、独立ear/tail、motif/prop anchors。旧研究の「fleece delay」を能力要件に加えない。Normal/Skinの保存と現行routingはSTATEに従う。accepted identity envelope/rig/Motion PASSは未取得。
- **Jill:** EXP §9のchest/upper-body→wings/tail/leaves、rooted heavy tailはA。最新horn-like解釈を保護。wing/leaf/limb/tail rootの分離と干渉、素材/marking fidelityはPOSE/VIEWSのP/U。wing搭載creatureのTripo rig成功は未検証。
- **Pino:** EXP §9のrounded/inward-arm tendency、buoyant but grounded、thick tail delayはA。広いtailと胴/脚の融合、両眼/片眼表現の完全性、支持、座位移行のidentity保持はPLAN Phase 4 / POSE §3の将来課題であり、座位Neutral/rig方式は確定しない。
- **Shushu:** EXP §9のgrounded plush compression/settle、小ear、crown/bouquet attachmentはA。短脚・pad・腹/腿・前肢の分離、deep sitでのcollapse、prop holdingとreleaseはPOSE §4のP/U。generation squatを通常立位のIdentityへ転用しない。

### D2. Camera — observed screen space ≠ four-character contract

CAMERA §§3,7,10–11の記録を使う。1920×1080上の手動visible contour測定で、通常contour±10–15px、遮蔽/clip等±20–30px、ratio概ね±0.005–0.015。edgeにclipしたtrue anatomical extentは不明。

| Reference measurement | Observation / boundary |
|---|---|
| Ordinary Neutral（Video 01/06） | width ratio 0.617–0.672、height 0.954–0.999、face center X 0.493–0.503 / Y 0.398–0.463。長耳は上端clip、足は下端近く。visible bbox値であり全silhouette収納率ではない |
| Ordinary maximum width | 0.745–0.779（median 0.762）。neutralだけでなくacting envelopeと表情readabilityの両立が課題 |
| Close outlier（Video 02） | median width 0.836、face Y 0.569。通常full-body統計に混ぜない |
| Camera stability | clean背景ROIの見かけshift概ね0–1pxはO。ほぼ固定cameraはI。内部transform/controller完全固定やroot寄与率はU |

CAMERA §§12–14のCarol width 0.58 / height 0.76 / faceY 0.40、safe envelope等は**P（design translation）**。見出しが「Final」でも本設計の承認済cameraではない。FOV、distance、height、focal length、world scale、near/farは未測定。4匹それぞれのface/appendage可読性・遮蔽・touch reachを評価してから調整する。

CAROL §21のA：front cameraが基準だがorientationはlockではなく、将来turn/3⁄4/back/walkingを許容する概念。MVP coreの意味はfrontから読め、camera orbitで弱いactingを救わない。Full CompanionとClose Window-Leanは概念であり実装/clip承認ではない。スマートフォン縦画面へ16:9実測をそのまま転写しない。

### D3. Production disposition

Tripo First → Codex Fallbackは制作方針A、各能力への割当は将来の仮説。モデル生成・texture・auto-rig・preset・eligible Text-to-Motion・後処理は別々に適合性を調べる。技術方式、rig topology、骨数、clip数、solver、exportの詳細をこのPackでは確定しない。Body-only承認はTRIPO_READYを意味せず、現在は全preflight pending。今回はStudio/Blender/アプリ操作もcredit使用も行わない。

## E. AstraへのDesign Questions（優先順、未回答）

1. **各個体と会いたくなる理由は何か。** 正式4方向とCanonical Identityを守りつつ、同じ30秒無入力場面で、attention・距離・静止・自発動機のどの違いから4匹別の相手だと感じられるか。形容詞/速さ/Carol catalog以外の根拠は何か。
2. **独立した意図とユーザーへの優しさをどう両立するか。** 各個体は何を見たい/求めたい/断りたいと表現し、応答・無応答・連続touchをどう受け取るか。拒否/WAIT/releaseが罰や罪悪感に見えない境界はどこか。
3. **触れた場所から何が伝わるか。** 同じL/R cheek/headのtap・slow pet・持続/反復で、各個体の局所ACK、評価、contact seeking、weight commitmentの差が何を語るか。sideと因果が中央macro反応に消えない条件は何か。
4. **沈黙と感情の時間はどのように固有か。** quiet/moving hold、注意dwell/release、小/大感情のchannel参加、settleとafterglow、次の行為への影響で、各個体らしさをどこまで示せるか。全Familyのleadを固定せずIdentityを保つには何が必要か。
5. **途中で話しかけたとき同じ相手であり続けるか。** happiness中touch、side change、WAIT応答、touch releaseで何を引き継ぎ何を譲るべきか。current affect/poseと支持/prop safetyの両立をどの代表場面でHumanに判断してもらうか。
6. **3–5分で関係がどう読めるか。** 同じgesture×10、無入力、ignored invitation、再contactが、既視感だけにならず意味の安定・慣れ・余韻・驚きへつながるか。量産せずに評価すべきIdentity差と反復リスクは何か。
7. **外見と身体の限界が演技の個性にどう関わるか。** Carolの小顔/巨fleece/zero macro lag、Jillのwing/leaf/heavy tail、Pinoのrounded body/broad tail、Shushuのshort-leg/plush/propsで、canonical appealを失わない表現の境界は何か。縦画面で読みたい意味と隠れる部位の問題は何か。
8. **承認済Carolと新設計の衝突をどう可視化するか。** 独立Identity案がFINALのcore/signature/locked contentと整合するか。必要な改訂をどの根拠・Human判断として切り出すか。Tripoの便利さがIdentityを狭めていないかは将来何で検証するか。

## Handoff boundary

最終Goalは30秒〜5分で4匹が別々にalive/lovable/causally responsiveな相棒になること。6フェーズは **Evidence → Experience Identity → behavior grammar/representative acting → Motion architecture/catalogs → anatomy/Tripo contract → independent audit/Human approval**。今回完了対象は最初のEvidenceのみ。

次の明示指示を受けたAstra / HighがPhase 1の `GRIMO_FOUR_CHARACTER_EXPERIENCE_IDENTITY_DRAFT.md` へ進む。Phase 2の代表actingと合わせて**Human Gate 1を通過してからdense Motion production**。Phase 3は `GRIMO_FOUR_CHARACTER_MOTION_ARCHITECTURE_DRAFT.md`、Phase 4は `GRIMO_MOTION_TO_ANATOMY_TRIPO_CONTRACT_DRAFT.md`。Phase 5は独立adversarial auditとHuman experience/personality/major concessions承認。DRAFT→FINALへ黙って昇格しない。

`DESIGN_READY`、`TRIPO_PREFLIGHT_READY`、実適合gate後の`TRIPO_READY`は別状態。本Packはいずれも付与しない。Phase 0の設計上のunknownは次段階へ明示して引き継ぎ、推測による解決・Motion/性格の創作・後段の実行を行わない。ここで停止し、ChatGPT Planner / Humanへ返す。
