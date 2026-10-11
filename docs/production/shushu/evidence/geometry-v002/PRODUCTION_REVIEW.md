# Shushu Geometry v002 — Human Geometry Gate

2026-10-12 · Codex Executor · Blender 5.2.1 LTS. Production branch:
`codex/grimo-motion-zero-based-design-20261011`; input checkpoint
`1d52d842b4029bedf5f2a706e3176d1f4c02e8e9` (verified locally and remotely before work).

**Candidate delivered for Human inspection. Human Geometry acceptance: PENDING.
Actual Tripo Studio import / Texture / Auto Rig compatibility: UNKNOWN.**
**Focused technical checks: PASS within the demonstrated bounds.** The exact numerical verdict
is recorded in [focused-validation.json](focused-validation.json).
Technical checks establish the demonstrated bounds below; they do not establish visual acceptance.
No Tripo upload, processing, API, credits, trial, subscription, final rig, final motion library,
color, texture, fur, map baking or UV unwrap was performed.

## Review first

1. [Identity / donor / v001 comparison](review-01-identity.png): front, side, rear and three-quarter.
2. [Face comparison](review-02-face.png): neutral, half, complete and independent closure,
   tiny mouth opening, smile, surprise and combined controls.
3. [Support / contact comparison](review-03-support-contact.png): shallow rest, true seated,
   offering, holding, head turn, pressure and self-contact.

All 3D comparisons share one neutral clay and ordinary inspection lighting. The authority
PNGs are shown unchanged. All five primary authorities and all 17 reference-pack PNGs were
inspected; **the user's explicit acceptance of all 17 overrides stale pending labels in the pack**.
Reference poses guide appearance; their joint positions and reach are not treated as measured anatomy.

Human review should decide whether the head/chin profile, eye footprint and orientation,
tiny nose/mouth, cheeks, short limbs and seated silhouette retain Shushu's appeal. Eye blossoms,
iris details, markings and highlights are intentionally absent from this untextured geometry.
Standing versus seated daily Game Neutral remains undecided.

## Deliverables and ownership

| Artifact | Purpose |
|---|---|
| `assets/grimo/production/shushu/blender/shushu-geometry-v002.blend` | Neutral editable master; original normalized donor topology hidden separately; local keys and disposable development rig |
| `assets/grimo/production/shushu/tripo/geometry-v002/shushu-geometry-v002-tripo.fbx` | Static geometry-only interchange; preserves editable polygons/quads |
| Same directory, `shushu-geometry-v002-tripo.glb` | Static triangulated alternative; local import tested |
| `assets/grimo/production/shushu/blender/shushu-geometry-v002-proof.blend` | Separate 23-state sampled development proof, frames 1–177 at 24 fps; holding fixture independent |
| `assets/grimo/production/shushu/runtime-probes/shushu-geometry-v002-proof.glb` | Separate skin/morph/animation proof of the same candidate; donor, fixture and inspection objects excluded |

Paths above are repository-relative. Exact file hashes/sizes are in
[artifact-manifest.json](artifact-manifest.json). Candidate collections are `SHUSHU_GEOMETRY`,
`DEVELOPMENT_ONLY`, `INSPECTION_ONLY` and hidden `SOURCE_B_REFERENCE_ONLY`.
Both static files contain only 14 character meshes; no skeleton, animation, morph, donor,
fixture, UV, vertex color, material slot or texture. Blender uses Z up / −Y forward;
interchange axes and normalized source scale were verified by world-space reimport.

Head owns facial skin, ocular caps, nose/mouth and ear hierarchy; Root owns torso/support;
left/right paws and feet have separate development ownership. Future crown = Head,
Wear = ear/chest attachment, bouquet/Gift = paws, Food = mouth. No final accessory was made.

## Donor decisions

The actual original Candidate B FBX is the principal donor; **v001's visible face was not used**.
The untouched original FBX/GLB and 22 authority PNGs are verified against prior recorded hashes.
Eight donor anatomical modules are retained in silhouette, repaired separately for continuity
and surface sampling; the whole character was never destructively remeshed for export.

| Region | Decision and reason |
|---|---|
| Head / cheeks | B: retain donor mass/profile; remove inherited surface bands, locally smooth eye/mouth relief, round squared lower jaw corners |
| Eyes / lids | C locally within B head: donor-derived centers ±0.129, Z 0.660, elliptical radii 0.052/0.066, inward tilt 22°; head-connected annuli, small surface lid margins, independent shallow ocular caps |
| Nose / mouth | C locally: tiny neutral nose and two-lobed smile; small real aperture/minimal interior; no broad muzzle bowl |
| Torso / ears / short paws | B: donor modules, continuity repair; torso band smoothing; rounded ear cavities and short paw form retained |
| Feet / rump | B: real flat sole regions; shallow support keys reused; separate rump redistribution and whole short-leg forward rotation for sitting, with arc/ground correctives |

v001 supplied mesh/rig utilities, bounded support and engineering lessons. New face construction,
seated support and newly calibrated contact poses were tested against this candidate. Duplicate
donor surface strips are excluded from the candidate. The hidden donor retains its original topology.

## Measured capability and limits

See [focused-validation.json](focused-validation.json) for exact per-state measurements and
[build-manifest.json](build-manifest.json) for the proof frame/state map.

| Final check | Observed result |
|---|---|
| Static neutral surface round-trip | GLB 0; FBX worst error 1.64e−7 units |
| Separate deforming proof round-trip | All 23 samples PASS; worst error 8.30e−6, tolerance 2e−5 units |
| Seated support | Rump minimum Z 0.001127, 447 near-ground vertices; each foot minimum Z ≈0.001 |
| Source integrity | Original donor FBX/GLB + five primary PNGs + all 17 pack PNGs match prior hashes |

- **Face / Q01:** both fully closed eyes and smiling eyes expose 0/513 sampled cap vertices per side.
  Left-only/right-only closure leaves the opposite eye's exposed sample count unchanged.
  Half-blink, bounded cap gaze, mouth opening/surprise/smile and combined channels are preserved.
  Ocular caps recess under closing skin instead of inflating eyelid bowls. Cap gaze is a geometric
  control; illustrated gaze readability awaits later texturing and Human review.
- **Head / Q02:** bounded head turn/tilt and head response with self-contact/holding are proved.
  Cheek/belly pressure moves the protected eye/nose/mouth/lid modules by zero; release recovers exactly.
- **Support / Q03, Q08:** shallow rest lowers the body 0.065 units with foot soles fixed; torso
  volume remains unchanged. It remains feet-supported. True seated lowers the body 0.120 units,
  rotates short legs forward/outward, grounds the broad rump and projects feet forward.
  Seated torso volume is 1.0585× neutral; each seated leg retains its volume. Arc correction
  keeps intermediate leg volumes near 0.9946–1.0000× and ground correction maintains support
  through 41 sampled seat amplitudes. There is no human knee fold or limb length scaling.
- **Paws / Q04, Q13:** offering and both holding paws use rigid rotations of the original short
  volumes. Opposite paw displacement during one-paw offer is zero. Bounded holding uses a separate
  thin curved fixture positioned between the reachable paw surfaces; both ends have small positive
  contact gaps, with positive head/torso clearance. This does not prove arbitrary object sizes.
- **Self-contact:** actual lower-cheek and chest contact use calibrated rigid paw orientation,
  not arm extension. Distal free-paw samples have no penetrations beyond 0.001 units against head
  or torso in the demonstrated offering, holding, holding/head-response and grooming states.
  The original shoulder/body attachment junctions intentionally overlap: the free-paw test excludes
  the proximal 0.135-unit shoulder region. Neutral has four tested near-junction vertices inside torso
  by up to 0.00598 units. This is not a claim that every modular surface is globally intersection-free.
  External Human-hand contact and extreme shoulder angles remain unproved.
- **Food / Q09:** radius-0.003 entry probe has 27/27 clear head-aperture samples at the small
  open mouth. This establishes entry clearance only, not a consumption animation or arbitrary Food fit.
- **Composition / Q14, spatial export / Q15:** blink/mouth/cheek/head and holding/head-response
  are combined. FBX/GLB world-space neutral surfaces and 23 source/reimport proof samples are compared
  bidirectionally at tolerance 0.00002 units. FBX retains quads; GLB triangulates them.

The candidate has 50,738 vertices / 63,179 polygons / 33,028 quads across 14 meshes.
No edge has more than two incident faces. Eye and mouth apertures/caps have intentional open
boundaries; a watertight single solid or all-quad final retopology is not asserted. This is a
development geometry candidate, not a measured smartphone performance budget.

## Next gate / service boundary

**Next owner: Human — inspect the three boards and editable model for shape/identity acceptance.**
Essential bounded deformation is the technical evidence; no claim is made that all S01–S28
motions or all amplitudes are complete. Final skin weights, rig, motion tuning, attachment assets,
textures/UV, runtime performance and visual acceptance remain subsequent work.

The static exports are **candidates for a future Tripo import test**, not proof of Studio acceptance.
This task made no new external-service check. Previously recorded documented format support does
not verify this asset or the authenticated user's workflow/cost. Tripo may change topology, modules,
normals, UVs or rig behavior; Blender controls/IDs are not promised to survive it. If topology changes,
facial/control correspondence must be retested or rebuilt from this preserved master/proof.
Do not upload, consume trials/credits, unwrap, texture or rig from this review automatically.

## Reproduce

From repository root with Blender 5.2 and Python/Pillow available:

```text
blender -b -t 6 --python-exit-code 1 --python scripts/blender/build-shushu-geometry-v002.py -- --no-render
blender -b -t 6 --python-exit-code 1 --python scripts/blender/check-shushu-geometry-v002.py
blender -b -t 6 --python-exit-code 1 --python scripts/blender/render-shushu-geometry-v002.py
python scripts/blender/board-shushu-geometry-v002.py
```

`contact-targets.json` preserves the fitted orientation directions (they are not paw positions).
`fit-shushu-v002-contacts.py` can refit them if geometry changes. Proof Blender/GLB is disposable;
static FBX/GLB deliberately has none of these development controls.
