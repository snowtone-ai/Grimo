# Handoff

Target: HUMAN  
Repository: `snowtone-ai/Grimo`  
Branch: `codex/carol-zero-based-hero-geometry-v005`  
Stop: Carol v005 **A/B construction-direction Human Gate**

## Read first

1. `docs/grimo/knowledge/CURRENT_PROJECT_MEMORY.md`
2. `docs/production/carol/CAROL_PRODUCTION_STATE.md`
3. `docs/production/carol/evidence/hero-geometry-v005/README.md`
4. `assets/grimo/source/carol/approved-3d/authority.json`

## Current comparison

- **A:** `assets/grimo/production/carol/blender/carol-a-v005.blend`
  - zero-based full-volume construction;
  - stronger 3D volume;
  - unresolved fleece / face / ear geometry and missing motifs.
- **B:** `assets/grimo/production/carol/blender/carol-b-v005.blend`
  - deforms the recovered historical Carol while preserving retained topology / UVs / paint;
  - this historical-reuse exception applies to B only;
  - unresolved side stretching, intersections and missing independent four legs.
- **Historical source:** `assets/grimo/source/carol/historical/carol-15bfa8e-reference.glb`
  - useful comparison source;
  - not established as the exact previously accepted binary.

**Agent recommendation: FAIL for both A and B as final production hero geometry. Human comparison is pending.**

## Review evidence

Start from:

- `docs/production/carol/evidence/hero-geometry-v005/ab-five-view-comparison.jpg`
- `docs/production/carol/evidence/hero-geometry-v005/chrome-ab-front.png`
- `docs/production/carol/evidence/hero-geometry-v005/01-reference-board.png`
- `docs/production/carol/evidence/hero-geometry-v005/visual-qa.md`
- final A iteration under `iterations/parts-03/`
- final B iteration under `iterations/b-04/`

The review page compares A, B and the unmodified recovered source with shared cameras.

## Geometry authority

Concrete Carol geometry / volume / depth / proportion / part placement is governed by the six approved individual views recorded in `authority.json`:

- Front
- Side
- Back
- Top
- Left 3/4
- Right 3/4

Side and both 3/4 views must be read with Front. Do **not** flatten the face from Front alone. `carol-Identity-canonical.png` remains the identity/color/motif/appeal authority but does not overwrite concrete depth/thickness/volume established by the approved production views.

## Human decision to record

This gate is **not** “is Carol finished?” Decide the construction direction for the next hero-geometry iteration:

- A survives,
- B survives,
- use a hybrid based on clearly named strengths of A/B,
- or reject both.

Review the raw recovered source as well as A and B before deciding.

Record the Human decision with specific views/regions and the chosen next construction direction.

Do not claim hero completion and do not automatically advance to rigging, topology lock, production animation, final UV/material/shader lock, production GLB export, PlayCanvas runtime integration, or merge to `main` without a separate Human authorization.
