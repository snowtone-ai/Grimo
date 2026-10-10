# Carol Normal semantic v001 — Human review entry

**NORMAL_SEMANTIC_V001_AWAITING_HUMAN_VISUAL_REVIEW**

One saved candidate, produced from legitimate baseline `b20afbcda1fe8ea246382f4b5e199af8997a9141` on `codex/carol-normal-semantic-v001` (2026-10-10). Technical verification does not grant Human visual acceptance.

[Blender candidate](../../../../../assets/grimo/production/carol/blender/carol-normal-semantic-v001.blend). Its exact saved-file hash is recorded in the audit and every render manifest.

## Review

- [Spatial board](beauty/spatial.jpg): Front, 15°, 30°, both front 3Q directions, both sides, rear 3Q, Rear, Top and perspective Hero. All orthographic views use the same camera scale.
- [Approved Front/Side comparison](authority-comparison.jpg): equal visible height; candidate Side is mirrored for display to face the same way as the reference. No geometry or image retouching.
- [Form and look](form-and-look.jpg): identical Front/3Q/Side in stylized color, Clay and silhouette.
- [Clay board](clay/spatial.jpg) and [silhouette board](silhouette/spatial.jpg): additional exposed geometry diagnostics.
- [Reopened asset audit](asset-audit.json): exact candidate SHA256, frozen-source checks, coat mesh checks and candidate-local accommodation.

## Construction

The head, body and external tail coat were rebuilt. v002 and v004 were inspected as failure/spatial evidence; their fleece geometry and shaders are not used in this candidate. Overlapping, unequal anatomical authoring volumes and selective smaller relief are fused and softened into three continuous surfaces. The generated pieces are not independent balls or independently animated lobes.

The smaller head has medium/small cloud rhythm, cheek fleece terminating above the jaw, a short narrowing toward the larger rounded body, and room for the Skin ears. Chest fleece belongs to the torso, sits behind the jaw and covers the upper forelegs. Rounded lower rump fleece covers the previously exposed lower chassis while tapering toward the hind-leg exits. The pearl tail tuft remains outside the rump under the existing tail pivot.

Frozen Skin v004 remains SHA256 `c14f15e35af18e17a63506ea1f4c8ec0f69cb4f52882d27cfa22cb01db7e1f7d`. All 19 original mesh/curve structures, their shape-key coordinates, modifiers and material graphs are retained unchanged in the candidate. The original `CENTRAL_CHASSIS` is retained hidden. A renderable copy, `CANDIDATE_NECK_SUPPORT`, recesses only the low neck below z=0.255 and x<0.40 behind the bare jaw. Its upper face remains coordinate-identical. This is explicitly candidate-local support accommodation, not a revised Skin baseline. Eyes, ears, limbs, hooves, support positions and Skin tail remain unchanged.

v002 donates the gold crescent, stars and glints. Their actual face direction is measured before seating them on the local coat; the crescent is torso-owned. The candidate uses intrinsic spatial vertex color, soft white/azure transitions and a camera-independent MToon-like smooth normal ramp, combined with actual lighting. It does not use genuine MToon 1.0, projected authority images, VRM, or a new runtime dependency. Clay separates genuine geometry from the colored shadow response.

This remains editable geometry. No production topology, rig, animation, deformation, GLB, runtime or device acceptance is claimed. Human must judge identity, cuteness, cloud rhythm, head/chest integration, ear emergence and the independent tail read against the approved references. Head/neck articulation and contact deformation require the subsequent representative evaluation.

## Reproduce

Run from repository root with Blender 5.2.1 and Python/Pillow/NumPy:

```powershell
blender -b -t 8 --python-exit-code 1 --python scripts/blender/build-carol-normal-semantic-v001.py
blender -b -t 8 --python-exit-code 1 --python scripts/blender/build-carol-normal-semantic-v001.py -- render --final --size 768
blender -b -t 8 --python-exit-code 1 --python scripts/blender/build-carol-normal-semantic-v001.py -- render --final --mode clay --views front,yaw+45,yaw-45,side,yaw-90,rear,top --size 640
blender -b -t 8 --python-exit-code 1 --python scripts/blender/build-carol-normal-semantic-v001.py -- render --final --mode silhouette --views front,yaw+45,side,top --size 640
blender -b -t 8 --python-exit-code 1 --python scripts/blender/audit-carol-normal-semantic-v001.py
python scripts/blender/review-carol-normal-semantic-v001.py docs/production/carol/evidence/normal-semantic-v001/beauty --final
```

All final render manifests identify the same saved asset hash and verify its stability through rendering. The compositor verifies every render hash against that manifest; the authority comparison records its source hashes and display mirroring. Rebuilding a `.blend` may change its binary serialization hash; regenerate evidence after each rebuild.

**NEXT GATE: HUMAN NORMAL/FLEECE VISUAL REVIEW**
