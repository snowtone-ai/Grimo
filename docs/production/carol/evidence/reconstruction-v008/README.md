# Carol v008 — bounded Skin continuation

**STATUS: BLOCKED_AT_V008_SKIN_FINAL_FIT**

**Selected revision: 5. Human Geometry Gate: PENDING; not ready for submission.**

Ear distal shape and head-side curvature improve prior selected revision 2.
Three local attempts ran (4–6); revision 6 was rejected. Root, inset,
head/chest deformation and support fitting still prevent advancement.

## Source and reproduction

- Branch: `codex/carol-final-reconstruction-v008`.
- Fetched starting HEAD: `26cc5c79890d3bc10aaaece5802f3a63c323da0a`.
  Local/remote matched; worktree was clean.
- Asset: `assets/grimo/production/carol/blender/carol-v008.blend`.
- Generator: `scripts/blender/build-carol-v008.py`.
- Evidence: `scripts/blender/carol-v008-evidence.py`.
- Disposable probes: `scripts/blender/carol-v008-clearance.py`.
- Blender **5.2.1 LTS**, build `9e2066aef7ef`; Python/Pillow for sheets.
- Existing session, one agent, no subagents; same geometry phase/toolset.
  Blender CLI/background only; no configuration, plugin or MCP changes.

```powershell
blender -b --python scripts/blender/build-carol-v008.py -- --revision 5
blender -b assets/grimo/production/carol/blender/carol-v008.blend --python scripts/blender/carol-v008-clearance.py
python scripts/blender/carol-v008-evidence.py --revision 5 --include-clearance --publish-blocked
```

The generator always contains selected revision-5 controls. `--revision` labels
output only; it does not switch historical geometry. Rejected source snapshots
remain local. Build outputs use `tmp-carol-v008/revision-5/`; probes use
`tmp-carol-v008/clearance-selected/`. No diagnostic pose is saved to the asset.

The before/after sheet uses prior pushed revision-2 evidence captured before
editing. Reproduce it by adding `--baseline-directory <prior-evidence-directory>`
to the evidence command. Reference registration and hashes must agree.

## Diagnosis and decision

| Area | Root cause | Selected solution |
| --- | --- | --- |
| Ear | Swept ellipses coupled taper and frame orientation; a pink longitudinal face strip did not define a rim-bounded bowl. | Explicit 16-point 3D perimeter, independent inner lip and seven closed shell loops. Control depth separately from silhouette. |
| Head / chest read | Front/back powers 2.7/.85 met at the widest side with zero/infinite slopes, producing a vertical ridge. Closed head/socket/torso overlap also lacks shared transition tangency. | Tangent-matched side-band interpolation and smooth rear-only underside lift. Preserve central frontage and head placement; keep chest unchanged. |
| Support | Proximal mass and Front hoof overlap remain imperfect; placements are frozen. | Preserve them in this task and report remaining shape work. |

Scaling/rotating the bad ear, retracting whole jaw rings, shrinking/moving the
head and enlarging the chest to hide the join were rejected as strategies.
A wholesale fused body would exceed this local task and would not establish
articulation. The socket is already buried; deleting it alone cannot repair
surface ownership. The selected ear shares topology across back shell, rim and
bowl; it is not a flat card or separate pink overlay. ROOT/MID/TIP weights
support later local control, but are not a production skinning setup.

## Attempts

| Revision | Change | Both-view decision |
| --- | --- | --- |
| Prior 2 | Pushed baseline. | Attached tail/fixed supports; triangular ear and vertical cranial ridge. |
| 4 / attempt 1 | Perimeter/rim/bowl ear shell. | Rounder distal Front/Side outline and readable inset. Retained; narrow root/upper fold remain. |
| 5 / attempt 2 | Smooth cranial side join and rear underside. | Removes vertical ridge; softer rising jaw; Front equivalent. **Selected.** |
| 6 / attempt 3 | Broaden ear root, soften inset depth and broaden first chest stations. | Exposed hooked Side root and abrupt Front attachment; insufficient chest benefit. **Rejected in full.** |

Exact revision-5 geometry controls were restored. Final deterministic rebuilds
did not introduce another geometry attempt. Rejected revision 3 is historical
evidence only, not an implementation source.

## Changed and frozen geometry

Only **HEAD_CAGE, EAR_L, EAR_R** changed against the starting blend. Comparison
covered coordinates, world matrices, oriented face connectivity, material slots,
modifiers and render visibility. UV-sphere face enumeration differs between
builds; canonical oriented connectivity agrees.

- Ears: **112 vertices / 110 quads each**, previously 128/126. Seven loops,
  rolled rim, recessed bowl and graded ROOT/MID/TIP groups. Positive-ear bounds:
  X=.37363–.69578, Y=.21955–.58821, Z=.29723–.60051 H; mirrored opposite ear.
- Head: **240 vertices / 238 quads** retained. Side profile joins original
  powers at cos(theta)=+/-.70 with matching tangents. Smooth rear lower lift,
  capped by .065 H control displacement. **70 central-front vertices unchanged**.
  Evaluated X/Y bounds and maximum Z=.70294 H stay fixed. Minimum Z changes
  .22308→.22800 H through underside smoothing. No head move, scaling or muzzle extension.
- Eyes, eyelids, glints/irises, tiny nose, closed mouth and philtrum unchanged.
- Torso, short socket, four limbs/hooves and tail core unchanged. Support
  X=.390/.920; fore Y=+/-.145; hind Y=+/-.245 H.
- Tail pivot=(.985,0,.355); core X=.98963–1.07437 H; rump overlap=.06226 H.
  Independent tail architecture and all twelve debug landmarks retained.
- Four references/hashes, registration, cameras, materials and geometry contract
  unchanged. No new contract interpretation was needed.

## Visual results and motion limits

| Check | Finding |
| --- | --- |
| Skin Front | Better rounded ear/rim; face and grounded stance retained. Head remains squarer; proximal and hoof overlap still differ. |
| Skin Side | Rounded distal ear replaces triangular taper; cranial ridge removed and rear jaw softened. Root and upper inset fold still miss the reference. |
| Head/chest | More coherent neutral read without a new long neck. Separate overlapping surfaces are not a deforming anatomical bridge. |
| Head yaw +/-8 degrees Z | No obvious immediate detachment; jaw/chest overlap slides. Far-ear visibility changes with rotation. |
| Head pitch +/-6 degrees Y | No open gap/catastrophic collapse observed; underside boundary shifts and retains a seam. |
| Head roll +/-5 degrees X | Contact visually retained in small rigid tilts; asymmetric overlap is not soft deformation. |
| Right-ear sweep +/-8 degrees Z | No obvious root tear/detachment; bowl readable, upper inset fold persists. Root deformation/follow-through untested. |
| Support / tail | Fixed during probes; planted read and repaired tail attachment retained. Dynamic COM/support transfer untested. |

All eight transformed states were rendered and inspected in both locked views.
Head probes rotate head, face and both ears about (.410,0,.370); socket/torso
stay fixed. Ear-only probes rotate EAR_R about (.397,-.221,.565). These are
**disposable rigid transforms, not animation or deformation approval**.

Each probe restored the exact neutral digest; the diagnostic left the blend
file unchanged. No rig, keyframe or pose was saved. Cheek/forehead lean, blink,
COM transfer, forelimb adjustment and fleece clearance remain untested. Future
deformation must solve the sliding head/chest boundary and ear-root emergence.

Numerical tail surface-contact counts remain 92 neutral, 81 up 20 degrees,
98 down 20 degrees, and 92 at either lateral 7 degrees. These establish contact
only; they do not approve penetration quality, motion or Human geometry.

## Technical validation

Clean rebuild and independent deterministic rebuild produced neutral digest
**a5fd36d929b747e48c6558f14a88bf03a536fd5b963f69964075a147be6a4dcb**.
Both cameras and the reloaded asset match it. Frozen-object comparison,
reference hashes/registration, fixed supports, planted hoof minima (.0000224 H),
landmarks and resolved reference paths passed. Source hashes are recorded in
measurements and the motion report.

Primary cages retain quads and unapplied subdivision. No hidden alternate body,
Boolean/remesh, armature, production animation, old v007 import or view-specific
geometry was introduced. Python sources parse; diff whitespace is checked.
No unrelated application tests ran. Technical checks do not grant Human PASS.

## Evidence and next bounded task

- [Before / after](skin-before-after.png): LOCKED / prior 2 / selected 5.
- [Registered review](skin-review-sheet.png): LOCKED / selected / 50% overlay.
- [Front](skin-front.png), [Side](skin-side.png),
  [Front overlay](skin-front-overlay.png), [Side overlay](skin-side-overlay.png).
- [Yaw](clearance-head-yaw.png), [Pitch](clearance-head-pitch.png),
  [Roll](clearance-head-roll.png), [Ear sweep](clearance-ear-sweep.png).
- [Motion report](motion-clearance.json), [Measurements](measurements.json).
- [Rejected revision 6](rejected-revision-6-sheet.png);
  [historical rejected revision 3](rejected-revision-3-sheet.png).

Main overlays retain H=1 registration and 1.52-H orthographic span. Before/after
and diagnostic panels share fixed crop (25,200)–(600,550) of 640-pixel renders
solely to remove empty framing; no fitted rescaling or per-view correction.
The registered Front/Side skull-height discrepancy remains visible.

**CHATGPT_PLANNER:** scope ear-root/inset curvature and head/chest surface
ownership next, then reassess proximal silhouettes at frozen support centers.
Retain the improved bowl and smooth cranial side profile. Fleece, Normal and
subsequent production phases remain unstarted. Human Gate remains **PENDING**.
