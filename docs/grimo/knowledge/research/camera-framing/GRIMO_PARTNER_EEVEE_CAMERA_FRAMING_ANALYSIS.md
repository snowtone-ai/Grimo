# Grimo — Partner Eevee Camera Framing Analysis

**Status:** Active reference evidence  
**Updated:** 2026-09-23  
**Role:** screen-space benchmark evidence; not a 3D camera/FOV authority

## Executive conclusion

Partner Eevee evidence indicates a front interaction presentation centered on
face readability and large screen presence. Carol must not blindly copy Eevee's
occupancy because Carol's fleece silhouette is wider and ordinary secondary
motion needs room.

Recommended Carol screen-space starting contract:

```text
target_character_height_ratio      = 0.76
acceptable_character_height_range  = 0.70–0.86

target_character_width_ratio       = 0.58
acceptable_character_width_range   = 0.50–0.76

target_face_center_y_ratio          = 0.40
acceptable_face_center_y_range      = 0.36–0.46

minimum_top_margin_ratio            = 0.08
minimum_bottom_margin_ratio         = 0.06
minimum_left_right_margin_ratio     = 0.10 per side
```

Preferred neutral margins:

```text
preferred_top_margin     ≈ 0.10–0.14
preferred_bottom_margin  ≈ 0.08–0.12
preferred_lr_margin      ≈ 0.18–0.22 per side
```

## Observed principles

- In ordinary full-body Partner Eevee framing, the face is near horizontal
  center; neutral face-center Y is roughly 0.40–0.46.
- Eevee may clip ear tips or approach the lower frame edge. Therefore its raw
  occupancy is not a universal safe-area rule.
- Ordinary neutral width occupancy observed in representative full-body footage
  is roughly 0.62–0.67; larger normal reactions reach roughly 0.75–0.78.
- The close high-five footage is a framing outlier and should not define neutral
  camera calibration.
- No clear camera follow/zoom change was required to explain the representative
  interaction intervals; much screen-space change can be explained by character
  root/pose/forward lean.
- Carol should keep the “large on-screen companion” philosophy while pulling
  back enough to protect her wider fleece/ears/tail secondary envelope.

## Usage

This document supplies evidence for a current Decision Question involving Hero
framing, motion extent, or runtime presentation. It must not independently force
a production phase or prevent a cheaper probe.

Exact source-frame measurements and older derivation notes are retained as
historical evidence in the archived camera benchmark.
