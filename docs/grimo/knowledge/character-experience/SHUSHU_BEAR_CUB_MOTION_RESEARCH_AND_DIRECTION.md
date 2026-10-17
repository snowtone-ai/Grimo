# Shushu — Bear-Cub Motion Research & Performance Bible v001

**Updated:** 2026-10-18 JST  
**Status:** EVIDENCE-SYNTHESIZED / PRODUCTION-DIRECTION CANDIDATE / HUMAN MOTION GATE PENDING  
**Purpose:** リアルな子熊・パンダ幼獣の身体力学と、魅力的なキャラクターアニメーションの演技原則を分離・統合し、Shushuの座位⇄四足立位、歩行、視線、待機、余韻、割込みを**実際に制作・検査できる**仕様として定める。  
**Not a claim:** 本書の秒数、フレーム、角度、動作順・カメラ構成のうち明記した演出値は、野生熊の計測結果ではない。外部の動画全尺をフレーム計測したとも、C1のスマホ／Human MotionがPASSしたとも主張しない。  
**Human決定:** ShushuにTripoのAnimation生成は不要。Codex / Blender / PlayCanvasで制作。高次のCanonical Identity・既承認v004外観、Main Goal/Character Experience Specを優先。

## 0. 一番大切な判定

> 子熊らしさとは「重そうな体を上下に揺する」ことではない。**次の接点を用意してから荷重を渡し、幼い好奇心に従って頭と目が先に注意を向け、体は慌てずついて行き、動いたあとに自分で落ち着く**ことが、Shushuらしい演技候補である。

目標：
- **G1 Cute/appealing:** v004の顔・大きな目・ピンクの輪郭・短肢・丸胴・花v002・承認された足裏の同一性を保つ。
- **G2 Living:** 「休む→気になる→どうしようか考える→支持を組み替える→行為→落ち着く」意図を15–30秒で読める。静止を許す。
- **G3 Body mechanics:** 接地・支持・足裏の摩擦・COM proxy・骨盤と胸郭の関係を論理的に成立させる。正面だけで「可愛く見せて」横から足を滑らせない。
- **G4 Technical:** 新たなRig/GLBの丸ごと再生成や無関係なMotion量産なしに、まず一つの正しい座位→四足立位を制作・検証する。

これは犬の四足歩行cycle、赤ちゃん人間の立ち上がり、二足立ちする着ぐるみ熊、熊の転倒動画の**どれでもない**。Shushuは**子パンダ風の幻想キャラクター**であり、バイオメカニクスの忠実さと可愛さの両方をHumanが判定する。

## 1. 調査計画の設計→攻撃→改善→実行

### 1.1 初期計画 v0

A. 動物園の「可愛いパンダ」動画を集める。B. 子熊の足運びと座位を調べる。C. 既存の可愛い熊キャラクターを参考にする。D. 動きに秒数を割り振り、Codex用資料にまとめる。

**これだけでは不合格。** 人気動画は編集、再生速度、転倒scene、レンズ、年齢などが混在し、「可愛い」から「実際の子熊が立つ機構」を推定できない。

### 1.2 Red-team — あえて破綻を探した14個の攻撃

| ID | 偏り・破綻シナリオ | 改善ルール |
| --- | --- | --- |
| RT01 | パンダ幼獣をクマ科全種と同一扱い | **同種パンダ幼獣を第1群**、他種の子熊は検証補助、成獣の力学は外挿に限定 |
| RT02 | 寝返り・転倒・二足「stand up」を座位→四足立位と混同 | **開始姿勢／終了姿勢／接地点**の組合せで映像を分類。異なる遷移を同一サンプルにしない |
| RT03 | 3か月の初歩行を成熟した安定歩行へ直輸入 | 月齢・成熟度・個体差を記録。Shushuは「意図ある幼さ」であり、常時歩行不能ではない |
| RT04 | 短いSNS切り抜きから平均秒数を捏造 | 元動画 fps・速度・無編集区間を確認できなければ **UNMEASURED**、時間は `[DIR]` 演出案 |
| RT05 | 人が誘導した直立姿勢を自然行動とする | 調教／ターゲット／餌／舞台演出の**文脈**を表示し、一般化しない |
| RT06 | グリズリー成獣の床反力をパンダ幼獣の数値へ転送 | 接地・荷重という定性的原理のみ。質量・力・時間・歩幅は転用禁止 |
| RT07 | 子犬の爪先歩行／人間の二足立ちモデルを導入 | クマ科の前肢掌面・後肢足底と短肢の位置関係に沿ってポーズ確認 |
| RT08 | 正面から可愛いのに側面で腹・脚が融合 | Front/Side/左右3Qの同時合格、接点/厚み/花の追従を優先 |
| RT09 | 目線だけ無作為に動かせば生命感が出ると考える | **何が気になったか**を先に決め、eyes→head→必要なbody。理由なく常に動かさない |
| RT10 | リズムをすべて等間隔・左右対称にする | 支持の必要性と意図からタイミングを変える。偶然のnoiseは使わない |
| RT11 | ディズニー/ゲームの誇張を実生物の証拠とする | **OBS（動物）/SCI（力学）/CRAFT（演技技法）/DIR（Shushu演出）**を厳格に分ける |
| RT12 | v004の既存診断Actionや旧Arm FKを正式Motionとして再利用 | 診断clipは動作検証のみ。現行v004の `Seat` + `Wrist` + `Hold/SelfContact/Offer` のownershipを守る |
| RT13 | 生物らしさのためCanonicalの顔・花・足を犠牲 | Human外観FAILなら技術PASSでも採用しない。モデル改造の前に可動・演出方法を再検討 |
| RT14 | フレーム刻みの細かさを品質と取り違える | 数値は制作開始値、録画比較・Humanレビューで反証可能に。不要な全84/252 profile量産は禁止 |

### 1.3 改善後計画 v1 と実施した範囲

1. **Authority Lock**：mainの`Goal√map.md`、`GRIMO_CHARACTER_EXPERIENCE_SPEC.md`、`GRIMO_CHARACTER_PRODUCTION_ARCHITECTURE.md`、Shushu v004 donor `final-v004/REVIEW.md`、C1 evidenceを確認。
2. **動物群 A・PANDA**：SmithsonianのXiao Qi Ji/Bei Beiを中心に、幼獣の発達・四肢を下に入れる・滑る床・足の選択・座位中の行動を収集。**元動画のフレーム単位計測は未実施**。
3. **動物群 B・OTHER CUBS**：North American Bear Centerのツキノワグマではなく**アメリカクロクマ幼獣**を確認。発達速度はパンダと異なるので「未熟な四肢と遊び」を補助比較に限定。
4. **力学群 C**：グリズリー成獣の査読済み床反力・歩容・足底の知見を収集。幼獣の速度・膝角などの絶対値に転用しない。
5. **創作群 D**：Disney Animation、Framestore（Paddington 2）、Animation Mentorを使用。姿勢・目・間・体重感を**制作原則**として採用。Disney `Brother Bear` のKoda、DreamWorks `Kung Fu Panda` Po、Netflix `Rilakkuma and Kaoru` は媒体・原画風参考の境界だけ明記。直接映像のコマ検証や具体尺の確認はしていない。
6. **統合**：ポーズごとに `支持/COG/前後肢/顔/視線/花/時間/割込/QA` を揃えて、座位⇄四足、歩行、待機、触覚を設計。可動域・接触・スマホ性能は実装前にUNKNOWNとする。
7. **後続研究必須**：正規速度の合法な原映像を再生できる環境で、最低5例（座位→四足2、歩行開始/停止2、座り直し1）を2人/2個体以上から選び、4接点・骨盤・頭のtimecodeを注釈後、演出値を調整する。これは**未実行**であり本書の弱点として残す。

## 2. Evidence claim ledger — 何が実際に裏付けられるか

タグ：**[OBS]** 飼育担当者による実動物の記述／動画公開の事実、**[SCI]** 査読論文の実測、**[CRAFT]** 制作者の発言/職業教育、**[DIR]** Shushu向け創作仮説、**[UNKNOWN]** 未計測/未承認。

| ID | 資料・観察できる事実 | 何を採用するか / 外挿の限界 |
| --- | --- | --- |
| A01 | [OBS] Smithsonian `Xiao Qi Ji Takes His First Steps`: 生後3か月5日、**四足を胴の下へ**揃えて数歩、その後転倒。<https://nationalzoo.si.edu/animals/news/pandastory-xiao-qi-ji-takes-his-first-steps> | 四肢配置が歩き始めの前提。毎回転倒・未熟児化はしない |
| A02 | [OBS] Smithsonian `Xiao Qi Ji Is On The Move`: 3.5か月でcrawl/walkの混在、後肢を胴下へ、床のtractionを獲得中。<https://nationalzoo.si.edu/animals/news/pandastory-xiao-qi-ji-move> | 後肢が瞬時に直立する表現は疑わしい。床条件で前肢補助を変える |
| A03 | [OBS] `Bei Bei Takes His First Steps`: 平滑床と岩場でtraction差、四肢を身体下に入れる。<https://nationalzoo.si.edu/animals/news/bei-bei-takes-his-first-steps> | 足裏の水平slideは故障扱いか制御した滑り演技。デフォルトはグリップ |
| A04 | [OBS] `Top 8 Giant Panda Moments in January 2021`: 歩行成熟後に注意深く岩を登り、同腹個体とも転び方が違う。<https://nationalzoo.si.edu/animals/news/top-8-giant-panda-moments-january-2021> | 「そろそろ足を置く」慎重さをShushu固有の気質へ翻訳。熊全部の共通法則にしない |
| A05 | [OBS] `A Playful Panda Cub`：座って落ち着く、探索中は止まって玩具を前肢や口で調べる。<https://nationalzoo.si.edu/animals/news/pandastory-playful-panda-cub> | 座り姿勢・止まって考える時間を肯定。アイテムがない時に架空物へ手を伸ばさない |
| A06 | [OBS] 10か月のXiao Qi Jiの`stand up`は飼育員が指を上げ誘導する**後肢二足立ち**。<https://nationalzoo.si.edu/animals/news/pandastory-quick-learner> | 座位→通常の**四足立位**の参考とはしない |
| B01 | [OBS] North American Bear Center `The Cubs Develop`: クロクマ幼獣は生後初期crawlからwalkへ発達、映像も公開。<https://bear.org/bear-facts/the-cubs-develop/> | 「幼さ・重心の迷い」の補助。パンダと同じ週齢に換算しない |
| B02 | [OBS] `The Family Emerges`: 雪のような基質で歩行が難しくなる／木登りと遊び。<https://bear.org/bear-facts/the-family-emerges/> | 接地点・摩擦環境をMotion文脈に組み込む。通常Grimo床は固定/乾燥 |
| C01 | [SCI] Shine et al. (2015), adult female grizzlies n=4, JEB 218:3102–3109, <https://doi.org/10.1242/jeb.121806>: slow walking / running walk / canter, lateral force、hindquarter long-axis rotation。 | Bearの歩行を単純な犬のtrotとして流用しない。**成獣・異種**でありShushuの角度/秒数を算出しない |
| C02 | [SCI] JEB 220:1322 `forelimb joint mechanics`: 成獣グリズリーの肩・肘・手首に荷重吸収と支持の機能。<https://journals.biologists.com/jeb/article/220/7/1322/19549/Grizzly-bear-Ursus-arctos-horribilis-locomotion> | 前肢が接地する過程を可視化。ただし幼獣の関節角度を直接取得できない |
| D01 | [CRAFT] Disney Animation公式 process: 演技の価値はtiming、staging、anticipation、follow-through、anatomy、weight、appeal。<https://www.disneyanimation.com/process/animation/> | 単に骨を補間しない。意味と力の流れを演じる |
| D02 | [CRAFT] Framestore `Paddington 2`: 監督・Animation担当は**小さな行為と思考・視線・目蓋、過剰な表情を避ける**ことを重視。<https://www.framestore.com/work/paddington-2> および <https://www.framestore.com/news/paddington-2-how-find-characters-performance> | Shushuの微表情・静止の選択に適用。Paddingtonの二足構造と歩幅は流用禁止 |
| D03 | [CRAFT] Animation Mentor `Tutorial: How to Animate a Quadruped Walk Cycle`: reference anatomy→contact/passing→重心・支持肢・foot roll→グラフ整形。題材は犬。<https://www.animationmentor.com/blog/tutorial-how-to-animate-a-quadruped-walk-cycle/> | **工程のみ**採用。犬の膝・足の形や体尺はクマへ転用しない |
| D04 | [CRAFT] Animation Mentor `12 Principles` と`Anticipation`: 主動作前の情報提示、各部の位相差、円弧、魅力。<https://www.animationmentor.com/blog/tutorial-12-principles-of-animation/>; <https://www.animationmentor.com/blog/anticipation-the-12-basic-principles-of-animation/> | 目→前肢支持準備→骨盤→頭/花余韻の可読性。具体フレームはDIR |
| D05 | [CRAFT] Disney `Brother Bear` (Koda) <https://www.disneyanimation.com/films/brother-bear/>、DreamWorks `Kung Fu Panda` (Po) <https://www.dreamworks.com/movies/kung-fu-panda>、Netflix/dwarf `Rilakkuma and Kaoru` <https://about.netflix.com/en/news/rilakkuma-and-kaoru-will-premiere-globally-as-netflix-original-series-in-spring-2019> | **スタイル比較候補**。公式ページは出演/制作形態の証拠で、ここから動作fps/秒数/具体ポーズを捏造しない。Koda=情感の可読性、Po=大質量の演技、Rilakkuma=穏やかな間という**分析仮説** |
| E01 | [LOCAL] Shushu v004 donor body Human外観PASS、足裏PASS、花v002後続Human GO。<../../../../docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v004/REVIEW.md>（**mainには候補資料未統合**、実参照は制作branch参照） | Canonical/Human Gateが最優先。形状・眼・短肢・装備を勝手に変形しない |
| E02 | [LOCAL] App C1 branch `codex/grimo-shushu-runtime-c1-v001` local technical display GO, Human app-stage / phone / Vercel delivery HOLD; `SHUSHU_APP_RUNTIME_C1_V001.md` | MotionはC1上で制作。外観や実機の未承認をtechnical testで埋めない |

### 2.1 入手済み証拠の限界

- [OBS] は動物園の一次文章を実際に確認したが、YouTube・ライブカメラ・映画本編を本調査でフレーム単位に連続再生・校正した**直接時系列測定ではない**。A01–05から「0.42秒で後肢を引く」といった主張は不可能。
- [SCI] C01は成獣・4頭、C02も成獣であり個体差/成長/造形による変化を許す。「すべての熊はこの足順」といった絶対化禁止。
- [CRAFT] 作品製作者が述べた演技原則は、生体測定の代わりにはならない。Koda/Po/Rilakkumaは**公式作品の存在と創作候補**としてのみ記録。
- [LOCAL] donor sourceとcanonical imageそのものは正本。本文にない独立眼球/morph名、膝角、接触可能な脚を**実装できると仮定しない**。
- 外部著作権素材の画像/動画/音源をGit repoへ無断収録しない。参照URL・派生した自作ポーズ資料だけを保存。

## 3. Character brief — Shushuの熊らしさをどこで表現するか

**対象:** Canonicalは白・桜ピンクのパンダ風、丸い幼児顔、大きな潤んだ瞳、ふっくら胴、短く丸い手脚、幅広い肉球、耳、頭の独立桜装飾（v002）。**正規キャラ画像は演出付き座位の絵**であり、その輪郭を維持したまま日常使用の四足/座位の両方を実装する。Canonに描かれる花束・周囲の花・蝶等の**背景演出は身体部位や標準手持ち物とは限らない**。標準Head花と花束を混同しない。正面からの可愛さとSide支持姿勢を両立させる。

**性格の翻訳 [DIR]:**
1. **自分の落ち着ける姿勢を選ぶ**。反射的に跳び上がるより、立ちたい理由が顔の注意から分かる。
2. **ゆっくりだが鈍重/病的ではない**。支持を整えればしなやかに歩ける。毎回何かにつまずかせない。
3. **独立心がある**。誘いが来ても即「はい！」と全身で反応しないことがあるが、入力無視ではなく目・頬・小耳で局所的に受け止める。
4. **重量は下胴と骨盤にある**。顔だけ浮遊しない。大きな頭の首・頬が胴体へ自然に乗る。
5. **接地は技術ではなく演技**。前肢をどこへ置くか考える、ゆっくり荷重を受ける、後肢を胴下へ引く過程が愛嬌につながる。
6. **止まったあとが可愛い**。立ち上がってすぐ全身ポーズを揃えず、頭・耳・瞼・花が意図的に落ち着く。

**避ける比較誤用**: 人間の赤ちゃんが手を使わず二足立ちする姿、犬のdigitigrade trot、Poの格闘アクション、Paddingtonの二足散歩、乳児パンダの転倒頻度。Shushuは穏やかな表情を保てる**歩行可能な幻想幼獣**である。

## 4. Body mechanics contract — 画像だけで通過させない

### 4.1 体と支持点の記録

毎フレームの最低限の状態:
- `supportContact`: `hindL, hindR, foreL, foreR, rump, optional heldObject` のうち**実際に床/物へ荷重を伝達している点**。絵からの推測ではなく、対応する足裏/臀点を可視化。
- `contactLock`: planted feetのworld位置/向き。下半身のリフトで足がワールド座標を滑るのは禁止。
- `COM_proxy`: torso/pelvis質量の簡易proxy。実際のmass simulationがない場合、**未測定の近似**と明記。支持多角形外に出る場合は次の接点を先に形成するか動作を止める。
- `pelvis/torso/head`: 一塊のrigid transformにしない。首/頬を過伸張せず、眼窩の見えと顎下面を守る。
- `pawLeft/Right`: 実接地支持と`Hold/SelfContact/Offer`などの目的を競合させない。荷重中の前肢は接点を解放するまで物を差し出さない。
- `flower`: Head local attachmentを維持する。不要な独立花回転・顔遮蔽・頭部貫通は禁止。
- `sightTarget`: camera/user/現存するprop/自分の手元。現存しない虫や音を「見た」ことにしない。

Shushuの足形はCanonical優先であり、「熊だからリアルな爪と掌骨が必要」という理由で追加しない。後足のピンク肉球が空中に見える瞬間は意図したswing時だけ。臀support→前足→後足の切替をsoft bodyの潰れだけで偽装しない。

### 4.2 姿勢ラベルは区別

| ポーズ | 荷重と身体の必須説明 |
| --- | --- |
| `SIT_RUMP` | 臀/後腿部が実支持。前肢は腹前に休める、時に小さい補助。**四足立位の単純な膝曲げではない** |
| `SIT_PREPARE` | 視線・顎・前肢配置が変化し、身体を起こす意思が伝わるが臀支持は残る |
| `FORE_SUPPORT` | 少なくとも可動・接地可能な前肢が前方で荷重を受ける。身体の下に空間ができ始める |
| `RUMP_UNLOADED` | 臀supportがゼロに移る。後肢の裏面が床へ足場を作り、胸は前肢だけで宙吊りにならない |
| `FOUR_STAND` | 4肢で安定。頭の重心と胴体、足底接地点が一致。接地高さ/左右幅が破綻しない |
| `FOUR_WAIT` | 立位の待機。前肢を使う/手を見せる前に支持を再配分 |
| `HIND_UPRIGHT` | **後肢二足立ち**。獣医のstand trainingの対象。通常の座位→四足遷移とは別で、初回MVPに要求しない |
| `LEANING/SIDE_REST` | 寝そべり/横座り。座位の短縮版として解決しない。新サポート接点が必要 |

**Rig現状**: C1 Loaderの現行`Seat`、`Wrist.L/R`、`Hold.L/R`・`SelfContact.L/R`・`Offer.L/R`は変形/アンカー契約。旧Arm FKで新動作を動かしてはいけない。これらが実支持へ直結しているとは限らない。接点は追加で検査。

## 5. HERO study A — Rump sitting → natural four-paw stand

### 5.1 演技の意図

**S02→S25またはS01**：「なにかが気になる。でも急がない。まず足場を確かめて、少しだけ身体を前へ。よし、立てた。何を見るつもりだったっけ」。Shushuが「できない子」に見える長い失敗・毎回転倒は採用しない。

**正しい動作の不可欠な因果 [DIR]**：注視→前方に荷重先を確保→臀から荷重を外す→後足を胴下へ→骨盤/胸の支持を連続的に移す→四足立位→頭/耳/花が落ち着く。局所の先行/重なりはあるが**骨盤上昇だけが突然始まる**のは不正。

### 5.2 製品用Timing Profile — **演出仮説、動物実測値ではない**

単位s、24fpsの目安（24fpsはkey設計用。PlayCanvasは可変dt）。時間は動作状況とHuman評価で変更可能。各rangeには重なりがあり、実際の姿勢連続性を優先。

| Beat | 仮時刻 / frame | 身体支持・キーポーズ | 視線・顔・耳・花 |
| --- | --- | --- | --- |
| 0 Intent | 0.00–0.24 / f0–6 | `SIT_RUMP`で支持固定。立つ目的を選ぶ | 目が先に移る。瞼や口角を大きく動かさず、見たい方向が分かる |
| 1 Anticipation | 0.20–0.52 / f5–12 | 胸の前傾はごく小さく。近い前肢を伸ばせる位置へ（root跳ねなし） | 目線→頭がわずかに追う。耳と花は少し遅れる |
| 2 Place forepaw | 0.45–0.94 / f11–23 | 片前肢の接触→他前肢を含め`FORE_SUPPORT`へ。手先が床を貫通せず接地 | 眼は短く手元を見る。**頭を床に落とさない** |
| 3 Rump unload | 0.83–1.40 / f20–34 | 前肢+臀→前肢+後足へ荷重移行。股/膝はまだ折れ、腹が足を食わない | 少し力を込めるが grimace/顔の変形は禁止。花の重さは二次 |
| 4 Gather hindfeet | 1.16–1.72 / f28–41 | 後足を胴下へ小さく引き、必要なら片側ずつ足底を新しい位置へ。**planted反対側を固定** | 視線が目標へ戻る。頭の先行が胴を吊らない |
| 5 Extend and find balance | 1.58–2.12 / f38–51 | pelvis/chestを支持内で伸ばし`FOUR_STAND`へ。短肢は短いまま、足/臀/腹の余剰圧縮をほどく | 胴に小さな追従。顔が早く上を向きすぎない |
| 6 Settle | 2.05–2.55 / f49–61 | 4接点安定、残余の荷重移動と小さな前足の位置修正のみ | 耳→花の遅れ。目は目的へ、笑顔を無条件に最大化しない |
| 7 Afterglow / next action | 2.45–3.10 / f59–74 | `FOUR_WAIT`。必要に応じ次の1歩へ。立ち上がりを永遠に繰返さない | 「立った後どうするか」の注意が残る。静かな停止OK |

**基準案 [DIR]:** 主な着地→立位完成 約**2.1–2.6s**、視線の予備と余韻を含む全演技 約**2.5–3.1s**。**実際のパンダの平均秒数ではない**。最初のMotion Blockoutで遅い/重い/可愛さ低下ならHuman比較により縮める。

**短縮パターン [DIR]**: 既に前肢が床にあり、足が近い位置にある場合、意図0.1–0.2s→荷重移行0.5–0.8s→立位整定0.4–0.6s＝**概ね1.0–1.6s**。臀が安定した完全座位ではこの短縮パターンを適用しない。

**長め・うとうと変種 [DIR]**: 直前に休息していたとき、eyesを開く/周囲を見るのを0.3–0.8s延ばしても、脚を引きずる・常時苦しそうな荷重を演じない。**全体2.9–4.0s仮説**。繰り返しを避けるために使い、毎回遅いと入力レスポンスを損なう。

### 5.3 途中の破綻を防ぐ指示

1. **臀が床から離れる直前**が最重要：head側へ前のめりになったのに前肢接地がない＝転倒予告。接点がない状態でrootを上方へtranslate禁止。
2. 一方の前肢を伸ばすとき、残る臀/後足/前肢の支持を見せる。片手動作が`Offer`や`Hold`と競合したら保持を安全に諦める／別Animationにする。
3. **真横から見て**胴の最下面と前後肢が離れて見える時間帯を評価。「お腹と脚が一体の塊」のまま急に脚だけ現れるのはFAIL。
4. 後肢の床接点は「足が先に伸びきって足底が滑る」ではなく、接地してから体重を受ける。支持足がスリップしていないかworld markerを描く。
5. 伸長後、脊柱を一本の棒として真っすぐに伸ばしすぎない。頭/頬/顎下の可愛さとplush重量を残す。
6. 花v002はHeadに確実に追従し、二次遅延が必要なら**装飾専用の独立許可範囲内でのみ**制作。花の抜け・頭部の破裂を必ず検査。
7. 途中任意の50–100msで一時停止しても**成立する支持**が必要。前肢が浮いたまま肩だけ前進はFAIL。
8. 主動作の途中タップは消滅しない。危険な荷重移行区間では小さな目/顔ACKのみ返し、接触移動は安定後へ**短く保留/合流**。反応無視や暴力的な中断を禁止。

### 5.4 さらに映像を比べるべき競合演出

- **Version A / Bear naturalistic**：前肢を着ける→臀を浮かせる→後足配置→小さく立つ。前肢の可視接点を主役。
- **Version B / Shushu reserved**：先に視線を向け、一瞬迷う→同じ接地支持を保ちつつゆっくり立つ→少し耳だけ余韻。**根拠なく全体をスローモーション化しない**。
- **Version C / Very short**：前肢既接地時だけ、ごく少ないpose変更で立つ。通常座位からの直立と混同しない。
- Humanは**A vs B**を同一照明・カメラ・元GLB・HeadFlower onで比較し、どちらが可愛い/「子熊らしい」か判断する。Cは別前提条件の補助。

## 6. HERO study B — Four-paw stand → chosen comfortable rump sit

起点`FOUR_WAIT`→最終`SIT_RUMP`。**立位poseの逆再生を自動採用しない**。降りるときは重力と床に向かう接点変化が異なる。

| Beat | 仮時刻 [DIR] | 主動作 | 気持ち・顔 |
| --- | --- | --- | --- |
| Want rest | 0–0.30s | 足元や自分の前肢を見る、立位support維持 | 「ここが落ち着きそう」 |
| Back feet settle | 0.25–0.72s | 後足の位置と支持幅を調整 | 眼/頭は落ちる方向を確かめる |
| Rump lower | 0.60–1.30s | 骨盤が後下へ曲線を描き、後肢股/膝屈曲、胸は倒れない | 重みとsoft compressionを確認 |
| Rump contact | 1.15–1.52s | rump/腿の支持が発生した後に前肢荷重を順に外す | 顔に微小な安心の変化 |
| Paw withdraw | 1.45–1.94s | 前肢が腹前/床横など落ち着く位置へ。膝や肉球を隠しすぎない | 視線を手元に一瞬寄せてもよい |
| Rest and afterglow | 1.88–2.60s | 胴が遅れて落ち着き静止を許す | 1つ小さい瞬き/耳settle。過度なため息禁止 |

**可愛い失敗ではなく自然な重み**: どすんとお尻を落とすワンパターン、浮いたまま床に吸着、腹が足を溶かす、両前肢が荷重中に同時消失、花がheadを貫く、標準花を抱える等はFAIL。

## 7. HERO study C — Start walking, bear-like slow quadruped steps, stop, turn

### 7.1 Bear gait vs dog gait

[SCI C01] 歩く熊はplantigrade/palmigradeのfoot contactと特有の前肢・後肢の横力/回旋が見られる。成獣グリズリーの研究ではslow walkのfootfallは典型的な**lateral sequence**（後肢の接地と同側前肢の順序）であり、**dog trot cycleを前提にしない**。歩容は速度と個体で変わる。Shushuの歩幅・歩容・歩数は本研究で直接測っていない。

### 7.2 操作可能なwalk設計 [DIR]

初期の正式採用候補は**ゆっくり2〜4歩の短距離探索**。可愛さとFront Heroの顔可読性を優先し、カメラへ大きく近づきすぎず小さな横/奥行きへの移動も設計。アプリのfront-fixed camera下では実移動が無いwalking-in-placeを主役にしない。

**一歩に必要な状態:** (1)次の位置を目/頭で選ぶ、(2)支持脚/体重側を決める、(3)遊脚の足裏を剥がし短い弧で運ぶ、(4)着地点へ踵/足裏の幾何が矛盾しないよう接地、(5)荷重を移し反対脚へ、(6)胴/肩の遅れを回収する。**足を置く前に身体を空中移動させない**。

| Prototype parameter | 開始値 [DIR] | 注意 |
| --- | --- | --- |
| Slow gait周期 | 同じ脚の次の接地まで **1.25–1.75s**を試作レンジにする | 成獣の生体測定値でない。脚が短く見えても速度は評価次第 |
| Swing比率 | 1歩の周期中**約22–38%**を探索レンジ | 実stance比を測定せず固定しない。接地マーカーで検証 |
| 踏み出し長 | v004身長`H`比で**0.08–0.18H**の候補から開始 | 機能確認用。歩幅を増やすため脚を伸ばさない |
| 足の上がり | `H`比**0.015–0.045H**の候補、最小clearance優先 | 厳密な生体値ではなくフレーム判読/地面衝突の試験値 |
| 骨盤左右回旋 | 動きが伝わる最小値で比較、固定角度なし | hip wiggleを繰り返して魅せない |
| Head・eye | 接地点/目標を時々見るが全歩数で視線Downしない | 瞳の可愛さ優先、顔を隠さない |
| 肩・耳・花 | 体幹の支持移動に対するごく小さい遅れ | 揺れは必要な時だけ、花は独立anchor |
| Stop | 次足を接地→反対脚に荷重を渡し→頭/耳が静かにsettle **0.25–0.65s** | 滑走停止、ループ停止フレームのsnap禁止 |

**Footfall candidate (順序だけの出発例):** `LH → LF → RH → RF`の順を研究C01のlateral sequenceを参考に検討。これは**Shushuで検証する候補**であり、実際の遅延・位相・地面速度は動画計測とRigで調整する。斜め対角ペアを同時に蹴り出す犬のtrotを不用意に適用しない。

### 7.3 始歩・歩行中・終歩は同じcycleの切断ではない

**START (0.4–1.0s仮):** 目標を見る→一方の支持が少し変わる→最初の前/後肢swing→足を置く。歩き出しでroot速度が突然最大にならない。

**CRUISE (実距離依存):** 2〜4歩。重さのある胴、短い足、静かな注意変化。前肢と後肢がそれぞれの接点を保持。近いviewでも物理的な幅と厚みが保てる。

**STOP (0.3–0.7s仮):** 最後のswing足を床に置く→胴の前進を自然にゼロへ→小耳・瞼→選んだ対象を見る。ループ中任意フレームで完全停止して足が滑らないよう、stop transitionはfoot contact phase-awareにする。

**TURN**: 先に眼→頭→前足or後足の再接地で支持polygonを変え→胴が連続旋回。身体全体を垂直軸で回すturntableは不採用。固定hero cameraなので必要時の小旋回のみ実装し、主役の正面顔を失わない。

## 8. Living Idle・顔・視線・耳・装飾 — 可愛さの時間設計

### 8.1 S01 30-second readable idle storyboard [DIR, not animal data]

| Time | 選択と行為 | 何もしていない部位 |
| --- | --- | --- |
| 0–3s | 既存の安定座位/四足立位を保持。まぶたの小反応、顔の活きた視線 | 前足・脚・花に無意味な同時振動なし |
| 3–6s | 何か気になる方向へeyesを先行し、頭がごく少し追う | 骨盤/支持は固定 |
| 6–10s | 観察する**hold**。選んだ対象を見ていると読める | 常時瞬き・きょろきょろは禁止 |
| 10–13s | 注意を戻す。ゆるい瞬き／極小の耳settleが入ることがある | 大きな全身動作なし |
| 13–20s | 休む。呼吸は強調しない。顔/腹の印象を守る | 丸胴の全体scale/bob禁止 |
| 20–25s | 必要性がある時だけ手元や腹前へ小さな注意。支持位置を壊さない | 中断された腕が勝手に持ち上がらない |
| 25–30s | 短い余韻→次の自然な選択。本人が落ち着く | 30秒目で頭/胸/耳を一斉Neutralへresetしない |

**これは唯一の固定30s loopではない。** 使うのは状態と小行為の素材。短時間サンプルはHumanレビュー基準であり、繰り返し視聴では出来事の発生間隔・型・強さ・同じ表情の連投を文脈で調整する。

### 8.2 顔・注意の可読性

- 目: 優しい視線、大きなハイライトを守り、pupilが急にsocketから飛び出さない。先行は自然に見える小さい量だけ。目線の無意味な左右往復は禁止。
- 瞼: blinkは上下瞼・頬・見える白目/虹彩の形の関係を壊さず行う。単なるTexture fadeや黒目消失は不可。**瞬き頻度の絶対値は資料から未測定**。
- 頭: 目が向いた後に小さな遅れで必要な距離だけ追う。頬/鼻下/顎下が硬い板のように動かないこと。
- 口: 常時開口の「笑顔」禁止。閉じた状態を基本とし、小さな口角だけで感情が読めるかを優先。
- 耳: 両耳の同時完璧シンクロを避ける一方、完全ランダムでもない。耳根の局所反応。頭花が耳を貫かない。
- 花v002: canonical-attached equipment。おもちゃやgiftではない。先に身体Motion、後で必要なfollow-throughを付ける。独立揺れが未検証なら**正しいHead追従だけ**の方がよい。
- 呼吸: 丸胴の厚みをほんの少し体幹で示す。腕・足・眼・頭を一括スケールしない。座位supportが動くほどの膨張は不要。

### 8.3 意図→局所ACK→反応→余韻

同じ笑顔でも、直前の身体状況で意味が変わる:
- 安心中: 目だけ返事→呼吸が続く→相手の方を少し向く→選んだ姿勢を保つ。
- 歩行開始: 目で選択→足場→胴→目的地へ進む→最後の一歩と顔が遅れて落ち着く。
- 座位のままtouch: touchされた左右頬が先に分かる小反応→顔が開く→前足が休まる→落ち着きが残る。
- 動作中touch: 現在のSupportを壊さない小さなACK、必要なら安全な足を置いてから大きい反応。
- 勝手に機嫌が悪くなる・放置罰・隠れた好感度の上げ下げは禁止。

## 9. Touch / interruption — First user-facing motion

**最初は頭・頬のセマンティックな左右2 zoneだけ**。3D hit testが信頼でき、scroll/DOM/touch captureを分離できた場合に限る。

| Phase | 開始値 [DIR] | Shushuの読みやすい因果 |
| --- | --- | --- |
| Touch local ACK | touch後目標**0–100ms** visual | 触れた側の局所に小さい反応。UI応答とキャラ反応の計測は別 |
| Attention | ACK後約0.08–0.23s | 目→頭→相手を見る。現行poseは保持 |
| Commit | 約0.20–0.65s | 頭/頬を気持ちよい側に少し預け、必要なら胸のみ小さく参加 |
| Hold | 入力中変動 | 触り方に応じたhold、機械的に最初の動作を何度もrestartしない |
| Release | 接触終了後約0.20–0.55s | 接点を現在値から解き、表情は急に消えない |
| Afterglow | さらに0.35–1.1s | 余韻から自己の待機へ戻る／続ける。無理に全身Neutralを通らない |

右頬→左頬: 最初の右接触を解除し、**現在の姿勢と支持のまま**左局所ACKへ移動。頭を中央まで巻き戻してから左へ回すテンプレートは不可。支持系が別の動作中なら重複タッチを弱い顔応答に抑えるのは可。最初のHead・Gaze・Blink・Earのownershipを明文化する。

## 10. Practical Rig/Animation integration map — **実物確認が必要**

| Channel / concern | 既知/未知 | 制作／禁止事項 |
| --- | --- | --- |
| Body+Torso | v004 8-influenceとcorrectivesあり [KNOWN] | loaderを保持し、supportを変えるposeをBlender/PCで比較。whole-root bobで擬似呼吸禁止 |
| `Seat` | v004 controller入力 [KNOWN] | 0/1が与える局所correctiveと連続支持は要実測。単純0→1補間で自然座位ができるとは**未確認** |
| `Hold.L/R, SelfContact.L/R, Offer.L/R` | Paw purpose priority [KNOWN] | 支持中のPawにOfferを重ねない。途中の目的切替を実poseに対応させる |
| `Wrist.L/R` | 独立入力 [KNOWN] | 先端向きが支持床と噛み合うか試験。手首だけ曲げて足がfloating禁止 |
| `mixamorig:Head` | 頭花が取り付くnode [KNOWN] | head回転の軸/可動域/頬への影響を比較。大角度を即許可しない |
| Eye, lid, mouth, ears | 存在する形状/表情検査あり、**製品用individual channel names not enumerated here** | GLBとBlenderで実名を列挙・可動試験。無い操作を創作して「実装済み」と言わない |
| Hind foot / rump support | v004座位/脚はHuman比較を通過 [KNOWN]、実IK/pin contract [UNKNOWN] | 立ち/座りに必要な足底world pinを発見・追加。短肢延長や形状変更はしない |
| Flower v002 / pads | 標準装備の独立資産 [KNOWN] | 追従とmaterialを守り、見え方を認められる範囲で動かす。花束と別 |
| Demo 821-frame Action | **diagnostic only** | 直接Living idle loop化、古いArm FK採用、clip全量配信はしない |
| App lifecycle | C1は初期静止・on-demand rendering [KNOWN] | C2が必要なRAFを追加しても非表示時pause、route exitでlistener/GL解放、Task/Calendar 3D-requestゼロ維持 |

**推奨段階:** `preflight control inventory → 1 pose stress → v004 compatible rig/clip layer → contact-based Sit→Four Stand → real PlayCanvas composite → Human Gate`。各段階で前に戻れるbranchを保つ。

## 11. Keyframe・Animation実装契約 — 上流DCCとPCの橋

1. **技術表現は自由**：Blender Action / NLA / GLB動作単体 / PlayCanvas Anim graph+layer / 小さな局所proceduralの複合。変形が実際に見えることが条件。24fps key設計は可、実時間dtで数値安定させる。
2. **既存Rigを維持**：v004のbone rest、mesh indices、morph target id、GPU 8-weight、Paw custom normalを変更せず、追加で必要なAnimationのみ独立asset化を検討。必要な追加clipが巨大GLBの再ダウンロードを毎回発生させないこと。
3. **pose actionとsupport**を別管理。終端poseに合わせるだけでなく、world-space foot contact lockと`Seat`/Paw purposeを同期させる。GLB driverは自動再現されない。
4. **blend/interrupt**: poseベクトルの現在値から新意図へ。まず接地とHeadFlowerが壊れない最小transition。エクスポートclipの最後に完全停止するだけの仕組みでは不十分。
5. **検証順**: Blender fixed camera（Front/Side/両3Q）→保存GLB再読込→現行2.22.2のPlayCanvas product loader（同pose）→実アプリで連続動画→端末。Blenderだけの判定で最終技術GOを出さない。
6. **過剰実装禁止**: 全28 Family/84 profiles/252 variants、全季節/全環境で数値固定しない。最初にB2S/S2B/Slow 2–4 stepsとS01の必要チャンネルを**一つずつ**Human Gateへ。
7. **timing hypothesis update**: 実際のヒト視聴者が「遅すぎる」「重さが読めない」「可愛さが失われる」と感じた場合、初期値に固執せず**画面の読みやすさと支持**を維持したままbeatを再構成。

## 12. 反証可能なHuman Review packetの仕様

### 12.1 1 Motionあたり必須の証拠

- 同じv004 source SHAの**neutral/final/no distortion**、HeadFlower ON、sole pads ON。
- `t=0`, anticipation, first forepaw contact, rump unload, rear foot plant, peak rise, settled standing, end/afterglowの姿勢を**Front/Side/3Q**で並べ、各画像にFrame/time、support contact、gaze targetを記入。
- 24fps以上の**連続した等速動画**（動画の切り抜き・可変再生速度・補間や合成による変形隠しなし）。比較A/Bは同一視点・照明・長さ条件を揃える。
- 足裏/臀/前足のworld contact markers、直感的なCOM proxy、足滑り/花侵入/瞼眼球の状態。
- Blender/saved GLB/PlayCanvasで同じ意味姿勢に見えるか。差異は原因をGeometry/Rig/Morph/Export/Shader/Controllerへ分解。
- Motionの始めと終わり、直前/直後、無視可能な入力、危険なinterrupt、再生終了後のsettle/quietの動画。
- 端末で必要なframe time (p50/p95)、GPU / CPU可能な部分、memory trend、5分程度の持続性と発熱。ADB permission blockedならPHONE UNKNOWN、迂回禁止。

### 12.2 FAIL taxonomy

| Gate | 即FAILの例 | 修復方向 |
| --- | --- | --- |
| A: Identity | eyes小さく/硬く、顔平たい、Pink印象崩壊、耳・花が消える | pose範囲 / 個別face補正 / material切り分け。元Canonicalは不変 |
| B: Weight/support | 骨盤が先に空中上昇、supportなしで前肢放す、後足滑走、浮いた接地影 | 接地工程再構成、foot IK/lock、COM移動 |
| C: Anatomy | 短肢が伸びる、肘と肩が塊、足裏と腹が融合、顎下面消える | 必要部位の骨・corrective・接点整合を局所修復 |
| D: Acting | 目線が無意味、毎回同じ大瞬き、急に喜ぶ、過剰な腰振り、全身ぶんぶん | 意図→視線→行動、静止/小反応の比率とtimingを直す |
| E: Temporal | 全Channel同frame開始/終了、等速、床設置直後に移動、afterglowなし | anticipatory beats / intervals / follow-through、支持に沿うblend |
| F: Interaction | 新touchでNeutralへsnap、左右ACK無視、触れた脚を接地中に引き抜く | owner arbitration・現在poseから遷移 |
| G: Runtime | GLBでは正常/PCで8-weight欠落、花material変更、RAF leak、TaskでPlayCanvasロード | 既存Loader互換とlifecycle修正 |
| H: Human | 検証値PASSだが「子熊の立ち方に見えない」「可愛くない」 | HUMAN FAIL、当該Motionを採用せず撮影referenceへ戻る |

**判定分離:** `SRC`(外部文献妥当性), `MECHANICAL`(支持/変形/実GLB), `CRAFT`(意図/間/余韻), `HUMAN`(可愛さ/自然さ), `PHONE`, `APP_DELIVERY`, `RELEASE`。UNKNOWNを自動GOにしない。

### 12.3 比較時の具体的なHuman質問

1. 「これは**子熊が自分で立っている**ように見える？それとも座位poseからモデルを引き伸ばしたように見える？」
2. 「立つと決めた瞬間が**目・頭・前肢**から読める？」
3. 「臀を浮かす前に**本当に前足が支えている**のが分かる？」
4. 「後足が身体の下に入る過程が短肢を壊さず、Sideでも可愛い？」
5. 「完全立位になってからの小耳・花・表情は、余計な振動ではなく身体の余韻？」
6. 「同じ動作を10回見ても、やらされている操り人形でなくShushuらしい？」
7. 「全Motionを押し込まず、途中の静止や小さなためらいが可愛さを増している？」
8. 「他のMotionへ繋いだとき顔と足がsnapしない？」

## 13. Video annotation protocol — 秒数を『事実』に昇格させる条件

**現在: 未計測（UNMEASURED）。次回Codexが合法アクセスできる動画を使い検証し、無理なら未測定のまま保つ。**

必要なcapture fields: `sourceId/URL/publisher/species/subjectAge/sex(if known)/date/fps(if known)/isSpeedAltered/shotAngle/lensUnknown/continuity/groundType/initialPose/finalPose/goalContext/t0Intent/tFore1/tFore2/tRumpUnload/tHindLeft/tHindRight/tStable/tGazeChange/tEarSettled/occlusionFlag/annotator/confidence`。

評価: 同一連続shotでsideまたは3Q、接地が3点以上確認でき、transition全区間が見えるものを優先。編集jump・slow motion・地面が隠れる・誘導された二足standは、測定母集団から除外。5例不足なら不足を記録し、代わりに推定fpsや平均を作らない。

各事件のtimeは**動画内時刻を元動画速度へ正規化**し、不確実度を±N frameで記録。画面奥で足が隠れていれば判定をUNKNOWN。生体の秒数を数える前に、開始/終了定義を全サンプルで一致させる。

**ソース間の非同質性**は同一の平均にまとめない。ジャイアントパンダ/クロクマ/グリズリー、野生/飼育、歩行開始/立ち上がり、3ヶ月/10ヶ月、平地/岩/雪、気分と人間のcueをgroupで分ける。

## 14. 採用優先順・次Codexへの正確な指示

- **First:** v004 actual rig/saved GLBで、`SIT_RUMP → FORE_SUPPORT → RUMP_UNLOADED → FOUR_STAND`の実装可能性を1回調査し、前肢/後肢支持が本当に成立するか最短で試す。これがFAILなら**座位→立位のRig/支点repairだけ**別門として切り出す。
- **Second:** 本章のHero Study Aの `A/B` を1つずつ制作、Front/Side/両3Q、全scene 2.5–3.1s試作、前肢支持と前/後足のworld lockを比較。採用前にHuman Gate。
- **Third:** 成立した場合のみ逆方向座位化、歩行開始2–4歩、終歩/stopを拡張。既存C2 Living Idleは独立に進められるが、本書を参照して大きな座位/立位行為を誤用しない。
- **Fourth:** 統合済みPlayCanvasで同じMotionを可視化し、UIは`DESIGN.md`のポケポケに忠実なshellを維持、背景等は高品質2D/2.5D。3D propの常時追加なし。
- **No authority escalation:** 既存DRAFTの「28 families」「S01–S28」は全て将来候補。本文の演出仮説は本人のHumanレビューで合格するまで**FINAL Motion Authorityへ昇格しない**。

## 15. Source coverage summary and open research risks

**Coverage:** (i) Giant panda cub primary keeper observation including first steps, traction and carefully placed steps; (ii) other cub context (North American Bear Center); (iii) adult bear foot mechanics peer review; (iv) primary studio craft and professional animation teaching; (v) Grimo actual rig/production branch and goal hierarchy. Searches included Japanese/English queries, Smithsonian/Wildlife zoo study, comparative animation / game work. Unverified viral clips, generated animation, breed-disparate recommendations and unsupported exact timings were excluded from factual evidence.

**Open blockers:** (U1) same-camera genuine rump-sit→four-paw uncut panda-cub clip with calibrated timing; (U2) quantitative cub kinematics rather than adult grizzly; (U3) multiple cub personalities and settings (current Smithsonian examples overrepresent Xiao Qi Ji), (U4) Shushu actual hip/forepaw IK/contact and expressions in v004, (U5) real Xiaomi and Vercel app performance/Human review, (U6) original protected frames rights. Do not disguise these limitations with pseudo-precise angles/seconds.

**Practical research stop rule:** start prototype once the transition phases and key source limitations are clear; further 20 web searches cannot substitute seeing the actual model move. If a critical anatomical or visual discrepancy occurs, make **a focused new reference study around that exact beat** instead of repeating the full search.

---
**Bottom line:** まず本物の子熊らしい**接点と荷重移行**を観察し、Shushu自身がそうしたいと分かる**目と間**を加え、動き終わりに落ち着く**余韻**まで一体で試す。**秒数は演出仮説であり、Humanが可愛くないと判断すれば不採用**。