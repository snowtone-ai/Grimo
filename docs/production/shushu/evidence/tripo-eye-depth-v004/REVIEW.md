# Shushu v003 — side-view eye depth candidate v004

2026-10-14 / Codex visual review: **local appearance PASS; Human Gate PENDING**.

The user additionally pointed out that the eyeballs project forward in profile. I compared two small bilateral Eye_L/R node offsets in the saved GLB, `0.006` and `0.012` Blender Y units toward the back of the head. The larger trial made the dark rim visibly separate and weakened the 3/4 expression, so I rejected it. The selected `0.006` offset reduces the profile bulge while preserving the floral irises, highlights and expression in front and both 3/4 views. The pink eye-surround Texture correction previously approved by the Human is untouched.

## Assets and images

- Fur-only baseline [v003](../../../../../assets/grimo/production/shushu/tripo/geometry-v003/texture-cleanup/shushu-geometry-v003-tripo-texture-candidate-v003.glb), SHA256 `ed94fbc4f6f78eb21d9f4ca8e3a4e4741be23fcc1109653710a3d31aaad6e9ee`.
- [Independent saved combined v004 GLB](../../../../../assets/grimo/production/shushu/tripo/geometry-v003/texture-cleanup/shushu-geometry-v003-tripo-texture-candidate-v004.glb), SHA256 `3eb85dcd3fa18d07874b36bbb7922d502bda1bf88855f3b79a91eb6a9a66b119`.
- [Seven matching views, v003 / v004 / difference ×4](01-seven-angle-eye-depth-comparison.png); [v002 / combined v004](02-v002-to-v004-seven-angle-comparison.png).
- [Selected and rejected eye-depth trials](03-depth-trials.png); [approved Body-only profiles / v002 / v004](04-approved-side-reference.png); [front, 3/4 and side eye closeups](05-eye-closeups.png).
- `renders/` contains native 1024×1024 images independently rendered from saved v004, with matching cameras and lighting. I opened the saved images at native resolution, including front, both 3/4, both profiles and crown. The eye shape remains believable and cute across the reviewed views. These are subjective candidate judgments, not a 100% guarantee or Human approval.

## Scope proof

[`targeted-checks.json`](targeted-checks.json) confirms v003→v004 changes **only** glTF nodes 3 and 4 (`ShushuStatic_Eye_L`, `ShushuStatic_Eye_R`) to translation `[0,0,-0.006]`, equivalent to Blender Y `+0.006` posterior. The binary chunk is byte-identical; all other nodes, meshes, UV/accessors, materials, Texture images, skins and animations are unchanged. Front render changes are within the two eye areas; the mouth and lower face have zero changed pixels. V004 candidate hash equals the render source hash and the seven camera records match the baseline.

The combined model retains the [bilateral side and crown seam repair](../tripo-fur-seam-v003/REVIEW.md), v002 Human-approved eye-border repair and v001 mouth repair. Original GLB, official Blender Geometry, Shape Keys, 285-frame Motion proof, other characters and existing user changes were protected. This offline Tripo candidate is not a final Rig or production asset. Human Gate remains PENDING for the new fur and eye-depth corrections.
