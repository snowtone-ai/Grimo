# Next-session handoff — Carol geometry interpretation

## Mission

Use **GPT-6 Astra / Medium** to perform Carol's initial 3D geometry interpretation and complete:

`docs/production/carol/CAROL_GEOMETRY_DECISION.md`

This is an evidence-based interpretation task. Geometry remains undecided until that decision record is completed and passes the Human Gate.

## Required inputs

- `assets/grimo/source/carol/carol-Identity-canonical.png` — visible identity authority
- `assets/grimo/source/carol/approved-3d/` — approved Carol 3D reference packet and `authority.json`
- `docs/production/carol/CAROL_CAMERA_CONTRACT.md`
- `docs/production/carol/CAROL_MODELING_CONTRACT.md`
- `docs/grimo/knowledge/character-production/carol/CAROL_MVP_MOTION_SPEC.md`
- `docs/grimo/knowledge/character-production/GRIMO_3D_BLENDER_PRODUCTION_BIBLE.md`
- `docs/grimo/knowledge/character-experience/GRIMO_EXPERIENCE_MOTION_BIBLE.md`

Consult the relevant Product, Data, and Research authorities as needed, including the formal Pikachu and Eevee Motion Masters and partner video analyses. Keep the authority order explicit: visible identity wins over 3D references where they conflict; Motion Masters are evidence, not motions to copy.

## Required output

- `docs/production/carol/CAROL_GEOMETRY_DECISION.md`

Record observations, confidence, unresolved conflicts, and missing measurements. Do not claim geometry interpretation is complete until the decision record contains evidence and the Human Gate is recorded.

## Explicit prohibitions

- Do not start a Blender blockout.
- Do not create a rig or animation.
- Do not generate a GLB production asset or begin PlayCanvas Carol implementation.
- Do not fill gaps with generic sheep anatomy.
- Do not guess unmeasured FOV, camera distance, camera height, or other numeric camera values.
- Do not prioritize 3D references over the canonical identity image.
