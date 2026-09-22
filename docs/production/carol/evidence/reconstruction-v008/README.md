# Carol v008 — blocked structured Skin cage

**STATUS: BLOCKED_AT_V008_SKIN_INTERNAL_GATE**

**Human Geometry Gate: PENDING; not ready for Human submission.**

Three Skin edit/render cycles were inspected in both Front and Side. Cycle 2
is retained: cycle 3 broadened the ear in Side but worsened its shape and
buried the mouth. No fleece was constructed. This is a blocked handoff to
ChatGPT Planner, not a completed four-view candidate. v007 remains historical
Human FAIL.

## Source and reproduction

- Branch: `codex/carol-final-reconstruction-v008`.
- Base: `d5bacf212eef6dd141f39b2abbf51b40d29a6a53`, fetched from remote v007.
- Candidate/source/evidence commit: `d65aba695c24faa037d2372cf7d86e384ea47e11`.
  The following documentation-only commit records this immutable artifact ID.
- Asset: `assets/grimo/production/carol/blender/carol-v008.blend`.
- Generator: `scripts/blender/build-carol-v008.py`.
- Evidence utility: `scripts/blender/carol-v008-evidence.py`.
- Blender: **5.2.1 LTS**, build `9e2066aef7ef`; evidence utility uses Pillow.
- One agent, Blender CLI only; no subagents, Blender MCP or MCP policy changes.

From repository root:

```powershell
blender -b --python scripts/blender/build-carol-v008.py -- --iteration 2
python scripts/blender/carol-v008-evidence.py --cycle 2 --publish-blocked
```

The generator starts from an empty scene, builds the selected cycle-2 controls,
renders both Skin views at 640 px, saves the editable `.blend`, and exports
measurements to `tmp-carol-v008/cycle-2/`. The iteration argument labels output
only; it does not switch historical geometry. The evidence utility creates
registered comparisons and copies only the blocked Skin packet here.
Temporary renders, logs and source snapshots are ignored by Git.

`rejected-cycle-3-sheet.png` preserves the rejected third comparison, not the
saved model. Its source snapshot remains local under `tmp-carol-v008/`; the
committed reproducibility claim is for cycle 2 only. No fourth geometry edit
cycle ran. A separate clean-process build reproduced the selected controls.

## Authority and registration

Geometry authority is exclusively `CAROL_GEOMETRY_PARAMETERS.md` plus the
four FINAL/LOCKED images in `assets/grimo/source/carol/approved-3d/`:
`carol_front.png`, `carol_side.png`, `carol_skin_front.png`, and
`carol_skin_side.png`. SHA-256 values are checked before every build and
recorded in `measurements.json`. The current
`assets/grimo/source/carol/carol-Identity-canonical.png` was inspected for
secondary identity only. No reference was changed or regenerated.

No old geometry authority was used. No historical Back/Top/3Q image was used
as a target; no v005/v006 mesh, old fleece construction, or old torso array
was imported. v007 supplied registration/rendering concepts and small utility,
eye, closed-ear and planted-hoof concepts only, never a runtime dependency.

X increases front to rear, Y is bilateral, Z is up; H=1 and ground Z=0.
Both orthographic cameras use the same 1.52 H span. Skin Front registration
uses 994 px/H from eye spacing, ground 1075 and centerline 626.5. Skin Side
uses 1019 px/H from support spacing, ground 1037 and origin 64. These prior
observational registrations were retained after verifying reference hashes
and inspecting the actual images. They are not new contract values.
Registered Skin Side skull height is about .728 H versus .698 H in Skin Front;
the candidate maximum is about .703 H. This difference remains unresolved.

## Implemented architecture

- `TORSO_CAGE`: 160 control vertices / 158 quad faces, longitudinal stations
  with X, bottom/top Z, Y half-width and exponent; named `chest`, `abdomen`,
  and `pelvis_rump` groups.
- `HEAD_CAGE`: 240 control vertices / 238 quad faces, horizontal cheek,
  muzzle and cranial sections. Head placement was not shifted to fake
  shorter torso length.
- `SHORT_NECK_SOCKET`: short broad overlapping cage, no ellipsoid connector.
- Four independent squat tapered limb cages, each 96 control vertices,
  partially buried in the torso. Heavy independent hooves retain support
  centers X=.390 and X=.920 with bilateral front placement.
- Closed-volume ears, shared huge-eye concept and closed neutral mouth.
- Non-rendered `TAIL_PIVOT` at (.985,0,.355), short independent
  `TAIL_ATTACHMENT_PAD`, and `TAIL_TUFT`. No long renderable root tube.
  This module is **not successfully attached to the rump**.

Primary cages retain unapplied Catmull-Clark subdivision. No fleece voxel
remesh or Boolean ear recess exists. There is no view-specific geometry,
scaling, object replacement or neutral-pose change. Front/Side geometry
digests match. Normal was not built, so Skin/Normal identity is not claimed;
there is only one underbody and no alternate Normal chassis.

The coherent subdivision fleece cage, six macro regions, sparse regional
fields and ear saddles remain **unimplemented** because Skin is blocked.

## Internal review and blockers

| Area | Observed result |
| --- | --- |
| Skin Front | Huge head/eyes, four supports, broad ears and heavy planted hooves remain readable. Ear bowl/root shape differs; hind supports are more exposed and the socket/body join still needs fitting. |
| Skin Side | Explicit chest/abdomen/rump is compact and support centers are fixed. Ear projection is narrow, head/chest overlap abrupt, limb roots too rounded, and tail visibly detached. |
| Normal Front / Side | Not built or rendered; Skin prerequisite not satisfied. |
| Derived coherence | Not generated; both primary gates required first. |
| Motion clearance | Not performed; neutral Skin remains unresolved. |

The strongest blocker is **tail/rump reconciliation**. The evaluated torso
ends at X=1.05190; the short attachment starts at X=1.19220, leaving at least
**.14031 H** longitudinal separation. The independent tuft spans
X=1.20263–1.28737, retaining the contract's visible base/center intent and
approximately .085 H length. Its internal pivot cannot close that visible gap.

Under the support-based registration, the Skin reference rump ends around
X=1.04 and its tuft is directly attached. Connecting the current pad would
require extending the visible rump, moving the tuft away from Normal's locked
visible-X intent, or reinterpreting the shared attachment and registration.
A long root tube would repeat the rejected v007 strategy. No such change was
silently made. This is a conflict in this construction, not proof that no valid
model exists. Planner must resolve the interpretation before the next attempt.

Iteration history:

1. Fresh primary cages, fixed supports and contract-positioned tail. Both
   views exposed the tail gap, weak Side ear read and narrow upper limb roots.
2. Broader upper limb roots and adjusted ear root/sections improved support.
   Tail detachment and narrow Side ears remained. Selected for preserved face.
3. Rotated across-ear sections and added a local muzzle offset. Side ear area
   increased but the outline worsened and mouth became buried. Rejected.

## Targeted evidence and scope

The retained candidate was rebuilt in a clean Blender process and the evidence
utility ran successfully. Required blocked-stage files exist. All primary
cages retain quad controls and `SUBSURF`; Front/Side neutral digests are equal.
Four evaluated hoof minimum Z values are about .0000224 H, negligible
subdivision rounding above ground. Tail separation uses evaluated geometry.
Both Python files parse successfully. Source inspection finds no construction
using remesh, Boolean difference or old geometry dependencies. The diff is
limited to v008, production state and its temporary-output ignore rule.
No unrelated application suite was run.

Technical checks are evidence only and do not approve identity, geometry or
motion. There is no production rig, final retopo lock, animation, final
material/lookdev, GLB, or PlayCanvas integration.

## Evidence and next handoff

- `skin-review-sheet.png`: retained reference/model/50% overlay for both views.
- `skin-front.png`, `skin-side.png`: selected neutral 640 px renders.
- `skin-front-overlay.png`, `skin-side-overlay.png`: registered 50% overlays.
- `rejected-cycle-3-sheet.png`: final rejected attempt, both primary views.
- `measurements.json`: reference hashes, registration, cage counts, evaluated
  bounds, neutral digests and explicit blocked-stage scope.

Next handoff: **CHATGPT_PLANNER**. Resolve Skin attachment and primary fitting
before another attempt. Fleece, derived views and motion clearance remain
gated. Human Geometry Gate remains PENDING.
