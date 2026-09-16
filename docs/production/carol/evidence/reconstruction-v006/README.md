# Carol v006 — paused reconstruction checkpoint

Status: **NOT ACCEPTED / geometry FAIL / Human Gate PENDING**.
User requested a clean stopping point and push on 2026-09-17. This is a resumable
clay checkpoint, not a production-complete character. No further modeling is
running. Continue with a single agent only when requested.

## Current artifacts

- Blender: `assets/grimo/production/carol/blender/carol-a-v006.blend`
- Generator: `scripts/blender/build-carol-v006.py`
- Final iteration: `iterations/pass-05-iteration-09/`
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
- Non-manifold edges: 0; non-finite vertices: 0.
- Converted lip/philtrum end caps were closed; the generator now also caps them.
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
