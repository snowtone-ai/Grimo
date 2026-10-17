# Pino Tripo mouth artifact — HOLD

2026-10-17 JST. Base: `994b59e825c005210997a23f0c791eb5c9bd3489`.
Branch: `codex/pino-gem-cleanup-v001-20261017`.

**Removal incomplete / HOLD. No corrected donor was produced.** The saved donor is an unchanged archive, not an approved or cleaned asset. Existing Rig/Master and returned-image map were not edited or applied.

## Evidence and attribution

[Review board](01-diagnosis.png), [face close-up](before-face-close.png), [front](before-front.png), [left 3Q](before-left-3q.png), [right 3Q](before-right-3q.png).
All are saved original GLB renders, Blender 5.2.1 Cycles, emission BaseColor, Standard view, 900px, 8 samples, no denoising. No visual PASS is claimed.

[Diagnostic oral-hidden image](without-oral-face-close.png) uses the identical close-up camera and hides only `PinoOralLiner_TRIPO_INPUT` in a disposable scene. The blue/purple faceted ring disappears and the main mesh's salmon tongue remains. **This is causal isolation, not a proposed mesh deletion or an after image.** Central speckling also changes with this occluding surface. It is consistent with competing closely overlapping surfaces; its precise depth/export cause is not resolved here.

[Oral texture](oral-atlas-enlarged.png) contains the blue/purple/pink mosaic on the regular oral liner. The faceted coloring is a **Texture defect on existing regular Geometry**. No separately attributable added jewel mesh was found. Do not interpret the diagnostic hide as permission to delete the liner.

[Surface diagnosis](geometry-correspondence.json) matches all 50,763 donor triangles one-to-one to source triangles after diagnostic uniform scale 1.00048852; source height 0.99951172 vs donor 1.0. Max corner distance 0.00002137 model units overall, 0.00001547 on oral. All 627 oral faces have unique existing source matches. This is tolerance-based diagnosis, not exact payload equality, a return correspondence, or permission to normalize the donor. Raw exact comparison in [diagnosis.json](diagnosis.json) fails for every triangle because coordinates differ. Donor position/UV/normal/index payload was never changed.

## Why HOLD

The apparent jewel is carried by the normal oral liner, not a detachable foreign component. The currently available references establish a pink tongue and dark mouth, but do not identify which pink texels on this overlapping Tripo liner are foreign versus legitimate tongue/interior. Deleting the liner would remove regular oral Geometry; replacing its entire atlas, flattening its depth, or projecting the main tongue onto it would also change legitimate oral appearance or boundaries. Those actions do not satisfy the user's artifact-only preservation requirement. No guessed mask, full oral repaint, transparency trick, or mesh removal was saved.

Consequently there is no valid before/after disappearance comparison or corrected GLB. The four original views and isolated close-up document the blocker; they are not completion evidence. Human identification of the permitted local texels/surface region, or an approved clean liner texture reference, is needed to proceed under the existing appearance lock. The requested complete removal remains OPEN.

## Image-return contract

[Contract result](return-contract.json): **HOLD** under the existing v005 CLI. Source Eye_L/Eye_R are merged into donor Pino_Skin; right lid material is renamed; positions differ. The diagnostic scale/nearest surface matching above is deliberately not used to bypass the required exact material-owned triangle contract. PBR/normal-map transfer, Master application, Rig/Morph, runtime/mobile, and Human appearance approval are outside this diagnosis and unverified. Geometry must never be transplanted into the Master.

Authority: [v005 State](../../PINO_PRETEXTURE_RELIABILITY_V005_STATE.md), [v005 REVIEW](../pretexture-reliability-v005/REVIEW.md), [TEXTURE_CONTRACT](../pretexture-reliability-v005/TEXTURE_CONTRACT.md), repository AGENTS/Goal, Canonical and approved Body-only refs. Earlier PENDING gates are not promoted by this work.

## Saved files and reproduction

Archive: `assets/grimo/production/pino/candidate-c/tripo-gem-cleanup-v001/pino-c-v005-tripo-donor-original.glb`; SHA256 `7ec49ea1e4f4f0fed87787e37856041c8ba4d41f816fd92b105098021aa0567f`, identical to the exact requested root file `pino-c-v005-tripo-output.glb.glb`.

With LFS assets hydrated: run `scripts/3d/pino-gem-cleanup-v001.py` with Python NumPy/Pillow; run Blender background `scripts/blender/pino-gem-cleanup-v001-review.py -- --tag before` and `--tag without-oral`; run `scripts/blender/pino-gem-cleanup-v001-geometry.py`. Scripts write evidence only, never the input/Master. Review uses disposable background Blender and does not affect an open scene.

[Protection checks](protection.json) compare exact donor hash and protected v005/source assets to committed LFS/content hashes. No Tripo regeneration, Smart UV, donor Geometry import into a Master, original replacement, or Rig application occurred. Commit scope is the archive and this diagnosis only; no app build is needed.
