# Production Rig v004 — editable seat redesign

Read [REVIEW](REVIEW.md) for the actual gate and limitations. This is a separate asset namespace and never replaces v003 or the approved static source.

`Seat=0` preserves standing Neutral. The path anticipates forward over the foot support, advances both short legs, rolls onto the heel regions, lowers the rump, and settles into forward-feet sitting. `Seat=1` has 0.180 forward foot travel, 0.018 outward travel per side, 65° sole pitch, and hip translation (0, .015, −.116). An additional −.045×sin(π×Seat) Y anticipation occurs before settling. These are authored candidate parameters, not species norms or a physical COM measurement. Returning Seat to 0 recovers standing. `Rest`, `WeightShift`, face/ear/gaze/pressure/stroke/paw controls are inherited.

Original bone rest matrices and lengths remain. Foot positions are now controlled by a continuous path rather than the old unconditional world pin. The rigid rotated foot's lower envelope sets its ankle height using 33 samples; individual mesh vertices are never clamped to a ground plane. The original `CTRL_Foot.Left/Right` rotations remain editable. New child `CTRL_SeatSole.Left/Right` contributes the automatic sole pitch. `SeatFootHeight.*` values are computed driver channels, not user controls. Lower-body DQ volume targets and seam-coherent local relaxation are transferred to linear Skin via 16×3 pose corrective samples. Basis/topology/UV/texture remain inherited. Face keys are never reauthored.

Reproduce sequential asset steps with Blender 5.2.1 LTS:

```powershell
blender -b --threads 8 --factory-startup --python-exit-code 1 --python scripts/blender/build-shushu-production-rig-v004.py -- --build
blender -b --threads 8 --factory-startup --python-exit-code 1 --python scripts/blender/prove-shushu-production-rig-v004.py -- --focused
blender -b --threads 8 --factory-startup --python-exit-code 1 --python scripts/blender/prove-shushu-production-rig-v004.py -- --capabilities
blender -b --threads 8 --factory-startup --python-exit-code 1 --python scripts/blender/prove-shushu-production-rig-v004.py -- --proof
python -B scripts/3d/report-shushu-production-rig-v004.py textures
blender -b --threads 8 --factory-startup --python-exit-code 1 --python scripts/blender/prove-shushu-production-rig-v004.py -- --roundtrip
blender -b --threads 8 --factory-startup --python-exit-code 1 --python scripts/blender/prove-shushu-production-rig-v004.py -- --render
blender -b --threads 8 --factory-startup --python-exit-code 1 --python scripts/blender/prove-shushu-production-rig-v004.py -- --render --detail --names seat,seat-half,seat-closed,seat-joy,seat-lowhead,seat-shift-L,seat-shift-R,seat-offer-L,seat-hold-R,seat-both-hold
blender -b --threads 8 --factory-startup --python-exit-code 1 --python scripts/blender/prove-shushu-production-rig-v004.py -- --render --saved --names neutral,legs-forward,seat,seat-rest,standing-return
blender -b --threads 8 --factory-startup --python-exit-code 1 --python scripts/blender/prove-shushu-production-rig-v004.py -- --sequence
python -B scripts/3d/report-shushu-production-rig-v004.py boards preserve manifest
node scripts/3d/validate-shushu-production-rig-v004.mjs
```

All full-body comparisons use 512² Cycles / 16 samples / no denoising / seed 0 / AgX exposure −.5 / ortho 1.14 / target (0,0,.5), fixed lights and ground z=−.002. Camera directions are recorded in the build script; the small common elevation exposes support surfaces. Face details use 512², ortho .56 with target following the inherited head height. Sequence is 448² / 12 samples, sampled every 6 frames from the editable proof's first 169 frames at 24fps (each image is 0.25 seconds apart). Boards only place/resize/label actual renders. No image painting or appearance repair.

The proof begins with a separately timed seat/return sequence and then the inherited 81 capability witnesses (timing is a diagnostic proposal, not adopted product motion). Saved GLBs bake ordinary Skin/Morph and seven Anchor channels. A separate proof GLB contains a diagnostic held sphere; it is not an approved real item or physical mass solver. Runtime/smartphone and all untested combinations remain separate gates.

`Corrective.TrueSeatGrip.*` and computed `TrueSeatGripFit/Offset.*` are additive distal contact adjustments on a 4×9 Seat/WeightShift grid, active only when both hands hold. They preserve original keys and single-hand behavior and repair the old fixed-span contract under the new hips path. This technical fit does not resolve the visible shoulder folds in occupied-paw poses.

For the additional consecutive seated-composition excerpt, run the proof script with `--composition-sequence`. Then `python -B scripts/3d/report-shushu-production-rig-v004.py boards videos` builds labeled frame boards and FFmpeg videos from the actual saved-action frames. `seat-return.mp4` uses frames 1–169 every 6 frames; `seated-compositions.mp4` uses 589–621 every 4 frames. No optical-flow interpolation or image repair is applied.
