# Carol production state

This file is the single mutable Carol execution truth.

## Current state — 2026-09-22

- Branch: `codex/carol-final-reconstruction-v008`.
- Asset: `assets/grimo/production/carol/blender/carol-v008.blend`.
- Retained geometry: Carol v008 revision **17**, best of three bounded attempts, **not an accepted static candidate**.
- Evidence: `docs/production/carol/evidence/reconstruction-v008/` and [Human review page](evidence/reconstruction-v008/human-review.html).
- Execution status: **BLOCKED_AT_V008_SKIN_IDENTITY_FIT**.
- Human Geometry Gate: **PENDING; do not submit for approval yet**.

Revision-14 evidence is preserved in `baseline-revision-14/` and revision-12 evidence in `baseline-revision-12/`. The four definitive Normal/Skin Front/Side sources remain FINAL/LOCKED, with unchanged hashes and registration. One neutral model serves Front and Side; no camera-specific geometry is used.

Revision 17 resolves the numerical torso-width ambiguity through two transverse station changes: X .575 half-width `.303→.3055 H`, X .730 `.305→.3075 H`, yielding `.598571 H` after subdivision. Torso/head and torso/limb surface intersection pair counts match revision 14. The hoof crown has three intended lower anterior lobes and two shallow valleys in one connected, grounded mesh per hoof. It is narrower in X (`.173107 H` evaluated depth versus `.188536 H` in revision 14) while retaining `.217385 H` evaluated Front width and `.111984 H` height. Front toe shading improves, but 3Q still reads as a broad tire; numerical pass does not override this visual failure. Revision 16's horn-like upper scallop was rejected.

Upper skull, lower-rear cheek shaping and oblique orbital housing were adjusted; locked Front eye dimensions/centers and packed pigment remain unchanged. Side forehead moves closer to the locked reference, yet Side eye/cheek identity still falls short. Ear-root perimeter broadened while the distal bowl remained unchanged; emergence is still abrupt. Head, socket and torso retain separate exterior surfaces; a disposable exact-union/smoothing test left the visible crease and was rejected. Future small head rotation retains a sliding risk. Tail geometry is unchanged from revision 14; Side reads round and partial Top occlusion alone is not a fault.

**Motion preflight was not run:** the static-selection prerequisite failed. Numerical neutral and virtual tail/rump contacts are diagnostics only, not motion clearance. No fleece, production rig, animation, GLB, PlayCanvas or runtime work was added.

Next handoff: **CHATGPT_PLANNER / HUMAN GEOMETRY REVIEW** of [the nine-row comparison sheet](evidence/reconstruction-v008/skin-human-fit-review.png) and remaining Side face, head/chest, ear-root and hoof blockers. Do not self-approve the Human Geometry Gate or advance to fleece.
