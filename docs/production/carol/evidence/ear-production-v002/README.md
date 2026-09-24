# Carol ear production v002

**READY_FOR_HUMAN_EAR_REVIEW — HUMAN REVIEW REQUIRED.** No perceptual approval or authority promotion.

- Branch: `codex/carol-ear-production-v002`.
- Verified source: `origin/codex/carol-ear-production-v001` at `f2a8d40807099ce8c99bac2bf3afda38a03556f0` (matched expected remote HEAD).
- Candidate: `assets/grimo/production/carol/blender/carol-ear-production-v002.blend`.

## Donor decision

Inspected actual blends and rendered Side plus supporting Front for **ear-production-v001, hero-modules-v003, hero-modules-v002, v011, v012, v013, hero-experience-probe-v001 and a-v006** (all have the `carol-` prefix). The exact unprefixed probe/a-v006 filenames were absent; their prefixed counterparts were inspected.

**Chosen: carol-ear-production-v001.blend.** Its face is identical to hero-modules-v003. Against approved Normal Side and supporting Front, it offers the best available combined rounded forehead/cheek/under-jaw read, short nose, closed mouth and seated-eye relationship. This is a fresh comparison, not a newest-version preference. v011/modules-v002 have the same muzzle and jaw with more protruding eyes; v012 does not improve the muzzle and increases eye bulge. v013 moves the nose forward but makes the forehead and jaw visibly planar/boxy. The experience probe retains the earlier face family; a-v006 has a sloped forehead, different eye proportions and an open mouth. None demonstrates a better complete side-face donor. The selected muzzle remains simplified relative to authority; this task does not correct it.

[Compact donor comparison](donor-audit-summary.png) shows every inspected donor with ears/fleece hidden, identical orthographic framing for current-axis assets and uniform head-fit framing for legacy a-v006. Neutral light was added only to the legacy audit render because its saved scene has no world/render lights. No donor was modified during audit.

## Ear changes / bounded scope

Only **EAR_L / EAR_R**, ear-only materials and their provisional test keys changed. **39 non-ear objects remain unchanged after save/reload; head edits: zero.** No donor migration, body/hoof/tail edits, runtime work or authority edits.

- Brown roughness raised from 0.48 to 0.86, specular reduced to 0.18; gentle sheen and tiny procedural normal variation soften the surface without a new material framework.
- Brown rim widened; pink tapers closed earlier, leaving the distal stations and cap brown. Pink remains a material region of the same closed shell, never a separate card.
- Section depth reduced and offsets curved to reduce the thick Side wedge. Broadest planform moves into the mid/distal-middle region with a narrower root and rounded taper.
- Deeper pink seat and stronger lower/distal containment improve cup read. One neutral mesh serves all views; reflected counterpart and fixed-root bend keys retain v001 architecture.

## Validation / limits

Output opens and saves/reloads. Both ears are finite closed shells with outward normals and exact neutral mirror correspondence. Neutral, lift, droop and attention checks show no detected non-adjacent triangle intersections; roots stay fixed and seated inside the unchanged head. Controls are zero in the saved asset. Image decoding and scoped Git checks complete the bounded validation; no unrelated tests were run.

Matte response and brown tip containment visibly improve over v001. **Side still differs from the authority's flowing silhouette; pink/cup proportion, surface softness and whole-ear identity need Human judgment.** Existing non-final fleece still substantially occludes ears and is shown only in diagnostic insets; it is not saved into this candidate. No full-rig or animation approval is claimed.

- [Authority / v002 Front, Side, Top, 3Q](ear-isolated-comparison.png)
- [Attached Front](carol-ear-attached-front.png) / [Attached Side](carol-ear-attached-side.png)
- [Representative bend checks](ear-deformation-check.png)
- [Validation](validation.json)

Reproduce: Blender `--background --python scripts/blender/audit-carol-ear-donors-v002.py`, then `--background --python scripts/blender/build-carol-ear-production-v002.py`, then system Python `scripts/blender/compose-carol-ear-evidence-v002.py`. Intermediate renders stay in the OS temporary directory.
