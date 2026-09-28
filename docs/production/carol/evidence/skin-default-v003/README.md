# Carol Skin default v003 — review entry

**DEFAULT_BASELINE = PROMOTED**

**EAR_VISUAL_HUMAN_REVIEW = PENDING**

The standalone asset is [`carol-skin-default-v003.blend`](../../../../../assets/grimo/production/carol/blender/carol-skin-default-v003.blend). It combines the saved internal Skin of `carol-normal-fleece-v004.blend` with locally refined ears from `carol-skin-ear-correction-v001.blend`. The older `carol-skin-final-v002.blend` remains the historical fallback. No Fleece was edited.

## Visual evidence

- [Ear authority comparison](ear-authority-comparison.png): canonical Identity, approved Normal views, and saved v003 Skin.
- [Matched Skin baseline comparison](skin-baseline-comparison.png): old standalone v002, v004 internal Skin, and v003 at Front, front 3/4, and Side.
- [Ear v001 versus v003](ear-v001-vs-v003.png): the prior ear candidate against the refined ear.
- [Temporary Fleece occlusion](fleece-occlusion.png): saved v003 ears under unchanged v004 Fleece at Front, front 3/4, and Side.

The v003 root has broader buried volume and a smoother emergence from the head. The outer ear has a softer arc and organic thickness taper. The inner pink area follows a recessed trough with a rounded, softened distal end. Both ears remain independent appendages for future motion work; this checkpoint adds no rig or animation.

## Composition and validation

The saved v004 `CENTRAL_CHASSIS` and all other non-ear Skin objects, including their materials, were retained. This carries forward the later under-chin geometry and surface response. `HeadFleeceBacking` is a mantle beneath external HeadFleece, so it was excluded along with HeadFleece, BodyFleece, TailFleece, ornaments, presentation references, and Fleece owners. Cameras and lights in the standalone file are review fixtures, not character geometry.

[`composition.json`](composition.json) records the object selection and source hashes. [`validation.json`](validation.json) records reopening the saved output, identical snapshots for all 19 retained non-ear objects and their material node trees, finite/manifold ears, buried roots, bilateral symmetry, Skin-only visible geometry, and unchanged source files.

The temporary Fleece check supports a credible visible ear at Front, front 3/4, and Side. Human judgment is still needed on the Side pink extent and a faint distal boundary. This is a working default, not a Human visual pass.

## Reproduction

Run `scripts/blender/build-carol-skin-default-v003.py` and `scripts/blender/validate-carol-skin-default-v003.py` with Blender background Python, then `scripts/blender/render-carol-skin-default-v003.py` with Blender and `python scripts/blender/compose-carol-skin-default-v003.py` from the repository root.
