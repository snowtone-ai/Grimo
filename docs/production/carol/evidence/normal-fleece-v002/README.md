# Carol Normal/Fleece v002 — final candidate review packet

Prepared 2026-09-28. **NORMAL_FLEECE_V002_AWAITING_HUMAN_REVIEW.** This is the delivered neutral modeling/look candidate, not a Human PASS. v001 failed Human Phase-1 review; Phase 2 has not started.

Branch: `codex/carol-normal-fleece-v002`. Asset: `assets/grimo/production/carol/blender/carol-normal-fleece-v002.blend`. Exact asset SHA256 and render provenance are recorded in [asset-audit.json](asset-audit.json), [render-manifest.json](render-manifest.json) and [packet-verification.json](packet-verification.json). Git HEAD identifies the delivery commit; the remote equality check is reported in the delivery message rather than embedding a self-referential commit hash here.

## Review evidence

- [01 — approved Front / Side versus v002](01-authority-comparison.jpg): both characters have exactly 540px outline height; aspect ratio and ground alignment are retained. Side is mirrored for comparison only.
- [02 — same-asset 3Q, opposite side, rear and top](02-spatial-review.jpg): derived spatial views, not additional authorities.
- [03 — fleece, pigment and hoof close views](03-surface-review.jpg).
- [04 — 160px character-height readability](04-small-scale-review.jpg): static appearance only; not device QA.
- Native 1000×1000 RGBA, Cycles 48-sample images: [Front](front.png), [Side](side.png), [3Q](3q.png), [Rear](rear.png), [Top](top.png), [Opposite side](opposite_side.png).
- [Eye silhouette measurements](eye-measurements.json), normalized by whole-character height; approximately one-pixel threshold/antialias uncertainty.
- [Professional production judgment and source links](PRODUCTION_JUDGMENT.md).

Every native view comes from the same saved neutral asset. No view-specific mesh edits, paintovers, bloom, depth of field or compositing are used. Sheets only crop, resize, arrange and, where labeled, mirror the images. The manifest ties each native image to the saved asset hash and actual camera/render settings.

Final eye dark-silhouette errors relative to approved Front (image-left / image-right): width **−1.65% / −0.69%**, height **+1.23% / +1.23%**. These are raster-threshold measurements, not exact dimensional or perceptual acceptance.

## Changes delivered

- Individually authored Front/Side fleece lobes form connected head and torso surfaces, replacing the random flower-cluster construction.
- Cheek depth is recessed to expose the Side eye while preserving the Front face frame. The chest connection is recessed so individual scallops replace the broad visible band. Lower-flank linking volume closes the small exposed underbody gap.
- A shared pearl/lilac/azure pigment field spans the fleece. Final look work cools the purple bias, moderates top glaze and adds subtle pigment variation without changing the face lighting.
- Eyes are refined using full-resolution normalized measurements. Hooves are compact continuous brown solids with two localized distal cuts, preserving three terminal lobes.
- Stars adapt the retained [Savino CC0 donor](../../../../../assets/grimo/source/carol/third-party/savino-star/README.md). The original solid crescent is oriented between Front and Side for visibility. The latest Human exception permits ornament shape departures; other visual authority remains in force.
- Neutral fleece/tail shape keys are explicitly zero. This fixes the previous non-neutral comparison bug and is asserted in the saved-file audit.
- The builder saves to a unique sibling before replacing the destination, avoiding Blender's failed overwrite of an existing Unicode-path file on Windows. Render commands use `--python-exit-code 1` to surface Python failures.

## Preserved capabilities and acceptance limits

The accepted Skin source SHA256 remains `321dccd9d7a9789eb3b496b2da2281c03cabb9dcf164f01447c81a9ba940cd7a`; the source file is unchanged. Normal-specific candidate eye, hoof, forelimb and hidden abdomen adjustments do not reopen or overwrite that accepted baseline. Historical v001 assets/evidence are unchanged.

Separate head/torso ownership, independent ears/eyes/tail, regional and left/right masks, neutral local contact/opening channels, and named front/pocket/gift anchors remain. Saved-file checks cover finite mesh coordinates, four hooves, owners, masks, anchors, image dependencies and zero neutral channels. These are authoring capabilities, not a finished production rig.

Human review must judge likeness, cuteness, softness, naturalness and attachment. The render remains a volumetric interpretation: lobe-by-lobe layout, side ear/face projection and watercolor surface character are not proven exact matches to the illustrated references. Those differences are visible in the side-by-side evidence and are not waived by numeric measurements or the ornament exception. No Human, motion, deformation, runtime or device PASS is claimed.

## Reproduce the delivered evidence

From the repository root, with the existing Blender 5.2 and Python/Pillow installations:

```powershell
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' -b -t 8 --python-exit-code 1 --python scripts/blender/build-carol-normal-fleece-v002.py -- render views front side 3q rear top opposite_side
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' -b -t 8 --python-exit-code 1 --python scripts/blender/audit-carol-normal-fleece-v002.py
python scripts/blender/measure-carol-normal-fleece-v002.py
python scripts/blender/compose-carol-normal-fleece-v002.py
python scripts/blender/verify-carol-normal-fleece-v002.py
```

The first command reopens the delivered file; it does not rebuild geometry. Omitting `render` rebuilds from the accepted Skin source and returns to convergence state. Rebuilding is not required for review. See [RESUME.md](RESUME.md) for the final handoff and preserved checkpoint history.
