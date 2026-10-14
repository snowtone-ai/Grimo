# Grimo Partner Eevee camera-framing benchmark

## Record status

This is a condensed production evidence record derived from a separate full
source-video analysis. The full external analysis was not imported into the
repository. It captures the measurements and production decisions needed by
Carol; it does not claim to recover the source application's internal camera
parameters.

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

Ordinary maximum interaction: width ratio 0.745–0.779 (median approximately
0.762) and height ratio 0.897–0.962 (median approximately 0.930). Eevee often
clips its ears at the top edge. Carol must not copy that clipping; the reusable
principle is intimate presence with Carol-specific safe margins.

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

## Carol translation and screen-space contract

Carol's fleece is wider, her face is smaller relative to the body, her ears
spread laterally, and her rounded rear tuft/tail needs room for subordinate
expressive motion. Visible canonical identity remains the priority if it
conflicts with a numeric target.

| Measure | Target | Acceptable range / minimum |
|---|---:|---:|
| Character height ratio | 0.76 | 0.70–0.86 |
| Character width ratio | 0.58 | 0.50–0.76 |
| Face center X ratio | 0.50 | — |
| Face center Y ratio | 0.40 | 0.36–0.46 |
| Top margin ratio | — | minimum 0.08 |
| Bottom margin ratio | — | minimum 0.06 |
| Left/right margin ratio | — | minimum 0.10 per side |

Preferred neutral: width 0.56–0.60, height 0.73–0.79, face center X
approximately 0.50, and face center Y approximately 0.40. Preferred neutral
side margins are approximately 0.18–0.22 per side when practical; hard minimum
is 0.10 per side.

The ordinary interaction safe envelope is normalized `x = 0.10–0.90` and
`y = 0.08–0.94`. A future explicitly classified close state may use width
0.80–0.90+, height 0.90–1.00, and face center Y 0.52–0.58, with controlled
clipping, but it must not redefine the default companion camera.

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
