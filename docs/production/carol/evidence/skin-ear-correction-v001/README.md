# Carol Skin ear correction v001

Status: **ear-only correction candidate, awaiting Human perceptual review**. Not a completed Skin redesign, accepted Skin replacement, or Normal/Fleece pass.

## Routing and source

- Branch: `codex/carol-skin-ear-correction-v001`.
- GitHub checked first with `git fetch origin --prune` and `git ls-remote --symref origin HEAD`. Latest active production branch and local HEAD both resolved to `f135284bf30a6fb4f1dfd9bfc4a9aee1ad173ac4`; remote main was `825febfde94f1998b55073cadcdf96c53d6b19e3`. This focused branch starts at the active production checkpoint.
- Input: `assets/grimo/production/carol/blender/carol-skin-final-v002.blend`, SHA256 `321dccd9d7a9789eb3b496b2da2281c03cabb9dcf164f01447c81a9ba940cd7a`.
- Output: `assets/grimo/production/carol/blender/carol-skin-ear-correction-v001.blend`. Output hash is in `validation.json`.
- Current canonical identity and approved Normal Front/Side were visually inspected first, then supporting Skin Front/Side, active ear module, geometry parameters and accepted Skin evidence. Normal's broad brown cushion and pink lower bowl take priority over realistic sheep anatomy. Historical Skin evidence says approval pending; current production state explicitly identifies v002 as accepted and takes routing precedence.

## Diagnosis and local change

The accepted Front already has a useful broad droop. Its root rises into a narrow folded-looking ridge; Side compresses the pink bowl into an angular distal end, while the outer brown tip dominates. Oblique views preserve the ear identity but expose the abrupt root seat. This pass preserves that useful base rather than rebuilding it.

Only the vertex coordinates of `EAR_L` and `EAR_R` change:

- Expand section depth by 14%, with an additional smoothly decaying 20% at the buried root, and seat the proximal ear inward by up to `0.010 H`.
- Extend the tip-side sweep progressively by up to `0.016 H`; increase the middle section height by up to 5.5% and add a gentle downward displacement up to `0.006 H`. Preserve broad rounded ends, avoiding a pointed realistic leaf.
- Ease the distal pink cup height locally by up to 18%, with a falloff into neighboring brown surfaces. Preserve the continuous recessed cup, brown/pink material assignments and blush attribute.
- Retain the existing 2,280 vertices / 2,258 faces per ear, subdivision, transforms and materials. No remesh or new objects.

Ear enclosed volume changes from approximately `0.008248 H³` to `0.010430 H³` (+26.5%). This measures volume, not a perceptual acceptance score.

No changes to face, eyes, lids, muzzle, nose, mouth, head/chassis, torso, legs, hooves, tail, proportions, lights, material nodes or approved references. Head-adjacent surface edits were unnecessary. The accepted source asset is untouched. Existing untracked `prompt.md` and v004 iteration 33 `spatial.png` were preserved and excluded from the commit.

## Review evidence

- [old-vs-new.png](old-vs-new.png): old above / new below; full Skin Front, Side, front-weighted 3Q.
- [ear-focused.png](ear-focused.png): attached Side detail and Top attachment/thickness diagnostic, old above / new below.
- `new/front.png`, `new/side.png`, `new/front-3q.png`: individual full character renders.
- `new/ear-side.png`, `new/ear-top.png`: local details, with adjacent geometry visible.
- `old/`: identically framed accepted-source renders.
- [validation.json](validation.json): save/reload comparison, unchanged-object snapshots, topology and root checks.

All images are Cycles renders from the saved/reopened source or candidate with the same settings for each paired view. Boards only label, uniformly resize and alpha-composite onto white. No paint-over, shape warping or per-view geometry changes. Top is a diagnostic, not an authority image.

## Validation and remaining uncertainty

Saved/reopened candidate changes exactly two objects; the other 39 object snapshots match, including mesh/curve geometry, transforms, material slots and parents. Ear counts, subdivision and material assignments are retained. Both evaluated ears have finite coordinates, outward volume, zero nonmanifold edges and zero detected nonadjacent triangle intersections. Both root section centers remain inside the unchanged head. Center-inside testing alone does not establish seamless surface attachment or animation readiness.

The intended improvement is deliberately restrained: fuller side volume and a broader, softer distal body with a more substantial root. The Side pink end **still reads somewhat angular**, and the proximal ridge remains visible on naked Skin. Exact Normal identity fidelity and root naturalness require Human judgment. No Human PASS is declared. The existing dense section layout has no rig or shape keys; motion/deformation and future fleece clearance were not tested. This is a reusable neutral structural candidate, not a certified production rig.

Next minimal task: Human comparison of the two boards, focused on root naturalness and Side pink-end shape. If rejected, restrict the next edit to those ear sections; do not begin Normal/Fleece or broaden the Skin task.

## Reproduce

```powershell
blender -b --python-exit-code 1 --python scripts/blender/refine-carol-skin-ear-v001.py
python scripts/blender/compose-carol-skin-ear-v001.py
```

The builder always starts from the hash-pinned accepted Skin, so reruns do not compound edits. The composer uses Pillow and Windows Arial.
