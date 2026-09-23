# Grimo — Character Experience Specification

**Status:** Highest durable character-experience authority  
**Updated:** 2026-09-23  
**Scope:** Carol / Jill / Pino / Shushu motion, attention, interaction, behavior and Human experience gates

> Grimo is not a character that merely moves a lot. It is a companion whose
> attention, intent, bodily causality, emotion, afterglow and agency make it feel
> present.

## 1. Experience quality model

Living Companion Quality is approximately multiplicative across:

```text
Identity Fidelity
× Causal Responsiveness
× Attention / Intent Readability
× Temporal Layering
× Agency
× Behavioral Variability
× Continuity of Internal State
× Character Specificity
```

Major failure factors include generic motion, latency, obvious repetition,
off-model deformation, floaty/root-dominant motion, VFX dependence, and
personality retargeting.

## 2. Core terminology

- **Living idle:** internal state/attention/tiny behavior remain readable without
  user input.
- **Moving hold:** pose/emotion holds while only small channels continue.
- **Afterglow:** emotion/gaze/posture/next-action probability persist after the
  main action.
- **Local acknowledgement:** contacted region visibly receives input before
  larger propagation.
- **Behavior family:** reactions sharing semantic purpose.
- **Performance variant:** timing/side/face/appendage/settle variation that
  preserves meaning.
- **Intentional stillness:** valid living behavior, not scheduler failure.
- **Identity envelope:** allowed expression/deformation/pose range preserving
  canonical identity.

## 3. Motion philosophy

- **Cause before motion.** Motion should arise from user input, attention,
  internal state, reciprocal intention, or self-initiative.
- **Local before global for touch.** Contact normally acknowledges locally
  before larger body response.
- **Correlated asynchrony.** Life comes from selective asynchronous channel
  ownership, not random desynchronization or full-body animation on every event.
- **Intentional stillness.** Constant oscillation is prohibited as a substitute
  for life.
- **Grounded weight.** Support/COM must make actions feel physically owned.
- **Temporal phrase.** Anticipation → action → follow-through → settle →
  afterglow.
- **Context sensitivity.** Zone, side, gesture, duration, speed, current state,
  recent history, and interruption context matter.
- **Repetition suppression.** Variation exists both at behavior-family and
  performance-execution levels.

## 4. Attention / gaze

Support natural blinking, gaze changes, attention toward interaction,
environmental looking-away, coordinated head/eye behavior, smooth expression
changes, and attention persistence. The character must not stare continuously.

## 5. Touch grammar

Runtime input should preserve semantic zone, left/right side, gesture class,
speed, duration, and relevant direction/history.

Typical positive chain:

```text
touch
→ immediate local ACK
→ facial evaluation
→ head / upper-body commitment
→ optional contact-seeking lean
→ secondary follow-through
→ settle
→ positive afterglow
```

Contact seeking may be bidirectional: the companion can move the contacted region
toward accepted contact.

Boundary grammar is non-hostile:

```text
hint → mild refusal → withdrawal → recovery
```

## 6. Agency / autonomy

Required autonomous families include quiet living state, attention shifts,
self-expression/grooming, environment/user checking, affection invitation,
WAIT, recovery/settle, and rare signature behavior.

Character → User interaction is first-class:

```text
character initiates
→ presents intention/body part
→ holds / waits
→ user reciprocates
→ immediate acknowledgement
→ shared emotional payoff
```

WAIT must feel alive without constant body motion.

## 7. Emotion / interruption

Emotion persists beyond a single-frame preset. Stronger emotion may recruit more
channels; small reactions should not spend every channel at once.

New input must be able to interrupt/redirect current behavior without mandatory
finish-to-neutral or clip queue spam.

## 8. Secondary motion

Secondary systems reinforce primary acting; they do not create its meaning.
Primary motion must read with sound/VFX/secondary motion disabled. Secondary
structures may lag/overshoot/settle only inside character-specific limits.

## 9. Character signatures

### Carol — attention-seeking + relaxed
Grounded, reassuring, soft timing; short limbs/heavy hooves; face/eyes/ears carry
subtle attention; cheek/head contact seeking is central; dream-cloud fleece is a
dominant identity system with restrained delayed softness; avoid jelly-like
global fleece motion.

### Jill — attention-seeking + energetic
Emotion tends to begin chest/upper body then recruit wings/tail/leaves; rooted,
heavy tail; delayed leaves/flowers.

### Pino — energetic + independent
Soft rounded body, inward arm tendency, buoyant but grounded; thick tail follows
with delay; water/bubbles are accents.

### Shushu — relaxed + independent
Grounded plush weight, delayed compression/settle, small ear bounce, believable
crown/bouquet attachment.

Share runtime semantics, not signature performance.

## 10. Carol Minimum Experience Set

P0 Carol must eventually prove: canonical-faithful neutral identity; 15–30 s
living idle; left/right-aware head + cheek touch causality; distinct touch
outcomes; contact-seeking lean; self-initiated invitation + WAIT; mild
boundary/withdrawal + recovery; one larger emotional phrase; representative
interruption; history-aware repetition suppression; smartphone runtime
feasibility.

These are **acceptance scenes, not a mandatory sequential production
waterfall**.

## 11. Human Experience Gates

- **Identity Gate:** unmistakably Carol; canonical appeal preserved.
- **Living Idle Gate:** 15–30 s feels alive while allowing genuine quiet.
- **Touch Causality Gate:** contact location, propagation, and settle are readable.
- **Agency Gate:** invitation + WAIT read as intention, not loop.
- **Hero Acting Gate:** larger phrase reads professionally without VFX/sound.
- **Interruption Gate:** new input redirects without snap/queue spam/forced neutral.
- **Repetition Gate:** repeated interaction avoids obvious identical/family spam.
- **Runtime Experience Gate:** approved experience survives export/runtime/device.
- **Companion Gate:** several minutes sustain identity, agency, responsiveness,
  variation, continuity, and character specificity without canned-puppet feel.

## 12. Failure diagnosis priority

Diagnose in this order:

1. identity / appeal
2. causality / attention
3. weight / support
4. temporal phrase / settle / afterglow
5. repetition / state continuity
6. deformation or visual artifact causing the above
7. technical implementation details only insofar as they cause user-visible or
   functional failure
