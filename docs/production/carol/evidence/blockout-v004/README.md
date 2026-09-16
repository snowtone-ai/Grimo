# Carol Structural Blockout v004 — HUMAN Geometry Gate

**Target: HUMAN. Human result: PENDING. Agent supporting review: FAIL for full
canonical-quality convergence; partial identity recovery is demonstrated.**
The three permitted geometry iterations are exhausted. This is a reviewable
candidate and evidence packet, not a claim that all visual goals were reached.

## Review first

1. [Face comparison](carol-v004-face-comparison.png)
2. [Ear comparison](carol-v004-ear-comparison.png)
3. [Full review board](carol-v004-review-board.png)
4. [Geometry / clay board](carol-v004-geometry-board.png)
5. [Fleece comparison](carol-v004-fleece-comparison.png)
6. [Registered front overlay](carol-v004-front-overlay.png)
7. [Three-iteration board](carol-v004-iteration-board.png) and [causal QA record](visual-qa.md)

Source: `assets/grimo/production/carol/blender/carol-blockout-v004.blend`.
Branch: `codex/carol-structural-blockout-v004`, based on latest pushed v003
`d2b5ddc5a3e225469a432360ad202ca3cade62bb`, verified before branching.
Commit and remote verification are reported in the task handoff, outside the
commit's own contents.

## Historical source and actual observations

The **user-designated historical visual benchmark** is
`snowtone-ai/grimoire`, `codex/restore-carol-3d-check`,
`15bfa8e4c3a8ba24c246fe806bd125b307d8f076`. It is **not proven to be the exact
final accepted binary from 2026-09-10**. The historical builder and checked-in
GLB are separately recorded; byte-identical regeneration was not asserted.

The actual page at `/plant/carol-3d` was found from source, opened in the existing
local checkout, paused, switched to original mode and captured before modeling.
The page's orbit is limited to ±0.12 rad, so its slight-angle capture is not a
45-degree turnaround. The separate diagnostic viewer captures a 20-degree view.
The original page and historical repositories were left unchanged.

`build-carol-reference.py` supplies independently authored FACE, EAR_L, EAR_R,
HEAD, BODY_OUTLINE, 27 BODY_LOCKS, 21 HEAD_LOCKS, eye centers and eye-line basis,
ear roots, shallow superellipse recess, and moon/star placement. Its front
quality also depends heavily on source-derived paint. **Eye radii, inner-ear
outlines, cheek/nose/mouth contours are not separate historical meshes.** New
manual approximations are labeled separately in the extracted data. The source
warp radii (36,40) are not mistaken for visible eye dimensions.

`build-carol-3d.py` was read as contrast only: analytic ellipsoids, repeated
lobes, symmetric ears and generic facial assembly are not the visible authority.
Its code was not imported into the v004 generator.

See [historical-provenance.json](historical-provenance.json) for source hashes,
renderer values, normalization, capture types and limitations. Only extracted
design data was added; neither the old repository nor its GLB was copied into
current production assets.

## Coordinate and material boundary

Historical source: 624×400. Current canonical: 768×493 (same artwork with a
0.138% aspect-ratio difference after normalized registration).

`u=(x−324)/446`, `v=(380−y)/372`; current Blender coordinates are
`X=3.2112u`, `Z=0.37+2.604v`, front = −Y. Body/face bounds, ear roots, feature
provenance and all authored lock tuples are in
`scripts/blender/carol-v004-reference-data.json`. Source coordinates are never
used directly as Blender units. Depth is independently constructed in full 3D.

Family A uses one orthographic browser camera, registered source coordinates,
requested diagnostic lights/exposure and the unchanged historical materials.
The verified old page actually uses exposure 1.15, opaque background, different
lights, and `toneMapped=false` on materials. Therefore this reconstruction is
explicitly distinguished from direct historical captures. It is not production
camera authority. V003 and v004 use diagnostic materials, without historical
paint. No claimed equality of final material treatment.

Family B retains the exact v003 geometry-review camera transforms, 60 mm
perspective and 5.7 orthographic scale. These remain provisional review cameras,
not a newly approved production camera. Seven 1400×1190 Blender images include
perspective front, orthographic front, three-quarter, side, back, silhouette and
clay; clay/silhouette actually override every mesh material.

## Changes and remaining limits

- Face: closed traced contour replaces generic centered mask; angled broad
  composition, convex cheeks and shallow overlap. Upper contour and jaw still
  read too cleanly separated from the fleece in some views.
- Eyes/features: source-relative centers and 19-degree axis, enlarged expressive
  eyes, diagnostic iris/highlight solids, nose and mouth. Mouth and raised
  eye details are simplified; not canonical-fidelity certification.
- Ears: independent traced closed shapes and separately authored inner-ear
  regions replace mirrored horizontal forms. Left root still looks too exposed;
  inner regions read as inserts rather than naturally recessed tissue.
- Fleece: one closed union of a full-depth body, head region and lower cover;
  original front lock field plus asymmetric directional side/rear fields. Source
  trace relief fades internally to avoid radial fluting. No old lateral tail.
- Side/back: v003's central rear oval is replaced by asymmetric sweeping regions.
  They remain too broad and smooth relative to the approved hidden-volume
  references. Lower cover is visibly a band. Canonical cloud rhythm is only
  partially recovered, and the front has excessive repeated dimple-like valleys.

No fourth geometry iteration was performed. Remaining defects are visible in
the packet and explicitly block an agent PASS. Full-3D depth and part separation
support future work, but rigging/deformation feasibility has not been tested.

## Validation

Saved and reopened `.blend`; four independent supports, four hooves, low chassis
and independent rooted rear tuft match v003 by vertex hash and world matrix.
Fleece: one connected closed surface, positive signed volume 15.1600 BU³,
328,540 triangles, finite coordinates and zero detected nonadjacent triangle
intersections. Fleece bounds: 3.5428×3.4541×2.7352 BU (X/Y/Z), so it is not a plate.
Canonical images, approved references, v003 blend and v003 evidence match
pre-build hashes. No Armature, Actions, animation data or shape keys.

The intersection check is a surface self-intersection check, not a proof of
deformation readiness or all contact correctness. Root overlaps are intentional;
the render review finds no large accidental body penetrations. See
[validation.json](validation.json), [surface validation](surface-validation.json)
and [image metrics](image-metrics.json). No full application test suite was run.
No GLB was exported, so no changed-GLB validation was applicable.

## Reproduction

1. Extract data with Python:
   `scripts/blender/extract-carol-v004-reference.py --repository <historical-repo>`.
2. Run Blender 5.2.1 with `--background --python scripts/blender/build-carol-v004.py
   -- --pass-number 3 --output artifacts/carol-v004/loop3 --width 1400
   --blend-path assets/grimo/production/carol/blender/carol-blockout-v004.blend`.
   The generator also supports the earlier structural stages, but the exact
   earlier captures are the authoritative iteration record; facial cleanup
   was refined during this session.
3. Browser-only mesh JSON is generated under ignored `artifacts/`, never as a
   runtime GLB. A pass-1 run produces the v003 diagnostic JSON. Serve using
   `scripts/blender/serve-carol-v004-diagnostic.py --historical <extracted-root>
   --three <three-package-root> --candidate artifacts/carol-v004/loop3`.
   The server exposes only allowlisted data and binds to loopback.
4. Switch canonical/historical/v003/v004 with the source control; drag or use
   yaw; toggle clay. Capture at 1100×948 (48 px controls + 1100×900 canvas).
5. `scripts/blender/build-carol-v004-review.py` composes the saved captures and
   local iteration renders. It does not synthesize artwork.

## Human decision

Use all twelve questions in `prompt.md`. Record PASS / CONDITIONAL PASS / FAIL
with the views and regions driving that result. **Stop: HUMAN Geometry Gate.**
Main merge, production rigging, animation, final UV/material/shader lock,
PlayCanvas work and runtime GLB integration have not been performed.
