# Shushu Production Rig v003 — reproduction and controls

This separately named derivative reads the saved v002 editable rig. All existing numeric controls, their names, rest bones, anchors, source mesh Basis, topology, UV and original Texture remain. Set numeric controls to zero for Neutral. Do not treat arbitrary FK or arbitrary combinations outside the tested support domain as approved poses.

Production outputs are `assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v006-production-rig-v003{.blend,.glb,-proof.blend,-proof.glb}`. The proof retains editable IK/drivers and the inherited 81-witness capability sequence. The main GLB bakes evaluated Skin/Morph/Anchor channels. The optional sphere in the proof GLB remains a diagnostic fixture, not an approved item. The existing v002 contacts GLB remains immutable; its real-item/runtime limitations are not resolved here.

Run from the repository root with Blender 5.2.1 and Python/Pillow/NumPy/SciPy. Every command writes only this v003 namespace:

```powershell
blender -b --factory-startup --python-exit-code 1 --python scripts/blender/build-shushu-production-rig-v003.py -- --trace
blender -b --factory-startup --python-exit-code 1 --python scripts/blender/build-shushu-production-rig-v003.py -- --build
blender -b --factory-startup --python-exit-code 1 --python scripts/blender/prove-shushu-production-rig-v003.py -- --focused
blender -b --factory-startup --python-exit-code 1 --python scripts/blender/prove-shushu-production-rig-v003.py -- --audit
blender -b --factory-startup --python-exit-code 1 --python scripts/blender/prove-shushu-production-rig-v003.py -- --proof
python -B scripts/3d/report-shushu-production-rig-v003.py textures
blender -b --factory-startup --python-exit-code 1 --python scripts/blender/prove-shushu-production-rig-v003.py -- --roundtrip
blender -b --factory-startup --python-exit-code 1 --python scripts/blender/build-shushu-production-rig-v003.py -- --render-before
blender -b --factory-startup --python-exit-code 1 --python scripts/blender/build-shushu-production-rig-v003.py -- --render --tag candidate
blender -b --factory-startup --python-exit-code 1 --python scripts/blender/build-shushu-production-rig-v003.py -- --faces
blender -b --factory-startup --python-exit-code 1 --python scripts/blender/build-shushu-production-rig-v003.py -- --trace-pose
blender -b --factory-startup --python-exit-code 1 --python scripts/blender/prove-shushu-production-rig-v003.py -- --render-saved
python -B scripts/3d/report-shushu-production-rig-v003.py lineage boards manifest preserve
node scripts/3d/validate-shushu-production-rig-v003.mjs
```

Wait for each asset-producing step before the next dependent step. Restore original embedded image bytes/material semantics before validating and reimporting the final GLB. `--thigh-owner` is an explicitly rejected diagnostic variant; do not use it to build the delivery.

The support corrective grid samples Seat 0…1 at 0.125 intervals and WeightShift −1/0/+1. The foot's existing low volume below rest z=.095 is rigidly owned by the original pinned foot; the transition above it blends into the inherited skin. Original foot proportions are not reconstructed from a new primitive. Lower-body quaternion volume and seam-coherent local relaxation are transferred through inverse linear skin; a broad posterior field settles the rump without per-vertex floor flattening. Existing v001 SeatVolume/v002 SeatFlow keys are replaced, other key coordinates are unchanged.

`Corrective.EyeIntegrity.LowHead` is limited to seated low-head/rest/half-blink context; `ShiftL` to seated left shift/left roll/partial Joy. Both fade off toward full blink, remain off at Neutral and in the other inherited witnesses, and change only eye/lid regions. The current repair opens the affected apertures to retain a coherent globe/pupil silhouette; it does not claim a newly approved half-lid or Joy design. Mouth, cheek, head pose and remaining facial keys are preserved.

Review images are actual renders, without painted fixes. Whole body: 640², Cycles 16 samples, seed 0, no denoising, AgX exposure −0.5, ortho 1.14, target (0,0,.5), distance 3, identical lights/ground. Face details: 768²/24 samples, ortho .56, fixed target (0,−.01,.715−.115×Seat); front and both 3Q cameras. Boards only crop/resize/place/label the original PNGs. Native images remain available. Technical checks and Codex observations do not substitute for Human visual approval.
