# Carol Skin default v004 — review entry

**`DEFAULT_BASELINE = PROMOTED`**

**`EAR_VISUAL_HUMAN_REVIEW = PENDING`**

The working standalone asset is [`carol-skin-default-v004.blend`](../../../../../assets/grimo/production/carol/blender/carol-skin-default-v004.blend), SHA256 `c14f15e35af18e17a63506ea1f4c8ec0f69cb4f52882d27cfa22cb01db7e1f7d`, built fresh from the preserved v003 Skin. Only `EAR_L`, `EAR_R`, and their existing `SoftInnerBowl` point values changed. All 19 non-ear Skin structures and both ear material node trees match v003. No Fleece or ornaments are in the standalone Skin.

## Visual evidence

- [Ear authority comparison](ear-authority-comparison.png): Identity and approved Normal Front/Side authority above v004 Front, Side, front 3Q and Top views.
- [Matched v003/v004 ear comparison](ear-v003-vs-v004.png): Front, Side detail and Top detail at the same cameras and lighting.
- [Fleece occlusion](fleece-occlusion.png): v004 ears beneath unchanged v004 Fleece at Front, front 3Q and Side.
- [Full Skin v003/v004 comparison](skin-v003-vs-v004.png): matched Front, front 3Q and Side views; non-ear appearance is unchanged.

The ears have fuller mid and distal sections, distributed centerline and lower-rim droop, a quieter distal cross-section, a 0.003 H maximum distal retreat, and a longer `SoftInnerBowl` trough with a brown perimeter and soft distal fade. The material graph and trough shader are unchanged.

The Fleece-visible front axis measures **10.94°** for v004 versus **11.08°** for v003, below the 13–23° diagnostic target. The exposed silhouette ratio estimates are Front **0.818 / 0.859** and Side **0.902**; the side estimate is just above its 0.90 guide. These are image diagnostics, not geometry locks. The Front render still shows the inner pink trough subtly. The permitted single micro-adjustment has been used; this residual is for Human review, not a Human PASS.

## Technical record

[`build-report.json`](build-report.json), [`validation.json`](validation.json), and [`front-axis-diagnostic.json`](front-axis-diagnostic.json) record the build, saved-file checks, source hashes, and Fleece-visible measurements. The reopened output passes: 95 × 24 base topology (2,280 vertices per ear), mirror error 0, finite/manifold/intersection and outward-normal checks, root inside head at 0.052731 H, evaluated volume 0.011838 H³ per ear, maximum displacement 0.019900 H and mean displacement 0.004311 H. The existing ear material graphs are unchanged; `SoftInnerBowl` keeps zero pigment at the outer perimeter and tip.

Preserved source hashes:

- v003 Skin: `4f4661b672f8b2022ca819241c0624f36693e36505775736042fe821b703915a`
- v004 Fleece: `a73426d8483e5431e60bc5949b96506c447928682ad92ead6af3cbd1d1092420`
- v002 Skin: `321dccd9d7a9789eb3b496b2da2281c03cabb9dcf164f01447c81a9ba940cd7a`

## Reproduction

From the repository root with Blender 5.2 and the existing Python/Pillow environment:

```powershell
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' -b -t 8 --python-exit-code 1 --python scripts/blender/build-carol-skin-default-v004.py
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' -b -t 8 --python-exit-code 1 --python scripts/blender/validate-carol-skin-default-v004.py
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' -b -t 8 --python-exit-code 1 --python scripts/blender/render-carol-skin-default-v004.py
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' -b -t 4 --python-exit-code 1 --python scripts/blender/render-carol-skin-default-v004.py -- --axis-comparison
python scripts/blender/compose-carol-skin-default-v004.py
```
