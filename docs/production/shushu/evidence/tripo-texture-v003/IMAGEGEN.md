# Built-in image_gen local repair material

Tool: built-in `image_gen` / `imagegen` skill. No CLI/API fallback, Tripo upload, or paid external request.

Image 1 edit target: `renders/before-front.png`, unretouched original GLB render.
Image 2 identity reference: `assets/grimo/source/shushu/tripo-generation-pose/shushu_bodyonly_front.png`.

Returned 1254×1254 image saved as `textures/imagegen-local-repair-projection.png`. This image is a repair material, **not a render of the final candidate**. Only mapped mouth ghost texels and 2 texels of adjacent atlas padding were transferred into the final candidate. Eye edit trials were rejected.

## Exact prompt

Use case: precise-object-edit. Asset type: local texture-repair projection, 1024x1024. Edit target Image 1 is an exact front orthographic render of an existing Shushu model. Supporting Image 2 is approved identity reference ONLY; do not copy its geometry or camera. Change only the faint duplicate/ghost contours beside the existing eyes and mouth in Image 1. At the mouth, retain the strong central curved smile and central peach tongue exactly; remove the pale duplicated smile hooks and pale extra tongue-shaped arcs immediately to the left and right of that main mouth, replacing them with matching warm cream fur. Around both eyes, remove only thin stray secondary gray contours and offset pale duplicate edges outside the main dark eye rim. Preserve the strong dark rims completely, the pink eye surrounds, flower pupils, all highlights, cheeks, central smile, tongue, nose, ears, silhouette, pose, colors, fur details and background. Pixel-aligned composition and 1024 square output, no movement, crop, relighting, rescaling, reshaping, global smoothing, new lines, or global texture redesign. Repair only those small ghost areas naturally with neighboring cream/pink texture.
