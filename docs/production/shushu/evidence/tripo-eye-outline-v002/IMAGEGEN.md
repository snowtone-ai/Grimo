# Local eye-band repair material

Tool: built-in `image_gen.imagegen`, 2026-10-14. No external Tripo operation.

Inputs, in order:
1. Saved v001 GLB emission render, `renders/before-front.png` (same pixels as preceding candidate-front).
2. Human annotation, `human-annotation.png`; black pen identifies the doubled boundary, not the entire enclosed pink surface.
3. Approved `assets/grimo/source/shushu/tripo-generation-pose/shushu_bodyonly_front.png`.

Prompt:
> Edit FIRST image with extremely localized texture retouch ONLY. Keep first image exact camera, geometry, all features, mouth, colors, proportions, lighting, size and layout. SECOND image is user's black pen annotation of the unwanted doubled border on right eye. Apply corresponding fix to BOTH eyes. Third image approved identity reference shows single smooth pink surround. Remove ONLY thin pale duplicate band running along upper and outer contour of pink eye surrounds and thin whitish duplicate boundary beside nose and beneath eyes. Preserve the entire main pink eye surround shape and pink fill, blush, white cheek sparkles, thick dark maroon eyelid outline, flower patterned purple irises, all iris highlights. Pink surrounds must have ONE continuous natural edge where pink meets cream, no pale concentric second arc. Fill pale pink arc using adjoining main pink color, keep existing outer pink silhouette unchanged. Along nose/lower rim remove whitish duplicate crescent adjacent to dark eye rim by continuing appropriate nearby cream/pink surface, WITHOUT removing dark eye rim or changing pupil size. Do not invent white eyelid rings. No global blur or regeneration. Keep already repaired smiling mouth and tongue unchanged. Photographically identical first rendered model except those thin unwanted duplicate borders. Return square full original view; alignment must match first image exactly.

Returned image: 1254×1254. Only samples inside the independently traced thin masks in `repair-config.json`, plus 2 atlas texels for filtering, are eligible for the Head PNG. The full generated image is **not** comparison evidence and is not used to replace the model's other pixels. Final comparison images must come from importing the saved candidate GLB.

Approximate annotation registration: original 1024px model render → screenshot `x=1.375*x+204`, `y=1.375*y-294`. Nose and eye highlights align; pen line has width and freehand error. The masks were traced against the clean original render at native resolution and enlarged eye crops, separately for each side.
