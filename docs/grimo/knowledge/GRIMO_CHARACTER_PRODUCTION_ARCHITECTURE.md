# Grimo — Character Production Architecture

**Status:** Active durable production-architecture authority  
**Updated:** 2026-09-24  
**Scope:** Carol first vertical slice; reusable architecture principles for Jill / Pino / Shushu

## 1. Architecture decision

Adopt **Full-Spatial 3D Living Character Architecture with View-Weighted Polish** as the current baseline.

Grimo characters are authored as coherent spatial 3D characters whose exterior form remains valid across front, three-quarter, side, back, top-derived inspection, and the practical articulation range required by present or future character motion.

The front companion presentation remains the highest visual-polish priority, but **front priority is not permission for front-only geometry, camera-specific cheating, or off-axis structural collapse**.

The production rule is:

> **Full-3D spatial coherence everywhere the character can plausibly expose; polish investment weighted toward actual user-facing views.**

This architecture is subordinate to the Product North Star. Architecture Review may change implementation details when evidence shows a different method better delivers the companion experience, but view-specific geometry hacks are not the default escape route.

## 2. Core rules

1. **Full spatial coherence is the baseline.** Carol must remain one coherent 3D character when viewed or moved through practical front, 3/4, side, rear, top-derived, lean, pitch, yaw, support-shift, and appendage-motion states.
2. **Front priority means polish priority, not structural exclusivity.** The Hero front receives the highest identity/appeal polish. Other exterior views may receive less aesthetic polish, but must remain structurally believable and free of obvious collapse.
3. **Future motion must not require rebuilding the character simply because a newly exposed angle was previously ignored.** AI-authored local fixes must not create hidden view debt.
4. **Exterior geometry has a coherence floor.** Any external surface that can plausibly become visible must have sufficient volume, attachment, continuity, and deformation readiness to survive reasonable motion/camera exposure.
5. **Hidden geometry is functional.** Permanently hidden chassis/interior structure exists for support, deformation, attachment, collision/clearance, and spatial continuity; Hero beauty is not required there.
6. **One watertight hero body is not required.** Modular/separate meshes are allowed when they behave as one coherent character through all relevant views and motions.
7. **Rig for semantics, not anatomical purity.** Head, eyes/face, ears, forelimbs, support, tail, and fleece regions need independent control because the experience uses them independently.
8. **Facial acting may be hybrid.** Geometry, skinning, morphs, material states, and local procedural controls may be combined, but the visible result must remain spatially owned by the character.
9. **Fleece is a full-spatial Hero identity system.** Carol fleece is not a camera-facing shell, a ring of proxy balls, or a physics blob. It needs real 3D volume, coherent front/side/back/top form, and authored regional motion ownership.
10. **Motion/deformation testing precedes production lock, not spatial coherence.** Production retopo/weights/shaders may remain provisional while motion is tested, but the visible geometry used for Human perceptual judgment must already be representative enough to support that judgment.
11. **Every geometry task names the final interaction or visible failure it fixes.** Technical cleanliness alone is not a Product Goal.
12. **Whole-character image pseudo-life remains prohibited.** No global finished-image warp/scale/bob as the living system.
13. **Reuse before reconstruction.** Existing higher-quality geometry, fleece, rigs, scripts, and validated historical assets must be audited before generating a lower-fidelity replacement from scratch.

## 3. Why full-spatial 3D is the baseline

Partner reference evidence and Carol production history both show that interaction-critical behavior exposes surfaces unpredictably:

- head turns and contact-seeking leans change near/far ordering;
- ears can rotate, droop, lift, and partially occlude or emerge from fleece;
- forelimbs/hooves can shift toward the viewer or transfer support;
- cheek contact changes the visible relationship between face, fleece, ear, and chest;
- body pitch, recoil, settle, feeding, social presentation, and future motion can expose angles not anticipated by a narrow initial camera envelope;
- future behavior discovery should not force a new geometry architecture simply because an initially “out-of-scope” angle becomes useful;
- AI-driven local iteration is especially vulnerable to view-specific fixes that appear correct from one camera while creating hidden structural debt elsewhere.

A reusable companion therefore benefits from a coherent 3D source of truth. Grimo may choose not to show every angle in the final product, but **the model should remain capable of showing them without obvious structural failure**.

This does not mean every surface receives equal artistic investment. It means spatial validity is broad; Hero polish is selective.

## 4. Surface investment classes

### HERO_PRIORITY

Highest identity/appeal polish.

Typical Carol examples:

- face;
- eyes;
- ears;
- visible hooves;
- front/crown fleece;
- primary fleece silhouette;
- tail when visible;
- exposed face/fleece/head transitions;
- surfaces emphasized by the primary companion camera.

### GENERAL_EXTERIOR

All exterior surfaces that may plausibly become visible through character orientation, future motion, debugging, or camera/framing changes.

Requirements:

- coherent 3D volume;
- plausible attachment;
- no obvious holes/collapse/view-specific flattening;
- motion-safe continuity;
- sufficient visual quality that exposure does not immediately break the character.

These surfaces do **not** require equal Hero polish.

### MOTION_CRITICAL

Any HERO_PRIORITY or GENERAL_EXTERIOR region used strongly by a motion family.

Requirements increase according to the behavior:

- deformation quality;
- contact ownership;
- clearance;
- silhouette readability;
- support/weight behavior;
- stable secondary-motion attachment.

Motion exposure raises the required fidelity but does not create the underlying 3D existence requirement; exterior coherence already exists.

### FUNCTIONAL_HIDDEN

Permanently hidden support/deformation/attachment/collision/clearance structure.

Functional correctness is required. Hero visual polish is not.

If a supposedly hidden region becomes plausibly visible, it moves into GENERAL_EXTERIOR or MOTION_CRITICAL.

## 5. Carol functional degrees of freedom

The architecture must support, at minimum where required by approved or reasonably anticipated companion behavior:

- stable support base / grounded COM read;
- independent head yaw, pitch, roll, and restrained lean;
- eye/gaze and facial expression controls;
- independent ears with real root volume and stable occlusion through head motion;
- independent front limbs / hoof presentation;
- limited torso/chest pitch, compression, and weight shift;
- rear support stabilization;
- tail control;
- Carol fleece primary regional control plus restrained secondary follow-through;
- left/right touch locality;
- recoverable transitions and interruption;
- coherent visibility through front, 3/4, side, rear, and derived top inspection.

Realistic sheep anatomy is not required. Spatial coherence and Carol-specific acting are required.

## 6. View and camera policy

The front companion camera remains the **primary presentation and highest-polish reference**.

However, camera policy must not define the geometry's existence.

Use these view classes:

- **PRIMARY_HERO_VIEW:** front/front-weighted neutral and ordinary interactions; highest polish.
- **SECONDARY_CHARACTER_VIEWS:** 3/4 and side views likely to appear through motion, inspection, future behavior, or framing changes; strong coherence and attractive character read required.
- **TERTIARY_EXTERIOR_VIEWS:** rear/top-derived and uncommon exterior exposures; coherent full-3D structure required, but lower cosmetic polish is acceptable.
- **FUNCTIONAL_HIDDEN:** genuinely non-visible internal/support geometry only.

There is no “OUT_OF_SCOPE exterior angle” that permits a visibly broken model.

Free-orbit beauty parity is not required. Full-spatial structural validity is.

## 7. Human-evaluable fidelity floor

Prototype-before-polish does **not** mean “use arbitrarily low-quality visible proxies for Human perceptual judgment.”

Before asking Human to judge:

- identity;
- cuteness;
- appeal;
- motion naturalness;
- body ownership;
- weight;
- touch causality;
- companion quality;

all visible components that materially influence the judgment must meet a **Human-Evaluable Fidelity Floor**.

For Carol this includes, whenever visible in the probe:

- face / eyes;
- ears;
- visible feet / hooves;
- fleece silhouette and face opening;
- relevant attachment/occlusion relationships;
- the specific deformation/contact region being judged.

Cheap stand-ins are acceptable for technical questions when they do not dominate the result. If a proxy is visually off-model enough that Human cannot separate proxy failure from architecture/motion failure, the probe is **INVALID**, not a candidate FAIL.

## 8. Reuse-first production rule

Before generating new visible geometry or fleece:

1. inspect current assets;
2. inspect relevant historical Grimo branches/assets;
3. inspect recoverable local production artifacts when available;
4. compare candidate donors against current authority;
5. reuse or adapt the highest-value valid asset when cheaper and safer than reconstruction.

Do not create a lower-quality replacement merely because it is easier for the current executor to generate.

Historical assets are donors/evidence, not authority. Canonical identity and current approved references remain above them.

## 9. Provisional-before-production rule

Production topology, final weights, final shader, final rig, final fleece, and the complete animation library are not required before representative behavior testing.

Provisional implementation is allowed when:

- the Decision Question is actually answerable with it;
- visible proxy quality meets the Human-Evaluable Fidelity Floor when Human perception is being judged;
- the provisional mechanism does not create a dominant unrelated artifact;
- the source character remains spatially coherent.

Examples:

- provisional bones for a head-turn clearance test: allowed;
- temporary material for silhouette inspection: allowed;
- crude sphere-ring fleece used to judge Carol's cuteness or head/fleece ownership: not valid;
- low-detail hidden chassis used only for support mechanics: allowed.

Production-quality convergence follows successful representative tests, but full-spatial coherence is maintained throughout.

## 10. Stress conditions to prove before production lock

Use representative stress states, not static neutral alone.

At minimum as relevant:

- neutral Hero presentation;
- front → mild 3/4 head/body orientation;
- side exposure sufficient to reveal head/ear/fleece depth;
- blink/expression range;
- independent ear response;
- left/right cheek lean;
- one-front-limb or hoof presentation;
- small body weight shift;
- deeper head/chest bow/compression if approved;
- larger positive emotional pose;
- tail response;
- interruption / recovery;
- any new behavior that materially exposes a previously secondary surface.

The exact test set is task-specific, but no production lock should depend solely on one camera view.

## 11. Technical defects: when they block

A topology/self-intersection/mesh/attachment defect is a blocker when it materially causes or credibly threatens:

- visible artifact from a plausible exterior view;
- deformation collapse;
- unstable attachment/occlusion;
- bad clearance;
- unstable weighting/rig behavior;
- export/runtime failure;
- future motion exposure that would force structural rework;
- production scalability failure with demonstrated relevance.

Technical cleanliness is not an independent aesthetic goal.

When consequence is unknown, choose the cheapest **valid** probe. “Cheapest” does not override the Human-Evaluable Fidelity Floor.

## 12. Architecture Review triggers

Trigger Architecture Review when evidence shows the baseline cannot, at acceptable production/runtime cost, preserve one or more of:

- canonical identity / cuteness;
- full-spatial exterior coherence;
- required local touch causality;
- grounded spatial believability;
- required motion/deformation capability;
- interruptibility / variation;
- smartphone runtime feasibility;
- four-character production scalability.

Two bounded implementation cycles on essentially the same blocker without resolving the Decision Question trigger Architecture Review before attempt 3.

A second consecutive **probe-invalid** result also triggers review of the probe architecture rather than another cosmetic attempt.

## 13. Device boundary

Authoring may remain Blender-centered with GLB/glTF exchange and PlayCanvas runtime as the current implementation hypothesis.

- Xiaomi 14T Pro is the available real-device QA source.
- Pixel 7a-class is the lower-performance design/compatibility target and remains `UNVERIFIED_TARGET` until actual target-class validation exists.

Runtime constraints are architecture evidence, not merely final optimization chores.

## 14. Durable lessons from Carol v001–v013 and Hero Probe v001

Retain:

- canonical/authority system;
- numerical registration;
- geometry parameters;
- camera research;
- topology diagnostics;
- eye/socket lessons;
- intersection validators;
- bounded-attempt methodology;
- motion inventories;
- multi-view silhouette evidence;
- reusable historical full-3D fleece work;
- evidence methodology.

Additional durable lessons:

1. **Technical topology PASS does not guarantee visual identity.**
2. **Technical topology FAIL does not by itself quantify final companion impact.**
3. **A Human perceptual probe can be invalid even when implementation technically works.**
4. **Low-fidelity visible proxies can dominate judgment and make motion/architecture conclusions impossible.**
5. **View-limited geometry creates AI iteration debt: future motion can expose angles that were never made coherent.**
6. **Full-spatial coherence should be established broadly; polish should remain weighted toward actual user-facing views.**
7. **Existing validated assets should be reused before lower-quality reconstruction.**
8. **The correct response to an invalid probe is not to infer candidate failure.**