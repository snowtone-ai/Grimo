# Carol v006 — structural correction review

Status: **NOT ACCEPTED / geometry FAIL / Human Gate PENDING**.
Current candidate: **pass 05 / iteration 27**, based on the iteration-16 restore.
This is a revised geometry proposal for Human review, not production acceptance.

## Source and evidence

- Source: `assets/grimo/production/carol/blender/carol-a-v006.blend`
- Generator: `scripts/blender/build-carol-v006.py`
- Six-view renders and geometry data: `iterations/pass-05-iteration-27/`
- Approved / baseline 16 / candidate: `structural-comparison.png`
- Current comparisons and metrics: six root image sets, `metrics.json`
- Saved-asset audit: `geometry-audit.json`
- Changes, deltas and provenance: `structural-handoff.json`
- Exact submitted paths: `changed-files.txt`
- Browser capture and interaction results: `review-*.png`, `review-browser-qa.json`

## Geometry changes and limits

The face now has cheek-dependent widths, recessed temples, short muzzle relief
and an actual mouth recess. Ear roots, drooping outlines, upper folds and bowl
thickness were rebuilt. Each of four supports has a separate short leg and a
tapered hoof with a level sole and toe cleft. The rear has a filled rump and a
recessed attachment for a separate three-dimensional tuft; its lobes are no
longer confined to a flat flower plane.

Fleece uses actual unequal lobe surfaces, quiet recess domes and rounded welded
junctions. The anterior mantle is narrower and the dorsal torso is slightly
fuller. This reduces detail noise and improves structural differentiation, but
**the requested torso-dominant 3Q read is not fully achieved**. Main cloud-group
hierarchy, ear/face correspondence, rear-tuft proportions and hoof softness
still need refinement. These failures are not explained away by metrics.

Iterations 20–25 record the intermediate trials, including rejected tail
extension and mantle-height changes. Iterations 26–27 use the existing bounded
world-space section-fitting tool on iteration 25 to recover orthographic
contours. The saved base profile and camera calibration remain unchanged; the
additional sculpt guide is explicit in the command below. The same final mesh
is used by every camera. No reference image, camera, B-route mesh or historical
source geometry was altered or imported.

## Supporting measurements

| View | Baseline 16 IoU | Candidate IoU | Delta |
|---|---:|---:|---:|
| front | 0.943511 | 0.936253 | -0.007258 |
| side | 0.936985 | 0.944835 | +0.007850 |
| back | 0.921448 | 0.934204 | +0.012756 |
| top | 0.943943 | 0.965988 | +0.022045 |
| 3q-left | 0.826143 | 0.842496 | +0.016353 |
| 3q-right | 0.867420 | 0.889279 | +0.021859 |

Top mean width-profile error: **0.018550**
(target 0.02). Metrics use the existing isotropic bounding-box registration
and provisional 3Q foreground segmentation. No anisotropic image warp or new
mask exclusions were introduced. Silhouette scores do not certify identity,
part separation or full geometric acceptance.

The exact saved Blender asset was reopened: **23 evaluated mesh
objects, 579,406 triangles, 0 non-manifold
edges, 0 non-finite vertices**. Converted smile and
philtrum boundaries are now welded/closed by the generator. These checks do
not validate inter-object collisions, production retopology or deformation.

## Reopen the review

From the repository root, leave both terminals running:

```powershell
python scripts/blender/serve-carol-v006-review.py --port 3017
node scripts/qa/review-carol-v006.cjs
```

If port 3017 already serves this page, reuse that server. The second command
opens maximized Chrome, checks six views and comparison controls, then leaves
Front / Clay open for Human inspection: http://127.0.0.1:3017/ . The old-look
column remains a fixed historical front screenshot, never shape authority.

## Reproduce this candidate

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b --python scripts/blender/build-carol-v006.py -- --pass-number 5 --iteration 27 --resolution 768 --camera-fit docs/production/carol/evidence/reconstruction-v006/iterations/pass-05-iteration-04/camera-fit.json --profile-fit docs/production/carol/evidence/reconstruction-v006/iterations/pass-05-iteration-07/profile-fit.json --section-refine docs/production/carol/evidence/reconstruction-v006/iterations/pass-05-iteration-25/profile-fit.json
python scripts/qa/compare-carol-v006.py --folder docs/production/carol/evidence/reconstruction-v006/iterations/pass-05-iteration-27 --publish
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b assets/grimo/production/carol/blender/carol-a-v006.blend --python scripts/blender/audit-carol-v006.py
```

Intermediate `generator.py` files are source snapshots: restore one to the
canonical generator path before reproducing it, so repository-relative paths
resolve correctly. Baseline 16 is retained as comparison evidence.

No broad app checks, GLB export, runtime integration, rigging, animation or
material lookdev were performed. Motif work remains held. Next handoff:
**HUMAN** — review this structural proposal; no automatic production promotion.
