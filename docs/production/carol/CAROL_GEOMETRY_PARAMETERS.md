# CAROL_GEOMETRY_PARAMETERS.md

**Status:** FINAL AUTHORITY — FOUR-REFERENCE LOCK  
**Character:** Carol  
**Scope:** Definitive Normal Front / Definitive Normal Side / Definitive Skin Front / Definitive Skin Side / Single-Model 3D Reconstruction / Rigging / Deformation / Motion Readiness  
**Last Updated:** 2026-09-21

---

# 0. Purpose

This file is the current single formal geometry authority for Carol.

It exists to lock the approved production geometry used for:

- 2D production references
- hidden underbody reconstruction
- 3D modeling
- rigging
- deformation
- support / COM design
- future motion implementation

This is **not** a lore document.  
This is **not** a style essay.  
This is a **production geometry contract**.

---

# 1. Authority Hierarchy

Use the following authority order.

## 1.1 Formal authority package

Carol’s current formal geometry authority is the **combined set** of:

1. **latest user-approved Definitive Normal Front**
2. **latest user-approved Definitive Normal Side**
3. **latest user-approved Definitive Skin / Underbody Front**
4. **latest user-approved Definitive Skin / Underbody Side**
5. **this file: `CAROL_GEOMETRY_PARAMETERS.md`**
6. `carol-identity-canonical.png`

These six together define the current production truth.

The four definitive production-reference images are **FINAL / LOCKED** and must not be regenerated, redesigned, averaged with older references, or replaced by new AI-generated alternatives.

## 1.2 Conflict rule

If any older material conflicts with the four definitive production references or this file, it must be ignored.

Ignore:

- old sheets
- old turnarounds
- old Fronts
- old Sides
- old underbody candidates
- old AI generations
- old Back / Top / 3/4 AI references when used as geometry authority
- old 3D interpretations that contradict current approved references

## 1.3 Domain roles

### Approved Normal Front
Authority for:
- front silhouette
- front facial structure
- front eye placement and scale
- front ear placement and read
- front hoof read
- centerline truth
- crown separation
- front fleece organization

### Approved Normal Side
Authority for:
- side envelope
- side total length
- side support spacing
- side muzzle projection
- side ear profile
- side tail position and scale
- side compactness
- side motion-readiness silhouette

### Approved Skin / Underbody Front
Authority for:
- hidden chassis front structure
- hidden body width
- head / body ratio
- chest / abdomen / pelvis width relationship
- bilateral four-limb architecture
- left / right support symmetry
- low center-of-mass read
- short limb architecture
- heavy hoof read without fleece occlusion
- head / torso connection from the front

### Approved Skin / Underbody Side
Authority for:
- hidden head depth
- minimal muzzle projection
- chest → abdomen → pelvis longitudinal structure
- forelimb / hindlimb root relationship
- front / rear support spacing
- belly clearance
- center-of-mass interpretation
- tail root relationship
- ear-root depth relationship
- articulation and deformation clearance from the side

### This file
Authority for:
- normalized coordinate system
- numerical lock values
- interpretation rules
- reconstruction rules
- support / COM logic
- tail rigging intent
- underbody reconstruction intent
- motion / deformation constraints

### `carol-identity-canonical.png`
Secondary support for:
- Carol-ness
- softness
- cuteness
- palette relationships
- charm / identity continuity

If identity-canonical conflicts with the four approved definitive production references, the definitive production references win for geometry. The identity-canonical remains secondary support for Carol-ness, softness, palette relationships, charm, and visual identity continuity.

## 1.4 Numerical / visual conflict rule

The authority package is intentionally split by domain:

- the four definitive reference images lock visible shape and structural interpretation
- this file locks normalized numerical geometry and tolerances

If an AI-generated reference differs from a locked number by a few pixels because of antialiasing, soft rendering, image-generation drift, or framing, do **not** rewrite the numerical contract from those few pixels.

Use:

1. locked numerical contract
2. intended visible shape in the approved reference
3. single-model 3D consistency

in that order for structural reconstruction.

**Status:** LOCKED

## 1.5 Reference freeze / no-regeneration rule

From this point onward:

- do NOT regenerate Normal Front
- do NOT regenerate Normal Side
- do NOT regenerate Skin Front
- do NOT regenerate Skin Side
- do NOT create a new AI Back / Top / 3/4 as geometry authority

Back / Top / 3/4 must be derived from the accepted **single 3D model** after Front + Side + Skin reconstruction.

**Status:** LOCKED

---

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

## 7.6 Ears — front read

- front ear angle ≈ `18°`
- visible ear thickness intent ≈ `0.028 H`

Interpretation:
- broad, soft, side-drooping
- not thin realistic sheep ears
- ear identity is protected

**Status:** LOCKED

## 7.7 Hooves — front read

Visible front hoof read:
- hoof width ≈ `0.219 H`
- hoof height ≈ `0.111 H`

Interpretation:
- heavy and grounded
- do not miniaturize hooves to fake elegance
- hoof read must remain strong

**Status:** LOCKED

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

Skin/Normal interpretation clarification (2026-09-22): one `TAIL_PIVOT`
owns the common `SKIN_TAIL_CORE` and the external `TAIL_FLEECE_SHELL`.
The cream Skin core attaches directly to the rump through a tiny hidden
overlap, remains present in both modes, and has no long visible connector.
Its visible relationship follows locked Skin Side. The rearward visible
base/tuft-center values below describe the **Normal external fleece read**;
they do not require the cream core to extend to that location. The external
tail shell hides with the other fleece in Skin mode and remains mechanically
independent of the main rump fleece. These are one acting tail assembly,
not two behavioral tails. No numerical lock values are changed.

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

## 9.3 Animation rule

Motion causality:

- primary head / hidden torso / support motion occurs first
- fleece follows with delayed softness
- small residual settle may occur
- fleece is secondary, not primary

**Status:** LOCKED

## 9.4 Fleece / hidden-body relationship

The fleece is an external silhouette and secondary-motion system built **around** the smaller hidden chassis.

It must not be used to conceal unresolved structural errors in the Skin model.

The production model must therefore pass hidden-body Front / Side validation **before** final fleece acceptance.

The fleece must preserve clearance for:

- head pitch / yaw
- cheek / forehead lean
- ear-root motion
- forelimb adjustment
- tail-root motion
- local contact compression
- delayed broad settle

**Status:** LOCKED

---

# 10. Hidden Underbody Contract

Underbody is not visible in the normal design, but must exist as a deformation chassis.

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

The latest user-approved **Skin / Underbody Front** and **Skin / Underbody Side** are now the definitive visual underbody references.

They are final production authorities for reconstruction and must not be regenerated or replaced by a new AI interpretation.

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

The definitive Skin Front + Skin Side must be reconciled into **one single 3D hidden chassis**.

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

There is only **one Carol geometry system**.

The Skin and Normal references do not define separate characters or separate body meshes.

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
- tail root / Skin tail core (the Normal external tail fleece shell hides
  with the rest of the fleece; see section 8.8)

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
→ ears / fleece / tail secondary response
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
- delayed fleece follow-through
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
- fleece regional masses
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

# 13. Current Production State

## 13.1 Locked and completed

The following are now formally locked:

- Definitive Normal Front
- Definitive Normal Side
- Definitive Skin / Underbody Front
- Definitive Skin / Underbody Side
- Front centerline truth
- Front key face / eye / nose / mouth / ear / hoof values
- Side envelope
- Side support spacing
- Side tail
- Fleece macro architecture rules
- Hidden underbody envelope intent
- Hidden underbody visual interpretation
- Four-point support interpretation
- Single-model Normal / Skin relationship
- Motion / rigging readiness principles

There are no remaining AI-generated orthographic geometry references required before Blender reconstruction begins.

## 13.2 Frozen production references

From this point onward:

- do NOT regenerate Normal Front
- do NOT regenerate Normal Side
- do NOT regenerate Skin Front
- do NOT regenerate Skin Side
- do NOT redesign Carol
- do NOT create a new AI Back / Top / 3/4 and treat it as geometry authority

These four images are fixed production references.

## 13.3 Next production step

The next geometry task is:

1. register the four definitive references in Blender
2. normalize the world-space contract with `H = 1.000`
3. build Carol from zero as one coherent hidden Skin chassis
4. validate Skin Front + Skin Side simultaneously
5. add the external fleece system
6. validate Normal Front + Normal Side simultaneously
7. derive 3/4 / Back / Top from the single 3D model
8. perform early deformation / motion-clearance diagnostics
9. submit the resulting structural model and evidence to Human Geometry Gate

Do **not** proceed directly to final retopology, production rigging, final lookdev, or animation before the structural Geometry Gate is accepted.

---

# 14. Derived View Policy

## 14.1 Back / Top / 3/4

Back / Top / 3/4 are now **DERIVED validation views**, not independent AI authorities.

They must be rendered from the same accepted neutral 3D model built from:

- Normal Front
- Normal Side
- Skin Front
- Skin Side
- this numerical contract

They exist to detect three-dimensional failure such as:

- flat head volume
- impossible torso transition
- support asymmetry
- ear-root failure
- tail fusion
- fleece discontinuity
- hidden mesh intersections
- unrealistic sheep drift

Do not deform the model to match any obsolete old Back / Top / 3/4 image.

**Status:** LOCKED

## 14.2 Validation principle

At minimum, structural Geometry Gate evidence must include:

- Skin Front render
- Skin Side render
- Normal Front render
- Normal Side render

Each must be comparable to its formal reference by overlay / silhouette / landmark inspection.

Derived 3/4 / Back / Top should then be inspected for single-model coherence.

Automated metrics are evidence only. Final geometry acceptance is Human Gate.

**Status:** LOCKED

---

# 15. Decision Rules for Future Work

If there is uncertainty, choose:

1. Front consistency
2. Side consistency
3. Skin consistency
4. single-model consistency
5. riggability
6. support clarity
7. deformation safety
8. motion-readiness
9. Carol identity preservation

Over:

- realism
- decorative beauty
- poster aesthetics
- speculative anatomy
- view-specific cheating

---

# 16. Summary Contract

Carol must always remain:

- low
- grounded
- compact
- soft
- cute
- fleece-dominant in the Normal version
- non-realistic
- structurally riggable
- motion-capable
- one coherent 3D character across all views

The following are now fixed:

- Normal Front
- Normal Side
- Skin / Underbody Front
- Skin / Underbody Side
- the numerical geometry contract in this file

All future modeling, rigging, deformation, and animation must be derived from this frozen authority package without redesign.

The required production direction is:

```text
Definitive Normal Front
+ Definitive Normal Side
+ Definitive Skin Front
+ Definitive Skin Side
+ CAROL_GEOMETRY_PARAMETERS.md
        ↓
ONE SINGLE CONSISTENT 3D MODEL
        ↓
derived Back / Top / 3/4
        ↓
rigging / deformation / motion
```

The target is not realistic sheep anatomy.
The target is not a prettier alternative Carol.
The target is the **currently approved Carol converted faithfully into one motion-capable 3D structure**.
