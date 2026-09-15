# Grimo — Partner Pikachu Video Motion & Interaction Analysis

## 0. Document Purpose

この文書は、Grimoのキャラクター制作・animation・interaction・behavior runtime設計のために、このチャット内で**実際に添付され、実映像として解析した Partner Pikachu の4本のMP4**を一つの恒久的なProject Knowledgeへ統合したものです。

対象は以下の4本です。

1. `1_【ピカブイ】ピカチュウとのふれあい【ポケモンレッツゴー ピカチュウ】_1080p30.mp4`
2. `2_【ピカブイ】ピカチュウを怒らせると...【ポケモンレッツゴー ピカチュウ】_1080p30.mp4`
3. `3_【ピカブイ】ピカチュウとのハイタッチ！【ポケモンレッツゴー ピカチュウ】_1080p30.mp4`
4. `5_【ピカブイ】ピカチュウのあまえる【ポケモンレッツゴー ピカチュウ】_1080p30.mp4`

### Source of Truth

この文書の基本的な根拠優先順位は以下です。

1. 添付MP4そのもの
2. MP4から抽出して確認したframe / timestamp
3. このチャットで既に行った動画別分析
4. そこから導いた時系列推論
5. Grimo向け設計判断

Partner Eeveeについては、このチャット内ではMP4直接解析を行っていません。したがって**Eeveeの動きをPikachuの結果から補完しません**。Eevee固有のmotion anatomy / timing / gaze / ears / tail / touch propagationは、本資料では「未確認」です。

### Evidence Classification

- **[V1] Direct Video Observation** — 実際のframe / 映像から直接確認
- **[V2] Temporal Inference** — 隣接frameや時間関係からかなり強く推定
- **[I] Inference** — 観察結果からの解釈
- **[G] Grimo Recommendation** — Grimoへ転用する設計判断

### Timing Precision

対象動画はすべて30fpsです。したがって1 frame ≈ 33.3 msです。  
この文書では、30fps映像から確認できる精度を超えた数値を断定しません。

また、「touchが起きたframe」と「ゲーム内部でinputが受理されたframe」は同一とは限りません。したがって、映像から確認した1–2 frame級のvisual acknowledgementを、そのまま内部input latency 33–66msと断定しません。

### Anatomical Left / Right

正面映像では解剖学的な左右を誤認しやすいため、必要に応じて `screen-left` / `screen-right` を使用します。内部rig上のL/Rを映像だけから断定しません。

### IP Boundary

この文書はPokémon固有animation asset・pose・exact motion・exact timingをコピーするための資料ではありません。

保存・転用する対象は、

- animation principle
- timing principle
- attention principle
- touch causality
- asynchronous motion
- reaction structure
- autonomy
- variation
- emotional continuity
- interaction grammar

です。

Grimoでそのまま複製しないものは、

- Pikachu固有pose
- exact performance
- exact timing sequence
- exact facial acting
- electric VFX等のspecies-specific signature
- copyrighted motion asset

です。

---

# 1. Executive Findings

## 1.1 Interactionは一発のtriggerではなく、時間積分される

**[V1/V2]** Video 1のpositive petとnegative interactionの両方で、contactが続くほどreactionが深くなる。

Positiveでは、

```text
continuous pet
→ small pleasure
→ partial settle
→ contact continues
→ deeper pleasure
→ larger whole-body delight
```

Negativeでは、

```text
contact
→ mild facial warning
→ warning hold
→ contact continues
→ full-body avoidance
```

が観察された。

**[I]** 「pointerdown → clip再生」ではなく、接触duration / trajectory / repetition / current stateを時間的に蓄積して評価しているように知覚されることが重要。

**[G]** Grimoでは `contactDuration`, `pathLength`, `velocity`, `reversalCount`, `recentRepetition` 等をcontinuous evidenceとして扱う。

---

## 1.2 過去のinteractionが次の通常状態を変える

**[V1]** Video 2ではnegative reaction終了後も、

- narrowed / slanted eyelid
- downturned mouth
- bodyは通常座位に近い

という**displeased idle**が数秒残る。

さらにmajor anger後、Partner Play再入場時に約12秒以上、Pikachuは正面へ戻らず背中〜側面を向いた状態を維持する。

**[I]** 見た目上は、

```text
touch
→ reaction
→ neutral reset
```

ではなく、

```text
touch
→ reaction
→ current affect changes
→ different baseline idle / orientation
```

に見える。

**[G]** clip終了とemotion終了を同一にしない。画面遷移でも感情状態をneutral resetしない。

---

## 1.3 キャラクターはユーザー入力より前から「欲求」を持っているように見える

**[V1]** Video 5冒頭では、cursorが出る前にPikachu自身が、

- eyelidを閉じる
- headを少しlower / forward
- mouthをsoftに変化
- closed-eye content hold
- second affectionate beat

を行う。

その後、Pikachuが甘えていたい状態であることを示すUIへ移る。

**[I]** 「ユーザーが触ったからaffectionが発生」ではなく、「先にaffection-seeking motiveが存在し、ユーザーがそれへ応答する」構図。

**[G]** `socialSeeking` のようなmotiveをemotionから分離する価値が高い。

---

## 1.4 生きている相棒はCharacter → Playerからinteractionを開始する

**[V1]** Video 3でPikachuはcursor contact前から片方の前脚を出し、約1秒以上その状態を保持してplayer responseを待つ。

```text
Pikachu offers
→ WAIT
→ player responds
→ Pikachu acknowledges
→ Pikachu offers next turn
```

**[I]** これはreactionではなくsocial turn-taking。

**[G]** Grimoには `INVITE_PREP → OFFER → WAIT_FOR_USER → CONTACT_ACK → NEXT_OFFER / COMPLETE` が必要。

---

## 1.5 Intentional stillnessは生命感の構成要素

**[V1]** 全身が常に動いているわけではない。

- Video 1のidleでは頭・胴体がほぼ固定でもtailだけ動く時間がある。
- blinkだけが起きる時間がある。
- Video 3のhigh-five WAITでは、social intentは強いのにbody motionは極めて小さい。
- Video 5のaffection-seekingも低振幅のface/head中心。

**[I]**

```text
Intent ≠ MotionAmplitude
```

である。

**[G]** 「全部を常時動かす」ではなく、「意味のあるchannelだけが必要な時に動く」設計にする。

---

## 1.6 Faceは全身motionより先に意味を伝えることがある

**[V1]** Video 1 / Video 2のnegative interactionでは、全身回避より先に、

- mouth downturn
- uncomfortable / displeased face
- eyelid change

が1秒以上維持される。

**[I]** 顔が低コストのwarningとして機能し、それが無視された後に身体がcommitする。

**[G]** Grimoのboundary responseは `facial warning → tolerance window → avoidance` と段階化する。

---

## 1.7 Emotionはactionより長い

**[V1]**

- Video 1: positive reaction後にpleased stateが残る。
- Video 2: body settle後もnegative faceが残る。
- Video 5: ≈102–105 sで数秒のcontent closed-eye afterglow。

**[I]**

```text
body settle ≠ emotion settle
```

**[G]** reaction peakの後にmoving hold / settle / afterglowを別phaseとして持つ。

---

## 1.8 大きなemotionにはanticipationがある

**[V1]** Video 2のmajor anger ≈47.8–49.55 sでは、

```text
forelimbs inward
→ head/body compression
→ ears spread
→ reverse upward
→ arms/body expansion
→ facial peak
→ electric VFX peak
```

の順。

VFXが先ではない。

**[G]** 大型reactionは `prepare → action → peak → follow-through → settle` を持たせる。VFXで演技を代替しない。

---

## 1.9 同じキャラクターでもbehavior familyごとにmotion leadが変わる

**[V1]**

- high-five: forelimb lead
- affection-seeking: face / eyelid / head lead
- negative warning: face lead
- major anger: forelimb + torso anticipation
- autonomous sway: eyelid/head → ears/body overlap

**[I]** character identityは「いつも同じ部位から動く」ことではなく、character-specificな**behavior-to-channel mapping**で成立する。

---

## 1.10 Pokémon側にも明瞭なrepetitionはある

**[V1/V2]** Video 1 / 5では、

```text
touch
→ eyes close
→ mouth opens/smile
→ musical / positive VFX
→ settle
```

という視覚的に非常に近いpositive familyが多数反復される。

同一clipかは映像だけから断定しないが、canned feelingが出る余地はある。

**[G]** Grimoでは単純なclip本数増加だけでなく、

- initial state
- reaction depth
- sub-channel variation
- player response timing
- afterglow
- current motive
- history

によってvariationを作る。

---

# 2. Video Corpus

| ID | Filename | Duration | FPS | Resolution | Main Behavior | Analysis Coverage |
|---|---|---:|---:|---|---|---|
| V01 | `1_【ピカブイ】ピカチュウとのふれあい【ポケモンレッツゴー ピカチュウ】_1080p30.mp4` | 253.300 s | 30.000 | 1920×1080 | petting / positive / negative / feeding / autonomous idle / touch interruption | 全編survey。重要区間5fps。14–17 / 29–32 / 63–66 / 146.6–148.8 / 186.3–187.3 / 192.8–195.6 / 224.1–227.1 sを高密度確認。164–223 sをidle重点解析 |
| V02 | `2_【ピカブイ】ピカチュウを怒らせると...【ポケモンレッツゴー ピカチュウ】_1080p30.mp4` | 129.3816 s | 30.000 | 1920×1080 | warning / avoidance / persistent displeasure / major anger / back-facing disengagement / recovery | 全編survey。重要区間5fps。13.8–17.8 / 24.4–28.0 / 31.8–35.4 / 47.8–49.6 / 58.0–60.4 / 67.0–69.4 / 74.0–76.4 sを30fps近傍確認 |
| V03 | `3_【ピカブイ】ピカチュウとのハイタッチ！【ポケモンレッツゴー ピカチュウ】_1080p30.mp4` | 190.8667 s | 30.000 | 1920×1080 | self-initiated high-five / wait / multi-turn reciprocity / completion reward | 全編3秒→1秒survey。19–32 sを10–15fps。invitation / contact / completionを30fps |
| V05 | `5_【ピカブイ】ピカチュウのあまえる【ポケモンレッツゴー ピカチュウ】_1080p30.mp4` | 153.333 s | 30.000 | 1920×1080 | autonomous affection-seeking / petting / satisfaction / attention / afterglow / feeding / gift / full-body autonomous action | 全編3秒survey。0–12 / 20–42 / 48–64 / 66–106 / 138–153 sを5fps。0–5 sを30fps、first head-petを10–30fps相当 |

### Codec / Frame Notes

- V01: H.264 / Opus 48 kHz stereo / 7,599 video frames
- V02: H.264 / AAC 44.1 kHz stereo / 約3,881 decoded frames
- V03: H.264 / Opus 48 kHz stereo
- V05: H.264 / Opus 48 kHz stereo / 4,600 frames

---

# 3. Timestamp / Scene Index

## 3.1 V01 — ふれあい

| Timestamp | Interaction / Behavior | Why Important |
|---|---|---|
| 0–4 s | Partner Play開始 | transition |
| ≈8.6–11.2 | positive head pet | positive local→whole-body reaction |
| ≈14.3–17+ | boundary / avoidance | facial warningが全身回避より先 |
| ≈18.6–21.4 | positive | pleasure reaction |
| ≈43.6–46.4 | positive | repeated family |
| ≈51.6–54.4 | positive | repeated family |
| ≈62.6–66.0 | positive escalation | small pleasure→larger delight |
| 67.6–70.4 | positive | repeated family |
| 74.6–77.4 | positive | repeated family |
| 85.6–88.4 | positive | repeated family |
| 89.6–92.4 | positive | repeated family |
| 93.6–96.4 | positive | repeated family |
| 102.1–104.0 | positive | repeated family |
| 109.6–112 | positive | repeated family |
| 113.1–115+ | positive | repeated family |
| 121.6–123.4 | positive | repeated family |
| 124.6–126.4 | positive | repeated family |
| 128.6–131.5 | large delight | full-body / forelimb expressive action |
| 134.6–137.4 | positive | pet reaction |
| ≈140 | feeding UI | mode transition |
| 145.6–148.8 | feeding | item contact→consume→delay→pleasure |
| 164–192 | neutral idle | low-energy living state |
| ≈172.8–173.8 | autonomous action | short bow/head action |
| 182–185 | tail-only / secondary | torso/head mostly quiet while tail changes |
| ≈186.73 | blink | ≈4 frames級 |
| 193.4–195.3 | autonomous sway | head/body/ears asymmetric action |
| 206–223 | long autonomous moving hold | eyes closed, slow head/ear/body motion |
| ≈224.8–226.7 | touch interruption / startle | autonomous stateからtouchでreaction |
| ≈229.9–231 | positive | positive touch |
| ≈233.4–235 | positive | positive touch |
| ≈240.4–242 | positive | positive touch |

## 3.2 V02 — 怒らせる

| Timestamp | Interaction / Behavior | Why Important |
|---|---|---|
| 8–13 s | initial positive head interaction | contrast baseline |
| 14–17.8 s | first discomfort→avoidance | warning→commitment |
| ≈18–24 s | repeated face contact | repeated negative reaction |
| 25.1–27.9+ s | persistent displeased face | emotion remains after body settles |
| 31.8–35.4 s | full avoidance | repeated family / recovery |
| 36–47 s | repeated contact | baseline remains variable/negative |
| 47.8–49.55 s | major anger / electric peak | anticipation→expansion→VFX |
| ≈49.6–53 s | Partner Play exit→re-entry | cross-scene continuity candidate |
| ≈54–67 s | prolonged back-facing state | social disengagement |
| 58.0–60.4 s | rear touch | head/eye acknowledgement while body remains away |
| 67.0–69.4 s | stronger rear reaction | full-body reorientation |
| 70–76 s | renewed front interaction | early recovery |
| ≈78–92 s | repeated positive | recovery / positive family |
| 94–100 s | neutral/positive transition | baseline repair |
| 100–122 s | low-energy living state | neutral idle |
| ≈122.6–126.3 s | autonomous eyes-closed sway | spontaneous behavior |
| 126.5–129.4 s | neutral recovery/end | terminal state |

## 3.3 V03 — ハイタッチ

| Timestamp | Interaction / Behavior | Why Important |
|---|---|---|
| 0–9 s | Partner Play entry | setup |
| 9–19 s | positive petting | pre-high-five context |
| ≈20.27 s | first paw offer begins | character initiative |
| ≈20.7–22.07 s | offer + WAIT | social waiting |
| ≈22.07 s | high-five #1 | immediate acknowledgement |
| ≈22.87–24.73 s | opposite paw offer + WAIT | reciprocal turn |
| ≈24.73 s | high-five #2 | second contact |
| ≈25.2–26.4 s | next offer | turn continuation |
| ≈26.4 s | high-five #3 | alternating chain |
| ≈26.8–28.0 s | next offer | alternating chain |
| ≈28.0 s | high-five #4 | alternating chain |
| ≈29–30.93 s | next offer | final observed turn |
| ≈30.93 s | high-five #5 | final contact |
| ≈31.77 s onward | completion heart/pleased reaction | hierarchical reward |
| 32–139 s | repeated petting | positive corpus |
| ≈140–155 s | feeding | other interaction |
| ≈156–164 s | gift / present event | non-petting behavior |
| 165–183 s | full-body interaction | larger acting |
| 183–190.87 s | quieter state | autonomous / end |

## 3.4 V05 — あまえる

| Timestamp | Interaction / Behavior | Why Important |
|---|---|---|
| ≈0.4–4.4 s | autonomous affection-seeking | motive before user input |
| ≈4.5–6.8 s | state text | system communicates current condition |
| ≈7 s | controls available | transition |
| ≈8.6–12.4 s | sustained forehead pet | desired touch still escalates gradually |
| ≈12–22 s | repeated head/face petting | positive family |
| ≈22.4–23.2 s | strong pleasure response | higher-intensity response |
| ≈23.4–31.6 s | side/forelimb contact | local feedback without full-body every time |
| ≈32.4–33.6 s | heart/deeper affection | distinct reward family |
| ≈35–37.2 s | positive musical reaction | repeated positive |
| ≈40–42 s | muzzle/face contact | touch zone example |
| ≈48–52 s | face contact + facial sequence | expression variation |
| ≈54–63 s | repeated lower-face/body contact | positive reactions |
| ≈66 s | strong positive response | reward |
| ≈67–77 s | low-energy head orientation | attention dwell/release candidate |
| ≈78–89 s | additional positive cycles | repeated family |
| ≈93–96 s | slow head orientation/tilt | attention candidate |
| ≈97–102 s | repeated positive→stronger reaction | accumulation |
| ≈102–105 s | long content afterglow | emotion > action duration |
| ≈105 s | feeding UI opens | transition |
| ≈111–121 s | feeding | other interaction |
| 123–128 s | transition | mode change |
| ≈129–136 s | gift/flower event | non-petting behavior |
| 138+ s | full-body companion screen | different framing |
| ≈143.6–144.6 s | short autonomous arm-opening action | large spontaneous action |
| 145–153 s | quiet full-body state | end idle |

---

# 4. Base Living State

## 4.1 Posture / Center of Mass

**[V1]** Neutral Pikachuのbaseはcompactでgrounded。forelimbsはtorso前方に小さく保持されることが多く、通常idleではroot / COMの大きな上下bounceは見えない。

**[V1]** large reaction時だけ、

- forward/down
- side lean
- upward expansion
- away orientation

などが明確になる。

**[I]** baseの低振幅がlarge actionのcontrastを作る。

---

## 4.2 Breathing

**[V1]** 30fps映像上で「周期的な全身scale」として目立つbreathingは確認されない。存在するとしても低振幅。

**[G]** Grimoで全身一律scale breathingを生命感の中心にしない。

---

## 4.3 Weight Shift

**[V1]** weight shiftは常時ではない。

- avoidance時にside/downへCOM commitment
- major anger時にcompression→expansion
- autonomous sway時にhead/bodyの重心変化
- back-facing disengagementではroot orientation自体が変化

が確認できる。

---

## 4.4 Head Micro-motion

**[V1]** headは毎秒動かない。

neutral idleでは長いholdを許容する。  
一方、

- autonomous bow
- slow orientation
- sway
- user attention candidate
- affection lean
- avoidance

では意味のある変化が入る。

---

## 4.5 Blink / Eyelids

**[V1]** Video 1の≈186.73 sで高速blinkを確認。

概ね、

- ≈186.700 open
- ≈186.733 close onset
- ≈186.767–.800 closed
- ≈186.833 reopening
- ≈186.867 open

で、約4 frames ≈133 ms級。

**[V1]** blinkはfixed periodic oscillatorのようには見えない。感情表現としての長いeye-closeはblinkとは別。

---

## 4.6 Gaze

独立pupil / iris trackingは4本を通して**明瞭に確認できない**。

**[V1/V2]** attentionは主に、

- head orientation
- eyelid state
- body orientation
- offer pose
- head turn-back
- delayed head release

で読める。

**[G]** Grimoでeye aimを実装してよいが、それを「Pikachu映像で明確に観測した事実」とは扱わない。

---

## 4.7 Ears

**[V1]**

- neutral / affection-seekingでは低activity
- avoidance / angerではlateral方向へ大きく変化
- autonomous swayではhead/bodyとphase差がある
- high-fiveでは主要channelではない

**[I]** earsはconstant decorationではなく、behavior-dependent amplifier。

---

## 4.8 Limbs

**[V1]** idle時のforelimbsはかなり静か。

そのため、

- high-five offer
- major anger anticipation
- large delight
- full-body autonomous action

でのarm movementが強く読める。

---

## 4.9 Tail / Secondary Structures

**[V1]** Video 1の182–185 sではhead/torsoが比較的静かなままtailだけが明確に位置を変える。

**[I]** tailは独立channelとして機能するがconstant wagではない。

---

## 4.10 Intentional Stillness

**[V1]** 意図的静止は複数sceneで確認できる。

- V01 neutral idle
- V03 high-five WAIT
- V05 affection-seeking moving hold
- V02 displeased idle
- V02 back-facing disengaged hold

**[I]** motionの少なさが「死んでいる」ことと同義ではない。pose / face / orientation / contextに意図があると、低motionでも高いagencyが成立する。

---

## 4.11 Channel Asynchrony

**[V1/V2]** 同時には動いていない例：

- tailが動くがhead/torsoはほぼ静止
- blinkのみ起きる
- warning faceは変わるがbodyはまだneutral
- high-fiveでは片forelimbのみ大きく動き、耳・bodyは抑制
- affection-seekingではface/head中心で耳・tailは低activity
- anger recoveryではbodyが戻ってもfaceがnegativeのまま
- rear touchではhead/eyeが振り返るがbody orientationはawayのまま

**核心:** correlated asynchrony。ランダムに全channelへoffsetを入れるのではなく、同じintent / affectの下で、必要な部位だけ異なるタイミングで動く。

---

# 5. Attention & Gaze Grammar

## 5.1 User / Camera Orientation

**[V1]** neutral / high-five時は正面orientationが多い。  
ただし常時userを見続けるわけではない。

## 5.2 Touch Location Attention

独立eye-only trackingは未確認。  
**[V2]** head orientationがcursor位置と時間的に相関する区間がV05 ≈67–77 s / ≈93–96 sにある。

## 5.3 Gaze Away / Social Disengagement

**[V1]** V02 major anger後、約54–67 sでPikachuは長時間背中〜側面を向ける。

これはattention grammarとして極めて重要。

```text
current relationship state
→ body orientation away
→ user touches
→ head / eye checks back
→ body does not immediately re-engage
```

## 5.4 Eye-only

**未確認。** pupil movementを確実に読める証拠なし。

## 5.5 Head-only / Partial Attention

**[V1]** V02 rear touch ≈58–60.4 sでbodyはawayのまま、head/eyeだけ部分的に振り返る。

## 5.6 Eyes → Head / Head → Eyes

30fps映像から確実に独立eye aimを読めないため、順序を断定しない。

## 5.7 Fixation / Dwell

**[V1/V2]** V05 head orientationはtarget change後もすぐcenterへ戻らず数秒保持する場面がある。

## 5.8 Release

**[V2]** `orient → dwell → release delay → center` に見える。pointer positionへhead angleを直接1:1 mappingしたようなsnapではない。

## 5.9 Anticipation

High-five WAITでは前脚presentation + front body orientationそのものが「あなたの番」を伝える。eye-only cueに依存していない。

## 5.10 Disengagement

**[V1]** 「見ない」「背中を向ける」こと自体がstate expression。

**[G]** Grimo gaze controllerには `lookAtPlayer` だけでなく、

- `avoidPlayer`
- `monitorPeripheral`
- `glanceThenRelease`

相当のpolicyが必要。

---

# 6. Facial Motion

## 6.1 Blink

高速blinkと、emotionによる長いeye-closeを分離して観察する必要がある。

## 6.2 Asymmetric Blink

明瞭な片目だけのblinkは今回の4本では未確認。

## 6.3 Eyelid Openness

最重要facial channelの一つ。

確認された変化：

- open attentive
- half-lidded / softened
- full close
- crescent-like pleased
- slanted / displeased
- squeeze-close during avoidance
- sharp open at anger peak

## 6.4 Eye Direction

独立方向は未確認。head/body orientationの寄与が大きい。

## 6.5 Mouth

複数の意味段階がある。

Positive:

```text
small neutral
→ tiny open
→ soft pleased open
→ broad happy open
```

Negative:

```text
neutral
→ downturn
→ protest / compressed
→ wide open at anger peak
```

## 6.6 Cheek / Muzzle

局所deformationの細部は映像解像度・cameraから十分に確定できない。semantic reactionとしてface/muzzle contactは確認。

## 6.7 Happy

- eyes close / crescent
- mouth opens
- body remains small or later expands depending intensity
- VFXは高強度時に付く

## 6.8 Anticipation

Major angerではface単独よりtorso/forelimb compressionと連動。

## 6.9 Surprise

Rear-touch large reaction / touch interruptionでwide eye / mouth openingを含む瞬間がある。

## 6.10 Confusion

明瞭に単独labelできるsceneは未確認。

## 6.11 Dislike

段階がある。

1. mouth downturn / uncomfortable
2. displeased eyelid
3. eyes squeeze + head withdrawal
4. torso/ear/limb commitment
5. major anger / social disengagement

## 6.12 Relaxation

V05 affection-seeking / content afterglowで、

```text
eyelid soften
→ eye close
→ soft mouth
→ low-amplitude head/body hold
```

が明瞭。

## 6.13 Recovery

faceとbodyが同時にneutralへ戻らない。

**[V1]** V02ではbodyが戻った後もnegative faceが残る。  
**[V1]** V05ではpositive peak後もclosed-eye contentが残る。

---

# 7. Touch Causality

## 7.1 General Positive Pattern

**[V1/V2]**

```text
input/contact
→ immediate visible acknowledgement or local feedback
→ reception/evaluation
→ facial response
→ head/body commitment if duration/intensity passes threshold
→ secondary appendage response
→ peak
→ moving hold
→ settle
→ content afterglow
```

## 7.2 General Negative Pattern

```text
contact
→ facial warning
→ tolerance window
→ contact persists
→ avoidance commitment
→ ears/forelimbs/torso overlap
→ peak / hold
→ body settle
→ displeased afterglow
→ possible disengagement if repetition continues
```

## 7.3 Motive-Driven Positive Pattern

V05:

```text
pre-existing affection-seeking state
→ user provides desired touch
→ initial reception
→ continued touch
→ deeper satisfaction
→ stronger feedback
→ content afterglow
```

## 7.4 Character-Initiated Interaction Pattern

V03:

```text
Pikachu initiates offer
→ exposes temporary touch target
→ WAIT
→ user contact
→ immediate acknowledgement
→ next offer / completion
```

---

## Touch Zone: Head / Forehead

**[V1]** V01 / V05でpositive sustained petting。

特徴：

- 初回contactで必ずmax responseではない
- durationによりpleasureが深くなる
- head/faceの意味変化が先
- larger delightはthreshold後

---

## Touch Zone: Face / Muzzle

**[V1]** positive sceneもnegative sceneも存在。

正確なinternal semantic zone boundaryは不明。

**重要:** 同じface周辺でもcurrent state / exact point / gesture / repetitionによって違うreactionに見える。

---

## Touch Zone: Side / Forelimb Region

**[V1]** V05 ≈23.4–31.6 s。

局所contact markerが出ても毎回full-body reactionへは行かない。

**[I]** contact detectionとemotional reactionを1:1に結び付けていないように見える。

---

## Touch Zone: Offered Forepaw

**[V1]** V03 high-five。

通常touch mapではなく、behaviorが生成する一時的interaction targetとして機能。

---

## Touch Zone: Rear / Back Side

**[V1]** V02 disengaged状態中のrear touch。

bodyをawayにしたままhead/eyeだけ部分的に反応する例と、後にfull-body reorientationする例がある。

---

## Disliked / Sensitive Zone

映像からexact semantic zone定義は不明。  
ただしV01/V02でface周辺の特定interactionがnegative progressionを起こしている。

**[G]** Grimoではzoneを明示的に持つが、Pikachuのinternal zone mapを推定してコピーしない。

---

# 8. High-Density Interaction Timelines

## 8.1 V01 — Boundary Escalation ≈14.3–17 s

| Time | Trigger / Input | Eyes | Face | Head | Ears | Body / COM | Limbs | Tail / Secondary | Interpretation |
|---|---|---|---|---|---|---|---|---|---|
| ≈14.3 | cursor face/muzzle付近 | open | neutral→change開始 | neutral | neutral | stable | stable | — | contact start candidate |
| ≈14.5–14.7 | contact継続 | open | mouth downturn / worried | large moveなし | large moveなし | base保持 | base保持 | — | **facial warning** |
| 14.7–15.7 | continuous | open / uncomfortable | warning持続 | largely still | largely still | largely still | largely still | — | tolerance window |
| ≈15.9 | contact continues | squeeze / close onset | negative | withdrawal begins | lateral change | COM shift begins | forelimbs inward begin | — | escalation |
| ≈16.0–16.3 | continues | closed | protest | head away | ears lateral | torso twist/lean | arms inward | — | full avoidance |
| ≈16.3–16.8 | reaction | closed | negative hold | bowed/withdrawn | displaced | moving hold | compressed | — | peak/follow-through |
| >16.8 | contact/reaction end | recovery | negative residue | gradual return | gradual return | settle | settle | — | no instant neutral |

---

## 8.2 V01 — Positive Cumulative Escalation ≈63–66 s

| Time | Trigger | Eyes | Face | Head | Ears | Body / COM | Limbs | Secondary | Interpretation |
|---|---|---|---|---|---|---|---|---|---|
| 63.0–63.3 | pet continues | closed | happy | stable | stable | stable | stable | — | already pleased |
| ≈63.4 | continuous | opens | transition | center | — | stable | — | — | phase transition |
| ≈63.47 | continuous | — | — | — | — | — | — | VFX begins | feedback |
| ≈63.8 | continuous | crescent | broad smile | slight lift | — | small response | — | — | pleasure peak 1 |
| ≈64.2–64.4 | continuous | half/open | near-neutral | near-neutral | — | near-neutral | — | — | partial settle |
| ≈64.63 | continuous | transition | transition | stable | stable | stable initially | stable | strong VFX/event | second escalation threshold |
| ≈64.9–65.1 | continuous | close | pleased | **bows** | begin spread | torso follows | stable→prepare | — | action |
| ≈65.0–65.4 | continuous | closed | pleased | bow/return | **lateral spread** | COM changes | — | — | overlap |
| ≈65.5–65.7 | continuous | pleased | broad smile | rises | wide | open posture | forelimbs lift | — | commitment |
| ≈65.8–66.0 | continuous | delighted | peak | open | open | whole-body peak | arms spread/up | — | major delight |

---

## 8.3 V01 — Feeding ≈146.6–148.8 s

| Time | Trigger | Observation | Interpretation |
|---|---|---|---|
| 146.6–147.0 | berry mouth前 | item held near mouth | approach |
| ≈147.0–147.3 | item contact/consume | mouth/action changes, item消費状態へ | ingestion |
| ≈147.3–148.1 | item gone | max celebrationはまだ出ない | evaluation / chew-like gap |
| ≈148.17 | post-consume | VFX / positive feedback begins | reward |
| ≈148.4+ | post-consume | happy eyelids + mouth + body | pleasure |

**[I]** item disappearanceとcelebrationを完全同時にしていない。

---

## 8.4 V01 — Autonomous Sway ≈193.3–195.3 s

| Time | Eyes / Face | Head | Ears | Torso | Interpretation |
|---|---|---|---|---|---|
| 193.30 | neutral/open | neutral | neutral | stable | pre-action |
| ≈193.37–.40 | closes | lean begins | near-neutral | micro | initiation |
| ≈193.47 | closed | turn/lean larger | one side lateralizes first | follows | overlap |
| 193.7–194.0 | relaxed closed | large side lean | splayed | follows | peak |
| 194.0–194.8 | closed | small oscillation | orientation changes | smaller oscillation | moving hold |
| ≈195.0 | half-lid | returns center | returning | settles | recovery |
| ≈195.2–.3 | open | neutral | neutral | neutral | complete |

---

## 8.5 V01 — Touch Interrupt ≈224.8–226.7 s

| Relative | Observation |
|---|---|
| T0 ≈224.80 | eyes abruptly wide, mouth opens |
| T+1–3f | head/body reaction starts |
| T+≈0.3–0.6s | head moves strongly side/down |
| T+≈0.4–0.9s | ears splay |
| T+≈0.8–1.4s | eyes close / narrowed expression |
| ≈226.4–226.7 | posture/face return toward neutral |

**[V1]** autonomous stateへのinput interruptionが視覚的に成立。

---

## 8.6 V02 — First Warning → Avoidance 13.8–17.8 s

| Time | Trigger | Eyes | Face | Head / Ears | Body | Interpretation |
|---|---|---|---|---|---|---|
| 13.8–14.3 | prior interaction | open | prior→neutral | neutral | stable | recovery |
| ≈14.4–14.7 | face contact continues | open | changes begin | mostly fixed | fixed | evaluation |
| **≈14.7–15.0** | continues | mostly open | clear mouth downturn | little movement | stable | **warning becomes semantic** |
| 15.0–16.4 | continues | uncomfortable | warning held | mostly held | nearly held | tolerance window |
| **≈16.47** | continues | stronger change | negative | head moves; ears spread | COM begins side/down | **avoidance commitment** |
| 16.53–16.9 | reaction | squeezed | negative | strong lean | forelimbs inward | reaction |
| 17.0–17.8 | reaction | closed | compressed | held away | moving hold | follow-through |

Facial warning→body commitmentまで約1.5秒以上。

---

## 8.7 V02 — Persistent Displeasure ≈24.4–28 s

**[V1]** ≈25.1 s以降、

- narrowed eyes
- inward-slanted upper eye contour
- downturned mouth
- body / feet / tailはほぼnormal pose

を保持。

**Key:** body still / face angry。

---

## 8.8 V02 — Repeated Avoidance 31.8–35.4 s

```text
face contact
→ ≈32.7 body commitment
→ eyes close
→ head leans
→ ears spread
→ forelimbs inward
→ torso follows
→ low pose hold
→ ≈35.3 body mostly returns
→ negative face persists
```

---

## 8.9 V02 — Major Anger 47.8–49.55 s

| Time | Eyes / Face | Head | Ears | Body / COM | Limbs | VFX | Interpretation |
|---:|---|---|---|---|---|---|---|
| 47.8–48.3 | displeased | stable | stable | touch state | normal | none | pre-escalation |
| ≈48.5 | negative | slight prepare | — | preparation | forelimbs inward | none | anticipation |
| ≈48.7 | eyes close | lowers | begin spread | compresses | inward | none | compression |
| ≈48.73–48.9 | closed | low | spread | deeper compression | held inward | none | energy storage |
| ≈49.0 | compressed | bottom | spread | minimum pose | prepared | none | reversal point |
| ≈49.07 | reopening | rises | — | reverses upward | begin opening | none | action |
| **≈49.10** | sharp open | up | expressive | body expands | arms expand | minimal | peak onset |
| ≈49.13 | mouth opens | up | expressive | expanded | open | beginning | facial peak |
| **≈49.17–49.20** | anger peak | up/open | strong | full expansion | open | strong electric VFX | effect peak |
| 49.2–49.53 | held | held | held | peak hold | held | strong | moving hold |

---

## 8.10 V02 — Back-Facing Disengagement ≈54–67 s

**[V1]** 再入場後、Pikachuは約12秒以上正面neutralに戻らず、背中〜側面orientation。

58秒付近のrear touch:

```text
body remains away
→ eyelid / eye activates
→ head partially turns back
→ displeased face
→ body does not immediately follow
```

**[I]** head attentionとsocial body orientationが分離。

---

## 8.11 V02 — Rear Touch → Larger Reorientation 67–69.4 s

```text
back-facing
→ head/face recognition
→ slight body preparation
→ ≈68.1–68.2 body commitment
→ ≈68.4–68.7 large turn / lift / arms out
→ ≈68.8+ front pose
```

感情labelはsurprise / protest / forced reorientation寄りに見えるが、**[V2]**であり断定しない。

---

## 8.12 V03 — Invitation Onset ≈19.4–20.9 s

| Time | Forelimb | Face | Body | Interpretation |
|---:|---|---|---|---|
| ≈19.4–19.9 | torso近く | happy→settle | stable | previous reaction |
| ≈20.0–20.2 | neutral | neutral/open | stable | transition |
| **≈20.27** | **screen-right paw leaves torso** | open | torso still | **initiative** |
| 20.3–20.5 | rises outward | restrained | almost still | presentation |
| **≈20.7** | offered position established | stable | stable | **WAIT begins** |

---

## 8.13 V03 — First Wait → Contact ≈20.7–22.4 s

WAIT:

```text
offered paw held
face stable
head stable
torso stable
player cursor approaches
```

Contact ≈22.07 s:

- ≈22.10: eyelid change / close — 約1 frame級
- ≈22.17: mouth / face change — 約3 frames級
- ≈22.2–22.4: forelimb retract + facial recovery
- ≈22.43: near-normal readable state

**[V1]** visual acknowledgementは1–2 frame級。ただし内部input latencyとは断定しない。

---

## 8.14 V03 — Turn Transition ≈22.4–23.4 s

```text
first high-five complete
→ short face response
→ recovery
→ ≈22.87 opposite paw begins offer
→ ≈23.2–23.3 new offer clearly established
```

成功animationを長く見せず、次のsocial turnへ素早く移る。

---

## 8.15 V03 — Multi-Turn High-Five Chain

Observed contacts:

| Turn | Contact Time | Offered Side |
|---:|---:|---|
| 1 | ≈22.07 s | screen-right |
| 2 | ≈24.73 s | screen-left |
| 3 | ≈26.40 s | screen-right |
| 4 | ≈28.0 s | screen-left |
| 5 | ≈30.93 s | screen-right |

構造：

```text
R offer → player responds → acknowledge
L offer → player responds → acknowledge
R offer → player responds → acknowledge
L offer → player responds → acknowledge
R offer → player responds
```

---

## 8.16 V03 — Completion ≈30.93–32.4 s

≈30.93 final contact。  
直後に即最大celebrationへは行かず、一度neutralに近いposeを経由。

≈31.77 s付近からheart系VFX。  
≈31.9 s以降、

- eyes closed
- soft pleased face
- slight head/body relaxation

へ。

```text
each contact → tiny acknowledgement
whole sequence completion → larger affection feedback
```

---

## 8.17 V05 — Autonomous Affection-Seeking ≈0.4–4.4 s

| Time | Eyes / Face | Head / Body | Interpretation |
|---:|---|---|---|
| 0.40–0.60 | open / neutral | normal | baseline |
| ≈0.67–0.73 | lids narrow, mouth begins changing | head slightly lower/forward | affection onset |
| ≈0.77–0.83 | eyes close | head lower | commitment |
| ≈0.8–1.3 | eyes closed, soft open mouth | small moving hold | comfort |
| ≈1.4 | crescent/pleased | subtle head/body shift | peak 1 |
| 1.4–2.6 | prolonged closed-eye smile | very low-amplitude hold | content moving hold |
| ≈2.7–3.1 | eyes reopen | partial release | variation/recovery |
| ≈3.3–4.0 | second closed-eye pleased beat | small body/forelimb participation | secondary affection beat |
| ≈4.1–4.4 | open / settling | neutralizing | transition |

---

## 8.18 V05 — First Pet Response ≈8.6–12.4 s

| Time | Input | Eyes / Face | Body | Interpretation |
|---:|---|---|---|---|
| 8.6–8.9 | forehead contact starts | open | stable | contact |
| 9.0–10.0 | continuous stroke | mostly open | tiny orientation change | reception/evaluation |
| ≈10.1 | continues | mouth opens | stable | pleasure onset |
| ≈10.2 | continues | eyes close | slight head softness | clear acceptance |
| 10.3–11.5 | continuous | content smile | moving hold | accumulated pleasure |
| **≈11.7** | continuous | transition | VFX starts | higher threshold |
| 11.9–12.2 | continuous | broad closed-eye smile | stronger body presence | delight peak |

---

## 8.19 V05 — Side / Forelimb Contact ≈23.4–31.6 s

**[V1]**

- repeated local contact markers
- full-body reaction does not happen every time
- occasional mouth surprise
- forelimb position changes
- short smile

**[I]** local contact acknowledgement and emotional response can be decoupled.

---

## 8.20 V05 — Deeper Affection ≈32.4–33.6 s

```text
heart / pink feedback begins
→ half-lid
→ eyes close
→ soft smile
→ broader smile
→ settle
```

Green musical positive familyとは感情質が違うように見えるが、internal conditionは不明。

---

## 8.21 V05 — Attention Orientation ≈67–77 s

**[V1/V2]**

- cursor moves around upper/side regions
- head orientation changes gradually
- no hard snap
- holds orientation
- does not immediately recenter
- releases over several seconds

独立pupil trackingは未確認。

---

## 8.22 V05 — Long Content Afterglow ≈102–105 s

大きなpositive reaction後、eyes closed / pleased faceを数秒維持。  
大きな新motionはほぼなし。

```text
reaction peak
≠
reaction end
```

---

## 8.23 V05 — Full-Body Autonomous Action ≈143.6–144.6 s

```text
neutral full-body pose
→ forelimbs open
→ mouth opens
→ both arms raised / body expands
→ brief peak
→ half-lidded transition
→ neutral
```

約1秒の短いlarge autonomous action。

---

# 9. Motion Anatomy

## 9.1 Primary Motion

behaviorごとにprimary channelが異なる。

| Behavior | Primary Lead |
|---|---|
| neutral living idle | root/body mostly stable; sparse micro channels |
| positive pet | face/head, then body if threshold crossed |
| boundary warning | face |
| avoidance | head → torso |
| major anger | forelimbs + torso anticipation |
| high-five | one forelimb |
| affection-seeking | eyelids / mouth / head |
| autonomous sway | eyelid/head → ears/body overlap |
| disengagement | root/body orientation |
| rear acknowledgement | head/face while body stays away |

---

## 9.2 Secondary Motion

- ears: strong amplifier in avoidance/anger, low in affection/high-five
- tail: intermittent independent channel
- forelimbs: mostly quiet baseline, strong in offer / delight / anger
- VFX: follows or amplifies acting; should not be treated as primary body performance

---

## 9.3 Anticipation

Confirmed examples:

- major anger: inward/compress before outward explosion
- high-five: forepaw presentation before user contact
- affection-seeking: eyelid/head softening before interaction UI
- large delight: head bow / ear spread / torso commitment before peak

---

## 9.4 Overshoot

明瞭なjoint-level overshoot量は今回定量化していない。  
large reaction後のreturn / swayにはovershootに見える部分があるが、厳密なcurve measurementなしでは断定しない。

---

## 9.5 Follow-through

- head action後にears/torsoが遅れて付くscene
- anger compression→expansion後のheld peak
- autonomous swayでear orientationがhead/bodyとphase差
- large positiveでforelimbs / earsがprimary head/body actionへ重なる

---

## 9.6 Overlap

全channel同時startではない。

特にnegative sequence:

```text
face meaning
→ head commitment
→ torso
→ ears / forelimbs overlap
```

---

## 9.7 Moving Hold

頻出し、非常に重要。

- negative avoidance peak hold
- high-five offered paw WAIT
- affection-seeking closed-eye hold
- content afterglow
- long eyes-closed autonomous state
- back-facing disengagement

「peak poseをfreeze」ではなく、低振幅のliving channelが残る。

---

## 9.8 Settle

bodyとfaceが同時にsettleしない例が多い。

- body returns while face remains displeased
- action ends while content expression remains
- high-five micro-turn returns quickly to readable base, but sequence-level affection is delayed to completion

---

## 9.9 Grounding

neutral bodyは比較的stable。  
大きなreaction以外で全身が浮遊するようなconstant bounceは確認されない。

---

## 9.10 Weight

- avoidance: side/down
- anger: compress→expand
- affection: low-amplitude soften / lean
- high-five: base body remains stable while one forelimb acts
- disengagement: root orientation change carries social meaning

---

## 9.11 Inertia

physics simulationかhand-authoredかは不明。  
ただしvisual performance上、head/ear/bodyが常にrigid synchronousではなく、遅れ・重なり・holdがある。

---

# 10. Asynchrony & Propagation

## Pattern A — Negative Warning

```text
contact
→ mouth / eyelid meaning
→ warning hold
→ head withdrawal
→ torso / COM shift
→ ears / forelimbs overlap
→ moving hold
→ body settle
→ face remains negative
```

V01 / V02で反復。

---

## Pattern B — Positive Escalation

```text
continuous contact
→ small face response
→ partial settle
→ continued contact
→ head bow / eye close
→ ears / torso follow
→ forelimbs open
→ whole-body peak
→ content afterglow
```

V01 / V05。

---

## Pattern C — Autonomous Sway

```text
eyelid close
→ head lean
→ one ear orientation change
→ torso follows
→ oscillatory moving hold
→ half-lid recovery
→ open neutral
```

V01。

---

## Pattern D — Major Anger

```text
persistent irritation
→ forelimbs inward
→ head/torso compress
→ ears spread
→ reverse upward
→ arms/body open
→ face peak
→ electric VFX
```

V02。

---

## Pattern E — Social Disengagement

```text
anger history
→ scene re-entry
→ body orientation away
→ rear touch
→ head/eye acknowledges
→ body stays away
→ later stronger input
→ full-body reorientation
```

V02。

---

## Pattern F — High-Five Turn Taking

```text
character offer
→ hold
→ user contact
→ 1–2 frame級 visual acknowledgement
→ retract
→ opposite-side offer
→ hold
→ next user contact
```

V03。

---

## Pattern G — Affection-Seeking Motive

```text
no user input
→ eyelid soften
→ head lower/forward
→ eyes close
→ content moving hold
→ secondary affectionate beat
→ state communicated
→ user may respond
```

V05。

---

# 11. Emotion Grammar

## 11.1 Affection

**Face:** softened / closed eyelid, soft mouth  
**Gaze/Attention:** front/open body or gentle head orientation  
**Body:** low amplitude  
**Appendage:** ears mostly restrained  
**Timing:** can begin before user input  
**Recovery:** slow, soft  
**Afterglow:** long content hold possible

---

## 11.2 Happiness / Pleasure

**Face:** crescent/closed eyes, open smile  
**Body:** small initially; larger only after threshold  
**Appendage:** ears / forelimbs may join at higher intensity  
**Timing:** duration-dependent  
**Afterglow:** pleased expression remains

---

## 11.3 Curiosity

明確な単独curiosity labelは未確認。  
head attention candidate / partial turn-backは存在するが感情をcuriosityと断定しない。

---

## 11.4 Anticipation

- offered forepaw
- anger compression
- large delight preparation
- affection onset before user touch

---

## 11.5 Relaxation

- eyes closed
- soft mouth
- low body amplitude
- long moving hold
- reduced secondary activity

---

## 11.6 Surprise

- touch interruption
- some rear-touch response
- fast wide-eye / mouth opening

感情labelはsceneによってV2。

---

## 11.7 Confusion

未確認。

---

## 11.8 Mild Dislike

```text
mouth downturn
→ displeased eyelid
→ hold
```

bodyはまだneutral。

---

## 11.9 Anger / Protest

```text
repeated negative history
→ compressed anticipation
→ explosive expansion
→ strong face
→ species-specific VFX
```

その後にdisengagement。

---

## 11.10 Satisfaction

- desired pet
- high-five sequence completion
- feeding
- prolonged closed-eye content state

---

## 11.11 Excitement

large delight / full-body open action。  
通常positiveよりforelimb/body amplitudeが大きい。

---

# 12. Autonomous / Self-Initiated Behavior

## 12.1 Invitation

V03 high-five: character initiates forepaw offer。

## 12.2 Attention Seeking

V05 affection-seeking: no inputで甘えたい状態を表現。

## 12.3 Self-Expression

V02 displeased / back-facing state。  
user requestではなくcurrent affectを身体で提示しているように見える。

## 12.4 Idling Action

- V01 ≈172.8–173.8 bow/head
- V01 ≈193.4–195.3 sway
- V01 206–223 long eyes-closed action
- V02 ≈122.6–126.3 eyes-closed sway
- V05 ≈143.6–144.6 full-body arm-opening action

## 12.5 Rare Action

発生確率はこの映像群だけでは算出不能。  
ただしhigh-five / gift / presentなど通常petとは異なるinteraction familyが存在する。

## 12.6 Spontaneous Gaze

eye-only spontaneous gazeは未確認。head/body spontaneous orientation changeはあり。

## 12.7 Spontaneous Movement

多数確認。入力がない時もmedium/large behaviorが時折発生。

---

# 13. Variation & Repetition

## 13.1 Identical-Looking / Very Close Positive Reactions

V01:

20 / 45 / 53 / 69 / 76 / 87 / 91 / 95 / 103 / 111 / 114 / 123 / 126 / 234 / 241秒付近などに、視覚的に近いpositive family。

V05でも、

```text
touch
→ eyes close
→ mouth opens/smile
→ musical/positive VFX
→ settle
```

が多数。

**同一clipかは断定しない。**

---

## 13.2 Same Family, Different Intensity

Positive:

- local contact only
- small pleased face
- stronger musical feedback
- heart/deeper affection
- full-body delight

Negative:

- warning face
- avoidance
- persistent displeasure
- major anger
- social disengagement

---

## 13.3 Timing Variation

user interaction timingに依存するhigh-fiveは、same motion familyでもturn timingが変わる。

---

## 13.4 Amplitude Variation

same positive familyでもface-only → head/body → forelimb/full-bodyまで段階がある。

---

## 13.5 Initial-State Variation

同じtouch familyでも、

- neutral
- affection-seeking
- irritated
- disengaged
- post-positive

の初期状態で意味が変わる。

---

## 13.6 Expression Variation

- green musical positive
- pink-heart deeper affection
- closed-eye content
- open-mouth delight
- displeased mouth/eyelid
- angry peak

---

## 13.7 Afterglow Variation

positive / negativeとも残留。長さはsceneによって異なる。

---

## 13.8 Obvious Repetition

Pokémon側の弱点として、特にpositive pet reaction familyのcanned感は観察できる。

### Anti-RepetitionとしてGrimoが学ぶべきこと

**[G]**

1. clipを無限に増やすだけではなく、state差を使う
2. local / face / head / ear / body / secondaryをmodularに組み合わせる
3. recent reaction historyを保持する
4. same family連続使用を抑制する
5. contact durationでintensityを変える
6. user response timingをinteraction variationへ使う
7. current motiveに応じて同じtouchの意味を変える
8. afterglow / next idleもvariationの一部とする

---

# 14. Character-Specific Motion Personality

## Partner Pikachu Motion Personality Bible — この4本から観測できる範囲

| Attribute | Consolidated Observation |
|---|---|
| baseline energy | low–medium |
| resting posture | compact / grounded / front-limb close |
| motion amplitude | normal時小、peak時大 |
| preferred motion lead | behavior-dependent: face/head, forelimb, torso |
| tempo | micro responseは速い。large reactionはanticipationを持つ |
| gaze personality | eye-onlyは未確認。head/body orientationでsocial attentionを強く表現 |
| blink personality | fast blinkあり。emotion eye-closeとは別 |
| ear personality | constantではない。negative / large reactionで強いamplifier |
| tail personality | intermittent / independent。constant wagなし |
| asymmetry | one-paw offer, one-side ear lead, partial head turnなど明瞭 |
| reaction latency | high-five contactでvisual acknowledgement 1–2f級 |
| anticipation | strong in large anger; explicit in social offer |
| overshoot | exact定量未確認 |
| settle | bodyとfaceが非同期。emotionが遅れて解ける |
| stillness | high tolerance; socially meaningful |
| affection style | low-amplitude face/head softness; can self-initiate |
| curiosity style | 未確定。head orientation candidateのみ |
| dislike style | face warning → hold → avoidance → persistent mood |
| anger style | compress → explosive open + species-specific effect |
| autonomous invitation style | direct physical affordance presentation + WAIT |
| disengagement style | body orientation away; partial glance-back |
| satisfaction style | progressive; completion/afterglow |
| generic-looking forbidden pattern | constant full-body bounce / every touch=max smile / immediate neutral reset |

---

# 15. What Creates the Sense of Life

## Tier 1 — Essential

### 1. Internal continuity

Past input changes current baseline.

### 2. Character-originated motive

The character appears to want something before the user acts.

### 3. Character → User initiative

Invitation / offer / wait.

### 4. Time-integrated touch causality

Continuous contact changes reaction depth.

### 5. Independent / asynchronous channels

Not all parts move together.

### 6. Intentional stillness

Strong intent can coexist with low motion.

### 7. Emotional afterglow

Reaction outcome persists after action ends.

---

## Tier 2 — Major Amplifier

### 8. Facial warning before expensive body reaction

Boundaries feel communicative.

### 9. Body orientation as social language

Turning away is stronger than extra facial noise.

### 10. Anticipation before large reaction

Emotion appears generated by a body.

### 11. Turn-taking

Interaction becomes a conversation rather than trigger/reward.

### 12. Reward hierarchy

Micro contact gets micro feedback; completed interaction gets larger feedback.

### 13. State-dependent base poses

neutral / content / displeased / disengaged / relaxed differ.

---

## Tier 3 — Polish

### 14. Ear / tail delayed secondary response

Amplifies but does not create core causality alone.

### 15. VFX / musical feedback

Useful after body acting, not instead of it.

### 16. Small timing variation

Adds polish after state/causality are correct.

---

# 16. Failure / Weakness Analysis

## 16.1 Positive Reaction Repetition

**[V1/V2]** Similar positive family appears many times.  
Risk: canned reaction recognition after repeated play.

## 16.2 VFX Reliance Risk

Some strong positive / anger moments are heavily reinforced by VFX.  
However major anger clearly has body anticipation first.

**[G]** Grimo acceptance should include “VFX offでもactingが成立するか”。

## 16.3 Gaze Evidence is Weak

Pikachu’s large black-eye design makes eye-only tracking difficult to verify.  
Do not overclaim sophisticated procedural gaze from footage.

## 16.4 Some Emotional Labels are Ambiguous

Rear-touch large reaction ≈68 sなど、surprise / protest / reorientationのexact labelは不明。

## 16.5 Clip Identity is Unknown

Visually similar motionが同一clipか別clipかは映像から断定不能。

## 16.6 Major Anger Natural Settle is Missing

V02 ≈49.5 s付近でPartner Playを抜けるため、peak後の自然settle全長を観察できない。

## 16.7 Exact Local Deformation is Hard to Read

cheek / muzzle / skin-level deformationはcamera / resolutionから定量化困難。

## 16.8 No Strong Evidence of Floating / Clipping / Mechanical Snap

今回重点解析した区間では、明確な重大clippingや常時floatは主要問題として確認されなかった。  
一方、repetitionの方が明瞭な弱点。

---

# 17. Transferable Principles for Grimo

## Principle 1 — Continuous Evidence

```text
Observed:
touch duration changes response intensity
↓
Why it feels alive:
the character appears to evaluate an ongoing experience
↓
Abstract principle:
input is a stream, not a discrete trigger
↓
Grimo:
continuous gesture accumulator
```

## Principle 2 — Boundary as Communication

```text
Observed:
face warns before full avoidance
↓
Why:
character communicates a preference before escalating
↓
Abstract:
small reversible warning precedes large reaction
↓
Grimo:
warning → tolerance window → avoidance
```

## Principle 3 — Persistent Affect

```text
Observed:
face / orientation remain changed after reaction
↓
Why:
past interaction appears to matter
↓
Abstract:
reaction writes back into baseline state
↓
Grimo:
affect state survives animation completion and page change
```

## Principle 4 — Social Orientation

```text
Observed:
angry Pikachu turns away
↓
Why:
character controls social availability
↓
Abstract:
attention can be withheld
↓
Grimo:
avoid-player / glance-back / re-engage policies
```

## Principle 5 — Character Initiative

```text
Observed:
Pikachu offers paw before user input
↓
Why:
character has agency
↓
Abstract:
some interactions start Character → User
↓
Grimo:
autonomous invitation behaviors
```

## Principle 6 — WAIT as Behavior

```text
Observed:
offered paw remains available ~1s+ while user responds
↓
Why:
creates social expectation
↓
Abstract:
waiting is an active state, not dead time
↓
Grimo:
first-class WAIT state with living micro channels
```

## Principle 7 — Turn Taking

```text
Observed:
alternate paw offers create multiple reciprocal turns
↓
Why:
interaction feels conversational
↓
Abstract:
reuse simple body vocabulary inside reciprocal protocol
↓
Grimo:
multi-turn interaction controller
```

## Principle 8 — Motive Before Input

```text
Observed:
affection-seeking begins before controls/input
↓
Why:
character appears to have independent inner life
↓
Abstract:
behavior can express current motive
↓
Grimo:
socialSeeking / playSeeking / restSeeking etc.
```

## Principle 9 — Emotion > Motion Duration

```text
Observed:
pleased / displeased state remains after action
↓
Why:
reaction feels like a state change
↓
Abstract:
action completion does not clear emotion
↓
Grimo:
moving hold + settle + afterglow
```

## Principle 10 — Behavior-Specific Channel Economy

```text
Observed:
high-five uses paw; affection uses face/head; anger uses torso/arms/ears
↓
Why:
motion remains readable and non-noisy
↓
Abstract:
not every channel participates in every behavior
↓
Grimo:
per-behavior activity budget
```

---

# 18. Carol Implications

Carolのidentity:

- attention-seeking + relaxed
- huge dream-cloud fleece
- tiny cream face
- large eyes
- brown ears
- hooves
- moon/star motifs
- calm / soft / grounded

Pikachuのposeそのものはコピーしない。因果grammarだけ再構成する。

## 18.1 Carol Living Idle

必要channel:

```text
hidden torso / COM
breath
eye L/R
eyelid L/R
head
ear L
ear R
front hoof L/R
fleece.front
fleece.side.L
fleece.side.R
fleece.top
moon/star secondary
```

ただし全channel同時稼働は禁止。

### Base Rule

- body / hooves: grounded, sparse
- eyelids: intermittent
- gaze/head: dwellを持つ
- ears: attention / affect-driven
- fleece: body movementから遅れて小さくsettle
- moon/star: rare / special only
- intentional stillness: valid behavior

---

## 18.2 Carol Positive Pet

**[G] Example starting timing — Pokémon実測値ではなくCarol向け初期設計値**

```text
T0
cheek/head contact

0–80 ms
local cheek / local fleece acknowledgement

50–150 ms
eyelid softness

80–220 ms
attention toward contact

120–320 ms
head begins lean

180–450 ms
one ear relaxes before the other

250–700 ms
hidden torso makes small grounded transfer

300–900 ms
nearest fleece cluster follows

700–1600 ms
mass settles

1.5–4 s
content afterglow
```

この数値はGrimo Recommendationであり、Pikachu実測値ではない。

---

## 18.3 Carol Continuous Pet Escalation

```text
comfortAccumulator
```

を持たせる。

例:

```text
0–0.5s
acknowledge

0.5–1.5s
soft eyelid / tiny lean

1.5–3s
deeper lean + ear relax

3s+
rare "melt into touch" candidate
```

毎0.x秒で同じhappy clipを再発火する方式は禁止。

---

## 18.4 Carol Boundary

### Level 1 — Subtle Warning

```text
touch disliked/sensitive region
→ eye acknowledgement
→ one eyelid tightens
→ near ear rotates away
→ tiny mouth uncertainty
→ body remains grounded
```

### Level 2 — Avoidance

```text
continued contact
→ head turns away
→ cheek withdraws
→ ears change asymmetrically
→ hidden torso shifts weight
→ nearest fleece cluster follows
→ hooves remain heavy
```

### Level 3 — Displeased Afterglow

```text
face mildly displeased
ear still slightly back
gaze avoids user
head offset remains
```

### Level 4 — Social Disengagement

```text
look away
→ slowly rotate body partly away
→ face sinks slightly into fleece
→ one ear still monitors player
→ long stillness
```

攻撃的にしないが、明確な主体と境界を持たせる。

---

## 18.5 Carol Cross-Screen Persistence

```text
character scene unmount
≠
emotion reset
```

displeasedで別画面へ移った場合、

```text
re-enter
→ initially not looking at player
→ notices arrival after short delay
→ decides whether to orient
```

のようにする。

---

## 18.6 Carol Autonomous Invitation

Pikachuのhigh-fiveをコピーせず、

```text
neutral/content state
→ brief look toward player
→ tiny head lift
→ one ear forward
→ cheek/head shifts to accessible side
→ local fleece settles
→ WAIT
```

で「ここ、撫でて？」を表現。

---

## 18.7 Carol WAIT State

```text
head/cheek remains offered
body remains grounded
one ear monitors
eyes occasionally blink
breathing remains tiny
fleece does not continuously wobble
```

WAITはanimation clipが終わるまでの時間ではなく、user responseでexitするbehavior state。

---

## 18.8 Carol Reciprocal Continuation

成功後、

```text
cheek invitation
→ successful pet
→ soft content reaction
→ tiny pause
→ one of:
   A. other cheek slightly presented
   B. forehead lowers
   C. tiny hoof moves closer
   D. interaction ends satisfied
```

Pikachuの左右paw chainの表面をコピーせず、turn-taking grammarだけ使う。

---

## 18.9 Carol `socialSeeking`

P0 parameter candidate:

```text
socialSeeking
comfort
trust
arousal
```

例:

```text
socialSeeking high
arousal low–medium
comfort high
→ "want affection"
```

### Autonomous affection expression

```text
neutral living idle
→ eyes seek player briefly
→ head lowers slightly
→ one ear turns toward user
→ cheek rotates accessible
→ front fleece compresses locally
→ eyes soften / partly close
→ tiny head lean
→ WAIT
```

---

## 18.10 Carol User Responds / Ignores

Responds:

```text
contact
→ local cheek/fleece acknowledgement
→ eyelid softness
→ head accepts touch
→ socialSeeking decreases
→ comfort rises
→ deeper lean
→ fleece delayed settle
```

Ignored:

```text
WAIT
→ tiny glance
→ small puzzled / hopeful variation
→ slow withdraw
→ normal idle
```

No guilt / punishment.

---

# 19. Jill Implications

Jill:

- attention-seeking + energetic
- chest / upper-body lead
- wings
- leaves
- flowers
- heavy tail

## Translation

### Positive

```text
local acknowledgement
→ chest/upper-body commits
→ head/face
→ wing intent
→ leaves/flowers delayed
→ heavy tail last
```

### Boundary

```text
face/chest stiffness
→ gaze/face warning
→ partial wing closure/opening
→ body shift
→ leaves follow
→ tail anchors
```

### Social Seeking

Pikachu paw / Carol cheekをコピーしない。

```text
chest forward
→ brief excited upper-body lift
→ one wing / forelimb presents invitation
→ WAIT
```

### Secondary Rule

wing / leaf / flowerを常時動かさない。  
tailは猫のようなfast wagではなくheavy / rooted。

---

# 20. Pino Implications

Pino:

- energetic + independent
- soft water-bag body
- arms
- delayed heavy tail
- restrained water / bubble motifs

## Translation

### Positive

```text
arms/body local response
→ soft body compression
→ face
→ body rebound
→ heavy tail delayed
```

### Boundary

```text
arms protect inward
→ body compresses
→ head/face away
→ turns side
→ thick tail follows late
```

### Social Seeking

```text
body approaches
→ arms half-open / hesitant
→ small pause
→ WAIT
```

independent性を保ち、常にplayerへ依存する演技にしない。

### Effects

water / bubble motifはVFX spamにせず、special peakだけ。

---

# 21. Shushu Implications

Shushu:

- relaxed + independent
- plush body
- grounded seated weight
- ears
- flowers
- bouquet
- delayed plush settle

## Translation

### Positive

```text
eyes/head soften
→ plush torso sinks slightly
→ small ear bounce
→ bouquet/flowers settle last
```

### Boundary

```text
eyes/head away
→ plush body sinks
→ ears lower
→ bouquet pulled closer
→ flowers settle
```

### Social Seeking

```text
quiet look
→ head tilt
→ bouquet / hand area subtly presented
→ WAIT
```

Carolよりさらに控えめ。

---

# 22. Runtime Requirements Derived from Video

以下は4本の映像から直接必要性が導かれたruntime機能。

## 22.1 Independent Animation Channels

最低:

```text
COM/root
torso
head
eyelid L/R
face
ear L
ear R
forelimbs
tail
character secondary
```

Grimo側ではgaze / fleece / wing / flower等を追加。

---

## 22.2 Continuous Gesture Integrator

```text
contactDuration
pathLength
velocity
reversalCount
zoneHistory
sameZoneDuration
recentRepetition
```

をframe-by-frame更新。

---

## 22.3 Reaction Phase Model

```text
ACKNOWLEDGE
→ EVALUATE
→ COMMIT
→ PEAK
→ MOVING_HOLD
→ SETTLE
→ AFTERGLOW
```

---

## 22.4 Escalation

reaction中でもcontinued inputに応じてdeeper stateへ進める。

```text
current reaction
+ continued evidence
→ stronger reaction
```

---

## 22.5 Progressive Boundary

```text
warning
→ tolerance window
→ avoidance
→ persistent displeasure
→ optional disengagement
```

---

## 22.6 Persistent Affect

```text
valence-like state
irritation
comfort
socialSeeking
disengagement
```

等をclip終了でresetしない。

---

## 22.7 Cross-Scene Persistence

UI component / scene remountでcharacter stateを破棄しない。

---

## 22.8 State-Dependent Base Poses / Policies

最低候補:

```text
neutral
content
displeased
disengaged
relaxed
social-seeking
```

---

## 22.9 Attention Refusal

```text
lookAtPlayer
avoidPlayer
monitorPeripheral
glanceThenRelease
```

相当。

---

## 22.10 Reaction Layering

```text
persistent baseline face/state
+
temporary event reaction
```

を合成可能にする。

---

## 22.11 Invitation State Machine

```text
IDLE
→ INVITE_PREP
→ OFFER
→ WAIT_FOR_USER
→ CONTACT_ACK
→ CONTINUE?
   ├─ NEXT_OFFER
   └─ COMPLETE
→ AFTERGLOW
```

---

## 22.12 Dynamic Interaction Target

behaviorにより一時的なtouch targetを生成。

```ts
interface ActiveOffer {
  sourceBehavior: string;
  targetZone: SemanticZone;
  validGestures: Gesture[];
  startedAt: number;
  accepted: boolean;
}
```

---

## 22.13 WAIT as First-Class State

`offer.glb`の終端で自動retractするのではなく、

- offer anticipation
- hold pose
- living micro layers
- user-driven exit

に分ける。

---

## 22.14 Turn Controller

```text
turnIndex
expectedZone
userResponseTime
interactionMomentum
cancelReason
completionLevel
```

---

## 22.15 Social Motive Layer

emotionとは別に、

```text
socialSeeking
playSeeking
foodInterest
restSeeking
curiosity
```

等を持つ余地。

今回直接強く根拠があるのは特に `socialSeeking`。

---

## 22.16 Motive Satisfaction

interaction outcomeがmotive / affectへfeedbackする。

```text
socialSeeking decreases
comfort increases
contentAfterglow increases
```

---

## 22.17 Attention Dwell / Release

```text
notice
→ orient
→ dwell
→ release delay
→ return
```

pointer positionへhead angleを直結しない。

---

## 22.18 Immediate Local / Visual Acknowledgement

V03 high-fiveでcontact後1–2 frame級のvisible acknowledgement。

Grimoでもtouch feedbackをbehavior planner完了まで待たせない。

---

## 22.19 Secondary Delay

secondary structuresはprimary motionに従う。  
原因なしに常時jiggleさせない。

---

## 22.20 Recent Behavior History / Repetition Suppression

same reaction familyの連続選択を抑える。

---

## 22.21 Per-Character Timing / Channel Policy

shared runtimeは可。  
motion personalityは共有しない。

---

# 23. Motion / Behavior Production Backlog

## P0 — Carol Vertical Slice

### Existence / Living State

1. Living Idle
2. persistent affect
3. social motive state
4. autonomous `want_affection`
5. WAIT / moving hold
6. state-dependent base pose / expression

### Touch

7. cheek pet
8. head pet
9. continuous-contact accumulation
10. local-first acknowledgement
11. afterglow
12. contact interruption of autonomous behavior

### Agency

13. autonomous invitation
14. offered semantic touch zone
15. user-response timeout
16. reciprocal second turn
17. interaction completion reward

### Boundary

18. warning
19. avoidance
20. displeased idle
21. disengagement
22. recovery
23. cross-screen emotional persistence

### Animation Architecture

24. independent face/head/ear/body/fleece channels
25. moving hold support
26. soft/hard behavior interruption
27. VFX-off acting gate

---

## P1

- large delight ×3 variants
- warning variation ×3
- avoidance variation ×3
- autonomous head/ear curiosity
- relaxed eyes-closed moving hold
- glance-back reaction
- turn-away transition
- re-engagement transition
- feeding: notice → orient → bite → chew/evaluate → react
- repeated-pet satiation
- state-dependent blink / ears
- mild protest vocal
- interaction timeout variation
- multi-turn invitation variants
- completion afterglow variants

---

## P2

- rare invitation
- moon/star special interaction
- self-groom equivalent
- environment-look behaviors
- long quiet companionship states
- relationship-dependent recovery speed
- long-term preferred-boundary learning
- rare reconciliation behavior
- autonomous return-to-player invitation
- richer gift / memory behavior

---

# 24. Quantitative Observations

## Video Metadata

| Video | Duration | FPS | Frames / Notes |
|---|---:|---:|---|
| V01 | 253.300 s | 30 | 7,599 frames |
| V02 | 129.3816 s | 30 | ≈3,881 decoded frames |
| V03 | 190.8667 s | 30 | — |
| V05 | 153.333 s | 30 | 4,600 frames |

## 30fps Frame Unit

1 frame ≈ 33.3 ms.

## Blink

V01 ≈186.73 s:

- close→open cycle ≈4 frames級
- ≈133 ms級

## First Negative Warning → Body Commitment

V02:

- facial warning clearly readable ≈14.7–15.0 s
- body avoidance commitment ≈16.47 s
- warning lead ≈1.5 s以上

V01でも同様にfacial warningが全身avoidanceより先。

## Positive Escalation

V01 ≈63–66 s:

- first pleased peak around ≈63.8 s
- partial settle ≈64.2–64.4 s
- second escalation event ≈64.63 s
- body/head large reaction ≈64.9–66.0 s

## Major Anger

V02:

- anticipation visible ≈48.5 s
- deepest compression ≈49.0 s
- expansion onset ≈49.07–49.10 s
- strong VFX ≈49.17–49.20 s

## Back-Facing Disengagement

V02:

- ≈54–67 s
- 約12秒以上

## High-Five Invitation Wait

V03:

- first offer established ≈20.7 s
- first contact ≈22.07 s
- wait ≈1.3 s以上

## High-Five Contact Visual Acknowledgement

V03:

- contact ≈22.07 s
- eyelid change ≈22.10 s
- 1–2 frame級のvisible response

内部input latencyとは断定しない。

## High-Five Turns

Approx contacts:

- #1 ≈22.07
- #2 ≈24.73
- #3 ≈26.40
- #4 ≈28.0
- #5 ≈30.93

## High-Five Completion Reward

- final contact ≈30.93 s
- larger heart/affection feedback begins ≈31.77 s

## Autonomous Affection-Seeking

V05:

- onset ≈0.67–0.83 s
- first content hold ≈0.8–2.6 s
- second affectionate beat ≈3.3–4.0 s
- total sequence ≈0.4–4.4 s

## First Pet During Affection State

V05:

- contact begins ≈8.6–8.9 s
- clear pleasure onset ≈10.1–10.2 s
- stronger feedback ≈11.7 s
- delight peak ≈11.9–12.2 s

## Long Positive Afterglow

V05 ≈102–105 s: several seconds of content closed-eye hold.

## Neutral Idle Major-Action Cadence Example

V01 164–223 sの約59秒で、明瞭なlarger self-initiated action startはおおよそ、

- ≈173 s
- ≈193.4 s
- ≈206 s

の3群。

単純平均ではmajor action startは約20秒に1回に近いが、その間にもblink / tail / micro-motionがあるため、**「20秒完全静止」ではない**。

---

# 25. Open Questions / Missing Evidence

以下はこの4本だけでは判断不能。

1. Partner Eeveeの直接motion anatomy。
2. Eeveeのear/tail/neck-fur timing。
3. Eeveeのtouch causalityとPikachuとの差。
4. Pikachuの独立eye / pupil trackingの実装・量。
5. exact semantic touch zone map。
6. cursor表示と内部contact判定の完全な対応。
7. cheek / muzzle等のlocal deformation量。
8. visually similar reactionsが同一clipか別variantか。
9. ear / tail secondaryがhand-authoredかsimulationか。
10. long eyes-closed autonomous behaviorが単一clipかlayered systemか。
11. reaction selection algorithm。
12. internal emotion/state representationがcontinuousかdiscreteか。
13. irritation thresholdが回数・duration・zoneのどれで決まるか。
14. major anger ≈49 sの正確な発生条件。
15. major angerの自然settle全長。
16. back-facing re-entryがanger専用か複数entry variantの一つか。
17. rear-touch ≈68 sの正確な感情label。
18. anger / displeasureが長時間画面外でどの程度persistするか。
19. high-fiveの発生条件。
20. high-fiveのbond / relationship条件。
21. high-five offerのmaximum wait time。
22. high-fiveを無視した時のbehavior。
23. high-five途中で別zoneを触った時のinterrupt behavior。
24. high-five chainが常に5回か今回だけか。
25. left/right high-five順序が固定か。
26. high-five final reward condition。
27. `あまえる` stateの内部発生条件。
28. `あまえる` とbond / recent interaction / time contextの関係。
29. affection-seekingを無視した場合のbehaviour。
30. affection-seeking中に別interactionをした場合のmotive transition。
31. pink-heart positiveとgreen musical positiveの内部条件。
32. feeding時のattention / chewing / swallowの詳細timing。
33. audio peakのPikachu vocal / contact SE / VFX SEの分離。
34. exact head/eye procedural tracking方式。
35. rare autonomous behaviorの確率分布。
36. autonomous actionのcooldown / repetition suppression方式。

### 追加動画として価値が高いもの

1. **Partner Eeveeの長時間Partner Play** — neutral idle / pet / negative / autonomousを同一個体で確認
2. **Eevee high-five / invitation** — Pikachuとのspecies difference
3. **Eevee dislike / anger / avoidance** — boundary grammar比較
4. **無入力30–60秒以上の連続capture** — action frequency / blink / gaze / stillness測定
5. **同一zoneへ同一gestureを10回以上連続** — variation / saturation / repetition suppression
6. **invitationを意図的に無視するcapture** — timeout / disappointment / recovery
7. **anger後に長時間放置→再入場** — emotional persistence decay
8. **feeding close-up high-density capture** — notice / bite / consume / evaluate / pleasure
9. **cursorをゆっくり左右へ移動するattention test** — eye-only vs head tracking
10. **左右別zoneへ同じtouch** — lateral asymmetry / local causality

**未解決証拠項目数: 36**

---

# 26. Final Character Motion Rules

## DO

- 部位ごとにindependent activity budgetを持つ。
- 大きなmotionより先に小さなfacial acknowledgementを使う。
- touchをcontinuous evidenceとして評価する。
- positive / negativeともreaction depthを段階化する。
- moving holdを正式なbehavior phaseにする。
- reaction後のemotionを数秒残す。
- character自身からinteractionを始める。
- user responseを本当に待つ。
- current motiveを身体で表現する。
- same touchでもcurrent affect / motive / historyで意味を変える。
- userを見ない / bodyをそむけることもattention grammarとして許容する。
- body settleとface settleを分離する。
- major reactionにはanticipationを入れる。
- secondary structuresはprimary motionから遅れて反応させる。
- stateをscreen transition後も必要に応じて保持する。
- micro rewardとinteraction completion rewardを分ける。
- repeated reaction familyにはhistory-based suppressionを入れる。

## DO NOT

- 一枚絵をwhole-image scale / squash / bounceして生命感としない。
- 全身を常時同周期で動かさない。
- blinkを固定intervalにしない。
- ear / tail / fleeceをrandom noiseで常時揺らさない。
- touch瞬間に毎回full-body happyへ飛ばない。
- disliked touchを即座に最大angerへ飛ばさない。
- reaction終了と同時にneutralへsnapしない。
- page remountでemotionを強制neutral resetしない。
- 常にuserを凝視させない。
- every contactで最大VFXを出さない。
- VFXでbody acting不足を隠さない。
- same animationを4 Grimoへ単純retargetしない。
- Pikachu固有のpose / electric anger / exact timingをコピーしない。

## Core Motion Rules

1. **Low baseline, high contrast.**
2. **Behavior-specific motion lead.**
3. **Correlated asynchrony, not random asynchrony.**
4. **Primary motion first; secondary follows.**
5. **Intentional stillness is valid animation.**
6. **Moving hold is not dead pause.**
7. **Body and face may settle at different times.**
8. **Large reaction = anticipation → action → peak → hold → settle → afterglow.**

## Core Interaction Rules

1. `input`ではなく`continuous interaction evidence`を読む。
2. `character motive`をinput以前に持てる。
3. `Character → User` interactionを持つ。
4. OFFER / WAIT / ACK / CONTINUE / COMPLETEを別stateにする。
5. local acknowledgementをbehavior planner完了まで待たせない。
6. repeated touchはhistoryを持つ。
7. userが止めた場合と続けた場合でboundary pathを分ける。
8. completion outcomeを次のbaselineへ書き戻す。

## Core Attention Rules

1. eye-only trackingを必須前提にしない。
2. head / body orientation自体をattention languageとして使う。
3. orient後にdwellを持つ。
4. releaseを遅らせる。
5. userを見ないことも合法。
6. body away + head glance-backのようなpartial attentionを許容。
7. offered interaction中は余計なmotionでtarget readabilityを壊さない。

## Core Emotion Rules

1. emotionはanimation clipではなく持続stateとして扱う。
2. mild warning → avoidance → displeased idle → disengagementを段階化する。
3. positiveもacknowledge → pleasure → deeper satisfactionへ段階化する。
4. motiveとemotionを分離する。
5. desired interactionでも即max happinessにしない。
6. positive / negative afterglowを持たせる。
7. character-specific body languageでemotionを表現する。
8. Carol / Jill / Pino / Shushuへはcause / grammarだけ共有し、最終motionは共有しない。

---

# Final Consolidated Model

4本の映像から確認されたPartner Pikachuのexperience architectureを、最も短く表すと以下です。

```text
Persistent Affect
        +
Current Social Motive
        +
Attention / Orientation
        +
Current Behavior
        +
Recent Interaction History
        ↓
Character may act first
        ↓
User may respond, ignore, repeat, or interrupt
        ↓
Immediate local / facial acknowledgement
        ↓
Time-integrated evaluation
        ↓
Character-specific body commitment
        ↓
Secondary follow-through
        ↓
Moving hold
        ↓
Settle
        ↓
Afterglow
        ↓
New living baseline
```

この4本から得られた最重要原理は、

> **Partner Pikachuは「入力が来た時だけanimationを再生するキャラクター」ではなく、映像上、入力前から気分・欲求・注意・姿勢を持ち、ユーザーとのやり取りの結果を次の状態へ残し、自分からinteractionを始め、時にはユーザーを見ない存在として演出されている。**

Grimoで再現すべきなのはPikachuのmotionそのものではなく、この**継続する身体的因果と社会的interaction grammar**である。
