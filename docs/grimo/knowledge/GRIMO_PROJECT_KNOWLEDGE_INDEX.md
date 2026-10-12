# Grimo — Project Knowledge index

**Role:** Single entry point to durable specifications on `main`. Read only sources relevant to the task. The working tree and current execution branch, not this index or Handoff, determine the actual implementation state.

## Durable authority (by subject)
| Subject | Source |
| --- | --- |
| Product goal and companion quality | [Product North Star](GRIMO_PRODUCT_NORTH_STAR_AND_MINIMUM_REQUIREMENTS.md) |
| Character experience, attention and Human gates | [Character Experience Spec](GRIMO_CHARACTER_EXPERIENCE_SPEC.md) |
| Coherent 3D capability, visual authority and runtime | [Character Production Architecture](GRIMO_CHARACTER_PRODUCTION_ARCHITECTURE.md) |
| Human/Planner/Codex autonomy and workflow | [Production Operating System](GRIMO_PRODUCTION_OPERATING_SYSTEM.md) |
| **Character production WHY** (goals → means) | [Goal√map](Goal√map.md) |
| Four screens, reward, item, collection rules | [Product Feature Spec](product/GRIMO_PRODUCT_FEATURE_SPEC.md) |
| Task/reward persistence and item data | [Data Model Spec](product/GRIMO_DATA_MODEL_SPEC.md) |
| UI/UX, navigation and visual design | [DESIGN.md](../../../DESIGN.md) |
| Canonical identity images | `assets/grimo/source/{carol,jill,pino,shushu}/` |
| Implementation routing | [repo-map](../../repo-map.md) |

## Production state and evidence
- [Handoff](../../production/Handoff.md): last-known cross-session pointer, **not a live state or Human approval**. It must be checked against the real branch/HEAD.
- `docs/production/<character>/`, `docs/production/motion/`: scoped working contracts, drafts and review evidence. These may exist **only on an execution branch**; read them there, not from an older `main` copy.
- `assets/grimo/production/`: versioned candidate meshes, reference inputs and generated artifacts. Presence is not acceptance. Canonical identity and separately approved references outrank candidate assets.
- [Carol Motion Spec](character-production/carol/CAROL_MVP_MOTION_SPEC.md): character-specific motions, consult when relevant. Later approved no-macro-fleece-lag decisions outrank generic earlier mentions of fleece delay.

## Supporting and historical sources
- `research/`: analysis and inspiration, never automatically promote measured/inferred reference values to product specifications.
- `character-experience/GRIMO_EXPERIENCE_MOTION_BIBLE.md` and `character-production/GRIMO_3D_BLENDER_PRODUCTION_BIBLE.md`: older reference documents, **not current primary authorities**.
- `docs/archive/`: superseded or historical material including Phase-0 prompts. Git history preserves previous decisions.
- `.agents/skills/` and `.codex/`: task-specific tooling and local policies, **not** replacements for product specs.

**Priority:** latest explicit Human decision and applicable approved canonical/specification → current actual implementation/evidence → supporting research/history. For visible approval, view the actual image, motion or runtime; text and technical PASS alone do not establish Human acceptance.
