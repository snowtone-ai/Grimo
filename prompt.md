# Handoff

Target: CODEX_ASTRA
Model: GPT-6 Astra
Reasoning: Medium

## Mission

Perform Carol's initial 3D geometry interpretation and complete:

`docs/production/carol/CAROL_GEOMETRY_DECISION.md`

This is an evidence-based interpretation task. Geometry remains undecided until
the decision record is completed and passes the Human Gate.

## Required inputs

- `assets/grimo/source/carol/carol-Identity-canonical.png` — visible identity authority
- `assets/grimo/source/carol/approved-3d/` — approved Carol 3D reference packet and `authority.json`
- `docs/production/carol/CAROL_CAMERA_CONTRACT.md`
- `docs/production/carol/CAROL_MODELING_CONTRACT.md`
- `docs/grimo/knowledge/character-production/carol/CAROL_MVP_MOTION_SPEC.md`
- `docs/grimo/knowledge/character-production/GRIMO_3D_BLENDER_PRODUCTION_BIBLE.md`
- `docs/grimo/knowledge/character-experience/GRIMO_EXPERIENCE_MOTION_BIBLE.md`

Consult relevant Product, Data, and Research authorities as needed. Visible
identity wins over 3D references where they conflict; Motion Masters are
evidence, not motions to copy.

## Required output

Write `docs/production/carol/CAROL_GEOMETRY_DECISION.md` with observations,
confidence, unresolved conflicts, and missing measurements. Do not claim the
interpretation is complete until evidence and the Human Gate are recorded.

## Explicit prohibitions

- Do not start a Blender blockout, rig, or animation.
- Do not generate a GLB asset or begin PlayCanvas Carol implementation.
- Do not fill gaps with generic sheep anatomy.
- Do not guess unmeasured FOV, camera distance, camera height, or other numeric camera values.
- Do not prioritize 3D references over the canonical identity image.

## Handoff contract

This file is a typed handoff artifact for the next session. Other valid forms
are `CHATGPT_PLANNER` for pushed-state planning that outputs a complete Luna
prompt, and `CODEX_LUNA` for an already specified deterministic task. A Luna
handoff must end with targeted validation as needed, commit, and push. A
Planner handoff must not modify the repository.

## Allowed handoff forms

### Type A — CHATGPT_PLANNER

```markdown
# Handoff

Target: CHATGPT_PLANNER
Repository: snowtone-ai/Grimo
Branch: <current pushed branch>

## Mission

Read the latest pushed state of the specified branch from GitHub. Do not modify
the repository. Complete the reasoning and output one complete
GPT-5.6 Luna / Low execution prompt.

## Task

<next problem>

## Required repository inputs

<only the files needed for planning>

## Planning requirements

<decisions and investigation required>
```

The Planner must confirm repository state, use known information without
re-asking, avoid guessing local-only state, and make the Luna prompt concrete
enough that Luna need not redesign. The Luna task must include lean targeted
validation and finish with commit and push.

### Type B — CODEX_LUNA

```markdown
# Handoff

Target: CODEX_LUNA
Model: GPT-5.6 Luna
Reasoning: Low

## Mission

<exact deterministic task>
```

### Type C — CODEX_ASTRA

```markdown
# Handoff

Target: CODEX_ASTRA
Model: GPT-6 Astra
Reasoning: Medium

## Mission

<explicit high-value specialist task>
```

Astra tasks may be direct handoffs and do not require a ChatGPT Planner step.
