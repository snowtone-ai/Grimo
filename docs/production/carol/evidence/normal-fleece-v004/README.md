# Carol Normal/Fleece v004: Head, Neck and Body Proportions

Status: **NORMAL_FLEECE_V004_IN_PROGRESS**. Not a completed phase or an accepted
Human-review candidate. Technical checks are not visual acceptance.

## Latest Human Decision

Checkpoint 37 corrected the direction, but the head and body still read as one
continuous mass. The Human clarified a smaller fleece surround at the head and
neck, with a larger round torso behind it. Head wool must not extend ahead of
the nose; the lower wool belongs to the neck, not the chin. The body fleece
should also be slightly smaller because its spatial volume still feels inflated.

Mareep is a comparative anatomy reference, not a replacement design or asset
donor. Game-rendered images were inspected through the browser on the
[Scarlet/Violet reference page](https://w.atwiki.jp/pokemonsvshiny/pages/62.html)
([inspected image](https://img.atwiki.jp/pokemonsvshiny/attach/62/2008/%E7%B8%A61.jpg)).
The useful visual reading is a forward-projecting face against a rounded woolly
body. Carol retains its own surrounding head fleece, eyes, ears, palette and
approved Front/Side authority. No external model or texture was imported.

The Human rejected iteration 33's shape: texture improved, but fleece around
the face and body is swollen, unnatural, and substantially inferior to v002.
Directly reconstructing Front/Side image shapes is insufficient. Interpret the
authority as a coherent creature. Production method is free to change.

This supersedes the earlier guide/lock approach as the preferred construction.
High silhouette IoU must not be used to justify inflated anatomy. v002 is the
preferred spatial baseline, not a newly accepted final model. Current approved
Front/Side remain the appearance authority; the original `prompt.md` is not a
fixed implementation contract.

## Active Checkpoint 41

The scene is rebuilt reproducibly from saved `carol-normal-fleece-v002.blend`:
`24d2cb5be9ee8f7261106f4927204b6fc8f332d876907efd2b049a29dfc0b3dc`.
The original v002 and accepted Skin source files are unchanged.

- Keep the v002 face opening, ear span, hoof size and ground contact as the
  baseline. Do not reuse v004-33's expanded guide and lock volumes.
- Keep v002's regional connected fleece geometry, with localized smooth sculpt
  fields: cheeks sit closer to the face; the bib moves slightly rearward and
  upward; the shoulder is slightly quieter. These are not image-outline fits.
- Reduce the head mantle's peripheral width without closing the face opening.
  Lower its crown and shorten its depth. Its frontmost point is now x=0.02737,
  behind the nose tip at x=-0.00346 (forward is -X).
- Recess the lower neck collar, with a gentle constriction toward the shoulder.
  Contract the resulting body fleece by 6% in X/Z and 7% in Y about its body
  lower attachment plane (z=0.06). This is an actual mesh change, not a camera
  or object display change. The low pivot avoids lifting the entire hem away
  from the legs while reducing the outer volume.
  Combined with the local sculpt, body bounds versus the v002 source decrease
  by about 12.1% in depth, 7.4% in width and 11.4% in height. The global scale
  factors alone must not be reported as the final measured bounds change.
- Head mantle width is 0.87050 versus body width 1.01715; head crown z=0.86358
  versus body crown z=0.90962. These establish geometric ordering, not appeal.
- Add a closed inner head mantle beneath the reduced locks. It stays inside
  their bounds, takes pigment from their nearest surface and shares the head
  owner. It bridges exposed scalp without inflating the outer head silhouette.
  It has no local contact shape keys; animation/contact behavior is unvalidated.
- Recess only the candidate lower chassis below the chin. The face above
  z=0.255 is unchanged by this field. This is not an accepted Skin revision.
- Preserve the existing shape-key deltas while moving their base coordinates.
  All keys are zero in the neutral review. Deformation is not accepted/tested.
- Retain the v004 spatial grain, colored occlusion and painted-light shader.
  Its pigment comes from v002's existing spatial color field, lifted into the
  pastel range, not from whole-image projection or camera-dependent geometry.
- Correct the inherited face emission for the new lighting, preventing a
  clipped-white face from concealing the jaw shape.
- Keep the ears in their original v002 position. Drooping/extending them in
  trials 35/36 increased occlusion and was rejected. Preserve tail geometry.
- Keep rigid ornaments; head and body ornaments follow their local shift without bending.
  Ornament and glint owners agree. Existing attachment issues are not waived.

This is **an in-progress head/neck/body proportion study**,
not a claim to have completed an entirely new semantic reconstruction.

`anatomy-construction.json` records the source hash, displacement magnitudes
and regional before/after bounds. `body-locks.json`, `face-locks.json` and
`spatial-locks.json` describe the rejected older construction, NOT checkpoint 41.
`tuft-inventory.json` remains a measurement record, not a final mesh recipe.

## Evidence

- `iterations/41/`: 12 same-saved-asset beauty views, comparison boards,
  product-scale comparison, manifests and outline diagnostics.
- `iterations/41-clay/`: Front, both 3Q directions, both sides and Top of that same saved asset.
- `iterations/41/neck-comparison.jpg`: checkpoint 37 above current, at identical
  camera scale, without equal-character-height normalization. Source hashes,
  asset hashes and side mirroring are recorded; camera matrices/scales/sizes
  are checked to match. This is the most useful size-change comparison.
- `iterations/41/anatomy-comparison.jpg`: authority, historical v002, rejected
  v004-33 and current revision at equal character height. Historical lighting
  differs; all model Side panels show the moon side, mirrored to face left. Source hashes
  and this display transform are recorded alongside the board.
- `asset-audit.json`: reopened asset audit including source and generator hashes.

Current saved asset SHA256:
`a73426d8483e5431e60bc5949b96506c447928682ad92ead6af3cbd1d1092420`.

Earlier iterations 01-32 and exploratory 34-36 are preserved locally under
`artifacts/carol-fleece-v004/iteration-history/`. Tracked 33 evidence is retained
as the Human-rejected comparison, not active evidence. A local copy of its asset
is `artifacts/carol-fleece-v004/iteration-33.blend`; Git also retains it.
Checkpoint 37 evidence remains tracked as the prior baseline; its saved asset
is also preserved locally as `artifacts/carol-fleece-v004/iteration-37.blend`.
Trials 38-40 are archived in `artifacts/carol-fleece-v004/iteration-history/`.
38 recessed/lifted the collar too far and exposed the upper forelegs. 39 reduced
the torso, but the head's outer width still equaled the torso. 40 reduces that
peripheral head mass while preserving the face aperture. 41 adds an internal
head backing and lowers the body scale pivot to reduce exposed scalp/leg gaps.
`iterations/33/spatial.png` is retained as the historical multi-view board for
the Human-rejected v004-33 checkpoint; it is not active production evidence.

## Remaining Work

Do not call this finished. v002's better anatomy still has a bead-like cheek
rhythm, a conspicuous lower collar, broad dorsal lobes and an imperfect ear/wool
junction. The authority's deliberate large/medium/small lock hierarchy and
blue/white grouping are not yet fully recovered. Ornament form and mounting
remain different. Full-spatial appeal is not established by mesh closure.
The smaller mantle exposes more of the unchanged ears and some upper foreleg
skin. Collar/leg transitions and ear-root continuity need refinement. The moon
and chest star are partly occluded; charm mounting is not complete. This is not
a claim that a numeric size reduction alone solves semantic construction.
Inspect the head backing and remaining skin/wool contacts in clay. Do not count
closed individual surfaces as an attachment PASS or assume the added backing
supports the inherited local shape keys.

Next decisions should preserve the recovered head/face/ear/body relationships,
not inflate each visible painted patch into an independent large volume.
Resolve macroform and attachment first, then develop shallow overlapping wool
and finer surface accents region by region. Check both 3Q directions throughout.

No Human, motion, deformation, runtime or device PASS. Phase 2 has not started.

## Verification and Reproduction

Actual saved-file reopen audit: PASS (finite vertices, closed nondegenerate
fleece, packed images, matching generator/source hashes and ornament owners).
Direct v002/current mesh comparison: PASS for unchanged ear, eye, eyelid and
hoof vertices/transforms; fleece shape-key deltas are preserved within 2e-7.
These checks do not establish visual quality or working deformation.

Use existing Python and Blender 5.2. No new dependencies or assets are needed.
The explicit flags below select the active construction, also selected by a bare
`build`. Historical paths require `--spatial` or `--radial-diagnostic` explicitly.

```powershell
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' -b -t 8 --python-exit-code 1 --python scripts/blender/build-carol-normal-fleece-v004.py -- build --anatomical-base --sculpt-anatomy --painted-shade --render --quick --folder iterations/41 --views front,yaw-45,yaw-30,yaw-15,yaw+15,yaw+30,yaw+45,side,yaw+90,yaw+135,rear,top
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' -b -t 8 --python-exit-code 1 --python scripts/blender/build-carol-normal-fleece-v004.py -- render --quick --clay --folder iterations/41-clay --views front,yaw-45,yaw+45,side,yaw+90,top
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' -b -t 4 --python-exit-code 1 --python scripts/blender/audit-carol-normal-fleece-v004.py
python scripts/blender/review-carol-normal-fleece-v004.py iterations/41 --anatomy-comparison --neck-comparison
python scripts/blender/review-carol-normal-fleece-v004.py iterations/41-clay --verify-only
```

The review verifier checks the current asset, generator and render hashes,
image dimensions and nonblank alpha. It rejects stale evidence. Pure sculpt
field checks cover bilateral symmetry, finite displacement and unchanged face
coordinates above the under-chin region. A 35 x 33 x 31 sample grid has positive
deformation Jacobian determinants (minimum: head 0.2384, body 0.3291, lower
chassis 0.3855); this is a local field check, not animation acceptance. Source
hashes protect the original v002 and accepted Skin. Outline measurements are
diagnostics only.
