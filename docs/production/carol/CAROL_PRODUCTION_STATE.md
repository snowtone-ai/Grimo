# Carol production state

## Current phase

Production infrastructure bootstrap, immediately before initial 3D geometry interpretation. No Carol modeling has started.

## Human Gates

- Passed: none recorded in the repository.
- Pending: initial geometry interpretation, then Human Gate review.

## Unresolved issues

- Numeric camera FOV, distance, and height remain unmeasured.
- Initial geometry interpretation and the Human Gate remain pending; `CAROL_GEOMETRY_DECISION.md` must not be treated as complete.

## Authoritative inputs

- `assets/grimo/source/carol/carol-Identity-canonical.png`
- `assets/grimo/source/carol/approved-3d/`
- `docs/grimo/knowledge/character-production/carol/CAROL_MVP_MOTION_SPEC.md`
- `docs/grimo/knowledge/research/motion-masters/PIKACHU_MOTION_MASTER_INVENTORY.md`
- `docs/grimo/knowledge/research/motion-masters/EEVEE_MOTION_MASTER_INVENTORY.md`
- `docs/product/README.md`
- `docs/setup/3D_TOOLCHAIN.md`
- `docs/grimo/references/README.md`
- `docs/grimo/references/pokemon-lets-go.md`
- `docs/grimo/references/rights-and-provenance.md`
- `docs/production/carol/CAROL_CAMERA_CONTRACT.md`
- `docs/production/carol/CAROL_MODELING_CONTRACT.md`

## Routing

- Current bootstrap: GPT-5.6 Luna / Low.
- Next interpretation: GPT-6 Astra / Medium.
- Subsequent Blender production: route through ChatGPT Planner → Luna by
  default; use Sol/Terra only when the documented local-iterative exception
  applies, after the geometry decision is complete.
- Multi-Agent/subagent usage: disabled for this Carol write-heavy workflow.

## Next exact task

The next session must use GPT-6 Astra / Medium to review the canonical image, every approved 3D reference, the contracts, and the Carol motion constraints; record an evidence-based initial geometry interpretation in `CAROL_GEOMETRY_DECISION.md`. Missing measurements and conflicts must be reported explicitly. Do not begin Blender blockout, rigging, animation, or GLB production in that session.
