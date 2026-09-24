# Carol production state

This file is the mutable Carol execution routing source.

## Current state — 2026-09-25

- Branch: `codex/carol-face-ear-authority-match-v001`.
- Exact source: `656d6510b6ca81205cca1fced46d176f10d7aca7` / `codex/carol-face-ear-production-v003`.
- Final candidate commit: resolve `git log -1 --format=%H -- assets/grimo/production/carol/blender/carol-face-ear-authority-match-v001.blend`. The executor report records the exact local/remote SHA after commit.
- Candidate: `assets/grimo/production/carol/blender/carol-face-ear-authority-match-v001.blend`.
- Evidence: `docs/production/carol/evidence/face-ear-authority-match-v001/`; begin with `README.md` and `human-review.png`. Full resolution candidate renders are in `renders/`.
- State: `READY_FOR_HUMAN_FACE_EAR_AUTHORITY_MATCH_REVIEW`.
- Face: reconstructed cranial sections, cheeks, chin, muzzle, orbital surfaces, eyes, lids, nose and closed smile. Locked Front eye aperture and spacing retained; Side eye depth and sagittal contour substantially recovered.
- Ears: new closed shells measured from the approved Module Front / Top, with continuous recessed inner surfaces, rounded thickness and updated attachment. Source Ear v002 is no longer the final ear geometry. Legacy provisional shape keys were removed; a replacement rig is outside this task.
- Selected fixed-registration contour MAE: Skin Front 17.75 → 2.54 px; Skin Side 59.49 → 3.21 px; Normal Side 40.33 → 3.62 px. Ear silhouette IoU: Front 0.610 → 0.966; Top 0.730 → 0.961. These are fitting diagnostics, not perceptual approval or whole-image scores.
- Technical validation: saved asset reload, unchanged out-of-scope object snapshots and torso control vertices, packed eye pigment, authority hashes, finite/outward/manifold head and ears, zero nonadjacent triangle self-intersections. Details and evidence hashes: `validation.json`.
- Human visual acceptance: **PENDING**. Candidate is reviewable; it is not an approved geometry authority.
- Residuals: Front/Side illustrated cranium disagreement; wider 3Q eye projection and jaw/neck shading; uncalibrated Ear Module Side camera, inner rim/thickness and attached root differences. Strict orthographic and elevated Side evidence are both retained.
- Skin Side uses an explicitly recorded face-local registration for nose/eye/chin. This does not validate the inherited whole-body registration.
- Existing torso, limbs, hooves and tail preserved. Comparison studio lighting changed equally for source and candidate. No fleece, motion, rig, PlayCanvas or runtime completion claimed.
- Active authority: `assets/grimo/source/carol/approved-3d/authority.json`. Canonical identity, approved Normal Front / Side, supporting Skin Front / Side, geometry parameters and localized Ear Module remain unchanged. Prior hoof module is historical only.
- No candidate Carol geometry, Blender asset, GLB, animation, or runtime result is accepted as authority by this update.

## Next handoff

**HUMAN — Face / Ear authority-match review**: compare the fixed Front / Side overlays, then assess 3Q facial naturalness, ear interior/thickness and attachment. Route the perceptual decision into the next production step. The earlier F2-only / Ear architecture handoff is superseded by this reconstruction candidate.

Historical execution detail remains in Git history and Carol evidence directories.
