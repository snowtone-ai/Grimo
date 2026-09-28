# Carol Normal/Fleece v004: Regional Construction Checkpoint

Status: **NORMAL_FLEECE_V004_IN_PROGRESS**. Not a completed Fleece phase and not
a Human-review candidate. Technical checks do not constitute visual acceptance.

## Current Direction

The latest Human instruction makes the old Carol's perceived appearance,
softness and material quality the target, not a compulsory production recipe.
Different regions can use different construction and attachment techniques.
The initial `prompt.md` is not an immutable method contract.

Current Front/Side remain the visual authority. The accepted Skin source is
unchanged and supplies the inner support and contact queries. The historical
`snowtone-ai/grimoire` commit
`15bfa8e4c3a8ba24c246fe806bd125b307d8f076` is a method/quality donor, never a
replacement image authority.

## Active Construction

- Torso: a joint Front/Side guide, inset in all three axes, supporting closed
  rounded lock volumes. The guide uses the adapted fifth-power Gaussian lock
  field. It is an internal construction surface, not the intended final look.
- Face fringe, cheeks and chin: separate rounded locks with regional depth and
  Skin contact. The forehead no longer relies on the old minimum-depth clamp;
  the chin locks sit ahead of the torso core rather than disappearing into it.
- Ears: retained candidate ear geometry, authority-derived ear pigment, and
  whole neighboring locks placed behind/inboard of the ear leaves. The failed
  per-vertex ear cavity cut is not active.
- Tail: a small independent three-lock volume with its own owner.
- Pigment: local source-color medians, fixed world-light direction, shallow
  colored occlusion and object-attached three-dimensional grain. This active
  variant does not project whole Front/Side shading patterns onto the fleece.
  Camera changes do not alter geometry or material assignments.
- Hoof rear caps use spatial brown pigment to avoid stretched image stripes.
  Ornament placement removes the old mounting tilt before fitting the new one.
  Their glints now share the same regional owner. Mounting gaps remain open.

The initial literal radial donor port and subsequent projection comparisons
remain explicit diagnostic code paths. They are not the active checkpoint.
Do not describe the current volumetric union as the unchanged historical method.

## Evidence

`iterations/33/` contains the current same-asset multi-angle diagnostic renders,
the render manifest, Front/Side comparisons, silhouette measurements, a spatial
board and a 160-pixel Front comparison. `iterations/33-clay/` is a separate
geometry-only diagnostic of the same saved asset. Neither is acceptance evidence.

`asset-audit.json` records the actual reopened asset and generator hashes.
`tuft-inventory.json` contains 84 measured Front units and 38 Side units; these
are source measurements, not an assertion that every final tuft matches.
`body-locks.json` and `face-locks.json` record the constructed lock positions.
Opposite-side and rear extensions are inferred diagnostics, not new authority.

Earlier experiments are preserved locally under
`artifacts/carol-fleece-v004/iteration-history/`; they are not active candidates.
The rejected iteration 30 made ornaments follow individual lock valleys and
distorted their rigid shapes. Iteration 31 retained rigid shapes but lacked
whole-ornament clearance. Iteration 32's clearance lift moved the ornaments too
far from their approved Front positions; its remaining renders were cancelled.
None is a visual improvement to promote. Checkpoint 33 restores iteration 29's
placement and retains the glint ownership and evidence-integrity fixes.

## Remaining Visual Work

The checkpoint is visibly different from the approved Carol. In particular:

- The Front lock overlap, proportions and blue/white pattern are not yet a
  tuft-level match to the approved Front or the old Carol's finished appearance.
- The Side ear exposure and surrounding wool still differ from the reference.
- The front-quarter face/collar integration and torso lock rhythm need further
  perceptual refinement. A smooth, closed mesh is insufficient evidence.
- Ornament mounting and the Side silhouette still need checking together with
  the fleece. The ornament exception does not waive obvious attachment defects.

No Human, motion, deformation, runtime or device PASS. Phase 2 has not started.

## Checkpoint Verification

Saved asset SHA256:
`2c43ee10a71d4682dcc95d50d7cd64e3d365c1bc2fa224b35907776aaa445311`.

- Actual asset reopen and technical audit: PASS, including unchanged accepted
  Skin source, current authority hashes, finite vertices, closed nondegenerate
  fleece, packed images and matching ornament/glint owners.
- Evidence integrity: PASS for all 12 beauty views and 4 clay views. Asset,
  generator and image hashes match; dimensions and nonblank alpha were checked.
- A stale iteration 29 manifest was rejected against the newer saved asset,
  confirming that old evidence cannot silently become the current comparison.
- Python syntax parsing: PASS for all five v004 scripts.
- Equal-height silhouette IoU: Front 0.96473, Side 0.90857. These are outline
  diagnostics only, not identity, surface-quality or visual-acceptance scores.

## Reproduction

Use the existing Python environment and Blender 5.2 installation. No new
packages, add-ons, dependencies or external assets are required.

```powershell
python scripts/blender/carol-fleece-v004-authority.py
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' -b -t 8 --python-exit-code 1 --python scripts/blender/build-carol-normal-fleece-v004.py -- build --spatial --solid-locks --painted-shade --draft --render --quick --folder iterations/33 --views front,yaw-15,yaw+15,yaw-30,yaw+30,yaw-45,yaw+45,side,yaw+90,yaw+135,rear,top
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' -b -t 8 --python-exit-code 1 --python scripts/blender/build-carol-normal-fleece-v004.py -- render --quick --clay --folder iterations/33-clay --views front,yaw+30,side,top
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' -b -t 8 --python-exit-code 1 --python scripts/blender/audit-carol-normal-fleece-v004.py
python scripts/blender/review-carol-normal-fleece-v004.py iterations/33
python scripts/blender/review-carol-normal-fleece-v004.py iterations/33-clay --verify-only
```

The build explicitly selects the regional variant. Bare legacy invocations are
not a reproduction command. Save uses a staging `.blend` followed by replacement;
textures used by the saved asset are packed.
The review command checks asset, generator and render hashes, image dimensions
and nonblank alpha before producing comparisons. It refuses stale evidence.
