# Carol v009 — blocked Phase A architecture candidate

**BLOCKED_AT_V009_PHASE_A_ARCHITECTURE.** Candidate `v009-A2` is retained as a structural experiment, not as a passing static model. Human Geometry Gate remains **PENDING HUMAN REVIEW**. The evidence records both the successful architectural measurements and the visual failures; it does not claim approval.

Recovery from `01e19d27519d5731015d553cdae1acc572edf8c9` stopped after A4's structural failure. A3 and A4 used a local posterior head portal, rounded jaw closure, three interior neck rows, and a dorsal chest portal. Both were one-component, closed, all-quad surfaces with Euler `2`, but failed the disjoint-face intersection gates: A3 control/evaluated **114/393**, A4 **224/644**. A3 omitted frozen seam coordinates; A4 preserved them and all frozen objects. The local head/chest connection still self-intersects. No A5, visual renders, or deformation probes were run. The retained A2 blend and comparison images are unchanged.

`phase-a-attempt-3/a2-localization.json` records the single A2 localization: 363 lower-head, 42 transition, and 50 front upper-chest seam pairs. The last cluster lies at X=.57573–.58758, not in the rear torso. The two new attempt directories contain numerical rejection proofs only. `scripts/blender/build-carol-v009-phase-a-repair.py` reproduces either rejected attempt with `--attempt 3` or `--attempt 4`; failed gates never overwrite the retained asset. Its `--verify-retained` mode records the final A2 reload and recovery disposition.

The candidate was built from the verified v008 HEAD `2583c23949487b2cb15a243001858bb06f358d9b` and keeps the four FINAL / LOCKED reference images and registration unchanged. The competing v008 head, socket and torso exterior owners were replaced with one authored `CENTRAL_CHASSIS` mesh. The mesh has one connected closed all-quad surface, named `HEAD`, `FACE`, `LOWER_CHEEK`, `FOREHEAD`, `NECK_TRANSITION`, `CHEST`, `ABDOMEN` and `RUMP` groups, and no Boolean or remesh modifier. The eye prototype is an embedded partial ellipsoid with a `.029 H` central relief and six lid/socket loops.

The candidate still fails visual inspection: the lower cheek has a hard shelf, the under-chin transition stretches into the chest, Side / 3Q eye identity remains weak, and the evaluated central surface has non-adjacent face intersections. The ears and hooves are explicitly temporary v008 modules; their rejected root / Top rod and tire-like 3Q failures were not patched. Because the Phase A static prerequisite failed, no ear phase, hoof phase, integration correction, or motion preflight was run.

Evidence:

- `human-comparison.png` — compact locked / v008 / v009 / overlay sheet. Derived 3Q and Top rows are diagnostic only; no locked derived reference is invented.
- `measurements.json` — candidate controls, locked values, topology and module status.
- `validation.json` — reload, digest, reference, frozen-module, numerical and blocker checks.
- `phase-a-attempt-1/` and `phase-a-attempt-2/` — low-resolution Front, Side and 3Q proof renders plus measurements.
- `diagnostic-top.png` — derived Top diagnostic showing the unchanged temporary ear architecture.

The retained asset is `assets/grimo/production/carol/blender/carol-v009.blend`. No fleece, production rig, animation, final retopology, GLB export, PlayCanvas or runtime work was performed.

The Human Geometry Gate is intentionally still pending. Next handoff: **CHATGPT_PLANNER — blocked after A4; new geometry planning required**.
