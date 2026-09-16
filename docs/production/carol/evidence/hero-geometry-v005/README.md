# Carol v005 — A / B method comparison, NOT an approved hero

Date: 2026-09-16. Branch: `codex/carol-zero-based-hero-geometry-v005`.
Starting commit: `041868310df584ae5efa4d05fb9f77877b00d0f7`.

**Outcome: unfinished geometry. Agent recommendation: FAIL for both A and B as
production hero geometry. Human review is pending.** This is a recoverable A/B
experiment and review page, not completion of the original hero-master brief.

## Current user steering

After the original zero-based brief, the user explicitly proposed retaining the
current attempt as Carol A and deforming the old 3D Carol toward the approved
Front/Side/etc. as Carol B, preserving the already-liked parts and surface look.
The user requested an A/B check page in Chrome. This authorizes the historical
mesh reuse in **B only**, superseding the initial zero-based prohibition for B.

- **A**: `assets/grimo/production/carol/blender/carol-a-v005.blend`.
  Frozen after primary passes 1–4, secondary passes 1–2, parts passes 2–3.
  No historical mesh was imported into A. Explicit regional volumes, voxel union,
  new face/eyes/ears/hooves. Fundamental fleece/ear/face defects remain; motifs
  are not implemented. It remains independently reopenable.
- **B**: `assets/grimo/production/carol/blender/carol-b-v005.blend`.
  Historical vertex deformation trial 4; original visible-part topology, UVs and
  paint retained. No remeshing or replacement fleece was added. Original neutral
  facial shape keys are inherited and kept at zero, not new animation work.
- **Historical source**: `assets/grimo/source/carol/historical/carol-15bfa8e-reference.glb`.
  Unmodified recovered binary, SHA-256
  `0871f077abadedb716bdfad5cc57b28e36803da1c868ce23d61ded38a5d2fc21`.
  From `snowtone-ai/grimoire`, `codex/restore-carol-3d-check`,
  `15bfa8e4c3a8ba24c246fe806bd125b307d8f076`.
  **Not established to be the exact binary the user previously accepted.**

## Review

- Local Chrome page: <http://127.0.0.1:3016/> while the local server is running.
- [Five-view A/B board](ab-five-view-comparison.jpg).
- [Actual Chrome comparison capture](chrome-ab-front.png). Five view controls,
  shared camera positions, clay/reset and all four reference images were checked
  in Chrome; no console errors/warnings on the final page.
- A final iteration: `iterations/parts-03/`; B final: `iterations/b-04/`.
- [Approved reference board](01-reference-board.png).
- [Reference registration](landmark-measurements.json).
- [Critical review](visual-qa.md).
- [Saved artifact check](saved-artifact-check.json), [validation](validation.json).

The page renders three models with identical camera, light and scale settings.
Original is unscaled, with original atmospheric decoration; B excludes atmosphere
and hides the legacy outline shell, which intersected the expanded body. A/B
are neutral. Five views, shared yaw/drag, common view span, clay and reset are
available. The four image references below are overview plates, **not** scaled
overlays. The A/B image board uses equal orthographic span 5.8 BU. B's top image
is rotated 180 degrees in the board to match A's front-up convention; the source
render is unchanged. Browser top view uses the same front-up camera for all three,
with a larger common span to include the entire tail.

## B experiment and limits

1. Partwise cage and depth expansion: moved parts but exposed layered surfaces,
   distorted the face and produced severe side stretching.
2. Shared smooth field: improved part registration; face still sheared.
3. Affine face leveling blended into the outside: improved face shape, but lost
   important frontal motif visibility. Outline shell excluded from rendering.
4. Combine the regularized outer cage with a local affine face field; level ears
   and preserve ornament shapes. Face/paint remain recognizable. Forehead and
   ornament intersections, elongated side surface and missing independent legs
   still fail the geometry target.

UV byte hashes match for every retained/deformed visible mesh. This proves
unchanged texture coordinates, **not unchanged appearance**: a deformed surface
can stretch its paint and alter occlusion despite identical UVs.

The recovered model is explicitly described by its source builder as a shallow
relief. Body depth is about 1.125 BU; the front-approved side layout calls for
substantially greater fore/aft volume. Eyes/mouth are painted into Face and feet
into BodyWool. There are no separate four leg objects to merely reposition.
Front-only visual acceptance therefore cannot establish all-view geometry.

Correction to an intermediate verbal diagnosis: the original builder describes
opaque watercolor paint with masked source-pigment transfer. Surface exposure
was initially described as transparent cutouts; this was not a validated alpha
diagnosis. Layered surfaces, outline-shell overlap, paint regions and deformation
are the supported causes/limitations recorded here.

## Assessment / next decision

Preserving the old look is useful. **Pure deformation of this recovered relief
has not produced the approved full-3D Carol.** Do not promote B, inherit historical
approval, or claim hero completion. A's full volume and B's painted identity are
different advantages; neither is approved. Review the raw original in the third
panel first to establish whether it is the user's intended starting source.
If it is, a subsequent hybrid approach needs explicit volumetric fleece/legs and
careful paint transfer; it must be assessed on all views, not presented as merely
stretching a finished four-legged mesh.

## Reopen and serve

From the repository root in PowerShell (Blender 5.2.1 used):

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b --python scripts/blender/export-carol-v005-review.py
python scripts/blender/serve-carol-v005-ab.py --three '..\task-plant-carol3d\node_modules\three' --port 3016
```

Open `http://127.0.0.1:3016/` in Chrome. `--three` can point to another installed
Three.js package containing `build` and `examples/jsm`. It is not fetched from a
CDN. The server binds only `127.0.0.1` and serves allowlisted files; preview GLBs
live in ignored `artifacts/`, never in application/public production routes.

`build-carol-v005-b.py` regenerates B from the retained historical GLB.
`export-carol-v005-review.py` reopens saved A/B without modifying them and creates
browser previews. Canonical images and v004 remain unchanged by checksum.
No rigging, animation production, final UV/material lock, runtime integration,
or main merge was performed.
