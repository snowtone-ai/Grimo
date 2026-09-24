# Carol hero ear and hoof modules v002 — executor evidence

Source: exact `carol-v011.blend` SHA-256
`568fb4378b6ca3093ba5134d8d082f37a6723c9d5b5cf0b491a7c8e5f757aed3`.
The two approved 1254 × 1254 PNGs were moved byte-for-byte into
`assets/grimo/source/carol/approved-3d/modules/`; paths and SHA-256 values
are in `validation.json` and the [review page](review.html).

The builder replaced only `EAR_L`, `EAR_R`, `HOOF_FORE_L`, `HOOF_FORE_R`,
`HOOF_HIND_L`, and `HOOF_HIND_R`. The other **35 objects** matched the source
by name, world transform, vertex/face count, mesh SHA-256, material slots, and
world bounds before work and after candidate save/reload. This includes the
v011 face, eyes, eyelids, nose, torso, tail, limbs, and camera objects.

## Bounded refinement record

1. Initial closed ear shell / single-mass hoof construction and four-view
   renders showed a narrow pink side region and blunt ear tip.
2. Correction 1 refined the ear material region and tip profile; the view
   comparison then exposed a stepped color boundary and thin root cushion.
3. Correction 2 made the inset boundaries continuous vertex strips and showed
   the exposed hoof against the frozen limb.
4. Correction 3 broadened the ear cushion and adjusted the hoof front
   projection and upper contour. This is the final bounded correction.

All eight view-specific reference/candidate/overlay comparisons and four
integrated Carol renders are available in `review.html`. `fit-metrics.json`
reports normalized **shape-only** silhouette IoU, not absolute world-space
registration. The approved sheets have no pixel-to-H registration, and their
3Q panels are validation rather than an independent fitting authority.
The Front/Side/Top 0.990 and 3Q 0.975 targets were **not met**. Final IoU:

| Module | Front | Side | Top | 3Q |
|---|---:|---:|---:|---:|
| Ear | 0.7080 | 0.5857 | 0.6739 | 0.6888 |
| Hoof | 0.8598 | 0.6696 | 0.5799 | 0.7674 |

The remaining mismatch is most visible in the ear Side/Top proportions and
hoof Side/Top contour. The ear centerline drop is approximately 25.2° versus
the contract's approximately 18° front-read intent. The hoof width is exactly
0.219 H, and support centers remain at Front X 0.390 H and Hind X 0.920 H.
The full hoof mesh rises to 0.150 H for hidden overlap; the exposed color
boundary and nominal 0.111 H visible crown need Human review in context.

**Technical Module Gate: ATTENTION. Executor Visual Precheck: ATTENTION.
Human Geometry Gate: PENDING HUMAN REVIEW.** The topology and freeze checks
pass, but the quantified fit targets do not. A further shape correction would
choose among conflicting visible proportions without a stronger approved
registration; the review page presents the decision-relevant evidence.
