# Carol v008 — Skin revision handoff

**STATUS: BLOCKED_AT_V008_SKIN_REVISION_GATE**
**Human Geometry Gate: PENDING; not ready for Human submission.**

Three newly authorized Skin revisions were inspected in both Front and Side.
**Revision 2 is selected.** Tail attachment and buried limb roots improve the
pushed baseline, but the ear bowl/profile and head/chest transition remain
insufficiently fitted. Revision 3 made the rear jaw more angular and reduced
the Side ear's root/bowl read. No fourth geometry revision ran.

## Source and reproduction

- Branch: `codex/carol-final-reconstruction-v008`; no new geometry track.
- Fetched baseline: `601296e8e44f7eb4e6f9843bedcca61f940d7abb`; local/remote
  agreed and the worktree was clean before editing.
- Starting geometry: retained old cycle 2, never rejected old cycle 3.
- Asset: `assets/grimo/production/carol/blender/carol-v008.blend`.
- Generator: `scripts/blender/build-carol-v008.py`.
- Comparisons: `scripts/blender/carol-v008-evidence.py`.
- Blender **5.2.1 LTS**, build `9e2066aef7ef`; Python/Pillow for evidence.
- New execution context; one agent; Blender CLI/background only. No subagents,
  Blender MCP, GUI production edits or new plugins. Existing project
  `multi_agent = false` and disabled Blender MCP were preserved. This is a
  continuation of the authorized v008 geometry phase with its existing toolset.

```powershell
blender -b --python scripts/blender/build-carol-v008.py -- --revision 2
python scripts/blender/carol-v008-evidence.py --revision 2 --publish-blocked
```

The generator builds the **selected revision-2 controls** from an empty scene,
renders Skin Front/Side at 640 px, performs disposable numerical attachment
probes, verifies neutral state, and saves the editable asset. Outputs go to
`tmp-carol-v008/revision-2/`. The revision argument labels output only; it
does not switch historical geometry. Only the selected candidate has a
committed reproducible source; rejected-attempt snapshots/logs remain local.

## Authority and registration

Geometry authority remains the four FINAL/LOCKED images in
`assets/grimo/source/carol/approved-3d/` plus `CAROL_GEOMETRY_PARAMETERS.md`.
All four were inspected and hash-checked; none was edited or regenerated.
`assets/grimo/source/carol/carol-Identity-canonical.png` supported identity
only. Relevant Carol causality, touch, head/face, support and secondary-motion
sections of the current motion and Blender production bibles were read.

The narrow contract edit clarifies common **Skin tail core versus external
Normal tail fleece shell**, as authorized by the current handoff. Normal's
numerical tail values are unchanged; they no longer force a floating cream core.

Registration is unchanged: H=1, X front-to-rear, Y bilateral, Z up; both
orthographic cameras span 1.52 H. Skin Front uses 994 px/H, ground 1075,
centerline 626.5; Skin Side uses 1019 px/H, ground 1037, origin 64. These are
observational registration values. Front/Side imply slightly different skull
heights (about .698/.728 H); the candidate remains one head at maximum
Z=.70294 H. There is no view-dependent correction.

## Selected architecture

- Semantic quad cages with unapplied Catmull-Clark subdivision.
- Raised front chest overlaps lower head and short internal socket. The
  connection improves but its visible segmentation remains unresolved.
- Separate fore/hind cages broaden and bury proximal supports. Hind roots
  slope inward into the pelvis; named groups distinguish proximal/taper/distal.
- Locked support centers remain **X=.390/.920 H**. Fore transverse centers
  changed from Y=+/-.175 to **+/-.145 H** to fit Skin Front; hind remain
  +/-.245 H. This changes the common model; hoof dimensions are unchanged.
- Ears have **8 local-frame stations**, explicit center XYZ, profile width and
  thickness, and ROOT/MID/TIP groups: 128 control vertices / 126 quads each.
  Side volume improves, but the triangle/inset still fails the broad soft bowl.
- `SKIN_TAIL_CORE` replaces the detached tuft/pad: 72 vertices / 70 quads,
  parented to `TAIL_PIVOT`, with no renderable rod/stalk. Pivot=(.985,0,.355),
  center X=1.032 H, evaluated X extent=.98963–1.07437 H, and longitudinal
  rump overlap=.06226 H. It is independent and directly attached.
- All twelve requested empties carry DEBUG/NON_EXPORT/NON_PRODUCTION metadata.
  Head, torso, limb and ear semantic groups remain editable.
- No fleece, Normal tail shell, production rig, skinning, animation, final
  retopology, final lookdev, GLB export or PlayCanvas work was implemented.

## New revision history

| Revision | Change | Both-view decision |
| --- | --- | --- |
| 1 | Attach compact Skin core; rebuild ears with local-frame stations; debug landmarks. | Tail gap closed; Side ear area increased but distal outline stayed triangular. Chest/limb segmentation remained. |
| 2 | Raise chest; separate fore/hind buried proximal shapes; fit fore transverse placement. | Improved support connection and stance. Ear and head/chest still block. **Selected.** |
| 3 | Revise local ear frames/profile and retract lower rear head sections. | More angular rear jaw; diminished Side ear root/bowl. **Rejected.** |

The selected geometry was rebuilt once in a clean process after selection.
Front/Side and the reloaded neutral asset share geometry digest
`c6e4482465ae128e8fd04b4f48d47f8edc6d61f473a69184c73529f1fc18606a`.
One rejected revision-3 sheet explains the selection. Old rejected-cycle-3
evidence was removed from the current packet to avoid confusing the attempts.

## Internal findings and limits

| Area | Finding |
| --- | --- |
| Skin Front | Large face/eyes and heavy hooves preserved; stance improved. Ear inset/rim and support overlap differ; cranial/cheek shape remains squarer. |
| Skin Side | Compact torso, fixed supports, attached tail. Ear still triangular; head/chest segmented; proximal silhouettes need fitting. |
| Head / face | No face/eye shrink. Articulation and blink/cheek deformation clearance unproven; no production eyelid system. |
| Support / COM | Neutral roots intersect torso; four hooves planted. Dynamic weight transfer unproven. |
| Tail | Neutral attachment and numerical pivot contact confirmed; visual deformation and future shell relation unproven. |
| Normal / fleece / derived views / motion sheet | Not reached; Skin prerequisite failed. |

Evaluated-mesh BVH probes use virtual tail transforms without changing the
scene. Core/rump surface-intersection pair counts: **92 neutral, 81 up 20°,
98 down 20°, 92 at either lateral 7°**. These establish contact, not good
deformation, acceptable penetration, motion clearance or Human approval.
Head and all four limb roots also intersect the torso in neutral. Tail contact
is therefore supported by surfaces, not just overlapping bounding boxes.

Head yaw/pitch/tilt, cheek lean, ear sweep, COM transfer and forelimb-adjustment
visual stress tests were **not reached**: their neutral prerequisites remain
unsatisfactory. Fleece/shell clearance is absent. Measurements explicitly
record these limits; no automatic Human PASS score is computed.

## Targeted validation

Clean Blender rebuild and selected evidence regeneration; both Python files
AST-parse; identical Front/Side neutral digests; unchanged reference hashes;
fixed support X; no Boolean/remesh/armature modifiers or animation; no old
v005/v006 runtime dependency or imported v007 geometry. The saved asset is
reloaded to check its digest, neutral flag, debug metadata, cage modifiers and
reference paths. Evaluated hoof minima=.0000224 H (negligible subdivision
rounding above ground). No unrelated application test suite was run.

Only one underbody exists. Skin/Normal sameness cannot yet be demonstrated
because Normal is unimplemented. Technical checks do not approve geometry.

## Evidence and next handoff

- [Selected comparison](skin-review-sheet.png): reference / revision 2 / 50% overlay.
- [Skin Front](skin-front.png), [Skin Side](skin-side.png).
- [Front overlay](skin-front-overlay.png), [Side overlay](skin-side-overlay.png).
- [Rejected revision 3](rejected-revision-3-sheet.png): diagnostic history only.
- [Measurements](measurements.json): hashes, cage counts, bounds, pivots and limits.

**CHATGPT_PLANNER:** audit the pushed packet and specify a new bounded Skin
revision for ear bowl/root and head/chest fitting. Retain attached core and
fixed longitudinal supports. Do not proceed to fleece or Human submission.
