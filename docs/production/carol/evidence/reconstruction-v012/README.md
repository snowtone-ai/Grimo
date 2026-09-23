# Carol v012 — bounded Phase A local reconstruction, visual gate failed

**Technical static gate: PASS. Executor visual precheck: FAIL.** The selected
**v012-T2-O2 is diagnostic only; it is not promoted.** Human Geometry Gate is
**NOT_REVIEW_READY**. Motion clearance was not run because the static visual
precheck failed. Phase B/C remain not started.

Source branch: `codex/carol-final-reconstruction-v011` at exact commit
`e95654fae3dc8434cbe651e7d6467aafe59dc667`. The source blend and four
locked reference hashes were verified. The v011 blend remains byte-identical.
Working branch: `codex/carol-final-reconstruction-v012`.

## Bounded probes

| Probe | Technical gate | Visual finding |
| --- | --- | --- |
| T1, `.035 H` maximum X compression | PASS | Long Side under-jaw plane remains. |
| T2, `.050 H` maximum X compression | PASS | Shorter than T1, but the Side oblique turn remains. |
| O1, independent anatomical-axis eye cap | PASS | `.128 H` Side whole-cap span and `1.080` near-eye 3Q ratio, but eye reads as protruding. |
| O2, local socket seat and matching lid rings | PASS | Selected `.075 H` eye depth gives `.1286 H` Side whole-cap span and `1.137` near-eye 3Q ratio, but exposed Side socket/eye remains. |

O2 shifts the local orbital chassis surface by at most `.015 H` in X. The
chassis Y/Z delta is exactly zero, as is the `.575 H` and rearward coordinate
delta. Front eye width/height stay `.137 × .149 H` at centers `±.162 H`.
The whole-cap metrics measure geometry, not visible occlusion or visual fit.
The numeric eye targets passing does not override the failed Side render.

The v011 face connectivity is retained exactly: 533 vertices, 1,062 edges,
531 quads, one component, zero nonmanifold edges, Euler 2, zero degenerate
faces. Control/evaluated disjoint intersections are **0/0**. The inherited
adjacent-triangle audit tested 5,903/93,515 pairs with zero improper contacts.
Frozen objects, including cameras, lights, ears, limbs, hooves, tail, materials
and reference registration, match v011 after save/reload. No Boolean, remesh,
hidden shell or view-dependent geometry was used.

## Evidence and decision

`diagnostic-sheet.png` places the candidate beside fixed-registration locked
Skin Front/Side references, 50% overlays, and derived 3Q/Top views. Individual
renders, overlays and face crops are included. Renders use inherited 480-square
16-sample Cycles settings. `measurements.json` and `validation.json` record
the numerical and static checks and the failed visual disposition.

The Front eye lock and the improved v011 3Q proportion survive. The rounded
posterolateral Top shoulders remain; anterior taper is not clearly improved.
The Side still shows a long oblique lower-cheek/head-to-chest surface rather
than the locked very short rounded turn. The Side eye is wider numerically but
looks like a protruding cap instead of an integrated eye. The Front under-chin
transition is also too sharp. These are visual failures, so motion clearance
and the Human Geometry Gate are not eligible.

Asset: `assets/grimo/production/carol/blender/carol-v012.blend`, saved in a
neutral pose with **DIAGNOSTIC ONLY — NOT PROMOTED** status. No fleece,
production rig, animation, GLB or runtime work was performed.

Reproduction: run `blender --background --python scripts/blender/build-carol-v012.py
-- --transition 2 --ocular 2 --render front,side,3q,top`, then
`--finalize-failure`, then `python scripts/blender/carol-v012-evidence.py`.
Further shape work requires a new bounded handoff.
