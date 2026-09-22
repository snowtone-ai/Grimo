# Carol production state

This is the single mutable source of detailed current Carol execution truth.
Do not duplicate candidate, gate, evidence, blocker or next-step facts in
durable memory, maps, contracts, prompts or skills.

## Current state — 2026-09-22

- Candidate: **Carol v008 — selected revision 9**.
- Asset: `assets/grimo/production/carol/blender/carol-v008.blend`.
- Generator: `scripts/blender/build-carol-v008.py`.
- Evidence: `docs/production/carol/evidence/reconstruction-v008/README.md`.
- Branch: `codex/carol-final-reconstruction-v008`.
- Execution status: **BLOCKED_AT_V008_SKIN_FINAL_FIT**.
- Human Geometry Gate: **PENDING; not ready for Human submission**.

This final-fit continuation began from clean pushed
`0fb3d38a67763eb87c780c848a8cbbefdf532942`. Three bounded geometry
attempts, revisions **7, 8 and 9**, were rendered and compared in both locked
Skin views. Revision 9 is selected for a small improvement to the upper ear
inset. Revision 7's changed perimeter made the Side root pointier. Revision 8
joined head and chest into one simple ring bridge, but created a hard triangular
underside and degraded the Front/Side read. Both were rejected. No fourth
attempt ran.

## Selected geometry and diagnostic result

- Only `EAR_L` and `EAR_R` differ from revision 5. Their distal perimeters,
  rounded bowls, topology and ROOT/MID/TIP groups remain. A buried back-shell
  saddle widens the internal root support; the upper inner lip rises and curves
  more gradually. The visible Side root remains too narrow.
- `HEAD_CAGE`, `SHORT_NECK_SOCKET` and `TORSO_CAGE` remain separate closed
  surfaces. The head/chest exterior transition still lacks coherent surface
  ownership and a demonstrated soft articulation strategy. Revision 8 shows
  that a direct chin-to-torso ring bridge alone does not solve this junction.
- Front cheek/cranium remains somewhat square. The head, central face, eyes,
  nose, mouth, limbs, hooves, tail, debug pivots and all other renderable objects
  have unchanged geometry records from revision 5.
- Support centers remain FORE X=.390, Y=+/-.145 H and HIND X=.920,
  Y=+/-.245 H. Four locked references, hashes and registration are unchanged.
  One neutral geometry serves Front and Side.

The selected asset was rebuilt and reloaded at the exact neutral digest
`a0e09b0deb26d349445cbb2ede3380f2f8d4133b1b7968e773a65d81f6ea270e`.
Disposable head yaw +/-8 degrees, pitch +/-6 degrees, roll +/-5 degrees and
right-ear sweep +/-8 degrees were rendered in both views. The ear bowl remains
readable, with no obvious small-sweep detachment or collapse. The rigid
head/chest probes still show surface sliding. All channels returned to the
exact neutral digest; no production pose, rig or animation was saved. These
probes are **not motion, deformation or Human approval**.

## Remaining blockers

- Ear emergence remains narrow/abrupt in Side. The upper fold is milder but
  still more graphic than the locked reference. A truly broad, soft root may
  require a local saddle and rim topology that blends into the head while
  retaining independent ear motion.
- Head/chest still presents intersecting exterior shells; neutral overlap and
  rigid clearance are insufficient for soft articulation. A local boundary
  with matched tangents and deformation ownership is needed. The rejected
  simple ring bridge is evidence against that specific construction, not
  against continuous skin in general.
- Front cheek/cranium is square relative to the reference. Proximal support
  silhouettes and Front hoof overlap also differ. Proximal fitting was not
  reached because ear and head/chest remained blocked; support centers stay
  frozen.
- The slight registered Front/Side skull-height discrepancy remains. Do not
  hide it with camera-dependent or view-specific geometry.

Fleece, Normal, derived production views, final retopology, production
rigging/animation, lookdev, GLB and runtime work remain unstarted.

## Authority and next allowed step

The four FINAL/LOCKED references (`carol_front.png`, `carol_side.png`,
`carol_skin_front.png`, `carol_skin_side.png`) and
`CAROL_GEOMETRY_PARAMETERS.md` govern one model. Identity canonical is
secondary support. Historical v007 Human FAIL remains unchanged.

**CHATGPT_PLANNER:** audit the pushed revision-5-to-9 packet and the rejected
ring bridge. Scope a new, bounded local exterior ownership design for the
head/chest junction and a genuine ear-root emergence topology; preserve the
distal bowl and central face. Reassess proximal silhouettes only after both
primary views improve with frozen support centers.

Do not proceed to fleece while Skin is blocked or to later production phases
without the required Human Geometry Gate. Historical chronology belongs in
`CAROL_REVIEW_LOG.md`, not this mutable state file.
