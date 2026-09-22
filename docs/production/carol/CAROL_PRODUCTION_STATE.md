# Carol production state

This file is the single mutable Carol execution truth.

## Current state — 2026-09-23

- Branch: `codex/carol-final-reconstruction-v009`.
- Retained asset: `assets/grimo/production/carol/blender/carol-v009.blend`.
- Retained candidate: **v009-A2**, a bounded Phase A architecture attempt; it is **not an accepted static candidate**.
- Execution status: **BLOCKED_AT_V009_PHASE_A_ARCHITECTURE**.
- Human Geometry Gate: **PENDING HUMAN REVIEW**; this state file does not self-approve or reject that gate.
- Executor-recorded static visual status: **FAIL**.
- Motion preflight: **NOT_RUN_STATIC_PREREQUISITE_FAILED**.

## Current v009-A2 architecture

- The current v009 exterior architecture is one authored `CENTRAL_CHASSIS` mesh. The old v008 exterior-owner combination is not current v009 architecture.
- `CENTRAL_CHASSIS` is one connected, closed, all-quad surface with nonmanifold edges = `0`; these topology facts do not make it a clean production exterior.
- Evaluated disjoint face intersection pairs = `455`; this is the recorded geometric-cleanliness failure.
- The selected eye prototype is an embedded partial ellipsoid with approximately `.029 H` central relief and six surrounding lid/socket loops.
- Frozen geometry authority remains: torso evaluated width ≈ `.598571 H`; support centers `.390 H` / `.920 H` with spacing `.530 H`; Front eye width `.137 H`, height `.149 H`, centers `±.162 H`.
- The four definitive Normal/Skin Front/Side sources remain FINAL/LOCKED. One neutral model serves Front and Side; no camera-specific geometry is used.

## Current blockers

- Hard lower-cheek shelf instead of a rounded jaw.
- Over-stretched under-chin → chest transition.
- Evaluated self-intersection in the central chassis (`455` disjoint face-intersection pairs).
- Side / 3Q face-eye identity remains insufficient against the locked Skin references.

These visual blockers and the evaluated intersection failure keep Phase A blocked. Manifoldness, connectedness, and all-quad topology are recorded successes, not a Phase A pass.

## Frozen / deferred modules

- Ears remain unchanged temporary v008 modules; Ear Phase B was **not started**.
- Hooves remain unchanged temporary v008 modules; Hoof Phase C was **not started**.
- Fleece: **not started**.
- Production rig: **false / not created**.
- Animation: **false / not created**.
- GLB export: **false / not performed**.
- PlayCanvas/runtime integration: **false / not performed**.
- Motion preflight was not run because the static prerequisite failed.

## Historical predecessor context

The following is historical v008 context only and is not current v009 production truth:

- v008 revision 17 is the rejected predecessor. Its evidence records the earlier Human Review FAIL for Side face/eye identity, head/chest transition, ear-root and true 3D ear volume, and hoof 3Q form.
- v008 used separate `HEAD_CAGE`, `SHORT_NECK_SOCKET`, and `TORSO_CAGE` exterior owners. v009 replaced those owners with the single authored `CENTRAL_CHASSIS` described above.
- The v008 Boolean union / smoothing experiment was disposable and rejected; it does not describe the retained v009 architecture.
- The temporary v008 ear and hoof modules are retained only because their replacement phases were not reached. Their historical failures are preserved in the v008 evidence package.

## Next handoff

**CHATGPT_PLANNER / HUMAN GEOMETRY REVIEW / Phase-A architecture correction.** Review the [v009 blocked comparison sheet](evidence/reconstruction-v009/human-comparison.png). Do not self-approve the Human Geometry Gate, start Phase B/C, or advance to fleece.
