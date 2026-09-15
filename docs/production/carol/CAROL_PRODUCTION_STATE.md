# Carol production state

## Current phase

Carol Structural Blockout v002 is complete as a volume study and **awaiting a
new Human Gate**. It is not approved production geometry. No automatic route
to rigging follows this handoff.

## Human Gates

- Initial geometry interpretation: **CONDITIONAL PASS**, 2026-09-16; G1–G5
  accepted in principle.
- Blockout v001: **CONDITIONAL PASS**, current explicit Human decision on
  2026-09-16. External/final visual quality was judged approximately **5/100**:
  visually very poor, but structurally not bad and worth refining. This did
  not approve visual fidelity or authorize rigging.
- Blockout v002: **PENDING**. Agent visual inspection and successful generation
  are supporting evidence, not a Human pass.

## Current artifacts

- Source: `assets/grimo/production/carol/blender/carol-blockout-v002.blend`
- Generator: `scripts/blender/build-carol-blockout.py`, Blender **5.2.1 LTS**
- Evidence: [Blockout v002 review packet](evidence/blockout-v002/README.md)
- History: v001 `.blend`, canonical PNG, approved packet and all v001 evidence
  remain unchanged. v001 generator is retained in starting commit
  `2bf64edea4043ac1dfda1f105ad975c6dedb4386`.
- Scope: neutral geometry and diagnostic materials only; no rig, animation,
  shape keys, production retopology, UV work, fur, GLB/glTF or runtime changes.

## Structural result and remaining uncertainty

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
- Next handoff: **HUMAN**, using `prompt.md` and the v002 evidence packet.
- Review identity, silhouette, cloud hierarchy, embedding, ears, low chassis,
  supports, rear/tuft, motifs, off-axis consistency and Full/Close feasibility.
- Rigging, topology lock, animation, export and runtime work require separate
  authorization after the Human decision.
