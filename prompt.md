# Handoff

Target: CHATGPT_PLANNER
Repository: snowtone-ai/Grimo
Branch: codex/carol-geometry-interpretation

## Mission

Read the latest pushed GitHub state of this branch. Do not modify the
repository. Complete the reasoning and output one complete GPT-5.6 Luna / Low
execution prompt for the next deterministic repository task.

## Task

Plan the next repository task: measure and formalize Carol's front-facing
companion camera/framing contract from the approved benchmark and relevant
repository sources. The Human Gate geometry result is **CONDITIONAL PASS**;
G1–G5 are accepted in principle, but numeric camera/framing values and the
listed geometry measurement gaps remain unresolved. Do not start modeling,
rigging, animation, GLB export, or PlayCanvas/runtime work.

## Required repository inputs

- `docs/production/carol/CAROL_GEOMETRY_DECISION.md`
- `docs/production/carol/CAROL_PRODUCTION_STATE.md`
- `docs/production/carol/CAROL_CAMERA_CONTRACT.md`
- `docs/production/carol/CAROL_MODELING_CONTRACT.md`
- `docs/grimo/knowledge/character-production/carol/CAROL_MVP_MOTION_SPEC.md`
- `docs/grimo/knowledge/character-production/GRIMO_3D_BLENDER_PRODUCTION_BIBLE.md`
- Relevant benchmark/reference README files listed in production state

## Planning requirements

Use the latest pushed repository state only and do not re-ask already known
project facts. Resolve the exact benchmark/reference files and define a lean,
evidence-based Luna task for measuring and recording the front-facing companion
camera/framing contract, including source/frame, landmarks, screen occupancy,
projection assumptions, units, method, and uncertainty. Preserve the existing
Human Gate conditions and camera-value holds. The resulting Luna prompt must be
concrete enough that Luna need not redesign the task, must include targeted
validation, and must finish with commit and push. It must not authorize
modeling/rigging/animation or runtime work.
