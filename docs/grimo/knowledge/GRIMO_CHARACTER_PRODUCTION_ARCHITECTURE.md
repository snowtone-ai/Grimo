# Grimo — Character Production Architecture

**Status:** Active durable production-architecture authority  
**Updated:** 2026-09-25  
**Scope:** Grimo character capability envelope; Carol first, reusable for Jill / Pino / Shushu

---

## 0. Architecture decision

Grimo uses a **Full-Spatial 3D Living Character Architecture with View-Weighted Polish**.

This document defines what the finished character system must be capable of.

It does **not** define how Codex must construct it.

The core architecture rule is:

> **The character must exist as a coherent spatial character wherever the product can plausibly expose it, while production effort is weighted toward the views and behaviors that matter most to the user.**

Implementation is free to evolve as long as that capability and the higher Product Goal are preserved.

---

## 1. Product Goal outranks implementation

The architecture exists to deliver the Grimo companion experience.

It is not a purity standard.

The target is not:

- perfect topology for its own sake;
- one specific Blender workflow;
- one mesh philosophy;
- one rig philosophy;
- one rendering technique;
- one procedural system;
- one asset-generation method.

The target is a character that remains:

- unmistakably itself;
- cute and appealing;
- spatially believable;
- grounded;
- expressive;
- independently controllable where the experience requires it;
- responsive to touch and attention;
- motion-capable;
- stable in the actual runtime;
- scalable to the four Grimo characters.

When implementation elegance and final experience conflict, final experience wins unless the implementation creates a credible downstream failure.

---

## 2. Architecture vs implementation

### Architecture fixes the capability envelope

Examples:

- a coherent spatial 3D character;
- front-priority presentation without off-axis collapse;
- independent control of meaningful expressive regions;
- motion/deformation readiness;
- stable attachments;
- runtime viability;
- character identity preservation.

### Codex owns implementation

Codex may independently choose:

- topology;
- mesh density;
- modular vs connected meshes;
- sculpted vs procedural geometry;
- manual vs scripted construction;
- local edit vs regional rebuild;
- reuse vs reconstruction;
- rig structure;
- bones;
- constraints;
- morphs / shape keys;
- corrective deformation;
- materials;
- shaders;
- local procedural systems;
- facial implementation;
- fleece implementation;
- export strategy;
- diagnostics;
- validation methods.

No implementation technique is promoted to architecture merely because it worked previously.

No implementation technique is forbidden merely because it failed previously in a different context.

Evidence decides.

---

## 3. Visual authority

Visual identity remains above implementation convenience.

For a character:

1. current explicit Human decision;
2. canonical identity;
3. approved character-specific visible authorities;
4. approved experience / motion requirements;
5. supporting geometry / numeric contracts;
6. implementation assets and historical production evidence.

A model must not redefine Carol, Jill, Pino, or Shushu to accommodate an easier topology or rig.

Supporting numbers help maintain consistency.

They do not justify a visibly off-model final character.

---

## 4. Full-spatial coherence

Front-facing interaction is the highest presentation priority, but the character is not a front-only object.

The model must remain spatially coherent through plausible exposure such as:

- front;
- front-weighted 3/4;
- side;
- rear exposure;
- derived top exposure;
- head turns;
- pitch / yaw / roll;
- contact-seeking lean;
- body compression;
- support shift;
- limb presentation;
- ear / wing / tail motion;
- feeding;
- social presentation;
- interruption and recovery.

This does not require identical beauty polish from every angle.

It requires that no plausible angle reveals an obviously fake, collapsed, missing, or camera-dependent construction.

---

## 5. View-weighted polish

Use quality investment according to final-use importance.

### HERO_PRIORITY

Highest perceptual fidelity.

Typical examples:

- face;
- eyes;
- mouth / muzzle where identity-critical;
- ears / wings / other signature appendages;
- visible hooves / paws / feet;
- primary front silhouette;
- Carol's front/crown fleece and face opening;
- other surfaces emphasized by the companion camera.

### GENERAL_EXTERIOR

Any exterior surface that may plausibly become visible.

It must have:

- coherent volume;
- believable attachment;
- stable silhouette;
- no obvious holes or flattening;
- sufficient quality to preserve character identity.

It does not need equal Hero polish.

### MOTION_CRITICAL

Any region whose deformation, support, touch ownership, or attachment becomes important during a motion family.

Its implementation must survive the required motion.

### FUNCTIONAL_HIDDEN

Permanently hidden support / deformation / attachment / collision structure.

It needs functional correctness, not beauty polish.

These classes describe desired output quality.

They do not prescribe a production order.

---

## 6. Independent expressive control

The architecture must allow meaningful regions to act independently when the experience requires it.

Across Grimo this may include:

- eyes / eyelids;
- gaze;
- mouth / face;
- head;
- ears;
- wings;
- forelimbs;
- hind support;
- hooves / paws;
- tail;
- chest / torso;
- character-specific secondary structures;
- wearable attachment regions.

The exact control mechanism is not prescribed.

A bone, morph, shader, local geometry system, procedural control, or combination is valid if it produces the required spatially owned result.

---

## 7. Carol capability envelope

Carol must be capable of supporting, where required by approved behavior:

- stable low grounded support;
- independent head orientation and restrained lean;
- expressive eyes / eyelids / gaze;
- facial expression without identity collapse;
- independently expressive ears with believable root volume;
- front-limb / hoof presentation;
- torso/chest pitch and restrained compression;
- support transfer without weightlessness;
- independent tail control;
- left/right touch locality;
- cheek / head contact-seeking;
- recoverable interruption and settle;
- dream-cloud fleece acting as a real spatial identity system.

Realistic sheep anatomy is not required.

Carol-specific spatial coherence is required.

---

## 8. Carol fleece

Carol's fleece is a primary identity system.

The finished result must preserve:

- recognizable full-spatial volume;
- approved front silhouette;
- coherent side / rear / top-derived mass;
- a stable relationship with face, ears, torso, and hooves;
- regional controllability;
- restrained delayed secondary response;
- motion that remains authored rather than jelly-like.

The architecture does **not** prescribe how the fleece must be built.

Codex may choose whichever geometry / rig / deformation / procedural combination best serves the approved result and runtime.

Camera-facing shells or other view-specific constructions are unacceptable only when they fail the required spatial exposure or motion.

---

## 9. Face / eyes / ears

Face and eyes are identity-critical.

The architecture must allow:

- canonical neutral appearance;
- blink;
- eyelid expression;
- gaze changes;
- subtle facial acting;
- head motion without eye/socket collapse;
- reasonable 3/4 and side projection;
- local corrective behavior where needed.

Ears must support:

- real spatial thickness;
- stable attachment;
- independent motion;
- droop / rotation / subtle asymmetry;
- believable occlusion with head / fleece;
- no obvious root detachment during required motion.

The exact topology or control system remains executor-owned.

---

## 10. Limbs, hooves, support, and weight

Visible support must preserve the character's intended weight.

For Carol this means:

- low support;
- short limbs;
- heavy grounded hooves;
- stable contact;
- plausible support transfer;
- no floating or arbitrary body-root motion.

The architecture must be capable of front-limb or hoof presentation without destroying support credibility.

How this is modeled or rigged is not fixed.

---

## 11. Motion ownership

Motion must be spatially owned by the character.

The architecture must support the experience principles of:

- local response;
- attention / face response;
- necessary body commitment;
- secondary follow-through;
- settle;
- interruption;
- afterglow;
- intentional stillness.

This does not require every behavior to be a monolithic animation clip.

It also does not require a specific procedural runtime.

Clips, layers, masks, morphs, procedural systems, state-driven composition, and hybrids are all implementation choices.

---

## 12. Whole-character pseudo-life prohibition

A completed character may not be made to feel alive primarily by globally treating the entire finished visual as one rigid image and applying:

- whole-character image translation;
- global squash / stretch;
- global warp;
- global bounce;
- whole-image deformation as a substitute for body-part ownership.

Global root motion may naturally occur as part of legitimate spatial acting.

The prohibition is against replacing articulated / local character behavior with finished-image pseudo-life.

---

## 13. Reuse, rebuild, and historical assets

Existing assets are resources, not mandatory starting points.

Historical geometry, rigs, scripts, measurements, and evidence may be:

- reused;
- adapted;
- compared;
- ignored;
- partially replaced;
- rebuilt.

Codex decides what best serves the current Goal.

There is **no architecture-level reuse-first rule**.

There is also no rebuild-first rule.

The only requirement is that historical material never outrank current authority.

---

## 14. Topology and mesh structure

No single topology doctrine is required.

Valid solutions may use:

- one mesh;
- multiple meshes;
- modular attachments;
- merged regions;
- separate expressive components;
- different local densities;
- corrective shapes;
- topology optimized around deformation.

A watertight single hero body is not inherently required.

A modular model is not inherently inferior.

Topology is successful when it supports the approved visual result, motion, attachment, export, runtime, and maintainability.

---

## 15. Facial and rendering hybridity

Hybrid rendering / deformation is allowed when the character remains spatially coherent.

Possible methods include:

- geometry;
- bones;
- shape keys / morph targets;
- materials;
- shaders;
- local procedural controls;
- texture / normal changes;
- constrained compositing when it remains spatially owned.

No method receives preference merely for being more “3D-pure.”

The user-visible result and required behavior determine suitability.

---

## 16. Runtime boundary

Grimo is smartphone-first.

Current implementation context may use:

- Blender for authoring;
- GLB / glTF exchange;
- PlayCanvas for runtime;
- PWA delivery.

These are current implementation choices, not aesthetic goals.

Character architecture must remain compatible with practical:

- frame pacing;
- memory;
- loading;
- texture / model footprint;
- animation footprint;
- touch responsiveness;
- thermal / battery constraints;
- browser behavior;
- four-character scalability.

Current device truth:

- Xiaomi 14T Pro = available real-device QA source.
- Pixel 7a-class = lower-performance design target until real target-class validation is available.

Codex may optimize implementation as needed to meet these constraints.

---

## 17. Technical defects

Technical defects matter according to consequence.

A defect is materially important when it causes or credibly threatens:

- visible identity failure;
- visible artifact;
- deformation collapse;
- bad attachment;
- broken occlusion;
- support / weight failure;
- interaction failure;
- export failure;
- runtime failure;
- device feasibility failure;
- future required motion collapse.

Technical cleanliness with no credible product consequence is lower priority.

A metric or validator is evidence.

It is not the final definition of visual correctness.

---

## 18. Human-evaluable output

When Human is asked to judge:

- identity;
- cuteness;
- appearance;
- naturalness;
- weight;
- touch ownership;
- motion quality;

the presented result must be representative enough that unrelated low-fidelity elements do not dominate the judgment.

This is an evidence-quality requirement, not a mandated prototype workflow.

Codex chooses how to reach a judgeable result.

If an artifact is visibly too unrepresentative to answer the Human question, no product conclusion should be inferred from that presentation.

---

## 19. Validation freedom

No fixed stress-test checklist is mandated by architecture.

Codex should validate the exposures and capabilities that are materially relevant to the current Goal.

Depending on the task, that may include:

- neutral presentation;
- 3/4;
- side;
- expression;
- ear / appendage motion;
- cheek lean;
- limb presentation;
- support shift;
- deformation;
- interruption;
- runtime;
- device behavior.

The executor chooses the smallest, largest, or most direct validation set that best reveals whether the actual architecture works.

Validation exists to discover failure, not to satisfy a checklist.

---

## 20. Architecture change

The current full-spatial 3D architecture is the approved baseline.

Codex may freely change implementation architecture **inside** this capability envelope.

Examples:

- topology;
- modularity;
- rigging;
- facial system;
- fleece system;
- procedural tooling;
- render implementation.

A change that would alter the product-level capability itself — for example abandoning coherent spatial 3D or removing required independent control — is a Product / Architecture decision and must not be silently substituted for the approved baseline.

If strong evidence suggests such a product-level change would materially improve Grimo, surface the evidence for Human decision.

There is no attempt-count trigger for raising such evidence.

Raise it when the evidence warrants it.

---

## 21. Superseded architecture-process rules

The following are not architecture requirements:

- mandatory reuse-first;
- mandatory reconstruction-first;
- fixed attempt limits;
- two-cycle stopping;
- prescribed probe order;
- prescribed production waterfall;
- predetermined topology architecture;
- predetermined rig architecture;
- mandatory local-only fixes;
- mandatory preservation of a historical candidate;
- fixed technical gate sequences.

Those belong to historical workflows unless explicitly reinstated for a specific task.

---

## 22. Final architecture rule

> **Constrain the character's required capabilities and identity. Do not constrain the executor's route without evidence.**

And:

> **Full-spatial coherence is a result requirement, not a modeling recipe.**

And:

> **Front receives the most polish; no plausible exposed view is allowed to reveal a structurally fake character.**

And:

> **The best implementation is the one that most reliably delivers the approved Grimo experience.**
