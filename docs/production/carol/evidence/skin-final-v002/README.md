# Carol Skin final head refinement v002

**Status: READY_FOR_HUMAN_FINAL_SKIN_REVIEW. Human approval is pending.**

- Branch: `codex/carol-skin-final-v001`.
- Input: pushed commit `0d6f26a9554639d780f626d2466c48c23e2d9f06`, with a clean working tree at task entry.
- Production asset: `assets/grimo/production/carol/blender/carol-skin-final-v002.blend`.
- Unmodified baseline: `assets/grimo/production/carol/blender/carol-skin-final-v001.blend`.
- Authority manifest: `assets/grimo/source/carol/approved-3d/authority.json`. All seven referenced authority hashes were checked and preserved.

## Human review

1. [before-after.png](before-after.png): prior candidate and refined candidate at identical Front, Side, and 3/4 camera settings and image scale. This shows the combined geometry, material, and saved lighting change.
2. [head-detail.png](head-detail.png): larger Front, Side, and 3/4 views of the final head, with neighboring geometry present. The close framing crops the distant ear tips; the full-body boards show the complete ears.
3. [skin-authority-comparison.png](skin-authority-comparison.png) and [profile-closeup.png](profile-closeup.png): original approved Skin references, final saved model, and fixed-registration 50% overlays. Front retains the inherited 994 px/H registration; Side retains the inherited support/ground registration of approximately 1030 px/H. Neither registration is refitted to the new head.
4. [matched-geometry-comparison.png](matched-geometry-comparison.png): unchanged v001 geometry versus v002, both with the final materials and lighting. Source blush remains at its original facial location. This separates the geometric correction from the presentation improvement.
5. [normal-identity-context.png](normal-identity-context.png): approved Normal Front/Side beside the refined Skin model. This is an identity-context comparison, not a common-scale silhouette fit; Normal includes fleece.
6. [spatial-review.png](spatial-review.png): full-body Front, Side, derived 3/4, Rear, and Top sanity checks of the same neutral mesh.
7. [validation.json](validation.json): source/output hashes, authority hashes, actual eye bounds, unchanged-region checks, ear attachment and evaluated mesh checks.

All final images come from the saved and reopened production asset. Raw Cycles RGBA images are in `renders/`. Review boards only composite onto white, crop, label, and uniformly resize; there is no render retouch, nonuniform image scaling, or camera-specific model deformation. The old baseline is never overwritten.

## Correction and cause

The Human feedback was treated as visible direction, taking priority over an exact match to the previous candidate's Front crown registration. The previous Side evidence placed the crown and eyes low relative to the body. Its face material also blended into an older darker cream at the jaw, while the body used a separate warmed material; strong frontal illumination compounded the contrast with the side body.

- Raise the head by `0.027 H` around a `Z = 0.45 H` reference and expand its vertical dimension by 6%. Width, front-to-back depth, short muzzle projection, and lateral eye spacing are retained. The short neck attachment strip receives a blended displacement into the unchanged torso.
- Add a restrained local vertical expansion across the eye band, fading out before the crown and ear roots. Carry eyes, lids, nose, smile, and procedural blush with the same smooth spatial mapping. Eye height changes from `0.149 H` to `0.16688 H` (12% overall); eye centers rise from `0.412 H` to `0.43672 H`. The local correction increases eye presence without another whole-head lift. This is an explicit visual correction requested by Human, rather than a claim that the supporting numerical target has been reapproved.
- Translate each ear rigidly upward by `0.03474 H` with its root. Ear vertices, topology, cup depth, droop, and materials are unchanged. Both roots remain seated inside the evaluated head.
- Bring face and body into a common light cream family, remove the old face-only emission boundary at the jaw, retain a subtle common `0.16` stylized fill term, and apply matching subtle subsurface settings. The blush remains attached to the cheeks.
- Increase broad neutral environment fill while reducing the directional/front light powers. Exposure stays at `-1.2`. This is saved scene presentation, not a postprocessed brightening of evidence.

The torso control cage from vertex 379 onward, four limbs, four hoof modules, and tail geometry are unchanged. Approved references are unchanged.

## Validation and limits

Save/reload validation passed. The evaluated central chassis and both ears have finite coordinates, outward signed volume, no nonmanifold edges, and no detected nonadjacent triangle intersections. Both ear roots remain inside the head surface. Signed eye-to-head surface clearances are recorded before and after, with a check against new penetration. Packed eye pigment is present. Unchanged body/limb/hoof/tail snapshots and unchanged local ear mesh hashes were checked.

The Front and Side paintings do not imply exactly the same head height under the inherited whole-body registration. Raising the head to improve the Human-visible read deliberately places the Front crown above the earlier exact Front alignment; the Side crown moves closer to the approved Side. These overlays remain diagnostics, not authority or acceptance scores.

The model retains more three-dimensional under-jaw shading and a more structured lower-cheek/chin contour than the softly painted authority. The Side eye also reads slightly narrower than the painted Side eye. These are disclosed perceptual differences for the final Human review; the pass preserves the accepted ear and body progress rather than reworking those regions. Fleece integration, rigging, animation, and runtime appearance are outside this focused Skin pass.

## Reproduction

```powershell
blender -b --python-exit-code 1 --python scripts/blender/refine-carol-skin-head-v002.py
blender -b --python-exit-code 1 --python scripts/blender/refine-carol-skin-head-v002.py -- --comparison-source
python scripts/blender/compose-carol-skin-head-evidence-v002.py
```

`--preview` on the refinement script makes disposable lower-resolution previews in ignored `artifacts/` without saving a production asset. The final rebuild always starts from v001, so rerunning cannot compound the correction.

**Next handoff: HUMAN — final Skin-phase approval review.**
