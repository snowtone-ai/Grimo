# Pino — Rig / Shape Key / Motion Reference Production Prompts

**Status:** DRAFT / IMAGE CANDIDATE PRODUCTION / HUMAN REVIEW PENDING
**Prepared:** 2026-10-15
**Scope:** 34 independent image-generation prompts, one complete prompt per numbered reference.
**Human decision:** この文章の設計・実行委任は34枚の画像の一括Human合格、Motion DRAFTの採用、課金の許諾を意味しない。

## 実行契約（最初にここだけ読む）

**目的と判定境界:** Pinoにまた会いたくなる可愛さ・生命感・愛着（G0/G1）を実現するRig / Shape Key / Motion用の独立2Dリファレンス34枚を生成する。各Referenceは独立した静止画検査候補であり、34枚は34個のクリップ・Shape Key・必須演技を意味しない。2D候補の生成完了 ≠ Human可愛さPASS ≠ Motion DRAFTの採用 ≠ 3D/Rig/GLB/スマホ実機PASS。Game Neutral / Rig Rest / Tripo Generation Poseも別概念として扱う。

**Codex実行推奨:** GPT-6 Luna / Low（利用可能な場合）。新規セッション、`/compact`不要、サブエージェント不使用。下位モデルに仕様や全34プロンプトの再設計を委ねない。高度な判断は本文で確定済みだが、本人らしさ・可愛さの最終判断はHumanに残す。生成そのものの画像生成ツール消費量とCodexのテキスト推論コストを混同しない。

**正式Authority（優先順）:**
1. 最新の明示Human判断と `assets/grimo/source/pino/pino-Identity-canonical.png`：個体の顔・目・耳・頬・鼻・口・ひげ・頭頂毛束、青白い配色、可愛さの最上位。Canonicalの片眼ウインクは一時表情であり、両眼・左右独立瞼を必ず保つ。
2. `assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png`, `pino_bodyonly_left.png`, `pino_bodyonly_right.png`, `pino_bodyonly_back.png`：Human選定済みの形状・比率・短肢・腹・単一の太尾・支持の派生基準。left/rightは**画面内の鼻先の向き**であり、解剖学的左右やツールのcamera slotではない。実際の5画像を確認し、無条件ミラー扱いしない。
3. `docs/grimo/knowledge/Goal√map.md`、`docs/grimo/knowledge/GRIMO_CHARACTER_EXPERIENCE_SPEC.md`。
4. `docs/production/motion/GRIMO_FOUR_CHARACTER_MOTION_ARCHITECTURE_DRAFT.md`、`docs/production/motion/GRIMO_MOTION_TO_ANATOMY_TRIPO_CONTRACT_DRAFT.md`。P01–P29の具体演技は**DRAFT**で、正式採用・実物可動性は未確定。
5. `docs/grimo/knowledge/character-production/GRIMO_BODY_ONLY_MULTIVIEW_ASSET_REGISTER.md`（登録した元画像のバイト列・役割を保護）。

**事前条件（最小限）:**
- 作業開始時に現行ブランチ/HEAD/未コミット変更とローカル`AGENTS.md`を確認し、その運用を守る。必要なGoal√map/Handoffと適用資料は最短で読む。古いHandoffを制作状態の証拠にしない。
- 現在の**プロンプト原本ブランチは `docs/pino-motion-reference-prompts-20261015`**。実画像生成はそこを起点とする独立した新規作業ブランチ/worktreeで行い、他キャラクターの制作やユーザーの未コミット変更と衝突させない。新規worktreeが無理なら安全に隔離してから実行。原本を変更・上書きしない。
- 各生成呼び出しに**当該REF-NN節のフルプロンプト1本と正式画像A〜Eの実ファイル5枚**を画像入力として渡す。画像パスの文字列だけでは画像入力として認めない。元ファイルのクロップ・再保存・色変更・上書きはしない。
- 公式のCodex内蔵画像生成（利用可能なら`image_gen` / `imagegen`スキル）を使用する。ただしスキルの表示だけではツールが動作する証拠にならない。**追加API課金、APIキーの要求、CLI/APIへの勝手なfallback、外部画像サービス、Tripo、代用品のSVGや擬似PNGを禁止**する。5枚の実画像を同時に参照入力できない場合は `REFERENCE_INPUT_BLOCKED`、ツール不存在・実行不能・network error等では `IMAGEGEN_UNAVAILABLE` と報告して停止。存在しない成功画像を記録しない。

**制作順序と自動停止条件:**
1. **#01だけを1回生成**し、画像生成ツールの実動作、正式5画像の投入、PNG出力と保存が成立するか確認。失敗したらその場で停止し、理由を短く報告。#02以降に進まない。
2. #01が生成できたら、#02と#03を順に各1枚生成。3枚を最小限の視認で診断：#01はPino Identity・両眼・重心、#02は真横90°・鼻/頬/顎の奥行き・太い尾、#03は短前肢・腹の非融合・両足支持。**明白なIdentity崩壊、部位の増減・融合、前肢長大化、尾の切断/平板化、重大な非支持、反対方向のSide、偽の継ぎ目**などの致命的欠陥が残る場合はここで停止し、生成済みを保全する。見た目の好みについてHuman PASSは宣言しない。
3. #01〜03に重大な問題がなければ#04〜34を番号順に独立生成。**各原則1回**。修正は誤りが局所的かつ明白な場合のみ**各ID最大1回**まで。前候補を失わず改訂は`-v2`のように別名保存。全画像に毎回A〜Eを投入し、以前の生成画像を新たなAuthorityへ昇格させない。
4. 1枚ごとの長い批評・全画像の再計画・他キャラの分析・サブエージェント・大規模テスト・無限再試行を行わない。生成結果の存在と明白な破綻だけ最小限確認し、Humanが後から一覧レビューできる状態にする。
5. **一括生成中に致命的な共通破綻が連続、参照入力不能、ツール障害、画像保存失敗、予期せぬ課金要求が出たら停止**。進行可能数を偽らず、成功分を残して報告。小さな問題だけで最初から全件やり直さない。

**成果物と保存:**
- 出力先：`assets/grimo/production/pino/references/pino-ref-NN.png`（NN=01〜34、元生成画像は上書き禁止）。画像生成ツールの一時保存先から必要なPNGだけコピーする。PNG署名・ファイル存在と少数の画像可読性を簡潔に確認する。大きいBinaryやGit制約でpush不可ならローカル成果を保持し、原因を報告。
- **必須**：同フォルダへ見やすい`contact-sheet.png`と簡潔な`REVIEW.md`を作成。コンタクトシートは生成に成功した画像のサムネイルとIDだけを並べる。サムネイルを作るために元PNGを改変しない。全34枚未達でも成功分を一覧化する。
- `REVIEW.md`は各ID・対応Motion(DRAFT)・生成結果（success/failed/skipped）・出力ファイル・重大な懸念・再試行有無・`Human Review=PENDING`を簡潔な表で管理。機械的自己採点、Human可愛さ認定、Rig/Runtime合格を記さない。
- 作業差分と衝突を確認し、**Pino関連生成物だけ**を安全にcommit/pushして遠隔HEADを再確認。Handoff同期は実際の重要状態変化がある場合のみRepository規則に従って安全に行う。報告は成功数、失敗/未着手ID、停止理由、生成物のパス、branch/HEAD、Human=PENDINGの順で短く記載する。

**コスト最適化:** 各画像の生成時にはこの文件の全文（約9万文字）や全34節をチャットへ展開しない。必要な`### REF-NN`節1つを範囲抽出し、それをそのまま画像生成ツールへ渡す。共有の外部ベース文やJillプロンプトの読み込みは不要。画像の生成品質を犠牲にするプロンプト短縮、引用先だけによる5画像省略は禁止する。

**品質Gate:** Pino本人の可愛さ・両眼・青白い色 → 短肢と腹の非融合 → 足の荷重と重い太尾の連続 → 触点と視線の因果 → 自発性・好意・余韻。P03の床到達は未実証なので前肢を伸ばさず同じ到達域の代替をHumanレビュー候補とする。34枚の静止画像生成は最終Motion採用でもRig/3D合格でもない。

## 画像ID → Motion対応（DRAFT）

| No. | テーマ | Motion |
|---|---|---|
| 01 | Neutral Front Three-Quarter / Identity and Grounded Body | P01 / P05 / P26 |
| 02 | True Left-Facing Orthographic Side / Head Belly Tail | P01 / P05 / P06 |
| 03 | Low Anatomical Left Forepaw Offer / Arm Belly Clearance | P03 / P14 / P15 |
| 04 | Both Eyes Open / Bilateral Eye Anatomy | P01 / P02 / P28 |
| 05 | Natural Complete Blink / Closed Eyes | P01 / P06 / P12 |
| 06 | Anatomical Left-Eye Wink / Right Eye Preserved | P28 |
| 07 | Anatomical Right-Eye Wink / Left Eye Preserved | P28 |
| 08 | Sleepy Half-Lidded / Soft Drowsiness | P06 / P12 |
| 09 | Focused Curiosity / Look to Own Forepaw | P02 / P03 |
| 10 | Gentle Surprise / A Different Result | P17 |
| 11 | Small Contentment / Quiet Satisfaction | P01 / P23 |
| 12 | Shared Delight / Bright Friendly Joy | P14 / P16 |
| 13 | Mild Boundary / Gentle Hint | P18 / P19 |
| 14 | Warm Recovery / Soft Afterglow | P20 / P25 |
| 15 | Head Pet Enjoyment / Gentle Active Acceptance | P08 / P12 |
| 16 | Anatomical Left Cheek Offer / Affection | P09 |
| 17 | Anatomical Right Cheek Offer / Opposite Affection | P09 |
| 18 | Ear Root Touch Local ACK / Independent Ear | P11 |
| 19 | Rounded Belly Contact / Local Softness | P10 / P13 |
| 20 | Paw Set and Gentle Press / Causal Contact | P03 |
| 21 | Paw Release and Result Inspection / Purposeful Pause | P03 / P17 |
| 22 | Low High-Five Target / Living WAIT | P14 |
| 23 | High-Five Touch ACK / Shared Happiness | P07 / P14 |
| 24 | Self-Initiated Pet Invitation / Offer and Wait | P15 |
| 25 | Thick Tail Follow-through / Supported Turn | P04 / P05 |
| 26 | Rear Three-Quarter Tail Root Local ACK | P04 / P11 |
| 27 | Grounded Weight Shift / Two-Foot Support | P05 |
| 28 | Low Relaxed Rest / Supported Settle | P06 |
| 29 | Wake and Supported Rise / Rest Transition | P06 / P20 |
| 30 | Small Food Handling / Mouth and Short Paws | P21 / P22 |
| 31 | Satisfied Taste / Delicious After-Savor | P23 |
| 32 | Gentle Gift Presentation / Short Paw Transfer | P27 |
| 33 | Natural Paw Sole Underside / Pad Anatomy | P05 / P06 |
| 34 | Wear Anchor Comfort / Head Neck Clearance | P24 |

## 34枚の独立したフルプロンプト

各節`### REF-NN`から次の節直前までに、唯一の完全プロンプトがある。どの節もほかの節や共通ベースを参照しない。画像A〜Eは各節ですべて再指定する。

### REF-01 — Neutral Front Three-Quarter / Identity and Grounded Body

- **Motion DRAFT:** P01 / P05 / P26
- **主眼:** 構造

```text
【Pino Reference 01 — Neutral Front Three-Quarter / Identity and Grounded Body】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。構造の検査。関連する動作候補は P01 / P05 / P26（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
Pinoが日常の静かな関心を保つGame Neutral候補。両足を自然に床へ接地させ、胴体を低重心で支え、短い左右前肢を内寄りに楽に下ろす。頭はほぼ正面、両眼を柔らかく開き、微笑みはごく小さい。尾は骨盤後方から太く連続して自然な曲線を描き、足の代わりに体重を支えない。

■ カメラ・画角・フレーミング
全身・正面から約30度の3/4。顔の高さに近い視点。顔、胸、腹、左右の前肢、足、尾先まで表示。歪みの少ないレンズ。

■ 顔・目・ひげ・感情
自然な両眼開眼と穏やかな関心。ウインク禁止。大きな瞳と小さな口、頬、ひげが可愛さの主役。

■ 立体構造・Rig変形を想定した保護事項
両足に安定した荷重を読み取れるようにする。腹と前肢の間に本物の立体境界を保ち、肩と肘を不自然に離さない。尾根元の厚さを保つ。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
背が高い人型、前肢がTポーズ、尾で三点支持、腹部が風船球、前脚・腹の癒着、正面だけの平面顔。

■ Human Reviewで見る重点
Canonicalと一目で同一個体とわかり、同時にBody-onlyの前後・左右の比率と支持構造に破綻がない。これを完成済みGame Neutralと呼ばない。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
01番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-02 — True Left-Facing Orthographic Side / Head Belly Tail

- **Motion DRAFT:** P01 / P05 / P06
- **主眼:** 構造

```text
【Pino Reference 02 — True Left-Facing Orthographic Side / Head Belly Tail】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。構造の検査。関連する動作候補は P01 / P05 / P06（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
鼻先が画面左を向く完全90度の側面。基本的な静かな支持姿勢を取り、顎を過剰に持ち上げない。横から見える頬・鼻・顎・耳・首・胸・腹・短い前肢・足・太い尾の接続を正確に再現する。片眼が側面として自然に見えればよく、反対眼を無理に出さない。

■ カメラ・画角・フレーミング
画面左向き真横90度、正投影、全身。尾端、鼻先、足底を一切切らず、全身が収まる横長または適切な余白の構図。斜め側面は禁止。

■ 顔・目・ひげ・感情
鼻先は小さく、頬・眼窩・下顎にしっかり奥行きがある。横顔でも柔らかい目と小さな微笑みがPinoに見える。

■ 立体構造・Rig変形を想定した保護事項
尾の後骨盤への太い連続根元、断面の厚み、曲率をCとD/Eの立体整合から守る。後脚と尾、腹と前肢を融合させない。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
カメラ回転で耳・両眼が見える3/4、平坦な頬・貼り付け顔、長い鼻、平板なヒレ尾、長脚、浮遊体。

■ Human Reviewで見る重点
前からは見えない横顔の奥行きと尾根元の立体接続が自然。01と別ポーズ・別個体を発明しない。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
02番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-03 — Low Anatomical Left Forepaw Offer / Arm Belly Clearance

- **Motion DRAFT:** P03 / P14 / P15
- **主眼:** 変形

```text
【Pino Reference 03 — Low Anatomical Left Forepaw Offer / Arm Belly Clearance】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。変形の検査。関連する動作候補は P03 / P14 / P15（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
Pinoが解剖学的左前肢を、相手が触れられる低い胸前へ小さく差し出している。正面観察では左前肢は画像右側。短い腕を肩から自然に回し、丸い先端が腹前に少し浮く。右前肢は内寄りの楽な位置で止める。両足で重心を支え、頭と眼は差し出した先端と相手の間へ向ける。

■ カメラ・画角・フレーミング
全身Front 3/4、約25〜35度。提示した左前肢の肩・先端・腹との実際の隙間、反対前肢、両足、尾が見える位置。極端な手前パースなし。

■ 顔・目・ひげ・感情
小さな期待と好意。両眼開眼。視線は自分の前肢先端に軽く向き、すぐ相手を見て交流しそうな優しい微笑み。

■ 立体構造・Rig変形を想定した保護事項
肩から先端の短い体積を保持。左前肢と白い腹の間に実際の空間を確保し、腹自体は変形しても全体縮小しない。支持は後脚・足。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
腕の伸長、人の手指、肩の脱臼、腹の削り落とし、左足浮き、尾の支柱化、両腕同時挙上、拍手。

■ Human Reviewで見る重点
短腕のまま提示面が読み取れ、肢腹独立・荷重・可愛さが同時に成立する。実際の3D到達可否は後工程で検証。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
03番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-04 — Both Eyes Open / Bilateral Eye Anatomy

- **Motion DRAFT:** P01 / P02 / P28
- **主眼:** 顔

```text
【Pino Reference 04 — Both Eyes Open / Bilateral Eye Anatomy】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。顔の検査。関連する動作候補は P01 / P02 / P28（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
Pinoが真正面を向き、両眼を自然に完全開眼する。Canonicalの片眼ウインクから欠落した眼を作るのではなく、左右の眼球・眼窩・上下瞼が本来どちらにも存在する個体として再構成。頭と頬と口の位置を変えず、表情を穏やかな注意に揃える。

■ カメラ・画角・フレーミング
頭・上胸を大きく見せる真正面、歪みの少ないカメラ。左右耳・ひげ・頭頂毛束、両眼・鼻・口を収める。上胸が少し見える。

■ 顔・目・ひげ・感情
左右両眼の瞳孔・虹彩・ハイライト・瞼厚・眼窩奥行きを自然に揃える。完璧な機械的鏡面コピーによる無表情化は避ける。

■ 立体構造・Rig変形を想定した保護事項
眼球と瞼は別制御を想定できる立体。両眼を大きくしても鼻を縮小せず、頬の体積を保つ。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
片眼が縫い目・線のまま、眼球欠損、巨大すぎる眼白、過剰な眉、鼻の押し潰し、少女漫画風の顔変更。

■ Human Reviewで見る重点
瞼を左右独立して開閉させられそうな眼窩構造と、Canonicalの可愛さが同居する。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
04番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-05 — Natural Complete Blink / Closed Eyes

- **Motion DRAFT:** P01 / P06 / P12
- **主眼:** 顔

```text
【Pino Reference 05 — Natural Complete Blink / Closed Eyes】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。顔の検査。関連する動作候補は P01 / P06 / P12（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
両眼を完全に閉じた一瞬。笑顔の誇張ではなく自然なまばたき。顔・鼻・耳・ひげ・頬・頭毛・首の輪郭はCanonicalから変えない。上下の瞼が自然に合わさり、眼球のふくらみと眼窩の立体量が残る。

■ カメラ・画角・フレーミング
顔と上胸の正面3/4約20度。両眼の閉眼線を確認できる緩い角度、余白と高解像度。

■ 顔・目・ひげ・感情
柔らかい閉眼。太く黒い貼り付け線や寝ていることを示す記号ではなく、薄い瞼形状。小さな穏やかな口元。

■ 立体構造・Rig変形を想定した保護事項
両頬の体積・目と耳の位置関係・鼻下の曲面を維持。瞼だけが可動したように読める。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
顔全体の縮小、線だけのペイント、眉の新設、満面の笑み、大幅な頭部傾斜、ウインク化。

■ Human Reviewで見る重点
04から両眼が同時に閉じた形状だと読め、Rig用Blink Shape Keyの目標として使える。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
05番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-06 — Anatomical Left-Eye Wink / Right Eye Preserved

- **Motion DRAFT:** P28
- **主眼:** 顔

```text
【Pino Reference 06 — Anatomical Left-Eye Wink / Right Eye Preserved】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。顔の検査。関連する動作候補は P28（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
Pino本人が解剖学的左眼だけをごく自然に閉じる。正面から見て画像右側の眼を閉じ、解剖学的右眼は開いたまま。ウインクは発見後に相手へ少し親しさを伝える希少な表情であり、常時片眼ではない。

■ カメラ・画角・フレーミング
頭部と上胸の真正面、両眼と耳の左右関係が曖昧にならない正投影寄り。

■ 顔・目・ひげ・感情
閉眼側は眼窩・頬が自然に連動し、反対側の瞳は大きく魅力を保つ。口元には小さな嬉しさ。

■ 立体構造・Rig変形を想定した保護事項
左右上下瞼の非対称制御を読み取れる。片眼だけの変形で顔全体が歪まず、鼻・ひげ・耳位置を保つ。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
左右逆転、開眼側が小さくなる、片眼の永久欠損、片頬の極端な変形、長い眉・人間的得意顔。

■ Human Reviewで見る重点
閉じているのが解剖学的左眼と明確で、両眼開眼状態への復帰が想像できる。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
06番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-07 — Anatomical Right-Eye Wink / Left Eye Preserved

- **Motion DRAFT:** P28
- **主眼:** 顔

```text
【Pino Reference 07 — Anatomical Right-Eye Wink / Left Eye Preserved】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。顔の検査。関連する動作候補は P28（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
Pino本人が解剖学的右眼だけを閉じ、左眼は完全に開いて相手を見る。正面から見て画像左側の眼が閉じる。06を単純反転した別個体ではなく、左右固有の耳・頬・毛束の立体関係を保つ。

■ カメラ・画角・フレーミング
頭部・上胸真正面、左右を混同しないカメラ。ひげ先端と両耳を含める。

■ 顔・目・ひげ・感情
開いている左眼はCanonicalの大きさ・光沢・優しいまなざし。右側の上下瞼を閉じ、口に小さな可愛い満足。

■ 立体構造・Rig変形を想定した保護事項
右眼だけの独立Blink。鼻・頬・下顎の体積変化は局所的にし、目の横幅を引き延ばさない。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
眼の左右間違い、左右完全ミラーの新Identity、頬と瞼の融合、貼り付けた弧のような線、眉の誇張。

■ Human Reviewで見る重点
左右の非対称表情を独立して作れることが可視的に理解できる。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
07番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-08 — Sleepy Half-Lidded / Soft Drowsiness

- **Motion DRAFT:** P06 / P12
- **主眼:** 顔

```text
【Pino Reference 08 — Sleepy Half-Lidded / Soft Drowsiness】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。顔の検査。関連する動作候補は P06 / P12（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
楽しい試行が終わり、少し眠たそうになったPino。下半身は支持したまま、頭だけ自然にわずかに緩む。両眼の上瞼が部分的に下がり、まだ周囲や相手を見ている。

■ カメラ・画角・フレーミング
顔・胸・内寄り前肢が入る正面3/4 medium shot。

■ 顔・目・ひげ・感情
左右半閉眼、柔らかな眼差し、閉じ切らない瞳、わずかな口のゆるみ。病的・不機嫌・酔った表情にしない。

■ 立体構造・Rig変形を想定した保護事項
瞼の弧と厚み、両頬の丸さ、耳の位置を守り、首だけ軽く脱力。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
眼球の縮小、下まぶたの大きな腫れ、口の長大化、首の折れ、睡眠記号。

■ Human Reviewで見る重点
Blinkの途中ではなく持続できる眠い安心の表情として読める。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
08番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-09 — Focused Curiosity / Look to Own Forepaw

- **Motion DRAFT:** P02 / P03
- **主眼:** 注意

```text
【Pino Reference 09 — Focused Curiosity / Look to Own Forepaw】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。注意の検査。関連する動作候補は P02 / P03（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
Pinoが自分の片前肢先端と小さな接点を興味深く見ている。片前肢は胸前に低く保持、反対前肢と足は動かさない。動かしている瞬間ではなく、結果を見て止まっている瞬間。頭は手元へわずかに向ける。

■ カメラ・画角・フレーミング
顔・両前肢・腹・足の支持が分かる全身Front 3/4。前肢と視線の先を同画面に収める。

■ 顔・目・ひげ・感情
両眼で実在の自分の前肢先端を焦点化。口元は小さな好奇心。可愛さを保ちながら、相手を常に見つめない自主性がある。

■ 立体構造・Rig変形を想定した保護事項
眼球・頭・首の連携。腹を潰さず短い前肢が見える。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
何もない空間を見つめる、手を揉む、拍手、首を長く伸ばす、過剰な寄り目。

■ Human Reviewで見る重点
何を見ているか初見で理解でき、探索の静止に意図がある。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
09番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-10 — Gentle Surprise / A Different Result

- **Motion DRAFT:** P17
- **主眼:** 感情

```text
【Pino Reference 10 — Gentle Surprise / A Different Result】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。感情の検査。関連する動作候補は P17（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
Pinoが自分で触れてみた結果を見て小さく驚く。手元は止まり、頭と視線が変化した接点に向く。胴や尾は大きく動かない。恐怖ではなく、もう一度確かめたくなる柔らかな驚き。

■ カメラ・画角・フレーミング
正面3/4、顔と前肢の接点を同時に見せる全身寄りmedium-wide。

■ 顔・目・ひげ・感情
両眼が少し開き、口がほんの少し丸まる。大きすぎる口や飛び出す目にはしない。

■ 立体構造・Rig変形を想定した保護事項
瞼・頬・口縁の局所変化。頭は小傾斜、支持は変えない。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
叫び顔、ビックリマーク、ジャンプ、全身反り返り、人間的歯列。

■ Human Reviewで見る重点
驚いた後に確かめる行為へ繋がる顔と重心の落ち着きがある。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
10番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-11 — Small Contentment / Quiet Satisfaction

- **Motion DRAFT:** P01 / P23
- **主眼:** 感情

```text
【Pino Reference 11 — Small Contentment / Quiet Satisfaction】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。感情の検査。関連する動作候補は P01 / P23（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
小さな実験や心地よい触れ合いが終わり、Pinoが静かに満足している。前肢の緊張は内側にほどけ、両足は接地。動かずに余韻を残す小さな可愛さ。

■ カメラ・画角・フレーミング
顔・上体・短前肢が確認できる正面3/4、必要な腰・足も画面内。

■ 顔・目・ひげ・感情
目はほどよく開き、小さく上がる口角、頬の柔らかさ。強すぎる笑顔との差を明確にする。

■ 立体構造・Rig変形を想定した保護事項
頬と口のごく小さな局所変化、頭の軽い弛緩。胴と尾を無意味に揺らさない。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
大口・大量のハート・瞳の別デザイン、満面の喜び、無理な前傾。

■ Human Reviewで見る重点
11は12の強い喜びと区別され、小さな満足だけで会いたくなる魅力がある。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
11番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-12 — Shared Delight / Bright Friendly Joy

- **Motion DRAFT:** P14 / P16
- **主眼:** 感情

```text
【Pino Reference 12 — Shared Delight / Bright Friendly Joy】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。感情の検査。関連する動作候補は P14 / P16（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
Pinoが自分の発見や相手のハイタッチを嬉しく共有している。両足は安定し、内寄り短前肢はわずかに弾んだ位置へ。胴体は小さく意欲的に上がるが球のように跳ねない。

■ カメラ・画角・フレーミング
正面3/4全身、顔と両前肢・腹部・尾を見せる。

■ 顔・目・ひげ・感情
大きな両眼に光、頬のふくらみ、Canon­icalを超えない明るい笑顔。口は小さく開いてもよいが巨大化しない。

■ 立体構造・Rig変形を想定した保護事項
頬と口、瞼、首、肩の協調。支持足は滑らず、尾は主動作へ控えめに追従。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
ジャンプ、拍手の固定化、尻尾の扇状展開、歯を見せる人間顔、膨張スケール。

■ Human Reviewで見る重点
嬉しさと「相手へ見せたい」気持ちが顔から明確に伝わる。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
12番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-13 — Mild Boundary / Gentle Hint

- **Motion DRAFT:** P18 / P19
- **主眼:** 感情

```text
【Pino Reference 13 — Mild Boundary / Gentle Hint】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。感情の検査。関連する動作候補は P18 / P19（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
今は自分の短前肢で試している途中なので、触れられすぎた面から少しだけ距離を取るPino。作業側の前肢を低く安全な範囲へ回収し、相手を認識しながらやわらかく区切りを表す。

■ カメラ・画角・フレーミング
顔・前肢・上体の3/4 medium shot。境界を示す面が画面内にある。

■ 顔・目・ひげ・感情
強い怒り・嫌悪ではなく軽い戸惑いと相手への温かさ。小さな口の緊張と視線を組み合わせる。

■ 立体構造・Rig変形を想定した保護事項
頭と短腕の局所回避であり、肩・腹・頬の交差を避ける。足尾は支持。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
叩く手、攻撃顔、口の吊り上げ、眉を新設した怒り記号、尾払い、全身逃走。

■ Human Reviewで見る重点
「嫌い」ではなく今の空間を少し守りたいだけだと伝わる。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
13番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-14 — Warm Recovery / Soft Afterglow

- **Motion DRAFT:** P20 / P25
- **主眼:** 感情

```text
【Pino Reference 14 — Warm Recovery / Soft Afterglow】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。感情の検査。関連する動作候補は P20 / P25（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
小さな戸惑いや楽しい試行が終わり、Pinoが肩と前肢を楽な位置へ戻し、安心と好意を残している。目は一度相手へ戻り、身体の主動作は終わっている。

■ カメラ・画角・フレーミング
全身の自然な3/4、表情と前肢の戻り、太い尾のsettleが分かる。

■ 顔・目・ひげ・感情
小さな微笑み、やわらかな両瞳。全くのNeutralより少しだけ温かい余韻。

■ 立体構造・Rig変形を想定した保護事項
頭・胴・尾の動作後の位置関係。太尾は遅れて静かに収まり、胴体は球状に弾まない。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
全身を一瞬で初期化したような姿勢、悲しげな謝罪顔、パーティクル、常時尻尾振り。

■ Human Reviewで見る重点
行為は終わったが気持ちは残っていると読める。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
14番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-15 — Head Pet Enjoyment / Gentle Active Acceptance

- **Motion DRAFT:** P08 / P12
- **主眼:** 接触

```text
【Pino Reference 15 — Head Pet Enjoyment / Gentle Active Acceptance】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。接触の検査。関連する動作候補は P08 / P12（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
相手に頭を撫でられ、Pinoが小さく頭を触点へ委ねて心地よさを味わう。人の手は描かず、頭頂の接触方向が頭の傾きと瞼で読める。短前肢は楽に下ろして支持は足で保つ。

■ カメラ・画角・フレーミング
正面3/4 medium-wide。頭頂・両耳・頬・首・胸、短前肢と足を見せる。

■ 顔・目・ひげ・感情
まぶたが少し緩み、口元と頬がほころぶ。自分で気持ちよさを選んでいる表情。

■ 立体構造・Rig変形を想定した保護事項
頭部の局所的な受けと首の小回転。耳の根元や瞼が乱れず、胸と顔が貫通しない。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
人の手の追加、頭が腹へ埋没、骨のない首の伸び、片眼消失、顔の極端な扁平化。

■ Human Reviewで見る重点
Pinoが撫でられることを本当に楽しんでいると一見で分かる。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
15番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-16 — Anatomical Left Cheek Offer / Affection

- **Motion DRAFT:** P09
- **主眼:** 接触

```text
【Pino Reference 16 — Anatomical Left Cheek Offer / Affection】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。接触の検査。関連する動作候補は P09（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
Pinoが自分の解剖学的左頬を相手へ近づけて、もっと撫でてほしいと穏やかに示す。頭の小回旋・傾斜で左頬面を前方に差し出す。両足は接地、内寄り前肢は休ませる。

■ カメラ・画角・フレーミング
正面からPinoの解剖学的左頬が明確に見える3/4。左右の方向を見た目で判断し、左右反転だけに頼らない。全身。

■ 顔・目・ひげ・感情
頬と片側瞼が心地よく緩み、近い目を潰さない。相手に近づきたい微笑み。

■ 立体構造・Rig変形を想定した保護事項
左頬の厚み、左眼窩、首・肩の干渉を管理。頬が胸に埋もれない。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
反対の右頬を提示、深すぎる頭の捻転、頬の扁平化、人の手、頬と耳の融合。

■ Human Reviewで見る重点
左頬であること、触点へ少し自ら寄ること、可愛さの三つが読める。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
16番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-17 — Anatomical Right Cheek Offer / Opposite Affection

- **Motion DRAFT:** P09
- **主眼:** 接触

```text
【Pino Reference 17 — Anatomical Right Cheek Offer / Opposite Affection】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。接触の検査。関連する動作候補は P09（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
Pinoが解剖学的右頬を相手に見せ、小さくその方向へ頭を寄せている。16と同一個体・同じ構造だが方向は逆。片側だけ得意・不得意にならず、右側の頬・耳・眼窩が立体的に成り立つ。

■ カメラ・画角・フレーミング
Pinoの解剖学的右頬が前方へ見える真の反対側3/4。左右が違うだけでカメラ高さ・全身倍率は16と整合。

■ 顔・目・ひげ・感情
大きく優しい目、少しだけ緩んだ瞼、小さな満足の微笑み。ウインクを必須にしない。

■ 立体構造・Rig変形を想定した保護事項
右頬と右眼窩・耳根、首回旋、腹や肩とのクリアランス。足支持と太尾維持。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
16の単純ミラーで模様や耳の相違を消す、左頬提示、頬と胸の融合、鼻先の伸長。

■ Human Reviewで見る重点
左右対称性より同一個体としての自然な右側解剖と好意を優先する。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
17番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-18 — Ear Root Touch Local ACK / Independent Ear

- **Motion DRAFT:** P11
- **主眼:** 接触

```text
【Pino Reference 18 — Ear Root Touch Local ACK / Independent Ear】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。接触の検査。関連する動作候補は P11（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
Pinoの解剖学的左耳の根元に軽い刺激が届き、左耳だけが小さく反応した瞬間。耳の外形・厚み・付け根は保ったままわずかに傾き、頭全体と反対耳は落ち着いている。人の手は描かない。

■ カメラ・画角・フレーミング
顔・左右耳・耳根と上胸を大きく写す前寄り3/4。反応側の耳が隠れない。

■ 顔・目・ひげ・感情
両眼開眼。触れられた側へ短く注意を向け、小さな「気づいた」顔。過剰な驚きなし。

■ 立体構造・Rig変形を想定した保護事項
耳根を軸とした局所運動、頭の毛束と耳の重なり回避。左右耳の制御独立性を意識。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
耳を巨大化、猫耳化、切り離し、反対耳の自動同調、顔全体の回転でごまかす。

■ Human Reviewで見る重点
触れた耳だけが先に反応したと理解できる。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
18番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-19 — Rounded Belly Contact / Local Softness

- **Motion DRAFT:** P10 / P13
- **主眼:** 接触

```text
【Pino Reference 19 — Rounded Belly Contact / Local Softness】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。接触の検査。関連する動作候補は P10 / P13（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
Pinoの丸い白い腹部の片側前面に優しく触れられ、ごく小さい局所的なへこみと体表の張りの変化が起きた瞬間。見えない指の接触を、腹の局所形状・表情・短前肢の弛緩で示す。外部の手は描かない。

■ カメラ・画角・フレーミング
腹・両前肢・顔・接地足が同時に読める全身Front 3/4。接触面に斜めの柔らかい光。

■ 顔・目・ひげ・感情
両眼開眼、少し驚いた後に心地よくなる穏やかな口元。

■ 立体構造・Rig変形を想定した保護事項
押圧は腹の一部だけ。胴全体の縮小・膨張なし。前肢根元・脚・背中に変形を伝染させない。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
腹がスポンジの大穴に、腕と融合、全身ゴム化、人の手追加、浮遊、泡。

■ Human Reviewで見る重点
局所的な触点が分かる一方で、全体のふっくらさと支持を保てる。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
19番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-20 — Paw Set and Gentle Press / Causal Contact

- **Motion DRAFT:** P03
- **主眼:** 探究

```text
【Pino Reference 20 — Paw Set and Gentle Press / Causal Contact】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。探究の検査。関連する動作候補は P03（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
Pinoが短い解剖学的左前肢を、実際に届く低い地面または支持面へ置き、非常に軽く荷重して接点を確かめる。支持面は床以外の新しい小道具ではない。到達のために腕を伸ばさない。届かなければ前肢の先が触れられる身体側の低い接面へ安全に変更し、届かない床置きは捏造しない。

■ カメラ・画角・フレーミング
全身3/4。接点、肩、丸い腹、反対前肢、両足、尾を見える角度。

■ 顔・目・ひげ・感情
前肢の触点に視線を向ける集中顔、少しだけ口を結ぶ。可愛さを保つ。

■ 立体構造・Rig変形を想定した保護事項
接面と丸いpaw先の局所圧縮。腹・腕分離、支持脚の荷重、尾の従属を示す。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
腕長化、長い手指、接していないのに床がへこむ演出、胴の前転、尻尾支柱化。

■ Human Reviewで見る重点
動かした短い前肢と結果の接点が同時に見えて、身体構造を破壊しない。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
20番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-21 — Paw Release and Result Inspection / Purposeful Pause

- **Motion DRAFT:** P03 / P17
- **主眼:** 探究

```text
【Pino Reference 21 — Paw Release and Result Inspection / Purposeful Pause】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。探究の検査。関連する動作候補は P03 / P17（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
Pinoが試していた片前肢を低い接点から少し離し、離れた場所とpaw先との隙間を目で確かめて静止した瞬間。反対前肢は停止、両足で支持。前肢を振り回さない。

■ カメラ・画角・フレーミング
接点と数センチ相当の自然な空間が同時に読める全身3/4。拡大のために小さいpawのサイズを変更しない。

■ 顔・目・ひげ・感情
『こうなるんだ』と納得しそうな軽い発見。目線は実際の隙間、口は小さな好奇心。

■ 立体構造・Rig変形を想定した保護事項
短い前肢を置いた時からの連続した姿勢。肩根元・腹・前肢先は別立体、背中と尾は不必要に動かない。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
拍手、手揉み、魔法の光る床、見えない対象への注視、全身ジャンプ、長腕。

■ Human Reviewで見る重点
動かす→止まる→結果を見るというPinoの探索行動が1枚でも理解できる。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
21番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-22 — Low High-Five Target / Living WAIT

- **Motion DRAFT:** P14
- **主眼:** 交流

```text
【Pino Reference 22 — Low High-Five Target / Living WAIT】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。交流の検査。関連する動作候補は P14（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
Pinoが相手と低いハイタッチをしたくて、解剖学的左前肢の丸い先端を胸前の到達できる高さへ示し、相手を見ながら静かに待っている。短前肢を上げすぎない。足で重心を保持し、太尾は補助腕にしない。

■ カメラ・画角・フレーミング
全身3/4、対象の前肢先端が顔や腹で隠れない角度。前肢と顔が一目で結びつく。

■ 顔・目・ひげ・感情
柔らかい期待、両眼開眼、押し付けない微笑み。静止中もこちらを認識している。

■ 立体構造・Rig変形を想定した保護事項
肩と腹のクリアランス、提示したpawの実面、反対肢の自然な静止。尾は止まっている。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
人間のハイタッチ高さ、長腕、5本指、両腕挙上、浮いた両足、焦らす怒り顔。

■ Human Reviewで見る重点
相手からの反応を待つ自発的な誘いが読み取れる。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
22番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-23 — High-Five Touch ACK / Shared Happiness

- **Motion DRAFT:** P07 / P14
- **主眼:** 交流

```text
【Pino Reference 23 — High-Five Touch ACK / Shared Happiness】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。交流の検査。関連する動作候補は P07 / P14（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
提示していた解剖学的左前肢の先端に相手のタッチが届き、Pinoがその接点で小さく受けてから相手へ明るい顔を向ける途中の瞬間。相手の手は画面に描かず、paw先端の微小な局所受けと目の嬉しさで示す。

■ カメラ・画角・フレーミング
全身3/4、顔・触点paw・腹・足の支持を同画面に。

■ 顔・目・ひげ・感情
相手との共同発見が嬉しい、両眼の光と控えめな笑顔。瞳の魅力を維持。

■ 立体構造・Rig変形を想定した保護事項
paw先の局所変形と肩の小反応。前肢と腹、足と床の一体感を保ち、尾はわずかに遅れて従う。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
パンチ、強く叩き返す、人の手の創作、巨大な口、全身爆発的なジャンプ。

■ Human Reviewで見る重点
触れた場所が先に反応し、その後で嬉しいという因果が伝わる。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
23番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-24 — Self-Initiated Pet Invitation / Offer and Wait

- **Motion DRAFT:** P15
- **主眼:** 交流

```text
【Pino Reference 24 — Self-Initiated Pet Invitation / Offer and Wait】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。交流の検査。関連する動作候補は P15（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
Pinoが自分から少し頭を低く差し出し、額や頬を撫でてほしくて静かに待つ。前肢は内寄りに落ち着かせ、足支持のまま頭首だけ小さく前へ。探究の途中でも好意を優先できるPinoの人格を示す。

■ カメラ・画角・フレーミング
全身正面3/4。頭頂と頬の触れられる面、目、前肢、腹、接地足が読める。

■ 顔・目・ひげ・感情
『撫でていいよ』と感じる優しい期待。目を閉じ切らず、相手へ短く温かい目線を向ける。

■ 立体構造・Rig変形を想定した保護事項
首の小屈曲と頬/胸の非接触クリアランス。腹の潰れと頭の胴埋没を避ける。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
土下座、人間的手招き、指さし、無理に頭を床へ落とす、浮いた後脚、巨大に伸びる首。

■ Human Reviewで見る重点
Pinoの自発的な甘えと、押し付けない静かなWAITを可愛く読める。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
24番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-25 — Thick Tail Follow-through / Supported Turn

- **Motion DRAFT:** P04 / P05
- **主眼:** 尾

```text
【Pino Reference 25 — Thick Tail Follow-through / Supported Turn】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。尾の検査。関連する動作候補は P04 / P05（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
Pinoが両足の支持内で胴体をほんの少し回し、その回旋に対して骨盤から生えた単一の太い尾が遅れて付いてくる途中。尾は身体と連続し、根元は厚く、中央部は曲がり、先端は自然に収まる。動くのは尾が主導ではなく胴。

■ カメラ・画角・フレーミング
後側面が見えるRear-biased 3/4全身。骨盤・尾根元・尾中程・先端・両後脚の関係を重視。顔も一部見えてよい。

■ 顔・目・ひげ・感情
尾を見ることが実際の視界で可能なら小さな関心、無理なら自然な落ち着き。

■ 立体構造・Rig変形を想定した保護事項
尾の体積保存・断面の連続・捻れの回避。根元は胴に固定され自由区間のみ遅延。床へ吸着しない。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
尾を細くしならせる、ヒレ化、胴体との接続が切れる、尾を手で掴む、尾で身体を支える。

■ Human Reviewで見る重点
厚い尾が生きた身体の一部として遅れて動くイメージがある。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
25番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-26 — Rear Three-Quarter Tail Root Local ACK

- **Motion DRAFT:** P04 / P11
- **主眼:** 尾

```text
【Pino Reference 26 — Rear Three-Quarter Tail Root Local ACK】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。尾の検査。関連する動作候補は P04 / P11（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
Pinoを後方斜めから見て、後骨盤から生える太い尾の根元に軽い接触が届いた直後。接触そのものは人の手を描かず、尾根元の小さな受けと頭の短い注意で示す。後脚は床を支え、尾は荷重しない。

■ カメラ・画角・フレーミング
真のRear Three-Quarter、背面から30〜45度程度の後方優位。Sideに逃げず、腰幅・尾根元・短後脚が見える。

■ 顔・目・ひげ・感情
顔が十分見えるなら一瞬の気づき。正面顔の無理な表示より身体構造を優先。

■ 立体構造・Rig変形を想定した保護事項
背中/骨盤/尾根の自然な接合、腹の横厚み、根元の局所変形。尾自由区間と脚を癒着させない。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
側面をrearと偽る、尾が腰に貼り付く、二本尾、第三脚、過剰な全身ののけぞり。

■ Human Reviewで見る重点
後方からも太い尾が正しい位置から生えており、尾根元への接触が局所反応として見える。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
26番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-27 — Grounded Weight Shift / Two-Foot Support

- **Motion DRAFT:** P05
- **主眼:** 支持

```text
【Pino Reference 27 — Grounded Weight Shift / Two-Foot Support】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。支持の検査。関連する動作候補は P05（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
Pinoが片足へ少し重さを移して反対側の短い足の位置をわずかに整える途中。低い胴の重さが足へ伝わり、腹が柔らかく移るが丸い厚みは保持。腕は内寄り、太尾は自動的な支柱にせず従う。

■ カメラ・画角・フレーミング
全身Front 3/4、足底接地と胴の重心ラインが読める高さ。足を背景影で隠さない。

■ 顔・目・ひげ・感情
作業を邪魔しない自然な集中と軽い満足。片眼を閉じない。

■ 立体構造・Rig変形を想定した保護事項
左右足の接点、短脚の曲がり、骨盤位置、腹の局所corrective、尾の追従が一体として成立。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
片足で飛ぶ、ダンスの大足上げ、骨のない胴の横滑り、長脚、尾で転倒防止。

■ Human Reviewで見る重点
荷重を動かした理由と支持の変化が自然に読み取れる。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
27番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-28 — Low Relaxed Rest / Supported Settle

- **Motion DRAFT:** P06
- **主眼:** 休息

```text
【Pino Reference 28 — Low Relaxed Rest / Supported Settle】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。休息の検査。関連する動作候補は P06（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
Pinoが十分遊んだ後、自分で低い休息姿勢へ落ち着き、腹やお尻を無理に潰さず、短い後脚・足と必要な下胴の接地で楽に支持されている。Canon­icalの寝そべり姿勢は感情の参考であり、無条件コピーしない。尾は骨盤から自然に横または後ろへ置かれ、形状が連続する。

■ カメラ・画角・フレーミング
全身3/4やや低め、顔・腹・後脚・床接点・尾を見せる。

■ 顔・目・ひげ・感情
少し半眼でほっとしている。撫でられれば嬉しく反応しそうな愛着のある表情。

■ 立体構造・Rig変形を想定した保護事項
下胴・腹・脚・尾の局所圧縮、支持面への自然な沈み込み。全身縮尺変化は禁止。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
球を地面へ押し潰す、尾が切断、脚が消える、頭が前転、完全な無支持浮遊、Canonicalの泡を描く。

■ Human Reviewで見る重点
休む身体が柔らかく重く、再び立てる自然な脚・腹の関係がある。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
28番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-29 — Wake and Supported Rise / Rest Transition

- **Motion DRAFT:** P06 / P20
- **主眼:** 支持

```text
【Pino Reference 29 — Wake and Supported Rise / Rest Transition】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。支持の検査。関連する動作候補は P06 / P20（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
低い休息姿勢からPinoが起き始める中間姿勢。顔を少し上げ、短い前肢を無理に伸ばさず、両足と下胴で段階的に荷重を受け替える。すでに完全立位になっていない移行途中を正しく描く。

■ カメラ・画角・フレーミング
全身の前寄り3/4。頭・首・前肢・腹と床、両脚、尾根元が見える。

■ 顔・目・ひげ・感情
眠たさが残り、こちらへの好意と目覚めの興味が戻っている。

■ 立体構造・Rig変形を想定した保護事項
腹と後脚の隙間、頭の移動、尾の支持非依存、床の接点変化を自然に。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
腕の伸長で立ち上がる、脚を突然生やす、人間的な腰起こし、浮遊、尾の杖化。

■ Human Reviewで見る重点
休息と立位の中間として連続した身体の力学が想像できる。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
29番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-30 — Small Food Handling / Mouth and Short Paws

- **Motion DRAFT:** P21 / P22
- **主眼:** 食事

```text
【Pino Reference 30 — Small Food Handling / Mouth and Short Paws】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。食事の検査。関連する動作候補は P21 / P22（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
Pinoが小さな単純形状の試験用食品1個を、内寄りの短い前肢で無理なく口の近くに保持し、ちいさくひと口食べようとする。食品は無地でシンプルな仮小物、正式Foodデザインを新設しない。可愛い食事体験であり派手なパフォーマンスではない。

■ カメラ・画角・フレーミング
全身3/4やや寄り。口縁、両前肢、食品と腹の隙間、足支持が見える。

■ 顔・目・ひげ・感情
興味を持って食べる直前の両眼の関心。口は小さく自然に開く。

■ 立体構造・Rig変形を想定した保護事項
口の縁、顎、前肢先の保持領域、食品との非貫通。両足支持と尾重量を維持。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
長い指、箸・スプーン、舌の巨大化、尾把持、食品が腹を貫通、嚥下のため口を巨大化。

■ Human Reviewで見る重点
短いpawと小さな口で食べる動作が自然に成立しそうな顔・接点を示す。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
30番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-31 — Satisfied Taste / Delicious After-Savor

- **Motion DRAFT:** P23
- **主眼:** 食事

```text
【Pino Reference 31 — Satisfied Taste / Delicious After-Savor】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。食事の検査。関連する動作候補は P23（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
食べ終わったPinoが味の良さをしみじみ確かめ、静かに嬉しさへ変わった瞬間。食品や食器はもう描かず、短い前肢を内側に戻して、気持ちよい余韻が顔と身体の小さな弛緩に残る。

■ カメラ・画角・フレーミング
頭・口・頬・胸・内寄り前肢・支持足が見える正面3/4。

■ 顔・目・ひげ・感情
自然にほどける瞼、丸い頬、小さく幸福な微笑み。過剰な大口や舌を見せない。

■ 立体構造・Rig変形を想定した保護事項
口周り・頬の繊細なshape変化、胴と尾のわずかなsettle、脚支持。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
食品の再追加、カラフルなエフェクト、舌を出しっぱなし、口の形が別個体、泡。

■ Human Reviewで見る重点
食後に自分の好きなものを味わっている可愛さが直感的に伝わる。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
31番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-32 — Gentle Gift Presentation / Short Paw Transfer

- **Motion DRAFT:** P27
- **主眼:** 交流

```text
【Pino Reference 32 — Gentle Gift Presentation / Short Paw Transfer】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。交流の検査。関連する動作候補は P27（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
Pinoが小さな無地の試験用ギフトを低い胸前で丁寧に提示し、相手が受け取るのを待つ。短い両前肢で持てる最小限の寸法。相手に贈りたい好意が目的で、玩具を試すことが主役ではない。仮小物は正式ギフトを確定しない。

■ カメラ・画角・フレーミング
全身3/4。小物・両paw・腹・顔・足支持が同時に確認できる角度。

■ 顔・目・ひげ・感情
相手を気にする優しい目と小さな期待の微笑み。

■ 立体構造・Rig変形を想定した保護事項
両肩と丸いpaw先の保持、ギフトと腹の隙間、受け渡し可能な低い空間。尾は保持に使わない。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
手が5本指、長腕、投げる、腕腹融合、ギフトが顔や腹を突き抜ける、尾で持つ。

■ Human Reviewで見る重点
小さな前肢の可愛さを活かしつつ、受け渡しの意図と支持が読み取れる。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
32番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-33 — Natural Paw Sole Underside / Pad Anatomy

- **Motion DRAFT:** P05 / P06
- **主眼:** 構造

```text
【Pino Reference 33 — Natural Paw Sole Underside / Pad Anatomy】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。構造の検査。関連する動作候補は P05 / P06（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
Pinoが安定した低い休息姿勢で座り、片方の短い後足の足底だけが自然に少しカメラへ向く。Canon­ical由来の肉球の位置・形・淡い色を観察できる。もう一方の足と下胴が支持し、尾は骨盤後ろに自然に配置。両足を同時に宙へ持ち上げない。

■ カメラ・画角・フレーミング
下半身を少し大きく見せる全身近い前方低め3/4。足裏・短脚・腹と床の関係、顔の表情まで入れる。

■ 顔・目・ひげ・感情
静かな休息の微笑み、両眼は自然。

■ 立体構造・Rig変形を想定した保護事項
足底の厚み、肉球、足首の短さ、支持している反対足と腹下胴の境界を明瞭にする。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
肉球をすね正面へ移す、足指を長大化、人間の足裏形状、浮遊する両足、腹が足を飲み込む。

■ Human Reviewで見る重点
立位では隠れる足裏意匠を、解剖学的に正しい位置で確認できる。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
33番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```

### REF-34 — Wear Anchor Comfort / Head Neck Clearance

- **Motion DRAFT:** P24
- **主眼:** 構造

```text
【Pino Reference 34 — Wear Anchor Comfort / Head Neck Clearance】

■ 目的・承認境界
GrimoのPino本人のRig / Shape Key / Motion制作用の高品質な2Dリファレンスを1枚制作する。構造の検査。関連する動作候補は P24（2026-10-11版DRAFT）であり、新規の正式Motion・Human承認・実機合格を示すものではない。Pinoらしい可愛さ・癒やし・好意と、実際の3Dで成立しそうな局所動作・支持を最優先する。新しいカワウソを発明しない。

■ 添付Authority — 全画像に同じ5枚を入力する
Image A：assets/grimo/source/pino/pino-Identity-canonical.png — Pino本人の顔・瞳・耳・頬・鼻・口・ひげ・頭頂毛束、青白い色、可愛さ、個体Identityの最上位。Canonicalの片眼ウインクは表情であり単眼構造ではない。
Image B：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_front.png — Human選定済み正面Body-only。頭と胴体の比率、丸い腹、左右前肢、後肢、足の位置。
Image C：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_left.png — Human選定済み画面左向きSide。顔・腹・脚・尾の前後奥行き。実際の解剖学的左右とは区別する。
Image D：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_right.png — Human選定済み画面右向きOpposite Side。Cとは反対の方向を向く。単純なミラー画像として扱わない。
Image E：assets/grimo/source/pino/tripo-generation-pose/pino_bodyonly_back.png — Human選定済みBack。背中・骨盤幅・脚・尾根元の立体接続。

■ この画像だけの具体的な身体姿勢・演技
Pinoに試験用の極めて単純な無地・中性色の柔らかな装着位置ガイドを頭上または首胸のいずれか一箇所だけに仮置きし、Pinoが新しい感触を確認している。装着物は正式Wearデザインではなく、可動と干渉を見る薄い非恒久マーカー。頭頂毛束と耳、顔を隠さない。

■ カメラ・画角・フレーミング
全身正面3/4。頭・耳・首胸と両短前肢・腹のクリアランスが見える。

■ 顔・目・ひげ・感情
違いに気づき、ほっと納得した両眼の優しい表情。

■ 立体構造・Rig変形を想定した保護事項
装着箇所の表面アンカー、頭首の可動、前肢が胸へ近づくときの余地。体形は変えない。

■ Pino本人の造形・質感の固定条件
幼い丸い大頭、光沢ある大きな両眼、小さく丸い耳と鼻・口、ふくらんだ頬と自然なひげ、頭頂毛束、Canonicalの青白い配色と固有模様を守る。丸くふっくらした低い胴、白い腹、左右に独立した短く内寄りの前肢、短い後脚と足、後骨盤に連続する単一の幅広く厚い尾を守る。足底の肉球の位置を移さない。眼球・眼窩・上下瞼は両側に存在し、左右独立して閉眼可能な立体を前提にする。新しい眉・人間の指・長腕・長脚・細い腰・尾の把持は禁止。
Image Aの完成時の可愛さをImage B〜Eの生成用姿勢で上書きしない。B〜Eは形状・寸法・方向を保護するための派生Authorityであり、Canonicalの低い水遊び姿勢、Tripo Generation Pose、Rig Rest Pose、Game Interaction Neutralを同一視しない。
接地/重心/支持は見た目で成立させる。腹と前肢、腹と後脚、尾と脚を溶接したように融合させず、肩・股・尾根元は解剖学的につながる。尾は平板なヒレでも細いロープでもなく、断面と根元の厚みが連続する。尾を第三の手や常設支柱にしない。全身を空気風船のように伸縮・バウンドさせない。
上質で可愛いスタイライズド3Dキャラクターのような、柔らかい立体感と控えめな体表ディテール。濡れゴム・硬質プラスチック・写実的すぎる毛・別の画風は禁止。淡い自然な照明、無地のニュートラル背景、接地を隠さない弱い影。人物・文字・寸法線・ラベル・透かしなし。泡・水しぶき・遊離した水滴など独立エフェクトは生成しない。各Referenceで明示した試験用Food/Gift/Wear以外の小物は生成しない。
1枚の高品質な静止画像のみ。参照の方向、身体、顔、色、支持を守るために、構図の可読性よりPinoのIdentityが優先する。2D画像は候補資料でありHuman承認・実Rig/3D検証済みとは言わない。

■ この画像固有の禁止・特に検出すべき破綻
正式装備意匠を新設、冠で耳を隠す、頭部が大きく変わる、首が細長くなる、前肢や尾にWearを装着、複数装着。

■ Human Reviewで見る重点
Identityを守る1か所の装着余地と顔・腕の通常Motionを両立できる。
顔の可愛さ、同一個体感、青白い色、まぶた、頬、短い左右前肢・脚、腹と肢の非融合、尾の断面・根元、床支持、接点と視線の因果を総合評価する。必要な形状が現実の3Dで動くかは後工程の実Rig/GLBで確認し、この画像だけでは認定しない。

■ 出力
34番だけの高品質な静止画像を1枚。無地背景・文字なし。原典は改変禁止。
```
