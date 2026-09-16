# Grimo — Current Project Memory

**Snapshot:** 2026-09-16  
**Repository:** `snowtone-ai/Grimo`  
**Authoritative working branch:** `codex/carol-zero-based-hero-geometry-v005`  
**Snapshot base commit:** `4957470d0cbf9dfa2021c0f7bf7c59cee1809ec0`

This file is the compact durable memory for agents entering the project without prior chat context. It records current decisions and routing; detailed evidence remains in the linked specifications and production records.

## 1. Stable product and architecture decisions

- Grimo is a smartphone-first PWA with four fixed main areas: Task, Calendar, Grimo, Collection.
- Current character architecture is **Full 3D + Blender-centered production + GLB/glTF + PlayCanvas runtime**. The old PixiJS / 2D / 2.5D implementation direction is obsolete and non-authoritative.
- Carol is the first vertical-slice character. Jill, Pino, and Shushu follow only after Carol validates the pipeline.
- The interaction quality bar is a living companion: independent body-part motion, attention, touch causality, intentional stillness, autonomous initiative, interruption, settling and emotional afterglow. Whole-image squash/stretch animation is prohibited.
- App/runtime product behavior is governed by the product/data specs; character experience by the Motion Bible; generic 3D production by the Blender Production Bible; Carol-specific motion by `CAROL_MVP_MOTION_SPEC.md`.

## 2. Carol visual and geometry authority

### Visible identity authority

`assets/grimo/source/carol/carol-Identity-canonical.png`

Use it for Carol's identity, palette, motifs, appeal, perceived softness/age, and the sacred recognizable front presentation.

### Highest concrete 3D geometry authority

`assets/grimo/source/carol/approved-3d/authority.json`

The six approved individual production views are the highest authority for concrete Carol geometry, volume, proportion, depth and part placement:

1. `carol-front-ortho-transparent.png`
2. `carol-side-ortho-transparent.png`
3. `carol-back-ortho-transparent.png`
4. `carol-top-plan-transparent.png`
5. `carol-front-3q-left.png`
6. `carol-front-3q-right.png`

Side and both 3/4 views must be read with Front. Never infer a flattened face from Front alone. The 3/4 images explicitly constrain facial depth, muzzle/cheek/forehead volume, eye-to-face depth, ear roots, fleece-to-face ordering, body depth, limb fore/aft placement, and overall fleece volume.

`carol-3d-production-canonical-sheet.png` is supplementary; if it conflicts with an approved individual view, the individual view wins for concrete geometry.

Identity canonical must not be used to overwrite concrete depth/thickness/volume/part placement already established by these approved views. Conversely, geometry work must preserve Carol's visible identity and appeal rather than using the geometry packet as permission to redesign her.

## 3. Current Carol production state

Current work is **Carol v005 A/B method comparison** on `codex/carol-zero-based-hero-geometry-v005`.

- **A — zero-based full-volume attempt:** `assets/grimo/production/carol/blender/carol-a-v005.blend`
- **B — historical-mesh deformation experiment:** `assets/grimo/production/carol/blender/carol-b-v005.blend`
- **Recovered historical source:** `assets/grimo/source/carol/historical/carol-15bfa8e-reference.glb`
- **Review packet:** `docs/production/carol/evidence/hero-geometry-v005/README.md`

Neither A nor B is approved hero geometry. Agent visual recommendation is **FAIL for both**; Human comparison is **PENDING**.

Known A issues include unresolved fleece/face/ear geometry and missing motifs. Known B issues include side stretching, intersections and lack of independent four legs. The recovered historical GLB is not proven to be the exact binary previously accepted by the user.

B is the only explicitly authorized exception to the zero-based rule: it may reuse/deform the recovered historical mesh and preserve its UV/paint while evaluating whether the previously liked look can be retained. This exception does not make B approved.

## 4. Gate history and what is NOT authorized

- Initial geometry interpretation: **CONDITIONAL PASS**.
- v001: **CONDITIONAL PASS** structurally; external visual quality was judged very poor and did not authorize rigging.
- v003: explicit Human **FAIL**.
- v004: no Human approval recorded; supporting agent assessment remained FAIL for full convergence.
- v005 A/B: **Human comparison pending**.

Until a Human explicitly approves a hero geometry direction, do **not** treat any current model as final and do not advance automatically to:

- rigging or topology lock;
- production animation;
- final UV/material/shader lock;
- production GLB export;
- PlayCanvas runtime integration;
- main merge.

## 5. Current human decision

The immediate decision is not “is Carol finished?” It is:

> Which construction direction should survive into the next hero-geometry iteration: A, B, a hybrid derived from their strengths, or neither?

Review the raw recovered source as well as A and B before deciding. The v005 packet uses common cameras and five-view comparison evidence. A has fuller volume; B preserves more of the historical painted identity. Neither currently satisfies the approved full-3D target.

## 6. Presentation architecture already decided

Two future presentation states are part of the production concept:

- **Full Companion State:** whole body visible in a low quadruped posture; Carol may turn, walk, show three-quarter and back views. Front is a presentation reference, not an orientation lock.
- **Close Window-Lean State:** Carol later approaches and leans toward the interaction viewport, with face, upper fleece and forehooves prominent. This requires preserved rear support, independent forelimbs and deformable front fleece regions.

These are conceptual constraints only; neither is implemented as a runtime state yet.

## 7. Camera status

- Perspective is the current practical review candidate.
- Orthographic views remain structural-comparison evidence.
- Final production projection/framing remains unresolved.
- Geometry must not be distorted merely to hit portrait occupancy numbers.
- Partner Eevee camera/framing research now exists under `docs/grimo/knowledge/research/camera-framing/` and is research evidence, not permission to alter approved character geometry.

## 8. Knowledge routing

Use `docs/grimo/knowledge/README.md` as the authority index and `docs/repo-map.md` as the repository map. Current execution/gate truth lives in `docs/production/carol/CAROL_PRODUCTION_STATE.md`; detailed v005 evidence lives in `docs/production/carol/evidence/hero-geometry-v005/`.

Research evidence informs decisions but never silently overrides a newer explicit Human decision or a current Carol production contract. `docs/archive/obsolete-2_5d/` is historical only.
