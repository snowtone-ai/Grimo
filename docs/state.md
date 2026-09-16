> Current Carol checkpoint (2026-09-17): v006 is paused at the user request, geometry FAIL / Human Gate PENDING. B is retired. The v005 A/B selection described below is historical. Follow [the v006 evidence and handoff](/docs/production/carol/evidence/reconstruction-v006/README.md) and /prompt.md for the current state. Single agent only; resume modeling only when requested.

# Production state

**Snapshot:** 2026-09-16
**Current authoritative working branch:** `codex/carol-zero-based-hero-geometry-v005`

`main` remains the merged Phase 0 Full-3D foundation at `825febfde94f1998b55073cadcdf96c53d6b19e3`. Current Carol production work has advanced beyond `main`; do not use `main` alone to infer the latest character-production state.

The stable architecture remains Blender-authored Full 3D → GLB/glTF → PlayCanvas in the smartphone-first PWA. Task / Calendar foundation and the surrounding web stack remain in place. Old PixiJS / 2D / 2.5D character implementation material is archived and non-authoritative.

## Carol — current production phase

The current work is **Carol v005 A/B construction-method comparison**. It is not an approved hero model.

- A: `assets/grimo/production/carol/blender/carol-a-v005.blend`
  - zero-based full-volume attempt;
  - stronger volumetric construction;
  - unresolved fleece / face / ear geometry and missing motifs.
- B: `assets/grimo/production/carol/blender/carol-b-v005.blend`
  - explicit experiment deforming the recovered historical Carol while retaining its UVs/paint;
  - historical reuse is authorized for B only;
  - unresolved side stretching, intersections and lack of independent four legs.
- Recovered historical source: `assets/grimo/source/carol/historical/carol-15bfa8e-reference.glb`.
  - useful reference evidence;
  - not proven to be the exact binary previously accepted by the user.
- Current evidence packet: `docs/production/carol/evidence/hero-geometry-v005/README.md`.

**Agent visual recommendation: FAIL for both A and B as production hero geometry. Human construction-direction comparison is PENDING.** The immediate gate is to choose whether A, B, a later hybrid, or neither should define the next geometry iteration. Presence of saved `.blend` files does not imply approval.

No final hero geometry, rigging, production animation, topology lock, production export, PlayCanvas integration or `main` merge is authorized yet.

## Carol geometry authority

The concrete 3D geometry source of truth is:

`assets/grimo/source/carol/approved-3d/authority.json`

Highest geometry / volume / depth / proportion / part-placement authority is the six approved individual views:

1. `carol-front-ortho-transparent.png`
2. `carol-side-ortho-transparent.png`
3. `carol-back-ortho-transparent.png`
4. `carol-top-plan-transparent.png`
5. `carol-front-3q-left.png`
6. `carol-front-3q-right.png`

Side and both 3/4 views must be evaluated with Front. Do not flatten Carol's face from the Front reference alone. The 3/4 views are formal depth evidence for face, muzzle/cheek/forehead, eyes, ear roots, fleece/face ordering, body depth, limb fore/aft placement and total fleece volume.

`carol-Identity-canonical.png` remains the authority for identity, color, motifs, appeal and recognizable Carol-ness, but must not overwrite concrete 3D depth/thickness/volume/part placement established by those six production views. `carol-3d-production-canonical-sheet.png` is supplementary and yields to conflicting individual approved views for concrete geometry.

## Human Gate history

- Initial geometry interpretation: **CONDITIONAL PASS**.
- v001: **CONDITIONAL PASS** structurally; visual quality remained far below final standard and no rigging authorization followed.
- v003: explicit Human **FAIL**.
- v004: no Human approval recorded; supporting agent assessment remained FAIL for full visual convergence.
- v005 A/B: **PENDING Human comparison**; agent recommendation FAIL for both as final hero geometry.

## Presentation constraints already established

### Full Companion State

Carol is a low quadruped with the whole body visible. She may turn, walk, and show front, three-quarter, side and back orientations. Front is the primary presentation reference, not an orientation lock.

### Close Window-Lean State

A future interaction state requires Carol to approach, shift weight toward the rear supports, lift the forebody and place the forehooves near/on the lower viewport boundary. Face, upper fleece and forehooves become prominent. Geometry must therefore preserve rear support, independent forelimbs and deformable/compressible front fleece regions.

These are production constraints only; neither runtime state is implemented yet.

## Camera / framing state

Perspective remains the primary practical review candidate. Orthographic is structural comparison. Final production projection is unresolved. Character geometry must not be distorted to satisfy portrait occupancy measurements.

The Partner Eevee framing benchmark is now stored under `docs/grimo/knowledge/research/camera-framing/` and should inform later framing/camera decisions without overriding approved Carol geometry.

## Project Knowledge routing

- Durable current memory: `docs/grimo/knowledge/CURRENT_PROJECT_MEMORY.md`
- Knowledge authority index: `docs/grimo/knowledge/README.md`
- Product specs: `docs/grimo/knowledge/product/`
- Experience Motion Bible: `docs/grimo/knowledge/character-experience/`
- Generic 3D production + Carol Motion spec: `docs/grimo/knowledge/character-production/`
- Research evidence, Motion Masters and camera benchmark: `docs/grimo/knowledge/research/`
- Active Carol production contracts / gates / evidence: `docs/production/carol/`
- Canonical and approved reference assets: `assets/grimo/source/`

For a new agent/session, read `CURRENT_PROJECT_MEMORY.md` first, then the domain authority, then `CAROL_PRODUCTION_STATE.md` if the task concerns Carol production.

## Tooling / QA baseline

The existing reproducible Full-3D environment remains the baseline: Blender 5.2.1 LTS, GLB/glTF validation tooling, PlayCanvas tooling, Storybook/Playwright frontend QA and smartphone-oriented validation. These tools provide evidence; Human Gates remain the final acceptance authority for character quality.
