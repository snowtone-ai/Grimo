# Carol camera contract

## Status

The screen-space framing contract is resolved for initial production. The
underlying 3D camera parameters remain intentionally unresolved until the
authorized Carol blockout is available. This contract does not authorize
modeling or runtime implementation.

## Authority / evidence

- Visible identity: `assets/grimo/source/carol/carol-Identity-canonical.png`.
- Hidden/off-axis geometry reference: `assets/grimo/source/carol/approved-3d/`.
- Current framing evidence: `docs/grimo/knowledge/research/camera-framing/GRIMO_PARTNER_EEVEE_CAMERA_FRAMING_ANALYSIS.md`.
- The older condensed benchmark is historical and superseded for routing.

## Front-facing invariant

The camera remains front-facing as the primary Hero interaction reference. **This does not
make Carol flat or forbid approved off-axis motion.** Off-axis fidelity is
required only to the degree approved motion exposes it; uniform 360° Hero
quality is not a target. Camera orbit is not required and must not repair weak
core interaction acting.

## Partner Eevee benchmark

Videos 01 and 06 are the primary ordinary full-body benchmark. Neutral width is
0.617–0.672 (median approximately 0.645), neutral face center Y is 0.398–0.463
(median approximately 0.431), and face center X is approximately 0.50. Ordinary
maximum interaction reaches width 0.745–0.779 (median approximately 0.762) and
height 0.897–0.962 (median approximately 0.930). Video 02 is a rare close
outlier, not the default median: width 0.820–0.924, height 0.954–0.999, and
face center Y 0.546–0.574, with controlled edge clipping.

## Carol screen-space contract

| Measure | Target | Acceptable range / minimum |
|---|---:|---:|
| Character height ratio | 0.76 | 0.70–0.86 |
| Character width ratio | 0.58 | 0.50–0.76 |
| Face center X ratio | 0.50 | — |
| Face center Y ratio | 0.40 | 0.36–0.46 |
| Top margin ratio | — | minimum 0.08 |
| Bottom margin ratio | — | minimum 0.06 |
| Left/right margin ratio | — | minimum 0.10 per side |

## Neutral target / safe envelope

Preferred neutral: width 0.56–0.60, height 0.73–0.79, face X approximately
0.50, and face Y approximately 0.40. Preferred neutral side margins are
approximately 0.18–0.22 per side when practical; hard minimum is 0.10 per side.
Ordinary built-in interaction must remain in normalized safe area
`x = 0.10–0.90` and `y = 0.08–0.94`.

Visible identity always wins over mechanically hitting a number. Report a
conflict for Human Gate review rather than distorting Carol.

## Close / special framing

The Human-defined **Close Window-Lean State** is a future separate interaction:
Carol approaches, shifts weight rearward, raises the forebody, and places the
front hooves near/on the bottom boundary of the 3D viewport. This is a character
pose and proximity concept, not permission to flatten geometry or orbit the
camera. Neither this state nor Full Companion runtime behavior is implemented
by Blockout v002. Exact portrait framing remains deferred.

An intentionally close interaction may have width 0.80–0.90+, height 0.90–1.00,
and face center Y 0.52–0.58, with controlled clipping. It must be explicitly
classified as a separate special state and must not redefine the default camera.

## Camera stability

Observed footage keeps background landmarks effectively fixed (about 0–1 px in
clean comparison regions). Strong inference is that the interaction camera is
effectively fixed and character animation/root movement supplies most
screen-space motion. The exact internal camera controller is unknown; this
inference is not an engine-level fact.

## 3D calibration boundary

The approved production contract is screen-space. FOV, distance, camera height,
target height, focal length, orthographic scale, world-space dimensions, and
near/far clipping planes are blockout calibration variables, not values to
reverse-engineer from Eevee footage. No numeric 3D values are assigned here.

## Aspect-ratio boundary and Blockout v001 evidence

The numeric contract above originates from 16:9 benchmark footage. It must not
be applied as simultaneous width/height requirements to the 412x915 phone
viewport. Blockout v001 therefore separates evidence into 16:9 benchmark
calibration at 1920x1080 and 412x915 portrait diagnostic renders. The portrait
renders record bbox, face center, clipping and readability only; they do not
finalize runtime portrait framing.

The provisional camera values are calibrated against the actual Blockout v001,
not inferred from Eevee footage. Perspective is currently the standard evidence
alias (`Carol_Camera_front`), while Orthographic remains a first-class
comparison candidate. Neither projection is production-final. Exact measured
values are versioned in `evidence/blockout-v001/framing-metrics.json`.

## Acceptance procedure

Camera evidence is selected by the current Decision Question rather than a
fixed geometry phase. For a Hero-camera or runtime framing probe:

1. use the current Carol candidate/prototype appropriate to that probe;
2. render/capture from the front Hero interaction camera;
3. measure bbox, face center, clipping, and motion envelope only as relevant;
4. compare against the benchmark envelope without distorting Carol identity;
5. include representative motion when framing under motion is the risk;
6. treat numerical metrics as evidence, not final perceptual acceptance;
7. submit user-visible evidence to Human when identity/appeal/naturalness must
   be judged.

This contract does not require a static Geometry Gate before motion/runtime
framing experiments.

## Unknowns

Projection choice, FOV, distance, camera height, target height, focal length,
orthographic scale, world-space Carol dimensions, and clipping planes remain
unresolved until calibration against the actual blockout.
