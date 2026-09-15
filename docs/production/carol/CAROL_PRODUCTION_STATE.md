# Carol production state

## Current phase

After initial 3D geometry interpretation and Human Gate conditional pass. Carol
Blockout v001 now exists as a reproducible Blender source with provisional
front-camera candidates and evidence renders. This remains pending the next
Human Gate and is not production geometry authorization.

## Human Gates

- Conditionally passed: initial geometry interpretation / Human Gate review
  (2026-09-16; G1–G5 accepted in principle).
- Pending: Human Gate review of Blockout v001, projection choice, geometry
  measurement gaps, and later production gates.

## Unresolved issues

- The screen-space framing targets and ordinary safe envelope are resolved.
- Source: `assets/grimo/production/carol/blender/carol-blockout-v001.blend`
- Generator: `scripts/blender/build-carol-blockout.py` (Blender 5.2.1)
- Geometry status: Blockout v001 created; Human Gate pending. No rig, animation,
  final materials, GLB, or runtime integration was created.
- Camera candidates: Perspective and Orthographic front candidates are both
  present. The standard `Carol_Camera_front` alias points to Perspective for
  evidence only; production projection is not finalized.
- 16:9 benchmark calibration: both candidates are within the current preferred
  width/height/face-center ranges; see `evidence/blockout-v001/framing-metrics.json`.
- Portrait diagnostic: both candidates were rendered at 412x915. These results
  are diagnostic only and do not define runtime portrait framing.
- Next Human Gate decisions: preserve G1–G5 and canonical identity, approve the
  blockout silhouette/face/hoof read, select or defer projection, and decide how
  later portrait runtime framing should be authored.

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

- Completed implementation route: GPT-5.6 Luna / Low on
  `codex/carol-geometry-interpretation`.
- Next handoff: `HUMAN` for the Blockout v001 geometry and camera Human Gate.
- Multi-Agent/subagent usage: disabled for this Carol write-heavy workflow.

## Next exact task

Review `docs/production/carol/evidence/blockout-v001/` and decide whether the
canonical identity, G1–G5 geometry direction, and provisional Perspective /
Orthographic camera candidates are ready for the next production stage. Keep
production projection and portrait runtime framing unresolved until that review.
