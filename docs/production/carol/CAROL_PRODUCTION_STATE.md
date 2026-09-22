# Carol production state

This file is the single mutable Carol execution truth.

## Current state — 2026-09-22

- Branch: `codex/carol-final-reconstruction-v009`.
- Asset: `assets/grimo/production/carol/blender/carol-v009.blend`.
- Retained geometry: Carol v009 candidate **v009-A2**, a bounded Phase A architecture attempt. It is **not an accepted static candidate**.
- Evidence: `docs/production/carol/evidence/reconstruction-v009/` and [Human comparison sheet](evidence/reconstruction-v009/human-comparison.png).
- Execution status: **BLOCKED_AT_V009_PHASE_A_ARCHITECTURE**.
- Human Geometry Gate: **PENDING HUMAN REVIEW; do not self-approve**.

Revision-14 evidence is preserved in `baseline-revision-14/` and revision-12 evidence in `baseline-revision-12/`. The four definitive Normal/Skin Front/Side sources remain FINAL/LOCKED, with unchanged hashes and registration. One neutral model serves Front and Side; no camera-specific geometry is used.

Revision 17 resolves the numerical torso-width ambiguity through two transverse station changes: X .575 half-width `.303→.3055 H`, X .730 `.305→.3075 H`, yielding `.598571 H` after subdivision. Torso/head and torso/limb surface intersection pair counts match revision 14. The hoof crown has three intended lower anterior lobes and two shallow valleys in one connected, grounded mesh per hoof. It is narrower in X (`.173107 H` evaluated depth versus `.188536 H` in revision 14) while retaining `.217385 H` evaluated Front width and `.111984 H` height. Front toe shading improves, but 3Q still reads as a broad tire; numerical pass does not override this visual failure. Revision 16's horn-like upper scallop was rejected.

v008 revision 17 is retained as the rejected predecessor and remains unchanged. Its Human Review FAIL is recorded for Side face / eye identity, head/chest transition, ear-root and true 3D ear volume, and hoof 3Q form.

v009-A2 replaces the competing `HEAD_CAGE` / `SHORT_NECK_SOCKET` / `TORSO_CAGE` exterior owners with one authored `CENTRAL_CHASSIS` mesh. The chassis is a single connected, all-quad, closed surface with named `HEAD`, `FACE`, `LOWER_CHEEK`, `FOREHEAD`, `NECK_TRANSITION`, `CHEST`, `ABDOMEN` and `RUMP` groups. It preserves the evaluated torso width `.598571 H`, support centers `.390 H` and `.920 H`, and locked Front eye projections `.137 × .149 H` at Y ±`.162 H`. The selected eye prototype is an embedded partial ellipsoid with `.029 H` central relief and six surrounding lid/socket loops.

The Phase A candidate is blocked because visual inspection still finds a hard lower-cheek shelf, an over-stretched under-chin/chest transition, Side/3Q eye identity failure, and evaluated non-adjacent face intersections. The ears and hooves are still temporary v008 modules; Phase B and Phase C were not started. Motion preflight was not run. No fleece, production rig, animation, GLB, PlayCanvas or runtime work was added.

Upper skull, lower-rear cheek shaping and oblique orbital housing were adjusted; locked Front eye dimensions/centers and packed pigment remain unchanged. Side forehead moves closer to the locked reference, yet Side eye/cheek identity still falls short. Ear-root perimeter broadened while the distal bowl remained unchanged; emergence is still abrupt. Head, socket and torso retain separate exterior surfaces; a disposable exact-union/smoothing test left the visible crease and was rejected. Future small head rotation retains a sliding risk. Tail geometry is unchanged from revision 14; Side reads round and partial Top occlusion alone is not a fault.

**Motion preflight was not run:** the static-selection prerequisite failed. Numerical neutral and virtual tail/rump contacts are diagnostics only, not motion clearance. No fleece, production rig, animation, GLB, PlayCanvas or runtime work was added.

Next handoff: **CHATGPT_PLANNER / HUMAN GEOMETRY REVIEW** of the [v009 blocked comparison sheet](evidence/reconstruction-v009/human-comparison.png), with the Phase A architecture blockers explicitly unresolved. Do not self-approve the Human Geometry Gate, start Phase B/C, or advance to fleece.
