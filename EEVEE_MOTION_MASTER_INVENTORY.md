# EEVEE_MOTION_MASTER_INVENTORY

> Scope: Partner Eevee 11-video corpus. This document normalizes only the eleven completed per-video Motion Inventories. It does not re-analyze MP4s and does not import Pokémon general knowledge, Pikachu data, Grimo/Carol specifications, web material, or unattached motions.

## 0. Source / Evidence Rules
- Formal source corpus: V01–V11 individual Eevee Motion Inventory Markdown files only.
- `[V1] / [V2] / [I]` distinctions from source inventories remain authoritative; this Master does not upgrade uncertainty.
- Duplicate exports, `(1)` files, URL-encoded duplicate names, and reuploads are not additional videos.
- VFX / audio / UI / cursor are context only and are never counted as Eevee body Motion.
- Master identity uses `Motion Family → Variant → Occurrence`. Source-local `Fxx`, `MF-xx`, `Mxxx` and timestamps are retained in traceability.
- Anatomical left/right is not invented when the source uses screen-left/screen-right.
- Occurrence totals are not blindly summed across parent/child phases; state/continuous layers remain lower-bound or uncounted when sources do not provide exact independent counts.

## 1. Source Corpus
| Video | Library source inventory | Source family count |
|---|---|---:|
| V01 | `EEVEE_MOTION_INVENTORY_01_【ピカブイ】イーブイとのふれあい【ポケモン Let's Go! イーブイ】_1080p30.md` | 25 |
| V02 | `EEVEE_MOTION_INVENTORY_02_【ピカブイ】イーブイとのハイタッチがかわいい！【ポケモン Let's Go! イーブイ】_1080p30.md` | 17 |
| V03 | `EEVEE_MOTION_INVENTORY_03_【ピカブイ】イーブイに進化の石を使うと...？【ポケモン Let's Go! イーブイ】_1080p30.md` | 25 |
| V04 | `EEVEE_MOTION_INVENTORY_04_【ピカブイ】バケツをかぶったイーブイ【ポケモン Let's Go! イーブイ】_1080p30.md` | 17 |
| V05 | `EEVEE_MOTION_INVENTORY_05_【ピカブイ】イーブイの嫌がるところを触り続けると...【ポケモン Let's Go! イーブイ】_1080p30.md` | 19 |
| V06 | `EEVEE_MOTION_INVENTORY_06_【ピカブイ】イーブイのほっぺすりすり【ポケモンレッツゴー イーブイ】_1080p30.md` | 10 |
| V07 | `EEVEE_MOTION_INVENTORY_07_【ピカブイ】イーブイの髪型まとめ！変更方法【ポケモンレッツゴー イーブイ】_1080p30.md` | 18 |
| V08 | `EEVEE_MOTION_INVENTORY_08_【ピカブイ】プリンの歌声で眠るイーブイ【ポケモンレッツゴー イーブイ】_1080p30.md` | 19 |
| V09 | `EEVEE_MOTION_INVENTORY_09_【ピカブイ】ぱっつんイーブイとのふれあい【ポケモンレッツゴー イーブイ】_1080p30.md` | 16 |
| V10 | `EEVEE_MOTION_INVENTORY_10_【ピカブイ】アフロイーブイとのふれあい【ポケモンレッツゴー イーブイ】_1080p30.md` | 24 |
| V11 | `EEVEE_MOTION_INVENTORY_11_【ピカブイ】ノリノリなイーブイ【ポケモンレッツゴー イーブイ】_1080p30.md` | 18 |

**Corpus audit:** 11 unique video identities; 208 source-local Family records mapped; duplicate exports excluded.

## 2. Executive Findings
- **Master Motion Families:** 77
- **Normalized Variants:** 156
- **Front-view readability:** HIGH 65 / MEDIUM 7 / LOW 5
- Positive contact is not a single animation: gentle holds, strong ear/body bursts, explicit two-lobe timing, retriggers, deep bow/rebound/paw-rise, head-lean/tilt, mouth-led responses and hero jump are mechanically separable.
- Negative/boundary behavior is likewise plural: uneasy warning, protest, strong face/ear reaction, sad hold, whole-body droop, half-lid disengagement, head withdrawal, side recoil, paw-thrust rejection, flinch and full turn-away are not collapsed.
- Stillness is functional motion/state vocabulary: neutral holds, contact latency/tolerance, side/profile holds, gift presentation, food processing pause, doze maintenance and delayed wake all remain explicit.
- Ears function as independent micro, emotion amplifier/follow-through, asymmetric rest micro and rest-state holder; tail evidence supports restrained micro/follow-through rather than an assumed constant wag.
- Rest vocabulary separates relaxed eye-close, doze entry/hold, ear switching within doze, distant sleep, sleep micro-cycle, delayed touch response and wake/startle.

## 3. Master Taxonomy Rules
- **Family:** shared meaning + major body mechanics + temporal grammar.
- **Variant:** same Family but a meaningful difference in amplitude, side, duration, entry, face/ear/paw participation, social context, settle or afterglow.
- **Occurrence:** a source-recorded concrete event identified by local occurrence ID and/or timestamp.
- Similar names do not force a merge; body mechanics and causality are decisive.
- Different UI/VFX/hairstyles alone do not create a new body-motion Family.
- Same/similar body performance under different causes may remain one Family with cause-specific Variants unless social function materially changes (e.g., reciprocal high-five vs generic paw lift).

## 4. Master Motion Family Catalog
| Global ID | Master Family | Category | Observable Definition | Key Variants | Video Coverage | Occurrence Count | Initiation | Lead Channel | Main Channels | Quiet Channels | Ear Role | Root / COM | Support | Tail Role | Temporal Form | Front View | Representative Sources | Confidence |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EEVEE-MF-001 | Neutral bilateral blink | A. Living / physiological | Short bilateral eyelid close followed by immediate reopen without a larger concurrent expressive action. | NEUTRAL_BLINK | 7/11 (COMMON) | at least 24 + recurrent/uncounted source occurrences | AUTONOMOUS | face | eyelids | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | pulse | HIGH | V02/BLINK, V03/F25, V05/BLINK, V06/F01, V08/BLINK… | HIGH |
| EEVEE-MF-002 | Context-linked short eye close | A. Living / physiological | Very short eye close embedded in, or immediately adjacent to, another action; source inventories do not always establish whether it is a physiological blink. | SHORT_CONTEXT_CLOSE | 4/11 (RECURRING) | exact-source subtotal 51 (phase overlap across source families not globally de-duplicated) | BOTH | face | eyelids | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | pulse | HIGH | V01/SHORT_EYELID_CLOSE, V04/F11, V05/EYE_CLOSE_SHORT, V07/BRIEF_EYE_CLOSE | HIGH |
| EEVEE-MF-003 | Idle body micro-sway | A. Living / physiological | Low-amplitude head/torso positional drift during otherwise neutral holding. | BODY_IDLE_MICRO_SWAY, IDLE_SWAY_LOOP | 2/11 (LIMITED) | recurrent/uncounted or state-based; no exact master total asserted | AUTONOMOUS | torso | head; torso; root/COM | hindlimbs unless listed; tail unless listed | QUIET | active | WEIGHT_SHIFT | QUIET | loop-like | MEDIUM | V04/F01, V07/BODY_IDLE_MICRO_SWAY | HIGH |
| EEVEE-MF-004 | Tail idle sway / swish | C. Ear / tail micro | Small or slow tail position change during idle/low-motion states; some sources treat it as a continuous layer rather than a discrete clip. | SLOW_TAIL_SWAY, TAIL_TORSO_COUPLED_SWAY | 6/11 (RECURRING) | at least 2 + recurrent/uncounted source occurrences | AUTONOMOUS | tail | tail; torso | channels not listed by source | QUIET | mostly stable / source-dependent | PLANTED | INDEPENDENT_MICRO | loop-like | LOW | V01/TAIL_SWAY_SUBTLE, V03/F14, V05/TAIL_IDLE_SWAY, V06/F10, V07/TAIL_IDLE_SWAY_SMALL… | HIGH |
| EEVEE-MF-005 | Independent single-ear flick | C. Ear / tail micro | Brief isolated one-ear movement with face/torso largely neutral. | EAR_FLICK_SINGLE | 1/11 (SINGLE-VIDEO) | exact-source subtotal 1 (phase overlap across source families not globally de-duplicated) | AUTONOMOUS | ear | ears L/R | hindlimbs unless listed; tail unless listed | independent micro | mostly stable / source-dependent | PLANTED | QUIET | pulse | HIGH | V01/EAR_FLICK_SINGLE | HIGH |
| EEVEE-MF-006 | Bilateral ear emotion/follow-through | C. Ear / tail micro | Bilateral ear lowering, outward rotation, or restoration coupled to another emotional/head/body action; not established as an independent clip in the relevant sources. | BILATERAL_EAR_LOWER, EAR_FOLLOW_OUTWARD | 2/11 (LIMITED) | recurrent/uncounted or state-based; no exact master total asserted | BOTH | ear | ears L/R; head | hindlimbs unless listed; tail unless listed | emotion amplifier / follow-through | mostly stable / source-dependent | PLANTED | QUIET | sequence | HIGH | V06/F05, V07/EAR_FOLLOW_OUTWARD | HIGH |
| EEVEE-MF-007 | Front neutral still hold | O. Intentional stillness | Front-facing low-motion baseline/WAIT-like hold with no large body action; small eye/ear/tail motion may remain. | FRONT_NEUTRAL_HOLD | 10/11 (COMMON) | at least 70 + recurrent/uncounted source occurrences | BOTH | full-body | full body / COM; eyes; ears L/R; tail | channels not listed by source | QUIET | mostly stable / source-dependent | PLANTED | QUIET | hold | HIGH | V01/MACRO_STILL_FRONT_NEUTRAL, V02/BASE_NEUTRAL_STILLNESS, V03/F05, V05/NEUTRAL_STILL, V06/F08… | HIGH |
| EEVEE-MF-008 | Touch latency / tolerate stillness | O. Intentional stillness | Player contact is present but Eevee intentionally remains near the current posture before another response or transition. | TOUCH_LATENCY_STILLNESS, TOUCH_TOLERATE_STILL | 2/11 (LIMITED) | at least 4 + recurrent/uncounted source occurrences | PLAYER_TRIGGERED | full-body | full body / COM; eyes; ears L/R | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | hold | HIGH | V04/F02, V09/F07 | HIGH |
| EEVEE-MF-009 | Side/profile still hold | O. Intentional stillness | Non-front-facing side/profile waiting state with little gross motion. | SIDE_IDLE, SIDE_PROFILE_STATE, STILLNESS_ROOM | 3/11 (RECURRING) | exact-source subtotal 7 (phase overlap across source families not globally de-duplicated) | BOTH | full-body | full body / COM; head; eyes; ears L/R; tail | channels not listed by source | QUIET | mostly stable / source-dependent | PLANTED | QUIET | hold | LOW | V03/F03, V05/SIDE_PROFILE_STATE, V08/STILLNESS_ROOM | HIGH |
| EEVEE-MF-010 | Close-up forepaw rest/presentation hold | O. Intentional stillness | UI-linked close-up state in which forepaws are placed toward the viewer and held with little further action. | CLOSEUP_FOREPAW_REST | 1/11 (SINGLE-VIDEO) | exact-source subtotal 2 (phase overlap across source families not globally de-duplicated) | SYSTEM / TRANSITION | forepaw | forelimb L/R; forepaw L/R; eyes | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | hold | HIGH | V03/F02 | HIGH |
| EEVEE-MF-011 | Hand-oriented attention candidate | B. Attention / gaze | Possible attention/gaze orientation toward the visible hand cursor; eye-only displacement is not strongly established. | GAZE_ORIENT_TO_HAND_CANDIDATE | 1/11 (SINGLE-VIDEO) | exact-source subtotal 1 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | face | eyes; head | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | hold | MEDIUM | V01/GAZE_ORIENT_TO_HAND_CANDIDATE | MEDIUM |
| EEVEE-MF-012 | Open-mouth attention hold | B. Attention / gaze | Open-eyed/open-mouth attention-like hold with little limb displacement; cause is unresolved in the source occurrence(s). | MOUTH_OPEN_ATTENTION, MOUTH_OPEN_ROUND | 2/11 (LIMITED) | exact-source subtotal 2 (phase overlap across source families not globally de-duplicated) | UNKNOWN | face | mouth; eyes; head | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | hold | HIGH | V07/MOUTH_OPEN_ROUND, V08/MOUTH_OPEN_ATTENTION | HIGH |
| EEVEE-MF-013 | Autonomous curious head tilt | F. Autonomous idle | Input-free or autonomous-candidate head/neck tilt with a held side inclination and return; sources preserve screen-side rather than inventing anatomical L/R. | AUTONOMOUS_TILT, CURIOUS_TILT, DROWSY_TILT, SCREEN_RIGHT_LONG_TILT… | 7/11 (COMMON) | exact-source subtotal 12 (phase overlap across source families not globally de-duplicated) | AUTONOMOUS | head | head; neck; eyes; ears L/R; mouth | hindlimbs unless listed; tail unless listed | follow-through | active | WEIGHT_SHIFT | QUIET | anticipation_action_settle | HIGH | V01/HEAD_TILT_SCREEN_RIGHT, V02/IDLE_DROWSY_HEAD_TILT, V03/F16, V05/AUTO_HEAD_TILT_LONG, V07/HEAD_TILT_R… | HIGH |
| EEVEE-MF-014 | Autonomous head sway / shake | F. Autonomous idle | Input-free closed-eye or relaxed head movement through more than one lateral direction before re-centering. | AUTO_HEAD_SHAKE_SWAY, IDLE_HEAD_SWAY | 2/11 (LIMITED) | exact-source subtotal 3 (phase overlap across source families not globally de-duplicated) | AUTONOMOUS | head | head; neck; eyelids; ears L/R; torso | hindlimbs unless listed; tail unless listed | follow-through | active | WEIGHT_SHIFT | QUIET | sequence | HIGH | V05/AUTO_HEAD_SHAKE_SWAY, V11/F16 | HIGH |
| EEVEE-MF-015 | Autonomous/contented smile hold | F. Autonomous idle | Input-free or startup-uncertain closed-eye smile with limited gross body displacement and possible ear relaxation. | AUTONOMOUS_HAPPY_SMILE, AUTO_HAPPY_SMILE_IDLE, ENTRY_HAPPY_GREETING, IDLE_CONTENTED_SMILE_EAR_SPREAD… | 5/11 (RECURRING) | exact-source subtotal 8 (phase overlap across source families not globally de-duplicated) | AUTONOMOUS | face | eyes; mouth; head; ears L/R | hindlimbs unless listed; tail unless listed | emotion amplifier | mostly stable / source-dependent | PLANTED | QUIET | hold | HIGH | V01/IDLE_CONTENTED_SMILE_EAR_SPREAD, V03/F15, V05/ENTRY_HAPPY_GREETING, V05/AUTO_HAPPY_SMILE_IDLE, V10/INITIAL_HAPPY_HOLD… | HIGH |
| EEVEE-MF-016 | Autonomous bilateral forepaw lift | G. Autonomous social | Both forepaws rise toward the viewer, usually with mouth opening, then lower back toward neutral; includes startup/autonomous-context variants when mechanics match. | BIPAW_FRONT_LIFT, STARTUP_BIPAW_SMILE | 4/11 (RECURRING) | exact-source subtotal 7 (phase overlap across source families not globally de-duplicated) | CHARACTER_INITIATED_SOCIAL | forepaw | forelimb L/R; forepaw L/R; mouth; head; torso | hindlimbs unless listed; tail unless listed | QUIET | active | WEIGHT_SHIFT | QUIET | anticipation_action_settle | HIGH | V01/BOTH_FOREPAW_LIFT_FORWARD, V06/F06, V10/IDLE_FOREPAW_GESTURE, V11/F02 | HIGH |
| EEVEE-MF-017 | Autonomous single-forepaw raise | G. Autonomous social | One forepaw rises toward the viewer and returns without confirmed reciprocal contact. | FOREPAW_RAISE_R | 1/11 (SINGLE-VIDEO) | exact-source subtotal 6 (phase overlap across source families not globally de-duplicated) | CHARACTER_INITIATED_SOCIAL | forepaw | forelimb L/R; forepaw L/R; mouth; head | hindlimbs unless listed; tail unless listed | QUIET | active | WEIGHT_SHIFT | QUIET | pulse | HIGH | V07/FOREPAW_RAISE_R | HIGH |
| EEVEE-MF-018 | Autonomous/unknown deep bow → bilateral paw rise | G. Autonomous social | Deep forward bow followed by a bilateral forepaw/paw-pad presentation and closed-eye settling, where touch causality is not established. | BOW_BIPAW_SEQUENCE, DEEP_BOW_FOREPAW_RISE | 2/11 (LIMITED) | exact-source subtotal 5 (phase overlap across source families not globally de-duplicated) | CHARACTER_INITIATED_SOCIAL | full-body | head; torso; root/COM; forelimb L/R; forepaw L/R; ears L/R | hindlimbs unless listed; tail unless listed | follow-through | active | WEIGHT_SHIFT | QUIET | sequence | HIGH | V07/BOW_BIPAW_SEQUENCE, V11/F09 | HIGH |
| EEVEE-MF-019 | Relaxed long eye-close moving hold | Q. Rest / doze / sleep | Several-second relaxed eye-close with ears lowered/outward and slow head/torso settling or sway; shallower/shorter than the clearly deep doze state when source distinguishes them. | BRIEF_RELAXED_EYE_CLOSE_EAR_DROOP, IDLE_LONG_RELAX_EAR_DROOP, IDLE_RELAXED_EYECLOSE_SWAY, RELAXED_CLOSE_SWAY… | 5/11 (RECURRING) | exact-source subtotal 7 (phase overlap across source families not globally de-duplicated) | AUTONOMOUS | head | eyelids; ears L/R; head; torso; root/COM | hindlimbs unless listed; tail unless listed | rest state | active | WEIGHT_SHIFT | QUIET | moving_hold | HIGH | V01/BRIEF_RELAXED_EYE_CLOSE_EAR_DROOP, V06/F07, V07/RELAXED_CLOSE_SWAY, V10/RELAXED_EYE_CLOSE_LONG, V11/F17 | HIGH |
| EEVEE-MF-020 | Doze/drowsy entry | Q. Rest / doze / sleep | Transition from neutral toward rest, commonly eyelids first, then head lowering and ear-state change. | DOZE_ENTRY, DROWSY_ONSET | 2/11 (LIMITED) | exact-source subtotal 2 (phase overlap across source families not globally de-duplicated) | AUTONOMOUS | head | eyelids; head; ears L/R; neck; root/COM | hindlimbs unless listed; tail unless listed | rest state | active | WEIGHT_SHIFT | QUIET | single_transition | HIGH | V01/DOZE_ENTRY, V03/F17 | HIGH |
| EEVEE-MF-021 | Deep doze / drowsy hold | Q. Rest / doze / sleep | Long closed-eye low-activity hold with head/body lowered or swaying; distinct from short relaxed eye-close where sources distinguish depth/duration. | DOZE_BOW_HOLD, DOZE_HOLD, DROWSY_SWAY_LONG | 3/11 (RECURRING) | exact-source subtotal 3 (phase overlap across source families not globally de-duplicated) | AUTONOMOUS | full-body | eyelids; head; ears L/R; torso; root/COM | hindlimbs unless listed; tail unless listed | rest state | mostly stable / source-dependent | PLANTED | QUIET | moving_hold | HIGH | V01/DOZE_HOLD, V03/F18, V10/DOZE_BOW_HOLD | HIGH |
| EEVEE-MF-022 | Ear switching inside doze | Q. Rest / doze / sleep | Repeated asymmetric ear-state switching while the rest of the body remains in a doze hold. | DOZE_EAR_SWITCH_CYCLE | 1/11 (SINGLE-VIDEO) | recurrent/uncounted or state-based; no exact master total asserted | AUTONOMOUS | ear | ears L/R; eyelids; head | hindlimbs unless listed; tail unless listed | asymmetric rest micro | mostly stable / source-dependent | PLANTED | QUIET | loop-like | HIGH | V01/DOZE_EAR_SWITCH_CYCLE | HIGH |
| EEVEE-MF-023 | Distant sleep stillness | Q. Rest / doze / sleep | Distant-view sleep state with very little body motion; screen sleep symbols are excluded as body motion. | SLEEP_STILLNESS_DISTANT | 1/11 (SINGLE-VIDEO) | exact-source subtotal 2 (phase overlap across source families not globally de-duplicated) | AUTONOMOUS | full-body | full body / COM | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | hold | LOW | V08/SLEEP_STILLNESS_DISTANT | HIGH |
| EEVEE-MF-024 | Sleep micro-cycle | Q. Rest / doze / sleep | Repeated small mouth-area/head/upper-body cycle observed while eyes remain closed in sleep. | SLEEP_MICRO_CYCLE | 1/11 (SINGLE-VIDEO) | exact-source subtotal 18 (phase overlap across source families not globally de-duplicated) | AUTONOMOUS | face | mouth; head; torso; eyelids | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | loop-like | MEDIUM | V08/SLEEP_MICRO_CYCLE | HIGH |
| EEVEE-MF-025 | Touch during rest with delayed/no immediate response | O. Intentional stillness | Touch occurs during doze/rest but the existing rest pose is maintained for a measurable interval before waking. | TOUCH_DURING_DOZE_NO_IMMEDIATE_RESPONSE | 1/11 (SINGLE-VIDEO) | exact-source subtotal 1 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | full-body | eyelids; head; ears L/R; torso | hindlimbs unless listed; tail unless listed | rest state | mostly stable / source-dependent | PLANTED | QUIET | hold | HIGH | V10/TOUCH_DURING_DOZE_NO_IMMEDIATE_RESPONSE | HIGH |
| EEVEE-MF-026 | Wake/startle transition | Q. Rest / doze / sleep | Rest state ends with opening eyes and raising/reorienting the head, sometimes with open mouth/startle and secondary body movement. | TOUCH_WAKE_RESPONSE, WAKE_ON_TOUCH_STARTLE, WAKE_STARTLE | 3/11 (RECURRING) | exact-source subtotal 3 (phase overlap across source families not globally de-duplicated) | BOTH | head | eyes; eyelids; head; mouth; ears L/R; torso | hindlimbs unless listed; tail unless listed | follow-through | active | WEIGHT_SHIFT | QUIET | single_transition | HIGH | V01/WAKE_ON_TOUCH_STARTLE, V03/F19, V10/TOUCH_WAKE_RESPONSE | HIGH |
| EEVEE-MF-027 | Positive-touch onset | H. Positive touch | Short transition from contact/neutral into a positive closed-eye state; sources preserve cases where mouth or eyelids clearly lead. | CHEEK_TOUCH_TO_HAPPY, PET_PLEASURE_ONSET | 1/11 (SINGLE-VIDEO) | exact-source subtotal 4 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | face | mouth; eyelids; head | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | single_transition | HIGH | V04/F03, V04/F09 | HIGH |
| EEVEE-MF-028 | Gentle positive touch hold | H. Positive touch | Contact-associated closed-eye smile/pleasant hold with limited COM excursion and no deep bow. | BLISS_HOLD, GENTLE_CALM_RUB, GENTLE_CLOSED_EYE_HOLD, PLEASURE_HOLD… | 9/11 (COMMON) | at least 68 + recurrent/uncounted source occurrences | PLAYER_TRIGGERED | face | eyelids; mouth; head; ears L/R | hindlimbs unless listed; tail unless listed | emotion amplifier | mostly stable / source-dependent | PLANTED | QUIET | hold | HIGH | V01/TOUCH_RELAXED_EYES_CLOSED_SMILE, V02/TOUCH_POSITIVE_CLOSED_EYE_SMILE, V03/F07, V03/F09, V04/F04… | HIGH |
| EEVEE-MF-029 | Strong positive touch burst | H. Positive touch | Contact-associated large smile with stronger ear splay and head/torso bob/lift than the gentle hold, but without the deep bow→paw-rise grammar. | BURST_DIP_PHASE, BURST_JOY_PHASE, EAR_SPREAD_BOUNCE, EAR_SPREAD_BURST… | 8/11 (COMMON) | at least 80 + recurrent/uncounted source occurrences | PLAYER_TRIGGERED | mixed | eyelids; mouth; ears L/R; head; torso; root/COM | hindlimbs unless listed; tail unless listed | emotion amplifier | active | WEIGHT_SHIFT | QUIET | anticipation_action_settle | HIGH | V01/TOUCH_POSITIVE_BURST_EAR_SPREAD, V02/TOUCH_POSITIVE_EFFECT_REACTION, V02/SPECIAL_HEART_JOY, V03/F10, V04/F05… | HIGH |
| EEVEE-MF-030 | Two-lobe positive touch sequence | H. Positive touch | Positive touch performance explicitly recorded as first closed-eye smile lobe, brief reset/opening, then second lobe. | TOUCH_POSITIVE_FULL | 1/11 (SINGLE-VIDEO) | exact-source subtotal 18 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | mixed | eyelids; mouth; ears L/R; head; torso | hindlimbs unless listed; tail unless listed | emotion amplifier | mostly stable / source-dependent | PLANTED | QUIET | sequence | HIGH | V10/TOUCH_POSITIVE_FULL | HIGH |
| EEVEE-MF-031 | Positive touch retrigger | H. Positive touch | Additional closed-eye positive pulse after a prior full reaction and a short reset, preserved because source explicitly separated the retrigger. | TOUCH_POSITIVE_RETRIGGER | 1/11 (SINGLE-VIDEO) | exact-source subtotal 1 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | face | eyelids; mouth; ears L/R; head | hindlimbs unless listed; tail unless listed | emotion amplifier | mostly stable / source-dependent | PLANTED | QUIET | pulse | HIGH | V10/TOUCH_POSITIVE_RETRIGGER | HIGH |
| EEVEE-MF-032 | Touch-linked deep bow → rebound/paw rise | H. Positive touch | Touch-associated large sequence with deep bow/compression, rebound/upright recovery and bilateral forepaw participation; retained separately from autonomous bow/paw sequences. | BOW_PAWS_TOGETHER, BOW_PAW_POP, DEEP_BOW_REBOUND | 3/11 (RECURRING) | at least 6 + recurrent/uncounted source occurrences | PLAYER_TRIGGERED | full-body | head; torso; root/COM; forelimb L/R; forepaw L/R; ears L/R; eyelids; mouth | hindlimbs unless listed; tail unless listed | emotion amplifier / follow-through | active | WEIGHT_SHIFT | QUIET | sequence | HIGH | V06/F03, V09/F06, V10/TOUCH_BOW_PAW_POP | HIGH |
| EEVEE-MF-033 | Touch head-lean / tilt response | H. Positive touch | Contact-associated head/neck lean or tilt held toward/away from the contact direction without the full negative withdrawal grammar. | TOUCH_HEAD_LEAN_RELAX, TOUCH_HEAD_TILT_FOLLOW, TOUCH_HEAD_TILT_OPEN_SMILE, TOUCH_HEAD_TILT_RESPONSE | 4/11 (RECURRING) | at least 3 + recurrent/uncounted source occurrences | PLAYER_TRIGGERED | head | head; neck; eyelids; ears L/R | hindlimbs unless listed; tail unless listed | follow-through | active | WEIGHT_SHIFT | QUIET | sequence | HIGH | V01/TOUCH_HEAD_LEAN_RELAX, V02/TOUCH_HEAD_TILT_FOLLOW, V03/F06, V09/F04 | HIGH |
| EEVEE-MF-034 | Touch open-mouth small/hold response | H. Positive touch | Touch-associated open-mouth response with limited gross body action; emotional valence is not assumed when the source leaves it unresolved. | CHEEK_TOUCH_OPEN_MOUTH_HOLD, TOUCH_MOUTH_OPEN_MILD, TOUCH_MOUTH_OPEN_SMALL | 3/11 (RECURRING) | exact-source subtotal 18 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | face | mouth; eyes; head | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | hold | HIGH | V02/TOUCH_MOUTH_OPEN_MILD, V04/F08, V10/TOUCH_MOUTH_OPEN_SMALL | HIGH |
| EEVEE-MF-035 | Touch surprise/open-mouth → smile | H. Positive touch | Touch response that begins with open-eyed/open-mouth surprise/attention and then resolves into a positive smile. | TOUCH_FACE_OPEN_MOUTH_RECOVER, TOUCH_SURPRISE_TO_SMILE | 2/11 (LIMITED) | exact-source subtotal 9 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | face | mouth; eyes; eyelids; head; ears L/R | hindlimbs unless listed; tail unless listed | emotion amplifier | mostly stable / source-dependent | PLANTED | QUIET | sequence | HIGH | V03/F08, V11/F06 | HIGH |
| EEVEE-MF-036 | Touch-linked forepaw lift/offer | E. Forelimb / paw gesture | One or both forepaws lift toward the viewer during touch/contact context without confirmed reciprocal contact. | FOREPAW_LIFT_SMALL, SMALL_PAW_LIFT_RESPONSE, TOUCH_FOREPAW_LIFT_SHIFT, TOUCH_PAW_OFFER… | 5/11 (RECURRING) | at least 7 + recurrent/uncounted source occurrences | PLAYER_TRIGGERED | forepaw | forelimb L/R; forepaw L/R; mouth; head; torso | hindlimbs unless listed; tail unless listed | QUIET | active | WEIGHT_SHIFT | QUIET | pulse | HIGH | V01/TOUCH_SINGLE_FOREPAW_LIFT, V05/FOREPAW_LIFT_SMALL, V09/F05, V10/TOUCH_PAW_OFFER, V11/F07 | HIGH |
| EEVEE-MF-037 | Small touch-linked eye-close/sink | H. Positive touch | Small touch-linked eye close with slight head/torso lowering, kept separate where source inventories did not equate it with a smiling hold. | TOUCH_CLOSE_SMALL | 1/11 (SINGLE-VIDEO) | exact-source subtotal 2 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | head | eyelids; head; torso; ears L/R | hindlimbs unless listed; tail unless listed | follow-through | active | WEIGHT_SHIFT | QUIET | pulse | HIGH | V07/TOUCH_CLOSE_SMALL | HIGH |
| EEVEE-MF-038 | Positive jump hero response | M. Large emotional / hero | Large positive reaction where the whole body rises enough that feet appear to leave the ground. | TOUCH_POSITIVE_JUMP | 1/11 (SINGLE-VIDEO) | exact-source subtotal 1 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | full-body | full body / COM; hindlimb L/R; head; ears L/R; face | hindlimbs unless listed; tail unless listed | emotion amplifier | active | SUPPORT_CHANGE | QUIET | anticipation_action_settle | HIGH | V11/F13 | HIGH |
| EEVEE-MF-039 | Small uneasy facial warning | I. Negative / boundary touch | Small negative/uneasy facial change without a large body withdrawal. | TOUCH_UNEASY_FACE_SMALL | 1/11 (SINGLE-VIDEO) | exact-source subtotal 1 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | face | eyes; mouth; head | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | hold | HIGH | V01/TOUCH_UNEASY_FACE_SMALL | HIGH |
| EEVEE-MF-040 | Angry/protest facial burst | I. Negative / boundary touch | Negative reaction led by sharper eye/face shape and mouth opening, with limited whole-body displacement. | NEGATIVE_ANGRY_BURST, TOUCH_NEGATIVE_PROTEST_FACE | 2/11 (LIMITED) | exact-source subtotal 5 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | face | eyes; mouth; head; ears L/R | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | sequence | HIGH | V01/TOUCH_NEGATIVE_PROTEST_FACE, V05/NEGATIVE_ANGRY_BURST | HIGH |
| EEVEE-MF-041 | Strong closed-eye/ear-splay negative face | I. Negative / boundary touch | Strong touch-negative face/ear reaction with forceful eye closure/ear lateralization but without the deeper whole-body droop/recoil grammars. | TOUCH_NEGATIVE_STRONG | 1/11 (SINGLE-VIDEO) | exact-source subtotal 7 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | face | eyelids; ears L/R; mouth; head; torso | hindlimbs unless listed; tail unless listed | emotion amplifier | active | WEIGHT_SHIFT | QUIET | sequence | HIGH | V02/TOUCH_NEGATIVE_STRONG | HIGH |
| EEVEE-MF-042 | Sad/downcast negative face hold | I. Negative / boundary touch | Sustained sad/concerned facial state while gross posture remains comparatively upright. | NEGATIVE_SAD_FACE_STATE | 1/11 (SINGLE-VIDEO) | exact-source subtotal 5 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | face | eyes; mouth; head | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | hold | HIGH | V05/NEGATIVE_SAD_FACE_STATE | HIGH |
| EEVEE-MF-043 | Negative droop / body sink | I. Negative / boundary touch | Negative response in which ears/head and then torso/COM move downward into a lower held posture before recovery. | NEGATIVE_DROOP, TOUCH_NEGATIVE_SINK_EAR_DROOP | 2/11 (LIMITED) | exact-source subtotal 5 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | full-body | head; ears L/R; torso; root/COM; eyelids | hindlimbs unless listed; tail unless listed | emotion amplifier | active | WEIGHT_SHIFT | QUIET | sequence | HIGH | V01/TOUCH_NEGATIVE_SINK_EAR_DROOP, V05/NEGATIVE_DROOP | HIGH |
| EEVEE-MF-044 | Half-lid/downcast disengagement hold | I. Negative / boundary touch | Half-lidded/downcast negative or ambiguous state maintained without a large recoil. | ANNOYED_HALF_LID_STATE, BRIEF_HALF_LID_DOWNCAST_FACE | 2/11 (LIMITED) | at least 5 + recurrent/uncounted source occurrences | PLAYER_TRIGGERED | face | eyelids; eyes; head; mouth | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | hold | HIGH | V05/ANNOYED_HALF_LID_STATE, V09/F08 | HIGH |
| EEVEE-MF-045 | Face-touch withdrawal head tilt | I. Negative / boundary touch | Face/nose touch followed by eye close and a large lateral head withdrawal/tilt, then dissatisfied/half-lid recovery. | TOUCH_FACE_WITHDRAW_TILT | 1/11 (SINGLE-VIDEO) | exact-source subtotal 1 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | head | head; neck; eyelids; mouth | hindlimbs unless listed; tail unless listed | QUIET | active | WEIGHT_SHIFT | QUIET | sequence | HIGH | V11/F04 | HIGH |
| EEVEE-MF-046 | Side recoil / rotate away-to-front | I. Negative / boundary touch | From a side/profile state, head/body recoil and rotate sharply with substantial root/COM participation before settling. | SIDE_RECOIL_ROTATE | 1/11 (SINGLE-VIDEO) | exact-source subtotal 1 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | full-body | head; torso; root/COM; forelimb L/R; ears L/R; tail | channels not listed by source | QUIET | active | TURN | FOLLOW_THROUGH | sequence | MEDIUM | V05/SIDE_RECOIL_ROTATE | HIGH |
| EEVEE-MF-047 | Strong rejection with paw/feet thrust | I. Negative / boundary touch | Large rejection sequence with sharp negative face, major whole-body motion and visible paw/foot-pad thrust toward the camera. | STRONG_REJECTION_PAW_THRUST | 1/11 (SINGLE-VIDEO) | exact-source subtotal 1 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | full-body | full body / COM; feet / support; face; ears L/R | hindlimbs unless listed; tail unless listed | emotion amplifier | active | SUPPORT_CHANGE | QUIET | sequence | HIGH | V05/STRONG_REJECTION_PAW_THRUST | HIGH |
| EEVEE-MF-048 | Impact-like face flinch | I. Negative / boundary touch | Brief strong eye closure and small head retraction synchronized with touch/context; screen effects are not counted as body motion. | TOUCH_FACE_IMPACT_FLINCH | 1/11 (SINGLE-VIDEO) | exact-source subtotal 1 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | head | eyelids; head; mouth | hindlimbs unless listed; tail unless listed | QUIET | active | WEIGHT_SHIFT | QUIET | pulse | HIGH | V11/F08 | HIGH |
| EEVEE-MF-049 | Full-body turn away | I. Negative / boundary touch | Large whole-body rotation from front toward back/away after interaction context. | TURN_AWAY_FULL | 1/11 (SINGLE-VIDEO) | exact-source subtotal 1 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | full-body | full body / COM; head; ears L/R; tail; feet / support | channels not listed by source | QUIET | active | TURN | FOLLOW_THROUGH | single_transition | LOW | V08/TURN_AWAY_FULL | HIGH |
| EEVEE-MF-050 | Turn return with bilateral paw presentation | M. Large emotional / hero | Return from back-facing orientation to front while raising both forepaws, ending in a frontal peak. | TURN_RETURN_DOUBLE_PAW | 1/11 (SINGLE-VIDEO) | exact-source subtotal 1 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | full-body | full body / COM; forelimb L/R; forepaw L/R; head; ears L/R | hindlimbs unless listed; tail unless listed | follow-through | active | TURN | QUIET | sequence | HIGH | V08/TURN_RETURN_DOUBLE_PAW | HIGH |
| EEVEE-MF-051 | Reciprocal paw offer / WAIT | J. Reciprocal social interaction | Forepaw is presented and held toward the player as an explicit reciprocal-interaction offer/WAIT state. | HIGH_FIVE_PAW_OFFER_HOLD, SINGLE_FOREPAW_REACH_FORWARD | 2/11 (LIMITED) | exact-source subtotal 5 (phase overlap across source families not globally de-duplicated) | RECIPROCAL | forepaw | forelimb L/R; forepaw L/R; head; eyes | hindlimbs unless listed; tail unless listed | QUIET | active | WEIGHT_SHIFT | QUIET | moving_hold | HIGH | V01/SINGLE_FOREPAW_REACH_FORWARD, V02/HIGH_FIVE_PAW_OFFER_HOLD | HIGH |
| EEVEE-MF-052 | High-five contact acknowledgment | J. Reciprocal social interaction | Player contact occurs on the presented paw; kept separate from the offer/WAIT and post-contact facial payoff. | HIGH_FIVE_CONTACT | 1/11 (SINGLE-VIDEO) | recurrent/uncounted or state-based; no exact master total asserted | RECIPROCAL | forepaw | forepaw L/R; face | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | pulse | HIGH | V02/HIGH_FIVE_CONTACT | HIGH |
| EEVEE-MF-053 | High-five success smile | J. Reciprocal social interaction | Short closed-eye smile immediately following successful paw contact. | HIGH_FIVE_SUCCESS_SMILE | 1/11 (SINGLE-VIDEO) | exact-source subtotal 3 (phase overlap across source families not globally de-duplicated) | RECIPROCAL | face | eyelids; mouth; head; forepaw L/R | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | pulse | HIGH | V02/HIGH_FIVE_SUCCESS_SMILE | HIGH |
| EEVEE-MF-054 | High-five alternate post-contact response | J. Reciprocal social interaction | Observed post-contact mouth/eye response that differs from the typical success smile; meaning remains unresolved. | HIGH_FIVE_ALT_RESPONSE | 1/11 (SINGLE-VIDEO) | exact-source subtotal 1 (phase overlap across source families not globally de-duplicated) | RECIPROCAL | face | mouth; eyes; head; forepaw L/R | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | pulse | HIGH | V02/HIGH_FIVE_ALT_RESPONSE | HIGH |
| EEVEE-MF-055 | Food notice / presentation wait | K. Feeding | Food is presented/approaches while Eevee attends or waits before mouth contact; source certainty about independent notice motion varies. | FOOD_NOTICE, FOOD_PRESENT_ATTEND, FOOD_PRESENT_WAIT | 3/11 (RECURRING) | exact-source subtotal 3 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | face | eyes; mouth; head | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | hold | HIGH | V02/FOOD_PRESENT_WAIT, V08/FOOD_NOTICE, V09/F09 | HIGH |
| EEVEE-MF-056 | Food contact / receive / mouth hold | K. Feeding | Food contacts or is held at the mouth; mouth/head carry the action while torso remains comparatively stable. | FOOD_CONSUME_TRANSITION, FOOD_CONTACT_EAT, FOOD_CONTACT_HOLD, FOOD_HELD_AT_MOUTH… | 6/11 (RECURRING) | exact-source subtotal 9 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | face | mouth; head; eyes | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | moving_hold | HIGH | V01/FOOD_CONTACT_EAT, V03/F11, V08/FOOD_RECEIVE, V08/FOOD_HOLD_CHEW, V09/F10… | HIGH |
| EEVEE-MF-057 | Post-food processing pause | K. Feeding | Food disappears/contact ends and Eevee holds nearly still for a short beat before emotional evaluation/response. | POST_FOOD_PAUSE | 5/11 (RECURRING) | exact-source subtotal 7 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | full-body | full body / COM; mouth; eyes; ears L/R | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | hold | HIGH | V01/FOOD_POST_EAT_PAUSE, V03/F12, V08/FOOD_PROCESS_PAUSE, V10/FOOD_PROCESS_STILL, V11/F11 | HIGH |
| EEVEE-MF-058 | Food-positive response | K. Feeding | Post-food positive response, usually closed-eye smile with ear splay and small head/torso accent; tilt variants are retained. | FOOD_HAPPY_STANDARD, FOOD_HAPPY_TILT | 7/11 (COMMON) | exact-source subtotal 9 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | mixed | eyelids; mouth; ears L/R; head; torso | hindlimbs unless listed; tail unless listed | emotion amplifier | active | WEIGHT_SHIFT | QUIET | anticipation_action_settle | HIGH | V01/FOOD_HAPPY_BURST, V02/FOOD_POST_EAT_JOY, V03/F13, V08/FOOD_HAPPY, V09/F11… | HIGH |
| EEVEE-MF-059 | Gift/item presentation hold | L. Gift / item | Gift/object is held centrally with forepaws toward the player for a sustained presentation. | GIFT_FRONT_HOLD | 4/11 (RECURRING) | exact-source subtotal 4 (phase overlap across source families not globally de-duplicated) | CHARACTER_INITIATED_SOCIAL | forepaw | forelimb L/R; forepaw L/R; eyes; head; torso | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | hold | HIGH | V03/F21, V09/F13, V10/GIFT_HOLD, V11/F14 | HIGH |
| EEVEE-MF-060 | Gift-holding smile | L. Gift / item | Eyes close into a pleased smile while the item remains presented/held. | GIFT_HOLD_SMILE | 3/11 (RECURRING) | exact-source subtotal 3 (phase overlap across source families not globally de-duplicated) | CHARACTER_INITIATED_SOCIAL | face | eyelids; mouth; ears L/R; forepaw L/R; head | hindlimbs unless listed; tail unless listed | emotion amplifier | mostly stable / source-dependent | PLANTED | QUIET | hold | HIGH | V03/F22, V09/F14, V10/GIFT_CLOSE_EYE_SMILE | HIGH |
| EEVEE-MF-061 | Gift lower/release transition | L. Gift / item | Gift/object lowers or disappears while forepaw/face state transitions away from presentation. | GIFT_LOWER_SMILE, GIFT_RELEASE_RECOVERY | 2/11 (LIMITED) | exact-source subtotal 2 (phase overlap across source families not globally de-duplicated) | SYSTEM / TRANSITION | forepaw | forepaw L/R; eyelids; head; mouth | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | single_transition | HIGH | V09/F15, V11/F15 | HIGH |
| EEVEE-MF-062 | Gift afterglow / result smile | L. Gift / item | Positive facial state persists or reappears after the gift disappears or result UI resolves. | GIFT_AFTERGLOW, GIFT_RESULT_SMILE | 3/11 (RECURRING) | exact-source subtotal 4 (phase overlap across source families not globally de-duplicated) | BOTH | face | eyelids; mouth; head; ears L/R | hindlimbs unless listed; tail unless listed | emotion amplifier | mostly stable / source-dependent | PLANTED | QUIET | hold | HIGH | V03/F23, V03/F24, V09/F16, V10/POST_GIFT_HAPPY | HIGH |
| EEVEE-MF-063 | Entry / pop-up / appear-settle | P. Transition | Scene/startup transition where Eevee rises/appears into view or settles into the interaction camera; editor/UI causality is preserved. | ENTRY_APPEAR_SETTLE, INTRO_POP_UP, POP_UP_GREETING | 3/11 (RECURRING) | exact-source subtotal 5 (phase overlap across source families not globally de-duplicated) | SYSTEM / TRANSITION | full-body | full body / COM; head; forelimb L/R; ears L/R; mouth | hindlimbs unless listed; tail unless listed | QUIET | active | SUPPORT_CHANGE | QUIET | single_transition | HIGH | V02/INTRO_POP_UP, V03/F01, V06/F02 | HIGH |
| EEVEE-MF-064 | Special backward recoil | M. Large emotional / hero | One-off special sequence phase with major backward whole-body lean/recoil and COM movement. | SPECIAL_BACKWARD_RECOIL | 1/11 (SINGLE-VIDEO) | exact-source subtotal 1 (phase overlap across source families not globally de-duplicated) | SYSTEM / TRANSITION | full-body | torso; head; root/COM; ears L/R; feet / support | hindlimbs unless listed; tail unless listed | follow-through | active | WEIGHT_SHIFT | QUIET | single_transition | MEDIUM | V04/F12 | HIGH |
| EEVEE-MF-065 | Special forepaw-lift accent | M. Large emotional / hero | One-forepaw high lift/paw-pad accent embedded in the special recoil sequence; source marks independence as uncertain/submotion candidate. | SPECIAL_FOREPAW_LIFT | 1/11 (SINGLE-VIDEO) | exact-source subtotal 1 (phase overlap across source families not globally de-duplicated) | SYSTEM / TRANSITION | forepaw | forelimb L/R; forepaw L/R; torso | hindlimbs unless listed; tail unless listed | QUIET | active | WEIGHT_SHIFT | QUIET | pulse | HIGH | V04/F13 | HIGH |
| EEVEE-MF-066 | Special forward bow | M. Large emotional / hero | Deep forward bow phase following the special recoil context, with head/torso/COM and ear participation. | SPECIAL_FORWARD_BOW | 1/11 (SINGLE-VIDEO) | exact-source subtotal 1 (phase overlap across source families not globally de-duplicated) | SYSTEM / TRANSITION | full-body | head; torso; root/COM; ears L/R | hindlimbs unless listed; tail unless listed | follow-through | active | WEIGHT_SHIFT | QUIET | single_transition | HIGH | V04/F14 | HIGH |
| EEVEE-MF-067 | Special startle open-mouth face | M. Large emotional / hero | Special-sequence open-eyed/open-mouth startle/attention face when the character becomes visible. | SPECIAL_STARTLE_OPEN_MOUTH | 1/11 (SINGLE-VIDEO) | exact-source subtotal 1 (phase overlap across source families not globally de-duplicated) | SYSTEM / TRANSITION | face | mouth; eyes; head | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | pulse | HIGH | V04/F17 | HIGH |
| EEVEE-MF-068 | Special closed-eye smile hold | M. Large emotional / hero | Closed-eye smile hold inside a special sequence; kept distinct in source due context even though body channels overlap other smile holds. | SPECIAL_CLOSED_EYE_SMILE_HOLD | 1/11 (SINGLE-VIDEO) | exact-source subtotal 1 (phase overlap across source families not globally de-duplicated) | SYSTEM / TRANSITION | face | eyelids; mouth; head | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | hold | HIGH | V04/F16 | HIGH |
| EEVEE-MF-069 | Grooming/appearance-change prep hold | R. Grooming / appearance-change / other | Body/face state observed while grooming/appearance-change effects obscure the head; the visual effect itself is explicitly excluded as body motion. | GROOM_CLOUD | 1/11 (SINGLE-VIDEO) | exact-source subtotal 8 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | face | eyelids; mouth; head; ears L/R | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | hold | MEDIUM | V07/GROOM_CLOUD | HIGH |
| EEVEE-MF-070 | Grooming/appearance-change surprise | R. Grooming / appearance-change / other | After grooming/appearance-change occlusion clears, Eevee opens eyes and forms an O-shaped mouth; extreme eye/open-mouth performance is an intensity variant. | EXTREME_SURPRISE, NORMAL_SURPRISE | 1/11 (SINGLE-VIDEO) | exact-source subtotal 8 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | face | eyes; mouth; head; ears L/R | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | hold | HIGH | V07/GROOM_SURPRISE, V07/GROOM_SURPRISE_EXTREME | HIGH |
| EEVEE-MF-071 | Side-to-front turn | P. Transition | Head leads a turn from side orientation, followed by torso and forepaw/support adjustment into front-facing stance. | SIDE_TO_FRONT_TURN | 1/11 (SINGLE-VIDEO) | exact-source subtotal 1 (phase overlap across source families not globally de-duplicated) | AUTONOMOUS | full-body | head; torso; forelimb L/R; root/COM; feet / support | hindlimbs unless listed; tail unless listed | QUIET | active | TURN | QUIET | single_transition | MEDIUM | V03/F04 | HIGH |
| EEVEE-MF-072 | Room reposition turn | P. Transition | Distant whole-body orientation change through side/back views into another side orientation; detailed foot action is not confirmed. | ROOM_REPOSITION_TURN | 1/11 (SINGLE-VIDEO) | exact-source subtotal 1 (phase overlap across source families not globally de-duplicated) | AUTONOMOUS | full-body | full body / COM; head; ears L/R; tail | channels not listed by source | QUIET | active | TURN | FOLLOW_THROUGH | single_transition | LOW | V08/ROOM_REPOSITION_TURN | HIGH |
| EEVEE-MF-073 | Recovery to neutral | N. Recovery / settle / afterglow | Return from an expressive/action peak toward the source-defined neutral baseline; timing and channel order vary by parent family. | GENERIC_RECOVERY, POSITIVE_BURST_RECOVERY, POSITIVE_RECOVERY_MOUTH_OPEN, SPECIAL_RECOVERY | 9/11 (COMMON) | at least 7 + recurrent/uncounted source occurrences | BOTH | mixed | head; eyelids; ears L/R; mouth; torso; root/COM | hindlimbs unless listed; tail unless listed | follow-through | active | WEIGHT_SHIFT | QUIET | single_transition | HIGH | V01/RECOVERY_TO_NEUTRAL, V02/RECOVERY_TO_NEUTRAL, V04/F07, V04/F15, V05/POSITIVE_RECOVERY_MOUTH_OPEN… | HIGH |
| EEVEE-MF-074 | Half-lid/downward recovery | N. Recovery / settle / afterglow | Short half-lidded/downward-faced transition between expressive states; semantic valence is unresolved. | HALF_LID_RECOVERY | 1/11 (SINGLE-VIDEO) | exact-source subtotal 1 (phase overlap across source families not globally de-duplicated) | UNKNOWN | face | eyelids; head; mouth | hindlimbs unless listed; tail unless listed | QUIET | mostly stable / source-dependent | PLANTED | QUIET | single_transition | HIGH | V07/HALF_LID_RECOVERY | HIGH |
| EEVEE-MF-075 | Drowsy/rest recovery to neutral | N. Recovery / settle / afterglow | Non-touch recovery from drowsy/wake state through closed/half-lid settling toward normal neutral. | DROWSY_RECOVERY | 1/11 (SINGLE-VIDEO) | exact-source subtotal 1 (phase overlap across source families not globally de-duplicated) | AUTONOMOUS | head | eyelids; head; ears L/R | hindlimbs unless listed; tail unless listed | follow-through | mostly stable / source-dependent | PLANTED | QUIET | single_transition | HIGH | V03/F20 | HIGH |
| EEVEE-MF-076 | Positive touch afterglow | N. Recovery / settle / afterglow | Closed-eye positive expression/ear state persists after the triggering contact phase has ended. | CHEEK_HAPPY_AFTERGLOW | 1/11 (SINGLE-VIDEO) | exact-source subtotal 1 (phase overlap across source families not globally de-duplicated) | PLAYER_TRIGGERED | face | eyelids; mouth; ears L/R; head; torso | hindlimbs unless listed; tail unless listed | emotion amplifier | mostly stable / source-dependent | PLANTED | QUIET | hold | HIGH | V04/F10 | HIGH |
| EEVEE-MF-077 | Open-eye smile/bob, cause unresolved | R. Grooming / appearance-change / other | Open-eyed large-mouth smile with small head/torso bounce where the source cannot reliably assign interaction vs autonomous cause. | POS_OPEN_SMILE | 1/11 (SINGLE-VIDEO) | exact-source subtotal 8 (phase overlap across source families not globally de-duplicated) | UNKNOWN | mixed | mouth; eyes; head; torso; ears L/R | hindlimbs unless listed; tail unless listed | emotion amplifier | active | WEIGHT_SHIFT | QUIET | hold | HIGH | V07/POS_OPEN_SMILE | HIGH |

## 5. Family → Variant → Occurrence Mapping
Each normalized Variant below carries all source-local Family records assigned to it. Timestamps/IDs are copied from the source family catalogs; where a source only provides a state count or “many”, this Master does not invent event boundaries.

### EEVEE-MF-001 — Neutral bilateral blink
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-001-V01 | EEVEE-MF-001 | 通常の短い両眼瞬き; 独立した短瞬目閉じ; 頭/耳の大きな変化を伴わない独立短閉眼。; Short neutral blink without a larger concurrent reaction; 中立または弱い反応中の短い両眼瞬き… | V02, V03, V05, V06, V08, V09, V10 | V02/BLINK; V03/F25; V05/BLINK; V06/F01; V08/BLINK; V09/F02; V10/BLINK | V02=2; V03=1+; V05=1 confirmed; V06=**5**; V08=6; V09=M002 (6.00–6.23), M041 (155.93–156.00), M042 (161.13–161.23), M051 (182.77–182.87); V10=10 | V02: 120.40–120.53, 123.60–123.73; V03: M053 ほか; V05: M056; V06: 18.73, 25.37, 31.90, 60.33, 91.27 s; V08: M029 01:46.30–01:46.43, M031 01:48.70–01:48.85, M033 01:51.03–01:51.13, M034 01:53.47–01:53.60, M043 02:15.67–02… | source inventory; original V1/V2/I retained |

### EEVEE-MF-002 — Context-linked short eye close
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-002-V01 | EEVEE-MF-002 | 0.03–0.10秒級の短い眼瞼閉鎖; 特殊シーケンス中の短い両眼閉じ→再開眼; 0.1–0.2秒級の短い閉眼。Blinkまたは接触反応候補。; 0.07〜0.23s級の短い閉眼。独立Blinkと遷移用閉眼を含む。 | V01, V04, V05, V07 | V01/SHORT_EYELID_CLOSE; V04/F11; V05/EYE_CLOSE_SHORT; V07/BRIEF_EYE_CLOSE | V01=22; V04=1; V05=6; V07=**22** | V01: E001–E022参照; V04: 3.633–3.767; V05: M023,M025,M027,M028,M030,M048; V07: 00:09.67–00:09.73, 00:12.03–00:12.13, 00:31.50–00:31.57, 00:33.90–00:34.00, 01:13.80–01:14.00, 01:21.73–01:21.80, 01:24.10–01:24.20, 01:35.43–… | source inventory; original V1/V2/I retained |

### EEVEE-MF-003 — Idle body micro-sway
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-003-V01 | EEVEE-MF-003 | 正面待機中にも胴体/頭が完全固定ではなく、低振幅で位置・姿勢が変化する。 [V1] | V07 | V07/BODY_IDLE_MICRO_SWAY | V07=離散回数ではなく、複数の`MACRO_STILL`区間で継続 | V07: 特に 00:21.20–00:27.60、01:08.90–01:15.10、02:21.60–02:34.10、02:55.50–03:00.70、03:23.80–03:27.40 で確認 | source inventory; original V1/V2/I retained |
| EEVEE-MF-003-V02 | EEVEE-MF-003 | ニュートラル時の生命感を作る低振幅ループ | V04 | V04/F01 | V04=3主要区間 | V04: 5.900–12.100 / 25.033–26.000 / 30.267–34.833 | source inventory; original V1/V2/I retained |

### EEVEE-MF-004 — Tail idle sway / swish
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-004-V01 | EEVEE-MF-004 | 正面姿勢のまま尻尾が緩く位置変化; 尻尾のみの小さなスイング; 頭/胴体をほぼ固定したまま尾の輪郭/位置が緩やかに変わる小待機運動。; 大動作のない区間でも、背後の尾の見える位置/角度がゆっくり変わる。 [V1]; 長いIdle中に見える… | V01, V03, V05, V07, V10 | V01/TAIL_SWAY_SUBTLE; V03/F14; V05/TAIL_IDLE_SWAY; V07/TAIL_IDLE_SWAY_SMALL; V10/TAIL_SWAY_SLOW | V01=2 bouts; V03=2; V05=1 interval; V07=離散回数化せず連続Motionとして扱う; V10=連続（4長Idle区間で確認） | V01: 01:55–02:00, 02:03.73–02:05.07; V03: M035, M053; V05: M060; V10: 02:31.100–02:48.700 / 03:04.200–03:10.500 / 03:12.100–03:17.300 / 03:44.750–03:49.867 | source inventory; original V1/V2/I retained |
| EEVEE-MF-004-V02 | EEVEE-MF-004 | Small slow lateral change of tail/torso visible during otherwise… | V06 | V06/F10 | V06=several low-amplitude passages; clearest around 28.3–29.4 and 57–60 s | see source-local family record | source inventory; original V1/V2/I retained |

### EEVEE-MF-005 — Independent single-ear flick
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-005-V01 | EEVEE-MF-005 | 中立時に片耳のみ短く倒して戻す | V01 | V01/EAR_FLICK_SINGLE | V01=1 | V01: 03:00.70 | source inventory; original V1/V2/I retained |

### EEVEE-MF-006 — Bilateral ear emotion/follow-through
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-006-V01 | EEVEE-MF-006 | Both ears rotate/drop outward/down during emotional/relaxed stat… | V06 | V06/F05 | V06=recurrent component in F03, F04, F07 | V06: e.g. 20.1–22.5, 39.9–41.5, 44.4–46.7, 106.1–110.0, 113.6–117.4 s | source inventory; original V1/V2/I retained |
| EEVEE-MF-006-V02 | EEVEE-MF-006 | 大型喜び、お辞儀、閉眼収束に連動して左右耳が外側/下方向へ回転する。 [V1] | V07 | V07/EAR_FOLLOW_OUTWARD | V07=独立回数ではなく、`POS_LARGE_MUSIC`、`BOW_BIPAW_SEQUENCE`等へ従属 | see source-local family record | source inventory; original V1/V2/I retained |

### EEVEE-MF-007 — Front neutral still hold
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-007-V01 | EEVEE-MF-007 | 大きい身体Motionを止め正面中立を保持; 正面中立の待機/ほぼ無動; 正面で大きく動かない保持/半眼待機; 大きな姿勢を崩さず静止/待機する状態。; Intentionally low-motion upright state, so… | V01, V02, V03, V05, V06, V07, V08, V09, V10, V11 | V01/MACRO_STILL_FRONT_NEUTRAL; V02/BASE_NEUTRAL_STILLNESS; V03/F05; V05/NEUTRAL_STILL; V06/F08; V07/MACRO_STILL; V08/NEUTRAL_IDLE; V09/F01; V10/IDLE_STILL_HOLD; V11/F03 | V01=13 bouts; V02=20区間; V03=5+; V05=21; V06=many long intervals; V07=**36**; V08=4; V09=6 major holds: M040, M043, M050, M052, M056, M058; plus short neutral gaps throughout petting; V10=4; V11=多数 | V01: 後述Stillness表; V02: M003,004,014,019,021,030,033,041,047,049,055,058,062,063,064,066,069,071,073,075; V03: 43.60, 145.20, 174.40, 252.40 ほか; V05: M002,M004,M006,M009,M012,M015,M018,M036,M039,M042,M045,M047,M049,M052… | source inventory; original V1/V2/I retained |

### EEVEE-MF-008 — Touch latency / tolerate stillness
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-008-V01 | EEVEE-MF-008 | 触られても即座には大反応せず、Neutralを保持する待ち | V04 | V04/F02 | V04=4 | V04: 12.100–13.467 / 17.100–17.767 / 20.833–22.167 / 26.000–26.867 | source inventory; original V1/V2/I retained |
| EEVEE-MF-008-V02 | EEVEE-MF-008 | user/cursor remains in contact while Eevee changes little; inten… | V09 | V09/F07 | V09=2 prominent windows: M013, M027 | V09: ~49.8–53.3, ~99.0–103.1 s | source inventory; original V1/V2/I retained |

### EEVEE-MF-009 — Side/profile still hold
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-009-V01 | EEVEE-MF-009 | 横向きで待機する | V03 | V03/F03 | V03=1 | V03: 30.90 | source inventory; original V1/V2/I retained |
| EEVEE-MF-009-V02 | EEVEE-MF-009 | 第2セッションの側面向き待機姿勢。 | V05 | V05/SIDE_PROFILE_STATE | V05=3 | V05: M022,M026,M029 | source inventory; original V1/V2/I retained |
| EEVEE-MF-009-V03 | EEVEE-MF-009 | 遠景または横向きで大きく動かず姿勢を維持。 | V08 | V08/STILLNESS_ROOM | V08=3 | V08: M001 00:00.00–00:10.90, M017 00:52.50–00:58.50, M062 02:55.50–03:04.70 | source inventory; original V1/V2/I retained |

### EEVEE-MF-010 — Close-up forepaw rest/presentation hold
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-010-V01 | EEVEE-MF-010 | 近接表示で前足を手前に置き保持 | V03 | V03/F02 | V03=2 | V03: 8.50, 10.90 | source inventory; original V1/V2/I retained |

### EEVEE-MF-011 — Hand-oriented attention candidate
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-011-V01 | EEVEE-MF-011 | 手カーソル側へ注意/視線を向けるように見える | V01 | V01/GAZE_ORIENT_TO_HAND_CANDIDATE | V01=1 | V01: 02:49.50–02:51.70 | source inventory; original V1/V2/I retained |

### EEVEE-MF-012 — Open-mouth attention hold
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-012-V01 | EEVEE-MF-012 | 中立から口を開き、正面への注意表情を保持。 | V08 | V08/MOUTH_OPEN_ATTENTION | V08=1 | V08: M030 01:46.40–01:48.40 | source inventory; original V1/V2/I retained |
| EEVEE-MF-012-V02 | EEVEE-MF-012 | 四肢大動作を伴わず、丸い口を開けて保持する。 | V07 | V07/MOUTH_OPEN_ROUND | V07=**1** | V07: 00:18.20–00:19.40 | source inventory; original V1/V2/I retained |

### EEVEE-MF-013 — Autonomous curious head tilt
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-013-V01 | EEVEE-MF-013 | 入力なしで頭を徐々に片側へ傾ける。 | V08 | V08/HEAD_TILT_AUTONOMOUS | V08=1 | V08: M058 02:47.50–02:48.80 | source inventory; original V1/V2/I retained |
| EEVEE-MF-013-V02 | EEVEE-MF-013 | 自発的に頭を傾げて注視する | V03 | V03/F16 | V03=2 | V03: M037, M052 | source inventory; original V1/V2/I retained |
| EEVEE-MF-013-V03 | EEVEE-MF-013 | 長い静止後、自発的に目を閉じつつ頭を傾け、再閉眼を挟み戻る | V02 | V02/IDLE_DROWSY_HEAD_TILT | V02=1 | V02: 114.43–116.33 | source inventory; original V1/V2/I retained |
| EEVEE-MF-013-V04 | EEVEE-MF-013 | 口開け/閉眼を入口に、片側へ長く頭を傾け、開眼保持後に閉眼を挟んで中央へ戻す。 | V05 | V05/AUTO_HEAD_TILT_LONG | V05=1 | V05: M064 | source inventory; original V1/V2/I retained |
| EEVEE-MF-013-V05 | EEVEE-MF-013 | 口/眼瞼前奏後、頭を画面右へ傾ける自発Motion; 半眼を経て頭を画面右側へ傾け、しばらく保持して戻る。; 入力なしの大きな画面右方向Head Tilt。 | V01, V07, V10 | V01/HEAD_TILT_SCREEN_RIGHT; V07/HEAD_TILT_R; V10/HEAD_TILT_LARGE_SCREEN_RIGHT | V01=4; V07=**1**; V10=1 | V01: 01:32.70, 01:45.67, 03:04.47, 03:22.37; V07: 01:38.43–01:40.40; V10: 02:54.000 | source inventory; original V1/V2/I retained |
| EEVEE-MF-013-V06 | EEVEE-MF-013 | 大きく傾けた頭で閉眼し、そのまま中央へ戻る。 | V08 | V08/HEAD_TILT_EYE_CLOSE | V08=1 | V08: M059 02:48.80–02:50.40 | source inventory; original V1/V2/I retained |

### EEVEE-MF-014 — Autonomous head sway / shake
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-014-V01 | EEVEE-MF-014 | 無入力時、閉眼しつつ頭を左右へ反復スウェイ。耳が大きく追従し、終盤に口開けを挟み復帰。 | V05 | V05/AUTO_HEAD_SHAKE_SWAY | V05=2 | V05: M058,M062 | source inventory; original V1/V2/I retained |
| EEVEE-MF-014-V02 | EEVEE-MF-014 | 入力なし。目閉じで頭を一方へ大きく倒し、反対側を通って下へ収束 | V11 | V11/F16 | V11=1 | V11: 145.2–147.2 | source inventory; original V1/V2/I retained |

### EEVEE-MF-015 — Autonomous/contented smile hold
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-015-V01 | EEVEE-MF-015 | 入力なしで一瞬喜ぶ | V03 | V03/F15 | V03=1 | V03: M036 | source inventory; original V1/V2/I retained |
| EEVEE-MF-015-V02 | EEVEE-MF-015 | 無入力時に自発的に閉眼・開口笑顔を持続し、頭/耳の小さな余韻を伴って戻る。 | V05 | V05/AUTO_HAPPY_SMILE_IDLE | V05=1 | V05: M066 | source inventory; original V1/V2/I retained |
| EEVEE-MF-015-V03 | EEVEE-MF-015 | 登場直後の閉眼＋頭沈み＋開口笑顔＋耳外展。 | V05 | V05/ENTRY_HAPPY_GREETING | V05=1 | V05: M001 | source inventory; original V1/V2/I retained |
| EEVEE-MF-015-V04 | EEVEE-MF-015 | 入力なし/開始演出で閉眼笑顔＋耳を外へ緩める | V01 | V01/IDLE_CONTENTED_SMILE_EAR_SPREAD | V01=2 | V01: 00:05.60, 01:52.07 | source inventory; original V1/V2/I retained |
| EEVEE-MF-015-V05 | EEVEE-MF-015 | 無入力で自発する閉眼＋開口笑顔＋耳外開き。 | V10 | V10/IDLE_SMILE | V10=1 | V10: 03:10.567 | source inventory; original V1/V2/I retained |
| EEVEE-MF-015-V06 | EEVEE-MF-015 | 動画開始時点で継続中の、長い閉眼笑顔＋耳外開きの喜び姿勢。 | V10 | V10/INITIAL_HAPPY_HOLD | V10=1 | V10: 00:00.333 | source inventory; original V1/V2/I retained |
| EEVEE-MF-015-V07 | EEVEE-MF-015 | 入力なしで目を閉じ、穏やかに笑う | V11 | V11/F01 | V11=1 | V11: 1.2–2.2 | source inventory; original V1/V2/I retained |

### EEVEE-MF-016 — Autonomous bilateral forepaw lift
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-016-V01 | EEVEE-MF-016 | 両前足を同時に前方へ上げ肉球を見せる; Short self-started-looking open-mouth action with both forepaws …; 入力なしで両前足を持ち上げ、口を開く自発Gesture。 | V01, V06, V10 | V01/BOTH_FOREPAW_LIFT_FORWARD; V06/F06; V10/IDLE_FOREPAW_GESTURE | V01=3; V06=**2**; V10=1 | V01: 00:00.67, 01:38.70, 02:55.83; V06: 96.60–97.50; 98.20–99.00 s; V10: 02:48.750 | source inventory; original V1/V2/I retained |
| EEVEE-MF-016-V02 | EEVEE-MF-016 | 目閉じ笑顔と前足持ち上げを伴う開始直後の短い喜び | V11 | V11/F02 | V11=1 | V11: 2.7–3.5 | source inventory; original V1/V2/I retained |

### EEVEE-MF-017 — Autonomous single-forepaw raise
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-017-V01 | EEVEE-MF-017 | Eevee右前足（画面左側）を単独で前上方へ上げ、肉球を見せて戻す。 | V07 | V07/FOREPAW_RAISE_R | V07=**6** | V07: 01:35.00–01:35.40, 01:36.20–01:36.60, 01:49.90–01:50.30, 01:51.80–01:52.30, 02:51.60–02:52.10, 03:07.60–03:08.00 | source inventory; original V1/V2/I retained |

### EEVEE-MF-018 — Autonomous/unknown deep bow → bilateral paw rise
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-018-V01 | EEVEE-MF-018 | 深いお辞儀→保持→起き上がりながら両前足を上げ肉球を見せる→閉眼で収束。 | V07 | V07/BOW_BIPAW_SEQUENCE | V07=**4** | V07: 00:41.10–00:43.53, 01:06.30–01:08.73, 01:52.90–01:55.33, 03:16.23–03:18.70 | source inventory; original V1/V2/I retained |
| EEVEE-MF-018-V02 | EEVEE-MF-018 | 深い前屈・耳下げ→上体を起こし前足肉球を前に見せる→目閉じで収束 | V11 | V11/F09 | V11=1 | V11: 51.0–53.5 | source inventory; original V1/V2/I retained |

### EEVEE-MF-019 — Relaxed long eye-close moving hold
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-019-V01 | EEVEE-MF-019 | 数秒だけ閉眼し両耳を低く開く短い休息 | V01 | V01/BRIEF_RELAXED_EYE_CLOSE_EAR_DROOP | V01=1 | V01: 03:12.60 | source inventory; original V1/V2/I retained |
| EEVEE-MF-019-V02 | EEVEE-MF-019 | 入力なし。目閉じを長く維持し、両耳を大きく横へ落とし、頭をゆっくり移動 | V11 | V11/F17 | V11=1 | V11: 152.9–157.0 | source inventory; original V1/V2/I retained |
| EEVEE-MF-019-V03 | EEVEE-MF-019 | Long relaxed idle with closed eyes and ears lowered | V06 | V06/F07 | V06=**2** | V06: 106.10–110.10; 113.57–117.50 s | source inventory; original V1/V2/I retained |
| EEVEE-MF-019-V04 | EEVEE-MF-019 | 長めの閉眼と低振幅の頭/胴揺れ。 | V07 | V07/RELAXED_CLOSE_SWAY | V07=**2** | V07: 00:45.50–00:49.37, 03:03.10–03:04.30 | source inventory; original V1/V2/I retained |
| EEVEE-MF-019-V05 | EEVEE-MF-019 | 閉眼・耳外開き・軽い頭沈みを数秒維持するRelax状態。 | V10 | V10/RELAXED_EYE_CLOSE_LONG | V10=1 | V10: 03:00.233 | source inventory; original V1/V2/I retained |

### EEVEE-MF-020 — Doze/drowsy entry
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-020-V01 | EEVEE-MF-020 | 長い休息への遷移。眼→頭→耳の順 | V01 | V01/DOZE_ENTRY | V01=1 | V01: 02:08.30 | source inventory; original V1/V2/I retained |
| EEVEE-MF-020-V02 | EEVEE-MF-020 | 眠気が始まる | V03 | V03/F17 | V03=1 | V03: M039 | source inventory; original V1/V2/I retained |

### EEVEE-MF-021 — Deep doze / drowsy hold
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-021-V01 | EEVEE-MF-021 | 深い閉眼Bowを長時間維持する自発State。 | V10 | V10/DOZE_BOW_HOLD | V10=1 | V10: 03:17.333 | source inventory; original V1/V2/I retained |
| EEVEE-MF-021-V02 | EEVEE-MF-021 | 長時間の閉眼・頭下げ・低運動状態 | V01 | V01/DOZE_HOLD | V01=1 | V01: 02:09.10–02:31.50 | source inventory; original V1/V2/I retained |
| EEVEE-MF-021-V03 | EEVEE-MF-021 | 目を閉じたまま長く揺れる | V03 | V03/F18 | V03=1 | V03: M040 | source inventory; original V1/V2/I retained |

### EEVEE-MF-022 — Ear switching inside doze
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-022-V01 | EEVEE-MF-022 | 休息保持中の左右非対称な耳切替 | V01 | V01/DOZE_EAR_SWITCH_CYCLE | V01=9 strong cycles | V01: 02:10.27, 02:12.57, 02:14.93, 02:17.23, 02:19.57, 02:21.93, 02:24.27, 02:26.60, 02:28.90 | source inventory; original V1/V2/I retained |

### EEVEE-MF-023 — Distant sleep stillness
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-023-V01 | EEVEE-MF-023 | 遠景で睡眠記号が出る間、Eevee本体はほぼ静止。 | V08 | V08/SLEEP_STILLNESS_DISTANT | V08=2 | V08: M002 00:10.90–00:13.90, M063 03:04.70–03:06.80 | source inventory; original V1/V2/I retained |

### EEVEE-MF-024 — Sleep micro-cycle
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-024-V01 | EEVEE-MF-024 | 閉眼睡眠中の約2.7–2.8秒周期の口元微小変化。頭/上体もごく小さく追従。 | V08 | V08/SLEEP_MICRO_CYCLE | V08=18 | V08: M004 00:16.30–00:19.00, M005 00:19.10–00:21.80, M006 00:21.90–00:24.70, M007 00:24.80–00:27.50, M008 00:27.60–00:30.40, M009 00:30.50–00:33.20, M010 00:33.30–00:36.00, M011 00:36.10–00:38.90, M012 00:39.00–00:41.70… | source inventory; original V1/V2/I retained |

### EEVEE-MF-025 — Touch during rest with delayed/no immediate response
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-025-V01 | EEVEE-MF-025 | Doze中にタッチされても直ちに大きな身体反応を起こさず、元Stateを維持する区間。 | V10 | V10/TOUCH_DURING_DOZE_NO_IMMEDIATE_RESPONSE | V10=1 | V10: 03:26.500 | source inventory; original V1/V2/I retained |

### EEVEE-MF-026 — Wake/startle transition
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-026-V01 | EEVEE-MF-026 | Doze中のタッチに遅れて発生する、開眼丸口→再閉眼→横揺れの複合反応。 | V10 | V10/TOUCH_WAKE_RESPONSE | V10=1 | V10: 03:28.433 | source inventory; original V1/V2/I retained |
| EEVEE-MF-026-V02 | EEVEE-MF-026 | 休息中タッチ後、遅れて眼を開き頭を上げる覚醒反応 | V01 | V01/WAKE_ON_TOUCH_STARTLE | V01=1 | V01: 02:31.50 | source inventory; original V1/V2/I retained |
| EEVEE-MF-026-V03 | EEVEE-MF-026 | 急に起きて驚く | V03 | V03/F19 | V03=1 | V03: M041 | source inventory; original V1/V2/I retained |

### EEVEE-MF-027 — Positive-touch onset
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-027-V01 | EEVEE-MF-027 | F08から閉眼喜びへの変換 | V04 | V04/F09 | V04=1 | V04: 28.567–28.733 | source inventory; original V1/V2/I retained |
| EEVEE-MF-027-V02 | EEVEE-MF-027 | 長押し/なでから閉眼笑顔へ入る短い導入 | V04 | V04/F03 | V04=3 | V04: 13.500 / 17.800 / 22.200付近 | source inventory; original V1/V2/I retained |

### EEVEE-MF-028 — Gentle positive touch hold
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-028-V01 | EEVEE-MF-028 | Repeated positive-looking contact response without the deep bow | V06 | V06/F04 | V06=**10 occurrences/variants** | V06: 38.20–41.60; 42.80–44.30; 44.37–45.40; 45.70–46.80; 48.50–51.40; 53.40–56.10; 61.20–61.40; 62.77–64.30; 71.80–74.50; 76.30–79.00 s | source inventory; original V1/V2/I retained |
| EEVEE-MF-028-V02 | EEVEE-MF-028 | 穏やかな撫で反応。半眼〜目閉じ | V03 | V03/F09 | V03=2 | V03: M013,27 | source inventory; original V1/V2/I retained |
| EEVEE-MF-028-V03 | EEVEE-MF-028 | 撫で継続中の穏やかな閉眼＋小笑顔; 閉眼笑顔を一定時間保持; 閉眼＋開口笑顔を比較的長く保持する、顔中心の肯定反応。 | V01, V02, V05 | V01/TOUCH_RELAXED_EYES_CLOSED_SMILE; V02/TOUCH_POSITIVE_CLOSED_EYE_SMILE; V05/TOUCH_POSITIVE_GENTLE | V01=11; V02=9; V05=5 | V01: 00:11.37, 00:22.37, 00:31.77, 00:41.80, 00:45.27, 00:49.00, 01:00.70, 01:07.43, 02:35.70, 02:39.77, 02:46.30; V02: M012,015,023,031,035,045,050,053,067; V05: M014,M034,M040,M043,M050 | source inventory; original V1/V2/I retained |
| EEVEE-MF-028-V04 | EEVEE-MF-028 | 閉眼・口開き笑顔を長く維持 | V04 | V04/F04 | V04=3 | V04: 13.667–15.633 / 18.000–19.700 / 22.333–23.900 | source inventory; original V1/V2/I retained |
| EEVEE-MF-028-V05 | EEVEE-MF-028 | タッチ後の単一ローブ型の閉眼笑顔。FULLの後段ローブを持たない。 | V10 | V10/TOUCH_POSITIVE_SHORT | V10=3 | V10: 00:25.800, 00:30.467, 03:39.933 | source inventory; original V1/V2/I retained |
| EEVEE-MF-028-V06 | EEVEE-MF-028 | 閉眼笑顔を主体とする小〜中のポジティブ表情。 | V07 | V07/POS_CLOSED_SMALL | V07=**17** | V07: 00:01.40–00:03.60, 00:13.13–00:14.53, 00:19.63–00:21.10, 00:35.23–00:36.50, 00:57.50–00:59.00, 01:00.60–01:02.07, 01:25.50–01:27.00, 01:30.20–01:31.63, 01:58.60–02:00.03, 02:02.30–02:03.87, 02:14.63–02:15.90, 02:19… | source inventory; original V1/V2/I retained |
| EEVEE-MF-028-V07 | EEVEE-MF-028 | dominant positive petting response: eyes close, mouth smiles/ope… | V09 | V09/F03 | V09=**29** clear touch-response occurrences, excluding the distinct bow M014 | V09: M003, M004, M008–M012, M015–M019, M022–M026, M028–M031, M033–M038, M048–M049 | source inventory; original V1/V2/I retained |
| EEVEE-MF-028-V08 | EEVEE-MF-028 | 典型的な撫で喜び。目閉じ笑顔中心 | V03 | V03/F07 | V03=18 | V03: M009,10,14,15,16,18,19,20,23,24,25,28,29,30,43,44,49,50,51 | source inventory; original V1/V2/I retained |

### EEVEE-MF-029 — Strong positive touch burst
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-029-V01 | EEVEE-MF-029 | 強い喜びの前半。閉眼・耳横倒し・頭沈み・口閉じ | V04 | V04/F05 | V04=3 | V04: 15.733–15.967 / 19.867–20.067 / 24.067–24.267 | source inventory; original V1/V2/I retained |
| EEVEE-MF-029-V02 | EEVEE-MF-029 | 強い喜びの後半。閉眼のまま口を大きく開き、起き上がる | V04 | V04/F06 | V04=3 | V04: 16.000–16.600 / 20.100–20.667 / 24.300–24.833 | source inventory; original V1/V2/I retained |
| EEVEE-MF-029-V03 | EEVEE-MF-029 | 閉眼笑顔、耳の外展/下降、身体バウンス。音符/円形エフェクトが同期する大型喜び。 | V07 | V07/POS_LARGE_MUSIC | V07=**11** | V07: 00:14.67–00:15.53, 00:36.63–00:37.50, 01:02.20–01:03.07, 01:27.13–01:28.03, 01:31.77–01:32.67, 02:04.00–02:04.87, 02:16.00–02:16.90, 02:20.60–02:21.50, 02:45.27–02:46.17, 02:54.50–02:55.43, 03:22.70–03:23.60 | source inventory; original V1/V2/I retained |
| EEVEE-MF-029-V04 | EEVEE-MF-029 | 撫でへの強い喜び。閉眼→耳外開き→大笑顔＋軽い上体反応; 喜びエフェクトに伴う半目/閉眼→開眼笑顔の反応 | V01, V02 | V01/TOUCH_POSITIVE_BURST_EAR_SPREAD; V02/TOUCH_POSITIVE_EFFECT_REACTION | V01=12; V02=10 | V01: 00:13.10, 00:24.23, 00:33.37, 00:43.40, 00:47.00, 00:51.10, 01:02.60, 01:03.83, 01:09.33, 02:37.37, 02:41.37, 02:47.87; V02: M013,016,017,024,032,036,046,051,054,068 | source inventory; original V1/V2/I retained |
| EEVEE-MF-029-V05 | EEVEE-MF-029 | 閉眼笑顔に加え耳を大きく外へ広げ、口開きも強める大反応。 | V05 | V05/TOUCH_POSITIVE_LARGE | V05=5 | V05: M035,M041,M044,M051,M053 | source inventory; original V1/V2/I retained |
| EEVEE-MF-029-V06 | EEVEE-MF-029 | 強い喜びで身体を上下に大きく動かす | V03 | V03/F10 | V03=1 | V03: M026 | source inventory; original V1/V2/I retained |
| EEVEE-MF-029-V07 | EEVEE-MF-029 | 接触に対する閉眼笑顔主体の反応。耳・頭・上体が強さに応じ追従。 | V08 | V08/TOUCH_POSITIVE | V08=20 | V08: M019 01:06.50–01:11.40, M020 01:12.00–01:16.20, M021 01:16.80–01:20.40, M022 01:20.80–01:24.40, M023 01:25.00–01:27.80, M024 01:28.50–01:31.80, M025 01:33.80–01:36.80, M026 01:37.20–01:40.00, M027 01:40.80–01:43.20… | source inventory; original V1/V2/I retained |
| EEVEE-MF-029-V08 | EEVEE-MF-029 | ピンク/ハート系の大きな喜び表情 | V02 | V02/SPECIAL_HEART_JOY | V02=1（ハイタッチ後） | V02: 43.33–44.27 | source inventory; original V1/V2/I retained |
| EEVEE-MF-029-V09 | EEVEE-MF-029 | タッチ中の目閉じ笑顔→頭を下げる→耳を左右へ広げる→顔を上げ大笑顔→neutral | V11 | V11/F05 | V11=**15** | V11: 11.3–15.1; 16.0–20.4; 21.3–24.3; 25.0–27.9; 28.5–31.3; 31.5–34.8; 53.9–56.6; 57.3–59.8; 60.8–63.5; 72.0–74.9; 87.3–90.3; 90.5–94.2; 96.0–98.8; 99.0–103.4; 118.8–121.5 | source inventory; original V1/V2/I retained |

### EEVEE-MF-030 — Two-lobe positive touch sequence
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-030-V01 | EEVEE-MF-030 | タッチ後の標準的な2段Positive。閉眼笑顔の第1ローブ→約0.1秒の開眼/reset→第2ローブ。 | V10 | V10/TOUCH_POSITIVE_FULL | V10=18 | V10: 00:14.900, 00:20.067, 00:33.133, 00:36.900, 00:48.633, 00:52.967, 00:56.733, 01:00.233, 01:11.733, 01:18.000, 01:21.400, 01:29.600, 01:33.933, 01:39.533, 02:06.567, 03:31.700, 03:34.733, 03:42.300 | source inventory; original V1/V2/I retained |

### EEVEE-MF-031 — Positive touch retrigger
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-031-V01 | EEVEE-MF-031 | 直前のFULL反応後、短い開眼を挟んで追加発生する閉眼Positive。 | V10 | V10/TOUCH_POSITIVE_RETRIGGER | V10=1 | V10: 02:09.267 | source inventory; original V1/V2/I retained |

### EEVEE-MF-032 — Touch-linked deep bow → rebound/paw rise
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-032-V01 | EEVEE-MF-032 | distinct forward bow with both forepaws gathering toward center | V09 | V09/F06 | V09=**1** clear example: M014 | V09: ~53.5–56.2 s | source inventory; original V1/V2/I retained |
| EEVEE-MF-032-V02 | EEVEE-MF-032 | 深いBowを先行させた後、両前足を正面へ一気にPopし、再閉眼で収束する複合タッチ反応。 | V10 | V10/TOUCH_BOW_PAW_POP | V10=2 | V10: 00:44.700, 01:07.100 | source inventory; original V1/V2/I retained |
| EEVEE-MF-032-V03 | EEVEE-MF-032 | Large positive-looking response during sustained contact | V06 | V06/F03 | V06=**4** | V06: 20.10–22.60; 33.43–36.00; 65.90–68.60; 91.47–94.10 s | source inventory; original V1/V2/I retained |

### EEVEE-MF-033 — Touch head-lean / tilt response
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-033-V01 | EEVEE-MF-033 | 撫でに頭を側方へ預ける/傾ける | V01 | V01/TOUCH_HEAD_LEAN_RELAX | V01=1 | V01: 02:32.10 | source inventory; original V1/V2/I retained |
| EEVEE-MF-033-V02 | EEVEE-MF-033 | 目を開いたまま頭を片側へ長く傾ける | V02 | V02/TOUCH_HEAD_TILT_FOLLOW | V02=1 | V02: 72.20–75.60 | source inventory; original V1/V2/I retained |
| EEVEE-MF-033-V03 | EEVEE-MF-033 | contact response dominated by lateral head/neck tilt while keepi… | V09 | V09/F04 | V09=2 clear examples: M006, M007 | V09: ~21.7–24.5, ~27.2–30.2 s | source inventory; original V1/V2/I retained |
| EEVEE-MF-033-V04 | EEVEE-MF-033 | タッチで大きく頭を傾ける | V03 | V03/F06 | V03=1 | V03: 50.10 | source inventory; original V1/V2/I retained |

### EEVEE-MF-034 — Touch open-mouth small/hold response
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-034-V01 | EEVEE-MF-034 | 頬付近タッチ中、開眼のまま口を開いて維持 | V04 | V04/F08 | V04=1 | V04: 26.900–28.533 | source inventory; original V1/V2/I retained |
| EEVEE-MF-034-V02 | EEVEE-MF-034 | タッチ中に目を開いたまま口を開く軽い警戒/困惑 | V02 | V02/TOUCH_MOUTH_OPEN_MILD | V02=12 | V02: M005,008,020,022,034,037,038,039,042,048,057,060 | source inventory; original V1/V2/I retained |
| EEVEE-MF-034-V03 | EEVEE-MF-034 | 顔・額付近のタッチに対する、主に口の開閉で構成される小反応。 | V10 | V10/TOUCH_MOUTH_OPEN_SMALL | V10=5 | V10: 00:11.000, 00:23.750, 00:29.000, 01:26.500, 03:37.750 | source inventory; original V1/V2/I retained |

### EEVEE-MF-035 — Touch surprise/open-mouth → smile
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-035-V01 | EEVEE-MF-035 | 顔タッチで口を大きく開ける/驚く様な顔→一部では後半に目閉じ笑顔へ | V11 | V11/F06 | V11=4 | V11: 37.6付近; 63.8–67.9; 75.0–82.3; 83.4–87.2 | source inventory; original V1/V2/I retained |
| EEVEE-MF-035-V02 | EEVEE-MF-035 | 驚き/口開きから笑顔に転じる | V03 | V03/F08 | V03=5 | V03: M011,12,17,21,22 | source inventory; original V1/V2/I retained |

### EEVEE-MF-036 — Touch-linked forepaw lift/offer
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-036-V01 | EEVEE-MF-036 | 口が小さく開いた後、片前肢を短く持ち上げ肉球が見える。 | V05 | V05/FOREPAW_LIFT_SMALL | V05=1 | V05: M046 | source inventory; original V1/V2/I retained |
| EEVEE-MF-036-V02 | EEVEE-MF-036 | 片前足を前へ持ち上げ、肉球を見せながら口を開く短反応 | V11 | V11/F07 | V11=2 | V11: 41.6–42.5; 71.1–71.9 | source inventory; original V1/V2/I retained |
| EEVEE-MF-036-V03 | EEVEE-MF-036 | response where a forepaw and body-weight shift are more salient … | V09 | V09/F05 | V09=2 clear examples: M005, M021 | V09: ~19.6–20.9, ~78.8–80.9 s | source inventory; original V1/V2/I retained |
| EEVEE-MF-036-V04 | EEVEE-MF-036 | 顔周辺へのタッチ時に前足を正面へ持ち上げる反応。 | V10 | V10/TOUCH_PAW_OFFER | V10=3 | V10: 00:06.470, 00:18.800, 01:16.750 | source inventory; original V1/V2/I retained |
| EEVEE-MF-036-V05 | EEVEE-MF-036 | タッチ中に片前足だけ前上方へ上げる | V01 | V01/TOUCH_SINGLE_FOREPAW_LIFT | V01=1 | V01: 00:15.37 | source inventory; original V1/V2/I retained |

### EEVEE-MF-037 — Small touch-linked eye-close/sink
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-037-V01 | EEVEE-MF-037 | 画面内のタッチリング/星と同期して閉眼し、頭/胴を少し沈める。 | V07 | V07/TOUCH_CLOSE_SMALL | V07=**2** | V07: 01:47.53–01:48.83, 03:13.77–03:15.10 | source inventory; original V1/V2/I retained |

### EEVEE-MF-038 — Positive jump hero response
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-038-V01 | EEVEE-MF-038 | 大Positive直後に身体全体が上昇し、足が地面から離れて見えるジャンプ型喜び | V11 | V11/F13 | V11=1 | V11: 121.87–123.4 | source inventory; original V1/V2/I retained |

### EEVEE-MF-039 — Small uneasy facial warning
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-039-V01 | EEVEE-MF-039 | 大きな姿勢変化なしの軽い不快表情 | V01 | V01/TOUCH_UNEASY_FACE_SMALL | V01=1 | V01: 00:38.80 | source inventory; original V1/V2/I retained |

### EEVEE-MF-040 — Angry/protest facial burst
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-040-V01 | EEVEE-MF-040 | 目/眉形が鋭くなり、口開閉を伴う短い負反応。 | V05 | V05/NEGATIVE_ANGRY_BURST | V05=2 | V05: M003,M005 | source inventory; original V1/V2/I retained |
| EEVEE-MF-040-V02 | EEVEE-MF-040 | 目を険しくし口を開ける抗議型。全身沈下は小さい | V01 | V01/TOUCH_NEGATIVE_PROTEST_FACE | V01=3 | V01: 00:55.73, 00:58.23, 02:43.30 | source inventory; original V1/V2/I retained |

### EEVEE-MF-041 — Strong closed-eye/ear-splay negative face
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-041-V01 | EEVEE-MF-041 | 両目を閉じ、耳を横に倒し、しかめる強い嫌反応 | V02 | V02/TOUCH_NEGATIVE_STRONG | V02=7 | V02: M006,009,040,043,056,059,061 | source inventory; original V1/V2/I retained |

### EEVEE-MF-042 — Sad/downcast negative face hold
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-042-V01 | EEVEE-MF-042 | 悲しげ/困り様の顔だけを比較的長く保持する負状態。 | V05 | V05/NEGATIVE_SAD_FACE_STATE | V05=5 | V05: M007,M010,M016,M020,M037 | source inventory; original V1/V2/I retained |

### EEVEE-MF-043 — Negative droop / body sink
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-043-V01 | EEVEE-MF-043 | 閉眼→頭低下→耳外展/横倒し→胴体/重心低下→低姿勢保持→復帰。 | V05 | V05/NEGATIVE_DROOP | V05=4 | V05: M008,M011,M017,M038 | source inventory; original V1/V2/I retained |
| EEVEE-MF-043-V02 | EEVEE-MF-043 | 不快表情から耳・頭・上体を下げる大きな撤退反応 | V01 | V01/TOUCH_NEGATIVE_SINK_EAR_DROOP | V01=1 | V01: 00:27.50 | source inventory; original V1/V2/I retained |

### EEVEE-MF-044 — Half-lid/downcast disengagement hold
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-044-V01 | EEVEE-MF-044 | 半眼/細目を維持する不機嫌様State。 | V05 | V05/ANNOYED_HALF_LID_STATE | V05=5 | V05: M013,M019,M024,M031,M033 | source inventory; original V1/V2/I retained |
| EEVEE-MF-044-V02 | EEVEE-MF-044 | short half-lidded/downturned facial configuration seen during an… | V09 | V09/F08 | V09=1 strong example inside M017 (~64 s) | see source-local family record | source inventory; original V1/V2/I retained |

### EEVEE-MF-045 — Face-touch withdrawal head tilt
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-045-V01 | EEVEE-MF-045 | 顔/鼻タッチから目閉じ→頭を横へ避ける→不満/半目で戻る | V11 | V11/F04 | V11=1 | V11: 8.9–11.3 | source inventory; original V1/V2/I retained |

### EEVEE-MF-046 — Side recoil / rotate away-to-front
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-046-V01 | EEVEE-MF-046 | 側面から閉眼/頭下げを起点に、胴体を急に正面へ回しながら身を引く/ひねる反応。 | V05 | V05/SIDE_RECOIL_ROTATE | V05=1 | V05: M032 | source inventory; original V1/V2/I retained |

### EEVEE-MF-047 — Strong rejection with paw/feet thrust
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-047-V01 | EEVEE-MF-047 | 鋭い顔→閉眼→全身前後動→左右の足裏をカメラ側へ提示/突き出し→開口→横傾き。 | V05 | V05/STRONG_REJECTION_PAW_THRUST | V05=1 | V05: M021 | source inventory; original V1/V2/I retained |

### EEVEE-MF-048 — Impact-like face flinch
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-048-V01 | EEVEE-MF-048 | 星エフェクトの瞬間に目を強く閉じ、頭を僅かに引く短いフリンチ | V11 | V11/F08 | V11=1 | V11: 44.3–45.6 | source inventory; original V1/V2/I retained |

### EEVEE-MF-049 — Full-body turn away
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-049-V01 | EEVEE-MF-049 | 全身を回して背面を向ける大きな回旋。 | V08 | V08/TURN_AWAY_FULL | V08=1 | V08: M038 02:07.00–02:07.80 | source inventory; original V1/V2/I retained |

### EEVEE-MF-050 — Turn return with bilateral paw presentation
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-050-V01 | EEVEE-MF-050 | 背面から正面へ戻りながら両前足を前方へ上げる。 | V08 | V08/TURN_RETURN_DOUBLE_PAW | V08=1 | V08: M039 02:07.90–02:08.50 | source inventory; original V1/V2/I retained |

### EEVEE-MF-051 — Reciprocal paw offer / WAIT
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-051-V01 | EEVEE-MF-051 | Eevee側から前足を上げ、肉球を前に向けて待つ | V02 | V02/HIGH_FIVE_PAW_OFFER_HOLD | V02=4 | V02: 33.23, 35.23, 37.77, 41.27開始 | source inventory; original V1/V2/I retained |
| EEVEE-MF-051-V02 | EEVEE-MF-051 | 手カーソル方向に片前足を前へ伸ばし肉球を見せる | V01 | V01/SINGLE_FOREPAW_REACH_FORWARD | V01=1 | V01: 02:51.77 | source inventory; original V1/V2/I retained |

### EEVEE-MF-052 — High-five contact acknowledgment
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-052-V01 | EEVEE-MF-052 | プレイヤー手が提示前足へ接触する局面 | V02 | V02/HIGH_FIVE_CONTACT | V02=5接触 | V02: 約33.70–34.43, 35.57–37.03, 38.20–39.27, 39.77–40.53, 41.77–42.60 | source inventory; original V1/V2/I retained |

### EEVEE-MF-053 — High-five success smile
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-053-V01 | EEVEE-MF-053 | ハイタッチ接触後の短い閉眼笑顔 | V02 | V02/HIGH_FIVE_SUCCESS_SMILE | V02=3明確 | V02: 34.50–34.77, 37.10–37.33, 39.30–39.63 | source inventory; original V1/V2/I retained |

### EEVEE-MF-054 — High-five alternate post-contact response
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-054-V01 | EEVEE-MF-054 | 追加接触後の口開き寄り反応。典型成功笑顔と異なる | V02 | V02/HIGH_FIVE_ALT_RESPONSE | V02=1明確 | V02: 40.60–40.90 | source inventory; original V1/V2/I retained |

### EEVEE-MF-055 — Food notice / presentation wait
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-055-V01 | EEVEE-MF-055 | 食物接近に対して顔/視線を正面に維持し口開き準備。 | V08 | V08/FOOD_NOTICE | V08=1 | V08: M048 02:26.60–02:27.20 | source inventory; original V1/V2/I retained |
| EEVEE-MF-055-V02 | EEVEE-MF-055 | food held directly at muzzle while Eevee waits/attends | V09 | V09/F09 | V09=1 | V09: ~167.4–171.6 s | source inventory; original V1/V2/I retained |
| EEVEE-MF-055-V03 | EEVEE-MF-055 | 食べ物が口元にある間ほぼ姿勢を変えない | V02 | V02/FOOD_PRESENT_WAIT | V02=1 | V02: 93.27–98.43 | source inventory; original V1/V2/I retained |

### EEVEE-MF-056 — Food contact / receive / mouth hold
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-056-V01 | EEVEE-MF-056 | food disappears at mouth; consumption occurs between adjacent fr… | V09 | V09/F10 | V09=1 | V09: ~171.5–171.8 s | source inventory; original V1/V2/I retained |
| EEVEE-MF-056-V02 | EEVEE-MF-056 | 食べ物を口元で接触/摂食 | V01 | V01/FOOD_CONTACT_EAT | V01=2 | V01: 01:14.87, 01:21.73 | source inventory; original V1/V2/I retained |
| EEVEE-MF-056-V03 | EEVEE-MF-056 | 食物が口元にある間の保持姿勢。明確な咀嚼反復は確認できない。 | V10 | V10/FOOD_CONTACT_HOLD | V10=2 | V10: 01:52.800, 01:59.200 | source inventory; original V1/V2/I retained |
| EEVEE-MF-056-V04 | EEVEE-MF-056 | 食べ物提示/口元保持 | V03 | V03/F11 | V03=1 | V03: M031 | source inventory; original V1/V2/I retained |
| EEVEE-MF-056-V05 | EEVEE-MF-056 | 食物を口元に保持し、口周辺が小さく反復。 | V08 | V08/FOOD_HOLD_CHEW | V08=1 | V08: M050 02:27.90–02:30.20 | source inventory; original V1/V2/I retained |
| EEVEE-MF-056-V06 | EEVEE-MF-056 | 食べ物が口元に接触・保持されるフェーズ | V11 | V11/F10 | V11=1 | V11: 111.6–115.0 | source inventory; original V1/V2/I retained |
| EEVEE-MF-056-V07 | EEVEE-MF-056 | 食物を口元で受け入れる口開き。 | V08 | V08/FOOD_RECEIVE | V08=1 | V08: M049 02:27.20–02:27.90 | source inventory; original V1/V2/I retained |

### EEVEE-MF-057 — Post-food processing pause
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-057-V01 | EEVEE-MF-057 | 摂食直後の短いほぼ静止; 食後の短い無動作処理間; 食物消失直後に一拍止まり、口を閉じる。『味わう』は解釈。; Food消失後から喜び反応までの短い静止/処理間。; 食べ物消失後、反応前に短いneutral間を置く | V01, V03, V08, V10, V11 | V01/FOOD_POST_EAT_PAUSE; V03/F12; V08/FOOD_PROCESS_PAUSE; V10/FOOD_PROCESS_STILL; V11/F11 | V01=2; V03=1; V08=1; V10=2; V11=1 | V01: 01:17.40, 01:24.83; V03: M032; V08: M051 02:30.20–02:31.20; V10: 01:56.100, 02:02.000; V11: 115.0–115.7 | source inventory; original V1/V2/I retained |

### EEVEE-MF-058 — Food-positive response
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-058-V01 | EEVEE-MF-058 | 食後の閉眼＋耳外開き＋大笑顔; 食物消失後の閉眼→開眼大口笑顔; 食後の短い喜び; 食後の強い閉眼笑顔、耳横開き、上体小バウンス。; immediate post-consumption pleasure response; Food後の… | V01, V02, V03, V08, V09, V10 | V01/FOOD_HAPPY_BURST; V02/FOOD_POST_EAT_JOY; V03/F13; V08/FOOD_HAPPY; V09/F11; V10/FOOD_POSITIVE | V01=2; V02=1; V03=1; V08=1; V09=1; V10=2 | V01: 01:18.53, 01:25.47; V02: 98.43–99.20; V03: M033; V08: M052 02:31.30–02:32.30; V09: 171.73–173.40 s; V10: 01:56.967, 02:03.100 | source inventory; original V1/V2/I retained |
| EEVEE-MF-058-V02 | EEVEE-MF-058 | 食後、目閉じ笑顔で頭をscreen-rightへ傾け、中央へ戻す | V11 | V11/F12 | V11=1 | V11: 115.8–117.2 | source inventory; original V1/V2/I retained |

### EEVEE-MF-059 — Gift/item presentation hold
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-059-V01 | EEVEE-MF-059 | 両前足でGiftを差し出し保持; Eevee appears already holding a flower-like gift centrally with …; Giftを前足付近で正面保持する特殊姿勢。; プレゼント状オブジェクト… | V03, V09, V10, V11 | V03/F21; V09/F13; V10/GIFT_HOLD; V11/F14 | V03=1; V09=1; V10=1; V11=1 | V03: M045; V09: ~192.0–194.8 s; V10: 02:17.900; V11: 131.0–133.3 | source inventory; original V1/V2/I retained |

### EEVEE-MF-060 — Gift-holding smile
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-060-V01 | EEVEE-MF-060 | Gift保持中に笑顔を作る; eye-close pleased smile while still holding gift; Gift保持中の閉眼笑顔。Gift消失後にも表情が残る。 | V03, V09, V10 | V03/F22; V09/F14; V10/GIFT_CLOSE_EYE_SMILE | V03=1; V09=1; V10=1 | V03: M046; V09: ~194.87–195.7 s; V10: 02:20.300 | source inventory; original V1/V2/I retained |

### EEVEE-MF-061 — Gift lower/release transition
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-061-V01 | EEVEE-MF-061 | Gift保持から目を閉じ、objectを下げ/消失させ、笑顔を残す | V11 | V11/F15 | V11=1 | V11: 133.4–135.3 | source inventory; original V1/V2/I retained |
| EEVEE-MF-061-V02 | EEVEE-MF-061 | gift vanishes, forepaws no longer hold object, happy eye-close l… | V09 | V09/F15 | V09=1 | V09: ~195.7–196.8 s | source inventory; original V1/V2/I retained |

### EEVEE-MF-062 — Gift afterglow / result smile
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-062-V01 | EEVEE-MF-062 | Gift消失後も笑顔が残る | V03 | V03/F23 | V03=1 | V03: M047 | source inventory; original V1/V2/I retained |
| EEVEE-MF-062-V02 | EEVEE-MF-062 | Gift結果後の短い喜び; short no-touch-visible eye-close/open-mouth smile after item-des…; Gift説明Overlay終了後に出る短い大きな喜び。 | V03, V09, V10 | V03/F24; V09/F16; V10/POST_GIFT_HAPPY | V03=1; V09=1; V10=1 | V03: M048; V09: ~200.9–201.67 s; V10: 02:30.200 | source inventory; original V1/V2/I retained |

### EEVEE-MF-063 — Entry / pop-up / appear-settle
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-063-V01 | EEVEE-MF-063 | Scene-entry whole-body transition into interaction view | V06 | V06/F02 | V06=1 | V06: 3.33–6.53 s | source inventory; original V1/V2/I retained |
| EEVEE-MF-063-V02 | EEVEE-MF-063 | 導入カットで下からせり上がる | V02 | V02/INTRO_POP_UP | V02=2 | V02: 1.30–1.77, 2.17–2.67 | source inventory; original V1/V2/I retained |
| EEVEE-MF-063-V03 | EEVEE-MF-063 | 画面下から出現し短く挨拶する | V03 | V03/F01 | V03=2 | V03: 5.07, 5.90 | source inventory; original V1/V2/I retained |

### EEVEE-MF-064 — Special backward recoil
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-064-V01 | EEVEE-MF-064 | 全身を大きく後ろへ反らす特殊リアクション | V04 | V04/F12 | V04=1 | V04: 4.733–5.167 | source inventory; original V1/V2/I retained |

### EEVEE-MF-065 — Special forepaw-lift accent
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-065-V01 | EEVEE-MF-065 | F12中に前足1本を高く上げ、肉球を見せる | V04 | V04/F13 | V04=1 | V04: 4.867–5.133 | source inventory; original V1/V2/I retained |

### EEVEE-MF-066 — Special forward bow
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-066-V01 | EEVEE-MF-066 | 後方反り後に頭/上体を深く前へ沈める | V04 | V04/F14 | V04=1 | V04: 5.300–5.667 | source inventory; original V1/V2/I retained |

### EEVEE-MF-067 — Special startle open-mouth face
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-067-V01 | EEVEE-MF-067 | 特殊シーケンスで顔露出直後の開眼/口開き注意表情 | V04 | V04/F17 | V04=1 | V04: 3.500–3.933 | source inventory; original V1/V2/I retained |

### EEVEE-MF-068 — Special closed-eye smile hold
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-068-V01 | EEVEE-MF-068 | 特殊シーケンス内の短い閉眼笑顔保持 | V04 | V04/F16 | V04=1 | V04: 3.933–4.333 | source inventory; original V1/V2/I retained |

### EEVEE-MF-069 — Grooming/appearance-change prep hold
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-069-V01 | EEVEE-MF-069 | 髪型変更前後の泡/雲エフェクト中に見える身体反応。エフェクト自体は身体Motionではない。 | V07 | V07/GROOM_CLOUD | V07=**8** | V07: 00:03.60–00:05.30, 00:27.70–00:29.20, 00:50.93–00:52.80, 01:15.20–01:16.80, 01:42.30–01:44.40, 02:08.67–02:10.80, 02:34.20–02:36.20, 03:00.80–03:02.90 | source inventory; original V1/V2/I retained |

### EEVEE-MF-070 — Grooming/appearance-change surprise
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-070-V01 | EEVEE-MF-070 | 通常のGROOM_SURPRISEの強いvariant。白目状/極端な見開きと大きい開口。 | V07 | V07/GROOM_SURPRISE_EXTREME | V07=**1** | V07: 03:01.60–03:03.00 | source inventory; original V1/V2/I retained |
| EEVEE-MF-070-V02 | EEVEE-MF-070 | 泡の退去に伴い開眼し、口を丸く開けて驚き状態を保持する。髪型state changeと同期。 | V07 | V07/GROOM_SURPRISE | V07=**7** | V07: 00:04.40–00:09.60, 00:28.60–00:31.40, 00:51.80–00:55.20, 01:16.00–01:21.70, 01:43.40–01:44.50, 02:10.00–02:11.00, 02:35.40–02:36.40 | source inventory; original V1/V2/I retained |

### EEVEE-MF-071 — Side-to-front turn
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-071-V01 | EEVEE-MF-071 | 横から正面へ向き直る | V03 | V03/F04 | V03=1 | V03: 42.90 | source inventory; original V1/V2/I retained |

### EEVEE-MF-072 — Room reposition turn
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-072-V01 | EEVEE-MF-072 | 遠景で横→背面→反対側横へ向きを変える。 | V08 | V08/ROOM_REPOSITION_TURN | V08=1 | V08: M061 02:54.00–02:55.50 | source inventory; original V1/V2/I retained |

### EEVEE-MF-073 — Recovery to neutral
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-073-V01 | EEVEE-MF-073 | Burst/抗議/傾け等から正面中立へ戻る依存相; 感情反応後に半目/開眼・耳復帰を経て中立へ戻る; 特殊/大反応後に頭・耳・まぶたをNeutralへ戻す; Short settling phase from expressive pos… | V01, V02, V04, V06, V08, V09, V10, V11 | V01/RECOVERY_TO_NEUTRAL; V02/RECOVERY_TO_NEUTRAL; V04/F15; V06/F09; V08/RECOVERY_TO_NEUTRAL; V09/F12; V10/RECOVER_TO_NEUTRAL; V11/F18 | V01=多数; V02=多数; V04=1明確 + variants; V06=follows most F03/F04/F06/F07 occurrences; V08=2; V09=after nearly every F03/F06/F11/F14 event; explicitly separated as M039, M047, M055; V10=多数・埋込（独立計数なし）; V11=多数 | V01: 各Primary Motion末尾; V02: M007,010,013,018,032,041,044,046,051,054,057,062,068,070; V04: 5.667–5.900 等; V06: e.g. 22.4–22.6; 35.7–36.0; 41.4–41.6; 68.3–68.6; 93.8–94.1; 97.3–97.5; 117.4–117.5 s; V08: M053 02:32.40–02… | source inventory; original V1/V2/I retained |
| EEVEE-MF-073-V02 | EEVEE-MF-073 | 強い喜びからNeutralへ戻る | V04 | V04/F07 | V04=3+1 variant | V04: 16.600–16.800 / 20.667–20.833 / 24.833–25.033 / 30.000–30.267variant | source inventory; original V1/V2/I retained |
| EEVEE-MF-073-V03 | EEVEE-MF-073 | 大肯定反応後、閉眼/頭下げから開眼し、短く口を開けて閉じる回復相。 | V05 | V05/POSITIVE_RECOVERY_MOUTH_OPEN | V05=1 | V05: M054 | source inventory; original V1/V2/I retained |
| EEVEE-MF-073-V04 | EEVEE-MF-073 | 特殊反応後、閉眼しながら前足を下ろして余韻を作る。 | V08 | V08/SPECIAL_RECOVERY | V08=1 | V08: M040 02:08.50–02:09.50 | source inventory; original V1/V2/I retained |

### EEVEE-MF-074 — Half-lid/downward recovery
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-074-V01 | EEVEE-MF-074 | 半眼〜やや下向きの顔で短時間保持する遷移。意味は断定できない。 | V07 | V07/HALF_LID_RECOVERY | V07=**1** | V07: 02:00.80–02:02.20 | source inventory; original V1/V2/I retained |

### EEVEE-MF-075 — Drowsy/rest recovery to neutral
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-075-V01 | EEVEE-MF-075 | 目覚め後に落ち着き直す | V03 | V03/F20 | V03=1 | V03: M042 | source inventory; original V1/V2/I retained |

### EEVEE-MF-076 — Positive touch afterglow
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-076-V01 | EEVEE-MF-076 | タッチ終了後まで残る閉眼・耳横倒し・笑顔 | V04 | V04/F10 | V04=1 | V04: 28.733–30.000 | source inventory; original V1/V2/I retained |

### EEVEE-MF-077 — Open-eye smile/bob, cause unresolved
| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp / IDs | Evidence |
|---|---|---|---|---|---|---|---|
| EEVEE-MF-077-V01 | EEVEE-MF-077 | 開眼のまま口を大きく開けて笑い、頭/胴を軽く弾ませる。 | V07 | V07/POS_OPEN_SMILE | V07=**8** | V07: 00:09.80–00:11.90, 00:31.60–00:33.80, 00:55.40–00:57.30, 01:22.00–01:24.00, 01:57.00–01:58.50, 02:39.00–02:40.70, 02:47.40–02:48.90, 03:09.40–03:11.50 | source inventory; original V1/V2/I retained |

## 6. Living / Physiological Master
| ID | Family | Coverage | Core observed mechanics |
|---|---|---:|---|
| EEVEE-MF-001 | Neutral bilateral blink | 7/11 | Short bilateral eyelid close followed by immediate reopen without a larger concurrent expressive action. |
| EEVEE-MF-002 | Context-linked short eye close | 4/11 | Very short eye close embedded in, or immediately adjacent to, another action; source inventories do not always establish whether it is a physiological blink. |
| EEVEE-MF-003 | Idle body micro-sway | 2/11 | Low-amplitude head/torso positional drift during otherwise neutral holding. |

## 7. Attention / Gaze Master
| ID | Family | Coverage | Core observed mechanics |
|---|---|---:|---|
| EEVEE-MF-011 | Hand-oriented attention candidate | 1/11 | Possible attention/gaze orientation toward the visible hand cursor; eye-only displacement is not strongly established. |
| EEVEE-MF-012 | Open-mouth attention hold | 2/11 | Open-eyed/open-mouth attention-like hold with little limb displacement; cause is unresolved in the source occurrence(s). |

## 8. Ear / Tail Micro Master
| ID | Family | Coverage | Core observed mechanics |
|---|---|---:|---|
| EEVEE-MF-004 | Tail idle sway / swish | 6/11 | Small or slow tail position change during idle/low-motion states; some sources treat it as a continuous layer rather than a discrete clip. |
| EEVEE-MF-005 | Independent single-ear flick | 1/11 | Brief isolated one-ear movement with face/torso largely neutral. |
| EEVEE-MF-006 | Bilateral ear emotion/follow-through | 2/11 | Bilateral ear lowering, outward rotation, or restoration coupled to another emotional/head/body action; not established as an independent clip in the relevant sources. |

## 9. Posture / Balance / COM Master
| ID | Family | Coverage | Core observed mechanics |
|---|---|---:|---|
| EEVEE-MF-063 | Entry / pop-up / appear-settle | 3/11 | Scene/startup transition where Eevee rises/appears into view or settles into the interaction camera; editor/UI causality is preserved. |
| EEVEE-MF-071 | Side-to-front turn | 1/11 | Head leads a turn from side orientation, followed by torso and forepaw/support adjustment into front-facing stance. |
| EEVEE-MF-072 | Room reposition turn | 1/11 | Distant whole-body orientation change through side/back views into another side orientation; detailed foot action is not confirmed. |

## 10. Forepaw Gesture Master
| ID | Family | Coverage | Core observed mechanics |
|---|---|---:|---|
| EEVEE-MF-036 | Touch-linked forepaw lift/offer | 5/11 | One or both forepaws lift toward the viewer during touch/contact context without confirmed reciprocal contact. |

## 11. Autonomous Idle Master
| ID | Family | Coverage | Core observed mechanics |
|---|---|---:|---|
| EEVEE-MF-013 | Autonomous curious head tilt | 7/11 | Input-free or autonomous-candidate head/neck tilt with a held side inclination and return; sources preserve screen-side rather than inventing anatomical L/R. |
| EEVEE-MF-014 | Autonomous head sway / shake | 2/11 | Input-free closed-eye or relaxed head movement through more than one lateral direction before re-centering. |
| EEVEE-MF-015 | Autonomous/contented smile hold | 5/11 | Input-free or startup-uncertain closed-eye smile with limited gross body displacement and possible ear relaxation. |

## 12. Autonomous Social Master
| ID | Family | Coverage | Core observed mechanics |
|---|---|---:|---|
| EEVEE-MF-016 | Autonomous bilateral forepaw lift | 4/11 | Both forepaws rise toward the viewer, usually with mouth opening, then lower back toward neutral; includes startup/autonomous-context variants when mechanics match. |
| EEVEE-MF-017 | Autonomous single-forepaw raise | 1/11 | One forepaw rises toward the viewer and returns without confirmed reciprocal contact. |
| EEVEE-MF-018 | Autonomous/unknown deep bow → bilateral paw rise | 2/11 | Deep forward bow followed by a bilateral forepaw/paw-pad presentation and closed-eye settling, where touch causality is not established. |

## 13. Positive Touch Master
| ID | Family | Coverage | Core observed mechanics |
|---|---|---:|---|
| EEVEE-MF-027 | Positive-touch onset | 1/11 | Short transition from contact/neutral into a positive closed-eye state; sources preserve cases where mouth or eyelids clearly lead. |
| EEVEE-MF-028 | Gentle positive touch hold | 9/11 | Contact-associated closed-eye smile/pleasant hold with limited COM excursion and no deep bow. |
| EEVEE-MF-029 | Strong positive touch burst | 8/11 | Contact-associated large smile with stronger ear splay and head/torso bob/lift than the gentle hold, but without the deep bow→paw-rise grammar. |
| EEVEE-MF-030 | Two-lobe positive touch sequence | 1/11 | Positive touch performance explicitly recorded as first closed-eye smile lobe, brief reset/opening, then second lobe. |
| EEVEE-MF-031 | Positive touch retrigger | 1/11 | Additional closed-eye positive pulse after a prior full reaction and a short reset, preserved because source explicitly separated the retrigger. |
| EEVEE-MF-032 | Touch-linked deep bow → rebound/paw rise | 3/11 | Touch-associated large sequence with deep bow/compression, rebound/upright recovery and bilateral forepaw participation; retained separately from autonomous bow/paw sequences. |
| EEVEE-MF-033 | Touch head-lean / tilt response | 4/11 | Contact-associated head/neck lean or tilt held toward/away from the contact direction without the full negative withdrawal grammar. |
| EEVEE-MF-034 | Touch open-mouth small/hold response | 3/11 | Touch-associated open-mouth response with limited gross body action; emotional valence is not assumed when the source leaves it unresolved. |
| EEVEE-MF-035 | Touch surprise/open-mouth → smile | 2/11 | Touch response that begins with open-eyed/open-mouth surprise/attention and then resolves into a positive smile. |
| EEVEE-MF-037 | Small touch-linked eye-close/sink | 1/11 | Small touch-linked eye close with slight head/torso lowering, kept separate where source inventories did not equate it with a smiling hold. |

## 14. Negative / Boundary Master
| ID | Family | Coverage | Core observed mechanics |
|---|---|---:|---|
| EEVEE-MF-039 | Small uneasy facial warning | 1/11 | Small negative/uneasy facial change without a large body withdrawal. |
| EEVEE-MF-040 | Angry/protest facial burst | 2/11 | Negative reaction led by sharper eye/face shape and mouth opening, with limited whole-body displacement. |
| EEVEE-MF-041 | Strong closed-eye/ear-splay negative face | 1/11 | Strong touch-negative face/ear reaction with forceful eye closure/ear lateralization but without the deeper whole-body droop/recoil grammars. |
| EEVEE-MF-042 | Sad/downcast negative face hold | 1/11 | Sustained sad/concerned facial state while gross posture remains comparatively upright. |
| EEVEE-MF-043 | Negative droop / body sink | 2/11 | Negative response in which ears/head and then torso/COM move downward into a lower held posture before recovery. |
| EEVEE-MF-044 | Half-lid/downcast disengagement hold | 2/11 | Half-lidded/downcast negative or ambiguous state maintained without a large recoil. |
| EEVEE-MF-045 | Face-touch withdrawal head tilt | 1/11 | Face/nose touch followed by eye close and a large lateral head withdrawal/tilt, then dissatisfied/half-lid recovery. |
| EEVEE-MF-046 | Side recoil / rotate away-to-front | 1/11 | From a side/profile state, head/body recoil and rotate sharply with substantial root/COM participation before settling. |
| EEVEE-MF-047 | Strong rejection with paw/feet thrust | 1/11 | Large rejection sequence with sharp negative face, major whole-body motion and visible paw/foot-pad thrust toward the camera. |
| EEVEE-MF-048 | Impact-like face flinch | 1/11 | Brief strong eye closure and small head retraction synchronized with touch/context; screen effects are not counted as body motion. |
| EEVEE-MF-049 | Full-body turn away | 1/11 | Large whole-body rotation from front toward back/away after interaction context. |

## 15. Reciprocal Social Interaction Master
| ID | Family | Coverage | Core observed mechanics |
|---|---|---:|---|
| EEVEE-MF-051 | Reciprocal paw offer / WAIT | 2/11 | Forepaw is presented and held toward the player as an explicit reciprocal-interaction offer/WAIT state. |
| EEVEE-MF-052 | High-five contact acknowledgment | 1/11 | Player contact occurs on the presented paw; kept separate from the offer/WAIT and post-contact facial payoff. |
| EEVEE-MF-053 | High-five success smile | 1/11 | Short closed-eye smile immediately following successful paw contact. |
| EEVEE-MF-054 | High-five alternate post-contact response | 1/11 | Observed post-contact mouth/eye response that differs from the typical success smile; meaning remains unresolved. |

## 16. Feeding Master
| ID | Family | Coverage | Core observed mechanics |
|---|---|---:|---|
| EEVEE-MF-055 | Food notice / presentation wait | 3/11 | Food is presented/approaches while Eevee attends or waits before mouth contact; source certainty about independent notice motion varies. |
| EEVEE-MF-056 | Food contact / receive / mouth hold | 6/11 | Food contacts or is held at the mouth; mouth/head carry the action while torso remains comparatively stable. |
| EEVEE-MF-057 | Post-food processing pause | 5/11 | Food disappears/contact ends and Eevee holds nearly still for a short beat before emotional evaluation/response. |
| EEVEE-MF-058 | Food-positive response | 7/11 | Post-food positive response, usually closed-eye smile with ear splay and small head/torso accent; tilt variants are retained. |

## 17. Gift / Item Master
| ID | Family | Coverage | Core observed mechanics |
|---|---|---:|---|
| EEVEE-MF-059 | Gift/item presentation hold | 4/11 | Gift/object is held centrally with forepaws toward the player for a sustained presentation. |
| EEVEE-MF-060 | Gift-holding smile | 3/11 | Eyes close into a pleased smile while the item remains presented/held. |
| EEVEE-MF-061 | Gift lower/release transition | 2/11 | Gift/object lowers or disappears while forepaw/face state transitions away from presentation. |
| EEVEE-MF-062 | Gift afterglow / result smile | 3/11 | Positive facial state persists or reappears after the gift disappears or result UI resolves. |

## 18. Rest / Doze / Sleep Master
| ID | Family | Coverage | Core observed mechanics |
|---|---|---:|---|
| EEVEE-MF-019 | Relaxed long eye-close moving hold | 5/11 | Several-second relaxed eye-close with ears lowered/outward and slow head/torso settling or sway; shallower/shorter than the clearly deep doze state when source distinguishes them. |
| EEVEE-MF-020 | Doze/drowsy entry | 2/11 | Transition from neutral toward rest, commonly eyelids first, then head lowering and ear-state change. |
| EEVEE-MF-021 | Deep doze / drowsy hold | 3/11 | Long closed-eye low-activity hold with head/body lowered or swaying; distinct from short relaxed eye-close where sources distinguish depth/duration. |
| EEVEE-MF-022 | Ear switching inside doze | 1/11 | Repeated asymmetric ear-state switching while the rest of the body remains in a doze hold. |
| EEVEE-MF-023 | Distant sleep stillness | 1/11 | Distant-view sleep state with very little body motion; screen sleep symbols are excluded as body motion. |
| EEVEE-MF-024 | Sleep micro-cycle | 1/11 | Repeated small mouth-area/head/upper-body cycle observed while eyes remain closed in sleep. |
| EEVEE-MF-026 | Wake/startle transition | 3/11 | Rest state ends with opening eyes and raising/reorienting the head, sometimes with open mouth/startle and secondary body movement. |

## 19. Grooming / Appearance-Change Master
| ID | Family | Coverage | Core observed mechanics |
|---|---|---:|---|
| EEVEE-MF-069 | Grooming/appearance-change prep hold | 1/11 | Body/face state observed while grooming/appearance-change effects obscure the head; the visual effect itself is explicitly excluded as body motion. |
| EEVEE-MF-070 | Grooming/appearance-change surprise | 1/11 | After grooming/appearance-change occlusion clears, Eevee opens eyes and forms an O-shaped mouth; extreme eye/open-mouth performance is an intensity variant. |
| EEVEE-MF-077 | Open-eye smile/bob, cause unresolved | 1/11 | Open-eyed large-mouth smile with small head/torso bounce where the source cannot reliably assign interaction vs autonomous cause. |

## 20. Large Emotional / Hero Master
| ID | Family | Coverage | Core observed mechanics |
|---|---|---:|---|
| EEVEE-MF-038 | Positive jump hero response | 1/11 | Large positive reaction where the whole body rises enough that feet appear to leave the ground. |
| EEVEE-MF-050 | Turn return with bilateral paw presentation | 1/11 | Return from back-facing orientation to front while raising both forepaws, ending in a frontal peak. |
| EEVEE-MF-064 | Special backward recoil | 1/11 | One-off special sequence phase with major backward whole-body lean/recoil and COM movement. |
| EEVEE-MF-065 | Special forepaw-lift accent | 1/11 | One-forepaw high lift/paw-pad accent embedded in the special recoil sequence; source marks independence as uncertain/submotion candidate. |
| EEVEE-MF-066 | Special forward bow | 1/11 | Deep forward bow phase following the special recoil context, with head/torso/COM and ear participation. |
| EEVEE-MF-067 | Special startle open-mouth face | 1/11 | Special-sequence open-eyed/open-mouth startle/attention face when the character becomes visible. |
| EEVEE-MF-068 | Special closed-eye smile hold | 1/11 | Closed-eye smile hold inside a special sequence; kept distinct in source due context even though body channels overlap other smile holds. |

## 21. Recovery / Settle / Afterglow Master
| ID | Family | Coverage | Core observed mechanics |
|---|---|---:|---|
| EEVEE-MF-073 | Recovery to neutral | 9/11 | Return from an expressive/action peak toward the source-defined neutral baseline; timing and channel order vary by parent family. |
| EEVEE-MF-074 | Half-lid/downward recovery | 1/11 | Short half-lidded/downward-faced transition between expressive states; semantic valence is unresolved. |
| EEVEE-MF-075 | Drowsy/rest recovery to neutral | 1/11 | Non-touch recovery from drowsy/wake state through closed/half-lid settling toward normal neutral. |
| EEVEE-MF-076 | Positive touch afterglow | 1/11 | Closed-eye positive expression/ear state persists after the triggering contact phase has ended. |

## 22. Intentional Stillness / WAIT Master
| ID | Family | Coverage | Core observed mechanics |
|---|---|---:|---|
| EEVEE-MF-007 | Front neutral still hold | 10/11 | Front-facing low-motion baseline/WAIT-like hold with no large body action; small eye/ear/tail motion may remain. |
| EEVEE-MF-008 | Touch latency / tolerate stillness | 2/11 | Player contact is present but Eevee intentionally remains near the current posture before another response or transition. |
| EEVEE-MF-009 | Side/profile still hold | 3/11 | Non-front-facing side/profile waiting state with little gross motion. |
| EEVEE-MF-010 | Close-up forepaw rest/presentation hold | 1/11 | UI-linked close-up state in which forepaws are placed toward the viewer and held with little further action. |
| EEVEE-MF-025 | Touch during rest with delayed/no immediate response | 1/11 | Touch occurs during doze/rest but the existing rest pose is maintained for a measurable interval before waking. |

## 23. Transition Master
| ID | Family | Coverage | Core observed mechanics |
|---|---|---:|---|
| EEVEE-MF-063 | Entry / pop-up / appear-settle | 3/11 | Scene/startup transition where Eevee rises/appears into view or settles into the interaction camera; editor/UI causality is preserved. |
| EEVEE-MF-071 | Side-to-front turn | 1/11 | Head leads a turn from side orientation, followed by torso and forepaw/support adjustment into front-facing stance. |
| EEVEE-MF-072 | Room reposition turn | 1/11 | Distant whole-body orientation change through side/back views into another side orientation; detailed foot action is not confirmed. |

## 24. Emotion / Motion Propagation Patterns
- **Positive touch:** eye/mouth onset can lead; stronger variants recruit ears, head/torso and sometimes COM. Deep-bow families recruit root/COM and forepaws and are not reduced to facial smile variants.
- **Negative touch:** facial warning can remain local, while droop/recoil/rejection families progressively recruit ears → head/torso → COM/support.
- **Rest:** source-confirmed examples frequently stage eyelid change before deeper head/ear state; doze can preserve life through ear micro-cycles or slow sway while gross motion is suppressed.
- **Afterglow:** positive expression can outlast touch, gift visibility or the large body peak; these held states are retained rather than truncated into recovery.

## 25. Grounding / Support Patterns
| Pattern | Families / evidence pattern |
|---|---|
| PLANTED | Face/ear/eye reactions, neutral stillness, feeding holds, gift holds, many positive/negative facial states. |
| WEIGHT_SHIFT | Head tilts, positive bobs, droop, deep bows, forepaw lifts and recovery phases. |
| SUPPORT_CHANGE | Positive jump and some scene-entry/large paw-thrust performances. |
| TURN | Side-to-front, room reposition, turn-away/return sequences. |
| UNCLEAR | Distant/occluded footage where foot support is not visible enough; Master does not infer hidden steps. |

## 26. Ear Role Master
| Ear role | Corpus treatment |
|---|---|
| independent micro | Confirmed isolated single-ear flick in V01; not generalized to all videos. |
| attention lead | Not established as a corpus-wide independent system; retained only where source family mechanics support it. |
| emotion amplifier | Strong positive and negative families repeatedly recruit both ears, often after facial onset. |
| follow-through | Head tilt, bow, turn and recovery families commonly carry ear follow-through. |
| asymmetric state | Explicit in V01 doze ear-switch cycles. |
| rest / doze state | Relaxed/doze families keep ears lowered/outward or switch asymmetrically. |
| rhythmic phrase lead | Not established as a corpus-wide independent rule. |
| quiet | Feeding mouth-hold, neutral facial pulses and other local actions can leave ears comparatively quiet. |

## 27. Tail Role Master
| Role | Corpus treatment |
|---|---|
| PRIMARY_ACTION | Rare; small tail-only swish/sway is observed, but no broad large-wag family is inferred. |
| LOCAL_RESPONSE | Limited/unclear; not generalized. |
| FOLLOW_THROUGH | Whole-body turns and large actions can carry the tail with the body. |
| INDEPENDENT_MICRO | Supported by tail-idle sway/swish families in multiple source inventories. |
| EMOTION_AMPLIFIER | Source-dependent and weaker than ear evidence. |
| QUIET | Many front-facing facial/paw/feeding interactions show no need for tail as the lead channel. |
| UNCLEAR | V06 tail/torso secondary sway is V2 and remains coupled/uncertain. |

## 28. Repetition / Variation
### Repeated Families
- Neutral stillness, positive touch, blink/short-close, head tilt, recovery, feeding phases and gift phases recur across the corpus.
- High within-video repetition is especially explicit in V01 positive touch/head tilt, V06 deep-bow and bliss families, V07 positive/grooming/forepaw families, V08 touch positive/sleep micro-cycle, V09 touch positive, V10 two-lobe touch positive, and V11 standard touch positive.
- Visually close but mechanically distinct families are deliberately retained: gentle positive vs deep bow/rebound; head tilt vs head sway; protest face vs body droop; neutral stillness vs social/interaction WAIT; relaxed eye-close vs doze/sleep.
### Variant Axes
Side/screen-side; amplitude; duration; initial state; face/eyelid/mouth; ear participation; forepaw participation; torso/COM; tail; contact location; interaction phase; settle; afterglow.
### Repetition Risk
Families with HIGH visual repetition risk within this corpus: neutral front hold, standard positive touch, short eye-close/blink and repeated grooming surprise. This is an observation about corpus repetition, not a Grimo solution recommendation.

## 29. Temporal Structure Patterns
- Positive touch commonly resolves as `neutral/contact → onset → hold/peak → settle → neutral/afterglow`; exact phase presence varies.
- Touch-linked deep bow: `contact/upright → head/ear descent → deep bow/compression → rebound → bilateral paw peak → closed-eye afterglow → recovery`.
- Reciprocal high-five (V02): `paw offer/presentation → WAIT → contact acknowledgment → success/alternate facial response → retract/repeat → completion payoff`.
- Feeding: `presentation/notice → mouth contact/hold/consume → post-food processing pause → food-positive response → settle`.
- Doze: `entry → long hold (+ optional ear-switch/micro cycle) → delayed or immediate wake transition → recovery`.
- Gift: `presentation hold → smile while holding → lower/release → afterglow/result smile`.
- Grooming: `prep/occluded body hold → reveal/open-eye O-mouth surprise → held surprise/intensity variant → settle`; VFX/hairstyle change is not body Motion.

## 30. Front-View Readability Matrix
| Global ID | Family | Front-view readability | Rationale |
|---|---|---|---|
| EEVEE-MF-001 | Neutral bilateral blink | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-002 | Context-linked short eye close | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-003 | Idle body micro-sway | MEDIUM | COM/turn/depth contribution is meaningful but still partly readable frontally. |
| EEVEE-MF-004 | Tail idle sway / swish | LOW | Action depends materially on side/back/distant or subtle tail/gaze information. |
| EEVEE-MF-005 | Independent single-ear flick | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-006 | Bilateral ear emotion/follow-through | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-007 | Front neutral still hold | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-008 | Touch latency / tolerate stillness | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-009 | Side/profile still hold | LOW | Action depends materially on side/back/distant or subtle tail/gaze information. |
| EEVEE-MF-010 | Close-up forepaw rest/presentation hold | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-011 | Hand-oriented attention candidate | MEDIUM | COM/turn/depth contribution is meaningful but still partly readable frontally. |
| EEVEE-MF-012 | Open-mouth attention hold | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-013 | Autonomous curious head tilt | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-014 | Autonomous head sway / shake | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-015 | Autonomous/contented smile hold | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-016 | Autonomous bilateral forepaw lift | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-017 | Autonomous single-forepaw raise | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-018 | Autonomous/unknown deep bow → bilateral paw rise | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-019 | Relaxed long eye-close moving hold | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-020 | Doze/drowsy entry | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-021 | Deep doze / drowsy hold | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-022 | Ear switching inside doze | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-023 | Distant sleep stillness | LOW | Action depends materially on side/back/distant or subtle tail/gaze information. |
| EEVEE-MF-024 | Sleep micro-cycle | MEDIUM | COM/turn/depth contribution is meaningful but still partly readable frontally. |
| EEVEE-MF-025 | Touch during rest with delayed/no immediate response | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-026 | Wake/startle transition | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-027 | Positive-touch onset | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-028 | Gentle positive touch hold | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-029 | Strong positive touch burst | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-030 | Two-lobe positive touch sequence | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-031 | Positive touch retrigger | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-032 | Touch-linked deep bow → rebound/paw rise | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-033 | Touch head-lean / tilt response | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-034 | Touch open-mouth small/hold response | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-035 | Touch surprise/open-mouth → smile | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-036 | Touch-linked forepaw lift/offer | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-037 | Small touch-linked eye-close/sink | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-038 | Positive jump hero response | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-039 | Small uneasy facial warning | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-040 | Angry/protest facial burst | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-041 | Strong closed-eye/ear-splay negative face | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-042 | Sad/downcast negative face hold | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-043 | Negative droop / body sink | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-044 | Half-lid/downcast disengagement hold | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-045 | Face-touch withdrawal head tilt | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-046 | Side recoil / rotate away-to-front | MEDIUM | COM/turn/depth contribution is meaningful but still partly readable frontally. |
| EEVEE-MF-047 | Strong rejection with paw/feet thrust | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-048 | Impact-like face flinch | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-049 | Full-body turn away | LOW | Action depends materially on side/back/distant or subtle tail/gaze information. |
| EEVEE-MF-050 | Turn return with bilateral paw presentation | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-051 | Reciprocal paw offer / WAIT | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-052 | High-five contact acknowledgment | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-053 | High-five success smile | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-054 | High-five alternate post-contact response | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-055 | Food notice / presentation wait | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-056 | Food contact / receive / mouth hold | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-057 | Post-food processing pause | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-058 | Food-positive response | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-059 | Gift/item presentation hold | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-060 | Gift-holding smile | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-061 | Gift lower/release transition | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-062 | Gift afterglow / result smile | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-063 | Entry / pop-up / appear-settle | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-064 | Special backward recoil | MEDIUM | COM/turn/depth contribution is meaningful but still partly readable frontally. |
| EEVEE-MF-065 | Special forepaw-lift accent | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-066 | Special forward bow | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-067 | Special startle open-mouth face | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-068 | Special closed-eye smile hold | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-069 | Grooming/appearance-change prep hold | MEDIUM | COM/turn/depth contribution is meaningful but still partly readable frontally. |
| EEVEE-MF-070 | Grooming/appearance-change surprise | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-071 | Side-to-front turn | MEDIUM | COM/turn/depth contribution is meaningful but still partly readable frontally. |
| EEVEE-MF-072 | Room reposition turn | LOW | Action depends materially on side/back/distant or subtle tail/gaze information. |
| EEVEE-MF-073 | Recovery to neutral | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-074 | Half-lid/downward recovery | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-075 | Drowsy/rest recovery to neutral | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-076 | Positive touch afterglow | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |
| EEVEE-MF-077 | Open-eye smile/bob, cause unresolved | HIGH | Face/ears/paws/silhouette remain readable from the corpus front interaction view. |

## 31. Cross-Video Source Matrix
| Master Family | V01 | V02 | V03 | V04 | V05 | V06 | V07 | V08 | V09 | V10 | V11 | Coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|---:|
| EEVEE-MF-001 Neutral bilateral blink | — | ✓ BLINK | ✓ F25 | — | ✓ BLINK | ✓ F01 | — | ✓ BLINK | ✓ F02 | ✓ BLINK | — | 11/11 |
| EEVEE-MF-002 Context-linked short eye close | ✓ SHORT_EYELID_CLOSE | — | — | ✓ F11 | ✓ EYE_CLOSE_SHORT | — | ✓ BRIEF_EYE_CLOSE | — | — | — | — | 11/11 |
| EEVEE-MF-003 Idle body micro-sway | — | — | — | ✓ F01 | — | — | ✓ BODY_IDLE_MICRO_SWAY | — | — | — | — | 11/11 |
| EEVEE-MF-004 Tail idle sway / swish | ✓ TAIL_SWAY_SUBTLE | — | ✓ F14 | — | ✓ TAIL_IDLE_SWAY | ✓ F10 | ✓ TAIL_IDLE_SWAY_SMALL | — | — | ✓ TAIL_SWAY_SLOW | — | 11/11 |
| EEVEE-MF-005 Independent single-ear flick | ✓ EAR_FLICK_SINGLE | — | — | — | — | — | — | — | — | — | — | 11/11 |
| EEVEE-MF-006 Bilateral ear emotion/follow-through | — | — | — | — | — | ✓ F05 | ✓ EAR_FOLLOW_OUTWARD | — | — | — | — | 11/11 |
| EEVEE-MF-007 Front neutral still hold | ✓ MACRO_STILL_FRONT_NEUTRAL | ✓ BASE_NEUTRAL_STILLNESS | ✓ F05 | — | ✓ NEUTRAL_STILL | ✓ F08 | ✓ MACRO_STILL | ✓ NEUTRAL_IDLE | ✓ F01 | ✓ IDLE_STILL_HOLD | ✓ F03 | 11/11 |
| EEVEE-MF-008 Touch latency / tolerate stillness | — | — | — | ✓ F02 | — | — | — | — | ✓ F07 | — | — | 11/11 |
| EEVEE-MF-009 Side/profile still hold | — | — | ✓ F03 | — | ✓ SIDE_PROFILE_STATE | — | — | ✓ STILLNESS_ROOM | — | — | — | 11/11 |
| EEVEE-MF-010 Close-up forepaw rest/presentation hold | — | — | ✓ F02 | — | — | — | — | — | — | — | — | 11/11 |
| EEVEE-MF-011 Hand-oriented attention candidate | ✓ GAZE_ORIENT_TO_HAND_CANDIDATE | — | — | — | — | — | — | — | — | — | — | 11/11 |
| EEVEE-MF-012 Open-mouth attention hold | — | — | — | — | — | — | ✓ MOUTH_OPEN_ROUND | ✓ MOUTH_OPEN_ATTENTION | — | — | — | 11/11 |
| EEVEE-MF-013 Autonomous curious head tilt | ✓ HEAD_TILT_SCREEN_RIGHT | ✓ IDLE_DROWSY_HEAD_TILT | ✓ F16 | — | ✓ AUTO_HEAD_TILT_LONG | — | ✓ HEAD_TILT_R | ✓ HEAD_TILT_AUTONOMOUS,HEAD_TILT_EYE_CLOSE | — | ✓ HEAD_TILT_LARGE_SCREEN_RIGHT | — | 11/11 |
| EEVEE-MF-014 Autonomous head sway / shake | — | — | — | — | ✓ AUTO_HEAD_SHAKE_SWAY | — | — | — | — | — | ✓ F16 | 11/11 |
| EEVEE-MF-015 Autonomous/contented smile hold | ✓ IDLE_CONTENTED_SMILE_EAR_SPREAD | — | ✓ F15 | — | ✓ ENTRY_HAPPY_GREETING,AUTO_HAPPY_SMILE_IDLE | — | — | — | — | ✓ INITIAL_HAPPY_HOLD,IDLE_SMILE | ✓ F01 | 11/11 |
| EEVEE-MF-016 Autonomous bilateral forepaw lift | ✓ BOTH_FOREPAW_LIFT_FORWARD | — | — | — | — | ✓ F06 | — | — | — | ✓ IDLE_FOREPAW_GESTURE | ✓ F02 | 11/11 |
| EEVEE-MF-017 Autonomous single-forepaw raise | — | — | — | — | — | — | ✓ FOREPAW_RAISE_R | — | — | — | — | 11/11 |
| EEVEE-MF-018 Autonomous/unknown deep bow → bilateral paw rise | — | — | — | — | — | — | ✓ BOW_BIPAW_SEQUENCE | — | — | — | ✓ F09 | 11/11 |
| EEVEE-MF-019 Relaxed long eye-close moving hold | ✓ BRIEF_RELAXED_EYE_CLOSE_EAR_DROOP | — | — | — | — | ✓ F07 | ✓ RELAXED_CLOSE_SWAY | — | — | ✓ RELAXED_EYE_CLOSE_LONG | ✓ F17 | 11/11 |
| EEVEE-MF-020 Doze/drowsy entry | ✓ DOZE_ENTRY | — | ✓ F17 | — | — | — | — | — | — | — | — | 11/11 |
| EEVEE-MF-021 Deep doze / drowsy hold | ✓ DOZE_HOLD | — | ✓ F18 | — | — | — | — | — | — | ✓ DOZE_BOW_HOLD | — | 11/11 |
| EEVEE-MF-022 Ear switching inside doze | ✓ DOZE_EAR_SWITCH_CYCLE | — | — | — | — | — | — | — | — | — | — | 11/11 |
| EEVEE-MF-023 Distant sleep stillness | — | — | — | — | — | — | — | ✓ SLEEP_STILLNESS_DISTANT | — | — | — | 11/11 |
| EEVEE-MF-024 Sleep micro-cycle | — | — | — | — | — | — | — | ✓ SLEEP_MICRO_CYCLE | — | — | — | 11/11 |
| EEVEE-MF-025 Touch during rest with delayed/no immediate response | — | — | — | — | — | — | — | — | — | ✓ TOUCH_DURING_DOZE_NO_IMMEDIATE_RESPONSE | — | 11/11 |
| EEVEE-MF-026 Wake/startle transition | ✓ WAKE_ON_TOUCH_STARTLE | — | ✓ F19 | — | — | — | — | — | — | ✓ TOUCH_WAKE_RESPONSE | — | 11/11 |
| EEVEE-MF-027 Positive-touch onset | — | — | — | ✓ F03,F09 | — | — | — | — | — | — | — | 11/11 |
| EEVEE-MF-028 Gentle positive touch hold | ✓ TOUCH_RELAXED_EYES_CLOSED_SMILE | ✓ TOUCH_POSITIVE_CLOSED_EYE_SMILE | ✓ F07,F09 | ✓ F04 | ✓ TOUCH_POSITIVE_GENTLE | ✓ F04 | ✓ POS_CLOSED_SMALL | — | ✓ F03 | ✓ TOUCH_POSITIVE_SHORT | — | 11/11 |
| EEVEE-MF-029 Strong positive touch burst | ✓ TOUCH_POSITIVE_BURST_EAR_SPREAD | ✓ TOUCH_POSITIVE_EFFECT_REACTION,SPECIAL_HEART_JOY | ✓ F10 | ✓ F05,F06 | ✓ TOUCH_POSITIVE_LARGE | — | ✓ POS_LARGE_MUSIC | ✓ TOUCH_POSITIVE | — | — | ✓ F05 | 11/11 |
| EEVEE-MF-030 Two-lobe positive touch sequence | — | — | — | — | — | — | — | — | — | ✓ TOUCH_POSITIVE_FULL | — | 11/11 |
| EEVEE-MF-031 Positive touch retrigger | — | — | — | — | — | — | — | — | — | ✓ TOUCH_POSITIVE_RETRIGGER | — | 11/11 |
| EEVEE-MF-032 Touch-linked deep bow → rebound/paw rise | — | — | — | — | — | ✓ F03 | — | — | ✓ F06 | ✓ TOUCH_BOW_PAW_POP | — | 11/11 |
| EEVEE-MF-033 Touch head-lean / tilt response | ✓ TOUCH_HEAD_LEAN_RELAX | ✓ TOUCH_HEAD_TILT_FOLLOW | ✓ F06 | — | — | — | — | — | ✓ F04 | — | — | 11/11 |
| EEVEE-MF-034 Touch open-mouth small/hold response | — | ✓ TOUCH_MOUTH_OPEN_MILD | — | ✓ F08 | — | — | — | — | — | ✓ TOUCH_MOUTH_OPEN_SMALL | — | 11/11 |
| EEVEE-MF-035 Touch surprise/open-mouth → smile | — | — | ✓ F08 | — | — | — | — | — | — | — | ✓ F06 | 11/11 |
| EEVEE-MF-036 Touch-linked forepaw lift/offer | ✓ TOUCH_SINGLE_FOREPAW_LIFT | — | — | — | ✓ FOREPAW_LIFT_SMALL | — | — | — | ✓ F05 | ✓ TOUCH_PAW_OFFER | ✓ F07 | 11/11 |
| EEVEE-MF-037 Small touch-linked eye-close/sink | — | — | — | — | — | — | ✓ TOUCH_CLOSE_SMALL | — | — | — | — | 11/11 |
| EEVEE-MF-038 Positive jump hero response | — | — | — | — | — | — | — | — | — | — | ✓ F13 | 11/11 |
| EEVEE-MF-039 Small uneasy facial warning | ✓ TOUCH_UNEASY_FACE_SMALL | — | — | — | — | — | — | — | — | — | — | 11/11 |
| EEVEE-MF-040 Angry/protest facial burst | ✓ TOUCH_NEGATIVE_PROTEST_FACE | — | — | — | ✓ NEGATIVE_ANGRY_BURST | — | — | — | — | — | — | 11/11 |
| EEVEE-MF-041 Strong closed-eye/ear-splay negative face | — | ✓ TOUCH_NEGATIVE_STRONG | — | — | — | — | — | — | — | — | — | 11/11 |
| EEVEE-MF-042 Sad/downcast negative face hold | — | — | — | — | ✓ NEGATIVE_SAD_FACE_STATE | — | — | — | — | — | — | 11/11 |
| EEVEE-MF-043 Negative droop / body sink | ✓ TOUCH_NEGATIVE_SINK_EAR_DROOP | — | — | — | ✓ NEGATIVE_DROOP | — | — | — | — | — | — | 11/11 |
| EEVEE-MF-044 Half-lid/downcast disengagement hold | — | — | — | — | ✓ ANNOYED_HALF_LID_STATE | — | — | — | ✓ F08 | — | — | 11/11 |
| EEVEE-MF-045 Face-touch withdrawal head tilt | — | — | — | — | — | — | — | — | — | — | ✓ F04 | 11/11 |
| EEVEE-MF-046 Side recoil / rotate away-to-front | — | — | — | — | ✓ SIDE_RECOIL_ROTATE | — | — | — | — | — | — | 11/11 |
| EEVEE-MF-047 Strong rejection with paw/feet thrust | — | — | — | — | ✓ STRONG_REJECTION_PAW_THRUST | — | — | — | — | — | — | 11/11 |
| EEVEE-MF-048 Impact-like face flinch | — | — | — | — | — | — | — | — | — | — | ✓ F08 | 11/11 |
| EEVEE-MF-049 Full-body turn away | — | — | — | — | — | — | — | ✓ TURN_AWAY_FULL | — | — | — | 11/11 |
| EEVEE-MF-050 Turn return with bilateral paw presentation | — | — | — | — | — | — | — | ✓ TURN_RETURN_DOUBLE_PAW | — | — | — | 11/11 |
| EEVEE-MF-051 Reciprocal paw offer / WAIT | ✓ SINGLE_FOREPAW_REACH_FORWARD | ✓ HIGH_FIVE_PAW_OFFER_HOLD | — | — | — | — | — | — | — | — | — | 11/11 |
| EEVEE-MF-052 High-five contact acknowledgment | — | ✓ HIGH_FIVE_CONTACT | — | — | — | — | — | — | — | — | — | 11/11 |
| EEVEE-MF-053 High-five success smile | — | ✓ HIGH_FIVE_SUCCESS_SMILE | — | — | — | — | — | — | — | — | — | 11/11 |
| EEVEE-MF-054 High-five alternate post-contact response | — | ✓ HIGH_FIVE_ALT_RESPONSE | — | — | — | — | — | — | — | — | — | 11/11 |
| EEVEE-MF-055 Food notice / presentation wait | — | ✓ FOOD_PRESENT_WAIT | — | — | — | — | — | ✓ FOOD_NOTICE | ✓ F09 | — | — | 11/11 |
| EEVEE-MF-056 Food contact / receive / mouth hold | ✓ FOOD_CONTACT_EAT | — | ✓ F11 | — | — | — | — | ✓ FOOD_RECEIVE,FOOD_HOLD_CHEW | ✓ F10 | ✓ FOOD_CONTACT_HOLD | ✓ F10 | 11/11 |
| EEVEE-MF-057 Post-food processing pause | ✓ FOOD_POST_EAT_PAUSE | — | ✓ F12 | — | — | — | — | ✓ FOOD_PROCESS_PAUSE | — | ✓ FOOD_PROCESS_STILL | ✓ F11 | 11/11 |
| EEVEE-MF-058 Food-positive response | ✓ FOOD_HAPPY_BURST | ✓ FOOD_POST_EAT_JOY | ✓ F13 | — | — | — | — | ✓ FOOD_HAPPY | ✓ F11 | ✓ FOOD_POSITIVE | ✓ F12 | 11/11 |
| EEVEE-MF-059 Gift/item presentation hold | — | — | ✓ F21 | — | — | — | — | — | ✓ F13 | ✓ GIFT_HOLD | ✓ F14 | 11/11 |
| EEVEE-MF-060 Gift-holding smile | — | — | ✓ F22 | — | — | — | — | — | ✓ F14 | ✓ GIFT_CLOSE_EYE_SMILE | — | 11/11 |
| EEVEE-MF-061 Gift lower/release transition | — | — | — | — | — | — | — | — | ✓ F15 | — | ✓ F15 | 11/11 |
| EEVEE-MF-062 Gift afterglow / result smile | — | — | ✓ F23,F24 | — | — | — | — | — | ✓ F16 | ✓ POST_GIFT_HAPPY | — | 11/11 |
| EEVEE-MF-063 Entry / pop-up / appear-settle | — | ✓ INTRO_POP_UP | ✓ F01 | — | — | ✓ F02 | — | — | — | — | — | 11/11 |
| EEVEE-MF-064 Special backward recoil | — | — | — | ✓ F12 | — | — | — | — | — | — | — | 11/11 |
| EEVEE-MF-065 Special forepaw-lift accent | — | — | — | ✓ F13 | — | — | — | — | — | — | — | 11/11 |
| EEVEE-MF-066 Special forward bow | — | — | — | ✓ F14 | — | — | — | — | — | — | — | 11/11 |
| EEVEE-MF-067 Special startle open-mouth face | — | — | — | ✓ F17 | — | — | — | — | — | — | — | 11/11 |
| EEVEE-MF-068 Special closed-eye smile hold | — | — | — | ✓ F16 | — | — | — | — | — | — | — | 11/11 |
| EEVEE-MF-069 Grooming/appearance-change prep hold | — | — | — | — | — | — | ✓ GROOM_CLOUD | — | — | — | — | 11/11 |
| EEVEE-MF-070 Grooming/appearance-change surprise | — | — | — | — | — | — | ✓ GROOM_SURPRISE,GROOM_SURPRISE_EXTREME | — | — | — | — | 11/11 |
| EEVEE-MF-071 Side-to-front turn | — | — | ✓ F04 | — | — | — | — | — | — | — | — | 11/11 |
| EEVEE-MF-072 Room reposition turn | — | — | — | — | — | — | — | ✓ ROOM_REPOSITION_TURN | — | — | — | 11/11 |
| EEVEE-MF-073 Recovery to neutral | ✓ RECOVERY_TO_NEUTRAL | ✓ RECOVERY_TO_NEUTRAL | — | ✓ F07,F15 | ✓ POSITIVE_RECOVERY_MOUTH_OPEN | ✓ F09 | — | ✓ SPECIAL_RECOVERY,RECOVERY_TO_NEUTRAL | ✓ F12 | ✓ RECOVER_TO_NEUTRAL | ✓ F18 | 11/11 |
| EEVEE-MF-074 Half-lid/downward recovery | — | — | — | — | — | — | ✓ HALF_LID_RECOVERY | — | — | — | — | 11/11 |
| EEVEE-MF-075 Drowsy/rest recovery to neutral | — | — | ✓ F20 | — | — | — | — | — | — | — | — | 11/11 |
| EEVEE-MF-076 Positive touch afterglow | — | — | — | ✓ F10 | — | — | — | — | — | — | — | 11/11 |
| EEVEE-MF-077 Open-eye smile/bob, cause unresolved | — | — | — | — | — | — | ✓ POS_OPEN_SMILE | — | — | — | — | 11/11 |

## 32. Cross-Video Shared Families
- **10/11:** EEVEE-MF-007 Front neutral still hold
- **9/11:** EEVEE-MF-028 Gentle positive touch hold, EEVEE-MF-073 Recovery to neutral
- **8/11:** EEVEE-MF-029 Strong positive touch burst
- **7/11:** EEVEE-MF-001 Neutral bilateral blink, EEVEE-MF-013 Autonomous curious head tilt, EEVEE-MF-058 Food-positive response
- **6/11:** EEVEE-MF-004 Tail idle sway / swish, EEVEE-MF-056 Food contact / receive / mouth hold
- **5/11:** EEVEE-MF-015 Autonomous/contented smile hold, EEVEE-MF-019 Relaxed long eye-close moving hold, EEVEE-MF-036 Touch-linked forepaw lift/offer, EEVEE-MF-057 Post-food processing pause
- **4/11:** EEVEE-MF-002 Context-linked short eye close, EEVEE-MF-016 Autonomous bilateral forepaw lift, EEVEE-MF-033 Touch head-lean / tilt response, EEVEE-MF-059 Gift/item presentation hold
- **3/11:** EEVEE-MF-009 Side/profile still hold, EEVEE-MF-021 Deep doze / drowsy hold, EEVEE-MF-026 Wake/startle transition, EEVEE-MF-032 Touch-linked deep bow → rebound/paw rise, EEVEE-MF-034 Touch open-mouth small/hold response, EEVEE-MF-055 Food notice / presentation wait, EEVEE-MF-060 Gift-holding smile, EEVEE-MF-062 Gift afterglow / result smile, EEVEE-MF-063 Entry / pop-up / appear-settle
- **2/11:** EEVEE-MF-003 Idle body micro-sway, EEVEE-MF-006 Bilateral ear emotion/follow-through, EEVEE-MF-008 Touch latency / tolerate stillness, EEVEE-MF-012 Open-mouth attention hold, EEVEE-MF-014 Autonomous head sway / shake, EEVEE-MF-018 Autonomous/unknown deep bow → bilateral paw rise, EEVEE-MF-020 Doze/drowsy entry, EEVEE-MF-035 Touch surprise/open-mouth → smile, EEVEE-MF-040 Angry/protest facial burst, EEVEE-MF-043 Negative droop / body sink, EEVEE-MF-044 Half-lid/downcast disengagement hold, EEVEE-MF-051 Reciprocal paw offer / WAIT, EEVEE-MF-061 Gift lower/release transition

## 33. Unique-to-Video Families
- **Video 01 only:** EEVEE-MF-005 Independent single-ear flick, EEVEE-MF-011 Hand-oriented attention candidate, EEVEE-MF-022 Ear switching inside doze, EEVEE-MF-039 Small uneasy facial warning
- **Video 02 only:** EEVEE-MF-041 Strong closed-eye/ear-splay negative face, EEVEE-MF-052 High-five contact acknowledgment, EEVEE-MF-053 High-five success smile, EEVEE-MF-054 High-five alternate post-contact response
- **Video 03 only:** EEVEE-MF-010 Close-up forepaw rest/presentation hold, EEVEE-MF-071 Side-to-front turn, EEVEE-MF-075 Drowsy/rest recovery to neutral
- **Video 04 only:** EEVEE-MF-027 Positive-touch onset, EEVEE-MF-064 Special backward recoil, EEVEE-MF-065 Special forepaw-lift accent, EEVEE-MF-066 Special forward bow, EEVEE-MF-067 Special startle open-mouth face, EEVEE-MF-068 Special closed-eye smile hold, EEVEE-MF-076 Positive touch afterglow
- **Video 05 only:** EEVEE-MF-042 Sad/downcast negative face hold, EEVEE-MF-046 Side recoil / rotate away-to-front, EEVEE-MF-047 Strong rejection with paw/feet thrust
- **Video 06 only:** none at Master-Family level
- **Video 07 only:** EEVEE-MF-017 Autonomous single-forepaw raise, EEVEE-MF-037 Small touch-linked eye-close/sink, EEVEE-MF-069 Grooming/appearance-change prep hold, EEVEE-MF-070 Grooming/appearance-change surprise, EEVEE-MF-074 Half-lid/downward recovery, EEVEE-MF-077 Open-eye smile/bob, cause unresolved
- **Video 08 only:** EEVEE-MF-023 Distant sleep stillness, EEVEE-MF-024 Sleep micro-cycle, EEVEE-MF-049 Full-body turn away, EEVEE-MF-050 Turn return with bilateral paw presentation, EEVEE-MF-072 Room reposition turn
- **Video 09 only:** none at Master-Family level
- **Video 10 only:** EEVEE-MF-025 Touch during rest with delayed/no immediate response, EEVEE-MF-030 Two-lobe positive touch sequence, EEVEE-MF-031 Positive touch retrigger
- **Video 11 only:** EEVEE-MF-038 Positive jump hero response, EEVEE-MF-045 Face-touch withdrawal head tilt, EEVEE-MF-048 Impact-like face flinch

## 34. Implementation-Relevant Classification
These are structural descriptors only; they do not prescribe rig/clip/runtime implementation.
| ID | Scale | Spatial scope | Grounding | Temporal form | Primary driver |
|---|---|---|---|---|---|
| EEVEE-MF-001 | MICRO | LOCAL | PLANTED | pulse | face |
| EEVEE-MF-002 | MICRO | LOCAL | PLANTED | pulse | face |
| EEVEE-MF-003 | MICRO | REGIONAL | WEIGHT_SHIFT | loop-like | torso |
| EEVEE-MF-004 | MICRO | LOCAL | PLANTED | loop-like | tail |
| EEVEE-MF-005 | MICRO | LOCAL | PLANTED | pulse | ear |
| EEVEE-MF-006 | MICRO | LOCAL | PLANTED | sequence | ear |
| EEVEE-MF-007 | SMALL | FULL_BODY | PLANTED | hold | full-body |
| EEVEE-MF-008 | SMALL | FULL_BODY | PLANTED | hold | full-body |
| EEVEE-MF-009 | SMALL | FULL_BODY | PLANTED | hold | full-body |
| EEVEE-MF-010 | SMALL | REGIONAL | PLANTED | hold | forepaw |
| EEVEE-MF-011 | MICRO | LOCAL | PLANTED | hold | face |
| EEVEE-MF-012 | SMALL | LOCAL | PLANTED | hold | face |
| EEVEE-MF-013 | MEDIUM | REGIONAL | WEIGHT_SHIFT | anticipation_action_settle | head |
| EEVEE-MF-014 | MEDIUM | REGIONAL | WEIGHT_SHIFT | sequence | head |
| EEVEE-MF-015 | SMALL | REGIONAL | PLANTED | hold | face |
| EEVEE-MF-016 | MEDIUM | REGIONAL | WEIGHT_SHIFT | anticipation_action_settle | forepaw |
| EEVEE-MF-017 | SMALL | LOCAL | WEIGHT_SHIFT | pulse | forepaw |
| EEVEE-MF-018 | LARGE | FULL_BODY | WEIGHT_SHIFT | sequence | full-body |
| EEVEE-MF-019 | SMALL | REGIONAL | WEIGHT_SHIFT | moving_hold | head |
| EEVEE-MF-020 | MEDIUM | REGIONAL | WEIGHT_SHIFT | single_transition | head |
| EEVEE-MF-021 | MEDIUM | FULL_BODY | PLANTED | moving_hold | full-body |
| EEVEE-MF-022 | MICRO | LOCAL | PLANTED | loop-like | ear |
| EEVEE-MF-023 | SMALL | FULL_BODY | PLANTED | hold | full-body |
| EEVEE-MF-024 | MICRO | REGIONAL | PLANTED | loop-like | face |
| EEVEE-MF-025 | SMALL | FULL_BODY | PLANTED | hold | full-body |
| EEVEE-MF-026 | MEDIUM | REGIONAL | WEIGHT_SHIFT | single_transition | head |
| EEVEE-MF-027 | SMALL | LOCAL | PLANTED | single_transition | face |
| EEVEE-MF-028 | SMALL | REGIONAL | PLANTED | hold | face |
| EEVEE-MF-029 | MEDIUM | REGIONAL | WEIGHT_SHIFT | anticipation_action_settle | mixed |
| EEVEE-MF-030 | MEDIUM | REGIONAL | PLANTED | sequence | mixed |
| EEVEE-MF-031 | SMALL | REGIONAL | PLANTED | pulse | face |
| EEVEE-MF-032 | LARGE | FULL_BODY | WEIGHT_SHIFT | sequence | full-body |
| EEVEE-MF-033 | MEDIUM | REGIONAL | WEIGHT_SHIFT | sequence | head |
| EEVEE-MF-034 | SMALL | LOCAL | PLANTED | hold | face |
| EEVEE-MF-035 | MEDIUM | REGIONAL | PLANTED | sequence | face |
| EEVEE-MF-036 | MEDIUM | REGIONAL | WEIGHT_SHIFT | pulse | forepaw |
| EEVEE-MF-037 | SMALL | REGIONAL | WEIGHT_SHIFT | pulse | head |
| EEVEE-MF-038 | LARGE | FULL_BODY | SUPPORT_CHANGE | anticipation_action_settle | full-body |
| EEVEE-MF-039 | SMALL | LOCAL | PLANTED | hold | face |
| EEVEE-MF-040 | SMALL | REGIONAL | PLANTED | sequence | face |
| EEVEE-MF-041 | MEDIUM | REGIONAL | WEIGHT_SHIFT | sequence | face |
| EEVEE-MF-042 | SMALL | LOCAL | PLANTED | hold | face |
| EEVEE-MF-043 | LARGE | FULL_BODY | WEIGHT_SHIFT | sequence | full-body |
| EEVEE-MF-044 | SMALL | LOCAL | PLANTED | hold | face |
| EEVEE-MF-045 | MEDIUM | REGIONAL | WEIGHT_SHIFT | sequence | head |
| EEVEE-MF-046 | LARGE | FULL_BODY | TURN | sequence | full-body |
| EEVEE-MF-047 | LARGE | FULL_BODY | SUPPORT_CHANGE | sequence | full-body |
| EEVEE-MF-048 | SMALL | REGIONAL | WEIGHT_SHIFT | pulse | head |
| EEVEE-MF-049 | LARGE | FULL_BODY | TURN | single_transition | full-body |
| EEVEE-MF-050 | LARGE | FULL_BODY | TURN | sequence | full-body |
| EEVEE-MF-051 | MEDIUM | REGIONAL | WEIGHT_SHIFT | moving_hold | forepaw |
| EEVEE-MF-052 | SMALL | LOCAL | PLANTED | pulse | forepaw |
| EEVEE-MF-053 | SMALL | REGIONAL | PLANTED | pulse | face |
| EEVEE-MF-054 | SMALL | REGIONAL | PLANTED | pulse | face |
| EEVEE-MF-055 | SMALL | LOCAL | PLANTED | hold | face |
| EEVEE-MF-056 | SMALL | REGIONAL | PLANTED | moving_hold | face |
| EEVEE-MF-057 | SMALL | FULL_BODY | PLANTED | hold | full-body |
| EEVEE-MF-058 | MEDIUM | REGIONAL | WEIGHT_SHIFT | anticipation_action_settle | mixed |
| EEVEE-MF-059 | MEDIUM | REGIONAL | PLANTED | hold | forepaw |
| EEVEE-MF-060 | SMALL | REGIONAL | PLANTED | hold | face |
| EEVEE-MF-061 | MEDIUM | REGIONAL | PLANTED | single_transition | forepaw |
| EEVEE-MF-062 | SMALL | REGIONAL | PLANTED | hold | face |
| EEVEE-MF-063 | LARGE | FULL_BODY | SUPPORT_CHANGE | single_transition | full-body |
| EEVEE-MF-064 | LARGE | FULL_BODY | WEIGHT_SHIFT | single_transition | full-body |
| EEVEE-MF-065 | MEDIUM | REGIONAL | WEIGHT_SHIFT | pulse | forepaw |
| EEVEE-MF-066 | LARGE | FULL_BODY | WEIGHT_SHIFT | single_transition | full-body |
| EEVEE-MF-067 | SMALL | LOCAL | PLANTED | pulse | face |
| EEVEE-MF-068 | SMALL | LOCAL | PLANTED | hold | face |
| EEVEE-MF-069 | SMALL | REGIONAL | PLANTED | hold | face |
| EEVEE-MF-070 | MEDIUM | REGIONAL | PLANTED | hold | face |
| EEVEE-MF-071 | LARGE | FULL_BODY | TURN | single_transition | full-body |
| EEVEE-MF-072 | LARGE | FULL_BODY | TURN | single_transition | full-body |
| EEVEE-MF-073 | SMALL | REGIONAL | WEIGHT_SHIFT | single_transition | mixed |
| EEVEE-MF-074 | SMALL | LOCAL | PLANTED | single_transition | face |
| EEVEE-MF-075 | SMALL | REGIONAL | PLANTED | single_transition | head |
| EEVEE-MF-076 | SMALL | REGIONAL | PLANTED | hold | face |
| EEVEE-MF-077 | MEDIUM | REGIONAL | WEIGHT_SHIFT | hold | mixed |

## 35. Quantitative Master Summary
- total Master Motion Families: **77**
- total identified Variants: **156**
- source-local Family records audited: **208**
- front-view HIGH / MEDIUM / LOW: **65 / 7 / 5**
- autonomous-dominant Master Families: **21**
- player-triggered/reciprocal Master Families: **38**
- intentional-stillness / hold primary Families: **5**
- rest/doze/sleep primary Families: **7**
- transition/recovery primary Families: **7**
- total exact-count Occurrences: **not asserted as one scalar** because several sources mix parent phases, child phases, recurrent components, state bouts and lower-bound counts. Exact per-source counts are preserved in §5 instead of double-counting them.
- lower-bound/continuous Occurrences: **preserved source-by-source in §5**; no unsupported exactification performed.

## 36. Conflict / Ambiguity Ledger
| Topic | Source A | Source B | Master treatment | Confidence |
|---|---|---|---|---|
| TOUCH_POSITIVE_STANDARD boundary | V03/F07 broad standard family | V11/F05 standard family has stronger head-down/ear-spread grammar | Master maps the shared label to Strong positive touch; source-specific gentler substructure remains in trace/variants | MEDIUM |
| SHORT_EYELID_CLOSE vs BLINK | V01/V05/V07 include context-linked short closes | V02/V06/V08/V09/V10 isolate neutral blinks | Master separates neutral BLINK from context-linked SHORT_CLOSE; ambiguous source events remain ambiguous | HIGH |
| BOW + forepaws causality | V06/V09/V10 are touch-associated | V07/V11 are autonomous/unknown candidates | Kept as two Master Families: touch-linked CONTACT_BOW vs autonomous/unknown BOW_BIPAW_AUTO | HIGH |
| Gift initiation cause | V03 describes autonomous/social presentation | V10/V11 preserve UI/scene-trigger uncertainty | Master initiation metadata uses character-initiated candidate where supported; exact game trigger remains unresolved | MEDIUM |
| Tail independence | Some sources isolate tail-only sway | V06 calls tail/torso sway V2 and not independent | Master retains tail micro family but flags coupled variant and does not infer constant wag | HIGH |
| Grooming cloud | V07 local family GROOM_CLOUD includes effect context | Same source explicitly says bubble/cloud/star is not body motion | Master preserves only body prep/hold under GROOM_PREP; VFX itself is excluded | HIGH |
| Touch-paw social meaning | V01/V10/V11 show paw lifts/reaches | Only V02 establishes reciprocal high-five contact chain | Generic touch paw is separate from Reciprocal paw offer/contact families | HIGH |
| Sleep/doze boundaries | V01/V03/V10 describe doze/drowsy holds | V08 records distant sleep plus a 2.7–2.8 s sleep micro-cycle | Master preserves relaxed hold, doze hold, distant sleep, sleep micro-cycle separately | HIGH |

## 37. Unresolved / Unconfirmed
- Anatomical L/R remains unassigned wherever source inventories intentionally use screen-left/screen-right.
- Whether every short context-linked eye close is a physiological blink remains unresolved; neutral blink and context close are separated.
- Exact internal game triggers for several startup, gift, special and autonomous-candidate performances remain unresolved.
- V06 tail/torso secondary sway independence remains unconfirmed.
- Hand-oriented eye-only gaze in V01 remains V2/candidate.
- Distant V08 footwork during room reposition is not resolved.
- Some V07 positive/open-smile causes remain unknown because visible input is absent or ambiguous.
- No corpus-wide tail wag rule, eye-only gaze system, or independent left/right ear rule is inferred beyond directly observed source cases.

## 38. Final Compact Master Inventory
| ID | Family | Category | Coverage | Variants | Front |
|---|---|---|---:|---:|---|
| EEVEE-MF-001 | Neutral bilateral blink | A | 7/11 | 1 | HIGH |
| EEVEE-MF-002 | Context-linked short eye close | A | 4/11 | 1 | HIGH |
| EEVEE-MF-003 | Idle body micro-sway | A | 2/11 | 2 | MEDIUM |
| EEVEE-MF-004 | Tail idle sway / swish | C | 6/11 | 2 | LOW |
| EEVEE-MF-005 | Independent single-ear flick | C | 1/11 | 1 | HIGH |
| EEVEE-MF-006 | Bilateral ear emotion/follow-through | C | 2/11 | 2 | HIGH |
| EEVEE-MF-007 | Front neutral still hold | O | 10/11 | 1 | HIGH |
| EEVEE-MF-008 | Touch latency / tolerate stillness | O | 2/11 | 2 | HIGH |
| EEVEE-MF-009 | Side/profile still hold | O | 3/11 | 3 | LOW |
| EEVEE-MF-010 | Close-up forepaw rest/presentation hold | O | 1/11 | 1 | HIGH |
| EEVEE-MF-011 | Hand-oriented attention candidate | B | 1/11 | 1 | MEDIUM |
| EEVEE-MF-012 | Open-mouth attention hold | B | 2/11 | 2 | HIGH |
| EEVEE-MF-013 | Autonomous curious head tilt | F | 7/11 | 6 | HIGH |
| EEVEE-MF-014 | Autonomous head sway / shake | F | 2/11 | 2 | HIGH |
| EEVEE-MF-015 | Autonomous/contented smile hold | F | 5/11 | 7 | HIGH |
| EEVEE-MF-016 | Autonomous bilateral forepaw lift | G | 4/11 | 2 | HIGH |
| EEVEE-MF-017 | Autonomous single-forepaw raise | G | 1/11 | 1 | HIGH |
| EEVEE-MF-018 | Autonomous/unknown deep bow → bilateral paw rise | G | 2/11 | 2 | HIGH |
| EEVEE-MF-019 | Relaxed long eye-close moving hold | Q | 5/11 | 5 | HIGH |
| EEVEE-MF-020 | Doze/drowsy entry | Q | 2/11 | 2 | HIGH |
| EEVEE-MF-021 | Deep doze / drowsy hold | Q | 3/11 | 3 | HIGH |
| EEVEE-MF-022 | Ear switching inside doze | Q | 1/11 | 1 | HIGH |
| EEVEE-MF-023 | Distant sleep stillness | Q | 1/11 | 1 | LOW |
| EEVEE-MF-024 | Sleep micro-cycle | Q | 1/11 | 1 | MEDIUM |
| EEVEE-MF-025 | Touch during rest with delayed/no immediate response | O | 1/11 | 1 | HIGH |
| EEVEE-MF-026 | Wake/startle transition | Q | 3/11 | 3 | HIGH |
| EEVEE-MF-027 | Positive-touch onset | H | 1/11 | 2 | HIGH |
| EEVEE-MF-028 | Gentle positive touch hold | H | 9/11 | 8 | HIGH |
| EEVEE-MF-029 | Strong positive touch burst | H | 8/11 | 9 | HIGH |
| EEVEE-MF-030 | Two-lobe positive touch sequence | H | 1/11 | 1 | HIGH |
| EEVEE-MF-031 | Positive touch retrigger | H | 1/11 | 1 | HIGH |
| EEVEE-MF-032 | Touch-linked deep bow → rebound/paw rise | H | 3/11 | 3 | HIGH |
| EEVEE-MF-033 | Touch head-lean / tilt response | H | 4/11 | 4 | HIGH |
| EEVEE-MF-034 | Touch open-mouth small/hold response | H | 3/11 | 3 | HIGH |
| EEVEE-MF-035 | Touch surprise/open-mouth → smile | H | 2/11 | 2 | HIGH |
| EEVEE-MF-036 | Touch-linked forepaw lift/offer | E | 5/11 | 5 | HIGH |
| EEVEE-MF-037 | Small touch-linked eye-close/sink | H | 1/11 | 1 | HIGH |
| EEVEE-MF-038 | Positive jump hero response | M | 1/11 | 1 | HIGH |
| EEVEE-MF-039 | Small uneasy facial warning | I | 1/11 | 1 | HIGH |
| EEVEE-MF-040 | Angry/protest facial burst | I | 2/11 | 2 | HIGH |
| EEVEE-MF-041 | Strong closed-eye/ear-splay negative face | I | 1/11 | 1 | HIGH |
| EEVEE-MF-042 | Sad/downcast negative face hold | I | 1/11 | 1 | HIGH |
| EEVEE-MF-043 | Negative droop / body sink | I | 2/11 | 2 | HIGH |
| EEVEE-MF-044 | Half-lid/downcast disengagement hold | I | 2/11 | 2 | HIGH |
| EEVEE-MF-045 | Face-touch withdrawal head tilt | I | 1/11 | 1 | HIGH |
| EEVEE-MF-046 | Side recoil / rotate away-to-front | I | 1/11 | 1 | MEDIUM |
| EEVEE-MF-047 | Strong rejection with paw/feet thrust | I | 1/11 | 1 | HIGH |
| EEVEE-MF-048 | Impact-like face flinch | I | 1/11 | 1 | HIGH |
| EEVEE-MF-049 | Full-body turn away | I | 1/11 | 1 | LOW |
| EEVEE-MF-050 | Turn return with bilateral paw presentation | M | 1/11 | 1 | HIGH |
| EEVEE-MF-051 | Reciprocal paw offer / WAIT | J | 2/11 | 2 | HIGH |
| EEVEE-MF-052 | High-five contact acknowledgment | J | 1/11 | 1 | HIGH |
| EEVEE-MF-053 | High-five success smile | J | 1/11 | 1 | HIGH |
| EEVEE-MF-054 | High-five alternate post-contact response | J | 1/11 | 1 | HIGH |
| EEVEE-MF-055 | Food notice / presentation wait | K | 3/11 | 3 | HIGH |
| EEVEE-MF-056 | Food contact / receive / mouth hold | K | 6/11 | 7 | HIGH |
| EEVEE-MF-057 | Post-food processing pause | K | 5/11 | 1 | HIGH |
| EEVEE-MF-058 | Food-positive response | K | 7/11 | 2 | HIGH |
| EEVEE-MF-059 | Gift/item presentation hold | L | 4/11 | 1 | HIGH |
| EEVEE-MF-060 | Gift-holding smile | L | 3/11 | 1 | HIGH |
| EEVEE-MF-061 | Gift lower/release transition | L | 2/11 | 2 | HIGH |
| EEVEE-MF-062 | Gift afterglow / result smile | L | 3/11 | 2 | HIGH |
| EEVEE-MF-063 | Entry / pop-up / appear-settle | P | 3/11 | 3 | HIGH |
| EEVEE-MF-064 | Special backward recoil | M | 1/11 | 1 | MEDIUM |
| EEVEE-MF-065 | Special forepaw-lift accent | M | 1/11 | 1 | HIGH |
| EEVEE-MF-066 | Special forward bow | M | 1/11 | 1 | HIGH |
| EEVEE-MF-067 | Special startle open-mouth face | M | 1/11 | 1 | HIGH |
| EEVEE-MF-068 | Special closed-eye smile hold | M | 1/11 | 1 | HIGH |
| EEVEE-MF-069 | Grooming/appearance-change prep hold | R | 1/11 | 1 | MEDIUM |
| EEVEE-MF-070 | Grooming/appearance-change surprise | R | 1/11 | 2 | HIGH |
| EEVEE-MF-071 | Side-to-front turn | P | 1/11 | 1 | MEDIUM |
| EEVEE-MF-072 | Room reposition turn | P | 1/11 | 1 | LOW |
| EEVEE-MF-073 | Recovery to neutral | N | 9/11 | 4 | HIGH |
| EEVEE-MF-074 | Half-lid/downward recovery | N | 1/11 | 1 | HIGH |
| EEVEE-MF-075 | Drowsy/rest recovery to neutral | N | 1/11 | 1 | HIGH |
| EEVEE-MF-076 | Positive touch afterglow | N | 1/11 | 1 | HIGH |
| EEVEE-MF-077 | Open-eye smile/bob, cause unresolved | R | 1/11 | 1 | HIGH |

## 39. Coverage / Traceability Audit
- [x] Video 01: all source Families recovered — 25/25
- [x] Video 02: all source Families recovered — 17/17
- [x] Video 03: all source Families recovered — 25/25
- [x] Video 04: all source Families recovered — 17/17
- [x] Video 05: all source Families recovered — 19/19
- [x] Video 06: all source Families recovered — 10/10
- [x] Video 07: all source Families recovered — 18/18
- [x] Video 08: all source Families recovered — 19/19
- [x] Video 09: all source Families recovered — 16/16
- [x] Video 10: all source Families recovered — 24/24
- [x] Video 11: all source Families recovered — 18/18
- [x] No source-local Family is orphaned.
- [x] Duplicate exports are not counted as separate videos.
- [x] Parent/child phase counts are not blindly summed into a false exact global occurrence total.
- [x] VFX/audio/UI/cursor are excluded as body Motion.
- [x] Hairstyle/effect difference alone does not create a new body-motion Family.
- [x] Source uncertainty is not promoted to certainty.
- [x] LOW front-view Families are retained.
- [x] Single-video Families are retained.

**Master Coverage Confidence: HIGH**

Reason: all 208 source-local Family records from the 11 unique inventories are mapped to a Master Family and Variant, with source IDs/timestamps/count strings retained where available. Confidence applies to *coverage/traceability*, not to unresolved semantics or source-level V2/I interpretations.

---

**Non-goal:** This Master does not decide which motions Carol/Grimo should adopt, motion counts for Carol, rig design, Blender clips, PlayCanvas implementation, or comparison superiority versus Pikachu.
