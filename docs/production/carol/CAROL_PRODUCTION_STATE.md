# Carol production state

## Current phase — v006 structural correction candidate

2026-09-17: the explicit geometry request was executed through **pass 05 /
iteration 27**, with six-view evidence for iterations 20–27. Ear roots/bowls,
cheek/muzzle sections, independent legs/hooves, rump/tuft attachment and fleece
junctions were rebuilt. Camera calibration and approved images are unchanged.
**NOT ACCEPTED / geometry FAIL / Human Gate PENDING.** Single agent only.

The exact saved asset has 0 non-manifold edges and
0 non-finite vertices. Structural improvements do not
establish full six-view identity or the required torso-dominant 3Q hierarchy.
See [current evidence, measured tradeoffs and exact commands](evidence/reconstruction-v006/README.md).

Asset: `assets/grimo/production/carol/blender/carol-a-v006.blend`.
Review: http://127.0.0.1:3017/ while its server runs. Next handoff: **HUMAN**.

## Previous v005 comparison

Carol **v005 A/B method comparison** is available on
`codex/carol-zero-based-hero-geometry-v005`. The zero-based attempt is frozen as
`carol-a-v005.blend`. Under the user's subsequent explicit instruction, B reuses
and deforms the recovered historical mesh, preserving its UVs and paint, and is
saved as `carol-b-v005.blend`. This exception applies only to B.

**The approved hero geometry master is NOT complete.** Agent visual recommendation
is FAIL for both; Human comparison is pending. A retains unresolved fleece/face/
ear geometry and missing motifs. B retains side stretching, part intersections
and no independent four legs. Chrome comparison shows A, B and unmodified old
source with common cameras. The exact historical accepted binary is still not
established; the shown source is identified by commit and SHA-256.

- [v005 A/B packet and reopen instructions](evidence/hero-geometry-v005/README.md)
- A: `assets/grimo/production/carol/blender/carol-a-v005.blend`
- B: `assets/grimo/production/carol/blender/carol-b-v005.blend`
- Recovered source: `assets/grimo/source/carol/historical/carol-15bfa8e-reference.glb`
- Local page: `http://127.0.0.1:3016/` while its dedicated server runs.
- Next: **HUMAN**, construction-direction/source comparison only. No final
  geometry approval, automatic rigging, production export or runtime integration.

### Previous v004 submission

Carol Structural Blockout **v004** is submitted for **HUMAN Geometry Gate** on
`codex/carol-structural-blockout-v004`, based on latest pushed v003 `d2b5ddc`.
V003 received explicit Human FAIL. V004 Human review is PENDING; agent supporting
review is FAIL for full canonical-quality convergence after three iterations.
Face/eye/ear identity improved, but pillow-like side regions, repetitive valleys,
a lower band and simplified facial features remain. No main merge or automatic
rigging advancement.

### Current v004 artifacts

- Source: `assets/grimo/production/carol/blender/carol-blockout-v004.blend`
- Generator: `scripts/blender/build-carol-v004.py`; extracted design data:
  `scripts/blender/carol-v004-reference-data.json`
- Evidence, provenance and three-loop QA: [v004 review packet](evidence/blockout-v004/README.md)
- Historical restore source `15bfa8e` was inspected and captured before modeling;
  direct old-page captures are distinguished from reconstructed diagnostics.
- Saved fleece: one closed connected surface, 328,540 triangles, positive volume,
  finite coordinates and zero detected nonadjacent triangle intersections.
  Four supports/hooves, chassis and tuft match v003 by mesh hash/world matrix.
- Canonical/approved images and v003 assets/evidence remain unchanged. No rig,
  Actions, shape keys, production GLB export or runtime integration.

### Previous v003 artifacts

- Source: `assets/grimo/production/carol/blender/carol-blockout-v003.blend`
- Generator: `scripts/blender/build-carol-v003.py`
- Evidence and limits: [v003 review packet](evidence/blockout-v003/README.md)
- Saved surface: one closed connected component, 235,848 triangles, no detected
  nonadjacent triangle intersections. V002 protected structures match by hash
  and world matrix; canonical/v001/v002 files remain unchanged.
- Historical recovery found the actual Human acceptance statement, source
  excerpt and a predecessor screenshot; the exact accepted binary is unavailable.
  The accepted experience used shallow 2.5D relief. V003 preserves Full-3D depth.
- Remaining: broad smooth masses, heavy canopy/deep opening, coarse motif
  sampling, watercolor fidelity and later deformation. All need appropriate review.

## Human Gates

- Blockout v004: **PENDING**. Agent supporting review: **FAIL** for full visual
  convergence. See the current packet above.
- Blockout v003: **FAIL**, explicit user instruction, 2026-09-16.

- Initial geometry interpretation: **CONDITIONAL PASS**, 2026-09-16; G1–G5
  accepted in principle.
- Blockout v001: **CONDITIONAL PASS**, current explicit Human decision on
  2026-09-16. External/final visual quality was judged approximately **5/100**:
  visually very poor, but structurally not bad and worth refining. This did
  not approve visual fidelity or authorize rigging.
- Blockout v002: **PENDING**. Agent visual inspection and successful generation
  are supporting evidence, not a Human pass.

## Previous v002 artifacts (historical)

- Source: `assets/grimo/production/carol/blender/carol-blockout-v002.blend`
- Generator: `scripts/blender/build-carol-blockout.py`, Blender **5.2.1 LTS**
- Evidence: [Blockout v002 review packet](evidence/blockout-v002/README.md)
- History: v001 `.blend`, canonical PNG, approved packet and all v001 evidence
  remain unchanged. v001 generator is retained in starting commit
  `2bf64edea4043ac1dfda1f105ad975c6dedb4386`.
- Scope: neutral geometry and diagnostic materials only; no rig, animation,
  shape keys, production retopology, UV work, fur, GLB/glTF or runtime changes.

## Previous v002 structural result and uncertainty

- G1–G5 remain valid. Implementation was revised substantially: deeper
  concealed chassis, real fore/rear separation, one continuous cloud surface,
  shallow nested face, larger thick ears, small independent rear-centered tuft,
  and motifs attached to the actual surface.
- The face-opening contour and exact large/medium cloud correspondence to the
  posed canonical remain Human judgments. Crown/cheek transitions are still
  coarse blockout forms; fine appearance is outside this stage.
- Approved reference views disagree about hidden motif correspondence. One
  moon and five front-associated stars are provisional; no back motifs were
  invented to reconcile the plates.
- Full depth and tuft root are coherent proposals, not measured ground truth
  from the uncalibrated source sheets.
- A neutral structural study does not establish deformation ranges or prove
  the future Close pose. See the review packet's explicit feasibility limits.
- The requested 85–90/100 overall structural confidence is **not certified**;
  do not convert file generation or local checks into that acceptance claim.

## Human presentation architecture — 2026-09-16

### Full Companion State

Whole body visible in a normal low quadruped posture. Carol may turn left or
right, show three-quarter or back views, rotate and walk. The front-facing
camera is the presentation reference; **Carol's orientation is not locked**.
Camera orbit is not required.

### Close Window-Lean State

Future interaction: Carol approaches, shifts weight toward the rear supports,
raises the forebody, and places the forehooves near/on the bottom boundary of
the 3D interaction viewport, like leaning on a window sill. Face, upper fleece
and forehooves become prominent. The neutral blockout is not posed this way.

Both states are conceptual architecture only. Neither runtime state nor its
motion was implemented. Rear support, independent forelimbs, front opening
and compressible fleece regions must be retained for later development.

## Camera boundary

Perspective remains the primary practical review candidate; Orthographic is
the structural comparison. Production projection is unresolved. The v002
1400x1190 views are geometry evidence, not smartphone framing proposals.
The earlier 16:9 benchmark calibration and 412x915 clipping diagnostic remain
historical evidence. Portrait must be framed separately later; geometry must
not be distorted to hit occupancy numbers.

## Routing

- Current task: explicit Astra visual/spatial refinement, no subagents.
- Next handoff: **HUMAN**, using `prompt.md` and the v004 evidence packet.
- Review identity, silhouette, cloud hierarchy, embedding, ears, low chassis,
  supports, rear/tuft, motifs, off-axis consistency and Full/Close feasibility.
- Rigging, topology lock, animation, export and runtime work require separate
  authorization after the Human decision.
