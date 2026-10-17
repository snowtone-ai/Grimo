# Jill v008 — historical FAILED texture-only trial

Derived from approved mouth + clover v007. The local BaseColor repair removes dark eye artwork accidentally retained on the surrounding body skin. Every geometry/UV/weight/Morph/driver/bone/anchor value is unchanged. Horns are unchanged.

- `jill-textured-rig-v008.blend`: packed editable model, neutral.
- `jill-textured-rig-v008.glb`: static skinned model, 130 bones / 20 Morphs / 16 anchors. Existing authoring contract has 39 channels.
- `jill-review-bounded-v008.glb`: bounded QA motion only, not a full motion library.
- `jill-basecolor-v008.png`: original 4K art with a local host-skin repair; all pixels outside the explicit mask are exact v007.

Evidence: [v008 diagnosis, renders and checks](../../../../../../../docs/production/jill/eye-boundary-v008/Evidence.md). Human rejected v008: the physical outer-eye cords remain. Historical texture-only trial; superseded by v009. Full-model completion is HOLD. Mouth Human GO, clover Human OK, horns unchanged. The existing 4-Morph mouth controller remains applicable to the static GLB.
