# Carol face / ear production v003

**READY_FOR_HUMAN_FACE_EAR_REVIEW. Final candidate: Face F2 + exact source Ear v002.** Human review remains required; no Human identity/cuteness/geometry PASS or authority promotion.

- Branch: `codex/carol-face-ear-production-v003`.
- Exact fetched source: `origin/codex/setup-codegraph-mcp`, `880b35506c0b085fdbb4081c1de6c3f9bdc4e58a`.
- Source Ear v002 LFS SHA-256: `bbff75858779a5b284e14c63c6f1bc3cfc206e1c6467a84a55eab64fa7c34fd7`.
- Candidate: `assets/grimo/production/carol/blender/carol-face-ear-production-v003.blend`.
- Final commit: resolve `git log -1 --format=%H -- assets/grimo/production/carol/blender/carol-face-ear-production-v003.blend`. The executor report records the exact pushed SHA. A tracked record cannot embed its own commit hash without changing that hash.

| Gate | Result | Meaning |
| --- | --- | --- |
| Authority preflight | PASS | Six image entries, including Ear Module, and canonical Git LF document verified |
| Face executor visual precheck | PASS | F2 provides partial local recovery; source Front/3Q preserved in executor comparison |
| Ear executor visual precheck | FAIL | E1/E2 do not solve Side / Top / cup together; source retained |
| Technical validation | PASS | Selected F2 + source ears; reload, topology, freeze, seating and bends |
| Skin Side registration probe | PROBE_INVALID | Inherited registration does not align current approved face landmarks |

## Human evidence

- [Combined review](human-review.png).
- [Face Side, authorities, fixed Normal overlays and 3Q](face-side-review.png).
- [Front preservation](face-front-preservation.png).
- [Ear E1/E2 stop evidence](ear-attempts-not-promoted.png).
- [Retained ears against four-view authority](ear-isolated-retained.png).
- [Attached candidate / non-final fleece diagnostic](candidate-attached.png).
- [Retained-ear bend checks](ear-deformation-check.png).
- [Invalid inherited Skin Side registration](skin-registration-diagnostic.png).

## Face F2

Source chassis: 533 vertices, 1,062 edges, 531 quads, one closed component, Euler 2. v009 at `5de182d5eab04f84e3fa46926a953efa3527d679` supplied only recorded Side projection evidence and the surface-sampling implementation lesson. No historical mesh was loaded or transplanted; its lower-cheek shelf / under-jaw architecture was not reused.

F1 moved six FACE controls by at most 0.025 H along negative X. Initial renders and chassis checks looked safe, but the subsequent evaluated-surface seating check found **7 newly covered eye controls and 6 newly covered lid controls per side**. F1 is rejected. Eye mesh equality alone was insufficient.

F2 narrows the same hypothesis to sagittal FACE vertices **38 and 39**, maximum **0.020 H**. All other controls, all Y/Z and all connectivity remain exact. The NOSE rigid X shift uses the evaluated surface delta at its original center; mouth and philtrum points preserve their individual source surface relief. Existing dimensions, thickness, materials and feature Y/Z remain unchanged.

Nose advance: **0.012419 H**; peak sampled local surface advance: about **0.01267 H** at Z=.365. The Side has a small rounded projection without a long snout in executor comparison. F2 has **zero newly covered eye or eyelid controls**. Eye clearance remains positive; lids retain the source set of embedded controls. No full blink/gaze or Human identity acceptance is implied.

The inherited Normal Side nose discrepancy is approximately 0.04–0.05 H. This is partial recovery, not authority matching: closing the whole gap with this sparse local field would exceed the 0.035-H control limit. No F3 or escalation. Existing simplified muzzle and source under-jaw remain limitations. Subdivision spreads small movement beyond the two controls (midline .00054 H at Z=.30 and .00219 H at Z=.45); not every evaluated head point is identical. Chest, neck, cranium and cheek/jaw controls are unchanged.

## EAR_V003_NOT_PROMOTED

Both E attempts preserved the 12 × 16 cage, root placement, first three stations, endpoint, shell/material region, mirror and provisional bend architecture. Only stations .085–.345 changed; perimeter coefficients, topology and materials did not.

E1 moved breadth toward the middle but excessive offset produced an unwanted wavy Top and left a heavy Side. E2 reduced offset and coordinated middle-to-distal breadth. Side narrowed, but Top developed a thin distal transition instead of the authority's broad middle flowing into a full rounded tip. Cup containment remained weak. E2 was spent on silhouette correction; no cup-only third attempt occurred.

**STOP LOCAL REPAIR: Ear architecture review required.** This is the observed limit of these two edits, not proof the whole architecture must be replaced. Neither is promoted. Final EAR_L/R and controls are exactly source v002. No final Ear improvement is claimed.

## Validation / integrity

[validation.json](validation.json) and [measurements.json](measurements.json) record checks, F2 deltas, rejected F1 seating and E1/E2 station values.

- Changed final objects: `CENTRAL_CHASSIS`, `NOSE`, `MOUTH_closed`, `PHILTRUM`. **37 others unchanged** after reload, including ears, eyes/lids, saved cameras, lights and reference registration.
- Finite closed outward chassis; unchanged connectivity; zero detected nonadjacent evaluated triangle intersections. Feature Y/Z delta zero; source-relief preservation error below 1e-6 H.
- Retained ears: 192 controls each, closed shells, outward normals, exact neutral mirror, pink on the same mesh. Neutral, lift +12°, droop −14°, attention +12° turn / +5° lift: zero detected nonadjacent intersections. Roots seated; root-control motion **2.98e-8 H**. Volume ratios **0.980356–1.015318**. Saved controls zero.
- All in-use material properties/nodes/links unchanged. Transient Blender session IDs excluded; two unreferenced historical v001 material datablocks are automatically omitted by Blender serialization. No used material or object removed.
- Existing non-final fleece was loaded only after save, is absent from the candidate and still substantially occludes the ears; future clearance unresolved.
- **pre-existing authority manifest hash drift repaired; no authority content or authority ordering changed.** Only the document hash was synchronized to `656C1C512017FC548D7F5DFABF66085FD1085A95BD739BBEFB7922F568D3B048`, using exact source Git LF bytes. Approved images and the geometry document are unchanged.
- Source/candidate cameras and scale shared; authority crops displayed uniformly. Normal overlays use inherited h=916 / ground=998 / origin=144 without fitting. The invalid Skin Side registration is shown, not corrected or used as geometry truth.

## Reproduction / handoff

With source LFS assets present, run Blender 5.2 background with `--python scripts/blender/build-carol-face-ear-production-v003.py -- --stage inspect`, then `face --attempt 1`, `face --attempt 2`, `ear --attempt 1`, `ear --attempt 2`, and `final --ear-selected source`. Run Python on `scripts/blender/compose-carol-face-ear-evidence-v003.py`. Intermediate blends/renders stay in OS temp `carol-face-ear-v003`. Passing retained-ear checks/renders may be reused only for the identical hashed source ears.

Next: **HUMAN — Face F2 review**, then **ChatGPT Planner — Ear architecture review / inherited Skin registration review**. No further local repair, rigging, animation, runtime work or authority promotion in this task.
