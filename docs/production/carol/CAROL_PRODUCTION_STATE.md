# Carol production state

## Current phase

After initial 3D geometry interpretation and Human Gate conditional pass. No
Carol modeling has started.

## Human Gates

- Conditionally passed: initial geometry interpretation / Human Gate review
  (2026-09-16; G1–G5 accepted in principle).
- Pending: camera/framing measurements and specification; geometry measurement
  gaps and later production gates remain unresolved.

## Unresolved issues

- Numeric camera FOV, distance, and height remain unmeasured.
- Numeric camera/framing values remain unresolved, including projection, FOV,
  distance, height, target height, and subject screen occupancy.
- Blender modeling has not started. The conditional pass in
  `CAROL_GEOMETRY_DECISION.md` does not authorize blockout or other production.

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

- Current completed handoff: GPT-6 Astra / Medium geometry interpretation,
  conditionally passed by Human Gate.
- Next planning route: ChatGPT Planner → GPT-5.6 Luna / Low.
- Subsequent Blender production: route through ChatGPT Planner → Luna by
  default; use Sol/Terra only when the documented local-iterative exception
  applies, after the geometry decision is complete.
- Multi-Agent/subagent usage: disabled for this Carol write-heavy workflow.

## Next exact task

Define and measure the front-facing Carol companion camera/framing contract from
the approved benchmark and relevant repository sources. Record the benchmark
source/frame, landmark definitions, screen-occupancy measurements, projection
assumptions, units, method, and uncertainty while preserving all unresolved
gaps. This task must still forbid starting modeling, rigging, animation, GLB
export, or PlayCanvas/runtime work.
