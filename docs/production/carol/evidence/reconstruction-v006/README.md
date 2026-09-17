# Carol v006 — reconstruction evidence checkpoint

Status: **NOT ACCEPTED / geometry FAIL / Human Gate PENDING**.
This remains a resumable clay checkpoint, not a production-complete character.
The latest valid state is **pass 05 / iteration 16**, a clean shared-geometry
restore after three camera-correspondence candidates and one coherent rear/ear
volume candidate were rejected.

## Current artifacts

- Blender: `assets/grimo/production/carol/blender/carol-a-v006.blend`
- Generator: `scripts/blender/build-carol-v006.py`
- Final iteration: `iterations/pass-05-iteration-16/`
- Current measurements: `../../carol-reference-measurements.json`
- Final comparison: `metrics.json`, six sets of reference/render/clay/overlay/difference/silhouette images
- Actual head sections and topology: `geometry-audit.json`
- Reference vertical consistency: `reference-vertical-consistency.json`
- Chrome evidence and interaction results: `review-front.png`, other view screenshots, `review-browser-qa.json`
- Overview: `six-view-review-sheet.png`

A contributes the accepted low quadruped/cloud macro direction only. New meshes
are authored by the generator. B is retired from the review and is not imported.
No historical mesh is imported into the new model. The old look column contains
an extracted historical **front screenshot fixed across tabs**, labeled as such;
it is not a matched-view geometry comparison. Its provenance is in
`old-look-provenance.json`. Approved source images are unchanged.

## Geometry at this checkpoint

The head has real cheek/forehead/jaw volume and a recessed mouth. Four separate
hooves and curved closed ear bowls are authored. Fleece uses a sectioned chassis,
major clusters and unequal integrated lobes. A shared world-space section
correction adjusts the waist and side crown; it is independent of the camera.
All six views render the same mesh. Orthographic cameras remain orthographic.
3Q camera candidates are fitted from explicit landmarks, with nonzero residuals;
they are not asserted to recover an original physical camera.

## Iterations 12–16 — residual decomposition and rejected candidates

The 3Q residual was partitioned into crown, forehead, face, both ears, front /
mid / rear fleece, both hoof groups, and lower contour with registered mask
difference areas. At the valid baseline, all large 3Q residuals are model
outward: the two ear zones, lower contour, front fleece and rear fleece are the
largest contributors. The face interior is not the silhouette driver. This
confirms that the rejected iteration-10 global anterior face-depth change is
not a valid root-cause fix.

Candidates 12–14 tested **camera correspondence only**, with the same mesh.
Moving the 3Q cameras can raise raw mask IoU (best isolated values: left
0.885679, right 0.888532), but creates normalized face/ear/hoof landmark
residuals as high as 19%. It is therefore classified as **CAMERA / REFERENCE
CORRESPONDENCE**, not a geometry fix, and is not retained. Candidate 15 tested
a shared compact-ear and rear-canopy geometry group. It degraded Front from
0.943511 to 0.934657, Back from 0.921448 to 0.919783, 3Q Left from 0.826143 to
0.825074, and 3Q Right from 0.867420 to 0.864932; it also introduced 96
non-manifold edges in audit. It is rejected. Iteration 16 restores the valid
same-mesh baseline exactly and publishes its six-view packet.

Classification: the persistent 3Q gap contains a **GEOMETRY** component in
ear/lower/fleece volume, but cannot be certified separately from the documented
**CAMERA / REFERENCE_CORRESPONDENCE** mismatch. The front/side vertical
incompatibilities below remain `PROVEN_REFERENCE_CONFLICT` for only the named
landmarks; they do not excuse the silhouette failures.

**Known failures:** eye/ear correspondence and 3Q identity do not converge;
ear/fleece intersections, generic facial detail, unfinished hoof shaping,
exposed chassis and uneven cloud hierarchy remain. These are model failures,
not excused by reference inconsistencies. Motifs and material/expression lookdev
have not advanced beyond the clay gate. Code for later passes is unvalidated.
Do not export this as production GLB or integrate it into runtime.

## Quantitative evidence

Images are centered on visible bounding boxes and uniformly normalized to the
same height, including the old look image. No anisotropic scaling is used.
The old screenshot's wide bounds constrain the shared display height. In this
packet `*-render.png` is explicitly the clay render; it is not a finished look.

| View | Silhouette IoU | Target | Max landmark error | Silhouette |
|---|---:|---:|---:|---|
| front | 0.943511 | 0.95 | 0.0949 | FAIL |
| side | 0.936985 | 0.95 | 0.1813 | FAIL |
| back | 0.921448 | 0.95 | 0.1829 | FAIL |
| top | 0.943943 | 0.95 | 0.2749 | FAIL |
| 3q-left | 0.826143 | 0.92 | 0.0994 | FAIL |
| 3q-right | 0.867420 | 0.92 | 0.0983 | FAIL |

Top mean width-profile error: **0.031334**;
target <=0.02. All-view acceptance is FAIL. 3Q masks remove border-connected
white and neutral floor shadow in a documented lower band; these are provisional
segmentations, not ground-truth alpha. Native manual landmarks have nominal
uncertainty and require audit. Earlier iteration comparisons used evolving
annotations/segmentation and must not be treated as directly comparable final
scores. Current root metrics supersede them.

The eye's normalized height differs by **7.70%** between Front and Side; nose
height differs by **5.36%**. With the same anatomical point, fixed pose and
horizontal orthographic views, normalized vertical position is invariant.
These differences exceed two 1% error intervals even after nominal annotation
uncertainty. Reconcile the plate pose/projection/correspondence before claiming
strict simultaneous landmark acceptance. This is a conditional geometric
consistency finding, not a decision to alter or override the approved artwork.

## Targeted verification

- 166 evaluated mesh objects; 905,174 triangles.
- Non-manifold edges: 96 (the two converted facial tube objects, `Smile_lip`
  and `Philtrum`); non-finite vertices: 0. This is a topology failure, not a
  rendering or segmentation exception, and prevents a geometry PASS.
- The prior statement that the converted lip/philtrum end caps were closed was
  corrected by reopening and auditing the exact tracked Blender asset.
- Actual head eye-line AP depth: 1.328 world units.
- Inter-object collision, production retopology, deformation and runtime performance are **not validated**.
- Review browser checks cover six views, comparison modes, opacity, grid,
  landmark markers and reset. This is UI validation, not visual character PASS.
- No GLB was exported; no broad app tests or full verification suite were run.

## Reopen / reproduce

From repository root, with Pillow/NumPy and Blender 5.2 available:

```powershell
python scripts/blender/serve-carol-v006-review.py --port 3017
# In another terminal, opens maximized Chrome at Front and leaves it open:
node scripts/qa/review-carol-v006.cjs
```

Local review: http://127.0.0.1:3017/ . The old 3016 entry script now serves this
same review if explicitly started; it has no B route.

```powershell
python scripts/qa/measure-carol-references.py
python scripts/qa/prepare-carol-old-look.py
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b --python scripts/blender/build-carol-v006.py -- --pass-number 5 --iteration 9 --resolution 768 --camera-fit docs/production/carol/evidence/reconstruction-v006/iterations/pass-05-iteration-04/camera-fit.json --profile-fit docs/production/carol/evidence/reconstruction-v006/iterations/pass-05-iteration-07/profile-fit.json
python scripts/qa/compare-carol-v006.py --folder docs/production/carol/evidence/reconstruction-v006/iterations/pass-05-iteration-09 --publish
python scripts/qa/check-carol-reference-consistency.py
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b assets/grimo/production/carol/blender/carol-a-v006.blend --python scripts/blender/audit-carol-v006.py
```

The saved fit JSON files are calibration inputs. Do not regenerate camera fitting
silently during geometry comparisons. Section/cluster entries in generation
metadata are authoring-space parameters; actual final sections are in the audit.

## Human checklist — agent supporting assessment

| Item | Agent assessment |
|---|---|
| Front / Side / Back / Top / 3Q Left / 3Q Right match | NO (each) |
| Face is volumetric / skin survives Side | YES structurally; identity unapproved |
| Eyes / ears / nose / mouth / hooves match | NO (each) |
| Top indentation matches within target | NO |
| Fleece density / major lobes match | NO |
| Fleece avoids equal-sphere packing | YES structurally; hierarchy still fails visually |
| Old geometry not reused / B not used | YES |
| Old look/expression preserved in new materials | NO — lookdev held |

Human decisions remain PENDING. Next handoff: **HUMAN** for reference
correspondence/pose and visual direction; resume **CODEX_ASTRA** geometry work
only under the user's next instruction, with no subagents.
