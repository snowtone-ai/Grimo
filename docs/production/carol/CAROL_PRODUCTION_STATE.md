# Carol production state

## Current phase

Production infrastructure bootstrap, immediately before initial 3D geometry interpretation. No Carol modeling has started.

## Human Gates

- Passed: none recorded in the repository.
- Pending: initial geometry interpretation, then Human Gate review.

## Unresolved issues

- `CAROL_MVP_MOTION_SPEC.md` is referenced by the bootstrap instruction but is not present in the repository.
- No approved Carol 3D production reference files are present under `assets/grimo/source/carol/approved-3d/`.
- Numeric camera FOV, distance, and height remain unmeasured.

## Authoritative inputs

- `assets/grimo/source/carol/carol-Identity-canonical.png`
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
- Subsequent Blender production: Sol / Medium, after the geometry decision is complete.
- Multi-Agent/subagent usage: disabled for this Carol write-heavy workflow.

## Next exact task

The next session must review the canonical image, every available approved 3D reference, and the contracts; record an evidence-based initial geometry interpretation in `CAROL_GEOMETRY_DECISION.md`. Missing references and conflicts must be reported explicitly.
