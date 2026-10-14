# Shushu v003 — fur seam Texture candidate v003

2026-10-14 / Codex visual review: **local appearance PASS; Human Gate PENDING**.

The black tracing identifies the continuous fur-like line from the ear toward the shoulder, on both sides, and the band between the ears. On the saved model, the strong continuous side line has become soft cream fur shading; the crown's pink streaks have been removed. The original fur grain, ear colors and silhouette remain. A faint natural tonal flow is still visible at the sides; there is no assertion that the Head texture or shape is perfect at every possible angle.

## Baseline and result

- Work branch at start: `codex/grimo-motion-zero-based-design-20261011`, HEAD `29acb461f9d1a00670905f0bcaed6fd2c2ab5c1d`.
- Baseline v002 (Human explicitly called its eye-outline correction perfect): SHA256 `d9bfbac01404c39a22fe14306a4d225c7b8efde34b3402cca0e9e9933d40b4d7`.
- [Independent saved v003 GLB](../../../../../assets/grimo/production/shushu/tripo/geometry-v003/texture-cleanup/shushu-geometry-v003-tripo-texture-candidate-v003.glb): SHA256 `ed94fbc4f6f78eb21d9f4ca8e3a4e4741be23fcc1109653710a3d31aaad6e9ee`.
- Original Tripo GLB (`338ad5f8…bf077b`), v001 mouth, v002 eyes, official Blender Geometry/Rig/Motion and other characters were not overwritten.

## Visual evidence

- [Seven matching views: before / saved v003 / difference ×4](01-seven-angle-fur-comparison.png); [mask overlay](02-local-mask-overlay.png).
- `renders/` holds independently reloaded saved-GLB front, left/right 3/4, left/right profile, crown and back at 1024×1024; camera parameters are equal.
- [Human tracing](human-annotation.png); [Head-only and flat-Head diagnostics](renders/); [approved Body-only beside v002 and final v004](../tripo-eye-depth-v004/04-approved-side-reference.png).
- I opened the native-resolution saved renders and compared the profiles, crown, front and 3/4 views with the approved Body-only. The previous pink eye surrounds, floral irises, highlights, smile, tongue and blush remain. The final combined candidate with the later eye-depth correction is [v004](../tripo-eye-depth-v004/REVIEW.md).

Head-only retains the line, while flat-Head removes it. This supports a baked Head Texture contribution without claiming to identify every cause of the original seam.

## Locality and verification

The built-in image_gen supplied local repair material only ([prompt and provenance](IMAGEGEN.md)). Left/right profile and crown masks were projected to Head UV with a 16-pixel screen-space feather and two adjacent atlas texels for filtering. The previous eye/mouth changed texels were excluded. [`repair-config.json`](repair-config.json), `projection-masks-*.json`, `projection-map-*.json`, [`applied-projection-map.json`](applied-projection-map.json) and [`textures/changed-texels.png`](textures/changed-texels.png) record the selected and actual atlas changes.

[`candidate-validation.json`](candidate-validation.json) and [`targeted-checks.json`](targeted-checks.json) confirm 120,113 / 4,194,304 Head texels changed (2.863%), zero changes outside the selected projection, zero changes to previous eye/mouth texels, 11 other images byte-identical, and unchanged mesh/UV/material/other GLB JSON structures. All 825 protected inputs in the start snapshot matched. The v003 source hash matches the saved file used for the review render. No whole build/test, external Tripo operation, payment or merge was performed.

Human Gate remains PENDING for this new candidate. This Tripo model is a review asset, not the final Rig replacement.
