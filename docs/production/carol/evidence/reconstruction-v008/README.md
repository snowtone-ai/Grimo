# Carol v008 — bounded Human appeal fit

**BLOCKED_AT_V008_SKIN_IDENTITY_FIT.** Revision **14** is retained as the best of two bounded local edits, but the static Skin identity is still not accepted. Human Geometry Gate **PENDING; do not submit for approval**. The primary review image is [skin-human-fit-review.png](skin-human-fit-review.png).

## Baseline and reproduction

The exact pushed revision-12 renders, overlays, face detail, measurements, validation, motion report and clearance sheets were copied to [baseline-revision-12/](baseline-revision-12/) before any geometry edit. Starting remote HEAD: `4c3e55b6f37f5491bf20a9bf95bbe6ea0b42ed3e`; branch: `codex/carol-final-reconstruction-v008`. The four locked source image hashes and registration remain unchanged. Blender 5.2.1 LTS built the single neutral model in the unchanged Front/Side Skin cameras.

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b --python scripts/blender/build-carol-v008.py -- --revision 14
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b assets/grimo/production/carol/blender/carol-v008.blend --python scripts/blender/carol-v008-verify.py
python scripts/blender/carol-v008-evidence.py --revision 14 --publish-blocked
```

The final generator directly constructs revision 14 only. `measurements.json` contains all control and evaluated dimensions, contact ratios, reference hashes and the shared Front/Side neutral digest. `validation.json` verifies the saved/reloaded asset, scene inventory, geometry freeze, supports, eye dimensions, hashes, cameras/registration and absence of production rig or alternate view geometry. The exact revision-12 object record comparison was performed with a local extracted pushed `.blend` and is recorded by checksum in validation.

## Changes and static result

| Area | Revision 13 target and observation | Revision 14 / outcome |
| --- | --- | --- |
| Torso | Central stations `.575: bottom .089/top .414/halfY .303`, `.730: .092/.410/.305`; other stations follow the supplied array. Side is clearly slimmer, with smooth 3Q/Top volume and no visible detached limb root. Head/torso contact ratio `.990`, fore `1.049`, hind `1.047` vs revision 12. | Unchanged. Control maximum width `.610 H`; evaluated width `.59404 H`, below the stated `.595 H` guard by `.00096 H` because subdivision shrinks the target control cage. This numerical discrepancy needs Planner resolution. |
| Lower face | Half widths at Z `.235/.248/.272/.315` became `.070/.173/.256/.300 H`. Mouth base `.3542`, depth `.0065`, min `.3477`, mean `.350152 H`; width `.091 H`. Front chin and mouth read slightly softer/higher. | Unchanged. Side eye/face hierarchy still falls short of the locked image. |
| Hooves | One mesh per hoof, three intended rounded lobes and two shallow anterior clefts; continuous sole; front `.105`, rear `.085 H` nominal extent. Original limb geometry kept. Clefts nearly vanish after smoothing. | **Only revision-14 root cause:** hoof cleft sampling `48→96`, retraction `.009→.011 H`, notch `.0018→.0025 H`. Evaluated width `.217385`, height `.111984`, Side depth `.188536`, min Z `.0000136 H`, all within formal hoof bounds. Front and 3Q still read as broad brown tires. This is the static failure; no further geometry attempt ran. |
| Tail | Pivot `(.985,0,.355)`, center X `1.032`, nine near-round sections, nominal `.085` length / `.095 H` diameter. Evaluated X/Z aspect `.954`. Side is rounder, with no visible stalk. | Unchanged. Top shows partial rump occlusion; do not claim final tail appeal or motion. |

The Human decision **exactly three lobes / two clefts in one continuous hoof** is recorded narrowly in `CAROL_GEOMETRY_PARAMETERS.md`. No independent toes or supports were added. Frozen object records: `EAR_L/R`, `SHORT_NECK_SOCKET`, `NOSE`, `FORE_L/R`, `HIND_L/R`. Changed object records: `TORSO_CAGE`, `HEAD_CAGE`, `MOUTH_closed`, `PHILTRUM`, four hooves, `SKIN_TAIL_CORE`, and minute head-conformal `EYE_L/R`/`EYELID_L/R` resampling caused by the lower-cheek edit. Eye architecture, size/centers/relief and packed pigment are fixed; its pixel hash matches revision 12. Support centers, cameras, registration, materials outside the eye, and locked references remain fixed.

## Evidence and unresolved work

The [primary Human sheet](skin-human-fit-review.png) has four columns (locked, revision 12, revision 14, 50% overlay) and seven rows (full Front/Side, face Front/Side, hoof Front/Side, Side tail), with identical crop coordinates within each row. [Revision 13 sheet](rejected-revision-13-sheet.png), [3Q](diagnostic-revision-14-3q.png) and [Top](diagnostic-revision-14-top.png) are technical diagnostics, not reference authority. [Raw Front](skin-front.png), [raw Side](skin-side.png), [overlays](skin-review-sheet.png), [measurements](measurements.json) and [validation](validation.json) support inspection. The 3Q shows coherent body volume but tire-like hoof mass; Top shows no geometry split, though the small tail is partly occluded.

[Motion record](motion-clearance.json) is explicitly **NOT_RUN_STATIC_GATE_BLOCKED**. The required order selects a convincing static candidate before preflight; revision 14 failed that gate. Numeric virtual tail/rump intersections remain positive at neutral, up/down 20°, lateral +/-7°, but no selected-revision support, yaw/pitch, blink or visual tail preflight was rendered. Revision-12 disposable motion evidence is archived under the baseline and does not validate revision 14. Continuous head/chest exterior ownership, final ear-root emergence, cheek/forehead deformation, intermediate blink tissue, target-convergent gaze, physical COM, fleece and final rig remain unresolved.

**HANDOFF: CHATGPT_PLANNER.** Review this pushed static failure. Resolve the hoof visual owner and the evaluated torso-width guard before authorizing another shape attempt. Human Geometry Gate stays PENDING.
