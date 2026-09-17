# Handoff — Carol v006 geometry escalation checkpoint

Target: CODEX_TERRA_HIGH
Repository: snowtone-ai/Grimo
Branch: codex/carol-zero-based-hero-geometry-v005
Status: GEOMETRY FAIL; stalled after two consecutive 3Q checkpoints; Human Gate PENDING.

The user requested a clean interruption and push. Do not restart modeling without
another instruction. **Use one agent only; no subagents.**

Read `docs/production/carol/evidence/reconstruction-v006/README.md` first.
It contains exact reconstruction/review commands, current metrics, known failures,
reference inconsistencies and evidence paths. The current Blender asset is
`assets/grimo/production/carol/blender/carol-a-v006.blend` (pass 5, iteration 11 clean restore).

A: macro silhouette direction only. B: retired, do not use. Old GLB: look only,
not geometry authority. Approved six individual images remain geometry authority.
No rigging, GLB export, runtime integration or final production acceptance.

Iteration 10 tested a coherent shared head-depth increase (anterior face depth
1.05 -> 1.19). It degraded Side IoU from 0.936985 to 0.921879 and left 3Q
effectively unchanged (Left 0.826143 -> 0.826158; Right 0.867420 -> 0.867548).
It was rejected; iteration 11 restores the prior geometry exactly.

Exact escalation: resolve the shared 3Q silhouette/identity failure without
regressing the fixed orthographic cameras: 3Q Left 0.826143 (target 0.92), 3Q
Right 0.867420 (target 0.92). Reconcile approved-plate correspondence, then
address shared fleece/body mass, face/ear depth, and fore/aft leg ordering.
Do not hide failures with materials or view-dependent shape.

Local review: http://127.0.0.1:3017/ . Chrome opens maximized at Front. The old look
column is a fixed historical front screenshot and explicitly labeled as such.
