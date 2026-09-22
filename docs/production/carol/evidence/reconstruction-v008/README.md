# Carol v008 — bounded Skin identity reconstruction

**BLOCKED_AT_V008_SKIN_IDENTITY_FIT.** Selected revision **12**. Human Geometry
Gate **PENDING; not ready for submission**. Eyes integrate better and toe
clefts are clearer, but the locked Carol identity has not been recovered.
The Side eye/face, hoof weight, head/chest ownership and ear root still block.

## Source and reproduction

- Branch: `codex/carol-final-reconstruction-v008`.
- Starting clean local/remote HEAD: `0235fbea56766b0edd85970d8f1111f244d96a3e`.
- Asset: `assets/grimo/production/carol/blender/carol-v008.blend`.
- Generator/evidence/probes/verification: `scripts/blender/build-carol-v008.py`,
  `carol-v008-evidence.py`, `carol-v008-clearance.py`, `carol-v008-verify.py`.
- Blender **5.2.1 LTS**, build `9e2066aef7ef`; Python 3.13/Pillow for sheets.
- Single agent, background Blender CLI. Project `multi_agent=false` and
  disabled Blender/runtime MCP configuration were already sufficient.
  Repository Skills directory was absent. No plugin/configuration changes,
  reload, external service, generated references or runtime tools were needed.

```powershell
blender -b --python scripts/blender/build-carol-v008.py -- --revision 12
blender -b assets/grimo/production/carol/blender/carol-v008.blend --python scripts/blender/carol-v008-verify.py
blender -b assets/grimo/production/carol/blender/carol-v008.blend --python scripts/blender/carol-v008-clearance.py
python scripts/blender/carol-v008-evidence.py --revision 12 --include-clearance --publish-blocked
```

Generator contains only selected revision-12 geometry. It does not switch to
historical shapes. Build output: `tmp-carol-v008/revision-12/`; probes:
`tmp-carol-v008/clearance-selected/`. The committed `baseline-revision-9/`
contains prior pushed raw views and measurements for reproducible comparisons.
The published validation additionally used pre-edit local object records and
the first revision-12 digest to compare frozen objects and the clean rebuild.

## Diagnosis and architecture decision

The four FINAL/LOCKED references and numerical contract governed geometry.
The identity canonical was inspected only for secondary appeal support.
Actual revision-9 Blender data, raw views, overlays, before/after sheets,
rejected 7/8 sheets and all four previous clearance sheets were inspected.
A local decision note was written before the first geometry edit.

Primary torso length, head/body scale and low support architecture were already
useful. The largest failures were secondary forms: eye integration, facial
curvature, hoof crown/leg emergence, then head/chest and ear root. Small iris
objects and reflections amplified these failures; tertiary decoration could
not repair the underlying volumes.

| Area | Root cause and selected strategy | Rejected alternative and remaining motion risk |
| --- | --- | --- |
| Eyes | The old closed ellipsoid plus solid iris/glint modules stood off the face. A shallow curved patch now follows an upright orbital housing belonging to the head; pigment and highlights share its surface. | A full or thinner ellipsoid preserves the independent globe edge. A flat card loses Side volume. A patch on the uncorrected head slants in Side (attempt 10). Future blink must close the aperture on the skull; gaze must move pigment, not rotate a ball. |
| Face/head | Monotonic frontage and broad low rings made a generic cranial shell; nose/mouth were independently placed. More local sections, a short central muzzle, rounder lower cheek and sampled facial attachments are retained. | Shrinking Front or flattening the entire head sacrifices one view. The Side jaw/forehead relation still fails; no cute-profile claim is made. |
| Hoof/support | Uniform ring profile, weak toe indentation and distal limb coverage hid crown volume. Paired toe clefts, rounded crown and distal-only limb taper redistribute volume within the numerical envelope. | Raising overall hoof height or moving supports violates authority. A forward-shifted crown looked like a tilted slipper (11). Side remains too slab-like even after correction. |
| Head/chest | Separate intersecting closed surfaces have no shared exterior/deformation ownership. No junction redesign was selected while facial identity remained blocked. | Prior whole-ring bridge (8) produced a triangular chin. Rigid head probes cannot establish soft continuity; sliding remains a blocker. |
| Ear root | Narrow oval emergence and upper inset fold remain. Entire revision-9 ear geometry was preserved to protect its rounded distal bowl. | Perimeter widening previously exposed a pointed root (7). Root articulation remains provisional. |

The chosen eye is a **geometry + packed UV pigment hybrid**. Its Front span
remains .137 x .149 H at Y=+/-.162; shared center Z=.418 H is derived from
Skin Front. Maximum X relief is .014 H, tapering to .0008 H at the edge.
A head-sampled skin margin owns the aperture transition. Warm lower iris and
large/small/star glints are diagnostic identity cues, not separate meshes.
No bloom, camera-facing cards, per-view scaling or production facial rig is used.
A future portable texture can use the same UVs; no runtime/export work occurred.

## Three meaningful attempts

| Revision | Both-view observation | Decision |
| --- | --- | --- |
| 10 | Globe protrusion disappeared; Front pigment improved. The patch inherited the cranial slope and became a diagonally tilted Side eye. Crown/cleft changes alone were insufficient. | Rejected. [Evidence](rejected-revision-10-sheet.png). |
| 11 | Cranial orbital housing made the eye upright in both views. The forward-shifted hoof crown made a tilted Side slipper edge; eye read remained matte/graphic. | Superseded; crown strategy rejected. [Evidence](rejected-revision-11-sheet.png). |
| 12 | Retains orbital housing; shared aperture rises .008 H, curved relief/gloss increases modestly, lower cheeks round, symmetric hoof crown replaces the shifted one. Front is more integrated; Side no longer has the inserted ball/slanted patch. | Selected partial improvement. Broad Side reflection and remaining form failures still block identity. |

Exactly three design attempts ran. The later clean rebuild reproduced the
selected neutral digest; it was not an additional design attempt. No shape
changes were made after revision 12 was reviewed.

## Exact changed and preserved scope

Changed geometry: **`HEAD_CAGE`, `EYE_L/R`, `EYELID_L/R`, `NOSE`,
`MOUTH_closed`, `PHILTRUM`, `FORE_L/R`, `HIND_L/R`, `HOOF_FORE_L/R`,
`HOOF_HIND_L/R`**. Only the bottom two control sections of each limb changed;
proximal sections stay as before. Removed: **`IRIS_L/R`, `GLINT_L/R`**,
whose visual roles moved onto eye pigment. No new renderable object was added.

Exactly preserved renderable records: **`TORSO_CAGE`, `SHORT_NECK_SOCKET`,
`SKIN_TAIL_CORE`, `EAR_L`, `EAR_R`**. The comparison includes control
coordinates, transforms, face connectivity, material slots, subdivision and
visibility. Skin debug materials outside the eyes, lights/cameras, debug
landmarks and support targets were retained. The compact torso, low chassis,
bilateral supports, independent tail/rump attachment and rounded distal ears
are preserved. There is no hidden alternate body or alternate view model.

FORE: X=.390, Y=+/-.145 H. HIND: X=.920, Y=+/-.245 H.
Evaluated hoof width=.223243 H, height=.112967 H (both within +/-2% of
.219/.111); minimum Z=.000029 H. Toe/crown redistribution does not relocate
the sole/support controls. The independent tail keeps the same pivot, geometry
and positive rump contacts in all existing static pivot probes.

## Neutral visual finding and gate

- **Front:** warm lower-eye hierarchy and integration improved; eye size was
  not reduced. Cheek corners are softer, but the head still looks more rigid
  and less soft than locked Carol. Broad front/rear hoof overlap persists.
- **Side:** ball protrusion and slanted aperture were removed. A broad grey
  reflection now washes out iris contrast. Eye/face hierarchy, tiny muzzle
  and lower jaw remain insufficiently close; this is not an accepted cute profile.
- **Hooves:** clefts and roundness are more readable. The heavy planted mass
  in the reference is not yet reproduced, particularly in Side.
- **Head/chest and ears:** no solution is claimed. Separate shell seam and
  narrow root remain visible.

Existing registered Front/Side skull/feature-height differences were not
hidden with per-view edits. The numerical authority remains unchanged and
still governs shared eye/hoof dimensions. Technical conformity does not
legalize the unresolved visual failures.

## Disposable motion rejection probes

Fifteen cases were rendered in both unchanged cameras: head yaw +/-8 degrees,
pitch +/-6, roll +/-5, right-ear root sweep +/-8; iris offsets +/-0.14 UV
horizontally and +/-0.12 vertically; one closed-eye endpoint; imposed body
shifts +/-0.010 H longitudinally with -.004 H settle and graded limb response.
These followed the visible improvement in eye integration, not an identity
approval. They are rejection probes and did not advance the production phase.

- Head rotations did not show a gross open hole or eye detachment at these
  small values, but the jaw/chest seam and sliding persist. There is no shared
  soft-tissue ownership. The broad Side eye reflection varies strongly with
  yaw/pitch, confirming a readability risk rather than fixing neutral appeal.
- Ear sweeps preserve the distal bowl with no obvious small-range detachment;
  the root remains narrow. This is not an approved articulation range.
- Iris offsets remain on the fixed aperture. Downward gaze clips the gold
  region at the lower rim; the shared mirrored pigment is not convergent
  target tracking. Attention readability is weak at full-body phone scale.
- The closed-eye endpoint leaves a continuous skull and no empty socket.
  Its closed line is too faint at phone scale. Intermediate lid travel,
  tissue volume, cheek touch and forehead touch remain unvalidated.
- Small support shifts keep evaluated hoof minimum Z exactly unchanged and
  show no obvious floating or detached ankle. This is an imposed deformation,
  not a mass-weighted COM simulation or approval of anticipation/settle.

Every probe restored exact neutral geometry **and** packed pigment; the saved
asset bytes were unchanged. No pose, animation, shape key or rig was saved.

## Evidence and technical verification

The clean selected build, saved/reloaded asset and both cameras agree at
`a189086ab4f2414a38c020db3f478539d5e95e330dd486f17ab0be6dc534212d`.
[Validation](validation.json) records exact changed/frozen inventory, the
numerical checks, reference hashes, same-view digest, neutral state and
absence of production rig, animation, keyframes or Boolean/remesh.
[Measurements](measurements.json) contain the selected controls and bounds.
No app tests, GLB export, fleece, Normal geometry or production animation ran.

- [Full before/after + 50% overlays](skin-before-after.png).
- [Face detail](skin-face-detail.png), [registered sheet](skin-review-sheet.png).
- [Raw Front](skin-front.png), [raw Side](skin-side.png).
- [Front overlay](skin-front-overlay.png), [Side overlay](skin-side-overlay.png).
- [Yaw](clearance-head-yaw.png), [pitch](clearance-head-pitch.png),
  [roll](clearance-head-roll.png), [ear sweep](clearance-ear-sweep.png).
- [Horizontal gaze](clearance-gaze-horizontal.png),
  [vertical gaze](clearance-gaze-vertical.png), [closed eye](clearance-blink.png),
  [support shift](clearance-support-shift.png), [report](motion-clearance.json).

Full comparison panels use the unchanged crop (25,200)-(600,550) of the
640-pixel renders. Detail panels use Front (170,225)-(470,445) and Side
(30,225)-(330,445), identical across reference/prior/selected/overlay within
each view. They are camera-derived image crops only. Raw full images remain.

**HANDOFF: CHATGPT_PLANNER.** Scope the next bounded identity correction from
this pushed packet. Do not proceed to fleece, final materials, production
rigging, GLB or runtime, and do not declare Human Geometry PASS.
