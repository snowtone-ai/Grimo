# Carol Reference Measurements

This artifact records a measurement pass over the six approved Carol production plates. The canonical sheet is included as a supplementary identity and cluster reference. Individual plates are the geometry authority.

## Coordinate contract

Pixel coordinates use native PNG coordinates with origin at the upper-left, x increasing rightward and y increasing downward. Each point also has a `normalized` coordinate relative to that plate's visible Carol silhouette bbox, not the transparent or white canvas. `null` means the landmark is not visible or cannot be separated reliably in that view. Values are estimates from an illustrated reference and include pixel uncertainty.

The face, eye, ear, nose, mouth, hoof, moon, star, and major cluster annotations are art-directed pixel landmarks, hand-annotated against the native source with a nominal 6 px uncertainty. The visible silhouette bbox and the Top 100-sample width profile are image-derived. This distinction is intentional: it keeps uncertain anatomy visible instead of manufacturing false precision.

## Per-view summary

| View | Source | Canvas | Visible bbox (x0,y0 → x1,y1) | Bbox W×H | Segmentation |
|---|---|---:|---|---:|---|
| `front` | `assets/grimo/source/carol/approved-3d/carol-front-ortho-transparent.png` | 1254×1254 | (96,137) → (1176,1103) | 1081×967 | alpha |
| `side` | `assets/grimo/source/carol/approved-3d/carol-side-ortho-transparent.png` | 1448×1086 | (89,106) → (1373,990) | 1285×885 | alpha |
| `back` | `assets/grimo/source/carol/approved-3d/carol-back-ortho-transparent.png` | 1254×1254 | (55,141) → (1198,1111) | 1144×971 | alpha |
| `top` | `assets/grimo/source/carol/approved-3d/carol-top-plan-transparent.png` | 1254×1254 | (192,36) → (1061,1245) | 870×1210 | alpha |
| `three_quarter_left` | `assets/grimo/source/carol/approved-3d/carol-front-3q-left.png` | 1254×1254 | (51,133) → (1217,1126) | 1167×994 | white_background_flood_fill_provisional |
| `three_quarter_right` | `assets/grimo/source/carol/approved-3d/carol-front-3q-right.png` | 1254×1254 | (45,150) → (1214,1116) | 1170×967 | white_background_flood_fill_provisional |

## Landmark and ratio notes

The JSON contains every point in pixel and bbox-normalized form. The following ratios are the high-value constraints for geometry work:

- `face_width / overall_width`, `face_height / overall_height`: face plate must remain a volumetric head while preserving the visible front proportion.
- `eye_spacing / face_width`, `eye_width / face_width`, `eye_height / face_height`: identity-critical face ratios.
- `ear_length / overall_width`, root and tip positions: ear depth and droop must be solved with side and 3Q views.
- `body_length / body_height`: use Side and Top bboxes together; do not infer hidden depth from a single plate.
- Top `width_px` profile at 100 evenly spaced longitudinal samples: the center minimum is the explicit indentation constraint.

## Top width profile

`views.top.top_width_profile_100` stores `s`, source y, visible width, centerline, and edge uncertainty. A missing sample is represented by null; it should be interpolated only for comparison, never treated as an observed zero.

## Cross-view conflicts and limitations

- The transparent orthographic plates and white-background 3Q plates have different framing and are generated illustrations, not a registered turntable. Bbox-normalized ratios are comparable; raw pixels are not.
- The front has both eyes, while Side exposes only one eye. Back exposes no face landmarks. Those entries are null by design.
- Motif placements vary by view because a single physical ornament projects differently. Moon and star annotations are visibility landmarks, not a claim that each depiction is a separate object.
- The white background can merge with very pale fleece on the 3Q plates. The script reports the conservative chromatic silhouette and records the limitation.
- Canonical sheet components are supplementary; it is not used to overwrite any six-view measurement.

## Reproducibility

Run:

```text
python scripts/qa/measure-carol-references.py
```

The script uses Pillow and NumPy for shared image decoding and segmentation and records source SHA-256 hashes. Do not edit the generated JSON manually; revise the annotated pixel table in the script and rerun it when a Human Gate changes a landmark.
