# Carol production state

This file is the single mutable Carol execution truth.

## Current state — 2026-09-22

- Branch: `codex/carol-final-reconstruction-v008`.
- Candidate: Carol v008 revision **14**, retained as the best bounded local fit, **not an accepted static candidate**.
- Asset: `assets/grimo/production/carol/blender/carol-v008.blend`.
- Evidence: `docs/production/carol/evidence/reconstruction-v008/`.
- Execution status: **BLOCKED_AT_V008_SKIN_IDENTITY_FIT**.
- Human Geometry Gate: **PENDING; do not submit for approval yet**.

The exact pushed revision-12 evidence is preserved in `baseline-revision-12/`. The new Human findings were excess torso mass, a slightly low mouth, narrow lower jaw and angular cheeks, tire-like hooves, and an elongated Skin tail. The Human locked **exactly three rounded toe lobes and two shallow clefts per single continuous hoof**; this narrow decision is in `CAROL_GEOMETRY_PARAMETERS.md`.

Revision 13 applied the specified torso stations, lower-cheek transverse widths, mouth curve, three-lobe hoof profile and near-round tail. The torso became visibly slimmer without contact loss: head/torso intersection ratio .990, fore/torso 1.049 and hind/torso 1.047 versus revision 12. The two central torso control thicknesses are .325 and .318 H; control maximum width is .610 H. Catmull-Clark evaluated maximum width is .59404 H, just under the stated .595 H guard; this discrepancy is disclosed, not treated as a visual pass. Face and mouth improved subtly; the tail is rounder in Side. Revision 13's shallow hoof clefts disappeared under smoothing.

Revision 14 changed **only the hoof cleft owner**: 48 to 96 ring samples, maximum anterior retraction .009 to .011 H and optional notch .0018 to .0025 H. It improves the technical groove but the Front and 3Q renders still read as a broad brown tire. No further shape attempt is authorized in this bounded task. The primary [Human review sheet](evidence/reconstruction-v008/skin-human-fit-review.png) shows locked, revision 12, revision 14 and 50% overlay in seven rows. The original Side face mismatch, head/chest exterior seam and ear-root emergence remain. The tail reads rounder from Side but is partly swallowed in Top; it needs Human/Planner review before claiming final appeal.

The revision-12 conformal eye architecture, width .137 H, height .149 H, Y centers +/-.162 H, Z .418 H, .014 H maximum relief and packed pigment remain. Lower-cheek subdivision causes minute conformal eye/eyelid vertex changes, but no eye control, pigment, lens system or orbital design was changed. Nose, ears, short socket and all four limbs are geometrically frozen. Support centers remain FORE (.390,+/-.145) and HIND (.920,+/-.245). Camera matrices, registration and four source hashes remain fixed. One neutral mesh serves Front/Side. No fleece, production rig/animation, GLB, Boolean/remesh or runtime work was added.

**Motion preflight was not run:** the specified order requires a valid static candidate first. The revised tail has positive virtual torso surface intersections in neutral, +/-20 vertical and +/-7 lateral; this is only a numerical contact diagnostic, not a visual motion pass. Earlier revision-12 motion sheets and report are archived in `baseline-revision-12/`. Cheek and forehead touch, intermediate blink, target-convergent gaze, real COM, head/chest skin ownership, ear articulation and fleece deformation remain unvalidated.

Next handoff: **CHATGPT_PLANNER**. Review the bounded static failure and decide a new hoof/torso guard resolution from the pushed sheet and measurements. Do not self-approve the Human Geometry Gate or advance to fleece.
