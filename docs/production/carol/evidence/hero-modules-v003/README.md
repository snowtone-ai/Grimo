# Carol hero modules v003 — local executor diagnostic

**Disposition: STALLED_PARAMETERIZATION. Executor visual precheck: REJECTED. Human Geometry Gate: NOT SUBMITTED.** The [review page](review.html) exposes the remaining differences; it is a diagnostic artifact rather than an approval request.

## Local provenance

- Started on `codex/carol-hero-modules-v002` at `c85b9ab202c5a9a9c663f246300b225ca47b617a`; branched locally to `codex/carol-hero-modules-v003` without discarding the uncommitted parameter file.
- Local parameter file SHA-256: `b18cbbca19256b824ab62dcf713d0ecedde8b98b586223587e28d4d375f2a9fa`.
- v002 starting asset SHA-256: `5731cc9064fec4907e8ed8c95ce8b9ff0b0d097159328588850645ce4394744a`.
- v003 asset SHA-256: `fb9b793d7443e942f0ad118df99bb8703e056ea806815a32f2897581fb33b299`.
- Ear authority SHA-256: `ca348f895689aefeea1844b12d7fb5a4af953e114859a552b6328311295e8563`; Hoof authority SHA-256: `00412f74458450d785b262403192979309e2b6d4ee5f33c6b1445cb36c4dbb7a`.

## Root cause and correction

The v002 ear's `.180 H` drop over `.382 H` lateral span produced approximately `25.2°`, outside the `18°` intent. The v003 centerline is `18.0°` with independent lateral, fore/aft, drop-easing, section breadth, upper/lower cushion, taper, and bowl controls. It remains one closed spatial ear per side.

The v002 hoof comparison under-reported quality in two ways: the Top candidate was not rotated into the authority sheet's presentation axis, and a single shading pixel inflated the Side bounding box. Those comparison defects are corrected. They do not explain the whole mismatch. The v003 hoof remains one closed mass with three toe lobes and two shallow clefts. Its exposed Top footprint still does not reproduce the approved contour. The pale helper stub in the authority sheet was not copied as brown geometry; Top comparison isolates the hoof, while integrated renders show the unchanged actual limb.

The v011 eye used about `.040 H` relief. v003 uses a `.013 H` central optical cap and socket-owned lid opening. An initial recessed edge shrank the visible Front aperture; the post-reload raycast found `.1215 × .1315 H`, so that result was rejected and corrected. Final measured visible Front aperture is `.1370 × .1485 H`, centered at `±.16175 H`. The Side eye no longer extends beyond the anterior head silhouette in the neutral pose. This is a static neutral correction; a production gaze or blink system was not built.

## Final measurements

| System | Front IoU | Side IoU | Top IoU | 3Q IoU |
|---|---:|---:|---:|---:|
| Ear | 0.8297 | 0.7553 | 0.7424 | 0.6970 |
| Hoof | 0.9376 | 0.9037 | 0.6083 | 0.7929 |

IoU is normalized shape-only silhouette overlap. The sheets have no absolute pixel-to-H registration. Front/Side/Top are fitting authorities and 3Q is validation. The metrics and overlays both show unresolved Ear Side/Top and Hoof Top errors. No Human Geometry PASS is claimed.

- Ear front centerline angle: `18.0°`.
- Hoof actual width: `.219 H`; nominal visible crown: `.111 H`; full mesh height including hidden overlap: `.146 H`.
- Eye visible Front aperture: `.1370 × .1485 H`; central relief `.013 H`; neutral Side silhouette bulge `0 H` by the anterior head outline diagnostic.
- Changed objects: `EAR_L`, `EAR_R`, four `HOOF_*`, `EYE_L`, `EYE_R`, `EYELID_L`, `EYELID_R`.
- Frozen objects: 31 of 31 equal after save/reload by world matrix, mesh digest, counts, material slots, and bounds. `CENTRAL_CHASSIS` remained frozen; socket seating was achieved in the eye/lid surfaces.
- All six changed Ear/Hoof meshes are one connected closed component with zero nonmanifold/boundary edges. The four hooves have no detached toe components.

## Convergence and stop

The grouped fitting history is in [fit-history.json](fit-history.json). The final ear basis reached its 12-round ceiling, with a weak Side view still gaining but far below the `0.90` primary-view goal. Architecture diagnosis: the swept elliptical section cannot reproduce the authority's independently changing upper/lower and fore/aft contours across all views. A further small parameter nudge would repeat the trade-off. The hoof's Top silhouette stalled around `0.62` in the local projector despite fitting width, depth, heel, and toe groups. The final rendered Hoof Top IoU is `0.6083`.

The task's post-convergence temporary motion-exposure check was not run because the static module fit did not converge. The neutral eye was checked in Front, Side, and both derived 3Q views. No unrelated v011 jaw/chest defect was revised.

## Browser review

Opened `review.html` in a headed local Playwright browser through `http://127.0.0.1:8765/`. The page title and all five major sections appeared, and all 32 review images decoded with no broken links. The initial favicon request returned 404; an inline empty favicon was added, and the page reloaded without a new console error. The executor inspected the actual Ear triptych in the browser and rejected the visible fit.
