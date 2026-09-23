# Grimo Character Production Architecture — Zero-Based Deep Research


> **Current status note — 2026-09-23**
>
> This document is retained as **architecture-research provenance**, not as an
> immutable architecture lock. Current durable policy is
> `docs/grimo/knowledge/CURRENT_PROJECT_MEMORY.md` plus root `AGENTS.md`.
> The former “final” Full-3D recommendation is now the **Front-Optimized
> 3D-First Living Character Architecture baseline hypothesis**, subordinate to
> the Product North Star. Historical passages that require static Gate A
> perfection before representative motion/runtime work, imply equal-fidelity
> 360° Full-3D purity, or name Pixel 7a as an already available real-device gate
> are superseded. Pixel 7a-class remains an **UNVERIFIED_TARGET**; current
> real-device evidence is Xiaomi 14T Pro. Preserve the research evidence and
> comparisons; do not reinterpret this note as discarding the study.


## 最重要結論と Executive Recommendation

**結論は一つです。Grimoのキャラクター基盤は、2D/2.5Dではなく「stylized full 3D character master + web-native realtime runtime」を採用するべきです。**  
その具体形として、現時点の最終推奨は、

> **Blenderを標準DCC → GLB/glTF → PlayCanvas EngineをPWA内のcharacter runtimeとして使用し、  
> hand-authored animationを主役に、layered animation graph + procedural micro-motion + semantic touch system + restrained secondary dynamicsを重ねる**

方式です。**Unity WebではなくPlayCanvasを総合1位**とします。ただし純粋なanimation/runtime機能の「品質上限」だけならUnityが上です。PlayCanvasを選ぶ理由は、Grimoではレンダリングエンジン自体よりも「アニメーターが作った演技を壊さず、Web/PWA上で多数の非同期channelを合成し、入力へ低遅延で反応させること」が支配的だからです。PlayCanvasにはstate graph、transition interruption、layer、additive blend、bone maskが公式機能として揃い、しかもWebGL 2/WebGPUのWeb-native runtimeです。citeturn23view1turn23view0turn24search1

**最重要結論は以下の3点です。**

| 結論 | 判定 | 根拠種別 |
|---|---|---|
| **生命感は「animation本数」ではなく、異なる時間スケールを持つ複数channelの非同期合成で作る** | 全身を常時動かす方式は棄却。呼吸・視線・瞬き・耳・姿勢・appendage・反応・余韻を疎に重ねる | [C/D/E] |
| **Grimoの要求を満たす最有力表現はfull 3D** | 局所touch、視線、頭眼協調、姿勢、四肢、左右非対称、secondary、将来のviewpoint変更を同一構造で扱える | [D/E] |
| **“物理で生かす”のではなく、“演技を主にして物理を残差に使う”** | primary motion、anticipation、overshoot、settleは手付け。spring/procedural dynamicsは最後の小さな残差だけ | [A/D/E] |

Creaturesの公式インタビューでも、ポケモンの3D化は単純なイラスト立体化ではありません。複数の設定画から骨格、筋肉、毛流れ、隠れた構造まで推測し、原案の印象を維持するために内部チェックと監修を繰り返しています。アニメーション側も生物観察、骨格、筋肉、重さ、浮力などを考えたうえで、キャラクター固有の動きを作っています。つまりPokémon級の生命感の中心は、エンジンの高度さではなく**character-specific art directionとmotion direction**です。citeturn3view0turn3view1turn3view2

さらに『Let's Go』では、増田順一氏へのFamitsuインタビューの英訳によると、当初Pikachu/Eeveeを一人で担当していたmotion designerを分け、**PikachuとEeveeそれぞれに専任motion designerを置いた**と説明されています。これは一次原文を直接取得できなかったため **[B — strong secondary]** と扱いますが、「相棒キャラクターだけ特別にmotion investmentを増やした」ことを示す重要な証拠です。citeturn35search1

**最終ランキング**

| 部門 | 1位 | 判断 |
|---|---|---|
| **総合1位** | **Full 3D + Blender + PlayCanvas Engine** | Grimoへの最終推奨 |
| **品質上限1位** | **Full 3D + Unity 6.x** | animation/rigging ecosystem単体では最強。ただしPWA統合コストを負う |
| **production効率1位・制約無視** | **Rive** | 2Dなら極めて効率的だが、今回の品質要求には不足 |
| **production効率1位・Grimo要求を満たす候補内** | **Blender + PlayCanvas** | DCCからWeb runtimeまで自動化しやすい |
| **Web/PWA適性1位・Grimo要求を満たす候補内** | **PlayCanvas** | Web-nativeかつ高水準animation orchestration |
| **custom runtime自由度1位** | **Three.js** | ただしGrimo専用animation systemを自作する量が増える |
| **PlayCanvasへの最強対抗** | **Babylon.js** | 2026年時点でanimation masking・additive・retargetingまで非常に強い |

ここで重要なのは、**Unityを低品質だから落とすのではありません**。Unity 6.6は現在mobile browser向けruntimeの改善、WebGPU、progressive asset loading、Animation State Machine、Layer、Maskなどを備えており、昔の「Unity Webはスマホ非対応」という評価は既に古いです。citeturn17search2turn26search1  
それでもGrimoではPWAそのものが製品であり、キャラクターはその中の一部です。Wasmでゲームエンジン全体を抱えるより、Webアプリと同じ実行環境にcharacter runtimeを置ける方が、ロード、状態同期、DOM/UI統合、Codexによるコード操作、profiling、自動テストまで含めて有利だと判断します。これは **[D/E]** です。

**重要な調査制約**も先に明示します。今回の環境ではConnected Google Driveで `GRIMO_TECHNOLOGY_AGNOSTIC_MINIMUM_REQUIREMENTS`、`Carol canonical`、さらに `Grimo` 全体を検索しましたが該当ファイルを取得できず、conversation側のFile Search sourceも提供されていませんでした。したがって、**4枚のcanonical画像を実際に視覚確認した、とは報告できません**。Carol/Jill/Pino/Shushuについて以下で行うgeometry-levelの判断は、今回の依頼文に明示された「huge fleece / tiny cream face / leaf / wing / water / flowers」等を材料にした **[E — provisional recommendation]** です。  
この制約はarchitecture全体の比較結果を逆転させるほどではありませんが、**Carolがfull 3Dでcanonical identityを維持できるかというGate Aだけは未通過**です。ここを誤魔化してfull 3D採用済みと扱うべきではありません。

本レポートの証拠ラベルは、指定どおり **[A] Primary、[B] Strong secondary、[C] Observable footage、[D] Inference、[E] Recommendation** とします。

## Pokémon production evidence と他作品から得られる原理

Pokémonの公開資料から最も強く見える原則は、**「共通化するのはcharacter identityではなく、制作インフラである」**ことです。

Creaturesの公式Character Modeler interviewでは、デザイナーによる複数のイラストをそのまま個別に3Dへ写すだけでは、角度間の矛盾が出るため、モデラーが骨格・筋肉・毛の流れ・アクセサリ下の構造などを解釈して一つの立体として統合すると説明されています。新規ポケモンについてはモデルをゼロから作り、監修を通して原案との一致を高めています。[A] citeturn3view0

これはGrimoに非常に重要です。

> **front canonical → generic animal mesh → texture projection**

はPokémonの考え方とほぼ逆です。

Grimoでは、

> **front canonical → identity分析 → unseen geometryの仮説 → turnaround reconstruction → 3D blockout → canonical cameraで再一致 → 3/4/backをart-direct**

と進むべきです。[E]

同じくCreatures公式Animator interviewでは、1000種を超えるポケモンのmotionを継続的に磨きつつ、設定や生態を読み、生物観察を行い、骨・筋肉・重力・浮力などを意識しながらmotionを作っていることが説明されています。同じフレーム数でも「重さ」の見せ方が異なるという趣旨の説明もあります。[A] citeturn3view1

つまりGrimoで重要なのは「物理シミュレータを入れれば自然になる」ではありません。

**motion designerが重さを決める。simulationはその演技を補助する。**

これを原則に置くべきです。

Game Freak側のproduction architectureも示唆的です。CEDEC 2022公式セッション概要によれば、『Sword / Shield』までのポケモンモデルはタイトルごとに仕様を定め、Maya上でデータを構築し、ShaderFXでmaterialを作り、locator等もMaya側に仕込む方式でした。1000種以上へ規模が増え、『LEGENDS アルセウス』と『Scarlet / Violet』を並行開発する段階でこの方式を見直したことが公式概要で明示されています。[A] citeturn9search1

CEDEC講演を取材した複数の技術媒体は、そこからさらに、

- 納品用の標準material / basic skeletonを共通化
- title-specificなlookやIK、gaze等を後工程で追加
- 体型を分類してmotionを再利用
- bone mapping / scale補正 / retargetingを行うmotion copy tool
- rig作業を標準化する **PokeRig**
- runtimeのdynamic control

が使われたと報じています。これらの詳細は今回アクセスできた公式CEDECページ本文にはすべて展開されていないため **[B]** と扱うのが正確です。公式セッションそのものの存在と目的は[A]です。citeturn9search1

そして2026年のCEDECでは、Game Freak自身の『Pokémon LEGENDS Z-A』セッションがcharacter riggingを扱い、講演者紹介・概要で**Game Freak独自rig system「ポケリグ」の進化・運用事例**を扱うことが明記されています。したがってPokeRigは2022年だけの一時的施策ではなく、少なくともZ-A世代まで発展が続いていることを確認できます。[A] citeturn7view0turn8view0

ただし、

> **PokeRigをGame Freakが使っている → Grimoも同じstandard skeletonを作るべき**

とはなりません。

Game Freak側の問題は1000種超のproduction scalabilityです。Grimoは4体です。Grimoが盗むべき原理は、

**rigそのものの共通化ではなく、semantic contract・tools・validation・export schemaを共通化すること**

です。[D/E]

たとえば4体すべての骨を同じにする必要はありません。しかし全キャラクターが、

```text
head
eye.L / eye.R
gaze_origin
face
touch.head
touch.cheek.L / R
body.COM
appendage.primary
expression.neutral / happy / curious / discomfort
```

のようなruntime semantic interfaceを持つことには大きな価値があります。

『Let's Go』固有の制作体制では、前述の通りPikachuとEeveeにmotion designerを一人ずつ付けたという開発者発言が報じられています。[B] citeturn35search1  
これは「専用motionを大量に作れ」という単純な話ではなく、

> **同じinteraction仕様でも、character personalityに合わせてtiming / pose / gaze / appendage / settleを作り分ける**

ことが重要だという証拠です。

最新Pokémonについては、公開情報の強度に差があります。

| 世代 | 公開確認できた事項 | Quality |
|---|---|---|
| Sword / Shield以前 | Maya / ShaderFX中心のtitle-specific model delivery workflow | [A] citeturn9search1 |
| Arceus / Scarlet & Violet | 共通assetを複数titleへ展開するproduction redesign | [A] citeturn9search1 |
| 同上のPokeRig / motion copy / runtime dynamic control詳細 | CEDEC取材各社による報告 | [B] |
| LEGENDS Z-A | 2026 CEDECでPokeRigの進化・運用を扱う | [A] citeturn7view0 |
| Pokopia | 今回、内部character rig/animation architectureを示す公開一次資料を確認できず | 不明 |

したがって**PokopiaがPokeRigを利用しているとは推定しません**。

Pokémon以外で最も有益だった比較対象は**Nintendogs + Cats**です。Nintendo公式のIwata Asksでは、犬と猫では背骨、尻尾、睡眠姿勢、対象への近づき方まで異なり、犬motionを猫へ流しただけでは「猫に見えない」ため、最終的にはほぼ別motionになったことが開発者自身によって説明されています。[A: Nintendo “Iwata Asks — Adding Kittens Doubled the Work”]

さらに3DS版では旧作のtexture eyesから実際のeyeballへ変更し、物体を目で追わせています。犬は見るとき頭全体を動かしやすく、猫はまず眼球中心で追うため、そのgaze behaviorまで別実装にしたと説明されています。[A: Nintendo “Iwata Asks — Back Flips in the Palm of Your Hand”]

これはGrimoにほぼそのまま使えます。

**「eye target systemは共通化できても、head-eye coordination profileはcharacter-specificであるべき」**

ということです。[D/E]

Nintendogsではpersonalityによって慎重・活発・friendlyなど行動傾向を変えたことも公式インタビューで説明されています。[A]  
この原理もGrimoでは、animation clip差分ではなく**behavior probability distributionの差**として実装するのがよいです。[E]

## Partner Eevee Life Analysis

公式の『Let's Go』説明では、partner Pokémonはpetting、feeding、ticklingができ、関係が深まるとhigh-fiveやgiftなどのinteractionへ発展します。[A] citeturn16search23turn32search5

ここで重要なのは、「petting minigameがある」ことではありません。

**Partner Eeveeは、入力されるまで停止して待っているUI objectではない。**

画面内で、

- attentionを変える
- gazeを保持してから外す
- 瞬きを入れる
- 耳を動かす
- head poseを少し修正する
- postureを保つ
- reaction後もしばらく表情や姿勢を残す

ことで、「自分の状態を持っている存在」に見えます。[C/D]

今回参照したPartner Eevee関連の直接映像corpusには、以下を含めました。YouTube側から正確なtimecode付きtranscriptを取得できなかった動画については、**timestampを推測して捏造していません**。

| 映像 | 主な観察対象 | Timestamp |
|---|---|---|
| `https://www.youtube.com/watch?v=RaV8-r7O68E` | Partner Play系 footage、touch時の姿勢・顔 | timecode取得不可 |
| `https://www.youtube.com/watch?v=1UVucW1EOHI` | Partner interaction | timecode取得不可 |
| `https://www.youtube.com/watch?v=fEw37N5i_t8` | Eevee introduction / companion motion | timecode取得不可 |
| `https://www.youtube.com/watch?v=FoJ_sG66_Sw` | partner introduction、指へのorient / lean系反応 | timecode取得不可 |
| `https://www.youtube.com/watch?v=Xv71ftV6XYY` | 長時間gameplay内のpartner behavior | timecode取得不可 |
| `https://www.youtube.com/watch?v=hKIv8gANUf0` | evolutionを拒むpartner reaction | **0:00–0:58 全編** |
| `https://www.youtube.com/watch?v=Hn8j0d_yNjc` | Eeveeとの初期interaction | timecode取得不可 |
| `https://www.youtube.com/watch?v=wpgQRajNDNo` | 約10時間規模のgameplay、spontaneous behavior候補 | timecode取得不可 |
| `https://www.youtube.com/watch?v=WgycxHLG8j4` | Eevee gameplay / interaction | timecode取得不可 |
| `https://www.youtube.com/watch?v=21eTYjNjWzk` | Eevee gameplay / interaction | timecode取得不可 |

検索上ではさらに「Playing with my Partner Eevee!」「Playing with Eevee — Direct Footage」「Pokédex and Partner Play」等のPartner Play動画も確認しています。citeturn29search0turn29search1turn29search6

ただし、この調査環境にはYouTubeをvideo editorのように全フレームscrubしてmotion curveを採取する機能がないため、以下のmicro-motion分解の一部は**内部animation layerを直接確認したものではなく、複数映像の外観からのreverse inference [D]**です。その境界を明確にします。

**Partner Eeveeの最も重要な観察結果 [C/D]**

まず、**全身が常時動いているわけではありません。**

これは非常に重要です。

耳が動いている間、脚は静止していることがある。  
視線を変えてもbody massはほぼ保持されることがある。  
全身reactionの後には一瞬のholdがある。  
blinkだけが発生する時間もある。

つまり生命感は、

```text
body always moving
```

ではなく、

```text
some channel is plausibly alive
while other channels are allowed to rest
```

から生まれています。[D]

機械的なキャラクターは、「breath 2秒周期」「tail 1.5秒周期」「ear 3秒周期」「blink 4秒周期」のように全部が独立oscillatorで永久運動します。

生き物はそうではありません。

Partner Eevee級を目標にするなら、必要なのは**asynchronyだけでなくcorrelated asynchrony**です。

たとえば興味が高まると、

```text
eyes orient
→ small head lead/follow
→ near ear rotates
→ body weight slightly forward
→ hold
```

となり、逆にrelaxed時は、

```text
breath
...
blink
...
ear flick
...
long stillness
```

となるべきです。[D/E]

**touch reactionも一つのclipとして考えない方がよい**です。

Grimoではtouchを次の時間構造へ分解するべきです。[D/E]

```text
contact detected
↓
recognition / attention capture
↓
local reflex
↓
facial response
↓
primary authored reaction
↓
secondary follow-through
↓
overshoot
↓
settle
↓
emotional afterglow
↓
new idle, not necessarily original idle
```

たとえばcheekを撫でた場合、

「happy_pet_cheek.glbを再生して終わり」

では弱い。

理想は、

1. 接触側のcheek / eyelid / earが先に応答
2. gazeが入力位置へ寄る
3. headが少し遅れてlean
4. neck/bodyがさらに遅れて追従
5. opposite earやfleece等にfollow-through
6. contact終了後も目を細めた表情を0.6–2秒程度残す
7. neutralではなく“content idle”へ戻る

です。[E]

この**afterglow**が非常に重要です。

入力が終わった瞬間にneutral poseへcrossfadeすると、

> 「ボタンを押したのでanimationが再生された」

に見えます。

少し残ると、

> 「触れられた結果、この子の気分が変わった」

に見えます。

Partner Eeveeが強い理由をarchitectureとして言語化すると、

> **reactionがanimationの終了ではなく、次のinternal stateの始まりになっているように見える**

ことです。[D]

Partner PikachuとEeveeを比較する原則も同じです。専任motion designerを分けたという開発者発言は、単なるproduction triviaではなく、**同じ“かわいい相棒”でもmotion languageを共有しすぎないこと**が重要だったと読めます。[B/D] citeturn35search1

Pokémon-Amie / Refresh側でも、speciesごとに好き・嫌いなtouch zoneが存在し、反復tapや特殊部位で反応が変わる仕組みが長く使われています。Partner Playはその系譜を相棒一体へ強く集中させたものです。[B]  
これがGrimoの `zone × gesture × current behavior × emotion × repetition` モデルの強い先例になります。

## Sense-of-Life Model と Recommended Animation Architecture

Grimoの「生命感」は、animation clipsの合計ではなく、次の積として考えるべきです。[E]

```text
Life ≈
Identity Fidelity
× Causal Responsiveness
× Temporal Layering
× Behavioral Variability
× Intentionality
× Continuity of Internal State
```

**積**で考えるのが重要です。

canonicalから外れた顔が高度に動いても失敗。  
touchに遅れて反応すれば失敗。  
100種類のidleがランダム再生されるだけでも失敗。  
physicsが豊かでも意図が感じられなければ失敗。

animation量でこれらを補えません。

推奨するruntime architectureは以下です。

```text
relationship / context memory
          ↓
emotion + arousal + attention state
          ↓
utility-based intent selector
          ↓
hierarchical behavior controller
          ↓
animation coordinator
          ↓
┌─────────────────────────────┐
│ authored base / major action │
├─────────────────────────────┤
│ posture / weight shift       │
│ breath                       │
│ gaze + head coordination     │
│ blink / eyelids              │
│ facial expression            │
│ ear / appendage micro-motion │
│ touch-local reaction         │
│ emotional afterglow          │
│ secondary follow-through     │
│ limited IK / constraints     │
└─────────────────────────────┘
          ↓
 identity / silhouette clamps
          ↓
       final pose
```

**Behavior layerには、純粋なBehavior Treeより `Utility AI + HFSM` を推奨します。[E]**

理由はcompanionの自発行動です。

Utility scoreなら、

```text
curiosity
attention_need
recent_touch
arousal
fatigue
time_since_last_action
user_presence
repetition_penalty
character_personality
```

から、

```text
look_at_user
look_away
ear_twitch
self_groom
invite_touch
inspect_environment
shift_posture
rare_action
rest
```

の重みを連続的に変えられます。

一方、大きなreactionやinteraction sequenceはHFSMで、

```text
anticipate
→ perform
→ settle
→ afterglow
```

を厳密に管理します。

Animation State Graphは**behavior AIとして使いすぎない**方がよいです。

PlayCanvas側のgraphは、

- clip playback
- transition
- interruption
- masking
- blending

に限定し、

**「なぜこの行動をするか」はTypeScript側のGrimo Behavior Runtimeが決定する**

という分離が最も保守しやすいです。[E]

PlayCanvasの公式Anim State Graphはtransition duration、exit time、transition interruption、priority、ANY state、parametersを持ち、複数layerをOverride/Additiveで合成できます。[A] citeturn23view1  
Bone maskも公式に存在するため、たとえばbodyのbase idleを継続しながら、head/earだけtouch reactionへ移行できます。[A] citeturn23view0  
animation eventsも利用できるため、contact moment、sound cue、safe interrupt point等をclipへ埋め込めます。[A] citeturn23view2

**channel設計**

| Channel | 通常のdriver | 常時動かすか | Grimo方針 |
|---|---|---:|---|
| body / COM | base behavior | × | 長いhold + 稀なweight shift |
| breathing | physiology/emotion | △ | 常時だが極小。大きくしない |
| blink | stochastic + emotion | × | refractory periodを持つevent |
| eyelid | gaze/emotion/touch | × | blinkと別channel |
| gaze | attention | × | dwellを重視 |
| head | gaze/intent | × | eyeより遅れて追う |
| ears L/R | attention/emotion | × | 左右を独立させる |
| mouth / cheek | emotion/event | × | preset中心 |
| forelimbs | posture/action | × | 原則静止、時々調整 |
| hindlimbs | COM/action | × | weight shift時のみ |
| tail | emotion/action | × | constant wag禁止 |
| fleece / leaves / flowers | residual dynamics | × | primary motionから遅れて小さく |
| autonomous acts | utility scheduler | × | cooldown + repetition suppression |
| touch reaction | input | × | local-first |
| afterglow | previous event | × | decayするinternal state |
| context memory | logic | 常時 | visualではなく確率分布を変える |

ここで**intentional stillnessを正式な状態として扱う**べきです。[E]

「完全静止を避ける」の意味は、

> 毎フレーム何かのboneを変える

ではありません。

> 数秒間観察しても“renderが止まった”ようには見えない

という意味です。

idleの優れたキャラクターには**静止のコントラスト**があります。

Grimoでは、micro channelごとに最低間隔とcooldownを持たせます。

```text
blink:
  random interval
  + emotion modifier
  + post-action suppression

ear:
  L and R separate clocks
  + attention correlation
  + recent-use penalty

weightShift:
  much lower frequency
  + requires stable base state

rareIdle:
  long cooldown
  + recent-history exclusion
```

recent behaviorは最低5～8件程度をring bufferで保持し、同じreaction familyの連続選択を抑えるのがよいでしょう。[E]

**Face / Eye / Gazeの最終推奨はhybridです。**

純bonesでも純morphでもありません。

```text
eye aim            → joints / transforms
pupil/iris offset  → eye rotation or shader
upper/lower eyelid → morph targets中心
blink              → paired eyelid morph
asymmetric squint  → side-specific morph
cheek              → morph
mouth corner       → morph
muzzle/nose        → small morph where needed
jaw large-open     → joint + corrective morph
head aim           → neck/head joints
```

理由はidentityです。

可愛いstylized faceでは、自由度が高すぎるfacial rigはむしろ危険です。

そこで各morphを自由に0–100%混ぜるのではなく、

```text
neutral
curious
content
delighted
discomfort
excited
sleepy
```

等の**approved expression presets**を作り、その間のみblendします。[E]

これを「identity envelope」とします。

Runtime procedural codeはこのenvelopeを超えない。

たとえばgaze targetが画面端にあっても、

```text
eye yaw max
head yaw max
eyelid compensation range
```

をキャラクターごとに制限し、off-modelな白目・潰れた目・不自然な口を作らないようにします。

Nintendogs + Catsで、犬と猫で「目だけ追うか、頭まで追うか」まで別設計したというNintendoの開発者説明は、このcharacter-specific head-eye coordinationを強く支持します。[A]

**Touch architecture**

最終推奨は、

> **semantic bone-attached analytic hit volumes**

です。[E]

render meshへのper-triangle skinned collisionをprimaryにしません。

```text
screen touch
   ↓
camera ray
   ↓
bone-attached sphere / capsule / OBB set
   ↓
semantic zone
   ↓
gesture trajectory accumulator
   ↓
zone × gesture × emotion × behavior × repetition
   ↓
reaction policy
```

基本zoneは、

```text
head
forehead
cheek.L
cheek.R
ear.L
ear.R
nose/muzzle
chest/body
forelimb.L/R
hindlimb.L/R
tail
character-specific appendage
```

です。

必要に応じて一部zoneに複数volumeを置きます。

render mesh colliderよりこちらを選ぶ理由は、

- deforming triangle meshをCPU側で追う必要がない
- touch semanticsが最初から得られる
- animation中もbone transformで追従する
- fleece等の特殊形状を意図的なtouch surfaceとして設計できる
- art側で「ここを触ってほしい」を設計できる

からです。[D/E]

gestureは最低でも、

```text
poke/tap
slow_stroke
back_and_forth_stroke
hold
```

まで内部では区別した方がよいです。

依頼上の3種類に加えて`hold`を内部分類する理由は、cheek leanやhead pressのような「触れ続けると成立するinteraction」を後から作れるからです。[E]

stroke判定には、

- contact duration
- path length
- average speed
- peak speed
- directional reversal count
- zone occupancy
- entry/exit position

を使います。

reaction selectionは、

```text
R = f(
  zone,
  gesture,
  current_behavior,
  emotion,
  arousal,
  recent_reactions,
  repetition_count,
  relationship,
  cooldowns
)
```

です。

これで同じcheek petでも、

初回 → surprised/curious  
2回目 → pleased lean  
連打 → mild disengagement  
眠い時 → eye-close lean  
別行動中 → earだけ返事して無視

のような**agency**を持てます。[E]

**Secondary motion**

結論は、

> **hand-authored primary + limited procedural residual**

です。

fully hand-authoredだけでも良い作品は作れますが、micro residualを全clipへ手付けすると修正量が爆発します。逆にfull runtime physicsではsilhouetteが壊れます。

したがって、

```text
authored animation
      ↓
authored follow-through
      ↓
small spring residual
      ↓
limit / damping / pose clamp
```

とします。

Carolのfleece全体をsoft-body simulationする案は**No-Go**です。[E]

huge fleeceがidentityの中心なら、外形はartist-controlledであるべきです。

Carolでは、

- main fleece mass：stable modeled silhouette
- 2～4程度のlarge deformation controls：authored
- outer tuft groups：小振幅secondary
- shading/normal：柔らかさの主表現
- special reaction：必要ならoffline simulationをbakeして手修正

とするのがよいでしょう。[E]

Jillはwing/leafの主要arcを手付けし、tipだけspring。  
Pinoのthick tailはbaseを手付け、末端1～2 chainだけresidual spring。水/bubble motifはsoft bodyではなくshader/particles。  
Shushuのflowers/bouquetはflower clusterをrigid-ish groupとして扱い、花首・petal clusterに小振幅lagを入れる。

**physical correctnessよりappealを優先します。**

これはPokémon/Creatures側が生物構造や重量を参照しつつ、最終的にはcharacter motionとして演出しているproduction philosophyとも整合します。[A/D] citeturn3view1

## Candidate Architecture Comparison と PWA / Pixel 7a

以下の点数は**公式benchmarkではありません。[E — architectural estimate]**  
10点満点で、今回の要求に対する適性を比較したものです。

略称：

- **PC** = Full 3D + PlayCanvas
- **BAB** = Full 3D + Babylon.js
- **THR** = Full 3D + Three.js custom runtime
- **UNI** = Full 3D + Unity Web
- **GOD** = Full 3D + Godot Web
- **L2D** = Live2D Cubism
- **RIV** = Rive
- **SPI** = Spine + PixiJS
- **PR2D** = 3D master → pre-rendered 2D runtime

**品質・interaction側**

| 評価軸 | PC | BAB | THR | UNI | GOD | L2D | RIV | SPI | PR2D |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| canonical fidelity | 9.0 | 9.0 | 9.0 | 9.2 | 8.8 | **9.5** | 9.0 | 9.0 | **10** |
| animation-quality ceiling | 9.3 | 9.4 | 9.5 | **10** | 9.0 | 7.8 | 7.8 | 8.0 | 8.5 |
| sense of life | 9.5 | 9.4 | 9.4 | **9.8** | 8.8 | 8.2 | 8.3 | 8.0 | 7.5 |
| facial quality | 9.0 | 9.2 | 9.2 | **9.7** | 8.8 | 9.2 | 8.5 | 8.0 | 9.0 |
| gaze | 9.5 | **9.7** | **9.7** | **9.8** | 9.0 | 8.3 | 8.0 | 7.5 | 6.0 |
| touch causality | 9.7 | 9.7 | 9.7 | **9.8** | 9.0 | 6.5 | 6.5 | 6.8 | 4.5 |
| autonomous behavior | 9.5 | 9.5 | 9.5 | **9.7** | 9.2 | 9.0 | 9.0 | 9.0 | 7.0 |
| secondary motion | 9.0 | 9.3 | 9.2 | **10** | 9.0 | 7.0 | 7.2 | 8.0 | 7.0 |
| interruptibility | 9.5 | 8.8 | 8.0 | **10** | 9.0 | 8.5 | 9.0 | 9.0 | 4.0 |

**production/runtime側**

| 評価軸 | PC | BAB | THR | UNI | GOD | L2D | RIV | SPI | PR2D |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| motion scalability | 9.0 | **9.3** | 8.0 | **10** | 8.7 | 7.5 | 7.0 | 8.0 | 3.0 |
| four-character scalability | 9.0 | 9.0 | 9.0 | **9.5** | 8.7 | 6.5 | 6.5 | 7.0 | 5.0 |
| authoring efficiency | **8.5** | 8.2 | 7.5 | 7.5 | 7.7 | 9.0 | **9.5** | 9.0 | 5.0 |
| AI automation | 9.0 | 9.0 | **9.5** | 8.5 | 8.5 | 7.5 | 8.5 | 8.0 | 8.0 |
| PWA compatibility | 9.7 | 9.6 | **9.8** | 6.8 | 7.0 | 9.8 | **10** | 9.8 | **10** |
| Pixel 7a fit | 9.0 | 9.0 | 9.2 | 7.2 | 7.5 | 9.8 | **10** | **10** | 9.5 |
| asset footprint | 8.0 | 8.0 | 8.5 | 5.5 | 6.5 | 9.5 | **10** | 9.5 | 4.0 |
| maintainability | **9.0** | 8.6 | 7.8 | **9.2** | 8.5 | 8.5 | 9.3 | 9.0 | 6.0 |
| long-term extensibility | 9.5 | 9.5 | **10** | **10** | 9.0 | 7.0 | 7.0 | 7.5 | 4.5 |

今回のquality-firstかつPWAを強めに重み付けした概算では、

| Architecture | Weighted estimate |
|---|---:|
| **Full 3D + PlayCanvas** | **9.25** |
| Full 3D + Babylon.js | 9.23 |
| Full 3D + Three.js | 9.20 |
| Full 3D + Unity Web | 9.09 |
| Full 3D + Godot | 8.51 |
| Rive | 8.45 |
| Live2D | 8.43 |
| Spine + PixiJS | 8.43 |
| 3D master → pre-rendered 2D | 7.27 |

差の0.02に意味を持たせすぎるべきではありません。**PlayCanvas / Babylon / Three.jsの上位3つは実質同じtier**です。[E]

それでもPlayCanvasを選ぶ理由は明瞭です。

Three.js公式にはAnimationClip / mixerやglTF loaderがあり、Draco、Meshopt、KTX2/Basis系を含むglTF extensionに強い基盤があります。[A] citeturn25search0turn25search1  
しかしGrimoでは、その上にstate machine、mask、interrupt policy、layer policyを自前で構築する領域が増えます。[D]

PlayCanvasはその中間層を既に持っています。citeturn23view1turn23view0

Babylon.jsは2026年時点ではかなり強力です。公式docsではAnimationGroupのweight/blending、mask、additive animation、BoneLookController、BoneIKControllerがあり、v9系ではavatar retargetingも追加されています。[A]  
これは**次点をThree.jsではなくBabylon.jsとする理由**です。

ただしGrimoは4体であり、人型100体をmotion retargetするゲームではありません。PlayCanvasのstate graph/interruption/layer orchestrationの方が、今回の中心課題に少しだけ近いと判断します。[E]

**2D系を最終的に棄却する理由**

Live2D/Rive/Spineが低品質なのではありません。

front canonicalへの一致ではむしろ非常に強い。

Live2Dは公式Web SDKを持ち、Riveもstate-machine-driven interactive animationをWebで効率よく実行でき、PixiJSも現在WebGL/WebGPUベースの2D engineとして強力です。citeturn27search0turn27search1

しかし今回必要なのは、

- cheekを触った方向へ局所変形
- head / eyes / ear / bodyの別タイミング
- body weight shift
- fore/hind limbの姿勢
- appendageの奥行方向follow-through
- four characters with very different volume
- 将来のcamera / pose expansion

です。

これを2D rigで実現できないわけではありません。

**できるが、奥行方向のvariationごとにartist-authored deformation assetsを増やすことになり、生命感を増やすほど組合せ爆発が起きる**のが問題です。[D]

`3D master → pre-rendered 2D`も、ルック固定には強いですが、runtimeでの局所touch、gaze target、非同期channel合成、interruptibilityを犠牲にします。

したがって今回は不採用です。

**Pixel 7a**

Google公式仕様ではPixel 7aはTensor G2、8 GB LPDDR5 RAMを搭載するclassの端末です。[A] citeturn31search4turn31search12  
しかし**Grimo modelの実測benchmarkは存在しません**。したがって以下は公式limitではなく、Vertical Sliceで検証するための **[E — initial engineering budgets]** です。

| 項目 | 初期budget |
|---|---|
| 同時表示hero character | 原則1体 |
| LOD0 geometry | **30k–60k triangles目安**。Carol fleeceで必要なら80kまでprofile |
| deform bones | **70–110程度を初期上限目安** |
| vertex influences | 4以内を基本 |
| character draw calls | **≤ 8を目標** |
| facial shapes | 必要な表情shapeのみ。総数より同時evaluation costをprofile |
| texture | main 2K級 + auxiliary 1K級を基本。不要なPBR mapsを持たない |
| compression | KTX2/Basis + mesh compressionを比較 |
| first-character compressed payload | **6–12 MB程度を目標** |
| 他3character | lazy load |
| interaction | **60 fps target** |
| quiescent long idle | thermal/battery次第でadaptive 30 fpsを検討 |
| main-frame target | 16.7 ms未満を基本 |
| severe stutter | 33 ms超の連続を許容しない |

PlayCanvasはGLBをnativeに扱い、KTX2/Basis textureもサポートしています。[A] citeturn18search0turn24search0

ここで重要なのは**WebGPU必須にしないこと**です。

PlayCanvasはWebGL 2とWebGPUの両backendを持ち、WebGPUからWebGLへのfallbackを提供していますが、Grimoのacceptance baselineはWebGL 2に置くべきです。citeturn24search1

理由は、

> WebGPUがあれば高品質になる

のではなく、

> WebGL 2でもPartner-quality characterが成立するほどasset/runtimeを軽くし、WebGPUでは余裕を増やす

方がrobustだからです。[E]

PWAにはもう一つ非常に重要な制約があります。

**アプリがOS backgroundへ回った後もcharacterをリアルタイムに動かし続ける設計は成立しません。**

これは「非入力時にも存在している」という要求とは分ける必要があります。

Grimoがforeground表示中だがユーザーが触っていない時間には、もちろんcharacterは生き続けます。

一方、PWAがbackground/frozen/discardedになるとbrowser側がanimation/timerを止め得るため、

```text
backgroundでずっとsimulation
```

ではなく、

```text
lastKnownState + timestamp
↓
resume
↓
elapsed-time reconciliation
↓
plausible new state
```

を採用すべきです。[E]

つまり戻ってきたときに、

「30分間見ていなかったので30分のanimationを早送り」

ではなく、

「少し眠そうになっていた」「別のposeで待っていた」

などinternal stateだけ進めます。

## Recommended Production Pipeline・Rig・AI Automation

**DCCはBlenderを最終推奨**します。

これは「Mayaより画質が良い」という意味ではありません。

MayaはGame Freakの公開pipelineにも明確に登場しており、大規模studio character animation pipelineでは依然合理的です。citeturn9search1

しかしGrimoは、

- 4 character
- small team
- AI-heavy production
- web delivery
- deterministic automation
- glTF/GLB
- custom scripting

という条件です。

BlenderのPython API、headless execution、rig/shape key/animation、glTF exporterまで一環してscript化できる利点の方が大きいです。[A/E] citeturn33search2

**推奨pipeline**

```text
canonical image
↓
identity analysis
↓
landmark / silhouette sheet
↓
unseen-geometry hypotheses
↓
human-approved turnaround reconstruction
↓
3D blockout
↓
canonical-camera match
↓
3/4 + side + back art-direction
↓
final modeling / sculpt
↓
retopology
↓
UV + texture / NPR lookdev
↓
character-specific rig
↓
facial identity envelope
↓
skinning / deformation QA
↓
authored animation library
↓
secondary authored/procedural setup
↓
touch semantic volumes
↓
LOD / optimization
↓
GLB export
+ character manifest
↓
automated validation
↓
PlayCanvas runtime
↓
Pixel 7a QA
```

**正面canonicalしかない問題**

一枚のfront imageから唯一の「正しい背面」は数学的には決まりません。

したがってAI生成turnaroundをsource of truthにしてはいけません。[D/E]

AIに複数案を作らせるのは有効です。

```text
Hypothesis A: spherical body
Hypothesis B: flattened fleece
Hypothesis C: deeper torso / small hidden body
```

などを出し、その中からhuman art directionで選びます。

**front canonicalは“sacred view”として固定**してください。[E]

最終モデルは少なくとも、

- canonical camera
- slight 3/4 left
- slight 3/4 right
- side
- rear 3/4

でrender comparisonします。

canonical viewでは、

- outer silhouette
- eye centers
- eye size
- eye spacing
- face/body area ratio
- ear angle
- visible hoof position
- key color regions
- moon/star landmark

等を数値化します。

ただしpixel similarityを最終判定にしません。

なぜなら3Dの正しいlighting variationまでpixel metricが罰する可能性があるからです。

**machine metric → anomaly detection  
human → identity verdict**

の順にします。[E]

**Rendering**

canonicalがillustrative characterなら、default PBR animalにしない方がよいでしょう。[E]

推奨はcontrolled NPRです。

- hand-painted base color
- restrained roughness
- very limited specular
- artist-directed shadow ramp
- face lightingを安定
- hard photoreal AOを避ける
- silhouette-first
- furはstrand hairではなくvolume/normal/detail texture中心

特にCarolのhuge fleeceでstrand furを全面採用すると、canonical identityを「リアルな羊毛」へ勝手に翻訳する危険があります。

**canonicalに毛一本一本が描かれていないなら、3Dでも描きすぎない。**

これが重要です。[E]

**Rig architecture**

4体に同じ骨格を押し付けません。

共通化するのはrig APIです。

```text
character_root
├── world_motion
├── body_root / COM
│   ├── torso / spine family
│   ├── neck
│   │   └── head
│   │       ├── eye.L
│   │       ├── eye.R
│   │       ├── eyelid/facial drivers
│   │       ├── jaw (optional)
│   │       ├── ear.L chain
│   │       └── ear.R chain
│   ├── forelimb.L
│   ├── forelimb.R
│   ├── hindlimb.L
│   └── hindlimb.R
├── tail / appendage chains
├── character-specific structures
├── touch anchors
└── effect / prop anchors
```

Carolについて、依頼文のdescriptionだけを前提にした暫定設計は、

```text
hidden torso / COM
+ four limb anchors
+ tiny-face-specific head rig
+ 2–3 bone ears
+ stable fleece mass controls
+ small secondary tuft groups
+ moon/star semantic anchor
```

です。[E — canonical未確認]

特に**fleeceをbody geometryそのものと同一視しない**方が良い可能性があります。

内部に簡略化したanatomical torsoを置き、その外側にfleece volumeを被せることで、

- COM shift
- limb attachment
- head movement
- fleece lag

を分離できます。

これなら「ふわふわの塊そのものが四肢と一緒にゴムのように伸びる」事故を防げます。[E]

Jill/Pino/Shushuも同じskeletonにしません。

代わりに、

```text
semantic role:
  gaze
  head
  primary_appendage
  expression
  touch_zone
  secondary_chain
```

を共通化します。

これこそPokeRigの「標準化」の原理を4体規模へ適切に縮小した形です。[D/E]

**Animation asset方針**

大きく3種に分けます。

**Authored full/base clips**

- major idle pose
- weight shift
- invite
- delight
- discomfort
- surprise
- large reaction
- feeding/social actions
- rare signature actions

**Authored additive/masked fragments**

- head micro
- ear twitch L/R
- small shoulder/body adjustment
- pleased lean
- recoil
- breath variation

**Procedural channels**

- gaze target
- eye/head coordination
- blink scheduling
- subtle breathing modulation
- spring residual
- touch tracking
- expression weight decay

「clip vs procedural」は二者択一ではありません。

**intentional motion = authored  
continuous targeting = procedural  
unpredictable residual = dynamics**

と役割で分けます。[E]

**AI / Codex automation**

2026年のCodexはCLIからrepositoryを読んで編集し、command executionを行い、MCP経由で外部tools/contextへ接続できます。[A] citeturn33search0turn33search1turn33search8

ただしproduction architectureを「特定のBlender MCP implementation」に依存させるのは避けます。

2026年にもCodex側のMCP interfaceには変更があるため、MCPそのものを唯一のautomation contractにすると脆いです。citeturn33search10

**production contractはBlender Python + CLI + deterministic manifests** にしてください。[E]

```text
Codex
  ↓
Python / CLI scripts
  ↓
Blender
  ↓
validated GLB
```

を本線にし、

```text
Codex ↔ MCP ↔ Blender
```

はinteractive convenience layerに置きます。

**AIに任せるべきもの**

- naming / hierarchy validation
- rig semantic-tag checking
- export
- batch render
- screenshot capture
- GLB metadata inspection
- texture-size checks
- bone/influence checks
- touch-volume visualization
- clip enumeration
- asset manifest generation
- browser startup
- scripted touch gestures
- FPS/frame-time collection
- visual regression diff
- canonical landmark deviation
- load-size regression
- dead-animation detection

**AI-assistedだがhuman approvalが必要**

- unseen geometry proposals
- turnaround drafts
- retopo suggestions
- texture drafts
- rough motion blocking
- animation retargeting
- automatic weighting
- expression candidate generation

**人間が手放してはいけない部分**

- face
- eye identity
- silhouette
- canonical interpretation
- key poses
- timing
- anticipation
- overshoot
- settle
- emotional afterglow
- “cute / alive / off-model”の最終判断
- hero reactions

ここをAIへ完全委任すると、production speedは上がっても今回のKPIは下がります。

## Carol Vertical Slice と四キャラ展開

**Carolは、今回の文字情報だけからは「full 3Dに不向き」と判断する理由はありません。**

むしろ、

- large volumetric fleece
- small face embedded in large body mass
- independent ears
- hooves
- touchable body
- head/cheek reaction

という構造は、**上手く3D化できれば3Dの利点が非常に大きいタイプ**です。[E]

ただし逆に、canonicalが「正面特化の図形的錯視」で成立している場合は、3D化すると3/4 viewで急激に別キャラクターになる可能性があります。

だからCarolこそ**最初のtechnology probe**に向いています。

いきなり4体作らないでください。

**Gate A — canonical identity**

まず静止状態だけ作ります。

animation不要です。

合格条件：

- canonical cameraから見て「同一キャラ」と即認識できる
- face/body比率を維持
- tiny cream faceの印象が崩れない
- huge fleeceがgeneric sheep woolにならない
- ears/hooves/moon-star landmarkが一致
- 3/4でも破綻しない
- NPR lighting下でcanonical color hierarchyを維持

**ここで失敗したfull 3Dへanimationを追加してはいけません。**

Gate Aが一番重要です。

**Gate B — 15–30秒 living idle**

次にtouch無しで30秒見ます。

必要なのは大量のidle clipではなく、

- stable base pose
- breath
- blink
- gaze
- eye/head coordination
- ear L/R
- 2～3種のsmall head adjustment
- 2～3種のweight shift
- fleece residual
- intentional stillness
- one small autonomous curiosity action

です。

合格条件は、

> 30秒見て「loopを見せられている」と感じないこと。

さらに、動画を音無しで見てもanimation layer同士が同周期に見えないこと。

**Gate C — head / cheek pet**

headとcheekだけでよいです。

必要reaction familyは最低3種類ずつ。

```text
gentle positive
surprised-positive
repeat / mild-satiation
```

headとcheekで**同じ全身animationを再生しない**こと。

cheek側の局所変化が最初に見えるべきです。

合格条件：

- touch位置と反応側が一致
- dragging中もzone trackingが破綻しない
- head turning中もcolliderが追従
- repeated petで完全同一reactionにならない
- interaction終了後にafterglowが残る
- touchからvisual responseまで「ボタン感」がない

**Gate D — one larger reaction**

大きな喜び、驚き、自発invitationなど一つだけ作ります。

ここで、

```text
anticipation
primary action
follow-through
overshoot
settle
afterglow
```

が全部読めるかを見ます。

このGateが通らない場合、animation quantityを増やしてもEevee級には届きません。

**Gate E — Pixel 7a**

実機で、

- cold load
- first-character load
- 30秒idle
- continuous pet
- large reaction連打
- 5～10分連続
- foreground→background→resume

を測ります。

Acceptance targetは[E]として、

```text
interactive motion:
  60 fps target

no sustained:
  >33 ms frame streaks

memory:
  no progressive leak

thermal:
  later-session frame timeが著しく崩壊しない

resume:
  no giant dt / simulation explosion

touch:
  collider tracking remains correct
```

とします。

**四キャラへ移るのはGate E通過後です。**

展開順は、

```text
Carol
↓
もっともrig morphologyがCarolから遠いcharacter
↓
remaining two
```

が良いです。

4体を似た順に作ると、shared architectureが本当にgeneralか分かりません。

今回のdescriptionだけなら、Carolの次には**JillかShushu**のようなwing/leaf/flower系を持つcharacterを置くのがよいでしょう。[E]

## Go / No-Go・Repository Rebuild・最終判定

**full 3Dを採用する条件**

次が全部成立したときです。

| Gate | Go条件 |
|---|---|
| Identity | canonical cameraで明確に同一キャラ |
| Multi-view | 3/4 viewで「別物」にならない |
| Idle | 30秒でloop感・robotic periodicityが目立たない |
| Face | blink/gaze/expressionでoff-modelにならない |
| Touch | local-first reactionが成立 |
| Large reaction | anticipation→settleまで読み取れる |
| Runtime | Pixel 7aでinteraction時60fps級を維持 |
| Load | PWA体験をcharacter runtimeが支配しない |
| Automation | export/QAがrepeatable |
| Scalability | 第2characterでruntimeを大幅forkしなくてよい |

**full 3Dを捨ててhybridを検討する条件**

最も重要なのは性能ではなく**identity failure**です。

以下のいずれかならfull 3Dを再考します。[E]

- canonicalのfront identityは再現できるが、わずかなhead rotationだけで顔が壊れる
- silhouetteを保つには極端なcamera-specific geometryが必要
- fleece等が3D lightingを受けるだけでcanonical印象を失う
- canonical identityを維持するため、ほぼfront-fixed cameraしか使えない
- 3D facial deformationの許容範囲が狭すぎて十分な表情が出ない
- Pixel 7aで品質を保つための削減がcanonical fidelityを壊す

この場合の第2候補は、

> **3D internal rig + controlled 2.5D presentation**

です。

ただし「完成一枚絵をwarp」は禁止を維持します。

3D geometry / independent facial / appendage structuresを持ったまま、cameraとrender styleを強く固定する方向です。

**2D系へ戻る条件**

さらに厳しく、

- Gate Aを複数の3D reconstructionで通せない
- character designそのものが2D optical constructionに依存
- 奥行を与えるほどcanonicalが壊れる
- interaction requirementを2D articulated rigで十分満たせることが実証された

場合です。

この場合もRive/Live2D/Spineの**独立part rig**を使い、1枚絵全体のscale/warp animationは禁止です。

ただし現時点の証拠では、ここへ戻ることを推奨しません。

**Repository Rebuild**

既存repoを前提にしない場合、残す/捨てるカテゴリは次の通りです。

| Category | 推奨 |
|---|---|
| product logic / auth / data / navigation / non-character UI | **残す候補** |
| user/account/state/domain models | **残す候補** |
| PWA shell / install / routing | **原則残す候補** |
| existing character-specific Pixi/2.5D renderer | **新architecture採用時は廃止候補** |
| whole-image idle transforms | **廃止** |
| legacy character animation state assumptions | **archiveして参照のみ** |
| old asset generation experiments | **archive** |
| old research | **evidence archiveとして保持、decision authorityは外す** |
| new `character-runtime` | **新規** |
| new `behavior-runtime` | **新規** |
| new `animation-orchestrator` | **新規** |
| new `touch-semantic-system` | **新規** |
| new `character-manifest/schema` | **新規** |
| Blender production repo/scripts | **新規** |
| GLB validation/export pipeline | **新規** |
| canonical visual-regression suite | **新規** |
| Pixel 7a performance harness | **新規** |

実装を始める前に、**Character Runtimeをproduct applicationからpackage boundaryで切る**べきです。[E]

理想的には、

```text
Grimo App
   ↓
Character Experience API
   ↓
Behavior Runtime
   ↓
Animation Runtime
   ↓
PlayCanvas
```

です。

Product側が、

```ts
character.reactToTouch(...)
character.setContext(...)
character.setMoodHint(...)
character.enterScene(...)
```

のようなsemantic APIしか知らない状態にします。

PlayCanvas entity名やbone名をReact/UI側へ漏らさない。

これにより、最悪Vertical SliceでPlayCanvasをBabylon.jsへ交換しても、product repoを巻き込まずに済みます。[E]

**最終的なGo判断**

現時点では、

> **Full 3DへGo。  
> Blender + PlayCanvas Engineを第一候補としてCarol Vertical Sliceを作る。  
> ただしproduction全体の確定ではなく、Carol Gate Aをfull 3D方式そのものの最終拒否権にする。**

が最も合理的です。

以前のPixiJS / layered 2.5D推奨は、今回の要求に対しては**覆すべき**です。

理由は「3Dの方が新しい」からではありません。

今回明文化されたGrimoの品質目標が、

- 局所touch causality
- depth-aware gaze
- head-eye coordination
- independent ears / limbs / appendages
- weight shift
- body-local reaction
- secondary follow-through
- interruptible layered behavior
- four morphologically different characters
- long-term spontaneous behavior

まで拡張されているからです。

この要求集合では、2D/2.5Dが持っていたfront-view fidelityと軽量性の優位よりも、**3Dの構造的独立性・局所性・composabilityの価値が上回ります。[D/E]**

一方で、Pokémonから最も真似すべきものは3D engineではありません。

Game Freak/Creaturesの公開情報から一貫して見えるのは、

> **asset standardizationとcharacter-specific artistryを混同しないこと**

です。モデル制作では設定画をそのまま機械変換せず、隠れた構造を人間が解釈する。motionでは生物・重量を理解し、キャラクター固有の演技を作る。大規模productionではrig/toolを標準化しながら、タイトル・character側で必要な調整を後付けする。citeturn3view0turn3view1turn9search1turn7view0

Grimoでも同じです。

**標準化すべきもの**

```text
asset schema
semantic rig interface
touch protocol
behavior protocol
animation layer protocol
export
validation
performance QA
```

**標準化しすぎてはいけないもの**

```text
face
silhouette
timing
head-eye character
ear language
posture
reaction personality
signature motion
```

そしてPartner Eeveeから取るべき最後の原則は、

> **「ずっと動いている」ことではなく、「何かを感じ、何かへ注意を向け、触れられた結果が少し残り、次に何をするかが完全には読めない」ことが生命感である**

ということです。[C/D/E]

したがってGrimoの最終architectureは、単なる「3D character viewer」ではありません。

```text
canonical-faithful 3D body
+
character-specific authored performance
+
asynchronous sparse micro-motion
+
attention system
+
semantic touch causality
+
emotion / short-term memory
+
utility-driven spontaneous behavior
+
layered interruptible animation
+
controlled secondary motion
+
web-native realtime delivery
```

であるべきです。

**これが、現在のGrimo要件に対する最終推奨1位です。**