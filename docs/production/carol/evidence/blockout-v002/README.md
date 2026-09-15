# Carol Structural Blockout v002 — review packet

Date: 2026-09-16. **Human Gate: PENDING. Next handoff: HUMAN.**

Starting local and pushed HEAD both matched
`2bf64edea4043ac1dfda1f105ad975c6dedb4386`; the working tree was clean.
v001 Human result is **CONDITIONAL PASS**, with approximately **5/100** external/
final visual quality and a structurally useful direction. v002 does not inherit
a visual pass from that decision.

## Evidence

| Image | Review purpose |
| --- | --- |
| [Front Perspective](carol-v002-front-perspective.png) | Primary practical front identity candidate |
| [Front Orthographic](carol-v002-front-orthographic.png) | Structural comparison; not production projection selection |
| [Three-quarter](carol-v002-three-quarter.png) | Face nesting, ear thickness, side transition, support depth |
| [Side](carol-v002-side.png) | Low chassis, face profile, front/rear support and tuft |
| [Back](carol-v002-back.png) | Complete rear body, closure, independent subordinate tuft |
| [Silhouette](carol-v002-silhouette.png) | Opposite three-quarter outline with uniform unlit material |
| [Clay](carol-v002-clay.png) | Uniform gray materials; geometry without color separation |
| [Comparison board](carol-v002-comparison.png) | Canonical, v001 front, v002 front/three-quarter/side/back |

Individual views are 1400x1190 transparent PNGs. The board places images on
white, independently fits each panel, and is **not** a common-scale measurement
plate. Canonical source pixels were never overwritten. The canonical is posed
and includes detached atmosphere; v002 is an unposed neutral body study.

## Visual iteration record

All five geometry iterations were directly inspected in front Perspective,
front Orthographic, three-quarter, side, back and silhouette. Intermediate
renders remain disposable local artifacts; only the final seven and compact
comparison are committed.

| Pass | Diagnosis and correction | Comparison result / next issue |
| --- | --- | --- |
| 0: source diagnosis | Viewed canonical, all five approved reference images, v001 front projections, three-quarter, side, back and silhouette; opened v001 `.blend` for structural inventory | Largest errors: wafer-like depth; giant smooth crown; disconnected front shelf/face; hidden ears; crowded supports; tuft on lateral X rather than rear Y; cropped back |
| 1: macro | Rebuilt the concealed chassis with depth, separated fore/rear supports, embedded a shallow face, moved tuft to actual rear; fused overlapping envelope volumes | Genuine four-support body, but balloon-like large faces and lower band remained |
| 2: hierarchy | Introduced directed crown/brow/cheek/flank/rear transitional volumes; attached motifs to shell depth | Front/back continuity improved; medium lobes too submerged in major masses, cheek opening too angular, side still too smooth |
| 3: character structures | Reduced the dominant masses to expose hierarchy, added local scallops, enlarged thick bowl ears, compound small tuft and rear support coverage | Shelf broken into changing-depth cloud volume; ears and tuft readable; face lower opening too narrow and crescent tips showed discontinuities |
| 4: cleanup | Broadened exposed lower face, shortened face height, moved lower cheek turns, repaired motif thickness/tips | More shallow rounded face; no external neck or muzzle; coherent clay read; side shoulder still over-dominant |
| 5: bounded final correction | Reduced right shoulder depth/height and offset flank transition; gave ear a brown upper region and subordinate pink bowl; adjusted crescent body | Side hierarchy improved without losing front envelope. Saved and inspected final seven views; stopped before fine surface/beauty work |

The generator's `--pass-number` selects macro-only (1), macro+medium (2), or
all final region groups (3). It is not the chronological iteration number and
does not recreate earlier edits byte-for-byte. Default 3 reproduces final v002.

## Structural decisions

- **G1 retained:** hidden low chassis and four short supports. Fore roots are
  at `(±0.68, -0.69, 0.69)`, rear roots at `(±0.73, 0.91, 0.69)`. Front is -Y.
  Hoof soles meet Z=0.025; there is no upright neutral posture.
- **G2 retained:** face is a shallow rounded acting volume nested among brow,
  cheek and chin forms. Its front reaches Y=-1.45, within the fleece's front
  envelope (approximately -1.486). The eyes/nose/mouth are landmarks only.
- **G3 retained:** 13 primary, 22 medium and 13 local control volumes form one
  connected, closed remeshed sculpt. These are design controls, not 48 separate
  animated wool objects or final topology. The lower volume varies in height,
  width and depth into the flanks instead of forming a horizontal disk.
- **G4 retained:** the independent tuft is centered on the actual rear, with a
  root at `(0, 1.43, 1.02)`. It extends approximately 0.35 beyond the main rear
  fleece envelope. It is visible in full side/back evidence and subordinate.
- **G5 retained:** one crescent and five provisional front-associated stars
  have thickness and follow actual shell depth. No additional back motif was
  invented. This does not settle contradictory full-body reference mapping.

v001 decisions G1–G5 did **not** require reversal. Its implementation of depth,
tuft direction, lower collar, supports, ears and motif surfaces did require
substantial revision. Neutral fleece bounds are about **3.592 wide x 3.171 deep
x 2.644 high**, in arbitrary Blender units; exact bounds and hashes are in
[validation.json](validation.json). These are model measurements, not a claim
that the source images establish physical dimensions.

## Full / Close feasibility

**Full Companion:** the front-facing camera is the reference, not an orientation
lock. Side/back closure, independent rear tuft and fore/rear supports provide a
coherent neutral body for future turning/walking. Animation is not implemented
or validated by still images.

**Close Window-Lean:** independent front supports and hidden roots can be
articulated later; no rigid front disk blocks them. A coordinate-only estimate
rotates the shell mathematically about the neutral rear-hip line `(Y=0.91,
Z=0.69)`. It neither transforms the saved model nor creates a pose or Action.

| Assumed forebody lift | Lowest fleece Z | Fore-root Z | Chassis-center Y |
| --- | ---: | ---: | ---: |
| 20 degrees | 0.188 | 1.237 | 0.181 |
| 35 degrees | 0.113 | 1.608 | 0.286 |
| 45 degrees | 0.067 | 1.821 | 0.380 |

The sampled rigid shell stays above the ground even at 45 degrees, so no
obvious rear-shell collision forces a chassis rebuild. The chassis center is
only a proxy for mass; it is **not** a computed COM. At 45 degrees it is still
roughly 0.50 in front of the rear hoof center, beyond that hoof's roughly 0.31
half-depth. Rearward weight transfer and/or sill contact are therefore required.
Actual rear joints, forelimb reach, local fleece compression, face pitch and
contact must be tested in separately authorized deformation work. This is
plausibility evidence, not certification of a balanced Close pose.

## Honest limits for Human review

The chassis, attached parts and all-view closure now form a convincing neutral
structural proposal. No inspected view demonstrated a necessary chassis
rebuild. However, the requested **85–90/100 overall structural confidence is
not established as an acceptance result**. In particular:

1. The neutral face-opening and crown proportions interpret a posed canonical;
   the exact frontal correspondence remains unresolved. The cheek/brow opening
   still has coarse sculpt transitions and may need regional remodeling.
2. Large/medium/small hierarchy is present, but the precise cloud grouping and
   silhouette rhythm require Human identity judgment. Side/rear forms are
   coherent proposed depth, not calibrated reference measurements.
3. Crescent relief still shows coarse surface sampling; final smoothing is
   deferred. Hidden star/moon correspondence is unresolved; no new motifs solve it.
4. Ear cross-sections, tuft root and support locations remain blockout proposals.
   Expression, root clearance under motion, contact and Close balance are not
   tested. Final eye appearance, fleece shading and texture are not evidence here.

Do not approve rigging or call this production-ready based on generation alone.

## Validation and reproduction

Verified with Blender **5.2.1 LTS**: generation, seven nonempty uncropped renders,
save and reopen; `Carol_Model`, `Carol_Face_Center`, all review cameras, four
support meshes and independent tuft; one closed connected fleece volume;
zero armatures, Actions, object animation data or shape keys. Canonical and
v001 SHA-256 values remained unchanged. No GLB/glTF export occurs in the script.
No web/runtime QA was run. Final Git checks are recorded in the session handoff.

From the repository root in PowerShell:

```powershell
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --python-exit-code 1 --python scripts/blender/build-carol-blockout.py -- --blend-path assets/grimo/production/carol/blender/carol-blockout-v002.blend --evidence-dir docs/production/carol/evidence/blockout-v002 --width 1400
python scripts/blender/build-carol-blockout-comparison.py
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background assets/grimo/production/carol/blender/carol-blockout-v002.blend --python-exit-code 1 --python scripts/blender/inspect-carol-blockout-feasibility.py
```

The comparison helper uses Pillow; the Blender generator uses Blender-bundled
Python/NumPy. Reproduction may change render/file hashes across machines;
`validation.json` records the actual delivered source and image hashes.
