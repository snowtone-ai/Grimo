# Carol v008 — final bounded static Skin pass

**BLOCKED_AT_V008_SKIN_IDENTITY_FIT.** Revision **17** is retained as the best of three new shape attempts (15–17), but it is **not** a passing static candidate. Human Geometry Gate remains **PENDING**. Motion preflight was not run because no static candidate met the visual criteria. Do not advance to fleece.

The primary [Human comparison sheet](skin-human-fit-review.png) shows LOCKED, revision 14, revision 17 and 50% overlays for full Skin Front/Side, face Front/Side, hooves Front/Side and tail Side. Derived [3Q](diagnostic-revision-17-3q.png) and [Top](diagnostic-revision-17-top.png) rows compare revisions 14/17 and have no invented locked reference. The [full-screen check page](human-review.html) offers all nine rows with zoom and keyboard navigation. Revision-14 evidence is preserved under [baseline-revision-14/](baseline-revision-14/); revision-12 evidence remains under [baseline-revision-12/](baseline-revision-12/).

| Owner | Revision-17 result |
| --- | --- |
| Torso | Abdomen half-width at X .575 increased `.303→.3055 H`, X .730 `.305→.3075 H`; other stations unchanged. Evaluated maximum width `.598571 H` is inside `.598–.600 H`. Head, fore and hind torso intersection pair counts remain 400, 128 each and 134 each, equal to revision 14. Front/Side/3Q retain compact volume. |
| Hooves | One connected mesh and continuous planted sole per hoof. The crown has three intended rounded anterior Y/Z lobes separated by two valleys at local Y ±`.0365 H`; anterior bulges are carried through the lower face instead of the top edge. Nominal front/rear X extents are `.075/.076 H`. Evaluated width `.217385 H`, height `.111984 H`, depth `.173107 H`, ground min Z `.0000136 H`. Front read improves, but 3Q still resembles a brown tire. **Visual fail.** |
| Head / Side face | Upper skull control Z at four top sections changed `.630/.674/.697/.703→.635/.689/.716/.722 H`. Lower-rear head lift changed `.065→.025 H`; orbital X target base/slope `.145/1.02→.130/1.12`. Side forehead moves toward the locked Skin Side, but eye/cheek hierarchy remains insufficient. Front eye width `.137 H`, height `.149 H`, bilateral Y centers ±`.162 H` and pigment are unchanged. Mouth width `.091 H`; nose and philtrum frozen. |
| Head/chest | Separate HEAD_CAGE, SHORT_NECK_SOCKET and TORSO_CAGE still create a visible lower-head/chest ownership line. A disposable exact Boolean union and local smoothing test did not remove the crease and was rejected. Future head rotation risks sliding. **Static fail.** |
| Ear | Four root perimeter controls widened the embedded saddle; distal perimeter and bowl controls are unchanged. Side/3Q emergence is still abrupt. **Static fail.** |
| Tail | Unchanged from revision 14. Side remains round; partial Top occlusion alone is not a failure. No visual tail-motion claim. |

Revision 15 introduced the torso, lower-crown, forehead/orbital/cheek and ear-root adjustments. Its upper hoof scallop still resembled a tire. Revision 16 raised the scallop too high and produced horn-like bumps at the leg boundary; rejected. Revision 17 moved relief down the anterior face and recovered a smooth hoof top. No fourth geometry attempt was made.

Blender 5.2.1 LTS generated one neutral model for the unchanged Front/Side cameras. [measurements.json](measurements.json) stores control/evaluated geometry, support/contact diagnostics and the shared Front/Side digest. [validation.json](validation.json) records saved/reloaded geometry, exact revision-14 object comparison, unchanged camera/light/registration/landmark records, reference hashes and eye pigment. The verifier asserts torso width, hoof dimensions/ground contact/connectivity, support centers, eye dimensions and absence of hidden alternates, production rig/animation, Boolean or remesh. Visual failure takes precedence over numerical passes. [motion-clearance.json](motion-clearance.json) is `NOT_RUN_STATIC_GATE_BLOCKED`.

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b --python scripts/blender/build-carol-v008.py -- --revision 17
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b assets/grimo/production/carol/blender/carol-v008.blend --python scripts/blender/carol-v008-verify.py
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' -b assets/grimo/production/carol/blender/carol-v008.blend --python scripts/blender/carol-v008-diagnostics.py
python scripts/blender/carol-v008-evidence.py --revision 17 --baseline-directory docs/production/carol/evidence/reconstruction-v008/baseline-revision-14 --publish-blocked
```

The four source images/hashes, support centers, camera matrices, registration and coordinate system are unchanged. There is no fleece, production rig, animation, GLB or runtime work. Next handoff: **CHATGPT_PLANNER / HUMAN GEOMETRY REVIEW** of the bounded static failure, without self-approving the Human Gate.
