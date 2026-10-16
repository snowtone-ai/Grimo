# Grimo Partner Eevee camera-framing benchmark

## Record status

## Source and measurement method

The source corpus was three Partner Eevee MP4s: Video 01 (ordinary full-body
interaction), Video 02 (close/forward interaction), and Video 06 (ordinary
full-body interaction). All sources are 1920 × 1080 at 30 fps. Screen-space
character bounds, face-center position, frame margins, and interaction extent
were measured directly from video frames. Ratios are normalized to the frame.
Videos 01 and 06 are the primary ordinary benchmark; Video 02 is secondary and
classified as a close-framing outlier.

## Observed benchmark statistics

Primary ordinary neutral (Videos 01 and 06): character width ratio 0.617–0.672
(median approximately 0.645); face center X approximately 0.50; face center Y
0.398–0.463 (median approximately 0.431).

Secondary close/forward outlier (Video 02): visible width ratio 0.820–0.924,
height ratio 0.954–0.999, and face center Y 0.546–0.574, with multiple
frame-edge clips. It is not part of the default-camera median.

## Camera stability

- **Observed:** background landmarks remain effectively fixed; clean comparison
  regions change by approximately 0–1 px.
- **Strong inference:** the Partner Eevee interaction camera is effectively
  fixed, and most screen-space movement comes from character animation/root
  movement.
- **Unknown:** exact internal camera-controller implementation.

The inference must not be promoted into an unsupported engine-level fact.

## Calibration boundary and planned procedure

The benchmark defines screen-space outcomes, not 3D camera values. FOV,
distance, camera height, target height, focal length, orthographic scale,
world-space dimensions, and near/far clipping planes remain intentionally
unknown. Later calibration will: build the authorized neutral blockout; render
from a provisional front camera; measure rendered bbox, face center, and
margins; adjust toward width ≈ 0.58, height ≈ 0.76, face Y ≈ 0.40; test ordinary
motion envelopes; review motion/root amplitude before changing a global camera;
and submit evidence renders/captures for Human Gate review.

This record authorizes no modeling, rigging, animation, export, or runtime
implementation.
