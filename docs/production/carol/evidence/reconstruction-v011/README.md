# Carol v011 — bounded Phase A refinement, visual gate failed

**Technical static gate: PASS. Executor visual precheck: FAIL.**
Selected **v011-A3 is diagnostic only, not promoted**. Human Geometry Gate is
**NOT_REVIEW_READY**. Motion clearance was not run because the visual prerequisite
failed. Three attempts are exhausted; no A4. Phase B/C remain not started.

Source branch: `codex/carol-final-reconstruction-v010`, exact commit
`9569bea8e08e0e068ed7debadf242419e9655a40`. Remote fetch confirmed the expected
HEAD, clean source worktree, and no superseding remote Carol mutable state.
Working branch: `codex/carol-final-reconstruction-v011`.

## Retained structure and bounded changes

The v010-A3 topology family and exact face connectivity are retained: 533
vertices, 1,062 edges, 531 quads, one component, zero nonmanifold edges,
Euler 2. There is one exterior `CENTRAL_CHASSIS`. No Boolean, remesh, new patch
family, hidden shell, or view-dependent geometry was introduced.

- Replace the cranial `.6*c + .4*c³` depth sections with elliptical sections.
  This removes the posterolateral shoulders while preserving the lateral Front
  control contour and head height.
- Redistribute lower-head depth and round the interior sagittal underside.
  A3 changes interior lower-head Z; it does not claim every Front-projected
  control vertex is unchanged. The maximum change is in `measurements.json`.
- Replace the steep `1.12` planar orbital target with a curved local surface:
  `.60` lateral tangent plus curvature in lateral and vertical directions.
  The eye cap uses a spherical depth profile with `.040 H` central normal
  relief; lids follow the same local surface. Front aperture dimensions and
  centers remain `.137 × .149 H`, at `±.162 H`.
- Seat the anterior chest cap behind its concave upper rim and round its lower
  interior. This is a local vertex correction within the same quad disk.

## Attempts and rejection evidence

| Attempt | Disjoint control / evaluated | Adjacent improper contacts | Result |
| --- | --- | --- | --- |
| A1 | 0 / 0 | 2 control / 0 evaluated | Technical FAIL: chest cap crosses neighboring neck-strip faces; no renders |
| A2 | 0 / 0 | 0 / 0 | Technical PASS, visual FAIL: Side eye too far forward/exposed; long under-cheek |
| A3 | 0 / 0 | 0 / 0 | Technical PASS, visual FAIL: dominant Side underside and narrow Side eye remain |

A3 tested 5,903 control and 93,515 evaluated adjacent triangle pairs with the
unchanged v010 detector, shared-contact rules and `5e-7 H` tolerance. No detector
threshold was relaxed. The A1 failure is retained in `attempt-1.json`; A2 has a
compact numerical record and `attempt-2-diagnostic.png`.

Front remains soft, with the eye locks intact and no meaningful observed
silhouette drift. The near eye's whole-cap derived 3Q width/height ratio falls
from **1.349 in v010 to 1.080 in v011**. This is geometric projection evidence,
not an occlusion-aware visual acceptance metric. Top's posterior shoulders are
rounded, though a slight anterior taper remains after the local socket edit.

**Strongest remaining rejection:** Side still exposes a long oblique lower-cheek
surface instead of the short rounded head/chest turn in locked Skin Side. The
Side eye is also too narrow and exposed: whole-cap depth span falls from about
`.145 H` to `.102 H`. Better 3Q roundness does not compensate for that Side
identity loss. The multi-view eye/socket gate and overall visual gate fail.

## Evidence and frozen scope

- `diagnostic-sheet.png`: locked Skin Front/Side, candidate, 50% overlays,
  derived 3Q and Top; fixed registration, no fitting.
- Individual Skin Front/Side, overlays, Face Front/Side crops and derived
  diagnostic images are included. Renders use 480-square / 16-sample Cycles;
  crops and overlays use the inherited fixed 640-pixel display registration.
- `validation.json` and `measurements.json`: topology, contact evidence, hashes,
  registration, rear-station retention, frozen-object fingerprints, ocular
  dimensions/projections, and truthful failed disposition.
- Asset: `assets/grimo/production/carol/blender/carol-v011.blend`, saved neutral
  with failure status; reload confirmed the same geometry digest and frozen
  objects. The source v010 blend is byte-identical.

Four locked source hashes and saved registration were verified before edits.
Ears, hooves, limbs, tail, support centers, cameras, lights, materials and
reference images remain unchanged. Rear control stations at `.730 H` and
rearward have zero coordinate delta. Temporary predecessor ear/hoof defects
remain outside scope. No fleece, production rig, animation, GLB, or runtime
work was performed.

The existing configuration was sufficient for this same Phase A task:
`multi_agent = false`, Blender MCP disabled; background Blender 5.2.1, local
image inspection, Python/Pillow evidence composition and Git only. No plugins,
subagents, configuration changes or architecture restart were used.

Reproduction: run `blender --background --python scripts/blender/build-carol-v011.py
-- --attempt N --render` for N = 1, 2, 3. A1 stops at technical failure.
`--attempt 3 --finalize-failure` archives the inspected A3 without a new geometry
attempt. Copy its four render PNGs from the temporary attempt folder to this
folder, then run `python scripts/blender/carol-v011-evidence.py` with Pillow.
Reproduction does not authorize additional shape iterations.

Next handoff: **CHATGPT_PLANNER**. Further geometry work requires a new bounded
handoff; this result does not prove a topology-family change is necessary.
