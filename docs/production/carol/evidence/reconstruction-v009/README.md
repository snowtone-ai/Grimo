# Carol v009 — blocked Phase A architecture candidate

**BLOCKED_AT_V009_PHASE_A_ARCHITECTURE.** Candidate `v009-A2` is retained as a structural experiment, not as a passing static model. Human Geometry Gate remains **PENDING HUMAN REVIEW**. The evidence records both the successful architectural measurements and the visual failures; it does not claim approval.

The candidate was built from the verified v008 HEAD `2583c23949487b2cb15a243001858bb06f358d9b` and keeps the four FINAL / LOCKED reference images and registration unchanged. The competing v008 head, socket and torso exterior owners were replaced with one authored `CENTRAL_CHASSIS` mesh. The mesh has one connected closed all-quad surface, named `HEAD`, `FACE`, `LOWER_CHEEK`, `FOREHEAD`, `NECK_TRANSITION`, `CHEST`, `ABDOMEN` and `RUMP` groups, and no Boolean or remesh modifier. The eye prototype is an embedded partial ellipsoid with a `.029 H` central relief and six lid/socket loops.

The candidate still fails visual inspection: the lower cheek has a hard shelf, the under-chin transition stretches into the chest, Side / 3Q eye identity remains weak, and the evaluated central surface has non-adjacent face intersections. The ears and hooves are explicitly temporary v008 modules; their rejected root / Top rod and tire-like 3Q failures were not patched. Because the Phase A static prerequisite failed, no ear phase, hoof phase, integration correction, or motion preflight was run.

Evidence:

- `human-comparison.png` — compact locked / v008 / v009 / overlay sheet. Derived 3Q and Top rows are diagnostic only; no locked derived reference is invented.
- `measurements.json` — candidate controls, locked values, topology and module status.
- `validation.json` — reload, digest, reference, frozen-module, numerical and blocker checks.
- `phase-a-attempt-1/` and `phase-a-attempt-2/` — low-resolution Front, Side and 3Q proof renders plus measurements.
- `diagnostic-top.png` — derived Top diagnostic showing the unchanged temporary ear architecture.

The retained asset is `assets/grimo/production/carol/blender/carol-v009.blend`. No fleece, production rig, animation, final retopology, GLB export, PlayCanvas or runtime work was performed.

The Human Geometry Gate is intentionally still pending. Next handoff: **CHATGPT_PLANNER / HUMAN GEOMETRY REVIEW**.
