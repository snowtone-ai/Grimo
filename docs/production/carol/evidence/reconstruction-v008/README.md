# Carol v008 — Skin final-fit continuation

**BLOCKED_AT_V008_SKIN_FINAL_FIT.** Selected revision **9**. Human Geometry
Gate **PENDING**, not ready for submission. The neutral model remains one
shared Front/Side geometry. Its upper ear inset is slightly softer than
revision 5; the ear root and head/chest junction remain material blockers.

## Source and reproduction

- Branch: `codex/carol-final-reconstruction-v008`.
- Clean starting local/remote HEAD:
  `0fb3d38a67763eb87c780c848a8cbbefdf532942`.
- Asset: `assets/grimo/production/carol/blender/carol-v008.blend`.
- Generator: `scripts/blender/build-carol-v008.py`.
- Evidence: `scripts/blender/carol-v008-evidence.py`.
- Disposable probes: `scripts/blender/carol-v008-clearance.py`.
- Blender **5.2.1 LTS**, build `9e2066aef7ef`; Python/Pillow for sheets.

```powershell
blender -b --python scripts/blender/build-carol-v008.py -- --revision 9
blender -b assets/grimo/production/carol/blender/carol-v008.blend --python scripts/blender/carol-v008-clearance.py
python scripts/blender/carol-v008-evidence.py --revision 9 --include-clearance --publish-blocked
```

The generator contains selected revision-9 controls only. Its revision option
labels output and does not reconstruct rejected historical geometry. Build
outputs use `tmp-carol-v008/revision-9/`; probes use
`tmp-carol-v008/clearance-selected/`. To remake the before/after sheet from a
saved revision-5 evidence directory, add
`--baseline-directory <revision-5-evidence-directory>` to the evidence
command. The published sheet uses revision-5 evidence captured before edits.

## Representation diagnosis

| Area | Visible symptom and owning geometry | Underlying cause, cross-view risk and deformation consequence |
| --- | --- | --- |
| Ear root/inset | Side root is narrow; the upper pink boundary makes a hard fold. `EAR_L/R` own both. | The seven-loop rim/bowl topology closes as one oval at the skull and lacks a separately resolved emergence saddle. Moving perimeter controls alone exposes a hook in Side and alters Front width. A narrow pinch limits independent root motion. |
| Head/chest | A line remains beneath the jaw; rigid head probes slide over the chest. `HEAD_CAGE`, `TORSO_CAGE` and buried `SHORT_NECK_SOCKET` share the junction. | Separate closed exteriors intersect without shared tangency or deformation ownership. Deleting the buried socket cannot solve the visible seam. A simple continuous chin-to-torso ring bridge instead produced a hard underside, so a local matched boundary is needed. Changes here can alter both Side jaw and Front chest/cheek. |
| Front cheek | Lower cranial outline is more square than locked Skin Front. `HEAD_CAGE` owns it. | Its current lower horizontal sections are broad; narrowing them blindly risks large-eye/face scale and the improved Side profile. No cheek change was selected. |
| Proximal supports | Front hoof overlap and Side upper-limb masses differ from locked Skin. Fore/hind limb cages and hooves own them. | Root taper, bury depth and torso emergence need local fitting; moving frozen support centers would violate the contract. Work was not reached because ear and head/chest remained blocked. |

The registered Front/Side skull-height discrepancy remains in the references.
It was not corrected with camera-dependent shape, scale or registration.

## Three bounded attempts

| Revision | Hypothesis and both-view observation | Decision |
| --- | --- | --- |
| 7 | Move root perimeter and upper lip to widen/soften emergence. Front remained close, but Side developed a sharper exposed root. | Rejected in full. |
| 8 | Replace separate head/socket/torso exteriors with one semantically grouped head-to-torso cage and short graded bridge. Both views showed a hard triangular underside; it did not read as Carol's soft short transition. | Rejected in full. |
| 9 | Preserve revision-5 outer perimeter and rounded distal bowl. Add buried back-shell saddle controls, ease upper inner lip curvature. Front and Side retain silhouettes; the upper inset fold is mildly softer. | Selected as a limited improvement. |

No fourth geometry attempt ran. The simple full-ring bridge failure is
specific to that construction; it does not rule out a better local exterior
ownership solution. Rejected [revision 7](rejected-revision-7-sheet.png) and
[revision 8](rejected-revision-8-sheet.png) sheets retain their two-view
overlay evidence. [Revision 6](rejected-revision-6-sheet.png) and
[revision 3](rejected-revision-3-sheet.png) remain historical evidence.

## Selected geometry and frozen controls

Only **`EAR_L` and `EAR_R`** changed against pushed revision 5. Each retains
112 controls, 110 quads, subdivision level 2 and ROOT/MID/TIP weights.
`EAR_PERIMETER` is exactly unchanged; the edited `EAR_INNER_LIP` and buried
`EAR_ROOT_SADDLE` are recorded in `measurements.json`. The selected ear has a
softer upper inset but still does not achieve the broad rooted Side reference.

Renderable object comparison used coordinates, world transforms, oriented
face connectivity, materials, modifiers and render visibility. All other
renderables match revision 5, including `HEAD_CAGE`, eyes/lids/irises/glints,
tiny nose, closed mouth, `TORSO_CAGE`, `SHORT_NECK_SOCKET`, four limbs/hooves
and the attached independent tail. In particular, central face controls,
head placement and cheek outline did not change.

Frozen support centers: FORE X=.390, Y=+/-.145 H; HIND X=.920,
Y=+/-.245 H. Tail pivot=(.985,0,.355), Skin core and rump overlap unchanged.
Four reference files, SHA-256 hashes, H=1 registration, cameras and geometry
contract remain unchanged. No fleece, Normal exterior, final retopology,
armature, production animation, Boolean/remesh, GLB or runtime work was added.

## Motion clearance and limits

Both views were inspected at head yaw +/-8 degrees, pitch +/-6 degrees, roll
+/-5 degrees and independent right-ear sweep +/-8 degrees. The bowl remains
readable in the small ear sweep, with no obvious gap or collapse. Head/chest
surfaces still slide in the rigid head probes; no soft junction deformation was
demonstrated. Far-ear visibility changes under head rotation as expected.

The disposable script restores exact neutral channels after each pose and
checks the neutral geometry digest and asset bytes. It creates no rig,
keyframe or saved pose. Cheek/forehead lean, blink, COM transfer and support
adjustment remain untested. These probes reject obvious failures only; they
are **not motion approval or a Human Geometry PASS**.

## Technical checks and evidence

The selected clean build, reloaded `.blend`, both camera digests and motion
restoration agree at
`a0e09b0deb26d349445cbb2ede3380f2f8d4133b1b7968e773a65d81f6ea270e`.
Reference hashes/registration, frozen object comparison, supports, tail,
unapplied quad subdivision and neutral save passed. The tail's evaluated
surface contact remains at all prescribed static pivots; contact counts are
not a penetration-quality or motion result. `measurements.json` records the
exact geometry and diagnostic values. No unrelated app tests ran.

- [Before / after revision 5 → 9](skin-before-after.png).
- [Registered review sheet](skin-review-sheet.png).
- [Front](skin-front.png), [Side](skin-side.png),
  [Front overlay](skin-front-overlay.png), [Side overlay](skin-side-overlay.png).
- [Yaw](clearance-head-yaw.png), [Pitch](clearance-head-pitch.png),
  [Roll](clearance-head-roll.png), [Ear sweep](clearance-ear-sweep.png),
  [motion report](motion-clearance.json), [measurements](measurements.json).

Main overlays retain H=1 registration and 1.52-H orthographic span.
Before/after and diagnostic panels use the same fixed crop
`(25,200)–(600,550)` from 640-pixel renders solely to remove empty framing.
There is no fitted or per-view geometric correction.

**CHATGPT_PLANNER:** use this pushed packet to scope a bounded local
head/chest exterior boundary with matched tangents and deformation ownership,
plus a true broad ear-root emergence. Preserve revision-5/9 distal bowl,
central face and fixed supports. Reassess proximal fitting only after both
authority Skin views improve. Human Gate stays **PENDING**.
