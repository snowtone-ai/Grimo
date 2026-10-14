# Jill — Rig / Shape Key / Motion Reference Image Prompts

**作成:** 2026-10-15　**対象:** Jill本人のみ　**件数:** 35（画像01–34設計上の基本検討、35はSecret任意候補）。本ファイルは画像生成プロンプトのAuthorityであり、**Human承認済み画像・Motion FINAL・Rig/Runtime PASSではない**。

## 実行者への短い運用契約（PROMPT本文とは別）

1. 作業branch/HEAD、`AGENTS.md`、Goal√map、Character Experience Specと必要なMotion DRAFTを確認し、元画像を不変で保護。画像生成のたびに後記の**該当PROMPT一つ**と、その中に明記された正式**実画像5枚**を入力する。単なるファイルパスの文字列だけでは画像入力を代替しない。
2. Codex内蔵`image_gen`使用を最優先。最初に01を1回試して可用性確認。使用不能またはnetwork errorなら**IMAGEGEN_UNAVAILABLE**として停止。API/CLIへの自動切替、`OPENAI_API_KEY`要求、追加課金、外部画像サービス/Tripoクレジット消費は禁止。
3. 01–03を先行して視認し、重大なIdentity崩壊、翼根・葉・前肢の融合、部位増減、支持不成立があれば以降の一括生成を止め、成功分だけ残す。軽微なら04–34を続行。35はOPTIONALなので安全に成立する場合のみ作成可能。Humanの代わりに可愛さPASSを決定しない。
4. 原則**各画像1回**、明らかな局所欠陥だけ最大1回の修正。修正でも正式画像5枚の添付を守る。大量再試行・過剰なテストや全リポジトリ調査はしない。
5. 作成したPNGは`assets/grimo/production/jill/references/jill-ref-XX.png`へ保存。Codex内蔵生成の標準保存先から必要なファイルだけ作業ツリーへコピー。既存成果は勝手に上書きしない。README/REVIEWにはファイルの有無・簡潔な所見・**Human=PENDING**を記録、必要ならcontact sheetを作る。安全な範囲でcommit/push。巨大バイナリやGit制約で公開できなければローカル成果を保持して阻害要因を報告。
6. 01–35は35 clip/35必須Shape Keyを意味しない。DRAFT J01–J26の詳細演技は未承認。J27は任意候補。ゲーム内通常支持・Rig Rest・自動Rigの適合も未確定。

**5入力のパスと順序:** A `assets/grimo/source/jill/jill-Identity-canonical.png`、B `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`、C `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`、D `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`、E `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。画像を実際に読み、登録Rightはscreen-right向き、Leftはscreen-left向きであることを照合する。背面はE。正式Body-onlyの2D選定はGeometryやRig受入ではない。

**資料由来:** `docs/grimo/knowledge/Goal√map.md`、`docs/grimo/knowledge/GRIMO_CHARACTER_EXPERIENCE_SPEC.md`、`docs/production/motion/GRIMO_FOUR_CHARACTER_MOTION_ARCHITECTURE_DRAFT.md`、`docs/production/motion/GRIMO_MOTION_TO_ANATOMY_TRIPO_CONTRACT_DRAFT.md`、`docs/grimo/knowledge/character-production/GRIMO_BODY_ONLY_MULTIVIEW_ASSET_REGISTER.md`。特にJillの胸先行の喜び、翼・葉・尾の選択的参加、局所ACK、WAIT、接地を保持。

## 全画像インデックス

| ID | 完全独立のReference名 | 関連Motion | 区分 |
|---|---|---|---|
| 01 | Neutral Front Three-Quarter | J01/J24 | PILOT |
| 02 | True Left-Facing Profile | J01/J02/J04 | PILOT |
| 03 | Unilateral Wing Partial Opening | J03/J14 | PILOT |
| 04 | Rear Three-Quarter / Folded Wings | J01/J03/J05 | CORE |
| 05 | Grounded Weight Shift / Tail Follow | J04/J23 | CORE |
| 06 | Attentive / Shareable Gaze | J02/J24 | CORE |
| 07 | Natural Full Blink / Closed Eyes | J01/J05 | CORE |
| 08 | Sleepy Half-lidded | J05/J01 | CORE |
| 09 | Small Contentment | J01/J10/J23 | CORE |
| 10 | Outward Delight / Wings Join | J14/J21 | CORE |
| 11 | Soft Surprise | J15 | CORE |
| 12 | Gentle Boundary Hint | J16 | CORE |
| 13 | Grounded Mild Withdrawal | J17 | CORE |
| 14 | Warm Recovery | J18 | CORE |
| 15 | Forehead Pet / Head Lowering | J06/J10 | CORE |
| 16 | Anatomical Left Cheek Offer | J07/J13 | CORE |
| 17 | Anatomical Right Cheek Offer | J07/J13 | CORE |
| 18 | Chest Touch / Local Response | J08/J10/J11 | CORE |
| 19 | Wing-root Touch / Protected ACK | J09 | CORE |
| 20 | Tail-root Touch / Heavy ACK | J09 | CORE |
| 21 | Low Forepaw High-five OFFER/WAIT | J12 | CORE |
| 22 | High-five Contact / Shared Payoff | J12/J14 | CORE |
| 23 | Self-Initiated Affection Invitation | J13 | CORE |
| 24 | Private Stretch / Wing Care | J03 | CORE |
| 25 | Low Relaxed Rest / Grounded Settle | J05/J04 | CORE |
| 26 | Warm Afterglow / Delayed Look-back | J23/J26 | CORE |
| 27 | Small Bite / Chewing Mouth | J20 | CORE |
| 28 | Gentle Lick / Tongue Contact | J20 | CORE |
| 29 | Drinking / Small Mouth Contact | J20 | CORE |
| 30 | Large Food / Forepaw Assist | J20 | CORE |
| 31 | Taste Evaluation / Mild Preference | J21 | CORE |
| 32 | Favorite Taste / Shared Happiness | J21 | CORE |
| 33 | Wear Anchor / Recognition Clearance | J22 | CORE |
| 34 | Gift Presentation / WAIT | J25 | CORE |
| 35 | OPTIONAL Wing-Shelter Peek | J27 OPTIONAL | OPTIONAL |

---

## PROMPT 01 — Neutral Front Three-Quarter

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Neutral Front Three-Quarter**を描く。対応する検討Motion：**J01/J24**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
全身の正面3/4、約25〜35°の回り込み。両目、胸、左右短前肢、短い後肢、翼収納、尾の接続と接地影が見える。中望遠的な弱い遠近感。

### 画像固有の表情・ポーズ・身体変形
開眼の穏やかな好意。胸は自然に丸く、前肢を腹から離して低く休め、後足の安定支持を保つ。左右翼は自然に畳み、尾は骨盤から太く巻く。Canonicalの座位をGame Neutralと断定しない。

### 重要検査点と追加の禁止
Identity、顔幅、頭と胴体の比率、翼根と膜厚、葉と首、腹のクリーム段模様、短い手足の独立。長い脚・腕、細い腰、翼膜の融合、尾支柱化を禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Neutral Front Three-Quarter**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 02 — True Left-Facing Profile

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**True Left-Facing Profile**を描く。対応する検討Motion：**J01/J02/J04**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
鼻先が画面左を向く正確な90°の全身側面。カメラ水平で正投影に近く、遠い側の翼・足を手前へ引き出さない。尾先と翼先まで見切れない。

### 画像固有の表情・ポーズ・身体変形
横顔の小さな鼻、頬、顎、後頭部の奥行きをImage Cから再現。自然な開眼と優しい口。短い前肢は胸から独立し、短く太い後脚が床に接する。

### 重要検査点と追加の禁止
頭・首葉・胸・腹・骨盤・翼根・太尾根元の前後連続。長い鼻、尖った顎、首の空洞、長胴、翼根が葉へ埋まる状態を禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**True Left-Facing Profile**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 03 — Unilateral Wing Partial Opening

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Unilateral Wing Partial Opening**を描く。対応する検討Motion：**J03/J14**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
全身正面3/4、30〜45°。手前の翼の根元と膜、両目、胸、短前肢、地面の接点をできる限り同時に観察。

### 画像固有の表情・ポーズ・身体変形
楽しさが顔と胸から生まれ、手前側の片翼だけが中程度に自然展開。奥側翼は収納。胸を小さく起こすが足は接地し、前肢と太尾は静かなまま。

### 重要検査点と追加の禁止
翼の実根元・淡クリーム膜と緑枠の連続、膜裏と厚み、翼と頭葉・首葉・前肢の非干渉。膜の紙化、根元潰れ、顔の遮蔽、飛行を禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Unilateral Wing Partial Opening**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 04 — Rear Three-Quarter / Folded Wings

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Rear Three-Quarter / Folded Wings**を描く。対応する検討Motion：**J01/J03/J05**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
側面寄りではない後方優位の約35〜45°全身。後頭葉、両翼背面、骨盤、短い後脚、尾根元を明確に見せる。

### 画像固有の表情・ポーズ・身体変形
落ち着いた休息姿勢で左右翼を収納。頭を極端に振り返らず、片側頬・目が少し見える範囲で本人らしさを保つ。

### 重要検査点と追加の禁止
Image Eによる左右翼根、膜の折畳み、背葉の所属、太尾と骨盤の連結。背中の新しい花、二翼の板化、尾根の切断を禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Rear Three-Quarter / Folded Wings**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 05 — Grounded Weight Shift / Tail Follow

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Grounded Weight Shift / Tail Follow**を描く。対応する検討Motion：**J04/J23**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
低めの全身3/4。後足の位置と床接地、骨盤・胸・太尾の関係が読める。

### 画像固有の表情・ポーズ・身体変形
姿勢を整えるため一方の足へ小さく荷重を移し、他方を軽く置き直す瞬間。胸と頭は自然に補正し、尾は太さを保ち体幹に従う。翼は静止。

### 重要検査点と追加の禁止
短く太い脚・腹部重量・足底・尾根の連続。足が浮く、尾支柱、人間歩行、胴のゼリー変形を禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Grounded Weight Shift / Tail Follow**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 06 — Attentive / Shareable Gaze

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Attentive / Shareable Gaze**を描く。対応する検討Motion：**J02/J24**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
顔・胸中心の3/4ミディアム。両眼、角、頭葉と首の一部が見える。

### 画像固有の表情・ポーズ・身体変形
何かに気づき、瞳が先に横へ動いて小さく頭が追従。口元と頬で好奇心を示し、胸は相手へ開く余地を残す。翼と下半身は止める。

### 重要検査点と追加の禁止
独立した視線・瞼・頭回旋、首葉の連結。目玉飛び出し、極端な横目、翼の同時羽ばたき禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Attentive / Shareable Gaze**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 07 — Natural Full Blink / Closed Eyes

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Natural Full Blink / Closed Eyes**を描く。対応する検討Motion：**J01/J05**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
顔の正面3/4クローズアップ。両眼位置と頬、口、角、頭葉、胸上部を含める。

### 画像固有の表情・ポーズ・身体変形
両眼を自然に完全閉眼する。上下瞼が眼球の丸みを残して合わさり、閉眼線は柔らかい。頬は安心した小微笑み。頭は大きく動かさない。

### 重要検査点と追加の禁止
再開眼で同じ大きな瞳に戻れる形状。太い黒線を描いただけの目、目の消失、眉追加、頬の潰れを禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Natural Full Blink / Closed Eyes**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 08 — Sleepy Half-lidded

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Sleepy Half-lidded**を描く。対応する検討Motion：**J05/J01**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
眼と頬が読める顔・胸の3/4。翼上部と頭葉も見せる。

### 画像固有の表情・ポーズ・身体変形
瞳を部分的に見せた自然な半閉眼。安心した眠さはあるが周囲を認識している。頭・胸を少し低く休ませ、翼は畳む。

### 重要検査点と追加の禁止
上下瞼・虹彩・頬の容積、低頭と首葉の接続。睨み目、失神した完全無反応、細長い首を禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Sleepy Half-lidded**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 09 — Small Contentment

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Small Contentment**を描く。対応する検討Motion：**J01/J10/J23**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
顔と胸上部、短い前肢の一部を含む正面3/4。

### 画像固有の表情・ポーズ・身体変形
触れ合いの後の小さな幸福。開眼の優しいまなざしと頬、控えめな口の弧で温かさを見せる。胸だけが少しほどけ、翼は静止。

### 重要検査点と追加の禁止
頻繁に使える微表情、瞼と頬・小口の整合。大口笑顔、過剰ウインク、全翼展開で幸福を代替すること禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Small Contentment**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 10 — Outward Delight / Wings Join

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Outward Delight / Wings Join**を描く。対応する検討Motion：**J14/J21**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
全身3/4、顔・胸・両翼と接地脚・太尾を一画面に配置。

### 画像固有の表情・ポーズ・身体変形
相手の返事を受けた明確な喜び。目と頬が先に輝き、胸が少し上がり、短前肢が低く開く。両翼は必要な範囲だけ部分展開、葉はわずかに追従。

### 重要検査点と追加の禁止
翼根・膜・枠、首葉、胸と腕の独立、接地。最大開口・ジャンプ・飛行・顔を隠す翼を禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Outward Delight / Wings Join**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 11 — Soft Surprise

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Soft Surprise**を描く。対応する検討Motion：**J15**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
顔と胸の3/4。眼・小さな口・顎と頭葉が大きく見える。

### 画像固有の表情・ポーズ・身体変形
無害な意外性への一瞬の驚き。瞳と小口が少し開き、顔が原因へ向き、胸は一拍停止。すぐに好奇心へつながる柔らかさ。

### 重要検査点と追加の禁止
口の小開閉、眼窩の自然な拡張、首の回旋。恐怖、威嚇、長い牙や巨大口、翼の大展開を禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Soft Surprise**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 12 — Gentle Boundary Hint

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Gentle Boundary Hint**を描く。対応する検討Motion：**J16**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
顔・胸・接触側前肢・翼根が見える3/4。

### 画像固有の表情・ポーズ・身体変形
接触が少し過密で小さく戸惑う。目と口に控えめな区切り、胸を少し閉じ、前肢と翼を安全な範囲へ収める。下半身は安定。

### 重要検査点と追加の禁止
穏やかな非敵対表情と肩根の収納。怒鳴り・泣き・翼威嚇・尾の攻撃を禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Gentle Boundary Hint**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 13 — Grounded Mild Withdrawal

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Grounded Mild Withdrawal**を描く。対応する検討Motion：**J17**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
全身3/4で支持点・太尾・顔の向きが見える。

### 画像固有の表情・ポーズ・身体変形
刺激面から頭と胸を少し離し、前肢と翼を内へ守る。相手を認識したまま自分の余地を取り戻す。短脚は自立、尾は追従。

### 重要検査点と追加の禁止
支持域内の小後退と首葉の曲げ。足滑り、尾で払う、長い人間脚、落ち込む悲嘆顔を禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Grounded Mild Withdrawal**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 14 — Warm Recovery

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Warm Recovery**を描く。対応する検討Motion：**J18**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
顔・胸・肩・畳んだ翼が見える3/4。

### 画像固有の表情・ポーズ・身体変形
刺激が解け、保護していた胸と前肢が緩み、目が相手へ短く戻る。口に小さな温かさ。急に喜びのピークへ飛ばない。

### 重要検査点と追加の禁止
瞼・頬・口・翼の落ち着き方。全身強制Neutral、無理な再招待、瞬間happy flipを禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Warm Recovery**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 15 — Forehead Pet / Head Lowering

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Forehead Pet / Head Lowering**を描く。対応する検討Motion：**J06/J10**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
額の軟部面と眼・角、首と胸が見える近めの3/4。

### 画像固有の表情・ポーズ・身体変形
額を撫でられた柔らかな受容。目が少しほどけ、自分から頭を少し下げる。胸は落ち着き、翼と尾は静か。

### 重要検査点と追加の禁止
実在の額軟部と硬い角の分離、首葉・顎の連続。角を耳として曲げる、顔を地面へ突っ込む、外部の手へ体重を預けること禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Forehead Pet / Head Lowering**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 16 — Anatomical Left Cheek Offer

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Anatomical Left Cheek Offer**を描く。対応する検討Motion：**J07/J13**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
解剖学的左頬が相手へ向く顔・胸3/4。画面上の左右だけで向きを定めず、B〜Eの体と顔の構造から側を判断。

### 画像固有の表情・ポーズ・身体変形
左頬の厚みを保ち、頭を少し向けて撫でられる面を提示。瞳と小口で期待を示す。胸は小さく開き、翼は休む。

### 重要検査点と追加の禁止
頬・眼窩・顎・首葉の局所可動。両頬の同時膨張、翼による顔の遮蔽、細首禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Anatomical Left Cheek Offer**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 17 — Anatomical Right Cheek Offer

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Anatomical Right Cheek Offer**を描く。対応する検討Motion：**J07/J13**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
解剖学的右頬を相手に見せる顔・胸3/4。Right画像の実際の向きに注意し、単純な画像反転はしない。

### 画像固有の表情・ポーズ・身体変形
右頬の自然な接触面と小さな期待。目の可愛さと右側角・頭葉を維持して頭を少し回す。胴体・翼は安定。

### 重要検査点と追加の禁止
反対側の頬と顎の立体整合、模様の個体的な配置。右眼のずれ、左右模様の鏡像コピー、片翼の誤移植禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Anatomical Right Cheek Offer**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 18 — Chest Touch / Local Response

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Chest Touch / Local Response**を描く。対応する検討Motion：**J08/J10/J11**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
胸のクリーム段模様と短前肢・翼根が見える全身寄り3/4。

### 画像固有の表情・ポーズ・身体変形
胸の実在の触面が小さく局所反応し、顔が触れた場所を確かめてから温かく喜ぶ。前肢を必要なだけ低くほどく。

### 重要検査点と追加の禁止
胸と前肢・翼の独立、模様の保持、局所圧縮。全胸ゼリー化、クリーム段消失、翼膜の連れ変形を禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Chest Touch / Local Response**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 19 — Wing-root Touch / Protected ACK

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Wing-root Touch / Protected ACK**を描く。対応する検討Motion：**J09**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
触れられる一方の翼根、背中の葉、前肢と顔の一部が見える後方寄り3/4。

### 画像固有の表情・ポーズ・身体変形
翼根への小さな気付き。目が同側へ向き、触れた翼だけ安全なfold方向へ軽く動く。反対翼は静か、膜は引っ張らない。

### 重要検査点と追加の禁止
実翼根・膜表裏・肩との分離。引き伸ばした膜、耳のような揉み、根元消失、両翼大羽ばたきを禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Wing-root Touch / Protected ACK**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 20 — Tail-root Touch / Heavy ACK

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Tail-root Touch / Heavy ACK**を描く。対応する検討Motion：**J09**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
骨盤と太尾の根元・尾先・脚と顔の一部が見える後方3/4。

### 画像固有の表情・ポーズ・身体変形
尾根元の接触を認識して目を少し向け、根元だけ小さく調整。太い尾は骨盤に従い、後脚支持は変わらず翼は静止。

### 重要検査点と追加の禁止
尾根元と骨盤の体積・稜線・腹側クリーム帯。紐の尾、握る尾、三脚化、後脚との融合禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Tail-root Touch / Heavy ACK**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 21 — Low Forepaw High-five OFFER/WAIT

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Low Forepaw High-five OFFER/WAIT**を描く。対応する検討Motion：**J12**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
全身正面3/4。提示する片前肢の実面、目・胸・足底を明確に見せる。

### 画像固有の表情・ポーズ・身体変形
相手と『ちょん』を交わしたい小さな期待。短い片前肢を低く差し出し、胸を少し開いてWAIT。もう片腕と短い後肢は支持を維持。翼と尾は静止。

### 重要検査点と追加の禁止
短前肢の肩・先端、触れられる面と腹の隙間。長い指、空中に浮く脚、翼を手の代用、催促顔禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Low Forepaw High-five OFFER/WAIT**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 22 — High-five Contact / Shared Payoff

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**High-five Contact / Shared Payoff**を描く。対応する検討Motion：**J12/J14**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
顔・胸・提示前肢先を近めの全身3/4で見せる。

### 画像固有の表情・ポーズ・身体変形
先端がちょんと触れられた直後、前肢が小さく受け、胸と顔に届いた喜びが広がる。翼は小参加に留め、後脚は接地。

### 重要検査点と追加の禁止
局所ACKと胸の感情の分離、腕と翼根の余地。巨大な他者の手、長腕、接触前成功、大きいジャンプを禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**High-five Contact / Shared Payoff**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 23 — Self-Initiated Affection Invitation

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Self-Initiated Affection Invitation**を描く。対応する検討Motion：**J13**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
触れられる頭・頬の実面が見える、胸までの正面3/4。

### 画像固有の表情・ポーズ・身体変形
楽しい気分のJillが自分から頭や片頬を少し差し出し、開眼の期待を保って静かに待つ。短前肢は低く、翼を閉じ、下半身を安定。

### 重要検査点と追加の禁止
頬・額の軟部、角・首葉の非圧縮、接地。外部の手を支柱にする、細首、無応答でしょげる表情禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Self-Initiated Affection Invitation**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 24 — Private Stretch / Wing Care

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Private Stretch / Wing Care**を描く。対応する検討Motion：**J03**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
全身3/4。胸・手前片翼根・短前肢が見える構図。

### 画像固有の表情・ポーズ・身体変形
自分のために胸を気持ちよく伸ばし、一方の翼を置き直す小さな身繕い。届く自分の身体面に短前肢を添えるなら自然な範囲だけ。翼・葉は付け根を保持。

### 重要検査点と追加の禁止
肩と背面翼根の非干渉、膜と枠の自然な折畳み。翼を腕で握る、葉を引き抜く、飛行や大反りを禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Private Stretch / Wing Care**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 25 — Low Relaxed Rest / Grounded Settle

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Low Relaxed Rest / Grounded Settle**を描く。対応する検討Motion：**J05/J04**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
全身3/4、腹下・短脚・床・翼と尾の関係が分かる少し低いカメラ。

### 画像固有の表情・ポーズ・身体変形
遊び終えて自分から胸と頭を少し下げ、短肢と実在の足底で静かに休む。両翼は自然に収納、太尾は後方で重く巻く。

### 重要検査点と追加の禁止
低姿勢での腹・腿・足底の実体、首葉と翼根、再び動ける余地。腹脚一塊化、翼の床刺さり、尾椅子、長脚禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Low Relaxed Rest / Grounded Settle**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 26 — Warm Afterglow / Delayed Look-back

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Warm Afterglow / Delayed Look-back**を描く。対応する検討Motion：**J23/J26**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
顔・胸・前肢・翼収納が読める正面3/4。

### 画像固有の表情・ポーズ・身体変形
喜びのピークを終え胸と翼が落ち着いた後、瞳と小口に温かさが残って相手をもう一度見る。再び催促はしない。

### 重要検査点と追加の禁止
表情と胸・翼の余韻が非同期で自然に終わること。ウインク依存、全身一斉Neutral、毎回新しい高揚禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Warm Afterglow / Delayed Look-back**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 27 — Small Bite / Chewing Mouth

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Small Bite / Chewing Mouth**を描く。対応する検討Motion：**J20**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
鼻・口・小牙・顎、瞳と胸上部が見える顔中心3/4。

### 画像固有の表情・ポーズ・身体変形
ごく小さな無地の食物を一口確かめる自然な小開口。短い上顎と下顎を壊さず、小牙と口内の奥行きを保つ。前肢と翼は休む。

### 重要検査点と追加の禁止
噛む途中の口縁・頬・顎・口内の立体。巨大口、人間歯列、牙増殖、食品で顔が隠れる状態禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Small Bite / Chewing Mouth**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 28 — Gentle Lick / Tongue Contact

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Gentle Lick / Tongue Contact**を描く。対応する検討Motion：**J20**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
顔の正面3/4クローズアップ。目・鼻・口・顎が全て見える。

### 画像固有の表情・ポーズ・身体変形
ごく小さい味を舌先で確かめる。Canonicalにない舌の形状は確定仕様でなく、必要最低限の短い自然な舌を小口から出す検討例。顔と胸は落ち着く。

### 重要検査点と追加の禁止
短い舌と口縁・小牙・顎の整合。長い蛇舌、二叉舌、よだれ、大口化、顔の変更を禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Gentle Lick / Tongue Contact**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 29 — Drinking / Small Mouth Contact

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Drinking / Small Mouth Contact**を描く。対応する検討Motion：**J20**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
小口と飲み口、胸・短前肢が見える近めの3/4。

### 画像固有の表情・ポーズ・身体変形
頭をわずかに低くして無地で浅い検討用容器から飲む。微かな満足、目は柔らかいまま。容器は商品仕様・正式Giftを意味しない。翼と足は休む。

### 重要検査点と追加の禁止
鼻・小口・下顎の水面接点、低頭での首葉。長い舌、口の貫通、顔の水没、翼や尾による支持を禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Drinking / Small Mouth Contact**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 30 — Large Food / Forepaw Assist

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Large Food / Forepaw Assist**を描く。対応する検討Motion：**J20**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
全身寄り正面3/4。口・胸・短前肢の届く範囲と足底が読める。

### 画像固有の表情・ポーズ・身体変形
無地の小さな丸い検討用Foodを、短い片前肢で低く支えながら口へ近づける中間姿勢。頭を自然に寄せ、翼は収納、足で自立。

### 重要検査点と追加の禁止
手足を伸ばさず口とFoodの接点・片前肢の支持面を作る。人間的な保持、長指、翼把持、尾支柱禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Large Food / Forepaw Assist**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 31 — Taste Evaluation / Mild Preference

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Taste Evaluation / Mild Preference**を描く。対応する検討Motion：**J21**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
顔と胸が中心の正面3/4。食後なのでFoodを写さない。

### 画像固有の表情・ポーズ・身体変形
食後の好き度2相当の微妙な評価。瞳に小さな迷い、口元がごく短く収まり、胸が少し休む。嫌悪ではなく穏やかな『少し違った』。

### 重要検査点と追加の禁止
小口・瞼・頬の微差と食後顎の閉鎖。吐き出し、泣く、怒り、嘔吐表現、威嚇翼禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Taste Evaluation / Mild Preference**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 32 — Favorite Taste / Shared Happiness

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Favorite Taste / Shared Happiness**を描く。対応する検討Motion：**J21**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
全身正面3/4。顔・胸・自然な翼部分参加・脚が見える。

### 画像固有の表情・ポーズ・身体変形
好き度5相当の食後、味を確かめた後に喜びを相手へ開く。明るい眼と頬、Canonical内の小笑顔、胸の伸び、短前肢の低い開き、部分的な翼の参加。

### 重要検査点と追加の禁止
翼根と葉の追従、太尾と接地、食後の口元。巨大に膨らむ腹、最大羽ばたき、FX依存、飛行を禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Favorite Taste / Shared Happiness**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 33 — Wear Anchor / Recognition Clearance

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Wear Anchor / Recognition Clearance**を描く。対応する検討Motion：**J22**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
顔・頭・首・胸・両翼根が見える3/4。

### 画像固有の表情・ポーズ・身体変形
頭中央または首胸に小さな無地の検討用仮装備1点を置く。正式採用装備ではなく装着アンカーの検査。Jillは気づいて軽く喜び、目線を極端に曲げない。

### 重要検査点と追加の禁止
角・頭葉・体表花・胸模様・翼根を隠さず装備が分離して見える。大型帽子、複数同時Wear、Canonical装飾の置換禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Wear Anchor / Recognition Clearance**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 34 — Gift Presentation / WAIT

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**Gift Presentation / WAIT**を描く。対応する検討Motion：**J25**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
全身正面3/4。顔・胸・片前肢で提示する小物・足底が読める。

### 画像固有の表情・ポーズ・身体変形
小さな無地の検討用Gift仮小物1点を、短前肢の届く低い位置または胸前でそっと見せる。相手へ嬉しそうに差し出しWAIT。翼は畳み、尾と脚は支持を維持。

### 重要検査点と追加の禁止
Giftの接触・保持・解放を想定できる面。長腕、人間指、翼把持、品物の浮遊、受領済みの偽装禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**Gift Presentation / WAIT**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。

---

## PROMPT 35 — OPTIONAL Wing-Shelter Peek

> **このセクション単独でコピー可能なフル生成プロンプト。** 別プロンプト、別Reference画像、共通ベースの外部参照は不要。

### 目的・Motion
GrimoのJillの**OPTIONAL Wing-Shelter Peek**を描く。対応する検討Motion：**J27 OPTIONAL**。Jillの「自分の楽しさを相手と共有したい」という性格を尊重し、顔と胸が演技の主体、翼・葉・太尾は必要なときだけ自然に参加する。これは新しいドラゴンの創作ではなく、既存本人のRig/Shape Key/Motionを成立させるための精密な形状・演技リファレンスである。

### 必須の正式参照画像5枚（すべての実画像を毎回添付）
- **Image A — Jill Canonical Identity** — `assets/grimo/source/jill/jill-Identity-canonical.png`。顔・目・頬・鼻・口・小牙・桃色系の角状付属物・体色・本人の可愛さ・クローバーその他の身体固有模様・身体に付いた葉や花・翼と太尾の外見の最上位Authority。
- **Image B — Tripo Body-only Front** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_front.png`。頭胸の正面比率、両眼と角、前肢・後肢・胸・腹・翼の左右位置と幅のGeometry基準。
- **Image C — Tripo Body-only Left Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_left.png`。画像内の顔はscreen-left向き。鼻先・頬・顎・頭部奥行き、首・胸・腹・短肢、翼根、太尾の側面Geometry基準。
- **Image D — Tripo Body-only Right / Opposite Side** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_right.png`。画像内の顔はscreen-right向きとして登録。反対側の頬・角・翼根・脚・尾の立体整合性の基準。
- **Image E — Tripo Body-only Back** — `assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_back.png`。後頭部/首背中の葉・左右翼の背面付け根・骨盤・太い尾根元・後肢のGeometry基準。
**優先:** AはIdentity・外観/色彩/可愛さ、B〜Eは立体形状・支持・サイズの基準。すべて画像実物を確認し、filenameのleft/rightを解剖学的左右にそのまま適用しない。Body-onlyで欠けるCanon­ical模様・身体装飾は削除と判断せず復元、独立した蝶などは追加しない。前に生成した参考画像を参照・上書きしない。

### Identity・解剖学の絶対保護
このキャラクターはCanonicalのJill本人。大きく丸い幼い顔、大きな緑系の艶やかな瞳、暖色チーク、短い鼻、クリーム色の頬・口元・腹、元の小牙を維持する。桃〜クリーム色の一対の頭部付属物は**horn-likeの硬い角状解剖**であり、柔らかな耳へ変形させない。春緑の頭・首・背中の葉はそれぞれ身体への根元と立体的な重なりを保つ。Canonicalで身体に固定された花や葉を勝手に除去せず、背景に浮く蝶・花・葉・星・地面植物を身体構造と混同しない。クローバーなどの身体固有模様をCanon­icalの所属部位・色・形で保護し、模様が見えない角度では反対側に複製しない。
胸は丸く立体的で、クリーム色の胸腹の段模様を保つ。前肢は左右独立した短い付け根・短い自由区間・丸い先端。脚を長くしたり、人間的な細腰/長い腕/長指を追加しない。下半身と短い脚/足底はB〜Eで確認できる支持を維持する。両翼は背中の左右別々の根元・緑系の外枠・薄クリーム色の実体ある膜と厚みを持つ。膜が葉や腕と全面融合したり裏から消えたりしない。太い尾は骨盤からつながり、背側葉状稜線と腹側クリーム帯を保ったまま緩く巻く。尾を紐状に細くせず、支持脚の代わりにしない。
**Generation Pose、Rig Rest Pose、Game Neutralは未確定の別概念。** ある一枚の画像をそのまま最終Neutralと決めない。動きのためにIdentityを変えず、どんな角度でも同一の立体身体として成立させる。

### 画像固有のカメラ・画角
顔と片側翼根・胸・足底が読める前3/4。

### 画像固有の表情・ポーズ・身体変形
通常の片翼を少し顔の横へ寄せ、頬のごく一部だけを隠して瞳でそっと覗く遊び。全顔は決して覆わない。もう片翼は収納、短肢・太尾は支持を維持。

### 重要検査点と追加の禁止
角・頭葉・翼根・膜の干渉なく成立する場合だけのSecret候補。翼の移植・巨大化、目の遮蔽、飛行、最終採用の断定禁止。
このテーマで動かさない部位はCanonical/Body-onlyの形状・体積・位置を可能な限り厳密に維持する。将来の動きのため、各部位を露出させる目的だけで根元を移植・拡大・伸長しない。

### 描画仕様
画像生成の対象は**JillのRig/Shape Key/Motion設計用、単体の高品質2D静止リファレンス1枚**。柔らかい高品質スタイライズド3Dイラストのような自然な厚み・陰影・清潔な素材。白〜淡い暖色の無地背景と最小限の自然な接地影。余計なキャラクター、文字、ラベル、矢印、線画注釈、モーション軌跡、複数コマ、分割図、透かし、背景蝶・浮遊葉・独立花は禁止。現実的な爬虫類の鋭い鱗や怖い恐竜、硬いプラスチックのような光沢、勝手な衣装・装飾追加は不要。ただし個別テーマで明示した中立的診断用Food/装備/Gift小物のみ例外とし、正式商品案とみなさない。
顔の見た目と可愛さ、目・口・首の変形余地、翼根・短前肢・尾の自然なつながり、支持の重さを両立する。可動部以外を補償変形させず、特に目・口・角・葉・胸・尾の良好な形を守る。

### 絶対禁止と判定境界
新しい個体、目の小型化や大きな位置ずれ、角の耳化、頭葉と首葉の削除、身体固有模様の勝手な変更、翼根の切断・潰れ、膜の紙化・破れ・消失、翼を開くたび顔を隠すこと、短い前肢と胸の融合、長脚化、不自然な縦線/切断線/縫い目/余分な部位、体型の過度な肥大や伸長、首の長い円柱化、尾根元の切断や支柱化は禁止。顔だけを美化して身体構造を破壊しない。外部VFX・音・演出文字で表情や行為の意味を代替しない。
今回成立させるのは**2D Referenceの視覚的検証候補**のみ。生成画像、画像のセルフチェック、Tripoへの入力、3D GeometryのHuman PASS、Rig/Shape Key/Motionの可動PASS、GLBスマホRuntime PASSはすべて別Gate。Human Reviewを勝手にPASSにしない。

### この画像の2D成功条件
Jill本人の可愛さとIdentityを守りながら、**OPTIONAL Wing-Shelter Peek**が自然な身体と意味のある一瞬として読める高品質画像を1枚出力する。顔・主変化・接点・支持・非干渉が視覚的に確認できること。
