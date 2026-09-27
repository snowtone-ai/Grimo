# Carol — Phase 1 Normal / Fleece review

**AWAITING HUMAN PHASE-1 REVIEW — NOT APPROVED.**

Candidate: `assets/grimo/production/carol/blender/carol-normal-fleece-v001.blend`.
Starting pushed HEAD: `3b84cbfc65f6d71f5d09a2442913c09d54247ca0`.
Branch: `codex/carol-normal-fleece-v001`.

## Review in this order

1. [Front and Side authority comparison](01-authority-comparison.jpg): identity, face opening, crown hierarchy, fleece envelope, ears and heavy three-toe hooves.
2. [Spatial views](02-spatial-review.jpg): same saved character from 3Q, rear, top and the opposite side.
3. [Bounded deformation samples](03-deformation-samples.jpg): local left contact, opening corrective and independent tail. These are construction diagnostics, not completed acting.

The comparison uses current approved Normal Front and Side only. The moon-side camera naturally faces the opposite screen direction from the approved Side; **only its displayed image is horizontally mirrored**, explicitly labeled, to compare silhouettes. Native [side](side.png) and [opposite side](opposite_side.png) images are retained. There is no camera-dependent mesh, pose or scale. Rear/Top/3Q are derived diagnostics, never authorities.

All neutral renders come from one saved asset. The diagnostic script reopens that file, applies temporary shape-key values or a tail-pivot rotation, renders, and exits without saving. [Asset audit](asset-audit.json) records the saved-file SHA256, topology counts, bounds, baseline differences and diagnostic limitations.

## Construction decisions

- Preserve the accepted Skin's head/face, eye pigment and geometry, eyelids, ears, limb architecture and independent tail core. Original accepted Skin file remains untouched.
- Normal integration exposed two concrete issues: undersized distal hooves and a bare strip below the fleece. Enlarge the existing three-toe hoof modules around their planted support locations to the Normal visible dimensions; tuck only the hidden abdominal underside into the fleece. These changes belong to the single candidate in both Skin and Normal visibility modes.
- Reconstruct the fleece from current Front/Side proportions. Broad unequal volumetric lobes are welded into continuous regional units, with quiet inner transition volumes protecting spatial continuity. There is no imported historical whole-fleece silhouette or camera-facing shell.
- Explicit regions: crown, face-frame, chest/front, central back, lower belly, rump and tail. Head-owned and torso-owned units overlap spatially while retaining separate ownership. The tail shell and its small covered attachment share `TAIL_PIVOT` with the original Skin core.
- Warm pearl, periwinkle and blue form a restrained material hierarchy. Soft roughness, small subsurface response, sheen and very restrained micro-normal detail support the cloud surface. Surface-fitted solid gold stars and one crescent remain character-attached. Rump stars occur on both flanks.
- Every cloud unit has regional and left/right touch groups, a neutral basis and a local compression shape. Face-frame/chest units also have a tapered opening corrective. These are editable construction affordances, not a finished motion library.

## Historical donor audit

The local `carol-a-v006.blend` matches the donor branch's LFS object:
`50f307a665aeccfb9c41f58f5a0731bdcc9c7d74b98650407230cb42404505de`.
Verified donor branch tip: `10ce89a619bbf6c766d8812c21fed56292502f57`.

The actual saved donor has simple Principled materials, a 213,048-vertex fleece structural shell and a separate 16,066-vertex tail unit. It does not contain a sophisticated finished fleece shader to transplant. Retain the useful warm-white/lilac/blue palette concept and welded unequal-lobe construction knowledge; build new materials and new current-scale units.

Targeted v006 evidence also records unsuccessful radial-envelope flowers stretching into scales, repeated filler flowers obscuring hierarchy, obsolete proportions, and unresolved torso/mantle and tuft relationships. The current construction uses actual rounded volumetric surfaces and quiet transitions instead. No old Back/Top/3Q artwork was consulted or restored.

## Motion reverse-design

Read the current Motion Spec's North Star, touch matrix, autonomous/self-comfort, social WAIT, wear, Secrets, gifts, fleece ownership, rig requirements and Human gates. The current Architecture governs full-spatial capability.

| Requirement | Phase-1 construction consequence |
|---|---|
| Face/head conveys meaning first; local touch ACK | Separate head and torso fleece ownership; left/right touch groups and localized compression |
| Cheek/forehead lean, ear roots, eyelid/gaze readability | Open face aperture; cheek fleece set behind the eye plane; no topology weld to ears or eyelids |
| Fleece Nestle, Face-in-Fleece, Hide-and-Peek | Overlapping compressible face-frame and chest units, tapered opening correctives; no monolithic closed helmet |
| Star Peek / gift reveal | Named `pocket_front_L`, `pocket_front_R`, `gift_reveal` markers and controllable front boundary |
| Stable `fleece_front` Wear | Surface-positioned torso-owned anchor, independent of optional residual shape channels |
| Delayed recovery / broad settle | Regional masks and shape channels; macro owner transforms have zero intended lag |
| Tail expression | Tail core, covered attachment and tuft share the existing independent pivot; no rump weld |
| Heavy support / rare forehoof assist | Existing support topology retained; fleece lower regions remain separate from hoof modules |

**No ambient independent ball motion, springs, global jelly deformation or delayed shell translation is implemented or intended.** Recovery is future authored shape change, not transform lag.

## Validation and remaining uncertainty

The executor inspected Front, both sides, 3Q, rear and top; iterated face clearance, lower coverage, crown depth continuity, tail-root coverage, motifs and lighting. Reopened-file checks distinguish inherited facial mesh boundaries from the new closed fleece surfaces.

Perceptual fidelity, cuteness and the exact balance of cloud masses remain Human decisions. The source images have illustrative lighting and asymmetrical motif presentation; the candidate is a single coherent 3D interpretation rather than a per-view reproduction. The comparison does not claim pixel equivalence.

The compression/opening samples establish local geometric controls only. Full head yaw/pitch/roll, deep face burial, support transfer, final collision corrections, attachment behavior through a production rig and runtime export/device performance remain Phase-2 validation. The mesh is an editable authoring foundation; runtime reduction/baking and final rig weights are not completed here. No Human deformation, motion or runtime gate is claimed.

## Reproduce

Run from the repository root with Blender 5.2:

```powershell
blender -b -t 8 --python scripts/blender/build-carol-normal-fleece-v001.py -- views front side 3q rear top opposite_side
blender -b -t 8 --python scripts/blender/review-carol-normal-fleece-v001.py
python scripts/blender/compose-carol-normal-fleece-v001.py
```

For neutral rendering without rebuilding, add `render` before `views`. The scripts never alter approved reference images or the accepted Skin source.

**Next handoff: HUMAN — Phase 1 Normal/Fleece Review.**
