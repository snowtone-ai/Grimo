# Carol ear production v001

**READY_FOR_HUMAN_EAR_REVIEW — HUMAN REVIEW REQUIRED.** No perceptual approval or authority promotion is claimed.

- Branch: `codex/carol-ear-production-v001`.
- Verified source: `origin/codex/carol-hero-modules-v003` at `f4c4d465b0adcb2ee8b7d95fe22aa9a3d4c878d5` (matched the requested source).
- Current ear authority: SHA-256 `f10d6aad9201da6030798050aff5f057a76ee5f0645a1e231186d5798fb58384`; actual size **1309 × 1202**, detected panel dividers **654 / 580 px**. Historical `ca348f…` authority was not used.
- Candidate: [carol-ear-production-v001.blend](../../../../../assets/grimo/production/carol/blender/carol-ear-production-v001.blend).
- Donor: `carol-hero-modules-v003.blend`. Its full spatial v011 chassis and corrected neutral eyes provide a readable attachment context. Its old ear geometry was entirely replaced.

## Donor / historical audit

Inspected the actual v003, v002, v011, v013, hero-experience-probe-v001 and a-v006 assets. v002/v003 share v011's support chassis; v013 changes the chassis/eyes without supplying fleece. The experience probe supplies continuous v004 fleece, but initial attached renders showed it hiding most of the approved ear envelope. a-v006 has an older face/axis system and densely sculpted fleece. The v003 body therefore gives the most useful frozen attachment context; the probe's unmodified fleece appears only in diagnostic insets and is **not saved in this candidate**.

The v003 README, metrics/history and ear/build/fitting code confirm that the previous swept elliptical family traded Front/Side/Top fit against one another. That fitter and its geometry were not reused.

## Ear construction and scope

Only **`EAR_L` and `EAR_R`** changed: mesh, ear-only materials, semantic station groups, subdivision and provisional test shape keys. **39 other objects** match before and after save/reload by transforms, mesh/shape-key digest, counts, material assignments, parent and modifier identity. Head-side edits: **zero**.

One asymmetric 12-station × 16-point closed control cage (192 vertices per ear; 2,946 evaluated vertices) independently controls anterior/posterior breadth, upper/lower contour, brown cushion, rounded distal cap and shallow pink seat. Pink is a material region in the same closed shell. The opposite ear is a geometry reflection across Y=0 with outward normals and positive object scales. All module views render the same neutral `EAR_L`; no per-camera geometry. The 3Q authority crop is explicitly mirrored for presentation only.

Independent `TEST lift`, `TEST droop` and `TEST attention flick` keys bend a fixed-root, progressively softer spine. Every test key is **zero in the saved file**. These controls are provisional, not a production rig or an approved animation.

## Targeted validation and review limits

Save/reload, finite coordinates, closed manifold topology, outward normals, mirror equivalence, zero neutral controls and four-image decoding passed. Evaluated neutral/lift/droop/attention meshes have zero non-adjacent triangle intersections. Volume stays within **−2.14% / +1.68%** of neutral. Root centers sit approximately **0.053 H inside the unchanged head**; the first three station loops stay fixed within floating-point tolerance. Front root-to-tip station angle: **18.12°**.

Inspected Front/Side/Top/3Q together, whole-character attachment, and fixed-camera bends for thinness/collapse, twist, tip sharpness, rim discontinuity, detached pink, root pegs/gaps/pinching, mirrored orientation and animal-style drift. Technical checks do not establish Carol identity, cuteness or motion naturalness. **Side curvature, brown/pink balance and root fullness still differ visibly from the authority and need Human judgment.** Existing fleece substantially occludes the ear and can expose separated portions during motion; final fleece clearance remains unresolved. The ear was not distorted to hide this donor limitation. Existing body/eye/hoof limitations remain frozen.

## Review images

- [Current authority / candidate, four views](ear-isolated-comparison.png)
- [Attached Front, with fleece diagnostic](carol-ear-attached-front.png)
- [Attached Side, with fleece diagnostic](carol-ear-attached-side.png)
- [Neutral / lift / droop / attention](ear-deformation-check.png)
- [Machine-readable validation](validation.json)

Reproduce with Blender's `--python scripts/blender/build-carol-ear-production-v001.py`, then run `scripts/blender/compose-carol-ear-evidence-v001.py` with Python/Pillow/NumPy. Intermediate renders go to the OS temporary directory. No frontend, runtime, GLB or full production-rig validation is claimed.
