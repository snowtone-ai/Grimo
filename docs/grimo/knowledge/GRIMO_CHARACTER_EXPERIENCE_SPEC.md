# Grimo — Character Experience Specification

**Status:** Highest durable character-experience authority  
**Updated:** 2026-09-23  
**Scope:** Carol / Jill / Pino / Shushu motion, attention, interaction, behavior and Human experience gates

> Grimo is not a character that merely moves a lot. It is a companion whose attention, intent, bodily causality, emotion, afterglow and agency make it feel present.

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

Major failure factors include generic motion, latency, obvious repetition, off-model deformation, floaty/root-dominant motion, VFX dependence and personality retargeting.

## 2. Core terminology

- **Living idle:** no user input, but internal state, attention, tiny behavior and intentional stillness remain readable.
- **Moving hold:** pose/emotion is held while only small physiological/attention/secondary channels continue.
- **Afterglow:** emotion, gaze, posture and next-action probability persist after the primary action ends.
- **Local acknowledgement:** contacted region visibly receives input before larger body reaction.
- **Behavior family:** reactions with the same semantic purpose.
- **Performance variant:** timing/side/face/appendage/settle variation while preserving the same meaning.
- **Intentional stillness:** explicitly valid living behavior, not scheduler failure.
- **Identity envelope:** allowed facial, gaze, deformation and pose range that preserves canonical identity.

## 3. Motion philosophy

### Cause before motion
Every meaningful motion should have a cause: user input, attention change, internal state, reciprocal intention or authored self-initiative.

### Local before global when touch supplies the cause
Touch should normally read as local acknowledgement first, then face/head/body/secondary propagation when appropriate.

### Correlated asynchrony
Life comes from selective, asynchronous channel ownership, not random desynchronization and not full-body animation on every event.

### Intentional stillness
Long quiet holds are valid. Constant oscillation is prohibited as a substitute for life.

### Grounded weight
The support base and center-of-mass read must make actions feel physically owned rather than floating.

### Temporal phrase
Use anticipation, action, follow-through, settle and afterglow as an authored temporal curve rather than snapping into one expression/pose.

### Context sensitivity
Reaction depends on contact zone, side, gesture, duration, speed, current state, recent history and interruption context.

### Repetition suppression
Variation is required at both behavior-family selection and performance execution level. Deterministic causality and stochastic variation are separate concerns.

## 4. Attention and gaze

The character should support:

- natural blinking;
- eye aim / gaze changes;
- attention toward interaction;
- looking away / environmental attention;
- coordinated head/eye behavior;
- expression changes without visible snapping;
- attention persistence before and after user input.

The character must not stare directly at the user continuously.

## 5. Touch grammar

Runtime input should preserve at least:

- semantic zone;
- left/right side;
- gesture class;
- speed;
- duration;
- direction/history where relevant.

A typical positive chain is:

```text
touch
→ immediate local ACK
→ facial evaluation
→ head/upper-body commitment
→ optional contact-seeking lean
→ secondary follow-through
→ settle
→ positive afterglow
```

Contact seeking is bidirectional: the companion may actively move the contacted body region toward accepted contact.

Boundary grammar is characterful and non-hostile:

```text
hint → mild refusal → withdrawal → recovery
```

## 6. Agency and autonomy

Required autonomous families include quiet living state, attention shifts, self-grooming/self-expression, environment/user checking, affection invitation, WAIT state, recovery/settle and rare signature behavior.

Character → User interaction is a first-class pattern:

```text
character initiates
→ presents intention/body part
→ holds / waits
→ user reciprocates
→ immediate acknowledgement
→ shared emotional payoff
```

WAIT must feel alive without constant body motion.

## 7. Emotion and continuity

Emotion is a persistent state, not a one-frame preset. Stronger emotions may recruit progressively more channels. Small reactions should not spend face + ears + limbs + torso + tail/fleece + VFX all at once.

New user input must be able to interrupt/redirection current behavior without mandatory finish-to-neutral or clip queue spam.

## 8. Secondary motion

Secondary systems reinforce primary acting; they do not create the action's meaning.

Primary motion must be readable with sound/VFX/secondary motion disabled. Secondary structures should lag, overshoot or settle only within character-specific limits.

## 9. Character-specific signatures

### Carol — attention-seeking + relaxed
- grounded, reassuring, soft timing;
- very short limbs and heavy hooves preserve low support;
- face/eyes/ears carry subtle attention;
- cheek/head contact seeking is central;
- dream-cloud fleece is a dominant identity system and follows authored primary movement with restrained delayed softness;
- avoid jelly-like global fleece motion.

### Jill — attention-seeking + energetic
- emotion tends to begin chest/upper body then recruit wings/tail/leaves;
- tail remains rooted/heavy;
- leaves/flowers follow with delay;
- avoid generic fast-dragon motion and overly long forelimbs.

### Pino — energetic + independent
- soft rounded body, inward hugging arm tendency;
- buoyant but grounded, not hollow-balloon;
- tail follows with delay;
- water/bubbles are accents, not constant activity.

### Shushu — relaxed + independent
- grounded seated/plush weight;
- soft delayed compression and settle;
- small ear bounce;
- crown/bouquet attachment must remain believable.

Shared runtime semantics are allowed. Direct sharing of signature performance, identical invitation poses, identical gaze distributions or identical settle timing is not.

## 10. Carol Minimum Experience Set

Coverage, not animation count, is authoritative.

P0 Carol must eventually prove:

- canonical-faithful neutral identity;
- 15–30 s living idle with multiple asynchronous micro-event combinations;
- head + cheek touch causality, left/right aware;
- distinct tap vs slow pet vs continuous/back-and-forth outcomes where applicable;
- contact-seeking lean;
- self-initiated affection invitation + WAIT;
- mild boundary / withdrawal + recovery;
- one larger affection/delight phrase with anticipation, peak, settle and afterglow;
- interruption in representative scenarios;
- history-aware repetition suppression;
- smartphone runtime feasibility.

These are **acceptance scenes**, not a mandatory sequential production waterfall.

## 11. Human Experience Gates

### Identity Gate
Unmistakably Carol; canonical appeal preserved in the actual presentation envelope.

### Living Idle Gate
15–30 s feels alive while allowing genuine quiet and selective channel activity.

### Touch Causality Gate
The viewer can read where contact occurred, how response propagated and how the body settled.

### Agency Gate
Character-initiated invitation and WAIT read as intention rather than a looping clip.

### Hero Acting Gate
A larger emotional phrase reads professionally with sound/VFX disabled.

### Interruption Gate
New input redirects behavior without snap, queue spam or forced neutral.

### Repetition Gate
Repeated interaction does not expose obvious identical-run or same-family spam.

### Runtime Experience Gate
The approved experience survives export/runtime/device constraints.

### Companion Gate
Several minutes sustain identity, agency, responsiveness, variation, continuity and character specificity without feeling like a technical demo or canned puppet.

## 12. Failure diagnosis priorities

When something feels wrong, diagnose in this order:

1. identity / appeal;
2. causality / attention;
3. weight / support;
4. temporal phrase / settle / afterglow;
5. repetition / state continuity;
6. deformation or visual artifact causing the above;
7. technical implementation details only insofar as they cause user-visible or functional failure.
