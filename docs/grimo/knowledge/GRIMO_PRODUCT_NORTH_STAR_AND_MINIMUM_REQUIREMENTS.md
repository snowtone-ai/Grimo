# Grimo — Product North Star and Minimum Requirements

**Status:** Highest durable product / quality authority  
**Updated:** 2026-09-23  
**Scope:** Carol / Jill / Pino / Shushu; technology-independent product requirements

## 1. Product North Star

Grimo is a smartphone-first task-management product whose emotional center is
its companion creatures. The Goal is **not** to produce a technically perfect
3D model.

> The user should want to meet and interact with a Grimo strongly enough that
> completing tasks naturally becomes a reason to return to the companion
> experience.

On the Grimo screen, Carol / Jill / Pino / Shushu must feel cute, alive, aware
of the user, causally responsive, capable of initiating interaction, and like
companions rather than canned puppets even across extended use.

Experience priority:

1. **Cuteness / appeal**
2. **Healing / comfort**
3. **Attachment**
4. **Fun**
5. **Surprise**
6. **Collection**

Typical interaction sessions are approximately **30 seconds to 5 minutes**.

## 2. Quality benchmark

Partner Pikachu / Partner Eevee are references for interaction quality and sense
of life, not for copying assets or proving 3D purity.

The abstract benchmark is: life without user input; readable attention/intent;
expressive face/body/appendages; local touch causality; anticipation,
follow-through, settle and afterglow; self-initiated reciprocal behavior;
interruptibility; variation/repetition suppression; and character-specific
motion.

## 3. Non-negotiable animation rule

A completed single illustration must never be treated as one rigid object and
globally translated, rotated, scaled, stretched, squashed, warped, or bounced to
simulate life.

Meaningful regions, facial components, appendages, and expressive secondary
structures must be independently controllable. Local 2D, material, shader,
morph, or compositing techniques are allowed when they improve the final
experience.

## 4. Visual identity authority

The four canonical identity images are the highest authority for final visible
identity. Turnarounds, geometry references, models, textures, rigs, expressions,
and generated hidden structure are subordinate to canonical visible appeal.

Neutral/default presentation must preserve silhouette, facial identity, eye
shape/scale/placement/appeal, proportions, major color relationships, signature
appendages/motifs, perceived age/softness/cuteness, and material impression.

A technically impressive character is unacceptable if it no longer looks
unmistakably like its canonical Grimo.

## 5. Character direction

- **Carol:** young sheep-like; dream-cloud fleece is a dominant identity system;
  attention-seeking + relaxed; calm, reassuring, soft, grounded; heavy feet;
  fleece follows authored primary motion with restrained delay.
- **Jill:** young spring-green dragon-like; attention-seeking + energetic;
  emotion propagates from chest/upper body to wings/tail/leaves; rooted,
  weighty tail.
- **Pino:** young blue otter-like; energetic + independent; soft and buoyant but
  grounded, never hollow-balloon.
- **Shushu:** young white/cherry-pink panda-like; relaxed + independent;
  grounded plush compression/settle with believable flower/prop attachment.

Shared runtime is allowed; shared personality is not.

## 6. Required interaction capabilities

Architecture must support tap/poke, slow pet/stroke, back-and-forth petting,
semantic body zones, local contact response, gaze/face response, appropriate
whole-body follow-through, secondary motion, mild boundaries, self-initiated
invitations, staged item/feeding play, interruption, reaction variation, and
emotional afterglow.

## 7. Autonomous life

The companion must feel alive when the user does nothing through coordinated but
asynchronous channels such as posture/breathing, blink, gaze, attention, head,
ears/wings/tail/limbs, weight shift, expression, secondary structures,
occasional larger actions, and intentional quiet.

The objective is not constant motion.

## 8. Reaction grammar

```text
input / event
→ local acknowledgement
→ anticipation / intent
→ local body response
→ attention / gaze / face
→ primary body action
→ secondary follow-through
→ optional sound / haptic / VFX
→ settle
→ emotional afterglow
→ return or transition to living idle
```

Not every reaction needs every stage. New input should be able to redirect
current behavior rather than endlessly queueing canned clips.

## 9. Positive-only care philosophy

No neglect punishment, affinity loss for absence, sickness/hunger punishment
loop, guilt-based notification design, or hostile punishment for ordinary
incorrect touching. Boundaries may use hint, avoidance, confusion, mild protest,
withdrawal, and recovery.

## 10. Device truth

Grimo is smartphone-first.

- **Primary available real-device QA:** Xiaomi 14T Pro.
- **Pixel 7a-class:** lower-performance compatibility / design target.
- A real Pixel 7a is currently unavailable; do not require or claim Pixel 7a
  real-device PASS.
- Pixel 7a status is **UNVERIFIED_TARGET** until actual target-class validation
  exists.

Architecture/assets must still account for sustained frame pacing, latency,
memory, asset footprint, loading, thermal/battery behavior, browser
compatibility, touch reliability, and four-character scalability.

## 11. Human acceptance

Automated tests are evidence, not final acceptance authority. Human-visible FAIL
overrides technical PASS.

Human acceptance asks whether identity is unmistakable and appealing, idle feels
alive without mechanical over-animation, touch causality is local and
convincing, and several minutes remain natural/responsive/varied on smartphone.

## 12. Technology principle

No renderer, DCC, rigging method, topology preference, or 2D/3D purity claim
outranks this document. Production architecture is selected separately and
remains falsifiable by final-use evidence.
