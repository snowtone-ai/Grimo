# Carol production state

## Current phase

After initial 3D geometry interpretation and Human Gate conditional pass. The
Partner Eevee camera/framing benchmark has been measured and Carol's initial
2D/screen-space framing contract is formalized. No Carol modeling has started.

## Human Gates

- Conditionally passed: initial geometry interpretation / Human Gate review
  (2026-09-16; G1–G5 accepted in principle).
- Pending: 3D camera calibration against the actual blockout, geometry
  measurement gaps, and later production gates.

## Unresolved issues

- The screen-space framing targets and ordinary safe envelope are resolved.
- Exact 3D projection, FOV, distance, camera height, target height, focal length,
  orthographic scale, world dimensions, and clipping planes remain intentionally
  unresolved until blockout calibration.
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
- `docs/grimo/knowledge/research/camera-framing/GRIMO_PARTNER_EEVEE_CAMERA_FRAMING_BENCHMARK.md`

## Routing

- Current completed handoff: GPT-6 Astra / Medium geometry interpretation,
  conditionally passed by Human Gate.
- Next planning route: ChatGPT Planner → GPT-5.6 Luna / Low.
- Subsequent Blender production: route through ChatGPT Planner → Luna by
  default; use Sol/Terra only when the documented local-iterative exception
  applies, after the geometry decision is complete.
- Multi-Agent/subagent usage: disabled for this Carol write-heavy workflow.

## Next exact task

Plan Carol's first Blender geometry blockout and simultaneously establish a
provisional front camera that reproduces the approved screen-space contract.
Calibrate only against the actual blockout; do not guess unsupported world-space
dimensions or camera values. Require evidence renders/captures suitable for the
next Human Gate. Blender modeling is the next authorized production problem,
but this state record itself authorizes no implementation.
