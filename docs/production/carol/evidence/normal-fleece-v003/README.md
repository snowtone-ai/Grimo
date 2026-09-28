# Carol Normal/Fleece v003 — failed geometry diagnostic packet

Prepared 2026-09-28. **`NORMAL_FLEECE_V003_GEOMETRY_FAILED`.** The requested Human-review candidate was not achieved. **`NORMAL_FLEECE_V003_AWAITING_HUMAN_REVIEW` is not the current state.** v002 is a Human visual FAIL, as explicitly instructed. This packet preserves reproducible failed work and evidence; it must not be presented as a successful successor.

## Result and exact blocker

Three geometry attempts were made, exhausting the explicit task budget. A3 removes A2's horizontal fluting and restores ear visibility, but the fleece still reads as a helmet with broad shelves above and below the face and deep recesses around the ears. The local relief does not produce the required fleece hierarchy. The macro form is not credible enough to begin pigment work. Appearance passes: **0 of 2**.

This is an implementation/convergence failure in the selected section-loft and depth-warp construction. Blender, repository access and rendering worked. There is no external technical-access blocker, and these visual errors are not being excused as unavoidable 3D differences. An additional geometry attempt would exceed the user's explicit limit, so further geometry needs a new production instruction. Color was not used to hide the failure.

## Review evidence

- [01 — authority comparison](01-authority-comparison.jpg): approved Front/Side versus the final saved failed asset. Equal 490px character height, original aspect ratio, ground alignment; Side mirrored only for presentation.
- [02 — geometry overlay, Front ear/chin crops and 3Q](02-geometry-overlay.jpg): pink authority, blue candidate, gray overlap.
- [03 — spatial diagnostics](03-spatial-review.jpg): 3Q, opposite side, rear and top.
- [04 — surface and integration crops](04-surface-review.jpg): neutral fleece, face opening, chin, chest, ears and hooves. This is **not** a completed pigment review.
- [05 — small-scale view](05-small-scale-review.jpg): 160px character height; no device acceptance implied.
- Final native 1000×1000, Cycles 48-sample RGBA views: [Front](front.png), [Side](side.png), [3Q](3q.png), [opposite side](opposite_side.png), [rear](rear.png), [top](top.png).
- [Authority contract](authority-contract.json), [geometry diagnostics](geometry-measurements.json), [ear/hoof/chin proxies](semantic-measurements.json), [saved-asset audit](asset-audit.json), [render manifest](render-manifest.json), [packet verification](packet-verification.json).

The six final native views above come from the same final saved asset, reopened before rendering. Their hashes and camera matrices are recorded. No camera-conditioned geometry, view-switched texture, billboard, paintover, composited authority art or post-render visual correction is used. Comparison sheets only crop, uniformly resize, arrange and label the native/reference images.

## Construction and preservation

The new builder starts from the accepted Skin v002. It generates a spatial section loft whose per-height width comes from current Front constraints and whose depth envelope comes from current Side constraints. Head/torso surface sections share boundary coordinates and preserve semantic ownership; regional and left/right vertex groups remain. There is an independent volumetric tail tuft, retained ears, and four front/pocket/gift anchors. These are authoring affordances, not a rig or deformation PASS.

Wool locks are shallow anisotropic Gaussian displacement fields placed using current approved-image landmarks. A2's periodic outline displacement caused visible side stripes; A3 removes that field and uses spatially localized scallops. The resulting relief is still too weak and smooth relative to the approved fleece, while the aperture warps introduce stronger unwanted shelves. **Do not reuse A3 geometry as accepted authority.**

Accepted Skin source SHA256 remains `321dccd9d7a9789eb3b496b2da2281c03cabb9dcf164f01447c81a9ba940cd7a`. The source file was never overwritten. Candidate eyes/eyelids, continuous three-terminal hooves and solid charms were retained from the delivered v002 asset. The fleece geometry was not retained. Candidate hooves were lowered and widened; the tail was rebuilt as an independent small displaced closed surface.

For the chin, candidate-only lower-front geometry and normals were adjusted and a shallow supporting fleece lip was attempted. No new emissive face shader was added; the face's emission strength was set to zero. The fixed image-aligned chin region is darker than v002 because it also exposes the failed lip/recess. The face brightness proxy cannot separate skin from that encroaching fleece and is not evidence of improvement. **The chin correction is not complete.**

For Front ears, the accepted ear meshes in the candidate use 72% vertical span and 118% longitudinal sweep, with revised root exposure. This reduces the mesh's vertical span, but increased exposure and the ear cavity prevent an improved visible-envelope result; the resulting edge/Side read does not match authority. **The ear integration is not complete.**

The intended pigment method was a stable object-space blend of current Front/Side color, baked into vertex colors with simple rough diffuse shading. It was not applied because the geometry gate failed. Neutral clay is used for the final diagnostic asset. Preliminary pigment preparation was removed from the packet; no completed watercolor appearance is claimed.

## Historical method donor

The read-only historical audit used the pinned `snowtone-ai/grimoire` review documentation at `15bfa8e4c3a8ba24c246fe806bd125b307d8f076`. Transferable ideas were connected silhouette-constrained fleece, shallow relief, outline detail fading inward, controlled face recess, and pigment fixed to real curved surfaces. The historical Side/ridge/rear-depth failure was a warning, not a template. **Historical geometry, coordinates, artwork, UV placement, 624×400 measurements and shallow rear solution were NOT current authority and were not imported.** The audit's verified report was documentation-based; it is not a claim that every historical script detail was independently reproduced.

## Attempt record

| Attempt | Inspected evidence | Finding |
|---|---|---|
| A1 | [comparison](iterations/A1/01-authority-comparison.jpg), [overlay/crops/3Q](iterations/A1/02-geometry-overlay.jpg) | Basic spatial envelope; excessive face recess, lower-eye occlusion from face edit, floating charm placement. Rejected. |
| A2 | [comparison](iterations/A2/01-authority-comparison.jpg), [overlay/crops/3Q](iterations/A2/02-geometry-overlay.jpg) | Lower eyes recovered; periodic silhouette displacement produced side fluting and ear exposure failed. Rejected. |
| A3 | [comparison](iterations/A3/01-authority-comparison.jpg), [overlay/crops/3Q](iterations/A3/02-geometry-overlay.jpg) | Fluting removed, ears exposed; broad shelves/cavities and helmet-like fleece remain. Rejected. |

Iteration PNGs/manifests are historical quick renders of their respective temporary saved assets, distinct from the final six-view manifest. Intermediate binary assets are not retained. A1's early lighting exposure was subsequently corrected; the final fixed review cameras are unchanged. Only the final saved failed asset and its final native packet are the delivery provenance target.

## Reproduce the final failed geometry and packet

Use existing Blender 5.2 and Python/Pillow/NumPy/SciPy; no installation is needed. These commands overwrite only v003 outputs. No application tests are relevant.

```powershell
python scripts/blender/measure-carol-normal-fleece-v003.py
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' -b -t 8 --python-exit-code 1 --python scripts/blender/build-carol-normal-fleece-v003.py -- build --attempt 3
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' -b -t 8 --python-exit-code 1 --python scripts/blender/build-carol-normal-fleece-v003.py -- mark-failed
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' -b -t 8 --python-exit-code 1 --python scripts/blender/build-carol-normal-fleece-v003.py -- render --views front,side,3q,opposite_side,rear,top
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' -b -t 8 --python-exit-code 1 --python scripts/blender/build-carol-normal-fleece-v003.py -- audit
python scripts/blender/measure-carol-normal-fleece-v003.py
python scripts/blender/compose-carol-normal-fleece-v003.py
python scripts/blender/verify-carol-normal-fleece-v003.py
```

## Acceptance

Human approval remains outstanding; this asset is **not review-ready**. No Human PASS, motion PASS, deformation PASS, runtime PASS or device PASS is claimed. Phase 2 has not started. No animation clips, GLB/runtime/device acceptance, merge or PR was performed.
