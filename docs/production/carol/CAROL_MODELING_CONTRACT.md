# Carol modeling contract

## Identity and evidence

- `assets/grimo/source/carol/approved-3d/authority.json` is the geometry authority for Carol's 3D production references.
- For geometry, volume, proportion, depth, and part placement, the six approved individual production views are the highest authority: Front, Side, Back, Top, Left 3/4, and Right 3/4.
- The six geometry authorities are `carol-front-ortho-transparent.png`, `carol-side-ortho-transparent.png`, `carol-back-ortho-transparent.png`, `carol-top-plan-transparent.png`, `carol-front-3q-left.png`, and `carol-front-3q-right.png`.
- `assets/grimo/source/carol/carol-Identity-canonical.png` remains the reference for identity, color, motifs, and appeal, but must not override those six views for concrete 3D depth, thickness, volume, or part placement. The production canonical sheet is supplementary and yields to conflicting approved individual views.
- Carol motion constraints: `docs/grimo/knowledge/character-production/carol/CAROL_MVP_MOTION_SPEC.md`.
- Side and both 3/4 views must be read together with Front when determining 3D volume. In particular, the face must never be flattened from the Front view alone.
- The Left/Right 3/4 views are formal evidence for muzzle/cheek/forehead volume, eye-to-face depth, ear-root/head connection, fleece-to-face ordering, body depth, fore/aft limb placement, and overall fleece volume.
- Preserve the sacred front-view identity: silhouette, face read, proportions, distinctive features, and appeal must survive the 3D interpretation.
- Do not treat generic sheep anatomy as a substitute for Carol. Generic anatomy drift is prohibited.
- The absence of a reference or measurement is an unresolved issue, not permission to guess.

## Production boundaries

- Author in Blender and exchange/ship through GLB/glTF for the planned PlayCanvas runtime.
- Do not begin geometry, rig, animation, or runtime implementation until the initial geometry interpretation and decision are complete.
- The front-facing render must satisfy `docs/production/carol/CAROL_CAMERA_CONTRACT.md`.
- Calibrate world-space geometry and camera settings together against that screen-space contract; production convenience may not distort canonical visible identity.
- Structural Blockout v002 is explicitly authorized and awaits its own Human
  Gate. This authorization does not extend to rigging, topology lock, animation,
  final materials, UV/fur, GLB/glTF or runtime integration.
- Physics must not decide hero acting, facial acting, primary touch reaction, main body acting, or primary fleece performance.
- Keep hidden geometry and camera-dependent cheats subordinate to the approved individual production views; do not derive concrete 3D shape from Identity-canonical when it conflicts with them.
- Final visual acceptance remains a Human Gate; automated checks are supporting evidence only.

## Neutral structure and future presentation

The 2026-09-16 Human decision retains G1–G5. Full Companion uses the whole low
quadruped body and permits Carol to turn, rotate, walk and show her back. A
front-facing camera reference does not lock character orientation.

The future Close Window-Lean state requires rear weight-bearing support,
independently movable front limbs, forebody lift and readable face/upper fleece
above forehooves near/on the bottom viewport edge. Keep the neutral geometry
compatible with this possibility; do not pose, rig or animate it in v002.
The fleece is a design volume, not a rigid armor shell for future deformation.

## v003 structural study authorization — 2026-09-16

The current user request authorizes historical investigation, Blender modeling,
render/inspect/correct/re-render, evidence, commit and push before HUMAN Gate.
V003 may revise the fleece and attachment depths while preserving the v002
Full-3D structure. Historical shallow relief/paint is research, not authority
to flatten the body or remove supports. Main merge remains prohibited; final
materials, rigging, motion and runtime integration are not authorized here.
