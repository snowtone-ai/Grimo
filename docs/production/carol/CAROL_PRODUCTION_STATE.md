# Carol production state

This file is the mutable Carol execution routing source.

## Current state — 2026-09-25

- Branch: `codex/carol-face-ear-production-v003`.
- Exact source: `origin/codex/setup-codegraph-mcp` / `880b35506c0b085fdbb4081c1de6c3f9bdc4e58a`.
- Final candidate commit: resolve `git log -1 --format=%H -- assets/grimo/production/carol/blender/carol-face-ear-production-v003.blend`. The executor report records the exact local/remote SHA after commit; a tracked record cannot embed its own commit hash without changing it.
- Candidate: `assets/grimo/production/carol/blender/carol-face-ear-production-v003.blend` — **Face F2 + exact source Ear v002**.
- Evidence: `docs/production/carol/evidence/face-ear-production-v003/`; begin with `human-review.png` and `README.md`.
- State: `READY_FOR_HUMAN_FACE_EAR_REVIEW`.
- Face executor visual precheck: `PASS`. F2 selected: two sagittal FACE controls, max 0.020 H negative-X displacement; surface-owned nose/mouth/philtrum. F1 rejected for newly covered eye/lid points. F2 newly covers zero points. Projection is only partially recovered; Human review required.
- Ear executor visual precheck: `FAIL`. `EAR_V003_NOT_PROMOTED`; E1/E2 exhausted. Side / Top / cup tradeoff unresolved. Final ears remain source v002. Further local repair stopped pending architecture review.
- Technical validation: `PASS` for F2 + retained ears: reload, unchanged topology, 37 frozen objects, eye/lid digests, surface ownership, intersections and representative bends.
- Skin Side inherited-registration probe: `PROBE_INVALID`; current authority face landmarks do not align with inherited registration. No reference/camera changes.
- Existing non-final fleece clearance remains unresolved; diagnostic fleece is not in the candidate.
- Active authority: `assets/grimo/source/carol/approved-3d/authority.json`.
- Pre-existing manifest hash drift repaired in one field from canonical Git LF bytes. No authority content, order, role, version, approval status or image hash changed.
- Accepted visual references: Carol canonical identity and approved Normal Front / Normal Side.
- Supporting underbody references: current Skin Front / Skin Side and `CAROL_GEOMETRY_PARAMETERS.md`.
- Localized motion-critical reference: current approved Ear Module sheet.
- The prior generated hoof module sheet is historical only. Normal Front / Normal Side remain visible hoof authority.
- No candidate Carol geometry, Blender asset, GLB, animation, or runtime result is accepted as authority by this update.

## Next handoff

**HUMAN — Face F2 review**, then **ChatGPT Planner — Ear architecture review / inherited Skin registration review**.

Historical execution detail remains in Git history and Carol evidence directories.
