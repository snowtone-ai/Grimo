# CAROL_GEOMETRY_PARAMETERS.md

**Status:** ACTIVE SUPPORTING GEOMETRY AUTHORITY — FOUR-REFERENCE LOCK  
**Character:** Carol  
**Scope:** Locked Normal/Skin reference geometry, numerical registration, full-spatial support, deformation, attachment, clearance, and motion-readiness constraints  
**Last Updated:** 2026-09-24

---

# 0. Purpose

This file is Carol's **supporting geometry contract**.

It locks the approved Normal/Skin reference package and numerical relationships needed for reconstruction, support, rigging, deformation, attachment, clearance, and motion readiness.

It does **not** define the Product Goal, current production task, or a mandatory geometry-first phase order.

It is not the highest authority for final visible Carol appeal: canonical identity and the actual fleece-included Hero appearance remain above hidden underbody perfection.

The geometry system must nevertheless support the current Grimo architecture:

> **Full-Spatial 3D Living Character Architecture with View-Weighted Polish**

That means Carol's exterior geometry must remain coherent across practical Front / 3/4 / Side / Rear / derived Top exposure and plausible motion, even when only the Front receives maximum Hero polish.

Locked numbers remain authoritative inside their stated geometry/support domain unless a later explicit approved authority changes them.

---

# 1. Authority Hierarchy

## 1.1 Final-use authority order

For production decisions:

1. **Carol canonical identity** — highest authority for final visible Carol-ness, cuteness, softness, proportions, palette relationships, motifs, and appeal.
2. **Approved Normal Front / Normal Side** — locked visible neutral production references.
3. **Fleece-included full-spatial Hero character** — current visible 3D realization, judged with Front priority but multi-view coherence.
4. **HERO_PRIORITY / MOTION_CRITICAL exterior geometry**.
5. **Approved exposed-Hero module sheets** — localized construction helper authority for the ear and hoof modules only:
   - `assets/grimo/source/carol/approved-3d/modules/carol-ear-module-authority.webp`
   - `assets/grimo/source/carol/approved-3d/modules/carol-hoof-module-authority.webp`
   These remain subordinate to canonical identity and the four locked Normal/Skin references and may not redefine whole-character proportions.
6. **Approved Skin / Underbody Front + Skin / Underbody Side + this numerical contract** — supporting underbody authority for support, rigging, deformation, attachment, clearance, and spatial continuity.
7. **FUNCTIONAL_HIDDEN implementation** — functional structure; Hero polish is unnecessary unless the region becomes externally visible.

The four production-reference images remain FINAL / LOCKED. This hierarchy changes their role, not their approved measurements.

## 1.2 Conflict rule

Do not redesign/regenerate the four locked references to solve implementation difficulty.

Do not use old sheets, turnarounds, unapproved AI candidates, whole-character Back/Top/3Q images, or old 3D interpretations as current geometry authority.

The explicitly Human-approved ear/hoof module sheets are a narrow exception: they are localized construction helper authorities for those exposed modules only. Their Front/Side/Top panels constrain one coherent 3D module; their 3/4 panels are validation views, not independent fitting authorities. The cream attachment stubs communicate attachment direction only and are not geometry to copy literally.

Historical 3D assets may be used as **donors or benchmarks** when they improve current production efficiency, but they remain subordinate to current canonical identity, approved Normal/Skin references, the approved exposed-Hero module sheets in their local domains, and this contract.

A supporting underbody number must not justify a visibly off-model final companion. Preserve evidence and route true conflicts through targeted correction or Architecture Review.

## 1.3 Domain roles

### Approved Normal Front
Locks approved neutral front silhouette, facial structure, eye/ear/hoof read, centerline, crown separation, and front fleece organization.

### Approved Normal Side
Locks approved neutral side envelope, total length, support spacing, muzzle projection, ear profile, tail relationship, compactness, and side motion-readiness silhouette.

### Approved Skin / Underbody Front
Supporting authority for hidden chassis width, head/body and chest/abdomen/pelvis relationships, bilateral support, short limbs, grounded hooves, and head/torso connection.

### Approved Skin / Underbody Side
Supporting authority for hidden head depth, minimal muzzle, longitudinal support structure, limb roots, support spacing, belly clearance, COM, tail/ear roots, and articulation/deformation clearance.

### This file
Supporting authority for normalized coordinates, numerical locks/tolerances, support/COM logic, reconstruction constraints, tail intent, and motion/deformation clearance.

### `carol-identity-canonical.png`
Highest final visible identity/appeal authority.

## 1.4 Numerical / visual conflict rule

The numerical contract protects structural consistency; visible references protect their visible domains; canonical identity protects final Carol appeal.

A few antialiasing/image-generation pixels are not grounds to rewrite a number.

When a technical discrepancy has no demonstrated visible, deformation, attachment, runtime, or future-spatial consequence, do not polish it as an independent goal.

## 1.5 Reference freeze / no-regeneration rule

- do NOT regenerate Normal Front
- do NOT regenerate Normal Side
- do NOT regenerate Skin Front
- do NOT regenerate Skin Side
- do NOT create a new whole-character AI Back / Top / 3/4 as geometry authority
- the approved ear/hoof module sheets are allowed only as localized module construction helpers; their 3/4 panels remain validation-only

Whole-character Back / Top / 3/4 remain derived diagnostics from the coherent full-spatial Carol character system, not new fitting authorities.

**Status:** LOCKED

# 2. Locked High-Level Character Rules

## 2.1 Character identity

Carol is:

- a young stylized sheep-like Grimo
- low
- grounded
- compact
- soft
- cute
- fleece-dominant
- not realistic sheep anatomy

## 2.2 Global shape rules

Must preserve:

- broad / rounded / obtuse top silhouette
- very large fleece envelope
- small cream face embedded in fleece
- huge glossy eyes
- broad soft drooping ears
- short visible legs
- heavy grounded hooves
- compact quadruped support
- independent small tail tuft

## 2.3 Absolute prohibitions

Do NOT introduce:

- realistic sheep proportions
- long neck
- long legs
- visible realistic ribcage / musculature
- flat sticker-like face profile
- tall elegant silhouette
- large dominant tail
- decorative extra atmosphere as geometry authority
- poster-like embellishment

---

# 3. Status Labels

Use the following status classes inside this file.

- **LOCKED** = approved and fixed
- **DERIVED** = computed from approved references / contract
- **PENDING** = not yet formally locked; to be decided in next step
- **GUIDANCE** = design intent for reconstruction / rigging, not a visible direct measurement

---

# 4. Global Normalized Coordinate System

## 4.1 Core normalization

All production geometry values use:

- total height `H = 1.000`

Side coordinates:
- `x` increases from front to rear
- `y` increases from bottom to top

Front coordinates:
- horizontal centerline is the body / face shared centerline
- vertical measurements are normalized by `H`

## 4.2 Blender world-axis interpretation

For Blender production, use one consistent world-space mapping:

- Blender `X` = front → rear
- Blender `Y` = anatomical left ↔ right
- Blender `Z` = bottom → top
- ground plane = `Z = 0`
- bilateral body / face / support centerplane = `Y = 0`

Mapping from this 2D contract:

- Side `x` → Blender `X`
- Side `y` → Blender `Z`
- Front horizontal offset from centerline → Blender `Y`
- Front vertical coordinate → Blender `Z`

Any older wording that used `z 0.000` for the Front centerline must be read as **zero horizontal offset from the bilateral centerline**, not as Blender vertical Z.

**Status:** LOCKED

## 4.3 General tolerance rule

Unless otherwise stated:

- major locked values: **target ±2%**
- highly visible silhouette relations: must visually match the approved authority images
- if a number and the approved image appear to disagree slightly because of image-generation softness, prefer **approved visible intent**, but do not violate the contract structurally

## 4.4 Reconstruction rule

All hidden-body interpretations must remain subordinate to approved visible references.

Do not invent anatomy that breaks:
- the approved Front
- the approved Side
- the compact low Carol identity

---

# 5. Definitive Normal Front — Final Locked Contract

## 5.1 Formal decision

The latest user-approved closed-mouth Front is the definitive **Normal Front**.

**Status:** LOCKED

## 5.2 Front structural rules

- body/support centerline = face centerline = front horizontal offset `0.000 H`
- Blender interpretation of that centerline = `Y = 0`
- face axis misalignment is not allowed
- mouth = closed neutral production mouth
- extremely weak soft smile is allowed
- open-mouth neutral authority is not allowed
- crown reads as a distinct upper mass
- crown and face-framing fleece must read separately
- vertical stretching is prohibited
- face / eyes / hooves must not be reduced
- low / grounded / compact quadruped must be preserved

**Status:** LOCKED

---

# 6. Front Measurement Basis

## 6.1 Approved Front measurement source basis

- approved Front canvas size = `1254 × 1254 px`
- normalized production height basis = `H = 1011 px`
- front centerline = `x = 626.5 px`

**Status:** LOCKED

## 6.2 Front normalization convention

For front interpretation:

- vertical normalization uses `H = 1011 px`
- horizontal left/right offsets are interpreted around centerline `x = 626.5 px`

**Status:** LOCKED

---

# 7. Locked Normal Front Geometry

## 7.1 Front overall envelope

### Fleece / body visible width
- max fleece width ≈ `1.161 H`

### Overall front width
- overall visible width ≈ `1.171 H`

Interpretation:
- the body remains broad
- front must not become vertically stretched or slimmed

**Status:** LOCKED

## 7.2 Face block

- face width ≈ `0.530 H`
- face height ≈ `0.324 H`
- face center Y ≈ `0.389 H`

Interpretation:
- face remains large enough to preserve Carol’s cuteness
- do not shrink face to make the fleece look lighter

**Status:** LOCKED

## 7.3 Eyes

Per-eye dimensions:
- eye width ≈ `0.137 H`
- eye height ≈ `0.149 H`

Eye spacing:
- center-to-center distance ≈ `0.324 H`

Eye center positions:
- left eye center ≈ `-0.162 H` from centerline
- right eye center ≈ `+0.162 H` from centerline

Interpretation:
- eyes are huge and identity-critical
- eye reduction is prohibited

**Status:** LOCKED

## 7.4 Nose

- nose width ≈ `0.039 H`
- nose center Y ≈ `0.378 H`

Interpretation:
- nose remains tiny
- do not enlarge toward realistic muzzle anatomy

**Status:** LOCKED

## 7.5 Mouth

- mouth width ≈ `0.091 H`
- mouth height ≈ `0.024 H`
- mouth center Y ≈ `0.350 H`

Interpretation:
- closed neutral mouth
- extremely weak soft-smile curvature acceptable
- open mouth not allowed for neutral production authority

**Status:** LOCKED

## 7.6 Ears — exposed Hero module

**Approved module helper:** `assets/grimo/source/carol/approved-3d/modules/carol-ear-module-authority.webp`

The sheet is the approved localized visual construction helper for one coherent Carol ear. The cream root stub is orientation-only and must not be copied as a visible final cut cylinder.

Primary locks:
- front ear angle ≈ `18°`
- visible front thickness intent ≈ `0.028 H`
- root-to-tip length ≈ `0.305 H`
- maximum planform breadth ≈ `0.124 H`
- root breadth ≈ `0.091 H`
- tip breadth ≈ `0.042 H`

Thickness profile:
- root thickness ≈ `0.058 H`
- mid thickness ≈ `0.043 H`
- tip thickness ≈ `0.021 H`

Projected / orientation targets:
- front outward projection ≈ `0.235 H`
- front downward drop ≈ `0.094 H`
- side visible length ≈ `0.266 H`
- side visible height ≈ `0.218 H`
- side pitch down ≈ `31°`
- top sweep back ≈ `10°`
- tip twist out ≈ `8°`

Inner-ear patch:
- length ≈ `0.205 H`
- maximum breadth ≈ `0.073 H`
- soft brown rim remains visibly present around the pink inset

Interpretation:
- broad, soft, side-drooping, plush, rounded
- not thin realistic sheep ears
- no sharp point or paper-flat flap
- root must read structurally attached and remain suitable for independent expressive ear-root motion
- one 3D ear family must satisfy Front / 3Q / Side / Top without per-view redesign

Construction tolerances:
- primary dimensions: approximately ±`0.010 H`
- thickness values: approximately ±`0.008 H`
- angles: approximately ±`3°`
- visible identity in canonical/Normal references overrides invisible micro-precision

**Status:** LOCKED — Human-approved module sheet + Planner-derived construction dimensions, 2026-09-24

## 7.7 Hooves — exposed Hero support module

**Approved module helper:** `assets/grimo/source/carol/approved-3d/modules/carol-hoof-module-authority.webp`

The sheet is the approved localized visual construction helper for one coherent front-hoof family. The cream pastern stub communicates insertion direction only and must not be copied as a visible final cut boundary.

Primary locks:
- visible front hoof width ≈ `0.219 H`
- visible front hoof height ≈ `0.111 H`
- hoof depth ≈ `0.150 H`
- hoof top width ≈ `0.184 H`
- hoof sole width ≈ `0.196 H`
- hoof sole depth ≈ `0.112 H`

Toe architecture — HUMAN LOCK 2026-09-22:
- exactly **three rounded toe lobes**
- exactly **two shallow clefts**
- one continuous stylized hoof mass
- center toe width ≈ `0.073 H`
- left/right outer toe width ≈ `0.066 H` each
- cleft width ≈ `0.007 H` each
- cleft depth ≈ `0.023 H`
- center toe may read slightly dominant, but not exaggerated

Volume / support:
- toe forward projection ≈ `0.014 H`
- heel back projection ≈ `0.009 H`
- front-face roundness radius ≈ `0.019 H`
- upper-edge softness radius ≈ `0.016 H`
- lower contact corner radius ≈ `0.010 H`
- pastern insert width ≈ `0.148 H`
- pastern insert depth ≈ `0.106 H`
- pastern-to-hoof transition height ≈ `0.031 H`

Interpretation:
- heavy, grounded, planted, soft-rounded
- do not miniaturize hooves to fake elegance
- no detached toe objects or per-view toe-count changes
- same single 3D toe architecture serves every view; camera projection may naturally hide part of one lobe
- independent toe articulation is not required for MVP

Construction tolerances:
- primary dimensions: approximately ±`0.008 H`
- toe/cleft values: approximately ±`0.005 H`
- support-center relationship remains visually exact

**Status:** LOCKED — Human-approved module sheet + Planner-derived construction dimensions, 2026-09-24

## 7.8 Front crown / fleece structure

The approved Front locks the following readable hierarchy:

1. crown mass
2. face-framing fleece
3. upper side fleece masses
4. lower front fleece band
5. lower side / hoof-covering fleece

Interpretation:
- crown must read separately from face-frame fleece
- top silhouette must remain broad / rounded / obtuse
- excessive fragmentation into many equal cloud balls is prohibited

**Status:** LOCKED

---

# 8. Definitive Normal Side — Final Locked Contract

## 8.1 Formal decision

The latest user-approved Normal Side is the definitive **Normal Side**.

**Status:** LOCKED

## 8.2 Approved Side source basis

- approved Normal Side canvas size = `1448 × 1086 px`
- production geometry is normalized in world space by `H = 1.000`
- canvas framing is **not** a shared pixel scale with the Front or Skin references
- do not directly resize different source canvases until their pixels overlap and treat that as geometry truth

**Status:** LOCKED

## 8.3 Side envelope

- total normalized height = `1.000 H`
- total normalized length = `1.300 H`

Carol must remain:
- low
- compact
- broad
- soft
- grounded

**Status:** LOCKED

## 8.4 Side landmark targets

- crown apex ≈ `x = 0.575`, `y = 1.000`
- lower fleece average bottom ≈ `y = 0.165`
- belly lowest point ≈ `y = 0.145`
- rear body end ≈ `x = 1.300`

**Status:** LOCKED

## 8.5 Support / hoof targets

- front hoof support center ≈ `x = 0.390 H`
- rear hoof support center ≈ `x = 0.920 H`
- front-to-rear support length ≈ `0.530 H`

Interpretation rule:
- support members must feel planted and load-bearing
- body must not appear to float
- legs must remain short and mostly hidden by fleece
- hooves must remain heavy and grounded

**Status:** LOCKED

## 8.6 Side face / head targets

The approved Side establishes:

- face is not flat
- muzzle projection is minimal but readable
- short rounded muzzle is required
- face remains cute and young
- eye remains large
- closed neutral mouth is required
- broad ear identity is required

Do NOT replace this with realistic sheep profile anatomy.

**Status:** LOCKED

## 8.7 Side ear profile

Ear intent:
- broad
- soft
- drooping
- readable root relationship
- non-realistic
- large enough for independent expressive rigging

**Status:** LOCKED

## 8.8 Tail targets

Tail is a small independent expressive module.

Skin/Normal interpretation clarification (2026-09-22): one `TAIL_PIVOT` owns the common `SKIN_TAIL_CORE` and the external `TAIL_FLEECE_SHELL`.

The cream Skin core attaches directly to the rump through a tiny hidden overlap, remains present in both modes, and has no long visible connector.

Its visible relationship follows locked Skin Side.

The rearward visible base/tuft-center values below describe the **Normal external fleece read**; they do not require the cream core to extend to that location.

The external tail shell hides with the other fleece in Skin mode and remains mechanically independent of the main rump fleece.

These are one acting tail assembly, not two behavioral tails.

No numerical lock values are changed.

Locked intent:

- internal root ≈ `x = 0.985`, `y = 0.355`
- visible base X ≈ `1.205`
- visible tuft center X ≈ `1.245`
- visual baseline height ≈ `y = 0.345–0.385`
- root width ≈ `0.060 H`
- visible tail length ≈ `0.085 H`
- maximum visible diameter ≈ `0.095 H`
- neutral orientation ≈ `+20°`
- approximately 70% of root remains hidden inside / behind rear fleece

Motion-readiness rule:
- tail must support subtle motion without becoming a major silhouette driver
- intended neutral range: approximately `±20°` vertical
- lateral range: small
- tail must not behave like a long animal tail
- tail must not merge into a second rear body mass

**Status:** LOCKED

---

# 9. Fleece Architecture Rules

The visible fleece is the dominant silhouette driver, but it must remain 3D-reconstructable and riggable.

## 9.1 Approved macro hierarchy

Approved readable fleece mass hierarchy:

1. crown mass
2. face-framing fleece
3. chest / front-body fleece
4. central back fleece
5. lower belly fleece band
6. rear rump fleece

**Status:** LOCKED

## 9.2 Production interpretation rule

Do NOT interpret the approved image as:

- hundreds of independently rigged equal-sized cloud balls
- a single rigid blob
- noisy tiny-lobe clutter

Reconstruct instead as:

- a coherent main fleece system
- sparse regional mass logic
- readable broad macro masses
- soft but controlled deformation volumes

**Status:** LOCKED

## 9.3 Fleece motion / ownership rule — 2026-09-24

Carol's fleece is a **body-attached stylized cloud mass**, not loose fur and not a second shell that visibly slides over Skin.

Motion causality:
- primary head / hidden torso / support motion owns the macro fleece position
- macro fleece follows its owning head/torso region with effectively zero perceptible positional lag
- no visible shell sliding, delayed translation, delayed rotation, or independent cloud-ball jiggle
- when interaction requires softness, use **local shape deformation**: compression, slight squash/stretch, opening/closing, and recovery
- adjacent fleece may receive lower-amplitude shape deformation only when causally justified
- an optional very small broad **shape settle** may occur after stronger authored actions, but the broad mass remains positionally attached to the body
- if a secondary fleece effect reads as jelly, mochi skin, floating balls, or detached outer clothing, remove it rather than preserving it for “life”
- life is carried primarily by face, gaze, ears, head/body weight transfer, limbs/hooves, and the independent tail

Mesh separation is allowed for authoring, weighting, replacement, and deformation control; mesh separation does **not** imply independent motion ownership.

**Status:** LOCKED

## 9.4 Fleece / hidden-body relationship

The fleece is an external full-spatial, body-attached silhouette system built around the smaller hidden chassis. It may remain a separate production mesh, but its macro transform ownership is tightly bound to the corresponding head/torso region.

It must preserve coherent real 3D volume across practical Front / 3/4 / Side / Rear / derived Top exposure.

The fleece must not be a camera-facing patch, front-only shell, ring of equal proxy balls, or view-specific cheat.

The hidden chassis does **not** need Hero aesthetic perfection before fleece work can begin. However, the combined character must remain spatially coherent and motion-safe.

Fleece may cover FUNCTIONAL_HIDDEN structure, but it must not be used to conceal a structural defect that causes:

- exterior collapse from a plausible view
- bad head/ear/limb/tail attachment
- deformation failure
- motion ownership failure
- clipping/clearance failure
- future plausible motion to require rebuilding the character

The fleece must preserve clearance for:

- head pitch / yaw / small roll
- cheek / forehead lean
- ear-root motion
- forelimb adjustment
- tail-root motion
- local contact compression
- optional broad shape settle with no visible positional drift

Existing validated historical full-3D fleece may be reused/adapted as a donor when it fits current authority better than rebuilding from scratch.

**Status:** LOCKED
---

# 10. Hidden Underbody Contract

Underbody is normally not HERO_PRIORITY. It must provide sufficient support, deformation, attachment, collision/clearance, and spatial continuity for the full-spatial Carol character. It may be modular; one continuous watertight Hero body is not a product requirement.

It must support:

- head
- chest
- abdomen
- pelvis
- forelimb pair
- hindlimb pair
- independent tail root

**Status:** LOCKED as requirement

## 10.1 Underbody philosophy

The underbody must be:

- stylized
- compact
- low
- deformation-friendly
- non-realistic
- consistent with Front + Side

It must NOT become:

- realistic sheep anatomy
- long-bodied animal anatomy
- muscular quadruped anatomy
- long-necked anatomy
- long-legged anatomy

**Status:** LOCKED

## 10.2 Underbody approximate bounding intent

Target hidden body chassis envelope:

- length ≈ `1.060 H`
- height ≈ `0.690 H`
- depth / width intent ≈ `0.610 H`

These are production guidance values for hidden-body reconstruction,
not visible-appearance replacement values.

**Status:** LOCKED

## 10.3 Definitive underbody visual-reference decision

The latest user-approved **Skin / Underbody Front** and **Skin / Underbody Side** are FINAL / LOCKED **supporting underbody references**.

They are authoritative for support/deformation/attachment/clearance and must not be regenerated or replaced by a new AI interpretation. They are not the highest authority for fleece-included Hero appearance.

The hidden chassis must clearly support segmentation into:

- head
- extremely short head / chest transition
- chest
- abdomen
- pelvis / rump
- forelimb pair
- hindlimb pair
- ear roots
- independent tail root

**Status:** LOCKED

## 10.4 Definitive Skin / Underbody Front

The latest user-approved Skin / Underbody Front is the definitive hidden-structure Front.

Approved source basis:

- canvas size = `1254 × 1254 px`
- image role = structural / geometric authority, not marketing art
- fleece / moon / stars / detached atmosphere are absent by design

It locks the visible interpretation of:

- hidden frontal chassis
- hidden body width
- head / body ratio
- very large head relative to torso
- bilateral limb architecture
- front and rear support relationship
- short limbs
- heavy planted hooves
- low grounded stance
- head / torso connection
- broad ear identity without fleece occlusion
- face scale and large-eye identity without using fleece to fake proportions

Interpretation rules:

- do not narrow the torso just to imitate the Normal Front silhouette
- do not lengthen limbs because the fleece is absent
- do not expose a long neck
- do not replace the approved stylized support system with realistic sheep anatomy
- left/right support must remain structurally coherent around the shared centerplane

**Status:** LOCKED

## 10.5 Definitive Skin / Underbody Side

The latest user-approved Skin / Underbody Side is the definitive hidden-structure Side.

Approved source basis:

- canvas size = `1254 × 1254 px`
- image role = structural / geometric authority, not marketing art
- fleece / moon / stars / detached atmosphere are absent by design

It locks the visible interpretation of:

- true head depth
- very short rounded muzzle
- non-flat face volume
- extremely short head / chest transition
- chest → abdomen → pelvis longitudinal structure
- forelimb root and hindlimb root placement
- front / rear support spacing
- short limb exposure
- belly clearance
- low center-of-mass read
- heavy planted hoof relationship
- ear-root depth
- independent tail-root relationship
- articulation clearance required for future movement

Interpretation rules:

- do not turn the torso into a generic bean
- do not create a realistic sheep ribcage
- do not add a long visible neck
- do not extend the muzzle toward realistic sheep anatomy
- do not shift support points just to make the Side look more elegant
- do not fuse the tail into the rump or future fleece shell

**Status:** LOCKED

## 10.6 Underbody construction interpretation

The definitive Skin Front + Skin Side must be reconciled into **one coherent functional 3D underbody system**. Modular/separate meshes are allowed when required support, deformation, attachment, clearance, and spatial continuity remain correct.

Recommended structural reading:

```text
HEAD
↓
extremely short head / chest transition
↓
CHEST
↓
ABDOMEN
↓
PELVIS / RUMP
↓
4 independent support limbs
```

Additional independent structures:

- left / right ears
- left / right eyes
- four heavy hooves
- tail root + small tail tuft

The chest, abdomen, and pelvis may blend smoothly in the final surface, but their functional roles must remain understandable for deformation and support.

**Status:** LOCKED

## 10.7 Single-model Normal / Skin relationship

There is one coherent Carol spatial character system. This forbids separate view-specific Carol characters, but does not require one continuous mesh.

The Skin and Normal references do not define separate characters.

For validation:

- **Skin mode** = hide external fleece + attached moon / star motifs
- **Normal mode** = show the same hidden body + external fleece + attached motifs

The following must remain the same objects / same neutral geometry in both modes:

- head
- eyes
- ears
- hidden torso
- four limbs
- four hooves
- tail root / tail tuft

Forbidden:

- Front-only mesh
- Side-only mesh
- Skin-Front-only body
- Skin-Side-only body
- camera-dependent geometry
- per-view neutral-pose changes
- per-view scaling

**Status:** LOCKED

## 10.8 Underbody support / COM rule

The hidden torso, limbs, and hooves form the real support system.

Locked support targets remain:

- front support center ≈ `x = 0.390 H`
- rear support center ≈ `x = 0.920 H`
- front-to-rear support distance ≈ `0.530 H`

The geometry must permit small future COM transfers while keeping the relevant support contacts planted.

Do not design Carol as a root object that merely bounces above decorative legs.

Body causality must remain:

```text
support
→ COM / hidden torso
→ head / primary body action
→ ears / tail secondary response + fleece-local deformation when causally justified
```

**Status:** LOCKED

## 10.9 Underbody deformation-clearance rule

Before final production topology is locked, the geometry must leave plausible clearance for at least:

- modest head pitch
- modest head yaw
- slight head roll
- cheek lean
- forehead lean
- blink / eyelid closure
- gaze movement
- small forelimb support adjustment
- hindlimb stabilization
- independent ear motion
- subtle tail motion
- local face-frame fleece compression
- broad fleece settle

Static neutral beauty alone is not sufficient.

**Status:** LOCKED

---

# 11. Motion / Rigging Readiness Rules

All next-stage geometry must remain compatible with future animation.

The neutral design must support:

- blink
- half-lid / eye expression
- subtle mouth expression
- gaze response
- head pitch / yaw / small roll
- cheek / forehead lean toward user touch
- subtle torso COM transfer
- four-point support readability
- subtle forelimb adjustment
- hindlimb stability
- invitation / reaction anticipation
- settle back to neutral
- local fleece compression / recovery where contact or authored pose requires it
- subtle ear response
- subtle tail tuft response

**Status:** LOCKED

## 11.1 Primary motion channels

Primary motion channels:
- face
- head
- hidden torso / COM
- support / hooves

**Status:** LOCKED

## 11.2 Secondary motion channels

Secondary motion channels:
- ears
- local fleece deformation / silhouette-safe authored shape settle (no macro transform lag)
- tail tuft

**Status:** LOCKED

## 11.3 Grounding rule

All future rigging and animation must preserve:

- low COM feel
- planted support
- compact quadruped balance
- no floating body
- no tallened stance
- no long-leg interpretation

**Status:** LOCKED

---

# 12. Normal Version Motif Rules

For the normal fleece-present version:

Keep:
- moon motif
- attached yellow star motifs

Do NOT include in geometry authority:
- extra atmospheric clouds
- extra sparkles
- decorative floating effects
- poster VFX

These may exist in illustrations, but are not authority for production geometry.

**Status:** LOCKED

---

# 13. Stable Reference Lock and Workflow Boundary

## 13.1 Locked durable facts

The following remain formally locked:

- Definitive Normal Front
- Definitive Normal Side
- Definitive Skin / Underbody Front
- Definitive Skin / Underbody Side
- Front centerline and locked numerical values in this contract
- Side envelope / support / tail relationships
- Fleece macro-architecture rules
- Supporting underbody envelope and support interpretation
- Motion/deformation-readiness constraints
- full-spatial single-character consistency: no view-specific Carol geometry

These are durable references, not a current-state log.

## 13.2 Mutable state lives elsewhere

Current branch, HEAD, selected candidate, attempt count, blocker, Human Gate, and next handoff live only in `docs/production/carol/CAROL_PRODUCTION_STATE.md`.

This file must not prescribe a mutable “next production step”.

## 13.3 Full-spatial production boundary

This contract does not require naked Underbody perfection, final retopology, production rigging, or a static Geometry Gate before every downstream experiment.

It **does** require that the character's exterior geometry remain spatially coherent beyond the primary Front view so that future motion does not routinely expose unbuilt/broken angles.

Production order is selected by the Goal-Backward Production Operating System.

For Carol, visible components used in Human perceptual review must first satisfy the task-specific **Human-Evaluable Fidelity Floor**. A visibly poor ear, hoof, fleece, or attachment cannot be mentally ignored when judging cuteness or motion ownership.

When useful, existing high-quality historical full-3D assets may be adapted as donors instead of rebuilt from zero.

Final production topology/weights/shaders may remain provisional while representative motion is tested, provided the visible geometry is already representative enough for the Decision Question.

# 14. Derived View / Full-Spatial Diagnostic Policy

## 14.1 Front / 3/4 / Side / Back / Top-derived views

Normal Front and Normal Side remain the locked visible neutral references.

Back / Top / 3/4 are **DERIVED diagnostic views**, not independent AI authorities.

They must be derived from the same coherent spatial Carol system and are used to detect failures such as:

- flat or camera-specific head volume
- impossible torso transition
- support asymmetry
- ear-root failure
- hoof/leg depth failure
- tail fusion
- fleece discontinuity
- view-specific collapse
- attachment/occlusion instability
- motion-exposed clipping
- unrealistic sheep drift

Do not deform Carol to match obsolete old Back / Top / 3/4 artwork.

There is no requirement that rear/top views receive equal Hero polish, but they must not reveal an obviously broken character.

## 14.2 Evidence is Decision-Question specific

There is no permanent evidence packet every task must generate.

Geometry tasks claiming full-spatial coherence should use enough derived views to demonstrate the affected region remains valid.

Human identity/appeal judgment should use representative-quality visible assets.

Motion/touch/runtime questions should use evidence as close as practical to final use; if touch causality is the question, actual interactive input is preferred over a prerecorded clip.

Automated geometry metrics are diagnostics. Human judgment controls visible identity, appeal, naturalness, life, and companion quality.

**Status:** LOCKED as diagnostic policy

# 15. Decision Rules for Future Work

When geometry-related choices compete, prioritize:

1. Product Goal and canonical identity / appeal