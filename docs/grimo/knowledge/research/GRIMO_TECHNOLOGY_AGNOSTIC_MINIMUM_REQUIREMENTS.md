# Grimo — Technology-Agnostic Minimum Requirements

**Purpose:** This document defines the minimum product, character, interaction, quality, and delivery requirements for selecting Grimo's character-production and runtime architecture from first principles.

It intentionally does **not** choose a renderer, engine, DCC tool, rigging system, animation framework, or 2D/2.5D/3D implementation method.

The research task is to identify the production approach most capable of meeting these requirements at the highest quality.

---

## 1. Product North Star

Grimo is a task-management product whose emotional center is a set of companion creatures called **Grimo**.

The experience goal is:

> The user wants to meet and interact with a Grimo strongly enough that completing tasks naturally becomes a reason to return to the companion experience.

Experience priority:

1. **Cuteness / appeal**
2. **Healing / comfort**
3. **Attachment**
4. **Fun**
5. **Surprise**
6. **Collection**

The character experience must never feel like a decorative animation attached to a productivity app. The Grimo must feel like a living companion with attention, intent, personality, continuity, and bodily causality.

Typical interaction session: approximately **30 seconds to 5 minutes**.

---

## 2. Primary Quality Benchmark

The primary interaction-quality benchmark is the **partner Pokémon experience in Pokémon: Let's Go, Pikachu! / Let's Go, Eevee!**, especially the sense of life created by the partner Eevee.

The target is not visual copying and not IP imitation. The benchmark is the following abstract quality bar:

- a character that appears alive even without user input;
- continuous attention and micro-behavior;
- expressive eyes, face, head, ears, body, limbs, tail, fur/fleece/ornaments, etc.;
- local bodily response to touch;
- anticipation, reaction, follow-through, settle, and emotional afterglow;
- multiple behavior variants rather than a single repeated canned reaction;
- self-initiated interaction and autonomous behavior;
- convincing transitions between idle, attention, interaction, and recovery states;
- character-specific motion rather than generic shared animation.

Other high-quality 3D companion / pet / creature games may be used as secondary references where they provide better production or runtime evidence.

---

## 3. Non-Negotiable Character-Animation Rule

### Whole-image motion is completely prohibited

A completed single illustration must **never** be treated as one rigid visual object and then scaled, stretched, squashed, rotated, translated, warped, bounced, or otherwise manipulated to simulate life.

This prohibition applies to:

- idle;
- breathing;
- touch reactions;
- emotional reactions;
- feeding;
- self-initiated behavior;
- transitions;
- rare behaviors;
- any other runtime state.

If a production method is selected, it must support genuine independent movement of the character's meaningful body regions, facial components, appendages, and secondary expressive structures.

The research may determine whether the correct solution is 3D rigging, hybrid 3D, 2D rigging, layered mesh animation, another method, or a combination. However, the final result must not reduce to moving a single finished image.

---

## 4. Canonical Identity

There are four canonical Grimo characters:

- **Carol**
- **Jill**
- **Pino**
- **Shushu**

Their canonical images are the **only authority for visual identity**.

Any generated turnaround, hidden geometry, 3D model, texture, rig, expression, or implementation reference is subordinate to the canonical image.

When a generated or inferred asset conflicts with the canonical image, the canonical wins.

A technically impressive character is unacceptable if it no longer looks unmistakably like the canonical Grimo.

### Identity acceptance principle

The neutral/default character presentation must preserve at minimum:

- silhouette;
- facial identity;
- eye shape, scale, placement, and visual appeal;
- proportions;
- major color relationships;
- signature appendages and motifs;
- perceived age / softness / cuteness;
- character-specific material impression.

---

## 5. Character-Specific Direction

### Carol

- Young sheep-like Grimo.
- Very large white-to-pale-blue-purple dream-cloud fleece.
- Small cream face.
- Large brown-to-amber glossy eyes.
- Brown ears and hooves.
- Moon / star motifs.
- Personality: **attention-seeking + relaxed**.
- Motion identity: calm, reassuring, soft, cloud-like.
- Fleece should visually follow primary body movement with delayed softness rather than behaving as a rigid mass.
- Head / cheek movement should feel gentle and secure.
- Ears react subtly.
- Feet should feel comparatively heavy and grounded.
- Moon / star elements may support special reactions but must not flash constantly.

### Jill

- Young spring-green dragon-like Grimo.
- Round head/body, very large green starry eyes, cream belly.
- Yellow-green wing membranes / horns.
- Leaf mane with white flowers and clover.
- Thick curved tail.
- Personality: **attention-seeking + energetic**.
- Motion identity: emotion begins around chest / upper body, then propagates to wings, tail, leaves.
- Tail must feel rooted and heavy, not like a fast cat tail.
- Leaves and flowers should follow primary movement with delay.
- Forelegs must remain short like the canonical design.

### Pino

- Young blue otter-like Grimo.
- Cream lower face and large belly.
- Round, soft body; short ears; large glossy blue eyes; blue paw pads; thick tail.
- Bubble / water-splash motifs.
- Personality: **energetic + independent**.
- Motion identity: soft water-bag-like body, inward hugging arm tendency, delayed tail follow-through, buoyant but not hollow-balloon motion.
- Water / bubbles must not become constant visual spam.

### Shushu

- Young white-and-cherry-pink panda-like Grimo.
- Round plush face/body; pink ears, arms, and legs.
- Large pink-brown glossy eyes with flower-shaped highlights.
- Cherry-blossom crown and bouquet.
- Personality: **relaxed + independent**.
- Motion identity: soft delayed plush compression / settle, small ear bounce, grounded seated weight.
- Bouquet relationship to the hands and crown relationship to the head must remain convincing.
- Flowers / petals should follow primary movement with delay.

### Cross-character requirement

A shared runtime is allowed; shared personality is not.

The same animation simply recolored or trivially retargeted across all four characters is unacceptable.

Each Grimo must have a distinct motion signature, attention style, timing, weight, secondary motion, and reaction language.

---

## 6. Required Interaction Capabilities

At minimum, the selected production/runtime architecture must be able to support:

- tap / poke;
- slow pet / stroke;
- back-and-forth petting;
- semantic body zones;
- local response at the contacted body region;
- facial / gaze response;
- whole-body follow-through where appropriate;
- secondary motion;
- mild dislike / avoidance / confusion reactions without aggressive punishment;
- self-initiated invitations to interact;
- feeding with staged consumption rather than instant disappearance;
- item / toy interactions;
- special character-specific interactions;
- interruptible reactions;
- reaction variation and repetition suppression;
- emotional afterglow instead of immediate snap-back to neutral.

A hold gesture may be supported but is not required as a core launch interaction.

---

## 7. Autonomous Life Requirement

The character must feel alive when the user does nothing.

The architecture must support multiple overlapping or coordinated behavior channels such as:

- breathing / posture maintenance;
- blinking;
- eye movement / gaze;
- attention shifts;
- head movement;
- ear / wing / tail / limb micro-adjustments;
- weight shifts;
- expression changes;
- secondary appendage / fleece / leaf / flower / bubble motion;
- occasional larger self-initiated actions;
- intentional quiet moments.

The objective is **not** to move every part constantly.

The objective is to avoid the appearance of a static object waiting for input while preventing mechanical over-animation. Different channels should be capable of operating at different cadences and with contextual coordination.

---

## 8. Motion and Reaction Grammar

Core reactions should be able to express the following causal structure:

```text
input / event
→ contact acknowledgement
→ anticipation / intent
→ local body response
→ attention / gaze / face
→ primary body action
→ secondary follow-through
→ optional sound / haptic / VFX
→ overshoot where appropriate
→ settle
→ emotional afterglow
→ return or transition to living idle
```

Not every reaction must contain every stage, but the user must be able to understand:

- what was touched or what happened;
- which body part noticed first;
- how the reaction propagated;
- what emotion the character expressed;
- how the body settled afterward.

New input should be capable of redirecting or interrupting current behavior rather than endlessly queueing canned clips.

---

## 9. Facial and Attention Requirements

The architecture must support sufficiently expressive face and attention behavior, including at minimum:

- natural blinking;
- eye direction / gaze control;
- looking toward user interaction;
- looking away / environmental attention;
- mouth / cheek expression where appropriate;
- multiple emotional expression states;
- coordinated head / eye behavior;
- expression transitions that do not visibly snap.

The character should not stare directly at the user continuously.

---

## 10. Positive-Only Care Philosophy

Grimo must not use neglect punishment as a retention mechanic.

Do not require:

- affinity loss because the user was absent;
- hunger / sickness punishment loops;
- item confiscation;
- guilt-based notification design;
- angry punishment for ordinary incorrect touching.

Disliked touch should be communicated through characterful avoidance, confusion, protection, mild protest, or other non-hostile responses.

Attachment should be strengthened through:

- wanting to see the character;
- new reactions;
- character initiative;
- meaningful item interactions;
- gifts / memories / surprises;
- increasing behavioral richness.

---

## 11. Delivery and Performance Boundary

Grimo is intended to be a **smartphone-first web/PWA product**.

Minimum acceptance device class: **Google Pixel 7a**.

A technically superior solution that only works acceptably on flagship hardware is not sufficient.

The selected architecture must therefore be evaluated for:

- sustained frame pacing;
- input latency;
- memory usage;
- model / texture / animation footprint;
- loading strategy;
- battery / thermal behavior where evidence is available;
- browser compatibility;
- touch interaction reliability;
- asset streaming / caching needs;
- scalability from one character to four characters.

Quality is the priority, but the result must remain practical on the target device class.

The research may recommend changes to the surrounding web architecture if necessary, but it must distinguish clearly between:

1. what is required for high-quality character runtime;
2. what is optional optimization;
3. what would require abandoning the PWA product boundary.

---

## 12. Production Scalability Requirement

The chosen approach must not only produce one impressive demo.

It must support production and long-term expansion for all four characters, including:

- reusable production conventions;
- character-specific rigs or adapters where needed;
- animation-library growth;
- facial-state growth;
- touch-zone growth;
- additional items / feeding / toys;
- autonomous behaviors;
- rare behaviors;
- future reactions without exponential asset-management collapse.

The research must evaluate not only runtime capability but also authoring, revision, QA, and iteration cost.

---

## 13. Human Quality Gates

Automated tests are evidence, not final acceptance authority.

### Gate 1 — Identity

At neutral / default presentation:

- Is this unmistakably the same Grimo as the canonical?
- Is the canonical appeal preserved?
- Does the face remain correct under the chosen production method?

### Gate 2 — Living Idle

In a 15–30 second observation with no interaction:

- Does the character appear alive?
- Are movement channels naturally varied rather than synchronized mechanically?
- Are there uncomfortable, floaty, rubbery, dead, or repetitive moments?

### Gate 3 — Touch

For identical user interactions:

- Is contact causality visually readable?
- Does the touched region respond correctly?
- Does the face / attention follow naturally?
- Does the response feel character-specific?
- Does the body settle convincingly?

### Gate 4 — Final Character System

- Four characters remain clearly distinct in motion and personality.
- Several minutes of interaction do not collapse into obvious repetition.
- The experience feels natural on a smartphone.
- The user is the final acceptance authority.

---

## 14. Research Evaluation Criteria

Any candidate production approach must be compared against at least these criteria:

1. canonical identity fidelity;
2. maximum attainable animation quality;
3. sense-of-life potential;
4. facial animation quality;
5. gaze / attention control;
6. local touch causality;
7. procedural / layered animation capability;
8. secondary-motion capability;
9. interruptibility and animation blending;
10. autonomous behavior capability;
11. character uniqueness;
12. animation-library scalability;
13. authoring and revision efficiency;
14. AI / coding-agent automation potential;
15. browser/PWA suitability;
16. Pixel 7a-class performance;
17. asset size / memory / loading cost;
18. four-character production scalability;
19. long-term maintainability;
20. ability to reach the interaction-quality bar represented by Let's Go partner Eevee.

The research must not assign high scores without evidence or explicit reasoning.

---

## 15. Technology Must Remain Open During Research

Do **not** assume any of the following is already selected:

- 2D;
- layered 2D;
- 2.5D;
- full 3D;
- hybrid 2D/3D;
- Blender;
- Maya;
- Three.js;
- Babylon.js;
- Unity;
- Godot;
- PixiJS;
- Live2D;
- Spine;
- Rive;
- WebGL;
- WebGPU;
- skeletal animation;
- morph targets;
- procedural animation;
- physics-based secondary motion;
- hand-authored secondary motion;
- any specific asset count or rig topology.

The task of Deep Research is to determine the best architecture from evidence, not to justify a predetermined stack.

---

## 16. Evidence and Intellectual-Property Rule

Pokémon and other commercial games are references for **production principles, interaction structure, animation design, and technical architecture** only.

Do not propose copying or extracting copyrighted runtime assets, animation files, models, textures, audio, or frames into Grimo.

Research may analyze publicly observable behavior, developer presentations, interviews, official documentation, patents where relevant, technical talks, job descriptions, and other lawful public evidence.

All recommendations for Grimo must result in original Grimo assets and original implementation.

---

## 17. Research Scope Boundary

This research is primarily about **character production and runtime architecture**.

Task CRUD, Calendar behavior, authentication, existing database migration, reward economy, and unrelated application UI are not the focus unless they materially constrain the character architecture.

The first production proof should use **Carol** as the vertical-slice character because a single character must validate the architecture before expanding to Jill, Pino, and Shushu.

However, the research must evaluate the architecture against all four canonical characters before recommending a final production method.

---

## 18. Required Research Outcome

The final Deep Research report should make a concrete recommendation rather than only listing options.

It must identify:

- the recommended character-production pipeline;
- the recommended runtime architecture;
- the recommended model / rig / facial / animation / secondary-motion strategy;
- how autonomous life should be structured;
- how touch reactions should be structured;
- how animation clips, procedural layers, and behavior scheduling should interact;
- the production workflow from canonical image to runtime character;
- what should be handmade, generated, procedural, simulated, or data-driven;
- the expected bottlenecks;
- the expected performance risks on Pixel 7a-class hardware;
- the Carol vertical-slice plan;
- the conditions under which the recommendation should be rejected and an alternative selected.

The report must distinguish clearly between:

- **verified fact**;
- **developer / primary-source statement**;
- **observable behavior from game footage**;
- **strong inference**;
- **design recommendation / prediction**.

Quality and evidentiary strength take precedence over speed.
