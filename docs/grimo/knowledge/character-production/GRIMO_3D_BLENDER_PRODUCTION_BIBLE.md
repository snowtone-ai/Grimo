# GRIMO 3D / Blender Production Bible

**Status:** Authoritative production specification candidate  
**Date:** 2026-09-14  
**Scope:** Carol first vertical slice; Jill / Pino / Shushu follow only after Carol passes all gates  
**Production baseline:** Stylized Full 3D → Blender → glTF/GLB → PlayCanvas → smartphone PWA  
**Primary quality target:** world-class stylized character production; Partner Pikachu / Eevee-class living-companion interaction quality without copying their assets, poses, rigs, or exact animation

---

## 0. Authority and source policy

This Bible normalizes the Grimo project around the current Full-3D direction. It must not be overridden by obsolete PixiJS layered-2D/2.5D implementation packs or by stale repository code that predates the technology-agnostic architecture decision.

### 0.1 Grimo authority hierarchy

1. **Product / quality requirements:** `GRIMO_TECHNOLOGY_AGNOSTIC_MINIMUM_REQUIREMENTS.md`
2. **Visual identity:** the four approved identity canonical images, plus any later user-approved 3D production canonical sheets
3. **Observed partner motion:** `GRIMO_PARTNER_PIKACHU_VIDEO_MOTION_ANALYSIS.md` and `GRIMO_PARTNER_EEVEE_VIDEO_MOTION_ANALYSIS.md`
4. **Experience / motion behavior:** `GRIMO_EXPERIENCE_MOTION_BIBLE.md`
5. **Production architecture:** `Grimo Character Production Architecture — Zero-Based Deep Research.md`
6. **This document:** 3D/Blender production technique, rig/deformation/animation/export/QA execution
7. **Repository implementation:** evidence of current implementation only; never allowed to veto an approved newer architecture decision

### 0.2 Evidence classes used here

- **[A]** current official / primary technical source
- **[B]** current professional production source
- **[V]** direct Grimo/Pikachu/Eevee visual observation already captured in Project Knowledge
- **[D]** strong production inference
- **[G]** Grimo production decision

### 0.3 Current external technical baseline verified on 2026-09-14

- Blender **5.2 LTS** was released 2026-07-14 and is supported until July 2028. **5.2.1 LTS** was released 2026-08-25. [A]
- Blender Studio currently documents a rigging workflow based on **procedural control-rig generation + manual weight painting + corrective shape keys**, tailored per production. CloudRig is the Studio rig-generation tool. [A/B]
- CloudRig current public version observed: **2.2.28 (2026-08-17)**. Its own changelog warns about backwards-compatibility changes, so Grimo must pin the exact extension version per accepted rig. [A]
- Blender 5.2 glTF export supports multiple animations, object transforms, pose-bone animation, shape keys and shape-key animation. Constraints/drivers/unsupported Blender-only behavior must be evaluated/baked into exportable results. [A]
- glTF 2.0 does **not** impose a global eight-morph-target limit. The specification states the number of morph targets is not limited; client implementations should support at least eight *morphed attributes*. Runtime performance remains implementation/device dependent. [A]
- Blender exports quads/n-gons to glTF as **triangles**. Authoring topology may be quad-centric, but final runtime QA must inspect triangulated output. [A]
- PlayCanvas currently provides animation state graphs, multiple animation layers, Override/Additive layer blending, layer masks, skinning and runtime morph target control. [A]

---

# 1. Executive production doctrine

## 1.1 Single recommendation

Grimo character production shall use:

```text
approved identity canonical
        ↓
approved 3D production canonical / geometry contract
        ↓
Blender 5.2.1 LTS — pinned production DCC
        ↓
model / retopo / lookdev / control rig / deform rig / facial system
        ↓
hand-authored primary animation + bounded secondary system
        ↓
export rig + glTF/GLB validation
        ↓
PlayCanvas behavior / layering / interruption / semantic touch
        ↓
smartphone PWA real-device validation
        ↓
Human Gate
```

**Blender is not merely an offline reference lab. It is the standard character-production DCC for the current Full-3D branch.** [G]

## 1.2 What determines world-class quality

The decisive factor is not the number of Blender features used. Quality comes from enforcing the correct decision order:

```text
identity
→ volume / silhouette
→ deformation feasibility
→ face / eyes
→ weight / support
→ primary acting
→ timing / spacing
→ contact causality
→ secondary motion
→ runtime fidelity
→ measured optimization
```

A downstream stage must never be used to hide an upstream failure.

Examples:

- bad Carol silhouette → return to model/volume; do not fix with texture
- scary gaze → fix eye geometry/range/head-eye coordination; do not add sparkles
- rubber joint → fix rig/weights/corrective; do not slow the animation
- weak touch causality → fix local reaction/pose composition; do not add VFX
- jelly fleece → reduce secondary freedom and restore authored mass control; do not damp an incorrect physics-led rig forever

---

# 2. Canonical system — identity canonical vs 3D production canonical

## 2.1 Do not destructively replace the original identity canonical

The current single-view artworks contain the strongest approved identity signal: face, proportions, color hierarchy, silhouette language and motifs. A newly generated turnaround necessarily invents unseen information. Therefore the correct system is **two-layer canonical authority**, not destructive replacement. [G]

### Layer 1 — Identity Canonical

Files:

- `assets/grimo/source/carol/carol-Identity-canonical.png`
- `jill-identity-canonical.png`
- `pino-identity-canonical.png`
- `shushu-identity-canonical.png`

Authority:

- face identity
- front/front-3-quarter appeal
- palette
- motif identity
- large/medium/small shape language
- canonical emotional impression

### Layer 2 — 3D Production Canonical

Files after explicit user approval:

- `carol-3d-production-canonical.png`
- `jill-3d-production-canonical.png`
- `pino-3d-production-canonical.png`
- `shushu-3d-production-canonical.png`

Authority:

- approved front/3-quarter/side/back geometry
- attachment roots
- hidden anatomy
- prop vs anatomy separation
- rig-neutral support pose
- orthographic proportions
- approved asymmetry that must survive modeling

### Conflict rule

If an approved 3D production sheet contradicts the identity canonical in visible identity, **Identity Canonical wins** and the 3D production sheet must be regenerated/revised. Hidden geometry is governed by the latest user-approved 3D production canonical.

## 2.2 Production canonical requirements

Each 3D production canonical must:

- show the same character in consistent scale across views;
- use orthographic or near-orthographic neutral presentation;
- contain front, front 3/4, left/right profile and back information;
- use a character-native neutral support pose, **not** a forced humanoid T-pose;
- remove detached atmosphere that is not anatomy;
- separate handheld/scene props into explicit callouts where they occlude anatomy;
- preserve original eye size, face/body ratio and motif placement;
- avoid adding speculative anatomy just because it is realistic;
- reveal the minimum hidden structure required for rigging and animation;
- contain no dramatic perspective, depth of field or cinematic lighting;
- be approved by the user before it can constrain Blender work.

This directly addresses the largest current open technical risk in the Experience / Motion Bible: exact unseen geometry that preserves the sacred visible identity. [G]

---

# 3. Character anatomy contracts — corrected from the actual canonical images

These contracts intentionally avoid inventing body parts that are not visually supported.

## 3.1 Carol

### Visible identity

- young sheep-like dream-cloud Grimo;
- extremely large white / pale-blue / pale-lilac cloud fleece;
- tiny cream face embedded in the fleece;
- extremely large glossy amber/brown eyes;
- brown ears with warm pink inner ear;
- short, dark-brown heavy hooves visible below the fleece;
- crescent moon motif embedded on the viewer-left fleece region;
- multiple attached yellow star motifs within/on the fleece;
- additional detached clouds/stars/sparkles in the original illustration are **atmosphere**, not automatically anatomy;
- **no production tail is to be invented unless a later approved 3D canonical defines one.**

### Production body grammar

- low, grounded support mass;
- hidden torso exists as a deformation/support chassis, not as a realistic sheep body to expose;
- face/head is a primary acting region;
- fleece is a dominant silhouette shell/cluster system that follows primary action rather than leading it;
- hooves must retain apparent weight and ground contact.

### Forbidden drift

- realistic sheep proportions;
- long visible legs;
- strand-fur realism that changes the cloud silhouette;
- global soft-body jelly;
- whole-body breathing balloon;
- invented wagging tail;
- moon/star effects acting continuously.

## 3.2 Jill

### Visible identity

- young light-green dragon-like Grimo;
- large rounded head/body and huge glossy green eyes with star-like highlights;
- pale cream/yellow segmented belly;
- two small-to-medium wings with yellow/cream membranes;
- short forelimbs held near the upper belly/chest;
- large seated hindquarters / feet;
- long thick curved tail forming a major silhouette arc;
- dense leaf crest / leafy back ornament with white flowers;
- clover motif on the thigh/body region;
- detached leaves, butterfly and sparkles in the illustration are atmosphere unless explicitly attached in the production canonical.

### Production body grammar

- seated/mixed dragon support, not generic upright humanoid;
- intention originates around chest/upper body;
- wings are episodic expressive channels, never constant insect flapping;
- foliage follows after primary torso/wing action;
- tail is a heavy rooted mass with delayed follow-through.

### Forbidden drift

- long ground-reaching forelegs;
- generic western-dragon anatomy;
- permanent wing flap;
- lightweight cat-tail wag;
- every leaf independently oscillating.

## 3.3 Pino

### Visible identity

- young blue otter-like Grimo;
- round soft body;
- cream lower face and very large cream belly;
- small round ears;
- one large glossy blue eye visible open in the current identity illustration and the opposite eye winking/closed in that specific pose;
- short forepaws/arms holding a central iridescent bubble in the identity artwork;
- hind feet presented forward with blue/pink paw pads;
- very large thick blue tail on the viewer-left side;
- water splash around the seated body and detached iridescent bubbles are scene/atmosphere unless a production sheet explicitly attaches a water element.

### Production body grammar

- grounded seated soft-heavy mass;
- arms naturally move inward/hugging;
- body may compress but must never read as hollow inflatable plastic;
- thick tail is a delayed heavy secondary mass;
- bubble is a **separate prop**, not fused into anatomy.

### Forbidden drift

- generic blue sphere;
- fast cat-like tail;
- uniform squash/stretch;
- transparent photoreal soap-bubble rendering that breaks the canonical art direction;
- water splash treated as permanent body geometry without explicit approval.

## 3.4 Shushu

### Visible identity

- young white-and-cherry-pink panda-like Grimo;
- round white face/body;
- round pink ears;
- pink arms and legs/feet;
- large glossy pink/brown eyes with flower-shaped highlight/motif;
- large forward-facing seated feet with visible pads;
- flower crown crossing the head/top silhouette;
- bouquet/flower cluster held at the chest by both arms;
- detached petals, flowers and butterflies are atmosphere;
- **no long tail is visible and none may be invented without a later approved 3D production canonical.**

### Production body grammar

- grounded seated plush mass;
- arms must preserve believable bouquet contact when the bouquet is present;
- head/eyelid leads subtle emotion;
- body settles softly and slowly;
- crown/bouquet/flowers follow primary body emotion as delayed secondary structures.

### Forbidden drift

- added long tail;
- long thin limbs;
- bouquet floating or detached from hands;
- flower-eye motif destroyed by facial morphs;
- springy stuffed-toy bounce;
- constant flower shaking.

---

# 4. Canonical → 3D reconstruction method

## 4.1 Sacred-view method

For each character, lock an approved **canonical camera** matching the identity artwork as closely as practical. During blockout:

1. place identity image as reference;
2. estimate camera projection/FOV only as much as needed to match visible proportions;
3. build primary masses in clay material;
4. render from the canonical camera after every substantial geometry change;
5. compare silhouette, landmarks and negative spaces;
6. expand to 3/4/profile only after canonical identity passes.

### Professional decision rule

When plausible 3D anatomy and canonical appearance conflict:

> **Preserve canonical appearance inside the required camera/animation envelope.**

A controlled art-direction cheat is valid if it does not break approved off-axis views, deformation or contact. A more anatomically correct mesh that makes the Grimo less itself is a failure. [G]

## 4.2 Shape hierarchy

Work in this order:

1. **Primary:** overall silhouette, head/body mass, support footprint, tail/wing/fleece macro-shape
2. **Secondary:** face plane, cheek/muzzle, limbs, wing thickness, leaf/fleece clusters, ears
3. **Tertiary:** pads, small flowers, texture relief, seam/detail, small motif bevels

No tertiary polish may delay correction of a primary-form failure.

## 4.3 Expression testing before topology lock

Before final retopo, build enough temporary facial deformation to test:

- blink;
- content eye-close;
- small smile/content mouth;
- mild discomfort;
- approved gaze extremes;
- one touch-oriented cheek/head lean.

If the character becomes off-model, fix underlying volume before production topology is frozen. Blender Studio's production documentation explicitly treats animation testing as feedback to modeling/rigging rather than a one-way downstream step. [B]

---

# 5. Modeling and sculpting doctrine

## Recommended

- primitive/low-density blockout for proportion exploration;
- subdivision/poly modeling for controllable hard/soft stylized structures;
- sculpt/multires for shape exploration and final organic surface where useful;
- Voxel Remesh/Dyntopo only as design tools before final retopo where topology freedom is useful;
- manual retopo or strongly supervised retopo assistance for deformation-critical areas;
- separate meshes where part boundaries, material, deformation or runtime control justify separation.

## Reject

- generic species base meshes that pull characters toward ordinary sheep/dragon/otter/panda anatomy;
- automatic remesh as final topology simply because it is fast;
- hundreds of small geometric wool/leaf/flower pieces without a clear silhouette or deformation purpose;
- hidden detail more elaborate than visible identity;
- symmetry maintained after it harms approved asymmetry/appeal.

---

# 6. Production topology doctrine

## 6.1 Quads are an authoring strategy, not a runtime law

Use quad-centric edge flow in deformation-critical authoring regions because it is easier to edit, sculpt, subdivide and reason about. But glTF export triangulates quads/n-gons. Therefore every accepted asset must pass **post-triangulation** visual/deformation QA. [A/G]

## 6.2 Density follows deformation and silhouette importance

Prioritize topology around:

- eyelids and eye socket;
- cheek/muzzle/mouth region;
- ear/wing roots;
- limb roots and deep bends;
- Carol fleece zones that must locally compress/lean;
- Jill tail root / wing root;
- Pino tail root / seated compression;
- Shushu arm/bouquet contact and seated plush compression.

Reduce density in hidden or rigid regions that do not affect silhouette/deformation.

## 6.3 Ownership rules

| Visual change | Primary owner |
|---|---|
| permanent silhouette / visible volume | mesh geometry |
| articulated reusable movement | bones |
| designed nonlinear local deformation | shape key / corrective morph |
| color / painted motif / micro-detail | texture/material |
| eye/head target adjustment, small compositional offsets | runtime procedural control |
| residual lag after authored motion | bounded secondary system |
| key pose / emotional peak | authored animation, never raw physics |

---

# 7. Eye and face system

## 7.1 Objective

Maximize readable expression while minimizing identity drift.

## 7.2 Eye construction rule

Do not force realistic eyeball anatomy. Test a small set of production prototypes:

- stylized partial sphere/ellipsoid with art-directed iris;
- shallow curved eye surface with independent iris/pupil control;
- geometry + texture hybrid;
- explicit canonical highlights when physically generated highlights cannot reproduce identity reliably.

Select the approach that best preserves:

- eye silhouette;
- iris/pupil size;
- canonical highlight identity;
- blink shape;
- profile/3-quarter appearance;
- gaze readability on a phone screen.

## 7.3 Identity Envelope

Every facial parameter must have an approved range. At minimum:

- gaze X/Y;
- convergence for close contact;
- blink L/R;
- half-lid/content close;
- squint;
- cheek raise/compress;
- small smile/content mouth;
- mild discomfort/protest;
- mouth open only as far as identity allows.

No human-style eyebrow/FACS freedom is added unless the canonical design actually supports it.

## 7.4 Blink is a designed expression

A blink must preserve:

- eye corners;
- face silhouette;
- cheek relation;
- closed-eye appeal;
- reopen timing.

A mechanically rotating eyelid that merely covers the eyeball is not sufficient.

---

# 8. Rig architecture

## 8.1 Three logical layers

```text
Animator / Control Rig
    ↓ drives
Deformation Rig
    ↓ baked/mapped to
Export / Runtime Rig
```

They may coexist in one `.blend`, but their responsibilities remain distinct.

### Animator / Control Rig

- animator-friendly semantic controls;
- FK/IK where useful;
- parent/space switching;
- facial actions/presets;
- non-export helpers;
- high-level fleece/tail/wing controls;
- limits that protect identity.

### Deformation Rig

- deform bones actually affecting meshes;
- helper/twist/volume bones where needed;
- predictable hierarchy;
- corrective drivers in Blender as authoring tools.

### Export Rig

- minimum runtime-relevant bone hierarchy;
- stable names;
- no unnecessary animator control bones;
- baked supported transforms;
- exported morph targets only where runtime needs them.

## 8.2 CloudRig decision

**CloudRig is a strong production-proven candidate, not an automatic mandate.** Blender Studio currently uses it to generate control rigs and explicitly combines generated rigs with manual weight painting and corrective shape keys. [B]

For Carol Phase Rig Prototype:

- prototype A: CloudRig-derived custom metarig;
- prototype B: compact custom rig if CloudRig complexity/export indirection becomes a liability.

Choose after comparing:

- pose usability;
- facial setup;
- custom fleece controls;
- deterministic regeneration;
- export-rig cleanliness;
- Codex automation;
- maintenance/version risk.

### Version rule

Pin exact CloudRig version in the project lockfile/manifest for an accepted character. Never auto-update an accepted production rig. CloudRig 2.2.28 itself documents backwards-compatible breakages. [A]

---

# 9. Skinning and corrective deformation

## 9.1 Auto weights are only a starting point

Blender Studio's current production documentation describes manual weight painting after rig generation and corrective shape keys as a final deformation-polish layer. [B]

Grimo policy:

```text
auto weights (optional first pass)
→ manual weight refinement
→ stress poses
→ corrective shapes / helper deformation where justified
→ combined-pose tests
```

## 9.2 Preserve Volume / dual-quaternion behavior

Blender's Armature modifier `Preserve Volume` can reduce rotational volume loss, but it is not a universal fix and must be validated against stylized shapes and export behavior. Do not assume Blender viewport deformation automatically equals final runtime deformation. [A]

## 9.3 Weight normalization

Use normalization tools deliberately. Blender internally evaluates deform-bone weights relatively; Auto Normalize is a workflow aid, not an artistic quality guarantee. [A]

## 9.4 Correctives

Corrective shape keys/pose-driven correctives are approved for:

- deep limb bends;
- shoulder/hip root volume;
- eyelid/cheek combinations;
- mouth/cheek combinations;
- Carol fleece compression/intersection avoidance;
- Jill wing root / tail root;
- Pino seated belly/hip compression;
- Shushu arm/bouquet contact and plush body compression.

Blender's driver/shape-key tools and Blender Studio's corrective workflow support this production pattern. [A/B]

---

# 10. Deformation stress-test suite

Every production rig must render/capture at minimum:

1. neutral canonical pose;
2. head yaw left/right;
3. head pitch up/down;
4. head roll;
5. approved gaze extremes;
6. blink left/right/both;
7. content eye-close;
8. squint;
9. small smile/content face;
10. mild discomfort face;
11. cheek lean/compression L/R;
12. ear extremes;
13. primary limb extremes;
14. seated/deep compression where applicable;
15. weight shift / support transfer;
16. character-specific appendage extremes;
17. combined hero pose;
18. triangulated/export-rig reproduction.

### Failure examples

- face becomes a different character;
- eye white exposure becomes frightening/human;
- fleece or belly loses volume;
- wing/tail root looks detached;
- hoof/feet slide or float;
- bouquet loses hand contact;
- tail/ear/fleece penetrates the body;
- correct pose exists only in control-rig viewport but fails on export rig.

Any such failure returns to the earliest responsible stage.

---

# 11. Lookdev doctrine

## 11.1 Goal

Match canonical readability and softness under realtime lighting. Physical realism is subordinate.

## 11.2 Material policy

Use glTF-friendly stylized PBR where it suffices; use runtime custom shading only when canonical identity materially requires it.

Prefer:

- controlled base color;
- restrained roughness/specular;
- carefully designed eye highlights;
- normal/detail only where it improves form without visual noise;
- face readability under multiple practical light conditions;
- low material count when visually equivalent.

Avoid:

- realistic animal fur replacing designed forms;
- physically correct reflections that destroy eye motifs;
- complex Blender-only node graphs with no runtime reproduction plan;
- hard cel outlines/shadows merely because they look “game-like” if they diverge from canonical softness.

---

# 12. Carol dream-cloud fleece system

## 12.1 Recommended production architecture

Start from:

```text
coherent master fleece silhouette
+
sparse major regional masses/controls
+
broad deform bones and/or lattice-like authoring controls
+
corrective morphs for local compression / intersections
+
authored secondary follow-through
+
very limited runtime residual if later proven safe
```

The exact implementation is not locked until Carol prototypes prove it.

## 12.2 Required properties

- front sacred silhouette remains stable;
- local touch can deform a region without collapsing the whole mass;
- head/body motion can transfer into fleece with delayed follow-through;
- hooves and face remain readable;
- volume stays visually coherent;
- settle stops cleanly when emotion has settled;
- no independent random tuft chatter.

## 12.3 Reject

- whole-fleece Soft Body as primary acting system;
- cloth-driven key poses;
- hundreds of independent wool balls;
- perpetual spring motion;
- full-body scale-breathing;
- secondary motion beginning before the face/head/hidden torso establishes intent.

---

# 13. Character-specific rig/motion implications

## Carol

- primary: face/head, hidden torso/COM, hooves;
- secondary: ears, fleece regional masses, attached motif residual;
- support: low/heavy/grounded;
- invitation/contact: cheek/forehead/head offer rather than invented tail behavior.

## Jill

- primary: chest/upper body, head, short forelimbs, wing pose;
- secondary: foliage/flowers, wing follow-through, heavy tail delayed;
- support: seated/mixed with strong hind mass;
- do not normalize into a biped humanoid dragon.

## Pino

- primary: soft torso, arms/paws, head/gaze;
- secondary: thick heavy tail, optional event-specific water accents;
- support: seated soft-heavy;
- held bubble is an independent prop when present.

## Shushu

- primary: head/eyelid, torso plush compression, arms/hand contact;
- secondary: ears, crown, bouquet, flowers;
- support: seated/grounded;
- no invented tail.

Shared production contracts are allowed; shared personality animation is not.

---

# 14. Professional animation workflow

The required workflow is:

```text
behavior intent
→ reference
→ key poses
→ silhouette / support check
→ stepped blocking
→ breakdown poses
→ timing / spacing
→ spline
→ arcs / overlap / contact
→ face / eyes
→ secondary
→ polish
→ playblast review
→ revision
```

Blender 5.2 documentation explicitly describes Constant interpolation as commonly used for initial pose-to-pose blocking; Blender Studio's animation-testing pipeline stress-tests rigs and feeds failures back into rigging/modeling. [A/B]

## 14.1 Key rule

Every **meaning-bearing** keyframe must have a reason.

Do not begin with noise, sinusoidal motion or an automatically smoothed curve and call the result life.

## 14.2 Weight and contact

Before polish, verify:

- support footprint;
- COM shift;
- planted contact;
- acceleration/deceleration appropriate to body mass;
- no root floating;
- no foot/hoof sliding during holds;
- appendage follow-through occurs because primary mass moved.

---

# 15. Graph Editor doctrine

Blender 5.2's Graph Editor provides Constant/Linear/Bezier interpolation, Auto/Auto-Clamped/Vector/Aligned/Free handles, Continuous Acceleration smoothing, decimation and Euler discontinuity filtering. These are mechanisms, not automatic taste. [A]

## 15.1 Grimo curve rules

- pose time/value first; interpolation second;
- use Constant during blocking where appropriate;
- use Bezier only after pose/timing intent is accepted;
- Auto Clamped is a safe starting handle, not a final guarantee;
- asymmetric tangents are allowed/encouraged when motion demands asymmetric arrival/departure;
- preserve intentional flat holds;
- no periodic `sin/cos/noise/random` on primary acting channels;
- no dense every-frame keys unless generated by an approved bake;
- if baked, reduce only after rendered motion comparison;
- use Euler filtering only as a repair tool for Euler discontinuity/gimbal artifacts, not as performance polish.

## 15.2 Good motion structure example

```text
anticipation
→ commitment
→ peak
→ small justified overshoot
→ asymmetric return
→ moving hold or true hold
→ settle
```

Not every action needs all stages.

## 15.3 Mechanical warning patterns

- all channels same phase;
- identical duration/ease on face/head/torso/appendages;
- fixed-frequency idle;
- same overshoot percentage everywhere;
- all channels move simply because time passed.

---

# 16. Living idle — authoritative motion integration

The Experience / Motion Bible governs idle grammar. The goal is not to keep the body moving. Partner Eevee/Pikachu observations support long quiet states and selective channel recruitment. [V]

Correct model:

```text
persistent internal state / motive
→ long intentional stillness or moving hold
→ sparse context-specific micro event
→ attention or posture phrase when motivated
→ settle / afterglow
```

### Required rules

- no whole-body bob as the core idle;
- no fixed cycle that repeats every few seconds;
- no permanent user stare;
- only necessary channels participate;
- gaze, eyelids, head, ears/appendages and body may operate at different cadences **because of state/cause**, not random phase offsets;
- recent behavior history suppresses obvious repetition.

Carol 15–30s no-input Gate must include quiet intervals and still feel alive.

---

# 17. Touch-causal acting

Author reactions around causality, not clip lookup.

General grammar:

```text
contact / gesture
→ immediate local acknowledgement
→ evaluation / attention
→ face / head intent
→ local-to-global body response when justified
→ secondary follow-through
→ settle
→ emotional afterglow
→ living-state transition
```

Not every behavior uses every stage.

## 17.1 Preserve contact information

Runtime state must retain:

- touch side;
- local position;
- direction;
- speed;
- duration;
- recent touch history.

Do not collapse left/right touch into one centered full-body reaction.

## 17.2 Blender-authored vs runtime

### Author in Blender

- key emotional poses;
- head/cheek/body contact-seeking poses;
- body weight transfer;
- hero reactions;
- major boundary/withdrawal phrases;
- designed local deformation morphs;
- major secondary timing where essential to silhouette.

### Runtime procedural

- gaze target within approved envelope;
- blink scheduling/state;
- small head/eye compositional adjustment;
- touch-driven blend weights;
- behavior selection/history/interruption;
- strictly bounded residual follow-through proven safe.

### Hybrid

- runtime selects/blends authored side-conditioned poses and morphs;
- runtime provides target location/intensity, authored rig defines visually safe solution.

---

# 18. Emotional afterglow and interruption

A reaction must not automatically reset to neutral after 1–2 seconds.

Partner analyses show emotion can persist after the peak. Grimo therefore uses:

```text
peak
→ settle
→ afterglow state
→ changed living idle / new motive / gaze release / invitation / quiet hold
```

All behavior must be interruptible according to channel ownership and safe redirect rules. New input should redirect current behavior where appropriate rather than endlessly queue canned clips. [V/G]

---

# 19. Animation library architecture

## 19.1 Blender

Use Actions/Action Slots/NLA as authoring containers, but do not force runtime state structure to mirror Blender exactly.

Example semantic families:

- `IDLE_*`
- `GAZE_*`
- `FACE_*`
- `TOUCH_HEAD_*`
- `TOUCH_CHEEK_L/R_*`
- `BOUNDARY_*`
- `INVITE_*`
- `HERO_*`
- `SETTLE_*`

Left/right may be mirrored only when the result remains visually correct; asymmetric motifs/props may require separately polished actions.

## 19.2 Runtime

PlayCanvas state graphs/layers/masks are appropriate for independently composable body/face/additive channels. Current docs support multiple layers, Override/Additive blending and layer masks. [A]

Do not assume a generic humanoid “upper/lower body” split. Masks are character-specific semantic regions.

---

# 20. Blender → glTF/GLB contract

## 20.1 Current verified compatibility

| Blender concept | glTF/GLB outcome | Grimo rule |
|---|---|---|
| object TRS | supported | export directly |
| pose-bone animation | supported | export/bake from control rig to runtime bones |
| armature skinning | supported | validate final runtime deformation |
| shape keys | morph targets | export only approved runtime morphs |
| shape-key animation | supported | reset between actions where needed |
| multiple animations | supported | choose exporter mode intentionally |
| constraints | not runtime constraint logic | bake/evaluate into supported transforms |
| drivers | not portable logic | bake or reimplement in runtime |
| B-Bones | Blender-specific control/deformation semantics | bake/map result to ordinary export bones; never assume B-Bone semantics survive |
| lattice | not glTF runtime deformer | apply/bake to mesh/morph/bones |
| Geometry Nodes graph | not portable as Blender graph | realize/apply or reproduce runtime logic |
| cloth/soft-body simulation | not glTF live physics | bake to supported animation or reimplement bounded runtime physics |
| Blender custom shader graph | only glTF-recognized material subset/extension portable | build runtime material explicitly |
| custom properties | can export as `extras` when enabled | use only if PlayCanvas ingestion path is validated; critical metadata also in sidecar manifest |
| animation markers | not a general standard event contract | store event metadata in Grimo sidecar/authoring manifest |
| quads/n-gons | triangulated | QA triangulated result |

Blender 5.2 supports animation export modes including Actions, Active Actions merged, NLA Tracks and Scene; shape key animation and deformation-bones-only export are current exporter options. [A]

## 20.2 Morph-target correction

Never encode a hard “8 morph target maximum” rule in Grimo. glTF 2.0 explicitly says morph-target count is not limited. Runtime/device cost must be profiled. [A]

---

# 21. PlayCanvas runtime contract

Current PlayCanvas documentation/API confirms:

- Anim State Graph assets;
- multiple layers;
- Override/Additive blending;
- per-layer masks;
- runtime layer weights;
- morph target instances and per-target weights;
- skin instances.

Therefore the Blender asset must expose semantic, stable bones/morphs suitable for runtime control.

Recommended runtime layers are conceptual, not fixed:

```text
BASE_BODY
FACE_EXPRESSION
GAZE_HEAD
TOUCH_LOCAL
REACTION_ADDITIVE (only where safe)
SECONDARY_RESIDUAL
```

Character-specific masks and ownership must be validated in PlayCanvas rather than assumed from one shared skeleton.

---

# 22. Performance policy

## 22.1 Do not lock invented asset budgets before profiling

Do **not** make 20–50k triangles, 50 bones, 10–20 morphs, 10 draw calls, etc. authoritative simply because they sound plausible.

The Minimum Requirements demand practical Pixel 7a-class PWA performance, sustained frame pacing, input latency, memory/load and thermal feasibility. Exact ceilings remain a prototype question. [G]

## 22.2 Target policy

- **Experience target:** 60 fps where practical; frame-time stability is more important than a misleading average.
- 30 fps may be an explicit degraded/fallback mode only if the final experience remains acceptable; it is not the initial artistic acceptance target.
- build the highest-quality Carol master required for the visual/animation gate;
- profile on target device;
- identify measured bottleneck;
- optimize that bottleneck;
- run visual regression;
- lock budgets only after real evidence.

## 22.3 Metrics to capture

- CPU frame time;
- GPU frame time where accessible;
- sustained FPS/frame pacing;
- input-to-visible-response latency;
- draw calls;
- triangles/vertices after glTF triangulation/splits;
- deform-bone count;
- skin influences;
- active morph count/cost;
- texture GPU memory;
- GLB size/load/decode time;
- thermal soak behavior;
- battery impact where practical.

---

# 23. AI Agent / Codex operating model

## 23.1 Preferred automation hierarchy

```text
versioned source + specifications
→ deterministic bpy/Python builders & validators
→ headless/background Blender tasks where suitable
→ reproducible renders/playblasts/exports
→ image/video/data comparison
→ diagnosis
→ smallest controlled correction
→ Human Gate
```

GUI/MCP interaction remains useful for genuinely visual sculpt/pose tasks, but opaque mouse imitation is not the production backbone.

## 23.2 AI may own

- file/hierarchy/naming setup;
- canonical camera setup;
- measurement extraction;
- repetitive rig/control generation;
- first-pass weight operations;
- export-rig generation/baking;
- GLB export;
- validation;
- batch turntables/playblasts;
- regression captures;
- curve anomaly detection;
- key density/periodicity checks;
- device telemetry collection;
- bounded variant generation.

## 23.3 AI first pass + Human Gate

- blockout volumes;
- unseen geometry proposals;
- topology proposals;
- rig architecture selection;
- final weights/correctives;
- facial morph design;
- animation blocking;
- secondary timing;
- visible optimization.

## 23.4 Human final authority

- “this is Carol/Jill/Pino/Shushu”;
- silhouette appeal;
- eye appeal;
- expression identity;
- hero pose;
- emotional acting;
- timing/spacing taste;
- acceptable stylization cheat;
- whether secondary motion helps or distracts;
- final runtime experience.

---

# 24. Automated QA — detector, never judge

Approved automated detectors include:

- canonical silhouette overlap from matched camera;
- landmark deviations;
- eye/face/body ratios;
- negative-space comparison;
- support contact/foot slide;
- self-intersection;
- joint volume change;
- morph range violations;
- periodic-motion detection;
- cross-channel correlation/synchronization;
- velocity/acceleration outliers;
- key density;
- bone/morph/mesh/material counts;
- GLB validator errors;
- Blender→GLB pose/capture regression;
- runtime screenshot/video regression;
- frame timing/load/thermal telemetry.

A metric can fail a build automatically for technical invalidity. A metric can **never** force artistic PASS over a Human FAIL.

---

# 25. Professional review loop

Every phase follows:

```text
create
→ capture evidence
→ compare against authority
→ identify symptom
→ diagnose earliest owning stage
→ correct upstream
→ recapture
→ Human Gate
```

Required review forms:

- canonical camera overlay;
- black silhouette;
- clay render;
- front/3-quarter/profile/back production views;
- eye close-up;
- facial expression sheet;
- wireframe/topology where relevant;
- deformation stress-test grid;
- stepped blocking playblast;
- spline playblast;
- slow-motion/frame-by-frame review;
- sound-off acting review;
- secondary-off vs secondary-on comparison;
- Blender control-rig vs export-rig capture;
- GLB/PlayCanvas comparison;
- real-device capture.

---

# 26. Failure diagnosis dictionary

| Symptom | Likely owner | Required response |
|---|---|---|
| generic AI mascot | blockout/model | restore canonical ratios, silhouette, asymmetry; remove generic species anatomy |
| front right, 3/4 wrong | volume/camera | rebuild unseen volume/camera cheat; do not texture-patch |
| scary eyes | eye system | reduce gaze envelope/white exposure; adjust eye depth/highlight/head assistance |
| blink changes identity | face model/morph | redesign lid/cheek closed shape |
| expression becomes another character | facial envelope | reduce range/redesign shapes/correct combinations |
| joint collapse | topology/weight/corrective | repair weights/helper/corrective; no animation patch |
| rubber limb | rig/stretch/timing | disable inappropriate stretch, fix joint/spacing/support |
| floating body | pose/COM/contact | rebuild support and weight transfer |
| mechanical motion | blocking/timing/curves | return to intent/key pose/timing; remove generic easing/noise |
| all parts move together | channel design | restore lead/follow hierarchy and selective recruitment |
| constant movement | idle scheduler/authoring | add stillness; remove oscillators |
| Carol fleece jelly | fleece rig/secondary | stabilize master silhouette; reduce/global physics; author clusters |
| Jill insect-like | wing/secondary | episodic wing action; chest lead; heavy tail |
| Pino balloon | body deformation | weighted seated compression, nonuniform designed squash, heavy tail |
| Shushu sad when idle | expression/state | calm neutral eyelids/posture; avoid downward gaze as default |
| touch side unreadable | touch composition | preserve local side through pose/morph selection |
| reaction snaps neutral | state/animation | authored settle + afterglow + living-state transition |
| Blender great, GLB bad | export contract | compare triangulation/normals/bone bake/morph/material export |
| desktop great, phone bad | optimization | profile measured bottleneck; reduce only with visual regression |

---

# 27. Carol vertical-slice execution plan

## Phase 0 — Authority and version lock

**Deliverables:** identity canonical hash; approved production-canonical status; Blender 5.2.1 LTS pin; extension pins; project coordinate/unit/export policy.  
**Gate:** no Blender authoring before authority is unambiguous.

## Phase 1 — Identity measurement

Measure silhouette, eye centers/size, face/fleece ratio, ear positions, hoof visibility, moon/star anchors, negative spaces.  
**Human:** confirms which measurements are identity-critical.

## Phase 2 — 3D production canonical

Use user-approved multi-view sheet. Resolve hidden torso/ear/hoof/fleece attachment without adding unsupported anatomy.  
**Gate:** user approves all required views.

## Phase 3 — Blockout

Primary volumes only. Canonical camera fixed.  
**PASS:** unmistakably Carol in clay from canonical view.

## Phase 4 — Volume gate

Front + approved 3/4/profile views.  
**FAIL:** if off-axis turns into generic sheep/cloud ball.

## Phase 5 — Early expression stress test

Temporary blink/content/smile/gaze/cheek-lean.  
**Purpose:** expose bad face volume before retopo.

## Phase 6 — Final model/sculpt

Resolve primary/secondary forms; no unnecessary micro-fur.

## Phase 7 — Production retopo

Deformation-driven topology; preserve silhouette; record final triangulated QA later.

## Phase 8 — UV/lookdev

Canonical palette/material readability; eye lookdev priority.

## Phase 9 — Rig prototype comparison

CloudRig-derived custom metarig vs compact custom rig if needed.  
**Decision:** choose only after actual Carol control/export test.

## Phase 10 — Skinning

Auto only if useful as first pass → manual refinement.

## Phase 11 — Corrective deformation

Pose-specific fixes; Carol fleece/face/limbs.

## Phase 12 — Final eyes/face

Identity Envelope locked by approved expressions and gaze extremes.

## Phase 13 — Deformation stress test

All standard + Carol-specific poses; capture grid.

## Phase 14 — Neutral support / COM

Carol must read heavy-hoof grounded before life motion.

## Phase 15 — Living idle

15–30s; long stillness allowed; no oscillator life system.

## Phase 16 — Gaze / blink / attention

Runtime-compatible approved envelope; no constant user stare.

## Phase 17 — Semantic touch local reflex

Immediate local ACK for head/cheek/fleece zones.

## Phase 18 — Contact-seeking

Head/cheek moves toward accepted contact; side preserved; fleece follows.

## Phase 19 — Autonomous invitation + WAIT

Character initiates and can patiently wait without full-body motion.

## Phase 20 — Boundary / withdrawal

Mild, non-hostile, grounded withdrawal; afterglow preserved.

## Phase 21 — Hero reaction

One larger authored emotional phrase; sound-off acting must pass.

## Phase 22 — Interruption / redirect

New input can safely redirect behavior without pop/snap/queue spam.

## Phase 23 — Variation / repetition suppression

Family/history/context variation rather than clip-count inflation.

## Phase 24 — Secondary fleece

Primary acting locked first; compare secondary off/on.

## Phase 25 — Export rig + GLB

Bake/export, glTF validation, morph/bone/animation manifest, triangulated capture.

## Phase 26 — PlayCanvas integration

State graph/layers/masks/touch/gaze/interruption.

## Phase 27 — Pixel 7a-class real-device profiling

Measure before locking budgets. 60fps experience target where practical.

## Phase 28 — Optimization + regression

Optimize measured bottlenecks only; visual/motion regression mandatory.

## Phase 29 — Final Companion Gate

Several minutes of interaction must no longer feel like a technical demo or canned puppet.

Only after PASS may the architecture expand to Jill. Jill is the preferred second character because wings + foliage + heavy tail stress-test generality.

---

# 28. Human Gate system

## Gate A — Canonical Identity
Neutral Carol is unmistakably Carol.

## Gate B — 3D Volume
Approved off-axis views preserve identity and attachment logic.

## Gate C — Face / Eyes
Blink, gaze and expressions stay inside identity envelope.

## Gate D — Deformation
No collapse, rubber, float, ugly compression or bad intersection.

## Gate E — Living Idle
15–30s feels alive while allowing real stillness.

## Gate F — Touch Causality
The viewer can read where contact occurred and how response propagated.

## Gate G — Hero Acting
Performance reads as professionally authored with sound/VFX off.

## Gate H — Runtime Fidelity
GLB/PlayCanvas preserve the approved Blender performance.

## Gate I — Smartphone
Target-class device preserves responsiveness, frame pacing and visual quality.

## Gate J — Companion Experience
Several minutes sustain agency, responsiveness, variation and character identity.

**Human FAIL always overrides automated PASS.**

---

# 29. Versioning / reproducibility

## 29.1 Pin now

- Blender: **5.2.1 LTS**
- CloudRig: only if selected after prototype; pin exact accepted version (current observed 2.2.28)
- EasyWeight / Pose Shape Keys: pin exact versions if adopted
- PlayCanvas engine/runtime: pin exact project version at implementation lock
- glTF exporter settings: serialize/export preset and commit it

## 29.2 Never silently migrate accepted rigs

Any Blender/extension/runtime upgrade requires:

1. duplicate branch;
2. deterministic re-export;
3. deformation capture comparison;
4. animation regression;
5. GLB validation;
6. device validation where runtime changed;
7. Human Gate for visible differences.

## 29.3 Asset structure

Suggested per-character structure:

```text
characters/carol/
  canonical/
    carol-Identity-canonical.png
    carol-3d-production-canonical.png
    authority.json
  blender/
    carol-master.blend
    scripts/
    presets/
  textures/
  manifests/
  qa/
    canonical/
    clay/
    deformation/
    animation/
    export/
    runtime/
  export/
    carol.glb
    carol.manifest.json
```

Binary asset strategy may use Git LFS or equivalent; source hashes and accepted-export hashes are mandatory.

---

# 30. Final one-page operational doctrine

## Grimo 3D must always

1. start from approved identity authority;
2. use the user-approved 3D production canonical for hidden geometry;
3. protect silhouette and face before detail;
4. test expression before final topology lock;
5. design topology for deformation, not quad aesthetics;
6. separate animator/control needs from runtime/export needs;
7. manually refine deformation where auto methods fail;
8. use correctives when stylized deformation demands them;
9. author primary acting before secondary dynamics;
10. give every meaning-bearing motion a cause;
11. preserve support/COM/contact;
12. allow intentional stillness;
13. preserve afterglow and interruption;
14. validate Blender → export rig → GLB → PlayCanvas → phone;
15. measure before optimization;
16. let Human Gate decide final aesthetic quality.

## Grimo 3D must never

1. turn the Grimo into a generic species model;
2. invent unsupported body parts;
3. let new turnaround art override visible identity without user approval;
4. use realistic anatomy as the final authority;
5. mistake auto weights for finished skinning;
6. mistake quad topology for runtime quality;
7. let physics determine key pose/silhouette;
8. use whole-body bob/scale breathing as life;
9. use noise/sine/random on primary acting;
10. move every channel all the time;
11. snap reaction peaks directly back to neutral;
12. hide weak acting with VFX;
13. assume Blender-only features survive GLB;
14. encode invented fixed performance budgets as facts;
15. auto-update a production rig/tool version;
16. expand to four characters before Carol proves the system.

## Before modeling

- identity canonical hash locked;
- 3D production canonical approved or explicit unresolved-view limits documented;
- anatomy vs prop vs atmosphere classified;
- canonical camera established.

## Before topology lock

- primary silhouette approved;
- 3D volume approved;
- early blink/gaze/expression stress test passed.

## Before rigging

- deformation requirements documented;
- export contract understood;
- character-specific controls listed.

## Before animation

- neutral support/COM passed;
- face/eyes identity envelope passed;
- deformation stress test passed.

## Before secondary motion

- primary acting passes without secondary;
- silhouette remains readable;
- desired lag has a narrative/physical cause.

## Before export

- unsupported Blender behavior baked/mapped;
- export rig validated;
- shape/bone/action manifest generated;
- triangulated result checked.

## Before Human Gate

- canonical captures;
- playblasts;
- GLB/runtime captures;
- technical validators;
- real-device evidence where applicable;
- known deviations listed explicitly.

## AI may own

repetitive execution, deterministic scene building, export, validation, capture, metrics, regression and first-pass proposals.

## AI requires Human approval

identity volume, face/eye design, hero topology, final deformation, expression envelope, animation blocking, hero timing and visible optimization.

## Human must decide

**Does it still look and feel unmistakably like the same Grimo, and does it feel alive rather than animated?**

---

# 31. Current unresolved questions that must remain unresolved until tested

Do not fabricate answers for:

- exact Carol hidden torso/side/back shape before approved production canonical;
- exact Carol fleece residual lag limit;
- exact touch-anchor robustness under deformation;
- exact Pixel 7a triangle/bone/morph/texture ceiling;
- final gaze/extreme facial ranges;
- final per-character touch preference maps;
- exact runtime cost of chosen eye/fleece/morph implementation;
- final CloudRig-vs-custom-rig choice for Carol.

These are prototype/Human-Gate questions, not documentation gaps to fill by guessing.

---

# 32. Source ledger used for this normalization

## Grimo Project Knowledge

- `GRIMO_TECHNOLOGY_AGNOSTIC_MINIMUM_REQUIREMENTS.md`
- `Grimo Character Production Architecture — Zero-Based Deep Research.md`
- `GRIMO_EXPERIENCE_MOTION_BIBLE.md`
- `GRIMO_PARTNER_PIKACHU_VIDEO_MOTION_ANALYSIS.md`
- `GRIMO_PARTNER_EEVEE_VIDEO_MOTION_ANALYSIS.md`
- current approved Carol/Jill/Pino/Shushu identity canonical images

## Current primary/professional external sources checked on 2026-09-14

- Blender — Blender 5.2 LTS release / LTS pages
- Blender 5.2 LTS Manual — glTF 2.0 exporter
- Blender 5.2 LTS Manual — Armature Modifier / Preserve Volume
- Blender 5.2 LTS Manual — Weight Paint / normalization
- Blender 5.2 LTS Manual — Graph Editor / F-Curve properties / Euler filter / decimation
- Blender 5.2 LTS Manual — corrective shape-key workflow examples
- Blender Studio — Rigging / CloudRig / manual weighting / corrective shape keys
- Blender Studio — Animation Testing / rig stress testing and feedback loop
- Blender Extensions — CloudRig and current version history
- Khronos — glTF 2.0 Specification, Morph Targets
- PlayCanvas Developer Site / Engine API — Anim State Graphs, layers, masks, morph and skin instances

---

**End of authoritative production specification.**
