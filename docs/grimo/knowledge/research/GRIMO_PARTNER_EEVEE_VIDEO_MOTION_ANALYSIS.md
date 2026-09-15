# Grimo — Partner Eevee Video Motion & Interaction Analysis

## 0. Document Purpose

This document consolidates the Partner Eevee MP4 analyses actually performed in this chat into a durable Grimo production reference. It is intended to be added directly to Project Knowledge so that the original long-form chat does not need to be reread for day-to-day motion, interaction, behavior, runtime, and production decisions.

The corpus is **Partner Eevee only**. No Partner Pikachu MP4 was analyzed in this chat. Therefore this document does **not** infer Pikachu timing, motion anatomy, or behavior from Eevee. Any Pikachu-specific point is marked **未確認 / この映像群からは判断不能**.

### Evidence classification

- **[V1] Direct Video Observation** — directly visible in the decoded MP4 frames or directly measured metadata.
- **[V2] Temporal Inference** — strong inference from adjacent frames, frame timing, or closely aligned audio transients.
- **[I] Inference** — interpretation of the observed behavior without claiming knowledge of the internal game implementation.
- **[G] Grimo Recommendation** — design/production/runtime recommendation derived from the observed behavior.

### Source-of-truth order

1. The five MP4 files actually analyzed in this chat.
2. Frame/timestamp observations extracted from those MP4s.
3. The motion/interaction analyses already produced from those frames.
4. Explicit inference from those observations.
5. Grimo-specific recommendations.

No unseen Pokémon behavior, undocumented internal implementation, or general franchise knowledge is used to fill gaps. When the footage does not support a conclusion, this document says so.

### Measurement limits

All five analyzed videos are 30 fps. Therefore the smallest defensible frame-level temporal step is approximately **33.3 ms per frame**. Sub-frame precision is not claimed. Audio was inspected in several important segments, but vocal / contact SE / UI SE / BGM were not source-separated; audio semantics are therefore conservative.

---

## 1. Executive Findings

### 1.1 Life comes from selective, asynchronous channel activity, not constant full-body motion

Across all five videos, Eevee frequently leaves the root, feet, tail, or torso almost still while only eyelids, one ear, head orientation, mouth, or one forelimb changes. Large actions do not automatically recruit every body channel. **[V1]**

Examples:

- Video E01, the autonomous paw action around 98.6–99.7 s uses eyes, mouth, and forepaws while ears/tail remain comparatively quiet. **[V1]**
- Video E02, repeated high-fives use one forepaw + face while the COM, hindlegs, opposite foreleg, and tail mostly hold. **[V1]**
- Video E04, the “ノリノリ” phrase begins with one ear, then face, then the other ear, and only at the stronger second accent do the forepaws join. **[V1]**

**[G]** Grimo must support per-action channel masks, not “play a full-body clip for every emotion.”

### 1.2 Intentional stillness is part of the living state

Eevee can remain in a stable or moving-hold state for many seconds without appearing like a dead render. The clearest case is E01 around 128.3–150+ s: eyes closed, head lowered, ears asymmetric, tiny drift, but no major action for roughly twenty-plus seconds. **[V1]**

Other videos repeat the same principle with shorter quiet windows: E02 105–128 s, E03 97–105 s, E04 140–145 s / 147–152.8 s, and E05 100–105 s. **[V1]**

**[G]** “Do nothing” / intentional stillness must be an explicit valid behavior, not a scheduler failure.

### 1.3 Facial meaning often precedes larger body meaning

Eevee frequently communicates emotional evaluation with eyelids/eyes/mouth before the ears, torso, or limbs reach peak motion. **[V1]**

- E01 negative reaction: narrowed/negative face is readable around 55.80–55.87 s; the large ear spread follows roughly a second later around 56.97 s. **[V1/V2]**
- E03 sharp protest: facial irritation begins around 9.667 s; open-mouth protest comes later around 10.333 s. **[V1]**
- E01 positive pet: pleasure is readable in the face around 11.367 s; the larger ear/VFX peak arrives around 13.10 s. **[V1]**

**[G]** Emotion should be authored as a temporal curve, not a single expression preset snapped on with the body action.

### 1.4 Different interaction families have different latency grammars

The footage does not support one universal “touch latency.” **[V1]**

- Slow pet/stroke can accumulate for hundreds of milliseconds or seconds before the major semantic response. E01 first head pet: hand/contact episode visible from 09.833 s; clear pleasure face at 11.367 s. **[V1/V2]**
- Reciprocal discrete high-five must acknowledge success almost immediately. E02 first contact flash at 34.400 s; clear happy face at about 34.467 s, approximately two frames / 67 ms later. **[V1]**
- Feeding repeatedly shows a consumption event followed by a roughly 0.8–0.9 s processing pause before the larger delight reaction. **[V1/V2]**

**[G]** Runtime latency policy must be interaction-class-specific: local reflex, reciprocal social contact, accumulated stroke, feeding, and large reactions should not share one timing rule.

### 1.5 Character → User initiation is a major source of agency

E02 shows Eevee raising a forepaw, presenting the pad toward the player, and **waiting** for player contact before the success response. **[V1]** The important structure is not the paw pose itself, but:

```text
Character initiates
→ presents body part
→ holds
→ waits for player
→ player reciprocates
→ immediate acknowledgement
→ shared emotional payoff
```

**[G]** Grimo needs explicit reciprocal interaction states, not only Player → Character reactions.

### 1.6 “Dislike” is not one angry animation; at least two distinct negative strategies are visible

E03 reveals two visually distinct negative reaction families. **[V1]**

- **Sharp protest / warning:** face first, front-facing attention largely preserved, mouth later opens in protest, body/COM restrained.
- **Withdrawal / disengagement:** ears spread/lower, head and visible body mass lower, gaze drops away, followed by a sad moving hold.

**[G]** Grimo boundary behavior should distinguish mild warning, clear refusal, withdrawal/disengagement, and recovery instead of using one generic ANGRY clip.

### 1.7 Touch can become bidirectional: Eevee sometimes moves its own body into the interaction

E05 cheek-rub reactions around 20.1–22.6 s and 65.9–68.4 s show Eevee entering a larger body phrase: ears open, eyes close, head/body lower into the contact, then rebound with forepaws and a second eyes-closed content hold. **[V1]**

The important abstract principle is:

```text
Player contacts character
→ character accepts/accumulates interaction
→ character actively changes its own body relative to the contact
```

**[G]** Carol should not merely “play happy after cheek pet”; she should be able to actively lean the contacted cheek toward the user.

### 1.8 High-energy mood is expressed as a bounded phrase, not a perpetual oscillator

E04 “ノリノリ” begins with a roughly three-second authored rhythmic phrase, then returns to ordinary living behavior. **[V1]** The phrase has non-uniform internal structure: asymmetric ear lead → face → opposite ear → partial reset → stronger second accent → forepaws → settle.

**[G]** Mood should alter phrase probability, tempo, and amplitude; it should not force every channel into continuous rhythmic motion.

### 1.9 Emotional intensity recruits more channels progressively

Small successes are often visually restrained; larger emotional peaks recruit more channels. **[V1]**

- E02 ordinary high-five success: forepaw + face dominate; ears and tail remain restrained.
- E02 delayed major affection reaction around 43.37 s: face, ears, broad VFX, and a wider overall expression are recruited.
- E04 first rhythmic subphrase uses ears + face; stronger second accent additionally recruits both forepaws.

**[G]** Reserve channels. Do not spend face + ears + tail + body + VFX on every event.

### 1.10 Pokémon footage also exposes reusable weaknesses: visible clip repetition and weak left/right locality

Repeated negative reactions, feeding delight, head-tilt families, and cheek-rub macro reactions become visually recognizable across long sessions and even across separate videos. **[V1/V2]** E05 is particularly clear: opposite-side cheek contacts can converge on a centered, bilateral macro response. **[V1]**

**[G]** Grimo should preserve deterministic causality while increasing performance variation, side-conditioning, continuous local contact, and reaction-family repetition suppression.

---

## 2. Video Corpus

| ID | Filename | Duration | FPS | Resolution | Main Behavior | Analysis Coverage |
|---|---|---:|---:|---|---|---|
| **E01** | `01_【ピカブイ】イーブイとのふれあい【ポケモン Let's Go! イーブイ】_1080p30(1).mp4` | **208.733 s** | 30 | 1920×1080 | general Partner Play: petting, negative response, feeding, autonomous idle | full survey; dense 9–25, 34–48, 52–64, 72–86, 92–112, 128–156, 156–174, 178–208 s; several 30 fps windows |
| **E02** | `02_【ピカブイ】イーブイとのハイタッチがかわいい！【ポケモン Let's Go! イーブイ】_1080p30.mp4` | **128.1667 s** | 30 | 1920×1080 | repeated reciprocal high-five, touch, feeding, idle | full survey; 30–48 s high-five survey; **32–44 s at 30 fps**; touch 8–30 / 44–90; feeding 90–106; idle 105–128 |
| **E03** | `05_【ピカブイ】イーブイの嫌がるところを触り続けると...【ポケモン Let's Go! イーブイ】_1080p30.mp4` | **125.333 s** | 30 | 1920×1080 | disliked touch, repeated protest/withdrawal, positive recovery, idle | full 1 s survey; 8–46 / 52–64 / 64–90 / 90–125 dense; 9.2–12, 14–16, 20.4–23, 39.4–42, 32.8–35, 66.4–69 at 30 fps |
| **E04** | `11_【ピカブイ】ノリノリなイーブイ【ポケモンレッツゴー イーブイ】_1080p30.mp4` | **160.400 s** | 30 | 1920×1080 | mood/self-expression phrase, touch, gift, autonomous sway, relaxed hold | full 1–2 s survey; **0.4–3.6 s at 30 fps**; 12.5–15.1, 43.3–46, 145–147.5, 152.8–157 at 30 fps; gift 130.5–141 |
| **E05** | `06_【ピカブイ】イーブイのほっぺすりすり【ポケモンレッツゴー イーブイ】_1080p30.mp4` | **120.400 s** | 30 | 1920×1080 | cheek rubbing / contact-seeking macro response, positive touch, idle | full 1 s survey; 8–24, 30–37, 48–56, 74–82 dense; **19–23 and 64.5–69 s at 30 fps**; idle 100–120 |

**Analyzed Partner Pikachu videos in this chat: 0.**

---

## 3. Timestamp / Scene Index

### 3.1 E01 — General Partner Play

| Timestamp | Interaction / Behavior | Why Important |
|---:|---|---|
| 09.833 s | first visible hand/contact episode | start of measured head-pet sequence **[V1]** |
| 11.367 s | eyes close + pleasure mouth | first clear semantic pleasure response **[V1]** |
| ≈13.10 s | second stronger positive peak begins | ear/VFX amplification occurs well after initial face response **[V1]** |
| 13.13–13.7 s | ears broad/lateral + smile peak | delayed appendage recruitment **[V1]** |
| ≈38.8–39.4 s | prolonged side/collar touch, uneasy face | touch can sustain low-valence state **[V1]** |
| 55.80–55.87 s | negative facial evaluation starts | face precedes large appendage response **[V1]** |
| 55.93–56.0 s | star/dizzy-like effect | semantic protest cue **[V1]** |
| ≈56.5 s | mouth opens | explicit protest follows facial evaluation **[V1]** |
| ≈56.97 s | ears spread strongly | ears arrive much later than facial onset **[V1]** |
| ≈58.4–59.8 s | visually similar negative response repeats | visible reaction-family repetition **[V1]** |
| ≈60.7–62.6 s | front/chest touch shifts positive, then peak | same session can transition negative→positive **[V1]** |
| ≈77.63 s | first berry disappears | feeding consumption event **[V1]** |
| ≈78.47–78.53 s | first feeding delight starts | ≈0.8–0.9 s post-consumption delay **[V1/V2]** |
| ≈84.6 s | second berry disappears | repeat feeding event **[V1]** |
| ≈85.4 s | second feeding delight | timing/structure very similar to first **[V1/V2]** |
| 98.633 s | blink before autonomous paw action | face leads self-initiated action **[V1]** |
| ≈98.80–99.4 s | paws lift / mouth opens / gesture peak | autonomous action with selective channel use **[V1]** |
| ≈106–107.4 s | autonomous head tilt | sparse self-initiated idle action **[V1]** |
| 128.333 s | eyelids soften/close; long relaxed state begins | beginning of >20 s moving hold **[V1]** |
| ≈128.63–128.87 s | one ear lowers; asymmetric relaxed pose established | eyelid/head/ear phase delay **[V1]** |
| 128.9–150+ s | long eyes-closed/head-down moving hold | strongest evidence for intentional stillness **[V1]** |
| ≈151.67 s | touch-driven re-engagement | long state can be interrupted into interaction **[V1]** |
| ≈157.3 / ≈161.3 s | positive front/head responses | later positive interactions **[V1]** |
| ≈184.6–186 s | autonomous tilt sequence | repeated idle family **[V1]** |
| ≈192.6 s | relaxed eyes-closed/ear-drop action | another relaxed family example **[V1]** |
| 200.567–200.700 s | isolated neutral blink | measured ~4-frame visible blink **[V1]** |
| ≈202.4–204 s | head-tilt idle returns | repetition / autonomous idle family **[V1]** |

### 3.2 E02 — High-Five / Reciprocal Interaction

| Timestamp | Interaction / Behavior | Why Important |
|---:|---|---|
| ≈33.27–33.33 s | first paw starts rising | Eevee initiates interaction **[V1]** |
| ≈33.40 s | pad presented to player | body part becomes explicit invitation target **[V1]** |
| ≈33.70 s | interaction cue around paw | contact opportunity **[V1]** |
| 34.400 s | high-five #1 contact flash | clear success contact point **[V1]** |
| ≈34.467 s | eyes closed + happy face | ~2 frames / 67 ms after contact **[V1]** |
| ≈35.20 s | next paw invitation | reciprocal loop restarts **[V1]** |
| ≈37.00 s | high-five #2 contact | invitation can wait ≈1.7 s for user **[V1/V2]** |
| ≈37.067 s | success face #2 | repeated low-latency acknowledgement **[V1]** |
| ≈37.77 s | next invitation | repeated social turn-taking **[V1]** |
| ≈39.23 s | high-five #3 contact | third loop **[V1]** |
| ≈39.30 s | success face #3 | same family, similar timing **[V1]** |
| ≈40.50 s | high-five #4 contact | variation case **[V1]** |
| ≈40.60 s | open-mouth response variation | success performance not fully identical **[V1]** |
| ≈42.50 s | high-five #5 contact | final small success before delayed event **[V1]** |
| ≈43.25 s | separate strong audio event | delayed larger response begins to emerge **[V2]** |
| ≈43.367 s | pink/heart-like major affect onset | delayed special payoff **[V1]** |
| ≈43.433–43.533 s | eyes close → broad smile | staged major emotional peak **[V1]** |
| ≈44.3 s | recovery | larger event settles **[V1]** |
| ≈97.8 s | food consumed | feeding timing comparison **[V1]** |
| ≈98.6 s | major feeding positive response | again ~0.8 s delayed payoff **[V1/V2]** |
| 105.8–114 s | very quiet neutral idle | strong quiet-state example **[V1]** |
| ≈114.4–116.2 s | autonomous head/ear/eye action | sparse idle phrase **[V1]** |
| 117–128 s | quiet neutral with sparse eye events | intentional stillness **[V1]** |

### 3.3 E03 — Disliked Touch / Boundary Behavior

| Timestamp | Interaction / Behavior | Why Important |
|---:|---|---|
| ≈8.0 s | sustained forehead/head touch begins | negative-context input begins **[V1]** |
| ≈9.667 s | first irritation in eyelids/brow-like contour | earliest clear protest acknowledgement **[V1]** |
| ≈9.77–9.83 s | star/dizzy-like cue | negative semantic cue **[V1]** |
| ≈10.333 s | mouth opens | protest escalates after face **[V1]** |
| ≈10.93 s | eyes close | recovery punctuation **[V1]** |
| ≈11.10–11.13 s | neutral restored | sharp protest family ends **[V1]** |
| ≈14.33 s | second sharp protest begins | repeated family **[V1]** |
| ≈14.97 s | open-mouth protest | similar timing to first **[V1]** |
| ≈15.57–15.73 s | eyes close then neutral | repeated staged recovery **[V1]** |
| ≈18–20.5 s | sustained sad/uneasy face | low-valence state persists between clips **[V1]** |
| ≈20.80 s | ears start withdrawal motion | withdrawal family starts with appendage/body strategy **[V1]** |
| ≈20.90–21.03 s | head/body lower | disengagement/withdrawal commitment **[V1]** |
| 21.1–22.0 s | lowered moving hold | negative state is held, not immediately reset **[V1]** |
| ≈22.17–22.33 s | eyes close; pose returns | staged recovery **[V1]** |
| ≈23.8–25.8 s | another sad hold | persistent low valence **[V1]** |
| ≈26–27.4 s | second withdrawal sequence | repeated withdrawal family **[V1]** |
| ≈28.2–33.0 s | long low-valence face hold | emotional continuity **[V1]** |
| ≈33.17 s | positive eyes-closed smile begins | negative→positive switch possible in same broad head region **[V1]** |
| ≈39.70–41.23 s | another withdrawal family | closely matches ~20–22 s sequence **[V1/V2]** |
| 52–61 s | side/back-facing touch | non-front contact context **[V1]** |
| ≈62.20–62.73 s | rapid whole-body reorientation to front | local/side interaction can produce pose-level spatial decision **[V1]** |
| 64–65.6 s | low-valence front state | negative context persists **[V1]** |
| ≈65.8 s | positive face begins | reaction sign can change quickly **[V1]** |
| ≈67.6 s | large positive response/VFX | strong positive peak **[V1]** |
| ≈71.8–73.6 s | another withdrawal / recovery | repeat family **[V1]** |
| 90–94.6 s | long quiet idle | no-input state **[V1]** |
| ≈94.8–96.6 s | autonomous head/ear action | sparse self-initiated behavior **[V1]** |
| 97–105.4 s | very quiet hold | long stillness **[V1]** |
| ≈105.6–107.2 s | autonomous head-tilt/eyes-close | repeated idle family **[V1]** |
| ≈110.8–112.8 s | another autonomous tilt/eye sequence | variation/repetition evidence **[V1]** |
| ≈119.4–120.8 s | spontaneous closed-eye happy-looking idle | positive self-expression without touch **[V1]** |

### 3.4 E04 — “ノリノリ” / Mood Phrase / Gift

| Timestamp | Interaction / Behavior | Why Important |
|---:|---|---|
| ≈0.60 s | first ear begins lateral move | first lead of rhythmic mood phrase **[V1]** |
| ≈0.87 s | mouth changes slightly | face starts joining after ear **[V1]** |
| ≈1.267–1.300 s | eyelids close | first joy phase **[V1]** |
| ≈1.33 s | smile | emotional peak #1 **[V1]** |
| ≈1.53 s+ | opposite ear increasingly involved | progressive bilateral recruitment **[V1]** |
| ≈2.13–2.17 s | eyes reopen | partial reset between accents **[V1]** |
| ≈2.70–2.80 s | second eyelid closure / accent | second phrase starts **[V1]** |
| ≈2.90 s | broader smile | stronger emotional amplitude **[V1]** |
| ≈2.93–3.10 s | both forepaws lift / pad accent | late forelimb recruitment makes second accent stronger **[V1]** |
| ≈3.47–3.50 s | eyes reopen / near-neutral | bounded phrase ends **[V1]** |
| 4–6 s | UI describes Eevee as “ノリノリ” | context label for observed mood phrase **[V1]** |
| ≈12.567–12.667 s | positive facial onset / eyes close | pet reaction comparison **[V1]** |
| ≈14.03–14.8 s | second larger positive peak with ear/VFX recruitment | two-stage positive structure **[V1]** |
| ≈44.30–45.67 s | sharp protest family | very close to E03 negative family **[V1/V2]** |
| ≈131.1–134.1 s | gift presentation + eyes-closed happy hold | self-initiated/social rare family **[V1]** |
| ≈145.27–147.2 s | autonomous asymmetric sway | distinct small idle phrase **[V1]** |
| ≈152.90 s | relaxed state begins with eyelids | start of measured relaxed hold **[V1]** |
| ≈153.07–153.13 s | ears follow and lower | eyelid → ear delay ~4–6 frames **[V1/V2]** |
| 153.2–156.7 s | relaxed moving hold | low-motion state **[V1]** |
| ≈156.83–156.87 s | eyes reopen / neutral | settle complete **[V1]** |

### 3.5 E05 — Cheek Rub / Contact-Seeking Response

| Timestamp | Interaction / Behavior | Why Important |
|---:|---|---|
| 8–19 s | repeated face/cheek contact | buildup to macro response **[V1]** |
| ≈20.12 s | ears swing strongly outward | earliest clear macro-reaction cue **[V1]** |
| ≈20.15 s | eyelids narrow; head starts downward | ear slightly leads head/eyes **[V1/V2]** |
| ≈20.18 s | eyes closed; body commits downward | deep contact phase begins **[V1]** |
| 20.5–20.88 s | deep lowered moving hold | character remains in contact-oriented body state **[V1]** |
| ≈20.92 s | rebound begins | compression releases **[V1]** |
| ≈20.98–21.22 s | mouth opens + both forepaws rise | rebound peak **[V1]** |
| ≈21.28 s | eyes close again | second content phase begins **[V1]** |
| 21.3–22.4 s | prolonged content hold | emotional after-phase **[V1]** |
| ≈22.5–22.6 s | eyes reopen / neutral | recovery **[V1]** |
| ≈33 s | similar deep response family | repeated positive macro family **[V1]** |
| ≈50–51 s | larger music-note response | separate positive family **[V1]** |
| ≈65.9 s | second highly similar cheek/contact macro response starts | repetition evidence **[V1]** |
| ≈66.0–66.6 s | deep lowered eyes-closed hold | same structure as ~20 s **[V1]** |
| ≈66.7–67.0 s | rebound + paws up | repeated peak **[V1]** |
| ≈67.1–68.2 s | second eyes-closed content hold | repeated after-phase **[V1]** |
| ≈68.3–68.4 s | recovery | reaction family ends **[V1]** |
| 100–105 s | very quiet neutral idle | low activity baseline **[V1]** |
| ≈106–109 s | autonomous relaxed eyes-closed / ear-head state | idle family **[V1]** |
| ≈113–115 s | another relaxed autonomous state | repeated living-state family **[V1]** |

---

## 4. Base Living State

### 4.1 Posture / Center of Mass

Eevee’s baseline COM is visually stable and grounded. Root translation is often minimal even while the face, ears, or one limb acts. **[V1]**

- High-five: one forepaw can present toward the player while hindlegs/root remain stable.
- “ノリノリ”: ear/face rhythm occurs largely on a grounded base; the character does not become a bouncing rubber object.
- Negative protest: face/mouth can carry the protest without a large root recoil.
- Withdrawal and cheek-rub macro responses are exceptions where the head and visible body mass deliberately shift downward/forward.

**[G]** Grimo characters need a clear distinction between a stable support pose and deliberate COM commitment.

### 4.2 Breathing

A dedicated breathing cycle was **not measured reliably** from this corpus. Small torso changes exist, but the analysis did not isolate a repeatable breath period from the other body motion. **未確認**.

**[G]** Do not infer Pokémon breathing amplitude or cycle from these videos. Grimo breathing should be tuned independently and kept subtle.

### 4.3 Weight Shift

Weight shifts are sparse rather than continuously oscillating. **[V1]** Clearer weight/body commitment appears in:

- E03 withdrawal: body visually lowers with head/gaze disengagement.
- E03 62 s reorientation: the whole character commits spatially toward front.
- E05 cheek/contact response: upper body/head move down into the interaction, then rebound.

### 4.4 Head Micro-motion

The head acts in several distinct ways:

- sparse idle tilt (E01 ≈106–107.4; ≈184.6–186; ≈202.4–204), **[V1]**
- autonomous sway (E04 ≈145.27–147.2), **[V1]**
- long relaxed head-down hold (E01 ≈128.3–150+), **[V1]**
- touch-driven lean/drop (E05 ≈20.15–20.88), **[V1]**
- withdrawal/downward disengagement (E03 ≈20.9–22.3, ≈39.8–41.2), **[V1]**
- restrained head participation during reciprocal high-five (E02). **[V1]**

The head is therefore not “always the lead”; its causal role depends on behavior.

### 4.5 Blink / Eyelids

The strongest measured neutral blink example is E01:

```text
200.567 s  open
200.600 s  closed
200.633 s  closed
200.667 s  partial-open
200.700 s  open
```

Visible blink duration in this one example is approximately **4 frames ≈133 ms**, with full closure for roughly **2 frames ≈67 ms**. **[V1, n=1]**

Eyelids are also used as emotional/behavioral channels rather than merely physiological blinks:

- high-five success: fast close immediately after contact,
- positive pet: close after pleasure evaluation,
- withdrawal recovery: brief closure before returning neutral,
- mood phrase: close during internal enjoyment, reopen for reset, close again for stronger accent,
- long relaxed states: eyelid closure often leads ear/head settling.

No stable blink interval distribution was measured. Fixed periodic blinking is not supported by the footage.

### 4.6 Gaze

Eevee spends large portions of Partner Play oriented toward the player/camera. **[V1]** Continuous pupil-level tracking of the cursor was **not** robustly confirmed. Important behavior-level attention changes include:

- protest: front/user-facing attention largely maintained,
- withdrawal: gaze/head drop away/down,
- high-five invitation: front/user-oriented while the paw is offered; the paw pose itself carries the invitation,
- mood phrase: eyes open toward user → close during enjoyment → reopen during reset,
- contact-seeking cheek response: eyes close during body commitment, reopen at rebound, close again during content hold.

### 4.7 Ears

Ears are one of the most informative channels in the corpus.

Observed roles:

1. **Independent micro/asymmetric state:** relaxed idle can leave one ear lower than the other.
2. **Anticipation/lead:** E04 mood phrase begins with one ear before face/forepaws.
3. **Reaction-type discriminator:** E03 sharp protest leaves ears comparatively restrained; withdrawal strongly spreads/lowers them.
4. **Emotion amplifier:** E01 major delight and E02 delayed special affection recruit larger ear motion than the earlier smaller positive stages.
5. **Contact response lead:** E05 cheek macro response shows ear movement slightly before clear eyelid/head commitment.

### 4.8 Limbs

Limbs are not baseline “life noise.” **[V1]** They become meaningful when a behavior requires them.

- E01 autonomous paw action: forelimbs become the primary gesture; ears/tail remain comparatively quiet.
- E02 high-five: one forepaw presents and waits; the opposite foreleg remains supporting/still.
- E04 mood phrase: forepaws are withheld until the stronger second accent.
- E05 cheek response: forepaws gather during compression, then both rise at rebound peak.

Hindlegs are primarily grounding in the observed front-facing Partner Play footage.

### 4.9 Tail / Secondary Structures

The tail has a large silhouette but low baseline activity. It does not automatically wag for every happy interaction or protest. **[V1]** This is consistent across the five videos.

Independent neck-fur / body-fur dynamic motion could not be reliably separated from the underlying body motion in this corpus. **未確認**.

### 4.10 Intentional Stillness

The corpus strongly supports intentional stillness as a legitimate living state. **[V1]**

Key examples:

- E01 ≈128.9–150+ s: ~20+ s relaxed moving hold.
- E02 105.8–114 s and 117–128 s: long quiet neutral windows.
- E03 97–105.4 s: ~8 s quiet hold.
- E04 140–145 s and 147–152.8 s: quiet windows between autonomous phrases.
- E05 100–105 s: very quiet neutral state.

These states are not necessarily perfectly motionless; tiny head/ear/eyelid drift may remain. The key observation is **low event density without deadness**.

### 4.11 Channel Asynchrony

The videos repeatedly show that “alive” does not mean simultaneous movement. Common patterns include:

```text
face → ears/body later
```

```text
one ear → face → other ear → forepaws
```

```text
eyelids → head → ear
```

```text
ears → eyelids/head → torso → forepaws
```

and selective behaviors where several other channels remain intentionally inactive.

---

## 5. Attention & Gaze Grammar

### 5.1 User / camera fixation

Front-facing attention is common in neutral Partner Play and especially during high-five invitation. **[V1]** The high-five is readable without Eevee repeatedly looking at its own paw.

### 5.2 Touch location attention

Clear continuous eye-only tracking of the touch point was not confirmed. **未確認**. The footage often relies more on eyelids, head pose, ears, and body response than on obvious pupil saccades.

### 5.3 Gaze away / disengagement

Withdrawal behavior in E03 is the clearest evidence: the head lowers and gaze visually drops away/down, contrasting with protest where attention remains more user-facing. **[V1]**

### 5.4 Eye-only vs head-only

The corpus does not provide enough reliable close-up evidence to quantify eye-only saccades. Head-only or head-dominant changes are visible in idle tilt/sway families. **[V1]**

### 5.5 Eyes → head / head → eyes

No single universal order is supported. Behavior-specific orders are more accurate:

- Relaxed state E01/E04: eyelids can soften/close before ear/head settling. **[V1]**
- Mood phrase E04: one ear/body cue begins before eyelids close. **[V1]**
- Cheek macro response E05: ears move first, then eyelids/head commit. **[V1/V2]**

### 5.6 Fixation and release

High-five gives the clearest social fixation grammar:

```text
present paw while facing player
→ wait
→ contact
→ close eyes / break visual monitoring during pleasure
→ reopen
```

### 5.7 Anticipation

The footage does **not** robustly show cursor approach always causing an anticipatory gaze/head move before touch. The strongest anticipation examples are character-authored body cues such as high-five paw presentation and E04 ear-led mood phrase. **[V1]**

### 5.8 Disengagement

The strongest disengagement grammar is:

```text
negative state persists
→ ears lower/spread
→ head lowers
→ gaze drops away
→ hold
→ staged recovery
```

This differs from direct protest, where the face stays communicative toward the user.

---

## 6. Facial Motion

### 6.1 Blink

Measured example: ~133 ms visible neutral blink, ~67 ms full closure in E01. **[V1, n=1]** No fixed interval confirmed.

### 6.2 Asymmetric blink

A clearly measured asymmetric left/right blink sequence was **not established** from this corpus. **未確認**.

### 6.3 Eyelid openness

Eyelid openness is an expressive continuous channel:

- open neutral,
- narrowed irritation,
- half-lidded transition,
- full close for pleasure/relaxation,
- full close as recovery punctuation.

### 6.4 Eye direction

Large behavioral changes are visible (front vs downward/away), but fine pupil/iris direction was not quantified.

### 6.5 Mouth

Observed mouth roles include:

- neutral small mouth,
- small positive opening,
- broad/open smile,
- downturned dislike,
- delayed open-mouth protest,
- open-mouth variation after repeated high-five,
- small restrained mouth during deep contact compression followed by wider rebound mouth.

### 6.6 Cheek / muzzle

The videos do not provide evidence for a strongly visible, physically deformed cheek/muzzle mesh at the exact contact point. **[V1]** Semantic facial meaning is clearer than local surface deformation.

### 6.7 Positive facial sequence

Positive reactions often evolve rather than switch instantly:

```text
neutral
→ eyelids soften/close
→ small smile
→ hold
→ reopen/reset
→ stronger close / wider smile at second peak
→ settle
```

E04 mood phrase and E05 cheek macro response are strong examples.

### 6.8 Anticipation face

High-five invitation is comparatively neutral/slightly content before success; Eevee does not display the full success smile before the player responds. **[V1]**

### 6.9 Surprise / confusion

A specific, confidently labeled “surprise” or “confusion” face could not be isolated with enough certainty. Open-mouth variations exist, but semantic labels beyond observable shape are **未確認**.

### 6.10 Dislike / protest

Two face-related negative styles are clear:

- narrowed eyes / brow-like compression + frown/open-mouth protest,
- sad/uneasy eyes + lowered gaze/head during withdrawal.

### 6.11 Relaxation

Closed eyes + lowered/broadened ears + stable COM/head-down hold recur in several videos. **[V1]**

### 6.12 Recovery

Recovery is often staged rather than an immediate neutral snap. A repeated negative pattern is:

```text
negative hold
→ eyes close
→ pose begins restoring
→ eyes reopen neutral
```

---

## 7. Touch Causality

### 7.1 General causal structure observed

The footage supports several distinct causal grammars rather than one universal pipeline.

#### Slow positive stroke

```text
continuous contact
→ gesture accumulation / quiet hold
→ facial pleasure evaluation
→ content hold
→ later stronger ear/body/VFX peak
→ settle
```

#### Sharp negative protest

```text
continued unwanted contact
→ face tightens
→ negative expression becomes readable
→ optional VFX
→ mouth opens / protest
→ settle / eye-close recovery
```

#### Withdrawal

```text
persistent low-valence state
→ ears spread/lower
→ head/body lower
→ gaze disengages
→ moving hold
→ eye-close recovery
→ neutral
```

#### Reciprocal high-five

```text
Character initiates
→ paw presented
→ wait-for-user state
→ discrete contact
→ 1–2 frame-scale acknowledgement
→ small social success
→ either next invitation / settle / delayed major affect
```

#### Cheek/contact-seeking response

```text
continued cheek contact
→ acceptance / accumulation
→ ears lead
→ eyes close + head/body move down into interaction
→ deep hold
→ rebound
→ forepaws join
→ second eyes-closed content hold
→ recovery
```

### 7.2 Head / forehead

Head/forehead contact can lead to both positive and negative states in the observed footage. **[V1]** Therefore screen-space zone alone is insufficient to explain reaction selection. Gesture, duration, repetition, and current affect likely matter. **[I]**

### 7.3 Cheek

E05 provides the strongest evidence of a larger contact-seeking macro response. **[V1]** However left/right locality is weak in the observed macro family; opposite-side contacts can converge on a centered bilateral response. **[V1]**

### 7.4 Ear

No ear-specific touch interaction was isolated with enough certainty to create a dedicated causal rule. **未確認**.

### 7.5 Face

Face contact broadly recruits eyelids/mouth/head/ears, but exact semantic subzones and collision boundaries are not observable from the footage.

### 7.6 Body / chest/front

Several front/chest interactions transition into positive expressions and larger pleasure responses. **[V1]** Exact chest-zone boundaries remain unmeasured.

### 7.7 Disliked zone / sustained negative input

E03 is the strongest evidence that prolonged input must preserve context. The character does not simply play one protest and forget; low-valence face states persist and additional protest/withdrawal families reappear while the interaction continues. **[V1]**

### 7.8 Feeding as staged interaction

Although not a touch-zone reaction, feeding repeatedly shows:

```text
item present at mouth
→ item disappears / consume event
→ short neutral processing interval
→ delight response
```

The repeated ~0.8–0.9 s gap is important temporal evidence. **[V1/V2]**

---

## 8. High-Density Interaction Timelines

### 8.1 E01 — Head Pet Positive

| Time | Trigger / Context | Eyes | Face | Head | Ear L | Ear R | Body / COM | Limbs | Tail / Secondary | Interpretation |
|---:|---|---|---|---|---|---|---|---|---|---|
| **09.833** | hand/contact episode visible | open | neutral | neutral | upright | upright | stable | stable | stable | interaction begins **[V1]** |
| 09.83–11.33 | continued stroke | mostly open | mostly neutral | little obvious change | stable | stable | stable | stable | stable | gesture accumulates **[V1/V2]** |
| **11.367** | ongoing pet | closes | pleasure mouth | slight | mostly upright | mostly upright | stable | stable | — | first semantic pleasure **[V1]** |
| 11.4–12.9 | continued interaction | closed | content | subtle hold | mostly stable | mostly stable | minor | stable | — | moving hold **[V1]** |
| ≈13.03 | transition | reopen | positive | — | — | — | — | — | — | reset before second peak **[V1]** |
| **≈13.10** | second positive event | softening | stronger | — | movement begins | movement begins | small | — | VFX onset | larger emotional peak starts **[V1]** |
| ≈13.13–13.20 | peak building | closes | smile | stable | sweeps outward/down | sweeps outward/down | small | — | VFX | appendage amplification **[V1]** |
| ≈13.3–13.7 | peak | closed | broad smile | stable | broad | broad | small | stable | VFX | major pleasure peak **[V1]** |
| 14 s range | release | reopening | content | recovers | recovers | recovers | stable | stable | VFX decays | settle **[V1]** |

### 8.2 E01 — Negative Forehead Reaction

| Time | Trigger / Context | Eyes | Face | Head | Ears | Body / COM | Tail / Secondary | Interpretation |
|---:|---|---|---|---|---|---|---|---|
| 55.50–55.77 | continued input | neutral | neutral | stable | upright | stable | none | pre-evaluation |
| **55.80–55.83** | continued input | narrow | brow-like tightening | stable | upright | stable | none | evaluation starts **[V1]** |
| **55.87** | continued input | narrowed | frown | stable | upright | stable | none | displeasure readable **[V1]** |
| **55.93–55.97** | — | negative | negative | stable | upright | stable | star/crescent cue | semantic confirmation **[V1]** |
| ≈56.5 | — | negative | mouth opens | stable | mostly upright | small | stars | protest escalation **[V1]** |
| **≈56.97** | — | protest | open/negative | stable | broad outward | stable | — | ear peak follows face by ~1.1 s **[V1/V2]** |
| ≈57.10 | release | closes | softens | stable | broad | stable | — | settle |
| ≈57.27 | — | reopens | neutral | stable | recovers | stable | — | recovery complete |

### 8.3 E01 — Feeding #1

| Time | Item | Eyes / Face | Ears | Body | Interpretation |
|---:|---|---|---|---|---|
| 74–77.6 | berry held at mouth | mostly neutral | upright | stable | presentation/contact phase **[V1]** |
| ≈77.60 | berry visible | neutral | upright | stable | last visible item |
| **≈77.63** | berry gone | neutral | upright | stable | consume event **[V1]** |
| 77.63–78.43 | gone | neutral | upright | stable | processing/chew-like pause **[V2]** |
| ≈78.47 | gone | face begins evaluate | — | — | emotional onset |
| **≈78.53** | gone | eyes closed | ears begin follow | small | delight starts **[V1]** |
| ≈78.73 | gone | smile opens | lower/outward | small | escalation |
| 78.9–79.2 | gone | broad smile | broad | small | peak |
| ≈79.4–79.47 | — | reopen/neutralize | recover | stable | settle |

### 8.4 E01 — Autonomous Paw Action

| Time | Trigger | Eyes / Face | Forelegs | Ears | Root / Tail | Interpretation |
|---:|---|---|---|---|---|---|
| 98.4–98.60 | no user trigger visible | neutral | resting | still | stable | intentional hold |
| **98.633** | autonomous | blink closed | still | still | stable | face leads **[V1]** |
| ≈98.70 | — | reopens | preparing | still | stable | transition |
| **≈98.80** | — | attentive | paws lift | still | stable | primary action starts |
| **≈98.87** | — | mouth opens | one/both paws higher | still | stable | intent readable |
| ≈99.0–99.3 | — | open/curious | gesture peak | still | stable | peak |
| ≈99.7 | — | recovery | paws lower | mostly still | stable | settle |

### 8.5 E01 — Long Relaxed Moving Hold

| Time | Eyes | Head | Ears | Body / COM | Interpretation |
|---:|---|---|---|---|---|
| **128.333** | half-close | neutral | upright | stable | relaxed state begins **[V1]** |
| **128.367** | full close | starts lowering | upright | stable | eyelids lead |
| ≈128.43 | closed | pitch down | upright | stable | head follows |
| ≈128.63 | closed | low | one ear starts lowering | stable | ear delayed |
| **≈128.87** | closed | low | asymmetric pose established | stable | relaxed configuration |
| 129–150+ | closed | low with tiny drift | asymmetric tiny drift | stable | ~20+ s moving hold |
| ≈151.67 | re-engagement | begins returning | responds | touch redirects state | interruptible living state |

### 8.6 E02 — High-Five #1

| Time | Trigger | Eyes | Face | Head | Ears | Body / COM | Forelimbs | Interpretation |
|---:|---|---|---|---|---|---|---|---|
| 33.233 | no player contact | open | neutral | neutral | stable | stable | resting | pre-invitation |
| **33.267–33.333** | character initiates | open | neutral | small | stable | stable | one paw rises | autonomous initiation **[V1]** |
| 33.400 | invitation | open | neutral | stable | stable | stable | pad faces player | body part presented |
| 33.500–33.667 | wait | open | neutral | stable | stable | stable | paw held | **WAIT_FOR_USER** behavior |
| ≈33.700 | cue | open | neutral | stable | stable | stable | paw held | contact opportunity |
| 34.00–34.33 | player approaches | open | neutral | stable | stable | stable | held | user turn |
| **34.400** | contact flash | open → change | neutral → change | stable | restrained | stable | contact | success contact **[V1]** |
| **≈34.467** | post-contact | closed | smile | stable | restrained | stable | starts retract | ~67 ms acknowledgement **[V1]** |
| 34.50–34.63 | success | closed | smile | stable | restrained | stable | retracts | micro-success hold |
| ≈34.70–34.80 | settle | reopens | near-neutral | stable | stable | stable | lowered | recovery |

### 8.7 E02 — High-Five #5 → Delayed Major Affect

| Time | Trigger | Eyes / Face | Ears | Body / Paw | Secondary | Interpretation |
|---:|---|---|---|---|---|---|
| ≈41.33–41.50 | character initiates | neutral | stable | paw rises | — | invitation |
| ≈41.70 | cue | neutral | stable | paw held | local cue | waiting |
| **≈42.50** | contact | small immediate change | restrained | success | local contact cue | micro-success **[V1]** |
| 42.53–42.67 | settle | small response | restrained | paw lowers | — | ordinary success |
| 42.8–43.2 | no new player action | neutral-ish | stable | settled | — | quiet interval |
| **≈43.25** | autonomous/delayed event | begins changing | starts recruiting | stable | strong audio transient nearby | delayed larger affect **[V2]** |
| **≈43.367** | — | eyelids soften | larger | stable | pink/heart aura | major event begins **[V1]** |
| 43.400–43.433 | — | closes | broader | stable | VFX | evaluation/commitment |
| **≈43.533** | — | broad smile | wide | stable | broad VFX | emotional peak |
| 43.53–44.10 | hold | closed/content | wide | stable | VFX | major hold |
| ≈44.30 | settle | reopens | recover | stable | decay | recovery |

### 8.8 E03 — Sharp Protest #1

| Time | Trigger | Eyes | Face / Mouth | Head | Ears | Body / COM | Secondary | Interpretation |
|---:|---|---|---|---|---|---|---|---|
| 9.600 | continued unwanted input | open | neutral | stable | upright | stable | — | pre-onset |
| 9.633 | — | open | neutral-ish | stable | upright | stable | — | pre-onset |
| **9.667** | — | begins narrowing | brow-like tightening | stable | upright | stable | — | first clear acknowledgement **[V1]** |
| 9.700–9.733 | — | narrowed | irritation readable | stable | upright | stable | — | emotion established |
| ≈9.767–9.900 | — | negative | frown | stable | upright | stable | star/dizzy cue | escalation |
| 10.033–10.300 | — | negative | negative hold | stable | upright | stable | — | moving hold |
| **10.333** | — | negative | mouth opens | stable | upright | stable | — | explicit protest |
| 10.40–10.63 | — | negative | repeated open-mouth shape | stable | upright | stable | audio peak ≈10.44 | peak **[V1/V2]** |
| 10.70–10.87 | release | softens | mouth closes | stable | upright | stable | — | settle |
| ≈10.93 | — | closes | neutralizing | stable | upright | stable | — | recovery punctuation |
| ≈11.10–11.13 | — | open | neutral | stable | upright | stable | — | complete |

### 8.9 E03 — Withdrawal #1

| Time | Trigger / State | Eyes | Face | Head | Ears | Body / COM | Interpretation |
|---:|---|---|---|---|---|---|---|
| 20.40–20.50 | persistent negative state | sad/uneasy | sad | upright | upright | stable | low-valence hold |
| ≈20.53–20.60 | — | short close | sad | upright | upright | stable | punctuation |
| ≈20.67 | — | reopens sad | sad | upright | upright | stable | negative state persists |
| **≈20.80** | continued context | sad | sad | begins changing | ears start lateral/down | stable | withdrawal starts **[V1]** |
| ≈20.87 | — | sad | sad | changing | strong spread | stable | appendage commitment |
| **≈20.90–21.00** | — | downward | sad | lowers | broad/low | visible body lowers | disengagement commitment |
| 21.1–21.9 | — | down/soft | sad | low | low/lateral | lowered hold | withdrawal moving hold |
| 22.00 | — | soft | sad | low | low | low | still held |
| ≈22.13 | recovery | starts closing | softens | starts restore | starts restore | stable | recovery begins |
| **≈22.17–22.27** | — | closed | neutralizing | restoring | restoring | restoring | staged reset |
| **≈22.33** | — | open | neutral | normal | normal | normal | recovery complete |

### 8.10 E04 — “ノリノリ” Entry Phrase

| Time | Trigger | Eyes / Face | Head | Ear screen-L | Ear screen-R | Body / COM | Forelimbs | Interpretation |
|---:|---|---|---|---|---|---|---|---|
| 0.400 | scene state | open neutral | neutral | high | high | grounded | resting | start |
| **≈0.600** | autonomous phrase | open | tiny change | starts lateral | high | stable | resting | first visible lead **[V1]** |
| ≈0.700 | — | open | small orientation | clearly lateral | high | stable | resting | asymmetric phrase |
| 0.80–1.20 | — | small mouth change | slight sway | held | begins responding | grounded | resting | anticipation/rhythm |
| **≈1.267** | — | eyelids lower | — | — | — | stable | resting | facial affect begins |
| **≈1.300** | — | eyes closed | — | — | — | stable | resting | first joy phase |
| ≈1.333 | — | smile | subtle | asymmetric | secondary move | stable | resting | first emotional peak |
| 1.5–2.0 | — | closed/content | soft | changing | changing | stable | resting | moving hold |
| ≈2.133–2.167 | — | reopens | neutral-ish | recovering | recovering | stable | resting | partial reset |
| **≈2.700** | second accent | eyelids lower | slight | broadens | broadens | stable | prep | stronger subphrase begins |
| **≈2.800** | — | closed | — | lateral | lateral | stable | prep | accent |
| ≈2.900 | — | broader smile | — | broad | broad | stable | starts recruiting | energy rises |
| **≈2.933** | — | closed/happy | — | broad | broad | stable | both paws lift | strong accent **[V1]** |
| 3.00–3.10 | peak | peak smile | small | broad | broad | stable | pads visible | peak |
| ≈3.133 | release | soft smile | settles | recover | recover | stable | descend | release |
| 3.2–3.43 | after-accent | closed/content | settles | recover | recover | stable | grounded | after-hold |
| **≈3.47–3.50** | settle | reopen | neutral | upright | upright | stable | resting | phrase complete |

### 8.11 E04 — Relaxed Moving Hold

| Time | Eyes | Ears | Head / Body | Interpretation |
|---:|---|---|---|---|
| 152.80 | open | upright | neutral | baseline |
| ≈152.90 | half-close | upright | stable | relaxed state begins |
| ≈152.93 | closed | upright | stable | eyelids lead |
| 153.00 | closed | starts changing | stable | appendage follows |
| **≈153.07** | closed | lowering | stable | ear response visible |
| **≈153.13** | closed | broad/lateral | tiny settle | relaxed configuration |
| 153.2–155.8 | closed | held low/lateral | tiny drift | moving hold |
| 156.0–156.6 | closed | slowly rises | stable | recovery |
| **≈156.83–156.87** | reopens | near-normal | stable | neutral return |

Eyelid → clear ear change delay is approximately **4–6 frames ≈130–200 ms**. **[V1/V2]**

### 8.12 E05 — Cheek / Contact-Seeking Macro Response #1

| Time | Trigger | Eyes | Face | Head | Ears | Body / COM | Forelimbs | Interpretation |
|---:|---|---|---|---|---|---|---|---|
| 19.98 | hand near cheek | open | neutral | neutral | upright | stable | grounded | pre-onset |
| 20.05–20.08 | continued contact | open | neutral | neutral | upright | stable | grounded | buildup |
| **≈20.12** | — | open | neutral | beginning | **swing strongly outward** | stable | grounded | earliest macro cue **[V1]** |
| **≈20.15** | — | narrows | changes | starts downward | broad | starts committing | gathered | ear leads head/eyes by ~1 frame **[V1/V2]** |
| **≈20.18** | — | closed | restrained | clearly down | broad | down/forward | inward/gathered | deep contact phase |
| 20.22–20.50 | — | closed | restrained | descends | broad | descends | gathered | compression |
| 20.5–20.88 | — | closed | restrained | deep low hold | broad | low hold | gathered | contact moving hold |
| **≈20.92** | — | begins reopening | changing | rises | still broad | rebound begins | preparing | release starts |
| ≈20.95 | — | opens | mouth opens | up | broad | rises | lifting | joy rebound |
| **≈20.98** | — | open | positive/open | up | broad | recovered | both paws raised | rebound peak starts |
| 21.0–21.22 | — | open | positive | high | broad | stable | paws up | peak |
| ≈21.25 | after-phase | lids lower | softens | settles | broad | stable | lowering | second content phase starts |
| **≈21.28** | — | closed | content | settled | relaxed/broad | stable | lower | afterglow hold |
| 21.3–22.4 | — | closed | content | stable | held | stable | grounded | prolonged content hold |
| ≈22.5 | recovery | reopens | neutralizing | neutral | recovers | stable | grounded | return |
| ≈22.6 | — | open | neutral | neutral | upright | stable | grounded | complete |

### 8.13 E05 — Cheek / Contact-Seeking Macro Response #2

| Time | Eyes / Face | Head / Ears | Body / Limbs | Interpretation |
|---:|---|---|---|---|
| ≈65.9 | preparatory | ears lateral | stable | onset |
| ≈66.0 | eyes close | head/body move deep down | forelimbs gather | compression |
| 66.0–66.6 | closed/content | lowered hold | deep moving hold | same structure as response #1 |
| ≈66.7 | reopen/open mouth | rises | paws rise | rebound |
| 66.7–67.0 | positive | up | paws raised | peak |
| ≈67.1 | eyes close | settles | paws lower | second content phase |
| 67.1–68.2 | closed/content | held | stable | afterglow |
| ≈68.3–68.4 | reopen | recover | neutral | complete |

---

## 9. Motion Anatomy

### 9.1 Primary Motion

Primary motion depends strongly on behavior family:

- positive head/face touch: eyelids/face, later ears,
- high-five: one forepaw,
- withdrawal: ears + head/gaze + lowered visible body posture,
- mood phrase: one ear first, later face/other ear/forepaws,
- cheek contact-seeking: ears/head/body, then rebound forepaws,
- idle sway: head/ears,
- feeding delight: face/ears after consumption pause.

### 9.2 Secondary Motion

The most consistently visible secondary/follow-up channel is the ear system. The tail is frequently *not* recruited. Fur-specific residual motion could not be confidently isolated.

### 9.3 Anticipation

Observed anticipation is clearest when the character initiates or enters a bounded phrase:

- high-five: paw rises and is held before the player acts,
- mood phrase: one ear initiates before stronger face/limb recruitment,
- cheek macro response: brief ear/head preparation before the deep body commit.

### 9.4 Overshoot / Rebound

E05 provides the clearest compression/rebound structure:

```text
deep head/body compression
→ held contact state
→ rapid rise
→ forepaw accent
→ second content hold
```

The analysis did not calculate joint-angle overshoot numerically.

### 9.5 Follow-through

Follow-through is usually semantic rather than all-body physics noise:

- ears enlarge the later emotional peak,
- forepaws join the stronger phase of the cheek response,
- relaxed ears settle after eyelid changes,
- body can settle after head/attention decisions.

### 9.6 Overlap

Actions overlap in time but do not begin together. This is one of the strongest recurring life cues.

### 9.7 Moving Hold

Moving holds are common and central:

- long relaxation >20 s,
- withdrawal hold ~1 s,
- cheek deep hold ~0.4–0.7 s,
- cheek second content hold ~1+ s,
- high-five WAIT_FOR_USER can last roughly 0.8–1.7 s in observed cycles,
- mood phrase contains a partial reset/hold between accents.

### 9.8 Settle

Settle is usually staged. A common rule is not “peak → neutral,” but “peak → softer state / closed eyes / hold → reopen / neutral.”

### 9.9 Grounding

Grounding is strong. Even energetic or social gestures often keep the root/hindquarters visually stable. The character only spends larger COM movement when the behavior meaning requires it.

### 9.10 Weight / Inertia

Exact mass/inertia values cannot be measured. Visually, Eevee avoids floaty whole-body oscillation. Downward withdrawal and contact-seeking compression create a sense of weight through held posture and delayed release rather than through continuous bouncing. **[V1/I]**

### 9.11 Internal implementation is unknown

The videos do **not** reveal whether observed secondary motion is produced by hand-authored animation, spring bones, runtime physics, additive clips, constraints, IK, or another system. No such implementation claim is made here.

---

## 10. Asynchrony & Propagation

The corpus contains several distinct propagation grammars. They should not be collapsed into a single universal order.

### Pattern A — Positive pet, face first

Observed in E01/E04:

```text
stroke/contact accumulates
→ eyelid / mouth pleasure
→ content hold
→ later ears
→ larger affect/VFX
→ settle
```

### Pattern B — Sharp protest

Observed in E01/E03/E04:

```text
continued unwanted contact
→ eyelid/brow-like tightening
→ frown
→ VFX cue
→ delayed mouth-open protest
→ eye-close recovery
→ neutral
```

Ears can remain relatively restrained.

### Pattern C — Withdrawal

Observed repeatedly in E03:

```text
low-valence state
→ ears spread/lower
→ head/body lower
→ gaze disengages/down
→ held withdrawal pose
→ eyes close
→ head/ears restore
→ eyes reopen neutral
```

### Pattern D — Reciprocal high-five

Observed in E02:

```text
paw rises
→ presentation hold
→ WAIT_FOR_USER
→ discrete contact
→ ~1–2 frames
→ eyes/face success acknowledgement
→ paw retracts
→ small settle
```

Larger emotional response may be scheduled later as a separate event.

### Pattern E — Rhythmic mood phrase

Observed in E04:

```text
one ear
→ slight mouth/head
→ eyelids close + smile
→ opposite ear joins
→ partial reset
→ second eyelid/smile accent
→ both forepaws join late
→ settle
```

### Pattern F — Relaxation

Observed E01/E04:

```text
eyelids soften/close
→ head settles
→ one/both ears lower after delay
→ long moving hold
→ gradual recovery
```

E04 measured eyelid-to-ear delay: roughly 4–6 frames / 130–200 ms. **[V1/V2]**

### Pattern G — Cheek/contact-seeking macro response

Observed E05:

```text
ears spread
→ ~1 frame later eyelids/head commit
→ torso/head lower
→ forepaws gather
→ deep hold
→ rebound
→ mouth opens + both forepaws rise
→ eyelids close again
→ prolonged content hold
→ recovery
```

### Core asynchrony rule

**[G]** Grimo should author causal phase relationships, not add random offsets to every bone. The offsets should have meaning: attention, evaluation, commitment, support, follow-through, or afterglow.

---

## 11. Emotion Grammar

### 11.1 Affection / Pleasure

**Face:** closed eyes, small-to-broad smile.  
**Gaze:** external attention can be suspended by eye closure during accepted contact.  
**Body:** often restrained initially; stronger body commitment in cheek/contact-seeking family.  
**Ears:** frequently stronger at later emotional peaks.  
**Timing:** can be slow/accumulated for petting, immediate for reciprocal social success.  
**Recovery:** often includes content hold before neutral.  
**Afterglow:** present, but ordinary small reactions can have shorter afterglow than ideal for Grimo. **[V1/G]**

### 11.2 Happiness / Delight

Two-stage positive reactions are common:

```text
small pleasure
→ hold/reset
→ larger delight
```

Large stages may recruit ears and VFX. **[V1]**

### 11.3 Curiosity

Curiosity is suggested by head-tilt / autonomous paw families, but a unique internal “curiosity state” cannot be proven. **[I]** Visually, small head/eye/ear actions with stable root are the reusable pattern.

### 11.4 Anticipation

Character-authored anticipation is clearest in high-five paw presentation and mood phrase ear lead. **[V1]**

### 11.5 Relaxation

Closed eyes, lowered or broadened ears, head-down or soft lateral pose, stable grounded body, and long quiet holds recur across multiple videos. **[V1]**

### 11.6 Surprise

Not confidently isolated as a dedicated semantic category. Open-mouth variations exist, but label remains **未確認**.

### 11.7 Confusion

Not confidently isolated. **未確認**.

### 11.8 Mild Dislike / Protest

Face remains user-oriented; eyes narrow, mouth turns negative and later opens; body is comparatively restrained. **[V1]**

### 11.9 Withdrawal / Disengagement

Gaze drops, ears lower/spread, head/body move down, pose is held. This is visually different from protest and is less confrontational. **[V1]**

### 11.10 Satisfaction / Contentment

Often expressed as a prolonged eyes-closed hold after a stronger peak rather than by continued large motion. E05 second content phase is the clearest example. **[V1]**

### 11.11 Excitement / “ノリノリ”

Expressed as a short bounded phrase with unequal accents, asymmetric lead, progressive channel recruitment, and a clear end—not permanent dance motion. **[V1]**

---

## 12. Autonomous / Self-Initiated Behavior

### 12.1 Reciprocal invitation

E02: Eevee raises one paw and waits for the user. The player is responding to Eevee’s action, not merely triggering a reaction. **[V1]**

### 12.2 Autonomous paw gesture

E01 ≈98.6–99.7 s: blink → paws lift → mouth opens → gesture peak → settle, with limited ear/tail involvement. **[V1]**

### 12.3 Head tilt / sway families

Observed repeatedly across E01, E02, E03, E04, E05. These are short bounded autonomous phrases between quiet states. **[V1]**

### 12.4 Long relaxed holds

Autonomous low-energy state changes occur without visible player input. **[V1]**

### 12.5 Mood self-expression

E04 opening sequence visually expresses the UI-labeled “ノリノリ” state before the player initiates touch. **[V1]** This is strong evidence that current state can alter self-initiated performance.

### 12.6 Gift presentation

E04 ≈131.1–134.1 s: Eevee appears holding a flower/plant-like gift, holds through message/UI, then shows an eyes-closed positive state. **[V1]** Trigger conditions are unknown.

### 12.7 Rare / special larger affect

E02 delayed special affection reaction after several high-five exchanges is visually separate from the immediate micro-successes. **[V1/I]** Exact trigger remains unknown.

---

## 13. Variation & Repetition

### 13.1 Identical-looking or near-identical families

- E01 ≈55.9 and ≈58.4 negative forehead reactions: visually very close. **[V1]**
- E03 sharp protest #1/#2 and E04 ≈44–45.7 protest: closely matching family. **[V1/V2]**
- E03 withdrawal around 20–22, 26–27, 39–41, 71–73: strongly repeated structure. **[V1/V2]**
- E01 feeding delight #1/#2 and E02 feeding delight: very similar consume-pause-delight timing family. **[V1/V2]**
- E01/E02/E03/E04/E05 head-tilt/relax idle families visibly recur. **[V1/V2]**
- E05 cheek macro response ≈20 s and ≈66 s: highly similar sequence and duration. **[V1]**

### 13.2 Same family, different variation

- High-five #1–#3: very similar closed-eye micro-success.
- High-five #4: same reciprocal structure but open-mouth variation after contact.
- High-five #5: small immediate success followed later by a separate larger affect event.
- Positive pet reactions: same broad face-first → later-ear principle, but amplitude/VFX timing varies.

### 13.3 Timing variation

High-five invitation hold duration varies with user response; the character can wait roughly 0.8–1.7 s in the observed cycles rather than advancing on a fixed clip time. **[V1/V2]**

### 13.4 Amplitude variation

Small high-five successes reserve ears/body/VFX; delayed special affect recruits more. Mood phrase second accent recruits forepaws after a smaller first accent. **[V1]**

### 13.5 Initial-state variation

The same broad touch region can yield positive or negative outcomes depending on continuing context; exact internal variables are unknown. **[V1/I]**

### 13.6 Afterglow variation

- small high-five success: short afterglow, fast return,
- delayed special affection: larger/longer hold,
- cheek contact-seeking: second eyes-closed content phase lasts around a second or more,
- long relaxation: state itself can persist many seconds.

### 13.7 Obvious repetition / cannedness

The corpus demonstrates that even high-quality Partner Play can expose clip families under repeated use. Negative protest/withdrawal and cheek-rub macro reactions are the clearest cases.

### 13.8 Anti-Repetition Lessons for Grimo

**[G]**

1. Keep deterministic causality stable; vary performance, not meaning.
2. Track recent reaction family, not only exact clip ID.
3. Suppress immediate repeats across “visually similar” groups.
4. Vary initial pose, gaze, ear side, amplitude, settle, and afterglow.
5. Side-condition macro reactions so left/right touch does not always collapse to one centered performance.
6. Do not restart a negative clip from frame 0 while contact continues; maintain state and layer escalation.
7. Reserve rare larger reactions and delayed follow-up events.

---

## 14. Character-Specific Motion Personality — Partner Eevee Motion Personality Bible

| Dimension | Consolidated Observation |
|---|---|
| **Resting posture** | front-facing, grounded, stable root/feet, ears usually upright; many long holds **[V1]** |
| **Baseline energy** | low–medium; punctuated by bounded autonomous actions rather than constant motion **[V1]** |
| **Motion amplitude** | small for baseline; medium/large selectively for ear peaks, withdrawal, cheek macro response, special affect **[V1]** |
| **Preferred motion lead** | behavior-dependent: face for evaluation, one ear for mood phrase, one forepaw for invitation, ears/head for withdrawal/contact-seeking **[V1]** |
| **Tempo** | mixed; fast 1–2 frame social ACK, 1–3 s reaction phrases, multi-second moving holds, >20 s relaxed state **[V1]** |
| **Gaze personality** | often player/front-facing; breaks gaze for withdrawal; does not visibly chase every cursor movement **[V1]** |
| **Blink personality** | fast neutral blink possible (~133 ms example); eyelids double as major emotional/behavioral channels **[V1]** |
| **Ear personality** | highly expressive; independent/asymmetric in idle, reaction-type discriminator, later emotion amplifier, sometimes phrase lead **[V1]** |
| **Tail personality** | restrained; large silhouette but low default recruitment; not a universal happy wag channel **[V1]** |
| **Asymmetry** | strong in idle/mood lead; can become more bilateral at emotional peaks **[V1]** |
| **Reaction latency** | interaction-class-specific; reciprocal contact ~2-frame visible ACK, slow pet/feeding much slower semantic payoff **[V1]** |
| **Anticipation strength** | strong when character initiates (paw presentation) or in bounded phrase; weak/uncertain for cursor approach anticipation **[V1]** |
| **Overshoot / rebound** | strongest in cheek/contact response: compression → rise → paws-up accent **[V1]** |
| **Settle** | frequently staged; eyes close or content hold before neutral **[V1]** |
| **Stillness tendency** | high; multiple 4–20+ s quiet or low-motion intervals **[V1]** |
| **Affection style** | eyes-close pleasure, delayed ears, body can actively lean/commit during stronger contact acceptance **[V1]** |
| **Curiosity style** | small head tilt / paw / ear actions on stable body; exact semantic state inferred **[V1/I]** |
| **Dislike style** | two main visible strategies: user-facing sharp protest and gaze-breaking withdrawal **[V1]** |
| **Autonomous invitation style** | presents one paw and waits; patient low–medium-energy social initiation **[V1]** |
| **Rhythmic joy style** | ear-led, asymmetric, short phrase, progressive recruitment, clear end **[V1]** |
| **Contact-seeking style** | accepted prolonged cheek contact can trigger deep head/body commitment + rebound + second content hold **[V1]** |
| **Forbidden/generic-looking risk** | constant tail wag, all-channel synchronous bounce, identical centered macro reaction for every touch side, fixed periodic idles **[G]** |

---

## 15. What Creates the Sense of Life

### Tier 1 — Essential

1. **Causal, interaction-specific timing** — a discrete social success acknowledges quickly; slow stroke and feeding use slower evaluation/processing. **[V1]**
2. **Autonomous agency** — Eevee can initiate, wait, offer a body part, self-express mood, and present a gift. **[V1]**
3. **State continuity / moving holds** — reaction and emotion persist through holds instead of collapsing immediately to neutral. **[V1]**
4. **Selective asynchronous channels** — some body parts act while others remain still. **[V1]**
5. **Boundaries / non-compliance** — disliked interaction produces clear protest or withdrawal, not universal happiness. **[V1]**
6. **Intentional stillness** — low event density is allowed and often strengthens the sense of weight and self-possession. **[V1]**

### Tier 2 — Major Amplifier

7. **Face-first semantic evaluation** — emotion becomes readable before large body motion in many reactions. **[V1]**
8. **Progressive channel recruitment** — larger emotion recruits additional channels rather than merely increasing one oscillator. **[V1]**
9. **Character moves into interaction** — accepted touch can become bidirectional physical participation. **[V1]**
10. **Asymmetry with reason** — one ear, one paw, one side can lead; symmetry appears more at selected peaks. **[V1]**
11. **Delayed autonomous follow-up** — large affect can occur after the immediate player event rather than on the same frame. **[V1/I]**
12. **Turn-taking and waiting** — the character can pause because it expects the user to act. **[V1]**

### Tier 3 — Polish

13. VFX/audio that reinforce but do not create the underlying causality. **[V1]**
14. Multiple facial states within one positive or negative phrase. **[V1]**
15. Rare social/gift events. **[V1]**
16. Larger appendage amplitude reserved for major emotional peaks. **[V1]**
17. Repetition suppression and side-conditioned performance beyond the reference footage’s visible limitations. **[G]**

---

## 16. Failure / Weakness Analysis

The reference footage is not idealized here. Several weaknesses are directly visible.

### 16.1 Repetition / canned feeling

Sharp protest, withdrawal, feeding delight, head-tilt idle, and cheek macro response families repeat clearly under long observation. **[V1/V2]**

### 16.2 Macro reactions can dominate local touch causality

In E05, once the large cheek/contact response begins, the authored centered macro motion visually dominates exact cursor trajectory and contact side. **[V1]**

### 16.3 Left/right locality is weak in some positive macro responses

Opposite-side cheek contacts can converge on a bilateral centered response. **[V1]** This is a major Grimo improvement opportunity.

### 16.4 Gaze variation is limited during high-five repetition

Eevee largely maintains front/player-facing attention; it does not show rich per-cycle gaze variation toward paw, user, environment, and away. **[V1]**

### 16.5 Small social successes can return to neutral quickly

Some high-five micro-successes settle within a few hundred milliseconds. **[V1]** Grimo can preserve a subtler emotional residue longer.

### 16.6 Reaction restarts can expose clip boundaries

Under sustained disliked touch, the visible structure can become reaction → partial recovery/neutral → reaction, making clip families easier to detect. **[V1]**

### 16.7 Local physical deformation is not strongly readable

Immediate touch-point compression/recoil of cheek/fur is weaker than the semantic face/global reaction. **[V1]**

### 16.8 VFX can cover body acting

Large positive effects sometimes obscure part of the actual body performance. **[V1]**

### 16.9 Excessive synchronization is generally avoided, but some peak poses are bilaterally symmetric

This is often effective at peaks, but repeated identical bilateral paw/ear peaks could become mechanical if overused. **[V1/G]**

### 16.10 No evidence of major clipping/floating failures was isolated

No specific persistent clipping or obvious floating defect was documented in the analyses above. **未確認 / not observed as a major issue in the reviewed windows.**

---

## 17. Transferable Principles for Grimo

| Observed behavior | Why it feels alive | Abstract reusable principle | Grimo implementation implication |
|---|---|---|---|
| Some channels move while others rest | avoids mechanical “all bones are animated” look | selective channel ownership | masked/additive layers with explicit per-action channel budget **[G]** |
| Long moving hold | character appears to possess its own state/time | intentional stillness is valid behavior | scheduler must allow no major action for long intervals **[G]** |
| Face often evaluates before body peak | reaction appears interpreted, not triggered mechanically | semantic evaluation precedes full commitment | face/eyelid layer can lead primary body motion **[G]** |
| High-five paw presentation + wait | character has initiative and expectation | reciprocal turn-taking | explicit `WAIT_FOR_USER` interaction state **[G]** |
| High-five ACK in ~2 frames | direct social contact feels contingent | discrete reciprocal contact needs very fast confirmation | immediate local/face ACK before slower semantic layers **[G]** |
| Feeding has ~0.8–0.9 s pause | event feels processed rather than instantly rewarded | staged outcome | consumption phase separate from emotion payoff **[G]** |
| Protest vs withdrawal | character has more than one way to say no | emotion strategy, not one negative intensity slider | separate warning/refusal/disengagement families **[G]** |
| Withdrawal breaks gaze | attention itself communicates boundary | gaze target can encode social meaning | protest = user target; withdrawal = away/down target **[G]** |
| Mood expressed as bounded phrase | self-expression feels intentional | phrase, not loop | mood phrase controller + cooldown **[G]** |
| Stronger second accent recruits paws | unequal accents create authored acting | progressive channel recruitment | low/medium/high intensity masks **[G]** |
| Cheek response commits body into contact | user/character relation becomes bidirectional | accepted touch can become contact-seeking | side-specific lean/contact-hold controller **[G]** |
| Repeated same macro reaction exposes reuse | deterministic causality alone is not enough | vary performance around stable meaning | recent-family history + weighted variation **[G]** |
| Left/right contact can collapse to same centered clip | weak local causality becomes noticeable | preserve contact side throughout macro reaction | pass `contactSide`/local position into pose composition **[G]** |

### IP boundary

The transferable material in this document is the **principle**: timing structure, causal ordering, attention grammar, asynchrony, state continuity, turn-taking, boundary behavior, variation strategy, and emotional layering.

Do **not** copy Eevee-specific poses, exact motion paths, exact timing sequence, face performance, paw presentation pose, ear silhouette, or species-specific signature animation into Grimo.

---

## 18. Carol Implications

Carol is attention-seeking + relaxed, with a huge dream-cloud fleece, tiny cream face, large eyes, brown ears, hooves, moon/star motifs, low–medium energy, and a grounded/soft motion identity.

### 18.1 Base living

**[G]**

```text
root / hooves         mostly grounded
breath                tiny; not a whole-body squash loop
eyes / eyelids        sparse but expressive
head                  sparse micro-orientation
ear.L / ear.R         independently available
fleece                 cause-driven only
moon/star motifs       event-driven only
large motion           rare
intentional stillness  explicit valid state
```

### 18.2 Blink

The Eevee ~133 ms blink is evidence that very fast stylized blinks can read naturally, but it is **not** a Carol value to copy. **[G]** Initial Carol tuning can explore ~130–200 ms while preserving character identity.

### 18.3 Head / cheek pet causal stack

**[G]**

```text
contact
→ immediate local cheek/fleece acknowledgement
→ eyelid / eye acknowledgement
→ side-specific head/cheek lean
→ near ear relaxes
→ grounded body transfer
→ local fleece cluster follows
→ neighboring fleece settles later
→ content hold
→ afterglow
```

A prior starting envelope proposed in the chat was:

- local physical acknowledgement: ~0–80 ms,
- eyelid/eye: ~80–200 ms,
- near ear: ~150–350 ms,
- comfort accumulation: ~300–800 ms,
- once threshold crossed, head/cheek lean: ~0–300 ms,
- body follow: +100–300 ms,
- fleece cluster follow: +150–500 ms,
- contact-seeking hold: ~0.4–0.9 s,
- afterglow: ~2–5 s.

These are **[G] tuning ranges**, not Pokémon measurements.

### 18.4 Side-specific contact-seeking

E05 exposes a reference weakness that Carol should surpass. **[G]**

```text
cheek.L contact
→ cheek/head lean L
→ ear.L responds first
→ fleece.L responds first
→ body follows with small grounded transfer
```

and vice versa for the right side, with non-identical variations so the system is not a perfect mirror machine.

### 18.5 Long relaxed moving hold

Translate Eevee’s long relaxed state into Carol-specific anatomy:

```text
eyes soften/close
→ tiny cream face lowers slightly
→ one ear relaxes
→ other ear remains semi-alert
→ hooves remain heavy/grounded
→ local fleece settles after head
→ 8–25 s moving hold
→ tiny asynchronous corrections
```

Do not move the entire fleece as one breathing blob.

### 18.6 Reciprocal social invitation

Do not copy Eevee’s high-five. **[G]** Carol-specific version:

```text
looks toward user
→ tiny head raise
→ one ear forward
→ one forehoof slowly emerges / offers low
→ WAIT
→ soft reciprocal contact
→ tiny eyelid/cheek response
→ head softens
→ local fleece settles
```

### 18.7 Boundary escalation grammar

Carol should communicate limits gently rather than using Eevee’s exact protest face/VFX. **[G]**

```text
Level 0: local acknowledgement
Level 1: gentle boundary hint
Level 2: clear refusal / small movement away
Level 3: withdrawal / gaze disengagement
Recovery: quiet stillness → eyes soften → head/ear return → mild boundary afterglow
```

A prior initial envelope proposed:

- local physical acknowledgement 0–80 ms,
- face/eyelid 50–180 ms,
- head-away 120–350 ms,
- ear response 200–500 ms,
- body transfer 300–800 ms,
- fleece follow-through 450–1200 ms,
- release settle 0.5–1.5 s,
- mild boundary afterglow 2–5 s.

Again, **[G]**, not Pokémon measured timing.

### 18.8 Carol mood phrase

Do not copy Eevee’s ear-dance. **[G]** Carol’s state-expression phrase should be low-energy and bounded:

```text
one ear / eye acknowledgement
→ tiny head lean
→ eyes soften/close
→ grounded weight transfer
→ local fleece follows
→ second softer sway
→ tiny hoof adjustment
→ fleece settles
→ eyes reopen
→ quiet living idle
```

### 18.9 Carol delayed affection

Use the principle from E02 rather than copying the heart reaction:

```text
interaction ends
→ Carol settles
→ brief quiet
→ she looks back / softens
→ both ears relax
→ grounded body subtly commits toward user
→ fleece settles
→ optional restrained moon/star accent
```

### 18.10 Carol DO NOT

- no whole-fleece sinusoidal bounce,
- no both-ears-always-synchronous motion,
- no body bob on every blink,
- no constant moon/star sparkle,
- no instant full-body happy clip for every touch,
- no immediate neutral snap after every reaction,
- no centered bilateral response that ignores left/right touch,
- no periodic “do an idle every N seconds” scheduler.

---

## 19. Jill Implications

Jill is attention-seeking + energetic; motion lead is chest / upper body, propagating toward wings, leaves/flowers, and a heavy rooted tail.

### 19.1 Living/mood phrase

**[G]**

```text
chest lift / upper-body intent
→ eyes
→ one wing
→ opposite wing
→ optional foreleg accent
→ leaves/flowers follow
→ heavy tail last
→ settle
```

Tail should not hit every beat.

### 19.2 Positive touch

```text
local acknowledgement
→ chest/upper-body commit
→ head/face
→ one wing response
→ leaf/flower delayed follow-through
→ heavy tail later if intensity justifies it
```

### 19.3 Reciprocal invitation

Higher energy than Carol:

```text
chest forward
→ one foreleg / wing invitation
→ shorter wait tendency
→ fast face success
→ wing follow-through
→ leaves lag
```

### 19.4 Boundary / withdrawal

```text
local acknowledgement
→ chest recoil
→ face
→ one wing opens defensively
→ head away
→ leaves follow
→ heavy tail much later
```

No aggressive punishment loop.

### 19.5 Anti-copy rule

Do not retarget Eevee’s ear-led rhythm or paw-high-five literally. Jill’s emotion should originate from chest/upper-body identity.

---

## 20. Pino Implications

Pino is energetic + independent with a soft water-bag-like body, arms as a major expressive channel, and a heavy delayed tail.

### 20.1 Living/mood phrase

**[G]**

```text
soft torso sway
→ arms inward/outward
→ face
→ second body accent
→ heavy tail catches up later
```

### 20.2 Positive touch / contact seeking

```text
cheek/body contact
→ local squish acknowledgement
→ head/body softly move toward contact
→ arms pull inward / hug tendency
→ soft rebound
→ heavy tail follows last
```

### 20.3 Reciprocal invitation

Because Pino is more independent, invitation frequency can be lower:

```text
glance
→ one paw offered
→ brief look-away possible
→ user responds
→ body squish / arms pull in
→ tail responds late
```

### 20.4 Boundary

```text
contact acknowledgement
→ eyes glance
→ body subtly pulls away
→ arms inward/protective
→ gaze breaks
→ heavy tail drags after body
```

### 20.5 Feeding

The observed Eevee “consume → short processing pause → delight” principle maps well to Pino. Do not make water/bubble motifs the primary source of emotion; use them only after body/face acting reads.

---

## 21. Shushu Implications

Shushu is relaxed + independent, plush, grounded, with ears, flowers, a crown/bouquet relationship, and delayed plush settle.

### 21.1 Living/mood phrase

**[G]**

```text
head
→ one ear
→ eyelid
→ plush torso settle
→ bouquet small movement
→ flower crown delayed bounce
→ quiet return
```

### 21.2 Positive touch / contact seeking

```text
cheek pet
→ eyelid softens
→ head sinks into contact
→ plush torso slightly compresses
→ one ear relaxes
→ crown/flowers follow later
```

Maintain convincing bouquet-hand relationship.

### 21.3 Reciprocal invitation

```text
head tilt
→ free hand raises slightly
→ plush palm offered
→ long patient wait
→ contact
→ tiny eye close
→ plush torso compression
→ flowers follow later
```

### 21.4 Boundary

```text
eyes down/soften
→ head turns away
→ one ear lowers
→ plush torso compresses/retreats
→ bouquet remains protected
→ flowers settle later
```

No guilt-inducing sadness or aggressive punishment.

---

## 22. Runtime Requirements Derived from Video

Only requirements supported by the analyzed footage and prior derived analyses are included here.

### 22.1 Independent animation channels

At minimum the runtime needs independently composable controls for:

- root / COM,
- torso/chest,
- neck/head,
- eye aim,
- eyelid L/R,
- mouth/muzzle,
- ear L/R,
- forelimb L/R,
- hindlimb support,
- tail,
- character-specific secondary structures,
- local touch response,
- expression,
- afterglow,
- audio/VFX cues.

### 22.2 Masked / additive layer composition

Required because many behaviors act on only a subset of channels while the rest of the body maintains the current state. **[G]**

### 22.3 Semantic touch zones

Runtime must preserve semantic zone and local contact information rather than reducing all contact to “character touched.” **[G]**

Useful fields derived from the analyses:

```text
zone
contactSide
localPosition
surfaceAnchor
localNormal
contactDuration
pathLength
speed
reversalCount
zoneContinuity
recentContactPressure
```

### 22.4 Gesture accumulator

Needed to distinguish discrete tap/high-five from slow stroke and prolonged/repeated disliked contact. **[G]**

### 22.5 Immediate local reflex path

The reference often has strong semantic facial response but comparatively weak local physical deformation. Grimo should preserve a fast local response path before higher-level behavior resolution. **[G]**

### 22.6 Interaction-class latency policy

At least the following classes are justified:

```text
LOCAL_REFLEX
SOCIAL_RECIPROCAL
STROKE_ACCUMULATION
FEEDING
LARGE_REACTION
```

High-five evidence supports very fast reciprocal ACK; slow pet and feeding support slower semantic interpretation.

### 22.7 Reciprocal Interaction Controller

State structure:

```text
IDLE
→ INVITATION_ANTICIPATE
→ INVITATION_PRESENT
→ WAIT_FOR_USER
├─ success
├─ timeout
├─ interruption
└─ cancel
```

Success path:

```text
CONTACT_ACK
→ MICRO_SUCCESS
→ SETTLE
→ next invitation / idle / delayed larger affect
```

### 22.8 Boundary Pressure / Negative State Controller

Maintain contact context across time:

```text
contactDuration
recentContactDuration
repeatCount
strokeSpeed
reversalCount
timeSinceLastDislike
boundaryPressure
```

At minimum distinguish:

```text
DISCOMFORT_HINT
CLEAR_PROTEST
WITHDRAWAL
RECOVERY
```

### 22.9 Hysteresis

Once the character becomes uncomfortable, a tiny pointer move should not instantly flip to happy. Enter/exit thresholds should differ. **[G]**

### 22.10 Contact-Seeking Controller

State model:

```text
CONTACT
→ STROKE_ACCUMULATION
→ ACCEPTANCE
→ CONTACT_SEEK
→ CONTACT_HOLD
→ REBOUND / SETTLE
→ AFTERGLOW
```

Contact anchors must follow character deformation so the character can move into contact without losing semantic touch state.

### 22.11 Side-conditioned pose composition

Pass contact side and local position through macro reactions. **[G]** This directly addresses E05’s visible centered-response weakness.

### 22.12 Mood Phrase Controller

State/context can trigger a bounded phrase:

```text
Mood / Context
→ Phrase Candidate Selector
→ Anticipation
→ Subphrase A
→ Moving Hold / Reset
→ Subphrase B / Accent
→ Settle
→ Living Idle
```

Mood phrase is not a looping oscillator.

### 22.13 Channel ownership / locks

During an authored phrase, unrelated random idle schedulers must not inject ear twitch/head turn/paw actions that destroy the acting. **[G]**

### 22.14 Emotional afterglow

Reaction completion should update a short-lived state that affects expression, gaze, posture, and next behavior selection. **[G]**

### 22.15 Recent behavior history / cooldown / similarity groups

Required to avoid the repeated reaction-family weakness visible in the footage. **[G]**

Suggested runtime data:

```text
lastUsedAt
recentUseCount
similarityGroup
cooldown
recentReactionFamily
recentAutonomousPhraseFamily
```

### 22.16 Delayed event scheduler

Needed for interaction → settle → delayed character-originated response, as seen in E02’s post-high-five major affect. **[G]**

### 22.17 Attention controller

Must allow state-driven targets such as:

```text
PROTEST    → user
WITHDRAWAL → away / floor / environment
INVITATION → user
RELAXED    → soft/closed or intermittent
```

### 22.18 Intentional stillness candidate

Scheduler must explicitly allow no major action; otherwise every idle becomes over-animated. **[G]**

### 22.19 Interruptibility

Long relaxed hold, invitation wait, contact-seeking hold, and boundary states all need interruption paths from their current pose, not forced completion to neutral first. **[G]**

### 22.20 Per-character timing and channel grammar

Shared runtime does not imply shared performance. Each Grimo needs its own lead channels, response amplitude, wait tendency, settle duration, and secondary delay.

---

## 23. Motion / Behavior Production Backlog

The following consolidates the P0/P1/P2 items repeatedly derived during the five-video analysis, with **Carol vertical slice** as the primary production target.

### P0 — Carol Vertical Slice Critical

1. **Living neutral base** — grounded hooves, stable root, tiny physiology, no whole-fleece bob.
2. **Independent eyelid / gaze / ears** — L/R ears independently addressable.
3. **Intentional stillness / long relaxed moving hold** — ~10–25 s-class behavior can remain alive without major action.
4. **Immediate local touch reflex** — cheek/head/fleece local acknowledgement before full semantic reaction.
5. **Slow-pet accumulator** — distinguish ongoing stroke from tap.
6. **Side-specific cheek contact-seeking lean** — left/right causality preserved.
7. **Contact hold** — character can remain leaned into touch.
8. **Interrupted contact-seeking recovery** — finger release redirects current pose; do not blindly finish a clip.
9. **Head/cheek pet positive causal stack** — local → face → head → ear → grounded body → fleece → afterglow.
10. **Boundary hint** — mild “not there” response without hostility.
11. **Clear refusal** — user-facing communication.
12. **Withdrawal / disengagement** — gaze away/down, distance creation, low-energy retreat.
13. **Boundary hysteresis / pressure accumulator** — repeated unwanted input changes state over time.
14. **Negative recovery / afterglow** — do not snap immediately to affectionate neutral.
15. **Reciprocal soft invitation** — Carol initiates a social contact opportunity.
16. **Invitation WAIT state** — animation pauses for user response while micro channels remain alive.
17. **Fast reciprocal contact ACK** — immediate local/face confirmation for discrete social success.
18. **Repeated reciprocal loop** — can transition directly into another social turn without neutral reset.
19. **Delayed affection payoff** — larger character-originated response after interaction settles.
20. **Carol-specific bounded mood phrase** — low-energy self-expression with unequal accents and a clear end.
21. **Phrase channel-lock / ownership** — random idle layers cannot corrupt authored acting.
22. **Local → global fleece follow-through** — cause-driven, delayed, low amplitude; no whole-fleece jelly.
23. **Settle → living idle transition** — every hero reaction exits into a plausible current state.
24. **Afterglow state** — positive and negative residue affects next few seconds.

### P1 — Variation / Coverage Expansion

- positive pet family 3–5 variants,
- boundary hint/refusal 3+ variants,
- withdrawal 2–3 variants,
- left/right cheek variants,
- shallow/medium/deep contact lean,
- eyes-open / eyes-closed contact-seeking variants,
- ear-side timing variants,
- small rebound variants,
- gaze-at-user / gaze-away variants,
- one-ear attention actions,
- autonomous head/ear curiosities,
- mood phrase A/B/C,
- two-accent phrase variation,
- tiny hoof accent variants,
- invitation wait-pose variants,
- successful reciprocal contact face variants,
- ignored/late invitation handling,
- invitation cancellation,
- user-stops-early soft recovery,
- feeding staged consumption,
- feeding emotional timing variants,
- reaction-family repetition suppression,
- phrase cooldown / recent-family suppression,
- character-specific short vocal palette integration,
- fleece cluster delay tuning,
- local protective hoof/head action,
- side-conditioned macro reaction blending.

### P2 — Long-Term Richness

- rare moon/star behavior,
- gift/item interaction,
- self-groom,
- rare larger Carol rhythm behavior,
- bond-dependent invitation strength,
- bond-dependent stronger cheek lean,
- remembered preferred touch tendencies,
- context-dependent sensitive zones,
- rare humorous boundary behavior,
- task-completion comfort response,
- session-entry recognition behavior,
- sleeping contact-seeking variant,
- toys / item-mediated social ritual,
- long-term remembered interaction,
- seasonal/contextual mini rituals,
- four-character-specific reciprocal interaction libraries.

---

## 24. Quantitative Observations

These are the measurements already obtained in the chat. Values marked approximate are frame-derived approximations, not internal game timings.

| Observation | Value | Video | Evidence |
|---|---:|---|---|
| frame duration | **33.3 ms** | all | 30 fps metadata **[V1]** |
| E01 visible neutral blink | **~4 frames ≈133 ms** | E01 | 200.567–200.700 s **[V1, n=1]** |
| E01 full eyelid closure in that blink | **~2 frames ≈67 ms** | E01 | 200.600–200.633 s **[V1, n=1]** |
| E01 first visible hand/contact → clear pleasure face | **~1.53 s** | E01 | 09.833 → 11.367 s **[V1]**; includes gesture accumulation, not input latency |
| E01 negative face onset → major ear peak | **~1.1–1.2 s** | E01 | 55.80 → ~56.97 s **[V1/V2]** |
| E01 feeding consume → delight | **~0.8–0.9 s** | E01 | ~77.63 → ~78.5; ~84.6 → ~85.4 **[V1/V2]** |
| E01 long relaxed moving hold | **~20+ s** | E01 | ~128.9 → 150+ s **[V1]** |
| E02 high-five contact → clear happy face | **~2 frames ≈67 ms** | E02 | 34.400 → ~34.467; similar repeats **[V1]** |
| E02 observed paw-presentation waiting | **~0.8–1.7 s range** | E02 | varies across cycles **[V1/V2]** |
| E02 final high-five → delayed major affect | **~0.8–0.9 s** | E02 | ~42.50 → ~43.37 s **[V1/V2]** |
| E02 feeding consume → delight | **~0.8 s** | E02 | ~97.8 → ~98.6 s **[V1/V2]** |
| E03 sharp protest duration | **~1.4–1.5 s** | E03 | ~9.667→11.1; ~14.33→15.73 **[V1]** |
| E03 withdrawal duration | **~1.5 s** | E03 | ~20.80→22.33; ~39.70→41.23 **[V1]** |
| E04 “ノリノリ” bounded phrase | **~3.0 s** | E04 | ~0.6→3.5 s **[V1]** |
| E04 eyelid → clear ear lowering delay in relaxed state | **~4–6 frames ≈130–200 ms** | E04 | ~152.93→153.07/153.13 **[V1/V2]** |
| E05 ear lead before clear eyelid/head commitment | **~1 frame ≈33 ms** | E05 | ~20.12→20.15 s **[V1/V2]** |
| E05 cheek macro response total | **~2.4–2.5 s** | E05 | ~20.12→22.5/22.6 s **[V1]** |
| E05 deep contact hold | **~0.4–0.7 s** | E05 | ~20.2–20.88 s **[V1]** |
| E05 second content hold | **~1.1 s** | E05 | ~21.28–22.4 s **[V1]** |

### Not quantitatively established

- exact joint angles,
- exact pupil saccade duration,
- stable blink interval distribution,
- breathing cycle,
- exact tail delay,
- exact fur secondary delay,
- exact touch pressure / cursor velocity,
- exact internal trigger thresholds.

---

## 25. Open Questions / Missing Evidence

There are **36 unresolved evidence items** in the consolidated corpus:

1. **Partner Pikachu motion corpus is absent.** Need matched Pikachu Partner Play videos covering idle, positive touch, negative touch, high-five/social invitation, feeding, and autonomous behavior.
2. Exact internal touch/contact trigger frame relative to the visible cursor/hand is unknown.
3. Exact semantic touch-zone boundaries are unknown.
4. Cursor/finger trajectory data used internally by the game is unknown.
5. Gesture-speed thresholds for tap vs stroke vs rub are unknown.
6. Whether slow-pet major reactions use a duration/path threshold, accumulated affection, or another selector is unknown.
7. The internal reaction-selection algorithm is unknown.
8. Current friendship/affection level’s effect on the observed timings and variants is unknown.
9. The rule selecting sharp protest vs withdrawal is unknown.
10. Whether an explicit internal “boundary pressure” accumulator exists is unknown.
11. Animation clip identity cannot be proven; visually near-identical reactions may still be separate assets.
12. Whether observed behavior is composed from additive/masked layers or one baked full-body clip is unknown.
13. Ear motion implementation (hand-authored, procedural, physics, hybrid) is unknown.
14. Tail motion implementation is unknown.
15. Independent neck-fur/body-fur dynamics are not clearly observable.
16. Exact gaze target and eye-aim system are unknown.
17. Fine eye-only saccade behavior is insufficiently resolved in this corpus.
18. Whether contact side is internally used even when the final macro clip appears centered is unknown.
19. High-five timeout behavior when the player never responds is missing; need a no-response capture.
20. Conditions required for high-five invitation are unknown; need controlled captures across different relationship/context states.
21. Left/right paw invitation variations are unconfirmed; need repeated high-five captures from multiple sessions.
22. Exact trigger for the delayed major affection reaction after repeated high-fives is unknown.
23. Gift event trigger/eligibility conditions are unknown.
24. Exact trigger for the “ノリノリ” mood phrase is unknown.
25. Number and probability of “ノリノリ” phrase variations are unknown; need repeated re-entry captures in the same mood state.
26. Whether the rhythmic phrase is synchronized to music/beat at runtime is unknown.
27. Exact semantic identity of analyzed audio transients (vocal/contact/UI/BGM) is unknown.
28. Audio source separation was not performed; vocal onset cannot be isolated reliably.
29. Cheek/contact-seeking interrupt behavior when the finger is removed mid-response is unknown; need a controlled early-release video.
30. Whether semantic contact remains continuously active while Eevee moves into the touch is unknown.
31. Collision/hit-volume implementation is unknown.
32. Whether bond/friendship changes invitation wait duration, face, afterglow, or contact-seeking depth is unknown.
33. Idle scheduler logic—random timer, stateful utility, authored sequence, or hybrid—is unknown.
34. Feeding “processing pause” may represent chew, animation staging, audio sync, or another state; internal meaning is unknown.
35. Trigger/selection rule for autonomous paw action is unknown.
36. Internal semantic identity of the long relaxed moving-hold state (sleepy, content, idle variant, etc.) is unknown.

### Highest-value additional videos

If more footage is added later, the most useful evidence would be:

- matched **Partner Pikachu** versions of the same interaction families,
- Eevee high-five with **no player response** until timeout,
- Eevee cheek pet with **controlled left vs right** identical gestures,
- cheek pet where the finger is **removed mid-contact-seeking reaction**,
- repeated “ノリノリ” entries to test phrase variation,
- long no-input idle captures (2–5 minutes) to estimate autonomous-action distribution,
- controlled repeated identical gesture captures to separate deterministic causality from performance variation,
- close-up footage where pupils/eyes are large enough to evaluate eye-only gaze.

---

## 26. Final Character Motion Rules

### DO

- **DO** allow long quiet states and moving holds.
- **DO** author behavior-specific causal order instead of one universal eyes→head→body rule.
- **DO** let only the necessary channels participate in each action.
- **DO** let facial meaning precede body peak when the behavior calls for evaluation.
- **DO** preserve character initiative: invitation, waiting, autonomous phrase, gift-like behavior.
- **DO** separate protest from withdrawal/disengagement.
- **DO** use gaze/attention as part of social meaning.
- **DO** let accepted contact become character-driven contact-seeking where appropriate.
- **DO** reserve larger appendage/body/VFX recruitment for larger affect.
- **DO** track recent reaction families and suppress obvious repetition.
- **DO** preserve left/right contact information into macro pose composition.
- **DO** keep settle and afterglow as meaningful states, not dead tails of clips.

### DO NOT

- **DO NOT** animate every body part continuously.
- **DO NOT** make every positive event a full-body bounce.
- **DO NOT** make tail wag a universal happiness channel.
- **DO NOT** run fixed-period blink/ear/tail/head oscillators as “life.”
- **DO NOT** make all interactions share the same reaction latency.
- **DO NOT** use one `ANGRY` animation for every disliked touch.
- **DO NOT** force every reaction through neutral before the next state.
- **DO NOT** restart the same negative clip repeatedly while contact continues.
- **DO NOT** discard touch side once a macro reaction starts.
- **DO NOT** let VFX substitute for body acting.
- **DO NOT** retarget Eevee’s species-specific paw/ear/face performance directly to Carol, Jill, Pino, or Shushu.

### Core Motion Rules

1. **Stable support, selective action.** Root/COM should remain grounded unless the behavior meaning requires commitment.
2. **Phase relationships are authored.** Delay must communicate cause, not random noise.
3. **Bounded phrases beat loops.** A mood has episodes of expression, not permanent oscillation.
4. **Moving hold is a first-class animation concept.** Hold states carry emotion and weight.
5. **Peak does not end the event.** Settle and afterglow are part of the performance.
6. **Stronger affect recruits more channels.** Small events should leave expressive headroom.
7. **Asymmetry is semantic.** One ear/paw/side can lead; symmetry is reserved for selected peaks.

### Core Interaction Rules

1. **Interaction type determines timing.** Tap/high-five/stroke/feeding/boundary have different temporal grammars.
2. **Touch is semantic and spatial.** Preserve zone, side, local position, trajectory, duration, and repetition history.
3. **Character may act back into contact.** Accepted touch can become contact-seeking.
4. **Reciprocal interactions require waiting.** Character-initiated invitations are state machines, not fixed-duration clips.
5. **Boundaries persist.** Continued unwanted input changes the ongoing state rather than producing one isolated protest.
6. **Interrupt from the current pose.** Do not finish a canned clip after the user has changed the situation.
7. **Deterministic causality + stochastic performance variation.** The user should understand why the reaction happened without seeing the same performance every time.

### Core Attention Rules

1. Do not stare at the user continuously.
2. Protest may remain user-facing; withdrawal should be able to break gaze.
3. Invitation can be communicated through body presentation while gaze stays on the user.
4. Fine cursor tracking is not required for every interaction; use it only when it strengthens causality.
5. Eyes can close to signal accepted contact/internal enjoyment, then reopen to re-establish external attention.
6. Attention target is part of behavior state, not a permanently active look-at solver.

### Core Emotion Rules

1. Positive emotion is a **curve**, not a binary preset.
2. Negative emotion has multiple strategies: hint, protest, withdrawal, recovery.
3. Emotional residue must survive the action peak.
4. Mood changes probability and phrase choice; it does not force continuous high-amplitude motion.
5. Rare large affect should feel discovered/earned because small events are visually restrained.
6. Character agency requires the ability to want, wait, accept, refuse, disengage, and re-engage.

---

## Closing Production Interpretation

Across these five Partner Eevee videos, the strongest reusable conclusion is not “Eevee has cute ears and many animations.” The observable system behaves more like a set of **time-structured social performances**:

```text
state exists
→ attention changes
→ one channel notices first
→ the character evaluates
→ only the necessary body parts commit
→ the action may wait for the user
→ the user may alter the character’s state
→ the character may alter the physical relationship back
→ the body settles
→ emotion remains for a while
→ quiet life resumes
```

For Grimo, the target is therefore not to copy Eevee’s animations. The target is to build a runtime and production language capable of producing the same *class of causal richness* with Carol-, Jill-, Pino-, and Shushu-specific anatomy, personality, timing, and motion identity.
