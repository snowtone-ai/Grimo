# Carol geometry decision

> Stable decision: the four FINAL / LOCKED Normal Front, Normal Side, Skin Front
> and Skin Side references plus `CAROL_GEOMETRY_PARAMETERS.md` produce one
> model; Back/Top/3Q are derived from it. Current candidate and gate truth live
> only in [`CAROL_PRODUCTION_STATE.md`](CAROL_PRODUCTION_STATE.md).

## Historical decision record


> Latest scope update (2026-09-16): v005 A/B method comparison is recorded in
> [the v005 packet](evidence/hero-geometry-v005/README.md). The user explicitly
> authorized historical mesh deformation for B while preserving zero-based A.
> Neither is approved hero geometry; the earlier conditional G1–G5 interpretation
> below is not approval of A or B. Handoff recorded at that time: HUMAN for
> method/source comparison.

> Historical milestone at 2026-09-16: v001 received Human **CONDITIONAL PASS**, with
> external/final visual quality approximately **5/100** but useful structural
> direction. At that time, v002 awaited a new **HUMAN** Gate. The interpretation record
> below remains the historical basis for G1–G5; its no-model statements describe
> that earlier task. Artifacts and measurements recorded for that task are in
> [the v002 review packet](evidence/blockout-v002/README.md).

Status: **CONDITIONAL PASS / geometry direction accepted in principle; production not authorized**
Date: 2026-09-16
Target / author: CODEX_ASTRA / GPT-6 Astra
Evidence baseline: `cef0ed0ea4e7aab68e8feda40b121bdfc8601eaf`
Human Gate: **CONDITIONAL PASS** (2026-09-16; Human Gate / user-approved)
Handoff recorded at that time: **HUMAN** — Structural Blockout v002; no automatic rigging

## 1. Scope and decision status

This record replaces the empty interpretation template with observations and a
reviewable geometry proposal. The Human Gate result is now recorded as a
**CONDITIONAL PASS**: G1–G5 are accepted in principle, subject to the explicit
unresolved conflicts and measurements below. Geometry direction is approved in
principle, but the result is not production authorization. Approval of the
source packet is not approval of this reconstruction proposal.

No Blender blockout, rig, animation, GLB or PlayCanvas implementation is part of
this task. No new artwork or replacement reference was generated.

Recommendation: retain the canonical tiny expressive face inside an enormous,
coherent dream-cloud fleece, supported by a concealed low quadruped chassis.
Use the approved packet to propose depth and rear structure, with explicit
holds on inconsistent motif correspondence, unmeasured proportions and camera
calibration. Do not promote a plausible sheep body into identity authority.

## 2. Evidence actually inspected

All paths below are repository-relative. Image observations are direct visual
inspection of the seven approved packet PNGs, not deductions from their
filenames. The seven packet files were also checked against their manifest
SHA-256 values: **7/7 matched**. That establishes file identity, not geometric
consistency.

| ID | Source | Authority / inspected scope |
|---|---|---|
| I | [Identity canonical](../../../assets/grimo/source/carol/carol-Identity-canonical.png) | Identity, color, motifs and appeal reference; not a geometry override |
| A | [authority.json](../../../assets/grimo/source/carol/approved-3d/authority.json) | Schema/version 2; six individual production views were treated as the highest geometry authority for this historical decision task; superseded for current production by the four FINAL / LOCKED references plus `CAROL_GEOMETRY_PARAMETERS.md` |
| S | [Production sheet](../../../assets/grimo/source/carol/approved-3d/carol-3d-production-canonical-sheet.png) | Large posed view, small turn views, eye/ear/motif details, gray chassis and partial fleece cutaway |
| F | [Front reference](../../../assets/grimo/source/carol/approved-3d/carol-front-ortho-transparent.png) | Frontal face, fleece, ears, motifs and visible feet |
| P | [Side reference](../../../assets/grimo/source/carol/approved-3d/carol-side-ortho-transparent.png) | Face toward image-left; body depth, short feet and rear cloud appendage |
| B | [Back reference](../../../assets/grimo/source/carol/approved-3d/carol-back-ortho-transparent.png) | Rear fleece, central cloud appendage, ears, motifs and visible feet |
| T | [Top-plan reference](../../../assets/grimo/source/carol/approved-3d/carol-top-plan-transparent.png) | Long cloud outline, ears, motifs and terminal cloud lobes; no axis labels |
| L | [Left 3/4 reference](../../../assets/grimo/source/carol/approved-3d/carol-front-3q-left.png) | Left-side oblique face, ear-root/head connection, facial and body depth, fleece volume and fore/aft limb placement |
| R | [Right 3/4 reference](../../../assets/grimo/source/carol/approved-3d/carol-front-3q-right.png) | Right-side oblique face, ear-root/head connection, facial and body depth, fleece volume and fore/aft limb placement |
| C | [Camera contract](CAROL_CAMERA_CONTRACT.md) | Front-facing companion; all numeric calibration pending |
| M | [Modeling contract](CAROL_MODELING_CONTRACT.md) | Sacred identity, conditional hidden-geometry authority and production boundary |
| V | [Carol MVP Motion Spec](../../grimo/knowledge/character-production/carol/CAROL_MVP_MOTION_SPEC.md) | §§0–2, 7, 9–25, 30–32: local acting, support, face/fleece capability, anchors, gates and open envelopes |
| D | [3D / Blender Production Bible](../../grimo/knowledge/character-production/GRIMO_3D_BLENDER_PRODUCTION_BIBLE.md) | §§2–7, 12–13: canonical hierarchy, Carol anatomy, sacred view, shape hierarchy, eyes and fleece |
| E | [Experience / Motion Bible](../../grimo/knowledge/character-experience/GRIMO_EXPERIENCE_MOTION_BIBLE.md) | §0, §14: evidence policy, low quadruped support, Carol identity and motion grammar |

Product/Data changes are not proposed; their implementation authorities were
not needed to decide this geometry scope. Motion Masters and reference videos
were not independently measured in this task. V/E are the consulted motion
constraints; Pokémon poses, timing and anatomy supply no geometry shortcut.

Confidence terms: **High** = clearly visible or explicitly required; **Medium**
= supported interpretation with occlusion/view ambiguity; **Low / pending** =
not sufficiently constrained. Confidence never substitutes for approval.
Image-left/right below always means the viewer's image coordinates. The new
3/4 filenames use anatomical side as viewed from the corresponding front
oblique: the image with the face toward image-right is `left`, and the image
with the face toward image-left is `right`, consistent with the supplied Side
reference. Anatomical left/right has not been assigned to the asymmetric motif
map.

### Geometry authority rule

For the historical decision task recorded below, the approved individual
production views were treated as the highest authority, in the set Front / Side
/ Back / Top / Left 3/4 / Right 3/4. That historical six-view authority is
superseded for current production by the four FINAL / LOCKED references plus
`CAROL_GEOMETRY_PARAMETERS.md`, which produce one model and derive Back / Top /
3Q. The historical task required Side and both 3/4 views to be consulted with
Front when determining face and body volume; flattening the face from Front
alone was prohibited. Those views were formal evidence at that time for facial
front-to-back thickness, muzzle/cheek/forehead volume, eye-to-face depth,
ear-root/head connection, fleece-to-face ordering, body depth, fore/aft limb
placement, and total fleece volume.

For that historical task, `carol-Identity-canonical.png` remained an identity,
color, motif, and appeal reference. It was not to be used to reverse-engineer
or override concrete 3D depth, thickness, volume, or part placement when it
conflicted with the six then-approved individual production views.
`carol-3d-production-canonical-sheet.png` was supplementary and also yielded
to those six views. These statements describe that historical evidence model;
they do not replace the current four-reference authority.

## 3. Canonical observations and sacred identity

| Region in I | Direct observation | Constraint / confidence |
|---|---|---|
| Overall connected body | A very large scalloped cloud mass surrounds a much smaller exposed cream face. Large white lobes overlap pale blue/lilac recesses. | Fleece must dominate; preserve large/medium/small hierarchy instead of uniform wool beads. High |
| Face, lower image-right | Rounded cream face, tilted in the illustration, with two large dark brown/amber glossy eyes, soft blush, tiny dark nose and a small open smiling mouth. | Preserve face-in-fleece contrast, rounded cheeks and eye appeal. The illustrated smile is evidence, not a mandated permanent neutral expression. High |
| Eyes | Dark oval outlines, white and star-like highlights, warm amber lower regions; no prominent white sclera. | Avoid realistic protruding eyeballs, exposed sclera and added human eyebrows. Exact surface depth and highlight construction are unobserved. High visible / pending depth |
| Ear pair beside face | Brown outer ears and pink inner surfaces project low and sideways from fleece; image-left ear exposes a broad inner bowl. | Keep broad soft ear forms and partly concealed roots. Do not infer unequal ear size solely from the tilted pose. High |
| Bottom edge | Several short brown hoof ends emerge beneath the fleece, with shallow toe separations. Upper legs are concealed. | Short exposed support, heavy grounded read; no elongated leg silhouette. Occlusion does not prove limb count. High |
| Upper image-left fleece | A yellow crescent lies against a blue-violet cloud patch, with its opening toward image-right. | Preserve its relationship to the face and surrounding color mass; do not mirror it for convenience. High |
| Crown, forehead, lower fleece | Yellow five-point star motifs sit on cloud regions; their placements are asymmetric. | Preserve recognizable attached motif landmarks. Exact 3D roots and thickness are unmeasured. High visible / pending construction |
| Outside body perimeter | Detached cloudlets, stars and small sparkles surround the figure. | Atmosphere is distinct from body geometry under D §3.1; do not turn every detached cloud into a limb or tail. High |

I is a posed, oblique illustration, **not a measured front orthographic plate**.
Its apparent face tilt, hoof overlap and ear asymmetry must not be baked into a
neutral skeleton without evidence. Conversely, frontalizing Carol does not
permit replacing the face or shrinking the dominant fleece.

## 4. Approved 3D reference observations

| Source / region | Observation | Interpretation and limitation |
|---|---|---|
| S, large upper view | Retains moon on image-left, tiny face, hanging ears and short feet, but uses denser, more individually rounded fleece lobes than I. | Strong continuity of parts; fidelity of clump scale/appeal still requires Human review. High observation |
| S, bottom gray diagram and adjacent cutaway | Shows a distinct head mass, horizontal concealed torso, short support members and rear rounded appendage; partial shell covers this structure. | Supports a minimal chassis rather than a solid cloud ball. It is a diagram, not calibrated bone/mesh dimensions. Medium geometry |
| F | Centered, level face below a tall fleece crown; two prominent feet below the front, bilateral ears; crescent remains image-left. | Useful frontal arrangement, not automatic replacement of I's ratios. Hidden feet can overlap. High observation |
| P | Face projects only modestly beyond the front fleece; no long exposed neck. Body extends behind face; two prominent feet and a raised rear cloud tuft are visible. | Supports depth, tucked head transition and short support. Only this profile is supplied as a standalone image; reverse-side topology is not established. Medium depth |
| B | Face absent, brown ear backs visible at sides, central rounded cloud tuft, two prominent feet. Crescent appears on image-right. | Supports a rear tuft and fleece closure. Whether the back crescent is the same physical motif as F/P is unresolved. High observation |
| T | Elongated outline, ears near the upper portion, rounded lobe at the lower end; many star placements along the length. | Suggests plan depth but lacks a labeled front arrow, common scale or view transform. Do not treat it as a calibrated footprint or infer a second appendage. Medium outline / pending orientation |
| S vs standalone views | Small turn views and standalone plates differ in clump detail and motif distribution. | Packet approval does not establish one-to-one surface correspondence; do not average these into invented attachment locations. High discrepancy |

The names `ortho` and `top-plan` state reference roles. They do not prove
orthographic projection, matching scale or a single coherent source mesh.

## 5. Hidden-geometry decisions proposed for Human Gate

| ID | Proposed decision | Evidence / confidence | Canonical conflict check and hold |
|---|---|---|---|
| G1 | Concealed low quadruped chassis with four support limbs; minimize anatomy that never affects support or deformation. | S cutaway; E §14.3; V §24. High requirement, Medium form | I's visible hoof overlap is compatible with concealment; do not expose generic shoulders, knees, belly or a long sheep neck. Lengths and contact footprint pending. |
| G2 | Head is a rounded, shallow projecting acting region nested within a fleece opening; concealed transition allows lean/lower/turn. | I face boundary, P profile, V §§14/24. Medium | No protruding muzzle or distinct external neck. Face depth, opening depth and clearance are pending. |
| G3 | Broad continuous fleece envelope surrounds the chassis, with regional cloud masses layered over it. | I silhouette; F/P/B; D §12. High structure, Medium depth | Recover I's broad cloud hierarchy where packet lobes become too granular; no traced one-ball-per-lobe construction. |
| G4 | A compact rear cloud tuft/appendage is supported as hidden production geometry and may act as an independent expressive appendage. | S diagram/cutaway, P/B. High existence, Medium attachment | A plus S/P/B supplies evidence for the rounded tuft. I does not reveal a root. Exact stalk, axis and footprint remain pending. Small cute “pyoko-pyoko” emotional motion is allowed, but it must remain Carol-like and subordinate to face/head/body/fleece acting; do not reinterpret it as a generic wagging dog tail or dominant motion driver. |
| G5 | Moon and attached stars are body-relative identity features, distinguishable from detached atmosphere and wearable props. | I; S detail panels; V §§22/24. High role, Low depth/map | Propose shallow shaped surfaces only as a candidate. Back/front correspondence, count, bevel, thickness and anatomical side cannot be locked from the images. Never duplicate the moon merely to satisfy every plate. |

## 6. Volume hierarchy and deformation ownership

1. **Primary:** coherent cloud silhouette; tiny exposed head relative to fleece;
   concealed low support mass; body depth and short hoof footprint.
2. **Secondary:** forehead canopy, cheek framing, lower front collar, crown,
   side/rear cloud regions, ears, rear tuft and major attached motifs.
3. **Tertiary:** small scallops, hoof grooves, motif bevels and eye highlights.
   Painted blue/lilac shadows are not automatic cavities or separate pieces.

These are semantic regions, not a committed mesh count, bone layout or topology.
Permanent silhouette belongs to geometry. Head/cheek/eyelid meaning must remain
independent of broad fleece deformation. Local cheek/front/side compression
needs regional ownership so touch acknowledgement does not deform the entire
shell. Ears need independent roots; support limbs need independent contact.
Broad fleece follows primary action and settles; physics cannot define hero
poses, touch response, facial acting or the main fleece silhouette (M, V, D).

## 7. Face / eye construction decision

Preferred **candidate**, confidence Medium: a shallow rounded face surface with
art-directed curved eye surfaces and controlled iris/highlight appearance.
D §7 also permits partial ellipsoid eyes or a geometry/texture hybrid; this
record does not select a tested winner. Physical eyeball realism is not evidence.

The later comparison must preserve the dark oval eye boundary, amber read,
large eye-to-face relationship, small nose/mouth and fleece-framed cheeks from
I. Highlights may need explicit art direction; a lighting highlight alone is
not sufficient evidence of matching identity. Keep room for independent lids,
small mouth changes and local cheek compression. Do not add visible teeth,
human brows or deep muzzle anatomy to solve feeding without approval.

Pending: eye centers and outline landmarks, socket depth, face curvature,
blink/closed-eye design, gaze/convergence bounds and safe mouth/cheek range.
V's twelve presets and five eating styles establish future capability needs,
not measured deformation values. Their implementation and tests are deferred.

## 8. Fleece structure decision

Propose a coherent shell with sparse major cloud regions and designed local
compression, consistent with D §12. Preserve unequal lobe sizes and overlap;
the white canopy and lower collar frame the face while blue/lilac recesses
supply depth. Keep I's large cloud reading even where F/S show many small lobes.
Do not bake all shading into geometry or simulate independent wool balls.

Face-in-Fleece Peek requires an opening that can compress/recover without
swallowing the entire face accidentally, leaking into the head or exposing the
chassis. Front pocket/prop interactions need accessible regions, not invented
permanent holes or visible bags. Shell thickness, head clearance, clump
boundaries and maximum compression remain unmeasured. No solver or morph
implementation is selected here.

## 9. Support / hoof decision

Use four short supports beneath the hidden torso, with rounded brown hoof ends
and restrained visible grooves. Four-support grammar comes from E and S, not
from guessing the number of feet behind I's fleece. F/B each showing two
prominent ends is compatible with overlap, not a two-legged design.

The front should retain readable grounded contact without stretching the legs
to reveal all four hooves. Rare low-forehoof offers and hoof adjustment require
separable fore supports, while rear support remains stable (V §§22/24).
Hoof underside shape, fore/hind separation, contact plane, support polygon and
center-of-mass location are pending. Illustration shadows do not measure them.

## 10. Geometry consequences of the motion contract

| Requirement | Space/structure to reserve later | Unresolved boundary |
|---|---|---|
| Cheek/forehead offers and local touch | Independent face/cheek region, concealed head transition, distinct ear roots | Contact-preserving displacement and clearance |
| Peek / deeper cheek press | Compressible front framing, recoverable opening and protected eye silhouette | Safe depth and occlusion limits |
| Feeding, Moon Ball and Gift | Readable mouth/front contact region and small/medium prop presentation space | Mouth envelope and prop size; no invented grasping anatomy |
| Wear | `head_top`, `ear_root_left`, `ear_root_right`, `fleece_front`; Dream Star Brooch uses `fleece_front` | Placement and size that avoid face/eye/moon-star occlusion |
| Star Peek | L/R/front fleece pocket markers separate from permanent identity stars | Marker positions and temporary prop clearance |
| Heavy support / quiet life | Stable feet plus small independent torso/head motion | Quantified support and deformation envelope |

Anchor names are requirements from V, not measured transforms. No transforms,
colliders or persistent-data changes were created. No core action can require
rear/tail visibility; an orbit camera cannot repair unreadable front acting.

## 11. Camera-dependent cheats

C's front-facing companion view is the operating requirement. I's oblique
illustration is the identity evidence; these are distinct comparison purposes.
Do not silently rotate the companion camera to reproduce I's pose.

Conditional candidates only: shallow face/eye depth, small face-plane or ear
presentation adjustments, and local fleece contour shaping to preserve the
front read. Each would need a named affected region and later front plus
oblique/profile evidence showing that it preserves identity, contact and
attachment. None has been implemented or approved.

Reject hiding a visible identity conflict through camera choice, view-switching
motifs, adding a second moon for a back view, or flattening the entire body into
a billboard. C overrides D's generic camera-estimation workflow for this task:
**do not invent FOV, distance, height, target height, ortho scale, projection or
subject screen occupancy.** The screen-space benchmark / occupancy contract is
**RESOLVED for initial production**. 3D FOV / camera distance / camera height /
target height remain intentionally unresolved until actual Carol blockout
calibration.

## 12. Unresolved conflicts and missing measurements

| ID | Conflict / unknown and evidence | Current disposition | Owner / next evidence |
|---|---|---|---|
| U1 | I's posed broad cloud composition vs F's centered face and taller crown | I wins visible identity; do not declare either a calibrated neutral proportion match | Subsequent camera/framing measurement task annotates face/fleece/ear/hoof landmarks separately for I and F, excluding detached atmosphere |
| U2 | I's broad cloud lobes vs denser S/F clumps | Preserve broad hierarchy; exact correspondence unresolved | Major lobe map remains a condition for later surface-detail lock |
| U3 | Moon visible in F/P/B and varying stars across S/F/P/B/T | No duplicate/mirrored motifs or inferred full-body count | One physical attachment map with anatomical side, same-feature IDs, and opposite profile evidence remains to be confirmed |
| U4 | T's front/back direction and apparent length; no common scale/view axes | Do not derive body depth ratios by comparing canvas sizes | Reference authority owner supplies labeled orientation and common-scale landmarks/plates; exact depth remains pending |
| U5 | Rear tuft visible in S/P/B, but root obscured and canonical does not expose it | Retain supported appendage proposal and approved small expressive use; no invented tail mechanism | Root/neck, allowed outline and small motion envelope remain to be measured against front/oblique identity; generic wagging-dog-tail behavior remains disallowed |
| U6 | Eye/face depth, lid closure and expression envelope absent in static images | Candidate construction only; no claimed prototype success | A separately authorized later prototype would establish ranges |
| U7 | Four-foot grammar vs occluded contacts; head-to-shell clearance unmeasured | No skeleton dimensions, COM or contact polygon asserted | Later authorized geometry work measures foot positions, underside clearance, head cavity and ear-root clearance |
| U8 | Screen-space targets are now defined, but no Carol blockout exists | Screen-space benchmark / occupancy contract is resolved; 3D projection and camera parameters remain pending | Blockout owner calibrates against the contract and supplies rendered bbox, face-center, margin and motion-envelope evidence |
| U9 | V §21 says HIGH front readability for every family, while §27 rows include MED and LOW–MED | Treat HIGH as the requirement, not demonstrated performance; no camera workaround | Motion specification owner reconciles labels before later acceptance planning; this task does not rewrite motion scope |

No pixel ratios, world-space dimensions, camera values, topology budgets or
numeric acceptance tolerances were measured in this task. The images allow
qualitative interpretation; missing measurements remain explicit. A later
measurement record should include source/view, landmark definitions, units,
method and uncertainty. Human approval of this document alone must not turn
these blanks into permission to guess.

## 13. Acceptance evidence and Human Gate

| Evidence item | Present status |
|---|---|
| Canonical reference | I directly viewed; remains authority |
| Approved front reference | F directly viewed; source evidence only |
| Approved 3/4 reference | S posed/turn views directly viewed; source evidence only |
| Approved side/back/top references | P/B/T directly viewed; orientation/consistency limits recorded |
| New matched canonical/front capture | **Not produced**; no model or calibrated camera |
| New 3/4, side and back captures | At the time of this record, the approved individual views in `authority.json` were the geometry authority for the task; that historical six-view authority is superseded for current production by the four FINAL / LOCKED references plus `CAROL_GEOMETRY_PARAMETERS.md`. |
| New isolated silhouette capture | **Not produced**; observations use reference outlines |
| New clay capture | **Not produced**; S's gray chassis diagram is not our model or a passing clay render |
| Deformation / animation / runtime evidence | **Not produced**, outside this task |
| Human reviewer | **Human Gate / user-approved** |
| Human review date | **2026-09-16** |
| Human result / approved revision | **CONDITIONAL PASS** — G1–G5 accepted in principle; unresolved measurements and identity conditions remain explicit |

The recorded Human Gate accepts G1–G5 in principle and retains U1–U9 and the
remaining measurement gaps as conditions. The approved direction includes the
rounded rear tuft as an independent, small expressive appendage, subject to the
acting hierarchy and identity caution above. Reference-packet approval must not
be copied into these result fields.

This pre-production document review is distinct from later model-based identity,
volume, face and deformation gates. Later capture requirements are recorded
here to prevent a false pass, not to authorize creating those assets now.

**Handoff: CHATGPT_PLANNER.** Plan the next repository task for Carol's first
Blender geometry blockout and simultaneous provisional front-camera calibration
against the approved screen-space contract. Camera values remain calibration
variables, and approval of geometry direction does **not** authorize rigging,
animation, GLB export or runtime work until separately authorized. This task
ends with this document committed and pushed.

## 14. v002 structural refinement and presentation clarification

G1–G5 did not need reversal. v001 implementation choices did: its near-flat
body, front-crowded support footprint, lateral rear terminal/tuft, elliptical
lower shelf and common-plane motifs have been replaced. The v002 shell is a
closed connected design volume; face, ears, supports and true rear tuft remain
distinct structural parts. Dimensions are now measured in arbitrary Blender
units in the v002 validation manifest, not asserted as source-image truth.

At that historical point, the Human architecture allowed **Full Companion** to turn/show its back
while the camera remains the front-facing reference. **Close Window-Lean** is a
future approach/rear-weight-shift/forebody-lift pose with front hooves near/on
the lower viewport boundary. These clarify orientation and capability; they do
not change G1 into an upright default or authorize motion implementation.

U1–U6 remain relevant approval limits in that historical record, especially posed-to-neutral identity,
lobe correspondence and hidden motif mapping. U7 has a concrete neutral
four-support proposal and a limited coordinate-only lift estimate, not a tested
COM/deformation envelope. U8's absence-of-blockout premise is historical; v001
and v002 existed in that historical record, while production projection/portrait
framing remained open.
U9 remains a later motion-specification issue.

## 15. V004 canonical-trace recovery — 2026-09-16

The explicit v004 request authorizes rebuilding visible face, eyes, ears and
fleece from restore source `15bfa8e`, while retaining v003 Full-3D anatomy.
BODY_OUTLINE, FACE, independent EAR_L/EAR_R, HEAD and BODY/HEAD lock fields
are extracted as reproducible design data and mapped through normalized source
coordinates. Painted feature approximations are labeled separately from authored
geometry. Historical shallow depth, lateral tail, paint and morphs are not
transplanted into production structure.

Three geometry iterations improved source-relative face/eye/ear relationships
and replaced the rear oval. The final side still reads too much like a pillow;
repetitive front valleys, a lower band and simplified face details remain.
Agent supporting review: **FAIL for full canonical-quality convergence**.
Human result: **PENDING**. No fourth correction loop or rigging advancement.

The saved fleece is closed and connected, with finite coordinates, positive
volume and zero detected nonadjacent triangle intersections. Protected four
supports/hooves, low chassis and rear tuft match v003. These checks do not prove
visual acceptance or deformation readiness. See the [v004 packet](evidence/blockout-v004/README.md).
