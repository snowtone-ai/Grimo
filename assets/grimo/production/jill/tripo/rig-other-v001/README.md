# Jill Rig Other v001 — REVIEW CANDIDATE / HOLD

Research → Plan commit `832e1e89bcbfadb74f14154a87211056b997497c` → implementation.

- `jill-rig-other-v001.blend`: editable Blender 5.2.1 LTS rig and bounded control proof. Human appearance approval **PENDING**.
- `jill-rig-other-v001.glb`: deform skeleton, morphs, semantic anchors and sampled proof. See [Evidence](../../../../../../docs/production/jill/rig-other-v001/Evidence.md) before adoption.
- `source/`: immutable input byte copies; never save over these files. [Manifest](../../../../../../docs/production/jill/rig-other-v001/manifest.json) records source and output SHA256.

## Operate in Blender

1. Open the blend. Frame 1 is neutral. Select `JILL_RIG`; Object Properties → Custom Properties contains 39 semantic channels. Anatomical L is +X; front is −Y; Z is up.
2. The active `Jill_Representative_Control_Proof` action animates these properties. For free authoring, unlink its action in the Action Editor (keep the action datablock), then set the desired channels. A frame change otherwise restores the action's values.
3. `wing_open.L/R`: +1 opens, −1 folds within the implemented small range; flap and camber are separate. `paw_offer.L/R`, chest/head, tail, eyes and face are independent. Bone collections group the skeleton.
4. Move `CTRL_paw_IK.*` / `CTRL_foot_IK.*` in world space and enable the matching `paw_ik.*` / `foot_ik.*`. No stretch. Unreachable targets retain residual error. They do not certify prop contact or physical balance.
5. Individual leaf bones expose `local_bend`; regional leaf properties add to it. Direct un-driven pelvis/spine/limb FK remains available. Driven channels should be operated through their properties.
6. [Proof schedule](../../../../../../docs/production/jill/rig-other-v001/proof-schedule.json) lists peaks/halves/returns. These are control demonstrations, not a finished Motion library. Low support is not true rump-supported sitting.

## GLB boundary

The GLB contains 130 joints, three meshes, 20 morph targets, 16 anchors and one sampled 361-frame proof at 30fps. Original UVs are retained; no formal Texture was authored. Blender drivers/IK are authoring logic and are not executable glTF controls. [Control contract](../../../../../../docs/production/jill/rig-other-v001/control-contract.json) and [exact driver/rest mapping](../../../../../../docs/production/jill/rig-other-v001/runtime-mapping.json) document porting. Arbitrary runtime control combinations, PlayCanvas/mobile performance, all Motion and equipment fit remain outside the verified result.

Natural blink/eye-socket continuity, mouth finish, root/leaf intersections and approved pose references remain HOLD. A file that opens and exports is not Human visual approval.
