# Pino v005 Tripo donor — oral repair v002

2026-10-17 JST / branch `codex/pino-gem-cleanup-v001-20261017` / start HEAD `3dcc388714e76fc632352a26298fe8916b851dab`.

**Requested static donor repair complete. Human oral-repair appearance GO=APPROVED (2026-10-17, explicit Human review). Existing Rig image return remains HOLD.**

Human explicitly authorized repainting the necessary oral-only Texture area, removing v001's texel-identification blocker. This does not authorize redesign of the face, original replacement, or applying donor Geometry to the Master.

## Review

- [Same-camera face before/after](01-face-before-after.png)
- [Same-camera front and left/right 3Q before/after](02-three-view-before-after.png)
- [Original → texture-only diagnosis → completed local repair](03-cause-and-repair.png)
- [Saved final GLB raster orbit, −35° to +35°](04-mouth-orbit.gif) / [all 15 views](05-orbit-contact-sheet.png)
- [Lit face](after-face-close-lit.png) / [lit left 3Q](after-left-3q-lit.png)

The corrected GLB retains all four Meshes. Blue/purple gemstone facets and central stippling are absent in the inspected final views. The existing main mesh's pink tongue, nose and mouth rim remain; the small dark/red regular cavity is retained when visible obliquely. Canonical and approved Body-only were reviewed for a soft pink tongue and red/dark interior. The Human explicitly approved the v002 oral repair appearance on 2026-10-17. This is scoped to the corrected mouth and does not approve all Motion/runtime or whole-character appearance.

## Exact edit scope

1. **PinoOralLiner BaseColor only:** a new lossless 2048² sRGB PNG is evaluated from the oral surface coordinates at UV triangle/barycentric samples and padded within the oral atlas. Pink is used on the lower/front tongue region; darker red on deeper/upper tissue. Every PNG texel is red-dominant, including unused/gutter areas, so no blue/purple mosaic is left in the active oral image. No reference screenshot was pasted as a decal. Original UV coordinates and material assignment are unchanged.
2. **Causal overlap repair on the donor oral liner only:** [diagnosis](overlap-diagnosis.json) found 431 vertices within 0.0001 model units of the main surface and 199 in front. Texture-only repaint removed blue but retained the protruding collar and competing triangles; see the middle panel of the cause comparison. Only 435 of 1,321 oral vertices were moved inward in depth to a 0.001 target clearance along the front ray. Maximum displacement is 0.00558642 of model height 1 (0.559% H). Oral x/z silhouette coordinates, all 627 triangles, indices and UVs are exact; normals were recomputed only on the altered oral surface. The deeper cavity was not forced invisible. No regular Mesh was deleted or made transparent.

The main mesh, including actual tongue/nose/lip shape, both lids, all their POSITION/NORMAL/UV/index accessors, node/mesh/material definitions and the three other compressed image payloads are exact. [Repair audit](repair-audit.json) and [saved GLB checks](saved-glb-check.json) verify this. No Rig/Morph/Weight/UV/Master/return-map edit, Tripo regeneration or other-character edit occurred.

## Focused validation and limits

The final saved GLB was reimported for all renders. Direct before/after uses the original v001 cameras: Cycles 8 samples, no denoising, emission BaseColor, Standard view, 900². [Pixel differences](render-difference.json) are confined to explicit mouth rectangles in all four views; changed pixels outside those rectangles = **0**. This is evidence for the rendered views, supported by unchanged other payloads, not an all-camera proof. Lit checks use Cycles 64 samples + denoising with neutral world/key/fill; they are additional final views, not the pixel-equality baseline.

[Depth stability](depth-stability.json): EEVEE 512², identical front orthographic projection at camera distances 2.95, 3.00, 3.05. Pixels varying by >5/255: **214 before → 0 after**; >20/255: **69 → 0**. The final max variation is 3/255. The 15-view EEVEE orbit was visually inspected: no gemstone pattern or central flickering/stipple was observed. [Oral-hidden control comparison](orbit-raster-audit.json) is diagnostic; nonzero side-view differences include retained legitimate cavity pixels and are not scored as a defect. Final renders always keep the oral Mesh enabled. These are bounded static-donor tests; Rig animation, PlayCanvas/mobile and all possible cameras are unverified.

[Protection](protection.json): original exact-name root donor and saved v001 archive share unchanged SHA256 `7ec49ea1e4f4f0fed87787e37856041c8ba4d41f816fd92b105098021aa0567f`; v005 input/Master/return-map and Canonical/Body-only match their committed hashes. Original user checkout and its unrelated edits were not used as an edit destination.

## Delivery / remaining gate

[Corrected donor](../../../../../assets/grimo/production/pino/candidate-c/tripo-gem-cleanup-v002/pino-c-v005-tripo-gem-cleaned-v002.glb)
SHA256 `2c0543f00c35c60d86a5f18db1c172c64f09cede90843fa00703757870ea4ae7`.
[Oral BaseColor](../../../../../assets/grimo/production/pino/candidate-c/tripo-gem-cleanup-v002/pino-oral-basecolor-v002.png) is embedded in it.

Do not import this donor Geometry into the Master. The original Tripo coordinate/material-ownership mismatch from [v001 diagnosis](../tripo-gem-cleanup-v001/REVIEW.md) remains; this local donor depth correction adds another deliberate position difference. The [v005 image-return contract](../pretexture-reliability-v005/TEXTURE_CONTRACT.md) is unchanged. Repaint approval and the subsequent explicit Human oral-repair visual GO resolve the local appearance gate only, not exact mapping, animation compatibility or whole-character appearance acceptance.

Reproduce with Blender `pino-gem-cleanup-v002-contact.py`, Python `scripts/3d/pino-gem-cleanup-v002.py`, Blender `pino-gem-cleanup-v002-review.py -- --tag after` (+ `--lit`), `--tag texture-only`, `pino-gem-cleanup-v002-orbit.py`, `pino-gem-cleanup-v002-depth-test.py`, then Python `pino-gem-cleanup-v002-package.py`. Blender scripts are under `scripts/blender/`. NumPy/Pillow and Blender 5.2.1 are used. The texture-only GLB and raw orbit/depth frames are diagnostic artifacts, not deliverables. Reuse v001 original camera renders; do not overwrite the original archive. [File hashes](file-manifest.json).

## Human decision — 2026-10-17

Human stated **「Human Review＝OK」** for the reported v002 gem-removal result (`pino-c-v005-tripo-gem-cleaned-v002.glb`, SHA256 `2c0543f00c35c60d86a5f18db1c172c64f09cede90843fa00703757870ea4ae7`). **Scoped visual GO: oral color / gemstone removal / local overlap repair.** No GLB or original assets were modified by recording this approval. **Image-only transfer to existing Rig, material correspondence, texture in animated poses, PlayCanvas/mobile and whole-character visual gates remain HOLD/UNVERIFIED.**
