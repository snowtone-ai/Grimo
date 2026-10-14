# Shushu fur seam local material

Built-in `image_gen` was used once to create local color material. The input was [`imagegen-source-panels.png`](imagegen-source-panels.png), a 2×2 board of v002 saved-GLB left profile, right profile, crown and approved Body-only front; [`human-annotation.png`](human-annotation.png) showed the Human's black tracing. The output was [`imagegen-local-material.png`](imagegen-local-material.png), 1254×1254. It is repair material, **not** model-review evidence.

Prompt intent supplied to the tool: edit the first image as a precise-object edit, keep the 2×2 panel alignment and Shushu's identity, and remove only the narrow pale pink/white fur bands that read as a stitched seam from each ear toward the shoulder and across the crown. Blend into neighboring warm cream and soft fur shading. Preserve ears, eye and mouth, pink eye surrounds, blush, silhouette, background and all other detail. Use the second image only to locate the traced seam; do not reproduce its black line. No global blur or new objects.

The generated panels were projected to the existing Head UV only through the recorded local masks. Color probes match surrounding cream. The candidate's actual appearance must be judged from the independently reloaded GLB renders.
