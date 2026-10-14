# Grimo Experience / Motion Bible

**Filename:** `GRIMO_EXPERIENCE_MOTION_BIBLE.md`  
**Status:** Authoritative production specification  
**Version:** 1.0 — Final Synthesis  
**Date:** 2026-09-14  
**Scope:** Carol / Jill / Pino / Shushu character experience, motion, interaction, runtime behavior, production gates, QA

> **North-star statement**  
> Grimoは「たくさん動くキャラクター」ではない。注意・意図・身体因果・感情・余韻・自発性を持ち、ユーザーの行為を身体で受け取り、自分からも関係を始める「そこに存在している相棒」である。

---

## 0. Bible Authority & Purpose

### 0.1 Purpose

本Bibleは、今後の以下すべてに対する最上位character experience specificationである。

- Blender modeling / lookdev / rigging / facial setup
- animation authoring / secondary motion
- semantic touch / interaction implementation
- behavior runtime / PlayCanvas integration
- Codex task specification / AI production routing
- animation review / regression / QA
- Carol Vertical Slice / Human Gate
- Jill / Pino / Shushuへの展開

本書の役割は「研究の要約」ではなく、**何を作り、どう動かし、何を禁止し、どう合否判定するかを一意にすること**である。

### 0.2 Formal input sources

本書は次だけを正式入力とする。

1. `GRIMO_TECHNOLOGY_AGNOSTIC_MINIMUM_REQUIREMENTS.md`
2. `Grimo Character Production Architecture — Zero-Based Deep Research.md`
3. `Grimo「生きている相棒」体験設計 — Partner Pikachu / Eevee の感動を分解し、四匹へ再構成する.md`
4. `GRIMO_PARTNER_PIKACHU_VIDEO_MOTION_ANALYSIS.md`（提供ファイル名は `(1)` suffix）
5. `GRIMO_PARTNER_EEVEE_VIDEO_MOTION_ANALYSIS.md`（提供ファイル名は `(1)` suffix）
6. `assets/grimo/source/carol/carol-Identity-canonical.png`
7. `jill-canonical.png`
8. `pino-canonical.png`
9. `shushu-canonical.png`

新規Web調査・一般知識による穴埋めは行っていない。

### 0.3 Authority hierarchy

| Domain | Highest authority | Rule |
|---|---|---|
| Product / quality requirement | Minimum Requirements | 他資料が低いquality barを許しても採用しない |
| Visual identity | 4 canonical images | 3D/model/rig/expressionより常に優先 |
| Observable Pikachu/Eevee motion | Direct Video Analysis | 実映像で確認できることを最優先 |
| Attachment / interaction principles | Experience Research + video verification | 原理のみ抽出し、Pokémon固有演技は複製しない |
| Technical implementation | Production Architecture | experience requirementを満たす範囲で採用・修正 |
| Final acceptance | Human Gate | 自動metricは補助証拠。最終合否は人間 |

### 0.4 Evidence labels

- **[A]** Primary / official evidence retained from source research
- **[B]** Strong secondary / academic / developer interview evidence retained from source research
- **[V1]** Direct video observation
- **[V2]** Temporal inference from adjacent frames / audio / sequence
- **[I]** Inference from evidence
- **[G]** Grimo design / production decision

数値は必ず「映像実測」「研究上の外部基準」「Grimo tuning target」を区別する。

### 0.5 Terminology

- **Living idle:** 入力がなくても、内部状態・注意・微小行動・静止の意図が読める状態。
- **Moving hold:** ポーズ/感情を保持しつつ、ごく小さい生理・注意・secondaryだけが残る状態。
- **Afterglow:** primary action終了後も感情・視線・姿勢・次行動確率に残る短期状態。
- **Local acknowledgement:** 接触された部位が、全身reactionより先に「届いた」と読める応答。
- **Behavior family:** 同じ意味/目的を持つ反応群。複数performance variantを持つ。
- **Performance variant:** 同じ因果を保ったまま、timing / side / face / appendage / settle等を変えた演技差分。
- **Intentional stillness:** schedulerが明示的に選ぶ「大きく動かない」行動。
- **Identity envelope:** canonical identityを壊さない facial / gaze / deformation / pose の許容範囲。

### 0.6 Conflict Ledger — adopted decisions

| Conflict | Evidence | Adopted decision | Reason |
|---|---|---|---|
| 「常時micro-behavior」 vs 「長い静止」 | Requirementsはalive without inputを要求。Pikachu/Eevee映像は長いmoving hold / quiet stateを示す [V1] | **常時“状態は生きる”。常時“全身を動かす”は禁止。** | 生命感はevent densityではなく、意図・状態・非同期channelで成立 |
| Production Architecture旧記述ではcanonical未視認 | 旧research環境の制約。今回4枚を実視認 | **旧制約をsupersede。4枚をvisual authorityとしてbody grammarを再裁定** | 現在の入力条件では視覚確認が可能 |
| Experience Researchのeye→head推奨 vs videoでeye-only gazeの証拠が弱い | Direct videoではfine pupil tracking未確認 | **Grimoにはeye aimを実装するが、Pokémon実測事実として扱わない** | capabilityとして有効だがevidenceを誇張しない |
| 過去資料の初期timing range vs video measured timing | 例：Pika/Eevee high-fiveの1–2f級visible ACK、単一blink約133ms等 [V1] | **実測値はreference evidence、Grimo値はtuning envelope。exact timingをコピーしない** | Pokémon固有performanceの複製を避け、偽精密性も避ける |
| Technology-agnostic requirement vs full-3D recommendation | Requirementsは研究前のtechnology neutrality。Architecture researchはfull 3D + web-nativeを総合1位 | **Carol Gate A–Hを通る限り full 3D + Blender + PlayCanvas をproduction baseline** | 研究終了後の具体決定として整合。Gate失敗時はhybridへ戻す |
| Negative Pokémon reaction vs positive-only care philosophy | Videoではanger/disengagementあり。Requirementsはpunishment禁止 | **Grimoはhint→mild refusal→withdrawalまで。攻撃・罪悪感・neglect punishmentは禁止** | agency/boundaryは残し、retention punishmentは採用しない |
| Physical correctness vs appeal | Requirementsはgrounded causality、Architectureはappeal > simulation purity | **重さ・因果はauthored actingで守り、physicsは小さい残差に限定** | 正しい物理より「その子らしい身体説得力」が目的 |
| Character sharing vs scalability | Shared runtimeは必要、同じanimation retargetは禁止 | **共有するのはsemantic/runtime contract。motion performanceはcharacter-specific** | 4匹の人格差を守りながら長期保守可能 |

---

# 1. North Star

## 1.1 Product experience

優先順位は固定する。

1. **Cuteness / appeal**
2. **Healing / comfort**
3. **Attachment**
4. **Fun**
5. **Surprise**
6. **Collection**

中心命題：

> **TaskをするためにGrimoを見るのではなく、Grimoに会いたいために戻り、その結果task completionにも意味が生まれる。**

典型sessionは約30秒〜5分。最短30秒でも「存在」を感じ、5分触ってもcanned reactionの羅列に崩れないこと。

## 1.2 Experience quality equation

Source researchの統合モデルをproduction用に圧縮する。

```text
Living Companion Quality ≈
Identity Fidelity
× Causal Responsiveness
× Attention / Intent Readability
× Temporal Layering
× Agency
× Behavioral Variability
× Continuity of Internal State
× Character Specificity
```

以下は乗算的な失敗要因として扱う。

```text
Generic Motion
+ Latency
+ Repetition
+ Off-model Deformation
+ Root-dominant / Floaty Motion
+ VFX Dependence
+ Personality Retargeting
```

**品質投資順:** identity → causality → agency → timing → variation → rendering polish. [G]

---

# 2. What Makes a Character Feel Alive

## 2.1 Final causal model

最低モデルを次に更新する。

```text
persistent state / motive
+ environment / user presence
+ recent history
        ↓
perception
        ↓
attention allocation
        ↓
evaluation / intent
        ↓
local acknowledgement OR anticipation
        ↓
primary bodily commitment
        ↓
facial / social meaning
        ↓
secondary follow-through
        ↓
peak / moving hold
        ↓
settle
        ↓
emotional afterglow
        ↓
state + history update
        ↓
next autonomous / intentional-stillness state
```

Touchでは「local acknowledgement」が早く、large autonomous actionでは「anticipation」が先に来る。順序は**behavior-specific**であり、一つの万能eyes→head→body規則にはしない。

## 2.2 Essential — 生命感の必要条件

1. **Canonical identity continuity** — neutralで本人である。
2. **Bodily causality** — 触れた場所・起きた出来事と動きの因果が読める。
3. **Attention state** — 見る、見ない、待つ、逸らすが意味を持つ。
4. **Internal continuity** — reaction終了で心が消えない。
5. **Selective asynchronous channels** — 必要な部位だけが異なる位相で動く。
6. **Grounded support / COM** — rootが浮かない。支持点と重さがある。
7. **Intentional stillness** — 静かな時間をschedulerが許す。
8. **Interruptibility** — 現状を無視してcanned clip完走しない。
9. **Agency** — Character → Userで始まる行動が存在する。
10. **Boundaries** — 何をしても喜ぶ人形にしない。

## 2.3 Amplifiers — 愛着を強めるもの

- social turn-taking / WAIT
- motive before input (`socialSeeking`, curiosity, rest etc.)
- staged anticipation
- moving hold / afterglow
- delayed character-originated payoff
- state-dependent base pose
- side-specific touch response
- rare but context-readable behavior
- feeding / gift / toyのstaged interaction
- audio / optional haptic coherence
- persistent relationship memory

## 2.4 Polish — 最後に効くもの

- small timing variation
- micro asymmetry
- secondary residual dynamics
- restrained VFX
- subtle vocal/foley variation
- lighting/material polish

**PolishでEssentialの欠陥を隠してはいけない。**

---

# 3. Motion Philosophy

## 3.1 Motion must have cause

各motionは最低どれか一つに属する。

```text
physiology / posture maintenance
stochastic but state-bounded micro event
internal-state driven
environment / attention driven
user / event driven
social-motive driven
```

原因不明のwiggleを「生命感」と呼ばない。

## 3.2 Local before global — when touch supplies the cause

Touch reactionでは原則、

```text
contacted local region
→ face / attention
→ head / torso commitment
→ appendage / secondary
```

とする。large surprise等、局所より先に全身startleが必要なbehaviorは例外。

## 3.3 Correlated asynchrony

非同期とはrandom offsetではない。同一intentの下で、部位ごとに役割とphaseが違う状態である。

- faceが評価する
- headが遅れてcommitする
- near appendageが意味を増幅する
- heavy structureは最後に追従する
- support limbは動かないこともある

## 3.4 Moving holds

peak後にすぐneutralへ戻さない。hold中は、

- eyelid / gazeの微調整
- tiny breath
- ear single-side correction
- secondary settle

だけでもよい。**holdはactionの残骸ではなく演技の一部。**

## 3.5 Intentional stillness

`intentional_stillness` を正式behavior候補にする。

- calm/relaxedほど長く取れる
- excitement中は短くなる
- invitation WAITでは静止がsocial pressureを作る
- disengagementでは「見ない」静止が強い表現になる

## 3.6 Grounded weight

- COM移動には支持点の変化を伴わせる
- fore/hind limbはroot bounceの飾りにしない
- tail / fleece / flowersはrootより先に原因なく動かさない
- seated characterは座面/臀部/尾/足の支持感を明瞭にする

## 3.7 Anticipation / follow-through / settle

Large actionは原則、

```text
prepare / compress / orient
→ commit
→ peak
→ follow-through / optional overshoot
→ moving hold
→ settle
→ afterglow
```

VFX peakはbody actingの後または同時。VFX先行で感情を代替しない。

## 3.8 Context sensitivity

同じtouchでも、

- current behavior
- emotion/arousal
- attention target
- recent history
- repetition pressure
- motive
- side / direction / speed / duration

で反応を変える。

## 3.9 Repetition suppression

**原因は予測可能、performanceは部分的に予測不能**を維持する。

同じgestureを繰り返してもreaction familyは意味的に一貫し、pose・face・side・settle・afterglowは変化し得る。

---

# 4. Never Do

以下は全Grimo共通の禁止事項。Human Gateで一つでも重大違反があればFAIL。

1. completed single image全体をscale / squash / stretch / rotate / warpして生命感を作る。
2. 全body channelが同時に同方向へbobbingする。
3. generic breathingをwhole-body periodic scaleとして見せる。
4. 何かを常に動かし続ける「perpetual motion」。
5. user/cameraを永続注視する。
6. touch直後に意味のないfull-body happy clipへsnapする。
7. reaction後にneutralへsnap-backする。
8. 同一interactionへ毎回同一performanceを返す。
9. every appendage reacting equally / every peak using all channels。
10. support pointと無関係にCOM/rootが浮く。
11. motion without bodily / attentional / emotional cause。
12. excessive squash/stretchでcanonical体積・年齢感・柔らかさを壊す。
13. VFX / particles / musical symbolsでbody actingを置換する。
14. 4匹へ同一animationをretargetし、速度差だけで人格を作る。
15. fixed-period blink / ear / tail / head oscillators。
16. random noiseをsecondary motionと呼ぶ。
17. disliked touchを即最大angerへ飛ばす。
18. neglect punishment / guilt / hunger sickness penaltyでreturnを強制する。
19. pointer positionへhead/eyesを1:1でsnap mappingする。
20. reaction clip完走をuser inputより優先する。
21. body partが接触しているのにsemantic contact anchorが外れて見える。
22. physics solverにsilhouette / key pose / appealの最終決定を任せる。
23. canonicalにないphotoreal fur / hard PBR materialでvisual identityを再解釈する。
24. AI-generated facial / hero motionをHuman Gateなしで採用する。

---

# 5. Shared Sense-of-Life Stack

## 5.1 Channel stack

| Channel | Purpose | Cadence | Priority | Interruptibility | Dependencies / masking | Interaction |
|---|---|---|---|---|---|---|
| Base pose / support | anatomy・support・current stateの基準 | continuous state | critical | hard actionでblend | locomotor/seated grammar | 全channelの土台 |
| Posture / COM | weight・engagement・withdrawal | sparse | high | soft/hard | support limbsと整合 | large reaction / boundary |
| Breath | 微小生理 | near-continuous, tiny | low | suppressible at peaks | body mask、identity clamp | arousalで振幅調整 |
| Attention state | 誰/何に注意しているか | event/state driven | critical | immediate redirect可 | gaze/head/body orientation | touch/autonomyの意味を決定 |
| Gaze / eyes | fixation, glance, away | intermittent | high | high | attention state | headより先/後はcharacter/behavior依存 |
| Blink / eyelid | physiology + affect | event-like | medium | peakで抑制可 | emotion, gaze | blinkとexpression closeを分離 |
| Head / neck | orient, lean, social pose | sparse | high | high | gaze/intent, body limits | touch/attention/invitation |
| Facial | emotion evaluation/readability | event/state driven | critical | high | identity envelope | local touch / emotion / afterglow |
| Limb / social gesture | offer, protect, support, action | sparse | high | behavior-owned | COM/support | invitation / feeding / toy |
| Character appendage | ear/wing/tail etc. | state/event driven | medium-high | masked during hero phrase | primary intent | amplifier, not constant noise |
| Local touch reflex | “届いた”最初の身体反応 | immediate | critical | latest contact wins | semantic zone/side | behavior plannerを待たない |
| Autonomous action | self-initiated agency | low-frequency distribution | high | user input can interrupt | utility/context/history | invitation/curiosity/grooming |
| Primary action | authored meaning-bearing motion | episodic | critical | safe interrupt points | HFSM/action ownership | peak acting |
| Secondary follow-through | softness / inertia residual | cause-driven | medium | clipped/masked if conflicts | primary transforms | delayed small residual only |
| Afterglow | reaction結果の残留 | seconds | high | new major event can overwrite | emotion/history | next gaze/posture probability |
| Audio / haptic / VFX | multisensory reinforcement | event driven | supportive | follows body cue | primary event markers | never source of meaning alone |

## 5.2 Layer ownership

Hero behaviorが特定channelを所有中、random idle schedulerはそのchannelへ割り込まない。

例：Carol cheek lean中はhead/near ear/fleece-localをinteractionが所有。blinkは許可しても、random head-turnはmaskする。

## 5.3 Priority order

```text
safety / identity clamp
> immediate local touch reflex
> current user interaction
> authored hero behavior
> attention / face continuity
> posture / support
> autonomous behavior
> physiology micro
> cosmetic secondary / VFX
```

---

# 6. Attention & Gaze Bible

## 6.1 Shared principles

- **User fixation:** social event時に短時間。永続しない。
- **Input fixation:** contact pointを見る必要がある時だけ。fine eye trackingの誇示は禁止。
- **Anticipatory gaze:** invitation / feeding / toy / upcoming eventで使う。
- **Glance:** 短いnotice。すぐhead/bodyまでcommitしなくてよい。
- **Gaze away:** calm independence / curiosity / boundaryで重要。
- **Environmental interest:** user以外へ注意を配ることでautonomyを作る。
- **Eye → head:** quick noticeで有効。
- **Head → eye:** character-specific pose adjustmentやrelaxed reorientationで許可。
- **Disengagement:** gazeだけでなくhead/body orientationを使える。
- **Moving hold:** targetを見続けながらtiny correctionだけ残す。
- **Gaze release:** target消失後に即centerへsnapせず、短いdwell / release delayを持つ。

## 6.2 Gaze state model

```text
UNCOMMITTED
→ NOTICE
→ FIXATE / GLANCE
→ optional HEAD_ORIENT
→ DWELL
→ RELEASE_DELAY
→ RETURN / NEW_TARGET / DISENGAGE
```

Boundaryでは別branchを持つ。

```text
NOTICE_USER
→ AVOID_PLAYER
→ MONITOR_PERIPHERAL / GLANCE_BACK
→ optional REENGAGE
```

## 6.3 Character profiles

| Character | Gaze style |
|---|---|
| Carol | soft, longer dwell; attention-seekingだがrelaxed。目→headは穏やか。ignored invitationではhopeful glance→withdraw |
| Jill | quick notice, shorter dwell, more frequent reorientation。chest/upper bodyもattentionに参加 |
| Pino | quick glance + deliberate look-awayが多い。independentなのでuser lockを短くする |
| Shushu | slow glance, long soft dwell, gaze-awayも自然。急なtrackingは最小 |

---

# 7. Blink / Eye / Facial Bible

## 7.1 Evidence-backed observations

- Partner Pikachu neutral blinkの一例：約4 frames ≈133 ms [V1, n=1]。
- Partner Eevee neutral blinkの一例：約4 frames ≈133 ms、full closure約2 frames ≈67 ms [V1, n=1]。
- これは**single examples**であり、Grimoの固定blink durationではない。
- emotion eye-closeはblinkと別channel/semanticとして扱う。
- Pikachu/Eevee映像からfine pupil saccadeの定量分布は確立していない。

## 7.2 Blink rules

- fixed interval禁止。
- refractory period + context modifierを持つ。
- social WAIT / surprise peak / contact peakでは抑制可能。
- relaxationではphysiological blinkと長いeye-closeを混同しない。
- asymmetric blinkはGrimoで使えるが、reference映像で強く確認された事実ではない。[G]

## 7.3 Facial system

Production Architectureに従いhybridを標準とする。

```text
eye aim            → joint/transform or safe shader offset
eyelids            → morph-centered
blink              → paired morph
asymmetric squint  → side morph
cheek / muzzle     → limited morph
mouth corner       → limited morph
jaw large-open     → joint + corrective morph if needed
head aim           → neck/head joints
```

自由なhuman face rigではなく、approved preset間のblendを中心にする。

## 7.4 Shared expression presets

最低concept：

- neutral
- curious
- content
- delighted
- anticipatory
- excited
- surprised
- confused
- mild-discomfort
- relaxed/sleepy
- satisfied

Characterごとにshapeと組合せは別。preset名だけ共有可能。

## 7.5 Identity preservation

- eye scale / spacing / highlight readabilityをcanonicalから逸脱させない。
- white-of-eye露出、mouth stretch、cheek deformationにcharacter-specific上限を持つ。
- expression transitionはsnap禁止。
- canonical neutral screenshotを毎hero expression QAの基準にする。

---

# 8. Touch Interaction Grammar

## 8.1 Input model

```text
zone
× gesture
× gestureDirection
× gestureSpeed
× contactSide
× localPosition
× currentBehavior
× attention
× emotion/arousal
× motive
× recentInteractionHistory
× repetitionPressure
→ reaction family
→ performance variant
```

最低gesture：

- `tap / poke`
- `slow pet`
- `continuous stroke`
- `back-and-forth pet`

内部分類として `hold` / `rapid repeated poke` を保持してよい。

## 8.2 Gesture accumulator

frame-by-frameで最低以下を蓄積する。

```text
contactDuration
pathLength
averageSpeed
peakSpeed
reversalCount
zoneHistory
sameZoneDuration
contactSide
entry / exit position
recentRepetition
```

## 8.3 Final reaction grammar

```text
RECOGNITION
→ LOCAL_ACK
→ ATTENTION / EVALUATION
→ optional ANTICIPATION
→ PRIMARY_RESPONSE
→ FACIAL_SOCIAL_MEANING
→ WHOLE_BODY_PROPAGATION if justified
→ SECONDARY_FOLLOW_THROUGH
→ PEAK / MOVING_HOLD
→ SETTLE
→ AFTERGLOW
→ STATE_UPDATE
```

Slow petはLOCAL_ACK後にaccumulation時間を持てる。Discrete social touchはACKを非常に速くする。

## 8.4 Positive contact-seeking

Eevee映像で「characterが自分の身体をcontactへ動かす」原理が確認される [V1]。Grimoでは、

```text
user touches
→ character accepts
→ character actively leans / compresses / presents
→ contact becomes bidirectional
```

をP0 Carolへ採用する。

## 8.5 Boundary grammar

```text
local acknowledgement
→ subtle hint
→ tolerance window
→ clear refusal
→ withdrawal / attention release
→ mild afterglow
→ recovery
```

hysteresisを持たせ、少しpointerが動いただけでhappyへ瞬時反転しない。

## 8.6 Dynamic interaction target

Invitation中はbody part自体がtemporary touch targetになれる。

```text
sourceBehavior
targetSemanticZone
validGestures
startedAt
timeoutPolicy
accepted
```

WAIT中もblink / tiny breath / one-ear monitor等は生きる。

---

# 9. Autonomy Bible

## 9.1 Required autonomous families

- spontaneous gaze / environmental interest
- body adjustment / weight shift
- self-grooming equivalent
- curiosity / inspect
- invitation to interact
- attention seeking
- autonomous emotion / mood phrase
- rare action / gift-like action
- intentional quiet
- disengagement / independent look-away

## 9.2 Utility + HFSM principle

「何をするか」はUtility-like selection、「どう最後まで演じるか」はHFSM / authored sequenceで管理する。[G]

Candidate scoreは概念的に、

```text
personality
+ current motive
+ affect fit
+ context fit
+ novelty
+ user presence
- repetition penalty
- interruption cost
- cooldown pressure
```

で決定する。

## 9.3 Event density rule

固定「20秒に一回」等は禁止。ReferenceではPikachu約59秒のneutral idle中にlarger autonomous startが約3群あった一方、その間にもblink/tail/micro eventsがあった [V1]。Eeveeでは20秒超のrelaxed moving holdもある [V1]。

したがって、

- micro event density
- small autonomous phrase density
- major autonomous event density
- quiet-state probability

を別distributionにする。

## 9.4 Invitation

Character → User interactionを必須にする。

```text
motive rises
→ orient / prepare
→ present affordance
→ WAIT
→ user responds / ignores / interrupts
→ character interprets outcome
→ settle / next turn / withdraw
```

ignored時にguiltを使わない。小さく引き上げ、normal lifeへ戻る。

---

# 10. Variation & Anti-Repetition Bible

## 10.1 Two-level variation

**Behavior family:** cause/meaningが安定。  
**Performance variant:** timing / side / gaze / expression / appendage / settle / afterglowが変わる。

## 10.2 Runtime memory

最低recent-history buffer：**5–8件程度をstarting target** [G]。ただし最終値はprototypeで調整。

保持候補：

```text
lastUsedAt
recentUseCount
similarityGroup
reactionFamily
performanceVariant
autonomousPhraseFamily
contactSide
recentEmotionOutcome
```

## 10.3 Selection policy

- hard cooldown：rare / hero behavior
- soft repetition penalty：common reaction
- similarity-group penalty：見た目が同じ別clipも抑制
- context weighting：current stateに意味が合うものを優先
- emotion weighting：valence/arousal/motiveと整合
- side conditioning：L/R contactをmacro poseまで保持
- delayed payoff：interaction後に別beatを入れてvariationを作れる

## 10.4 Interrupted recovery

中断後はneutralから再開しない。

```text
current pose + current affect + new input
→ safe redirect
→ new behavior
```

---

# 11. Emotion & Afterglow Bible

## 11.1 State representation

離散labelだけでなく、最低次の連続stateを併用する。

```text
valence
arousal
comfort
curiosity
socialSeeking
irritation / boundaryPressure
fatigue / restSeeking
engagement / disengagement
```

## 11.2 Shared emotion grammar

| Emotion | Face | Gaze | Posture | Amplitude / tempo | Appendage | Afterglow / decay |
|---|---|---|---|---|---|---|
| Neutral / calm | open-soft | intermittent | stable | low / slow | sparse | baselineへ自然遷移 |
| Affection | softened lids, small smile | user/contactへsoft dwell | slight approach | low–medium / slow | near appendage relaxes | 2–5s級starting envelope [G] |
| Happiness | brighter eyes/smile | userへ短いreturn | open posture | medium | selected appendage | content stateへ落ちる |
| Curiosity | eye/head asymmetry | glance→dwell | small forward intent | low–medium / irregular | one ear/wing/paw first | unresolved interestとして残る |
| Anticipation | restrained face | target fixation | compress / prepare | low then rising | lead appendage readies | actionへcommit |
| Excitement | wide/bright | rapid reorientation allowed | expanded | higher / faster | more channels recruited | short energetic residue |
| Surprise | fast eye/face change | stimulus | brief recoil/expand | fast | reactive asymmetry | quickly evaluate into another emotion |
| Confusion | small mouth/eyelid uncertainty | target↔user glance | head tilt / pause | low | one-side cue | curiosity or neutralへ |
| Mild dislike | tighten lids / small frown | user or contact initially | withdraw begins | low–medium | near appendage protects/turns away | boundary residue; no hostility |
| Relaxation | half/closed eyes | soft/away | sink / settle | very low / slow | droop/soften | long moving hold possible |
| Satisfaction | closed/soft eyes, settled smile | gaze can release | grounded content pose | low | secondary settles last | longer afterglow; next idle becomes content |

## 11.3 Positive-only care philosophy

禁止：affinity loss for absence, sickness/hunger punishment, confiscation, guilt notifications, aggressive punishment。

許可：preference, refusal, avoidance, mild protest, temporary disengagement, later recovery。

---

# 12. Secondary Motion Bible

## 12.1 Rule

> **Meaning-bearing motion is authored. Unpredictable residual is procedural/dynamic.**

## 12.2 Roles

| Type | Use | Do not use for |
|---|---|---|
| Authored | key arc, anticipation, emotional follow-through, silhouette | random life noise |
| Procedural | gaze, blink scheduler, safe micro offsets, target following | hero pose invention |
| Spring / dynamic | tiny residual lag of tuft/leaf/petal/tail tip | entire fleece/wing/body behavior |
| Hybrid | authored main deformation + small residual | unconstrained soft-body look |

## 12.3 Character rules

- **Carol:** main fleece silhouette stable; 2–4 large deformation controls authored; outer tuft groups small residual. Whole-fleece soft body = No-Go.
- **Jill:** wing arc / tail base / leaf-mane intention authored; leaf tips / flower heads small lag; heavy tail tip delayed, never cat-fast.
- **Pino:** body squish authored and identity-clamped; tail base authored, terminal chain small residual; water/bubbles are restrained event effects.
- **Shushu:** plush compression authored; crown/bouquet relationship maintained; flower/petal heads small lag only.

## 12.4 Priority

physical correctness < character appeal / readability, **but** grounded weight and cause remain mandatory.

---

# 13. Biped / Quadruped / Mixed Body Grammar

## 13.1 Upright / Biped Grammar — Pikachu-family biomechanical reference

Use for upright social gestures and forelimb-led acting, not for direct retarget.

- COM over feet / seated base; torso can carry emotion.
- face/upper body can communicate before lower body moves.
- forelimb presentation enables direct social turn-taking.
- large emotion may use compression→expansion.
- support limbs remain quiet to preserve gesture readability.
- settle returns through torso/feet before appendage residual ends.

## 13.2 Quadruped Grammar — Eevee-family biomechanical reference

- four-point / low support makes COM transfer and front/rear weight important.
- head/neck movement can propagate into shoulders/body.
- ears can act independently while feet remain planted.
- touch should preserve side and local body relationship.
- heavy tail follows body, not vice versa.
- low-body contact can become whole-body lean without losing grounding.

## 13.3 Seated Grammar

- seat / hindquarters are a support plane, not invisible floating root.
- arms/forelimbs gain social freedom because support is elsewhere.
- torso compression and rebound must read against seated support.
- feet/paws may remain forward as visual anchors.
- props held by hands must remain kinematically convincing.

## 13.4 Mixed / Character-Specific Grammar

Character may combine seated support with upright social gestures or quadruped rest transitions. Runtime grammar follows canonical anatomy, not Pokémon taxonomy.

### Adopted classification

| Character | Primary grammar | Secondary reference |
|---|---|---|
| Carol | **Quadruped / low grounded** | Eevee weight propagation + Pikachu face/social principles |
| Jill | **Seated mixed / upright-upper-body** | Pikachu torso/forelimb social grammar + heavy-tail follow-through principles |
| Pino | **Seated mixed** | Pikachu forelimb/social clarity + Eevee contact-seeking / tail lag |
| Shushu | **Grounded seated** | Pikachu upper-body social gesture + Eevee moving-hold / settle principles |

---

# 14. Carol Experience & Motion Bible

## 14.1 Identity — canonical non-negotiables

実視認した `assets/grimo/source/carol/carol-Identity-canonical.png` を唯一のvisual source of truthとする。

壊してはいけない特徴：

- 極端に大きい白〜淡い青紫の**dream-cloud fleece**が全体silhouetteの大半を占める。
- 小さなcream faceがfleeceへ埋め込まれるように見える。
- 非常に大きいbrown〜amber glossy eyes、星状highlights、柔らかい頬の赤み。
- brown ears、pink inner ear。左右へ低めに広がる。
- brown hoovesがfleece下から短く見える。足長化禁止。
- crescent moonとgold star motifs。cloud-like tufts / pale blue-violet shadow hierarchy。
- 幼く、丸く、安心感があり、硬い羊毛やrealistic sheep anatomyへ寄せない。
- neutral silhouetteは横長・低重心。fleeceがbodyを隠すこと自体がidentity。

## 14.2 Personality

**attention-seeking + relaxed**。

「構ってほしい」意思はあるが、興奮で押し付けない。ユーザーへ柔らかく空間を開き、待ち、触れられると体重を預ける。

## 14.3 Body Grammar

**Quadruped / low grounded**を採用。

- hidden torso / COMはfleece内にあるが、4 hoof supportを感じさせる。
- headはfleeceから独立してorient / leanできる。
- hoofは軽快に跳ねず、比較的heavy。
- face/headの小さい動きが主役。root motionは節約。
- fleeceはbodyそのものではなく、bodyに付随する巨大soft structure。全体を一塊で変形させない。

## 14.4 Motion Signature

| Dimension | Carol rule |
|---|---|
| motion lead | face / eyelid / head。touchではlocal cheek/fleece first |
| baseline energy | low–medium |
| amplitude | usually small; rare medium peak |
| tempo | slow, soft onset; no sluggish input ACK |
| weight | hooves / hidden torso grounded; fleece visually soft but not weightless |
| gaze | longer soft dwell; gentle glance-away |
| blink | soft; expression eye-closeは長くてもよい |
| head | small lean / lower / offer; sharp turnsを避ける |
| ears | subtle, asymmetric, attention-sensitive |
| limbs | minimal; forehoof can become rare social affordance |
| fleece | local→neighbor→global-small lag; cause-driven only |
| stillness | high tolerance; 8–25s-class relaxed moving hold可 [G] |
| settle | slow layered settle; fleece last |
| afterglow | long, warm, low-amplitude |

## 14.5 Living Idle Grammar — 15–30 s

固定loopではなく、次のbandを非同期合成する。

```text
continuous-ish: tiny breath / posture maintenance
intermittent: blink / eyelid change / eye glance
sparse: head correction / one-ear response
rarer: hoof micro-adjust / small weight transfer
rare: bounded autonomous affection / curiosity phrase
valid at all times: intentional stillness
```

**Example 20s session — sequenceではなくevent densityの例 [G]**

- 0–4s: content hold、tiny breath、one blink
- 4–8s: userへ短いglance、headは追わない
- 8–13s: quiet。one earだけsmall orientation
- 13–17s: tiny head lower、fleece local lag
- 17–20s: stillness + slow release

同じ秒配置を再生しない。

## 14.6 Attention Grammar

- attention-seeking時：eyes → tiny head lift → one ear forward → accessible cheek/forehead pose。
- relaxed時：soft user fixation後、gazeを外してもよい。
- pet中：contact sideへeye/headを寄せるが、eyesを閉じて「外界より触感へ注意」が移ることもある。
- ignored invitation：一度だけsmall glance、then slow withdraw。罪悪感表現禁止。
- mild dislike：最初はuser/contactを見る。withdrawalへ進むとgazeを外す。

## 14.7 Touch Zone Map [G]

指定資料にCarol固有の確定zone mapはないため、canonical anatomyとpersonalityから本Bibleで正式化する。Human Gateで必要ならrevisionする。

| Class | Semantic zones | Design intent |
|---|---|---|
| **Preferred** | forehead/head top, cheek.L/R, ear root.L/R | affection-seekingを最も読みやすくする |
| **Neutral** | front fleece, side fleece, upper back fleece | calm acknowledgement; every touchで大喜びしない |
| **Disliked / sensitive** | hooves/feet, hind-lower body under fleece, repeated rough poke near rear | grounded limb protection / personal boundary |
| **Special** | crescent moon anchor, large star motif anchors | rare magical recognition; low-frequency only |
| **Excluded** | eyeballs/iris, mouth interior, detached decorative particles/cloudlets | touch colliderを置かない |

## 14.8 Gesture × Zone Reaction Matrix

| Zone class | Tap / poke | Slow pet | Continuous stroke | Back-and-forth pet |
|---|---|---|---|---|
| Preferred | `notice_soft` / curious blink | `accept_lean` | `comfort_build` → deeper lean | `melt_into_touch` candidate; repetition saturationあり |
| Neutral | local fleece ack; small glance | mild content | relax if duration grows | may become preferred-like only if comfort high |
| Sensitive | local flinch / hoof protect | tolerate briefly | clear hint→withdraw | boundary pressure rises; mild disengage |
| Special | motif notices / gaze shift | no generic pet response | if held/slow: rare motif-affect branch | repeated rubbing does **not** spam VFX |
| Excluded | no semantic reaction | no reaction | no reaction | no reaction |

## 14.9 Positive Head / Cheek Pet Chain

Starting envelope [G], not Pokémon copied timing:

```text
0–80 ms      local cheek / local fleece acknowledgement
50–180 ms    eyelid / face softening
80–220 ms    attention toward contact
120–320 ms   head begins side-specific lean
180–450 ms   near ear relaxes; opposite ear may remain alert
250–700 ms   hidden torso makes tiny grounded transfer
300–900 ms   nearest fleece cluster follows
700–1600 ms  broader mass settles
1.5–5 s      content afterglow
```

Continuous pet uses `comfortAccumulator`; no repeated clip retrigger.

## 14.10 Self-Initiated Behaviors

P0/P1 candidates:

- `want_affection`: looks → cheek/forehead offer → WAIT
- `soft_check_in`: brief user glance → tiny head tilt → return
- `ear_monitor`: one ear responds while face stays relaxed
- `fleece_nestle`: face sinks a little into fleece, then looks out
- `quiet_content`: eyes soft/close, long hold
- `small_hoof_adjust`: support correction with local fleece lag

## 14.11 Affection Behaviors

- side-specific cheek lean
- forehead lower for pet
- gentle eye close + small smile
- post-pet delayed look-back
- rare deeper body commitment toward user
- second-turn offer: opposite cheek / forehead / low forehoof, never fixed sequence

## 14.12 Mild Dislike Behaviors

Four levels:

1. **Hint:** eyelid tighten, one ear away, tiny mouth uncertainty.
2. **Refusal:** head withdraws, cheek no longer offered, hoof protects.
3. **Withdrawal:** body partly rotates away, face sinks into fleece, one ear monitors.
4. **Residue:** mild gaze avoidance / ear offset / head offset for seconds.

No electric/anger analogue, no punishment, no dramatic sadness.

## 14.13 Feeding

Use staged temporal grammar:

```text
notice item
→ orient / sniff-like visual inspection
→ approach mouth
→ consume event
→ short evaluation / chew-like pause
→ face response
→ optional small head/body pleasure
→ fleece residual
→ afterglow
```

Reference footage supports consume→delight delay around 0.8–0.9s in Eevee and staged feeding in Pikachu [V1/V2]; Carol timing must be tuned independently.

## 14.14 Gift / Toy

- Carol may reveal / nudge / notice an item from the accessible front-fleece area only if prop relationship is physically readable [G].
- toy tracking uses eyes/head first; hoof use remains restrained.
- gift should be Character → User agency, not reward pop-up disconnected from body.
- rare moon/star accent may support discovery **after** bodily acting.

## 14.15 Rare Behaviors

- delayed affection after an interaction has already settled
- quiet moon/star recognition
- deeper cheek press
- rare forehoof offer / reciprocal touch ritual
- long dream-like eyes-closed moving hold

Rare = context/cooldown/history weighted, not pure low-probability RNG.

## 14.16 Secondary Motion — Dream-Cloud Fleece

### Structural policy

```text
stable main silhouette
+ authored large deformation controls
+ local fleece cluster controls
+ small residual tuft dynamics
```

### Causality

```text
head/body/hoof movement
→ nearest fleece cluster
→ adjacent cluster with smaller amplitude
→ outer tuft residual
→ settle
```

### Prohibitions

- whole-fleece sine wave
- global scale breathing
- endless jelly wobble
- all tufts moving in phase
- physics-driven silhouette loss
- moon/star decorations bouncing continuously

## 14.17 Sound / Haptic / VFX

- sound: soft nonverbal acknowledgement / content / tiny protest; body cue must read without sound.
- haptic: optional, light and event-specific; progressive enhancement only.
- VFX: moon/star only special or stronger affection beats. baseline sparkle spam禁止。
- final hero Carol may target broad short-vocal/foley coverage rather than dialogue; source research suggests 40–80 short units as a long-term production guide [G], not P0 requirement.

## 14.18 DO

- preserve tiny face vs huge fleece ratio.
- let cheek/head acting carry meaning before fleece.
- keep hooves heavy and sparse.
- use side-specific contact.
- allow long quiet, content states.
- make invitation gentle and patient.
- let fleece settle later than face/head.

## 14.19 DO NOT

- make Carol bounce like a cloud ball.
- turn fleece into soft-body simulation.
- constantly wiggle both ears.
- make moon/star effects the main emotion channel.
- use high-energy Eevee ear-dance or Pikachu paw chain directly.
- make all preferred touch immediately maximal happiness.

## 14.20 Carol Signature Rules — never share directly

1. **Face-in-fleece contrast:** tiny facial action leads a huge soft mass.
2. **Soft offering:** affection invitation is spatially opening a cheek/forehead, not energetic pawing.
3. **Hoof gravity:** feet stay heavier than the cloud-like surface.
4. **Fleece echo:** emotion propagates into fleece after the meaning is already readable.
5. **Dream accent restraint:** moon/star motifs are rare punctuation, never baseline activity.

---

# 15. Jill Experience & Motion Bible

## 15.1 Identity — canonical non-negotiables

`jill-canonical.png` visual authority:

- young spring-green dragon, round head/body, large glossy green eyes with star/flower-like highlights.
- cream muzzle/lower face and segmented cream belly.
- short forelegs; do **not** lengthen into generic dragon arms.
- pale yellow-green horns and broad wing membranes.
- dense leaf mane from head down the back, with white flowers and clover.
- very thick curved tail; visually rooted and heavy.
- bright, alive spring-plant motif; leaves/flowers are part of silhouette, not detached VFX.
- seated/mixed base in canonical: hindquarters grounded, forelegs free, wings open to sides.

## 15.2 Personality

**attention-seeking + energetic**。

Userへ向かう意思が早く、emotionは胸・上半身から外へ広がる。ただし「常時元気に跳ねる」ではない。quiet stateとのcontrastが必要。

## 15.3 Body Grammar

**Seated mixed / upright-upper-body**。

Canonical方向性を採用：

```text
chest / upper-body intent
→ head / face
→ wing
→ leaves / flowers
→ heavy curved tail last
```

このpropagationはbody grammarのsignature。毎behaviorで必ず全段を使う必要はない。

## 15.4 Motion Signature

| Dimension | Jill rule |
|---|---|
| motion lead | chest / upper torso; behaviorによりface or one wing |
| baseline energy | medium-high |
| amplitude | medium; rare high |
| tempo | quick onset, springy but grounded |
| weight | torso light-medium, tail heavy/rooted |
| gaze | quick notice, eager reorientation |
| blink | slightly quicker / more alert than Carol; no fixed interval |
| head | energetic tilt/lift; avoid constant bob |
| wings | authored social/emotion arcs; not flapping noise |
| forelegs | short, expressive accents |
| leaf mane | delayed secondary, not primary intent |
| tail | slow/heavy follow-through, low baseline movement |
| stillness | shorter than Carol but still valid |
| settle | chest settles first; leaf/flower/tail later |
| afterglow | bright, medium duration |

## 15.5 Living Idle Grammar

- stable seated support / hindquarters.
- tiny chest breath, not whole-body bounce.
- rapid small attention changes may occur, but user fixation is broken regularly.
- one wing can adjust independently; both wings never oscillate continuously.
- leaves/flowers move only after head/chest/wing cause or rare ambient authored phrase.
- tail may remain motionless for long windows.
- bounded energetic phrase can occur, then **must end**.

## 15.6 Attention Grammar

- quick eye notice → head/chest orientation more readily than Carol.
- invitation: chest forward before wing/foreleg offer.
- curiosity: one wing or head tilt can lead.
- boundary: attention may initially remain on user while chest stiffens; withdrawal turns head/wing away.
- environmental interest is important to prevent attention-seeking from becoming clingy.

## 15.7 Touch Zone Map [G]

| Class | Zones | Intent |
|---|---|---|
| **Preferred** | forehead/cheeks, upper chest, leaf-mane front/side near head | social energy / chest-led pleasure |
| **Neutral** | torso sides, belly edge, wing base | acknowledge without peak |
| **Disliked / sensitive** | wing tips/membrane edge, horn tips, heavy tail tip/base under repeated poke | protect delicate/structural areas |
| **Special** | white flowers/clover clusters, central leaf-mane accents | rare curiosity / spring-motif reaction |
| **Excluded** | eyeballs, mouth interior, detached butterflies/leaves/ambient particles | no collider |

## 15.8 Gesture × Zone Reaction Matrix

| Zone class | Tap / poke | Slow pet | Continuous stroke | Back-and-forth pet |
|---|---|---|---|---|
| Preferred | quick face/chest ack | chest softens→head/wing | pleasure builds; leaf lag | energetic but bounded happy phrase; tail only if intensity warrants |
| Neutral | curious chest/head response | mild content | body relax | may shift attention; not always happiness |
| Sensitive | quick recoil at local structure | small tolerance | clear refusal | wing protect / tail anchor / head away |
| Special | flower/leaf notice | gentle motif response | can trigger rare small nature phrase | no repeated sparkle spam |
| Excluded | none | none | none | none |

## 15.9 Self-Initiated Behaviors

- quick chest lift + user glance
- one-wing curiosity/opening
- leaf-mane shake-off equivalent, authored and rare
- short foreleg presentation
- plant-motif inspect
- energetic two-accent mood phrase
- intentional quiet after energy burst

## 15.10 Affection Behaviors

```text
local touch
→ chest/upper-body commits
→ face brightens
→ one wing opens / relaxes
→ leaf/flower lag
→ tail joins only on stronger affect
→ settle
```

## 15.11 Mild Dislike Behaviors

```text
local ack
→ chest stiffness
→ face warning
→ one wing defensive angle
→ head away
→ leaves follow
→ tail remains heavy / anchors
→ mild residue
```

No aggressive wing slap / bite / attack.

## 15.12 Feeding

- item notice is quick.
- chest/head approach carries anticipation.
- consume → short processing beat → bright face / wing accent.
- leaves lag after upper-body peak.
- effect motif stays restrained.

## 15.13 Gift / Toy

- can inspect with foreleg/wing framing, but short forelegs remain canonical.
- toy invitation should use chest/upper-body intent, not Eevee-style paw replay.
- rare flower/leaf response may accompany successful social event.

## 15.14 Rare Behaviors

- wing-and-chest social invitation
- short exuberant spring phrase with uneven accents
- flower/clover attention event
- rare tail-assisted body reposition showing its weight

## 15.15 Secondary Motion

- wing membrane main arc = authored.
- leaf clusters = delayed small follow-through.
- flower heads = smaller/later than leaves.
- tail base = authored; distal delay = restrained residual.
- no constant leaf breeze unless scene/environment explicitly supplies cause.

## 15.16 Sound / Haptic / VFX

- brighter, quicker vocal palette than Carol.
- haptic can be slightly sharper on successful reciprocal interaction.
- leaf/flower particles are punctuation only.

## 15.17 DO / DO NOT / Signature

**DO:** chest-led intent, quick attention, selective wing use, delayed plant structures, heavy tail.  
**DO NOT:** cat-tail wag, butterfly-wing flapping, permanent leaf rustle, elongated forelegs, Carol-like slow melt.  
**Signature:** **emotion grows outward from chest into wings/plants, while the tail resists and catches up late.**

---

# 16. Pino Experience & Motion Bible

## 16.1 Identity — canonical non-negotiables

`pino-canonical.png` visual authority:

- young blue otter-like Grimo with round soft body.
- pale cream lower face and very large cream belly.
- large glossy blue eye(s), small round ears, blue paw pads.
- short forearms positioned inward around an object; inward/hugging tendency is visually natural.
- hind feet forward in seated pose.
- very thick large tail, visually heavy and curved around the body.
- water splash and iridescent bubble motifs surround but do not replace the character.
- cute water-bag softness, not hollow inflatable balloon.

## 16.2 Personality

**energetic + independent**。

Movement can be playful and quick, but attention is not continuously offered to the user. Pino can glance, act, then return to self-directed activity.

## 16.3 Body Grammar

**Seated mixed**。

- seated body/hips are support mass.
- forearms are free social/holding channels.
- soft body compression/rebound is allowed only inside identity envelope.
- thick tail is a delayed heavy mass; never constant wag.

## 16.4 Motion Signature

| Dimension | Pino rule |
|---|---|
| motion lead | soft torso + arms, sometimes gaze first |
| baseline energy | medium-high |
| amplitude | medium with soft compression |
| tempo | quick start, elastic-but-weighted rebound |
| weight | belly/body soft-heavy; tail heavy |
| gaze | quick glance, frequent independent release |
| blink | alert but variable |
| head | compact; body often participates in lean |
| arms | inward/hugging is default expressive tendency |
| tail | clearly delayed; low-frequency |
| water/bubbles | event accent only |
| stillness | medium; can self-occupy |
| settle | body compresses/rebounds then tail finishes |
| afterglow | shorter than Carol/Shushu, often followed by look-away/self-action |

## 16.5 Living Idle Grammar

- seated support stays grounded.
- tiny torso/belly breathing, no spherical pulse.
- arms can reposition inward/outward sparsely.
- gaze often samples user then environment.
- tail usually rests; occasional slow catch-up shift.
- bubble/water motif absent or near-static in baseline unless scene cause exists.
- independent quiet behavior is required.

## 16.6 Attention Grammar

- quick user notice, shorter dwell.
- may glance away before the user responds to invitation.
- toy/item can compete strongly for attention.
- touch acceptance may close eyes briefly, then Pino can resume independent focus.
- boundary uses gaze break early.

## 16.7 Touch Zone Map [G]

| Class | Zones | Intent |
|---|---|---|
| **Preferred** | cheeks/lower face sides, head top, upper belly/chest | soft contact-seeking / body squish |
| **Neutral** | arms, torso side, back/shoulder | local acknowledgement |
| **Disliked / sensitive** | tail base/tip under repeated poke, hind feet/paw pads when prodded, ear edge | independent boundary |
| **Special** | blue paw pads, water/bubble semantic anchor used in special interaction | tactile/playful discovery |
| **Excluded** | eyeballs, mouth interior, free-floating bubbles/splash particles | no standard touch collider |

## 16.8 Gesture × Zone Reaction Matrix

| Zone class | Tap / poke | Slow pet | Continuous stroke | Back-and-forth pet |
|---|---|---|---|---|
| Preferred | quick squish/face ack | body leans in | arms pull inward + body softens | deeper compression→rebound; tail catches late |
| Neutral | curious/local response | mild accept | brief content | may turn into playful arm/body phrase |
| Sensitive | pull away / arm protect | short tolerance | clear gaze break | side turn + tail drag; no aggression |
| Special | paw-pad surprise / inspect | gentle playful response | toy-like branch if context valid | rare water accent only after body read |
| Excluded | none | none | none | none |

## 16.9 Self-Initiated Behaviors

- self-directed bubble/toy inspect
- small body sway + inward arms
- short paw offer then look-away
- tail-adjust / seated reposition
- water-curiosity phrase
- quiet independent rest

## 16.10 Affection Behaviors

```text
contact
→ local soft squish
→ face evaluation
→ head/body toward contact
→ arms pull inward / hug tendency
→ soft rebound
→ tail delayed follow-through
→ brief content afterglow
```

## 16.11 Mild Dislike Behaviors

```text
local acknowledgement
→ eyes glance
→ body pulls away
→ arms inward/protective
→ gaze breaks
→ side turn
→ tail drags after body
```

## 16.12 Feeding

Pino is a strong fit for staged consume grammar:

```text
notice → grab/hold if appropriate → consume → process pause → face/body delight → optional tiny bubble accent → settle
```

Do not make bubble burst equal emotion.

## 16.13 Gift / Toy

Pino may be the most toy-responsive character:

- arms can cradle/inspect.
- item can become temporary attention competitor.
- invitation frequency lower than Jill/Carol, preserving independence.
- successful play can yield body rebound + tail lag, not constant VFX.

## 16.14 Rare Behaviors

- self-started toy/bubble fascination
- short contact-seeking body press
- tail-assisted reposition
- rare playful water arc after a completed interaction

## 16.15 Secondary Motion

- body squish = authored deformation, not runtime balloon physics.
- tail base = authored; tip residual only.
- splashes/bubbles = effect layer with strict activity budget.
- water motifs never obscure face/arms.

## 16.16 Sound / Haptic / VFX

- bright, playful short sounds; some self-directed noises allowed.
- haptic can pair with soft rebound, but visual causality remains primary.
- bubbles/water used at peak/rare discovery only.

## 16.17 DO / DO NOT / Signature

**DO:** soft weighted compression, inward arms, independent gaze, delayed thick tail.  
**DO NOT:** balloon bounce, constant tail wag, bubble spam, user fixation, generic otter swimming motion in seated interaction context.  
**Signature:** **the soft body acts first, arms fold emotion inward, and the heavy tail arrives late.**

---

# 17. Shushu Experience & Motion Bible

## 17.1 Identity — canonical non-negotiables

`shushu-canonical.png` visual authority:

- young white-and-cherry-pink panda-like Grimo.
- round plush white face/body; pink ears, arms, legs/feet.
- large pink-brown glossy eyes with flower-shaped highlights.
- cherry-blossom flower crown attached to head.
- bouquet held between hands; hand-to-bouquet relationship is visible and must remain convincing.
- seated, grounded plush silhouette; large forward feet/paw pads.
- flowers, petals, butterflies surround as motifs; body remains primary.
- softness is plush/compressed, not jelly.

## 17.2 Personality

**relaxed + independent**。

Lowest social urgency of the four. Userを好んでも、静かな自己充足を保つ。Invitationは遅く、patientで、無視されても気にしない。

## 17.3 Body Grammar

**Grounded seated**。

- hips / seated base carry weight.
- feet forward provide strong visual anchor.
- torso compression is delayed and soft.
- arms maintain bouquet relationship unless a specific behavior temporarily frees one hand.
- crown follows head; bouquet follows hands; neither may float independently.

## 17.4 Motion Signature

| Dimension | Shushu rule |
|---|---|
| motion lead | head/eyelid; sometimes one ear |
| baseline energy | low |
| amplitude | small–medium |
| tempo | slow onset, slow release |
| weight | seated/plush heavy-soft |
| gaze | long gentle dwell, comfortable look-away |
| blink | soft and unhurried |
| head | small tilt/sink |
| ears | small bounce, low activity |
| arms/hands | bouquet relationship constrains range |
| crown/flowers | delayed tiny bounce |
| stillness | very high tolerance |
| settle | delayed compression release |
| afterglow | longest calm afterglow with Carol |

## 17.5 Living Idle Grammar

- stable seated base.
- tiny breath / plush maintenance.
- sparse blink and gaze.
- one-ear micro change.
- tiny bouquet hand correction only if believable.
- crown/flowers respond after head motion, never independently dance.
- long quiet windows are desirable.

## 17.6 Attention Grammar

- slow notice → soft dwell.
- can continue looking at flowers/bouquet/environment rather than user.
- invitation uses head tilt / free-hand or palm presentation, not urgent approach.
- boundary uses downward/away gaze and protected bouquet posture.

## 17.7 Touch Zone Map [G]

| Class | Zones | Intent |
|---|---|---|
| **Preferred** | cheek.L/R, forehead/head side, upper torso/shoulder outside bouquet | plush comfort |
| **Neutral** | arms, belly sides, outer ears | calm acknowledgement |
| **Disliked / sensitive** | hind feet/paw pads under poke, rough pulling at crown/bouquet attachment, lower body repeated poke | protect personal/prop space |
| **Special** | flower crown, bouquet flowers/leaves | delicate special response; slow gentle gesture only |
| **Excluded** | eyeballs, mouth interior, detached petals/butterflies/ambient flowers | no collider |

## 17.8 Gesture × Zone Reaction Matrix

| Zone class | Tap / poke | Slow pet | Continuous stroke | Back-and-forth pet |
|---|---|---|---|---|
| Preferred | soft notice | eyelid softens, head sinks | plush torso slowly compresses | deeper content hold; tiny ear/crown settle |
| Neutral | small glance | mild accept | calm | may remain mostly still by design |
| Sensitive | small protect / foot retract | uncertain | head away / bouquet closer | withdrawal; no guilt/sadness exaggeration |
| Special | flower/bouquet notice | delicate appreciation | gentle special branch | rough/fast repetition converts to boundary hint |
| Excluded | none | none | none | none |

## 17.9 Self-Initiated Behaviors

- bouquet inspect / adjust
- quiet flower look
- head tilt + user glance
- one free hand/palm invitation if rig/prop allows
- long plush rest
- rare petal/butterfly attention shift

## 17.10 Affection Behaviors

```text
cheek/head touch
→ eyelid softens
→ head sinks toward contact
→ plush torso compresses slightly
→ one ear relaxes/bounces
→ crown follows
→ bouquet/flowers settle last
→ long quiet content afterglow
```

## 17.11 Mild Dislike Behaviors

```text
notice
→ eyes down / away
→ head turns
→ one ear lowers
→ plush torso retreats/compresses
→ bouquet held closer
→ flowers settle
→ quiet neutral recovery
```

No guilt-inducing sadness.

## 17.12 Feeding

- slow notice, careful accept.
- staged consumption / evaluation.
- positive response is small and sincere, not explosive.
- hands/bouquet geometry must not interpenetrate food/item.

## 17.13 Gift / Toy

- bouquet-related gift interaction is semantically natural but must not detach bouquet arbitrarily.
- user toy may be inspected slowly; Shushu need not immediately engage.
- rare flower exchange can be a strong relationship ritual [G].

## 17.14 Rare Behaviors

- free-palm invitation
- slow bouquet offer / flower-sharing ritual
- long eyes-closed plush settle
- butterfly/petal curiosity
- delayed look-back after user interaction

## 17.15 Secondary Motion

- plush body compression = authored.
- ear bounce = tiny and delayed.
- crown base follows head rigidly enough to stay attached; petals/flower heads can lag slightly.
- bouquet follows hands; flower heads/leaf tips lag lightly.
- ambient petals are event/scene effects, not constant character motion.

## 17.16 Sound / Haptic / VFX

- quiet, breathy/soft nonverbal palette.
- haptic should be least assertive among four.
- flower/petal VFX only on rare/special event, not baseline.

## 17.17 DO / DO NOT / Signature

**DO:** grounded seated weight, slow plush compression, patient attention, convincing prop attachment, long stillness.  
**DO NOT:** bounce like a stuffed spring, constantly shake flowers, detach bouquet physics, make relaxed independence look sad, reuse Carol fleece timing unchanged.  
**Signature:** **Shushu absorbs emotion into a grounded plush body, then lets flowers and props settle after the feeling has already landed.**

---

# 18. Four-Character Differentiation Matrix

| Dimension | Carol | Jill | Pino | Shushu |
|---|---|---|---|---|
| Energy | low–medium | medium–high | medium–high | low |
| Weight | heavy hooves + soft huge fleece | light/active upper body + heavy tail | soft-heavy body + heavy tail | grounded plush seated mass |
| Motion lead | face/head/local touch | chest / upper body | torso + arms | head/eyelid |
| Tempo | slow-soft, responsive ACK | quick, springy | quick with elastic rebound | slow, delayed |
| Motion amplitude | small; rare medium | medium; rare high | medium | small–medium |
| Gaze | long soft dwell | quick notice/reorient | glance + deliberate release | slow gentle dwell |
| Blink | soft; long affect eye-close | alert/quick tendency | alert, playful | soft/unhurried |
| Head | lean/lower/offer | lift/tilt, energetic | compact with body participation | small tilt/sink |
| Appendage | subtle ears; fleece follows | wing → leaves/flowers → heavy tail | arms inward; tail late | ear → crown/bouquet flowers late |
| Touch response | accepts and leans, fleece echo | chest commits outward | soft squish, hug-inward, rebound | plush sink/compress |
| Invitation | cheek/forehead/rare hoof offer | chest-forward foreleg/wing offer | lower-frequency paw offer, may look away | patient palm/head-tilt offer |
| Dislike | soft hint → withdraw into fleece | chest stiff → wing defense → head away | arms protect → gaze break → side turn | eyes down → bouquet protect → quiet retreat |
| Settle | face/head then fleece | chest then plants/tail | body then tail | plush body then flowers/props |
| Afterglow | long warm | bright medium | medium-short, may self-direct | long calm |
| Stillness | high | medium | medium | very high |
| Rare behavior | dream/moon-star social beat | energetic spring/wing phrase | water/toy curiosity | flower-sharing / bouquet ritual |

### Differentiation acceptance

A reviewer who sees motion-only silhouettes or simplified clay renders should still be able to describe the four differently. If the only reliable difference is speed, **FAIL**.

---

# 19. Shared vs Character-Specific Architecture

## 19.1 Shared runtime logic — may be common code

- relationship/context memory
- emotion/arousal/motive state container
- attention target abstraction
- utility candidate scoring
- HFSM / behavior lifecycle framework
- gesture accumulator
- semantic touch raycast / hit-volume framework
- recent-history / cooldown / repetition penalty framework
- interruption protocol
- audio/haptic/VFX event bus
- runtime performance telemetry
- persistence / background resume reconciliation

## 19.2 Shared animation concepts — concept only

- acknowledgement
- anticipation
- commit
- peak
- moving hold
- settle
- afterglow
- invitation
- WAIT
- boundary hint / refusal / withdrawal
- contact-seeking
- delayed payoff

The **concept name** may be common; pose, timing, channel ownership, weight and facial acting are not.

## 19.3 Character-specific data

- semantic zone map
- personality weights
- gaze profile
- blink modifiers
- timing envelopes
- activity budgets
- emotion preset definitions
- contact preference / boundary weights
- cooldown ranges
- rare behavior eligibility
- audio palette mapping
- effect budget
- identity envelope / expression clamps

## 19.4 Character-specific animations

Must be authored separately for:

- hero idle phrases
- touch reaction families
- invitation performances
- boundary / withdrawal
- large emotion
- feeding / toy / gift acting
- settle / afterglow hero transitions
- signature rare behaviors

## 19.5 Character-specific rig behavior

- support / COM topology
- head-eye coupling limits
- ear / wing / tail chain response
- fleece / leaf / flower / plush / water-body deformation
- prop constraints
- safe facial ranges
- touch anchor placement

## 19.6 Never share directly

- Carol fleece solver settings → another character
- Jill wing rhythm → Shushu/Pino
- Pino body squash → Carol/Shushu
- Shushu plush compression → Pino water-body
- same `happy.glb` / `dislike.glb` retarget across all four
- identical invitation pose with only speed changes
- identical gaze dwell distribution
- identical settle duration

### Production evidence

Source research notes that Pikachu and Eevee received separate motion-design attention and emphasizes species/character-specific acting rather than generic retargeting. citeturn3view1 [B]

---

# 20. Minimum Experience Set

**Coverage, not animation count, is authoritative.** A behavior may use modular primitives; a hundred clips do not compensate for a missing capability.

## 20.1 P0 — Carol Vertical Slice / Life Minimum

| Purpose | Required behavior/capability | Required variation | Acceptance condition |
|---|---|---|---|
| Identity | canonical-faithful neutral Carol | canonical + ±15° view | Gate A pass |
| Living existence | 15–30s idle with asynchronous channels | at least multiple micro-event combinations | Gate B pass; no mechanical loop |
| Touch causality | head + cheek pet | side L/R + shallow/deep response | local→face→head→body→fleece readable |
| Gesture meaning | tap vs slow pet vs continuous / back-and-forth | minimum distinct semantic outcomes | scripted classification thresholds met |
| Contact seeking | Carol leans into accepted touch | L/R conditioned | contact anchor remains valid while moving |
| Agency | self-initiated affection invitation | at least 2 invitation performance variants | Character → User WAIT works |
| Boundary | hint → refusal → withdrawal | at least mild variant + recovery | no hostility; state persists |
| Large emotion | one hero delight/affection reaction | ≥3 performance variants or modular compositions | anticipation + peak + settle + afterglow |
| Interruption | touch/reaction/WAIT redirects from current pose | at least 3 interruption scenarios | no forced neutral/clip finish |
| Repetition | history-aware reaction selection | same gesture repeated ≥10 times | no obvious identical run / same-family spam |
| Runtime | Pixel 7a-class | cold/warm/background-resume | Gate H pass |

## 20.2 P1 — Launch Quality

| Purpose | Required behavior | Variation target | Acceptance |
|---|---|---|---|
| Positive depth | head/cheek/front-fleece families | 3–5 variants per major family | causality stable, performance varied |
| Boundary richness | hint/refusal/withdrawal | ≥3 hint/refusal, 2–3 withdrawal | pressure/hysteresis readable |
| Attention life | user/environment/contact gaze | multiple dwell/release profiles | no permanent stare |
| Autonomous life | curiosity, relaxed hold, check-in, self-adjust | several families + quiet option | 2–5 min session not scheduler-like |
| Feeding | notice→consume→evaluate→react | timing/facial variants | staged, not instant disappearance |
| Gift/toy | character notices/initiates/manipulates | ≥2 families | body relationship readable |
| Audio | nonverbal palette mapped to behavior | pitch/take/foley variation | no repeated identical SE feel |
| Secondary | fleece clusters tuned per action | local/medium/hero presets | never dominates primary acting |
| Memory | recent preference / interaction state | session-state dependent | next behavior visibly changes sometimes |
| Rare discovery | moon/star or relationship event | strict cooldown/context | feels discovered, not random popup |

## 20.3 P2 — Depth / Surprise

- longer relationship-dependent behavior distribution
- rare reconciliation / delayed affection
- remembered preferred-touch tendencies
- richer item/toy rituals
- seasonal/contextual mini rituals
- more autonomous self-groom / environment interactions
- rare social turn sequences
- deeper session-entry recognition
- character-specific collection-linked behaviors
- all-four-character expanded libraries only after Carol launch-quality proof

P2 must **not** be started to compensate for P0 causality/identity failure.

---

# 21. Carol Vertical Slice — Final Experience Specification

## Gate A — Identity

### PASS

- neutral frame is immediately recognizable as canonical Carol.
- tiny cream face / huge fleece ratio preserved.
- eye size/spacing/highlights, ears, hooves, moon/star landmarks and color hierarchy stay on-model.
- slight 3/4 does not reveal a different-looking character.

### Measurement [G]

- canonical-camera silhouette IoU target **≥0.90**.
- major landmark deviation target **≤ ~3% of character bounding box**.
- blind same-character rating target **≥4.3/5**.
- “3D made Carol less cute” responses target **≤15%**.
- canonical and ±15° comparison capture.

### FAIL

- generic sheep/wool look.
- face becomes too large/small or too protruding.
- fleece loses cloud silhouette.
- 3/4 face becomes off-model.
- animation polish is being used to hide a static identity problem.

### Human review

**静止していてもCarol本人か。** Machine similarity cannot override human identity verdict.

---

## Gate B — Living Idle

### Test

15–30 seconds, no user input, sound both ON and OFF.

### PASS

- at least six independently composable living channels available in the system.
- some channels act while others rest.
- no visible common period / synchronized cycle.
- intentional stillness looks intentional, not frozen.
- face/head/ears/hooves/fleece preserve grounded anatomy.

### Measurement [G]

- no perceived identical full-body loop within 30s.
- user `alive` rating target **≥4.0/5**.
- animacy improvement over static model target **≥+1.0 point** in formative comparison.
- event-history logs show non-fixed interval scheduling.

### FAIL

- whole character sways/breathes together.
- nothing except global scale changes.
- every 20–30s one canned idle plays while otherwise dead.
- fleece moves continuously with no body cause.

### Human review

“animationを見ている”より“Carolがそこにいる”が先に来るか。

---

## Gate C — Head / Cheek Pet

### Test

- left cheek, right cheek, forehead/head.
- tap, slow pet, continuous stroke, back-and-forth.
- slow/medium/fast trajectory.

### PASS

```text
correct semantic zone
→ local visible acknowledgement
→ attention/evaluation
→ character-specific lean/reaction
→ grounded propagation
→ fleece follow-through
→ settle
→ afterglow
```

### Measurement [G]

| Metric | Target |
|---|---:|
| semantic-zone classification on scripted paths | ≥98% |
| first visible acknowledgement p95 | ≤80 ms |
| semantic response onset p95 for immediate classes | ≤100 ms |
| tap vs slow-pet classification | ≥95% |
| repeated-poke recognition | ≥95% |
| users saying “reacted to where I touched” | ≥90% |
| touch-causality rating | ≥4.3/5 |

These are Grimo quality targets, not Pokémon internal timings.

### FAIL

- head and cheek invoke same centered full-body clip.
- left/right contact collapses to bilateral center response.
- dragged touch loses collider/anchor while Carol leans.
- finger release is ignored until clip ends.

### Human review

指がCarolの身体へ**届き、Carol自身がその触れ方を解釈した**ように見えるか。

---

## Gate D — Self-Initiated Invitation

### PASS

User inputなしでCarolが social motiveからinteractionを始める。

```text
notice / motive expression
→ cheek/head/rare hoof offer
→ WAIT
→ user response / timeout
→ interpretation
→ settle / second turn / satisfied end
```

WAIT中もmicro lifeが残る。

### Measurement

- invitation can persist without auto-retract until policy timeout.
- user contact target follows pose.
- ignored path, successful path, interruption path all exist.

### FAIL

- invitation is merely a clip that ends on a timer.
- Carol stares motionless during WAIT.
- ignored user gets guilt/sadness punishment.

### Human review

“押したから出た”ではなく、“Carolから求めてきた”と読めるか。

---

## Gate E — Larger Emotional Reaction

### PASS

At least one Carol-specific hero reaction contains readable:

```text
anticipation
→ primary body action
→ facial peak
→ selected appendage participation
→ authored follow-through
→ optional restrained overshoot
→ settle
→ afterglow
```

At least three performance variants/modular compositions without changing semantic meaning.

### FAIL

- VFX creates the emotion before body acting.
- every channel moves at full amplitude.
- reaction ends at peak and snaps neutral.
- it resembles Eevee/Pikachu signature performance rather than Carol.

### Human review

VFX OFF / audio OFFでも感情が読めるか。

---

## Gate F — Interruption

### Required scenarios

1. slow pet while Carol starts autonomous idle.
2. new touch while previous pet is settling.
3. user withdraws during contact-seeking hold.
4. touch different zone during invitation WAIT.
5. boundary input during content afterglow.

### PASS

- redirect begins from current pose/state.
- face/attention acknowledges changed situation.
- no neutral teleport.
- channel ownership changes cleanly.

### FAIL

- old clip keeps playing over new user input.
- body and face contradict each other for >brief transitional overlap.
- secondary continues the old action after primary was canceled without plausible inertia.

### Measurement

scripted interruption test capture + transition-discontinuity log + frame-by-frame human review.

---

## Gate G — Repetition

### Test

Repeat identical interaction ≥10 times under controlled state; repeat another set with varying recent history.

### PASS

- causality stays recognizable.
- reaction intensity/history evolves.
- immediate consecutive identical family is strongly suppressed unless intentionally appropriate.
- face/ear/settle/afterglow combinations vary.

### FAIL

- user can name the exact clip sequence after a few repetitions.
- random variation breaks contact causality.
- repetition suppression causes inappropriate emotional outcomes.

### Measurement

behavior-history logs, clip/similarity-group usage, video similarity review, blind human “mechanical/repetitive” rating.

---

## Gate H — Pixel 7a Runtime

### Baseline architecture

- smartphone-first PWA.
- Blender → validated GLB/glTF.
- PlayCanvas Engine web-native runtime baseline.
- WebGL 2 acceptance baseline; WebGPU is enhancement, not requirement. citeturn24search1

### Initial engineering budgets [G]

| Item | Starting budget / target |
|---|---|
| simultaneous hero character | 1 |
| LOD0 geometry | 30k–60k triangles; Carol may profile up to ~80k |
| deform bones | ~70–110 initial range |
| vertex influences | ≤4 preferred |
| character draw calls | ≤8 target |
| texture | main 2K-class + auxiliary 1K-class; avoid unnecessary PBR maps |
| first meaningful visual payload | ~3–8 MB candidate |
| total first-character compressed payload | ~6–12 MB target |
| other characters | lazy load |
| interactive frame rate | 60 fps target |
| quiescent long idle | adaptive 30 fps only if perceptual quality/latency remains acceptable |
| main frame | 16.7ms target |
| sustained severe frame streak | no repeated >33ms streaks |
| tab memory | ≤350MB initial target, then tighten from profiling |

Pixel 7a class requirement is product-authoritative; these budgets are starting points, not reasons to lower experience quality. Source architecture cites Tensor G2 / 8GB device-class evidence. citeturn31search4turn31search12

### Runtime acceptance [G]

- 10-minute warm/thermal-soak.
- median around 55–60 fps or better during interaction.
- no sustained <30 fps interaction periods.
- touch first-visible ACK p95 ≤80ms.
- PWA INP p75 ≤200ms. citeturn26search0turn26search16
- no obvious ~100ms freeze during character interaction.
- no progressive memory leak.
- foreground→background→resume has no giant-dt explosion.
- touch volumes remain correct under animation/deformation.

### Background rule

Do **not** simulate realtime animation while PWA is frozen/backgrounded.

```text
lastKnownState + timestamp
→ resume
→ elapsed-time reconciliation
→ plausible current state
```

### FAIL

If quality only works on flagship hardware, or input causality degrades under thermal load, the architecture fails the product boundary.

---

# 22. Timing & Motion Parameter Guidance

## 22.1 Reference measurements — direct footage only

| Observation | Measured example | Evidence discipline |
|---|---:|---|
| video frame unit | 33.3 ms | 30fps metadata [V1] |
| Pikachu visible neutral blink | ~133 ms | single example [V1] |
| Eevee visible neutral blink | ~133 ms; full closure ~67 ms | single example [V1] |
| Pikachu high-five contact → visible ACK | ~1–2 frames | internal input latency not claimed [V1] |
| Eevee high-five contact → clear happy face | ~67 ms | repeated examples [V1] |
| Pikachu first facial warning → body avoidance | ~1.5s+ | negative escalation example [V1] |
| Eevee negative face → major ear peak | ~1.1–1.2s | one negative family [V1/V2] |
| Eevee feeding consume → delight | ~0.8–0.9s | repeated [V1/V2] |
| Eevee high-five final contact → delayed major affect | ~0.8–0.9s | [V1/V2] |
| Eevee long relaxed moving hold | ~20+s | [V1] |
| Pikachu social disengagement orientation | ~12+s | [V1] |
| Pikachu positive afterglow | several seconds | V05 ~102–105s [V1] |
| Eevee bounded high-energy phrase | ~3s | E04 [V1] |

**Do not convert these into universal Grimo constants.**

## 22.2 Grimo timing dimensions

Each behavior declares ranges/distributions for:

- acknowledgement latency
- evaluation / accumulation time
- anticipation duration
- primary action duration
- secondary delay
- peak / moving-hold duration
- settle duration
- afterglow duration
- cooldown
- autonomous eligibility window

## 22.3 Interaction-class policy

```text
LOCAL_REFLEX          fastest visible response
SOCIAL_RECIPROCAL     very fast success acknowledgement
STROKE_ACCUMULATION   gradual semantic escalation
FEEDING               staged consume/evaluate/reward
LARGE_REACTION        anticipation + authored peak
BOUNDARY              warning/tolerance before withdrawal
```

## 22.4 Carol initial tuning envelope [G]

For preferred head/cheek touch:

- local ACK: ~0–80ms target
- eyelid/face: ~50–180ms
- attention/head onset: ~80–320ms depending behavior
- ear response: ~180–450ms
- body transfer: ~250–700ms
- fleece follow: ~300–900ms
- settle: ~0.7–1.6s common envelope
- positive afterglow: ~1.5–5s

For deep contact-seeking, hold may last roughly ~0.4–0.9s as a starting design envelope. These are **Grimo design ranges**, not reference copying.

## 22.5 Idle timing

Never encode “blink every X seconds” or “major action every 20 seconds.” Use probability distributions conditioned by state, recent history, and character.

Major event frequency should be lower than micro-event frequency; intentional quiet is always an eligible outcome.

---

# 23. Experience Runtime Model

## 23.1 Final conceptual architecture

```text
Persistent Relationship / Context Memory
+ Session State / Recent History
+ Environment / User Presence
+ User Input / Semantic Touch
                ↓
Perception & Immediate Local Reflex ───────────────┐
                ↓                                 │
Attention State + Affect + Motives                │
                ↓                                 │
Utility / Intent Candidate Selection              │
                ↓                                 │
Hierarchical Behavior Controller (HFSM)           │
                ↓                                 │
Performance Variant Selector                      │
                ↓                                 │
Animation Coordinator / Channel Ownership         │
                ↓                                 │
┌───────────────────────────────────────────────┐ │
│ Base/support pose                             │ │
│ Posture / COM                                 │ │
│ Breath                                        │ │
│ Gaze + head coordination                     │ │
│ Blink / eyelid                               │ │
│ Facial expression                            │ │
│ Primary authored action                      │ │
│ Limb / appendage intent                      │ │
│ Local touch response  ◀──────────────────────┘ │
│ Afterglow                                     │
│ Secondary follow-through                     │
│ Limited IK / constraints                     │
└───────────────────────────────────────────────┘
                ↓
Identity / silhouette clamps
                ↓
Final Pose + Audio + Optional Haptic/VFX
                ↓
Outcome Evaluation
                ↓
State / motive / history update
                ↓
Next behavior OR intentional stillness
```

## 23.2 Architectural separation

- **TypeScript/domain layer:** why behavior happens; relationship, affect, utility, history, gesture semantics.
- **PlayCanvas animation layer:** clip playback, masks, additive/override layers, transition, interruption, events. Source research notes official support for state graph/layers/masks. citeturn23view1turn23view0turn23view2
- **Blender production:** model, rig, identity-safe facial controls, authored animation, export.
- **Procedural layer:** gaze/blink/target-following, bounded micro residual.
- **Dynamics:** last small residual only.

## 23.3 Persistent state candidates

```text
bond / familiarity
current valence / arousal
comfort
curiosity
socialSeeking
restSeeking
irritation / boundaryPressure
engagement / disengagement
recently touched zones
repetition pressure
recent behavior history
last major event
rare-event cooldowns
session entry / last interaction time
```

Not every value must be visible at once; it must alter behavior probability or presentation when relevant.

## 23.4 Cross-scene continuity

UI remount must not automatically neutralize emotion. Character state belongs to character domain, not a single component lifecycle.

---

# 24. Behavior Data Model

Implementation code is intentionally omitted. The production contract should conceptually support:

| Field | Meaning |
|---|---|
| `behaviorId` | stable semantic identifier |
| `character` | Carol/Jill/Pino/Shushu |
| `family` | reaction/autonomy/invitation/etc. similarity group |
| `trigger` | input/state/context condition |
| `semanticZone` | eligible body zone(s) |
| `gesture` | tap/pet/stroke/rub/hold/etc. |
| `gestureDirection` | optional directional semantics |
| `contactSide` | L/R/center/bilateral |
| `prerequisites` | state/motive/pose/context requirements |
| `priority` | behavior scheduling priority |
| `interruptibility` | none/soft/hard + safe redirect policy |
| `channelOwnership` | body channels temporarily controlled |
| `cooldown` | hard/soft timing policy |
| `repetitionPenalty` | recent-use reduction |
| `similarityGroup` | perceptual repetition grouping |
| `emotionModifiers` | state influence on eligibility/weight |
| `attentionModifiers` | target/fixation/disengagement influence |
| `motiveModifiers` | socialSeeking/curiosity/etc. |
| `variants` | performance variants / weights |
| `animationChannels` | base/facial/head/limb/etc. clips or primitives |
| `timingProfile` | ACK/anticipation/hold/settle ranges |
| `secondaryRules` | lag/limits/solver preset |
| `audioRules` | vocal/foley/event timing |
| `hapticRules` | optional device feedback |
| `vfxRules` | restricted effect cues |
| `afterglow` | state written after performance |
| `nextStateInfluence` | updated affect/motive/attention probabilities |
| `timeoutPolicy` | invitation/hold failure or ignore path |
| `identityConstraints` | character-specific pose/facial clamps |

### Behavior authoring rule

A behavior definition is invalid if it only says “play animation X.” It must state **cause, semantic meaning, channel ownership, interruption, settle, and state update**.

---

# 25. Production Rules for AI / Codex

## 25.1 Stable principle — risk tier, not model brand

Specific model names are not normative production architecture. The durable rule is:

> **High-risk creative decisions require highest-reasoning + Human Gate; bounded production tasks can be delegated downward.**

If current workflow uses **Astra / Sol-class / Terra** labels, map them as follows:

### Tier H — Astra / highest-reasoning class

Use for:

- character-defining motion decisions
- canonical interpretation / unseen anatomy hypotheses
- identity-critical face/eye decisions
- rig architecture change
- new facial system / identity envelope
- new motion signature / signature rare behavior
- first hero reaction in a new family
- resolving conflicting evidence/specification
- Go/No-Go recommendation

Human approval mandatory.

### Tier M — Sol-class

Use for:

- normal character-specific animation work within an approved Bible
- runtime behavior logic
- semantic touch / interruption integration
- complex debugging
- blending/masking/channel ownership
- performance profiling / optimization
- new variants that still require animation judgment

Human review at gate/release boundaries.

### Tier L — Terra / bounded production class

Use for:

- parameter changes within approved envelopes
- repetitive Blender/Python scripting
- export / manifest / naming / hierarchy checks
- batch rendering / screenshots
- collider visualization
- clip enumeration
- regression capture
- validation / metrics collection
- low-risk variation assembly from approved primitives

Escalate if task changes identity, hero timing, rig architecture or motion signature.

## 25.2 Automation contract

Production contract should be **Blender Python + CLI + deterministic manifests**, with MCP as convenience layer rather than sole dependency. This follows the Production Architecture recommendation.

```text
AI/Codex
→ deterministic scripts / CLI
→ Blender
→ validated GLB + manifest
→ runtime tests / capture
→ Human Gate
```

## 25.3 AI may automate

- naming/hierarchy validation
- rig semantic-tag checks
- export / batch render
- GLB metadata / texture / bone / influence validation
- touch-volume visualization
- performance capture
- scripted gestures
- screenshot/video regression
- load-size regression
- dead-animation / fixed-loop heuristics

## 25.4 AI-assisted, human-approved

- unseen geometry proposals
- turnaround drafts
- retopo / weighting proposals
- rough motion blocking
- expression candidates
- motion variants
- secondary tuning proposals

## 25.5 Human must retain final authority

- canonical identity
- face / eyes
- silhouette
- key poses
- hero timing
- anticipation / overshoot / settle
- emotional afterglow
- “cute / alive / off-model” verdict
- character personality / signature motion

Source research conclusion: **the final quality-defining fraction should not be fully automated.**

---

# 26. QA & Measurement

## 26.1 Identity QA

Methods:

- canonical screenshot comparison
- silhouette / landmark metrics
- neutral + ±15° review
- expression envelope regression
- blind same-character rating

Pass requires human identity verdict.

## 26.2 Livingness QA

Methods:

- 15–30s no-input viewing, repeated several runs
- sound-off review
- channel activity timeline inspection
- fixed-period / synchronized motion detection
- static baseline A/B

Questions:

- alive or animated object?
- quiet or dead?
- cause-driven or random?

## 26.3 Touch Causality QA

- scripted trajectories per zone/gesture/side
- latency recording
- semantic classification confusion matrix
- frame-by-frame local→global review
- touch anchor tracking during deformation
- finger-release / mid-reaction interruption test

## 26.4 Attention QA

- permanent-stare test
- glance/dwell/release capture
- contact attention vs environment attention
- boundary disengagement
- invitation fixation
- off-screen / edge target identity-clamp test

## 26.5 Emotion Readability QA

Show body/face clips without labels; ask reviewers to classify broad state and intensity.

Success means valence/arousal/social meaning is readable **without VFX text/UI**.

## 26.6 Repetition QA

- 10× identical gesture test
- 2–5min free interaction capture
- behavior-history log
- similarity-group distribution
- human “mechanical/repetitive” rating

## 26.7 Character Differentiation QA

Blind clay/silhouette motion comparison across four characters.

Collect adjectives; desired clusters should separate:

- Carol: soft / reassuring / affection-seeking
- Jill: lively / eager / energetic
- Pino: playful / self-directed / elastic
- Shushu: calm / plush / independent

If reviewers describe all as “same cute pet, different speed,” FAIL.

## 26.8 Performance QA

On Pixel 7a class:

- cold load / first meaningful character
- continuous idle
- continuous pet
- hero reaction repetition
- 10-minute warm test
- memory / leak
- background/resume
- touch latency under thermal load

## 26.9 Human Gate

Automated tests = evidence. Human Gate = acceptance authority.

At minimum reviewers must answer:

1. Is this unmistakably the canonical character?
2. Does it seem to notice and interpret the user?
3. Does it have its own intent and boundaries?
4. Does the body carry weight and causality?
5. Does emotion survive beyond the clip peak?
6. Does repeated interaction still feel like the same living individual rather than a playlist?

## 26.10 Recommended comparative studies

- synchronous vs asynchronous idle
- generic full-body pet vs local→global pet
- immediate neutral vs afterglow
- no history vs recent-history suppression
- player-only initiation vs autonomous invitation
- visuals-only vs visual+audio
- random motion vs state-correlated stochastic motion

Source research proposed formative within-subject studies and standard animacy/likeability/perceived-intelligence measures; sample size remains a study-design question, not a fixed Bible requirement.

---

# 27. Failure Diagnosis Guide

| Symptom | Likely causes | Correction direction |
|---|---|---|
| **“ぬいぐるみを揺らしている”** | root-dominant motion; synchronized channels; no local causality; face/gaze independence weak | freeze root more; restore local lead; split channels; add intent-specific phase relationships |
| **“落ち着きがない”** | no intentional stillness; idle timers too frequent; every channel active; no cooldown | raise quiet probability; add channel refractory periods; reduce appendage baseline activity |
| **“死んで見える”** | static pose has no attention state; blink/gaze/face absent; long hold has no semantic context; afterglow resets | preserve attention/motive; add sparse micro channels; vary base state; make hold intentional |
| **“浮いて見える”** | COM moves without support; feet slide; seated base ignored; secondary pulls silhouette | re-author support/weight shift; lock contacts; reduce root oscillation; tune settle |
| **“反応がゲーム的”** | touch→clip mapping; no evaluation; ACK too late; snap neutral; VFX first | add immediate local ACK, accumulation, attention, staged response, afterglow |
| **“何度も見ると機械”** | fixed intervals; same similarity family; same side/face/settle; exact repeated timing | history buffer, penalty, context weighting, side conditioning, modular performance variants |
| **“4匹が同じ性格”** | shared animations; same gaze distribution; same amplitude/settle; speed-only variation | restore motion lead, weight, invitation, boundary, settle and appendage grammar per character |
| **“Carolがゼリー”** | whole-fleece soft-body; global breathing; too much residual | stabilize silhouette; authored cluster controls; reduce residual amplitude/duration |
| **“Jillが虫っぽい”** | constant wing flap; leaves always rustle; tail too fast | return intent to chest; wings episodic; tail heavy/rooted; plant follow-through only |
| **“Pinoが風船”** | uniform squash/stretch; body rebounds without support; tail too light | authored weighted compression; seated anchor; delayed heavy tail |
| **“Shushuが悲しそう”** | independence/quiet encoded as droop; gaze-down overused; boundary residue too long | distinguish calm from low valence; soften eyelids, preserve relaxed posture, shorter negative residue |
| **“目だけ怖い/人間的”** | gaze range too high; white-of-eye exposure; human mouth/eyebrow logic | tighten identity envelope; head assists gaze; use approved stylized presets |
| **“touch sideが分からない”** | side discarded after collision; centered macro clip | preserve contactSide/localPosition through selection and pose composition |
| **“VFXがうるさい”** | effects fire on baseline reaction; body acting weak | remove effects; pass VFX-off acting gate; reserve effects for special/rare peaks |
| **“reaction同士がぶつかる”** | no channel ownership; random idle injection; interruption policy absent | lock owned channels; define safe redirect; prioritize input/hero behavior |

---

# 28. Implementation Order

## 28.1 Production order

```text
Carol canonical identity
↓
3D reconstruction / canonical camera match
↓
rig / deformation / facial identity envelope
↓
neutral pose + support / COM
↓
living idle channels
↓
attention / gaze / blink
↓
semantic touch + immediate local reflex
↓
head / cheek pet + contact-seeking
↓
autonomous invitation + WAIT
↓
boundary / withdrawal
↓
one larger hero reaction
↓
interruption
↓
variation / repetition suppression
↓
audio / restrained haptic / VFX
↓
Pixel 7a optimization
↓
Human Gate A–H
↓
ONLY THEN: architecture expansion to a morphologically distant second character
↓
remaining two
```

## 28.2 Second-character choice

After Carol passes, choose a morphology that stress-tests generality rather than the most similar character. Jill is the strongest architecture stress test because wings + leaf/flower mane + heavy tail introduce very different channel/secondary requirements. Shushu is also valuable for seated prop constraints.

## 28.3 Stop rules

- Gate A fail → stop animation production, fix identity.
- Gate C fail → stop adding interaction quantity, fix causality.
- Gate G fail → stop adding rare content, fix variation architecture.
- Gate H fail → profile/optimize before expanding character count.
- Human says “not Carol” → automated scores do not overrule.

---

# 29. Open Questions

Only questions not resolvable from the specified sources remain here.

## 29.1 Additional footage required

1. **Fine eye-only gaze:** close-up footage sufficient to quantify pupil/iris tracking vs head tracking.
2. **Invitation timeout:** Pikachu/Eevee reciprocal invitation with no user response until natural timeout.
3. **Controlled left/right touch:** identical gestures on opposite cheeks/sides to isolate side conditioning.
4. **Mid-reaction release:** finger removed during Eevee contact-seeking lean / pet accumulation.
5. **Long idle distribution:** 2–5 minute no-input captures to estimate micro/small/major event density without montage bias.
6. **Mood phrase variation:** repeated same mood/context captures to determine performance variation and cooldown behavior.

## 29.2 Technical prototype required

7. **Carol unseen geometry:** exact side/back reconstruction that preserves front sacred view and 3/4 identity.
8. **Touch-anchor robustness:** bone-attached semantic volumes while cheek/head/fleece deform and character moves into contact.
9. **Fleece residual system:** maximum safe procedural lag before silhouette looks jelly-like.
10. **Pixel 7a sustained budget:** real triangle/bone/shape/texture ceiling after thermal soak.
11. **WebGL2 fallback quality:** whether full P0 experience remains stable without WebGPU.
12. **Background reconciliation:** best state advancement policy after long PWA suspension.

## 29.3 Human artistic decision required

13. **Final touch preference/boundary maps:** this Bible sets production defaults, but exact “loves/dislikes” should be artistically validated per character before lock.
14. **Expression envelope limits:** exact mouth/eye/cheek ranges that remain canonical.
15. **Signature rare behaviors:** final hero behavior that users should associate uniquely with each Grimo.
16. **Character vocal identity:** nonverbal timbre, density and recording/generation policy.
17. **Unseen motif anatomy:** how Carol moon/star, Jill plant structures, Pino water motif, Shushu crown/bouquet attach in 3D from unseen angles.

## 29.4 User testing required

18. **Partner-quality animacy:** does Carol generate comparable perceived agency/responsiveness, controlling for Pokémon familiarity?
19. **Repetition threshold:** after how many repeated interactions does each current family become recognizable/canned?
20. **Four-character adjective separation:** do users independently perceive the intended personality clusters?
21. **Return motivation:** does interaction create voluntary desire to revisit the character rather than only task/reward compliance?

**Unresolved open-question count: 21.**

---

# 30. Final One-Page Production Doctrine

## Grimo must always...

1. preserve canonical identity before adding motion.
2. make every meaningful motion have a cause.
3. let attention and intent exist before/after user input.
4. respond locally to touch before escalating globally when appropriate.
5. keep support/COM grounded.
6. use correlated asynchrony, not random desynchronization.
7. allow moving holds and intentional stillness.
8. let emotion outlast the action peak.
9. support Character → User initiation.
10. preserve WAIT as a living social state.
11. distinguish deterministic causality from stochastic performance variation.
12. preserve contact side, direction, speed, duration and history.
13. let stronger emotions recruit more channels progressively.
14. keep secondary motion subordinate to primary acting.
15. preserve boundaries without hostility or punishment.
16. remain interruptible from the current pose.
17. suppress perceptual repetition by family/history, not only clip ID.
18. remain practical on Pixel 7a-class PWA hardware.
19. make each character’s motion identity independently reviewable.
20. end at Human Gate, not automated confidence.

## Grimo must never...

1. animate a finished single image as one rigid puppet.
2. use whole-body breathing/bobbing as the core life system.
3. move every part all the time.
4. stare at the user permanently.
5. play the same happy/full-body reaction for every touch.
6. snap from peak to neutral.
7. ignore input until a clip finishes.
8. let root/COM float without support.
9. let ears/tail/wings/fleece run as independent noise oscillators.
10. make VFX carry emotion the body failed to express.
11. treat every appendage as equally important in every behavior.
12. use identical retargeted personality across four Grimo.
13. punish absence, create guilt, or use hostile care loops.
14. let physics determine silhouette or key pose.
15. let AI bypass identity/hero-motion Human Gate.
16. copy Pokémon exact pose, animation, signature timing or species acting.
17. optimize by deleting causality/attention/afterglow—the core experience.
18. expand to four characters before Carol proves the architecture.

## Carol is...

**A low, grounded dream-cloud companion who gently asks for affection; her tiny face acts first, her heavy hooves stay secure, and her enormous fleece answers later like a soft echo.**

## Jill is...

**An eager spring-dragon whose feeling starts in the chest, opens through wings and living foliage, and finally reaches a heavy rooted tail.**

## Pino is...

**A playful but self-directed soft otter whose body compresses with feeling, arms fold it inward, and a thick tail catches up after the moment has already begun.**

## Shushu is...

**A calm independent plush panda who lets emotion sink slowly into a seated body, while ears, crown, bouquet and flowers settle afterward with quiet weight.**

## When uncertain...

1. **Canonical wins.** If motion makes the character less itself, remove the motion.
2. **Cause before decoration.** Fix touch/attention/body causality before adding variants or VFX.
3. **Character before reuse.** Share runtime contracts, not personality performance.
4. **Quiet is allowed.** If two solutions are equally alive, prefer the one with less meaningless movement.
5. **Human Gate decides.** If metrics pass but the character feels like a puppet, it fails.

---

**End of authoritative specification.**
