# Carol Normal/Fleece v004: Anatomical Recovery

Status: **NORMAL_FLEECE_V004_IN_PROGRESS**. Not a completed phase or an accepted
Human-review candidate. Technical checks are not visual acceptance.

## Latest Human Decision

The Human rejected iteration 33's shape: texture improved, but fleece around
the face and body is swollen, unnatural, and substantially inferior to v002.
Directly reconstructing Front/Side image shapes is insufficient. Interpret the
authority as a coherent creature. Production method is free to change.

This supersedes the earlier guide/lock approach as the preferred construction.
High silhouette IoU must not be used to justify inflated anatomy. v002 is the
preferred spatial baseline, not a newly accepted final model. Current approved
Front/Side remain the appearance authority; the original `prompt.md` is not a
fixed implementation contract.

## Active Checkpoint 37

The scene is rebuilt reproducibly from saved `carol-normal-fleece-v002.blend`:
`24d2cb5be9ee8f7261106f4927204b6fc8f332d876907efd2b049a29dfc0b3dc`.
The original v002 and accepted Skin source files are unchanged.

- Recover the v002 head/torso relationship, face opening, ear span, hoof size
  and ground contact. Do not reuse v004-33's expanded guide and lock volumes.
- Keep v002's regional connected fleece geometry, with localized smooth sculpt
  fields: cheeks sit closer to the face; the bib moves slightly rearward and
  upward; the shoulder is slightly quieter. These are not image-outline fits.
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
- Keep rigid ornaments; bib ornaments follow the local shift without bending.
  Ornament and glint owners agree. Existing attachment issues are not waived.

This is **a recovery of the better spatial baseline plus local sculpting**,
not a claim to have completed an entirely new semantic reconstruction.

`anatomy-construction.json` records the source hash, displacement magnitudes
and regional before/after bounds. `body-locks.json`, `face-locks.json` and
`spatial-locks.json` describe the rejected older construction, NOT checkpoint 37.
`tuft-inventory.json` remains a measurement record, not a final mesh recipe.

## Evidence

- `iterations/37/`: 12 same-saved-asset beauty views, comparison boards,
  product-scale comparison, manifests and outline diagnostics.
- `iterations/37-clay/`: Front, 3Q, Side and Top of that same saved asset.
- `iterations/37/anatomy-comparison.jpg`: authority, historical v002, rejected
  v004-33 and current revision at equal character height. Historical lighting
  differs; all model Side panels show the moon side, mirrored to face left. Source hashes
  and this display transform are recorded alongside the board.
- `asset-audit.json`: reopened asset audit including source and generator hashes.

Current saved asset SHA256:
`c5903e810d17b46f1223664b5275683ffdf2a2b20995635fc378e0c58cc0eeec`.

Earlier iterations 01-32 and exploratory 34-36 are preserved locally under
`artifacts/carol-fleece-v004/iteration-history/`. Tracked 33 evidence is retained
as the Human-rejected comparison, not active evidence. A local copy of its asset
is `artifacts/carol-fleece-v004/iteration-33.blend`; Git also retains it.

## Remaining Work

Do not call this finished. v002's better anatomy still has a bead-like cheek
rhythm, a conspicuous lower collar, broad dorsal lobes and an imperfect ear/wool
junction. The authority's deliberate large/medium/small lock hierarchy and
blue/white grouping are not yet fully recovered. Ornament form and mounting
remain different. Full-spatial appeal is not established by mesh closure.

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
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' -b -t 8 --python-exit-code 1 --python scripts/blender/build-carol-normal-fleece-v004.py -- build --anatomical-base --sculpt-anatomy --painted-shade --render --quick --folder iterations/37 --views front,yaw-45,yaw-30,yaw-15,yaw+15,yaw+30,yaw+45,side,yaw+90,yaw+135,rear,top
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' -b -t 8 --python-exit-code 1 --python scripts/blender/build-carol-normal-fleece-v004.py -- render --quick --clay --folder iterations/37-clay --views front,yaw+30,side,top
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' -b -t 4 --python-exit-code 1 --python scripts/blender/audit-carol-normal-fleece-v004.py
python scripts/blender/review-carol-normal-fleece-v004.py iterations/37 --anatomy-comparison
python scripts/blender/review-carol-normal-fleece-v004.py iterations/37-clay --verify-only
```

The review verifier checks the current asset, generator and render hashes,
image dimensions and nonblank alpha. It rejects stale evidence. Pure sculpt
field checks cover bilateral symmetry, finite displacement and unchanged face
coordinates above the under-chin region. A 35 x 33 x 31 sample grid has positive
deformation Jacobian determinants (minimum: head 0.7101, body 0.7129, lower
chassis 0.3855); this is a local field check, not animation acceptance. Source
hashes protect the original v002 and accepted Skin. Outline measurements are
diagnostics only.
