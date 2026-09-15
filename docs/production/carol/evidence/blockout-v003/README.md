# Carol Structural Blockout v003 — Human Gate packet

2026-09-16. **HUMAN GATE: PENDING.** Branch: `codex/carol-structural-blockout-v003`.
Baseline: `9ba1a188269e09ac4678a21254bd25ac8a1ffb59` (v002).

## Result

v003 transfers the recovered historical continuous-relief principle onto the
full-depth v002 fleece. It opens the actual v002 file and retains its chassis,
face, eyes, ears, four independent supports/hooves, rear tuft and their world
transforms. Their vertex hashes and matrices are checked before and after the
change and again after saving/reopening. The fleece and motif depths change.

The result is a **structural candidate**, not an assertion that historical
beauty quality has been recovered. The inherited round masses are less isolated,
the crown trench is closed, and the front collar remains a continuous volume.
Large smooth side/rear regions and a somewhat heavy front canopy remain visible.
Human judgment is needed on whether that tradeoff improves Carol's cloud identity.

## Review first

- [Review board: canonical, v002, v003 and all seven views](review-board.png)
- [Clay comparison under the same diagnostic lighting](clay-comparison.png)
- [Actual iteration images, including rejected candidates](iteration-board.png)
- [Front at 320 pixels](front-at-320.png): static scale check, **not runtime QA**
- [Historical screenshot](historical-relief-screenshot.png): surviving predecessor
  evidence, **not a verified screenshot of the exact final accepted revision**

Final individual captures are 1400 × 1190 RGBA PNGs: [front perspective](carol-v003-front-perspective.png),
[front orthographic](carol-v003-front-orthographic.png), [three-quarter](carol-v003-three-quarter.png),
[side](carol-v003-side.png), [back](carol-v003-back.png), [silhouette](carol-v003-silhouette.png),
[clay](carol-v003-clay.png).
v002 and v003 use the same cameras, resolution, light placement/energy and
diagnostic materials. Canonical artwork is independently fit on the board;
it is posed and painted, and is not a calibrated neutral turnaround.

## Historical investigation: what was actually recoverable

The old `snowtone-ai/grimoire` repository is the separate local `task-plant`
checkout. Its `feat/carol-3d` and `feat/carol-reference-rebuild` branches point
to `0c067b8`, without the later Carol implementation committed. Local refs,
remote heads, reflogs, unreachable commit subjects and surviving output files
were examined. No exact accepted `.blend` or `.glb` was recovered there.

The relevant local Codex task is `01a0874f-e5ba-7753-92bc-1298900208e4`.
Its user message at **2026-09-10T05:26:23.454Z** says:

> よし、完全合格です。リポジトリに記録して、セッション終了します。余計な動作は禁止です。

The subsequent assistant record says the acceptance was recorded in `tasks.md`
and that no commit/push/publication occurred. That is historical evidence only;
the old instruction to end that session does not govern the present v003 task.
Only this relevant acceptance statement and the small source excerpt are
retained here; the private conversation is not copied into the repository.

The same task's recorded `scripts/grimo/build-carol-reference.py` source contains:

1. Closed radial surfaces derived from authored reference outlines.
2. Broad/medium/small elliptical Gaussian locks combined by a fifth-power norm:
   `sum((h * exp(-2 * elliptical_distance_squared)) ** 5) ** 0.2`.
3. A rounded base depth plus that continuous relief; a recessed face region.
4. Opaque curved-volume paint that blends source watercolor pigment with an
   authored reverse palette. Much of the apparent fine fleece is **paint**.
5. Later explicit shallow-relief changes: body reverse depth `.94 → .14`,
   head `.57 → .12`, face `.25 → .08`; independent feet removed in favor of
   the illustrated body silhouette. View movement was narrowed.

The formula and authored locks are preserved in
[historical-fleece-excerpt.txt](historical-fleece-excerpt.txt). This is an
excerpt recovered from a source read during that session, not a full final
source restoration. The exact final binary is unavailable. The surviving
`output/playwright/carol-2p5d-approved.png` was visually inspected and copied
unchanged to `historical-relief-screenshot.png`; its filename alone does not
establish final-revision equivalence. Hashes are in [historical-provenance.json](historical-provenance.json).

**Conclusion:** the accepted experience did exist, but its final architecture
was a shallow 2.5D relief. It is not evidence of an accepted full-depth rear or
four-support chassis. Its visual principles can be transferred; its geometry
cannot supersede v002's Full-3D structure.

## Modeling hypothesis and implementation

Separate two things that the old paint combined visually: the broad connected
cloud envelope and the local ridge pattern. Keep the full-depth envelope, use
anisotropic (different widths along/across a ridge) continuous fields for the
ridge pattern, and judge the result in clay as well as diagnostic color.

- Diffuse the v002 connected mesh to soften sphere-union ridges, without editing
  individual v002 construction spheres or changing its supporting anatomy.
- Evaluate 15 broad and 22 smaller directed Gaussian controls over the entire
  3D surface; extend the historical fifth-norm principle over side and back.
- Add 14 elliptical front relief controls for crown, cheeks and lower collar.
- Use radial rather than opposing-normal displacement to avoid folds in valleys.
- Apply local diffusion at crown and temples. A single additive crown brush
  fills the deep inherited saddle; a whole-surface voxel reconstruction makes
  that correction part of the same closed fleece, not an attached ball.
- Reattach the existing one moon and five stars to actual fleece depth. No
  extra motifs, projected original art, outline plane or camera-facing geometry.

The original rear tuft remains independent at its v002 root. Full Companion
continues to have a real back and fore/rear support separation. No rigging,
motion, GLB export, final shading/UV/fur, runtime or persistence change occurs.
Close Window-Lean balance/deformation remains untested; unchanged supports do
not prove a future animated pose safe after a fleece change.

## Actual autonomous visual loop

Every numbered iteration generated seven real Blender views. Inspection was
adaptive: fronts and obliques exposed the earliest defects; later side/back
and clay views tested closure, smooth regions and crown correction. The final
seven-view board and the 320-pixel front were inspected directly after rendering.

| Iteration | Diagnosis from images | Action/result |
| --- | --- | --- |
| 1 | Analytic ellipsoid too smooth; lower fleece receded, exposing supports and chassis | Reject; increase lower/front volume |
| 2 | Fuller parametric surface became a rectangular cushion | Reject analytic-envelope construction; retain the actual v002 envelope |
| 3 | Diffused envelope plus continuous relief preserved face/limbs, but crown trench and over-large smooth regions remained | Correct displacement direction and add directed secondary relief |
| 4 | Radial fields improved continuity; small relief became too pointed and crown notch remained | Reduce field strength; locally relax saddles |
| 5 | Global relaxation had erased too much small cloud rhythm | Reduce global diffusion from 160 to 65 iterations |
| 6 | Better scale hierarchy; crown trench still visible | Try a broader depth correction |
| 7 | Front trench became shallower, but clay revealed a folded crown flap | Reject; replace depth pull with one additive brush and whole-surface reconstruction |
| 8 / final | Crown flap/trench removed; connected front/side/back remain; small collar scallops retained | Render final at 1400 pixels; reopen and inspect; submit with limits below |

The final generator's `--pass-number 1/2` is an **ablation switch** for the
corrective fill/secondary relief, not a replay of this chronological table.
Intermediate renders are local `artifacts/carol-v003/pass1` through `pass8`;
the compact iteration board is versioned. Earlier source edits are not claimed
to be reproducible through that switch.

## Validation and limits

- Blender 5.2.1 LTS: actual v002 load, v003 save and reopen succeeded.
- One connected closed fleece; finite coordinates; positive signed volume.
- **235,848 fleece triangles; 0 nonadjacent triangle intersections** in the
  saved final asset. This is a sculpt study, not a runtime polygon budget.
- Four separate supports, independent rear tuft; protected mesh vertex hashes
  and world matrices match v002. No armatures, Actions or shape keys.
- Canonical, v001 and v002 SHA-256 hashes remain unchanged.
- Seven captures are nonempty and uncropped; alpha bounds are recorded in
  [image-metrics.json](image-metrics.json).
- [validation.json](validation.json) records source/helper/artifact hashes and
  structural checks. [surface-validation.json](surface-validation.json) records
  saved-surface checks. No app code changed, so no web/runtime or full app suite
  was run. Human visual quality is **not** inferred from these technical checks.

Remaining visual issues: the canopy and some side/rear masses are still broad
and smooth; the face opening reads relatively deep; the crescent retains coarse
depth sampling; eye/face materials remain v002 placeholders. The historical
watercolor beauty, micro-fleece and exact source-to-neutral correspondence are
not reproduced or approved. Hidden motif mapping remains unresolved.

## Reproduce

From the Grimo root in PowerShell:

```powershell
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background --python-exit-code 1 --python scripts/blender/build-carol-v003.py -- --pass-number 2 --width 1400 --output docs/production/carol/evidence/blockout-v003 --blend-path assets/grimo/production/carol/blender/carol-blockout-v003.blend
& 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe' --background assets/grimo/production/carol/blender/carol-blockout-v003.blend --python-exit-code 1 --python scripts/blender/validate-carol-v003-surface.py -- docs/production/carol/evidence/blockout-v003/surface-validation.json
python scripts/blender/build-carol-v003-review.py
```

The review compositor uses existing Pillow. It recreates the iteration board
only when local intermediate renders exist; the versioned board preserves that
history on a fresh checkout. The generator uses Blender-bundled modules only.

## HUMAN Gate

1. Does this continuous surface improve Carol's dream-cloud identity relative
   to v002, or does it smooth away too much of the cloud rhythm?
2. Are the crown, face opening and lower collar acceptable as structural forms?
3. Do side/back form and the unchanged supports/tuft remain convincing?

Record **PASS / CONDITIONAL PASS / FAIL** and the view/region needing revision.
No main merge, rigging or runtime advancement follows automatically.
