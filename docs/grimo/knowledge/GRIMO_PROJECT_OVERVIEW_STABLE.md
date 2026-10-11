# Grimo — Stable Project Overview for ChatGPT / Codex

**Role:** ChatGPT Project Knowledge にアップロードする長期的な「全体像」の入口。リポジトリでも同一内容を管理する。
**Scope:** 製品の目的・正式な体験設計・構造的に安定した決定。実装進捗を記録しない。
**Basis:** Grimo の Product North Star、Character Experience、Production Architecture、Product Feature、Data Model（2026-10-12時点で確認した正式資料）。
**Maintenance:** 原則として普段のターンでは書き換えない。Humanが製品の根本方針を変更した場合のみ、原典と整合させて版を更新する。「不変」は日々の作業状態を混ぜないという意味であり、永久に上書き不可という意味ではない。

> この文書は**経緯の要約・状態台帳ではない**。現在の作業・コミット・Tripo残回数・未検証事項・次タスクは、専用ブランチ \`coord/grimo-ai-handoff\` の \`docs/production/GRIMO_AI_HANDOFF.md\` を**最新のremoteから**取得すること。アップロード済みのハンドオフの静的コピーを最新とはみなさない。

## 1. Product North Star：何のためのGrimoか

Grimoは、**タスク管理／カレンダー × 生きているように感じられる4匹の相棒 × 報酬・反応の収集**を組み合わせた、スマートフォン優先のPWAである。

ユーザーがタスクを登録・完了することで相棒と会う理由が増え、相棒に会いたいから日々アプリを開く、という自然な循環をつくる。単なるToDoアプリでも、放置育成ゲームでも、3Dモデルの技術展示でもない。

体験の優先順位：
1. かわいさ・魅力
2. 癒やし・安心
3. 愛着
4. 面白さ
5. 驚き
6. 収集

参考品質は『Let's Go! ピカチュウ／イーブイ』のパートナー体験。**素材や演技のコピーではなく、生命感・視線・触れた因果・自発性・余韻という品質基準を参照**する。

## 2. 4画面と中核ループ

メイン画面は **Task / Calendar / Grimo / Collection** の4つ。

- **Task:** タスク登録・完了が報酬の発生源となる。タスク分割の仕方をGrimo側から強制しない。
- **Calendar:** 予定の把握。予定を見たこと／時刻の到来だけで報酬を出さない。
- **Grimo:** 相棒の生きている様子を見て、触れ、Foodを与え、Wearを装備し、特別な遊びを楽しむ。相棒自身からの誘い・Giftもありうる。
- **Collection:** 「物」と「4匹ごとに発見した反応」を集め、カードとして眺め、並べ替え・絞り込みする。

UI/UXの主要参考は『Pokémon TCG Pocket』の情報密度・カード収集・軽快な操作・報酬演出。Grimoのキャラクターやアセットは独自に制作する。

## 3. 4匹の固有Identity

**最終的な見た目の権威は各キャラクターのCanonical Identity画像。** 生成姿勢・Body-only多視点・3D・UV・Material・Rig・補助数値は、その外見を置き換えない。

| Character | 見た目／中心的特徴 | Personality／演技の方向 |
| --- | --- | --- |
| **Carol（羊）** | 幼い羊、夢雲のような立体的な羊毛、耳、短肢と重い蹄、月・星のモチーフ | **attention-seeking + relaxed**。安心、やわらかい触れ合い、頬・頭を差し出す、静かな余韻 |
| **Jill（ドラゴン）** | 春緑の小さなドラゴン、葉、翼、太い根付きの尾、頭部の角状付属 | **attention-seeking + energetic**。喜びが胸から翼・葉・尾へ広がる |
| **Pino（カワウソ）** | 青白い丸顔・丸胴、内寄りの短腕、単一の厚い大きな尾 | **energetic + independent**。試す→結果を見る→楽しむ。軽快だが重さがある |
| **Shushu（パンダ）** | 白／桜色の大頭・小耳・丸い頬・短肢・ふっくらした胴、花冠・花束 | **relaxed + independent**。自分の快適な時間を保ち、穏やかに歓迎し、plushな荷重・圧縮を感じさせる |

4匹でエンジンや行為の意味を共有しても、演技・視線・間・強度・余韻を単に速度変更で使い回してはいけない。

Carolの羊毛は身体に所有される立体表現。広域の位置遅れで浮遊する別shellにしてはいけない。Jillの翼・葉・尾、Pinoの太尾、Shushuの耳・短腕・花の取付も身体構造／独立付属物として尊重する。

## 4. Living Companion体験：どう動くべきか

相棒は無入力時も、生きていると感じられる。しかし**常時大きく動くことは生命感ではない**。静止を選ぶ意図、まばたき、呼吸、視線、荷重、顔、耳・翼・尾・雲毛などが意味をもって関係する。

基本的な反応文法（すべての工程を毎回要求しない）：

\`\`\`text
入力・出来事
→ 実際に触れた部位の即時ACK
→ 注意・意図・ためらい
→ 必要な顔・視線・身体の主反応
→ 部位固有の付随動作
→ 静止・回復
→ 感情の余韻
→ 生きているIdleまたは次の行為
\`\`\`

守る能力：
- tap/poke、slow pet、continuous stroke、back-and-forthを区別し、触れた身体zone・左右・直前の履歴を尊重。
- 見る／見ない、まばたき、表情、低い提示、ハイタッチ、Food、Gift、Wear、Secret Motionなどが本人の意図に見える。
- 相棒から提示→**WAIT**→ユーザーの応答→共有する喜び。不参加なら安全に戻り、罪悪感を与えない。
- 新しい接触は古いアニメーションの順番待ちにせず、現在の姿勢から応答する。局所ACKと主行為と余韻は分離。
- 決まりきった繰り返し・全身一斉揺れ・root bounce・完成画像の全体伸縮だけで生命感を偽装しない。
- 表情やMotionは音・派手なVFXなしでも意味が分かること。

## 5. 報酬・収集の基本仕様

**報酬の入口：**
- その日最初のログイン → Food。
- タスクを1件登録 → FoodまたはWearの抽選。
- タスクを1件完了 → Food／Wear／Special／Secret Motionの抽選。
- 相棒とのふれあい → 非常に稀なGift（**通常抽選とは別枠**）。

通常のレア度は **☆70% Food／☆☆20% Wear／☆☆☆6% MVP予約枠／☆☆☆☆3% Special／☆☆☆☆☆1% Secret Motion**。☆☆☆が選ばれたMVPの抽選は有効な枠へ再抽選。Giftは☆☆☆☆☆☆相当で通常抽選に含まない。

**Food:** 消費アイテム。同一Foodは個数加算、発見済みカードは所持0でも残る。5つの食べ方（小一口／複数口／舐める／飲む／大物）と、キャラごとの好き度1～5から反応を構成。好き度1は食べず**消費なし**、2～5は食後評価を行い消費する。食品ごとに専用Motionを量産しない。

**Wear:** 永久所有。MVPでは各Grimoが同時装着できるのは**1個**。身体ごとに安全なnamed anchorへ取り付け、目・顔・重要モチーフを塞がない。

**Special:** 特定キャラ専用のFood／Wear／Secret Motion。Food型のみ消費する。

**Secret Motion:** 特別な遊び・行為を解放する永久コンテンツ。旧Toy分類は存在しない。発動はユーザーのみ／自発のみ／両方をコンテンツごとに設定。

**Gift:** 相棒側から提示する非常に稀な永久コンテンツ。通常報酬の自動支給ではなく、**相棒本人が渡そうとする体験**が価値。

永久アイテムの重複は、新しい同一所有物を増やすのではなく、発見済みFoodから選んで交換する。Collectionは物とキャラ別反応発見の双方を追う。

**禁止：** 内部・表示ともに親密度／好感度／Relationship XPを持たない。放置・未達・不在による罰、減少、病気・空腹の懲罰ループ、罪悪感を与える通知を作らない。一時的な気持ちの状態は表情制御として許されるが、親密度ではない。

## 6. 3D／Motion／Runtimeの成立条件

現在の承認済みアーキテクチャは **Full-Spatial 3D Living Character with View-Weighted Polish**。

- 正面／正面寄り3/4を高品質に仕上げつつ、側面・背面・頭の回転・低姿勢・触れ合いで立体構造が崩れないこと。
- 眼・瞼・口・頬・頭・短肢・耳・翼・尾・羊毛・装備など、体験上必要な部分を個別に制御できること。
- 必要なMotionで支持・接地・重量感・局所圧縮・接点・保持・遮蔽が成立すること。
- 単一Mesh、複数Mesh、bones、morphs／Shape Keys、shader、correctiveなどの実装方法は固定しない。見た目と必要な動きに合えばよい。
- スマートフォンPWAでの負荷・読み込み・タッチ応答・メモリ・バッテリー・4匹への拡張を考慮する。
- Blender／GLB・glTF／PlayCanvas等は運用上の主要技術候補。具体的バージョン・制作サービス・ポリゴン数・機材実測結果は可変情報として最新hand-off／Gitを参照。

**Humanの知覚判定が最終権威。** 自動テスト・幾何学的PASS・GLBエクスポート成功は、「可愛い・自然・生きている・実機で成立する」の承認に代わらない。

## 7. 仕様と作業状態の分離

**恒常的な内容：** このファイルと、リポジトリの正式なNorth Star／Experience／Production Architecture／Product Feature／Data Model。

**変動する内容：** ブランチ・HEAD・進捗・制作候補・検証結果・Human Gateの現状・Tripoの残回数／料金／画面・次タスク。これらをこのファイルへ書き足してはいけない。最新の \`coord/grimo-ai-handoff:docs/production/GRIMO_AI_HANDOFF.md\` と現行のGit／各制作State／実証資料を読む。

**権威と参照順:** 最新の明示Human決定 → Canonical Identity → 正式な製品・体験・3Dアーキテクチャ／商品仕様 → 現行制作Stateと実測 → 補助資料／過去記録。ハンドオフは探索用の索引であり、正式な決定やHuman承認を勝手に上書きしない。

**作業役割:** Humanが目標・見た目・完成品質を承認し、ChatGPTは情報整理・判断・タスク設計、Codexは実物を調べ制作方法を選択・検証する。工程・テスト回数・局所修正と再制作の選択は、成果物とリスクに応じて柔軟に決める。

## 8. 原典索引（repository-relative paths）

- \`docs/grimo/knowledge/GRIMO_PROJECT_KNOWLEDGE_INDEX.md\` — 正式資料の最新ルーター
- \`docs/grimo/knowledge/GRIMO_PRODUCT_NORTH_STAR_AND_MINIMUM_REQUIREMENTS.md\` — 目的・品質・禁止原則
- \`docs/grimo/knowledge/GRIMO_CHARACTER_EXPERIENCE_SPEC.md\` — 生命感・注意・触れ合い・体験Gate
- \`docs/grimo/knowledge/GRIMO_CHARACTER_PRODUCTION_ARCHITECTURE.md\` — Full-Spatial／View-Weighted／独立制御
- \`docs/grimo/knowledge/GRIMO_PRODUCTION_OPERATING_SYSTEM.md\` — Human／ChatGPT／Codexの役割と自律性
- \`docs/grimo/knowledge/product/GRIMO_PRODUCT_FEATURE_SPEC.md\` — 4画面・報酬・Food/Wear/Special/Secret/Gift/Collection
- \`docs/grimo/knowledge/product/GRIMO_DATA_MODEL_SPEC.md\` — 商品・反応発見・消費・所有の論理データ
- \`AGENTS.md\` — GitHub作業ルール／ハンドオフ運用
- **最新ハンドオフ：** [coord/grimo-ai-handoff の GRIMO_AI_HANDOFF.md](https://github.com/snowtone-ai/Grimo/blob/coord/grimo-ai-handoff/docs/production/GRIMO_AI_HANDOFF.md)

**ChatGPT Project Knowledge運用:** このMarkdownを固定の全体像として登録する。実行時には毎ターン上記のGitHubの最新ハンドオフを取得し、必要な原典のみ追加確認する。GitHubにアクセス不能なら最新把握を装わず、未同期と明示する。
