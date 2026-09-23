# Grimo — Current Project Memory

This file contains durable decisions and routing only. Mutable Carol candidate,
Human Gate, evidence, blockers, and next-step facts belong exclusively to
[`CAROL_PRODUCTION_STATE.md`](../../production/carol/CAROL_PRODUCTION_STATE.md).

## Product North Star

Grimo does **not** exist to produce a technically perfect 3D model. The Goal is:

> On the smartphone Grimo screen, Carol / Jill / Pino / Shushu feel alive,
> cute, aware of the user, causally responsive to user actions, and like
> companions rather than canned puppets even across extended interaction.

Partner Pikachu / Eevee are quality and interaction references, not 3D-purity
benchmarks. Geometry, topology, rigging, fleece, animation, runtime, testing,
documentation, and automation are means to the companion experience.

## Architecture status

Current baseline hypothesis:

**Front-Optimized 3D-First Living Character Architecture**

- Use a spatial 3D character as the default production basis.
- Concentrate Hero quality inside the actual interaction envelope; do not pursue
  equal-fidelity 360-degree coverage as an end in itself.
- Hidden geometry is justified by support, deformation, attachment,
  collision/clearance, and possible motion exposure.
- Local 2D, material, shader, morph, and compositing techniques are allowed
  when they improve the final experience.
- Whole-character / single-finished-image warp, squash, scale, or similar
  pseudo-life remains prohibited.
- Blender-centered authoring + GLB/glTF + PlayCanvas remains the current
  implementation hypothesis, not a goal above Product North Star.
- If Partner Experience Production Analysis or a functional Carol prototype
  disproves this hypothesis, Architecture Review may move to a hybrid approach.

Archived PixiJS / old layered-2D / old 2.5D implementation is not the current
baseline and must not be revived by inertia. That does **not** prohibit a new,
evidence-driven hybrid architecture.

## Device truth

- Primary available real-device QA: **Xiaomi 14T Pro**.
- **Pixel 7a-class** remains the lower-performance compatibility / design target.
- A real Pixel 7a is not currently available. Pixel 7a real-device PASS must not
  be required or claimed. Treat it as **UNVERIFIED_TARGET** until a real device
  or sufficiently trustworthy validation environment is available.
- Runtime acceptance evidence is currently gathered on Xiaomi 14T Pro; lower
  device performance margin is managed through budgets/profiles and later
  target-class validation.

## Goal-backward production loop

Use this as a feedback loop, not a universal waterfall:

```text
Product Goal
→ Partner experience requirements
→ minimum architecture hypothesis
→ functional visual prototype
→ provisional rig / representative motion
→ Human experience review
↔ targeted geometry correction
→ production modeling / retopo / rig / fleece
→ early GLB / runtime integration
→ real-device QA
→ content expansion
```

Do not perfect an intermediate artifact merely because it exists. Technical PASS
cannot override user-visible failure. Motion, deformation, and runtime risk
should be tested as early as practical.

If essentially the same blocker survives **2 bounded implementation cycles**,
stop local repair and trigger Architecture Review before authorizing another
cycle.

## Carol durable production lesson

Carol's fleece is a dominant visible identity system. Final Carol quality must
not be gated indefinitely on a naked Underbody being visually perfect.

Classify Carol geometry by final-use importance:

- **HERO_VISIBLE** — face, eyes, ears, visible hooves, tail, exposed
  transitions, fleece silhouette and any other Hero-view surface.
- **MOTION_EXPOSED** — normally hidden but plausibly revealed by approved
  motion/deformation; sufficient visual and deformation quality is required.
- **FUNCTIONAL_HIDDEN** — permanently hidden support/deformation/attachment/
  collision structure; functional correctness is required, Hero polish is not.

The v001–v013 work is not discarded. Retain canonical/authority work, numerical
registration, camera research, geometry parameters, topology diagnostics,
eye/socket lessons, intersection validators, evidence methodology, motion
inventories, and motion/camera analysis. The durable failure lesson is primarily
about prioritization, gate ordering, and repeatedly optimizing the wrong
intermediate target.

## Carol authority and routing

Current Carol execution truth:
`docs/production/carol/CAROL_PRODUCTION_STATE.md`

Current-version evidence: follow the evidence path named by
`CAROL_PRODUCTION_STATE.md`.

Geometry authority:
`assets/grimo/source/carol/approved-3d/authority.json` and
`docs/production/carol/CAROL_GEOMETRY_PARAMETERS.md`.

The current geometry authority is four FINAL / LOCKED Normal Front, Normal Side,
Skin Front, and Skin Side references plus the parameter contract, producing one
model from which Back / Top / 3Q are derived. These define geometry; visible
identity and appeal remain subordinate to the Product North Star and canonical
identity requirements.

## Mandatory Phase Tool Preflight

Before any materially new Grimo production phase or task class, ChatGPT Planner
must audit the latest pushed GitHub state and the actual Codex environment
before substantive work begins. The audit must cover the current state and
evidence, relevant contracts, `.codex/config.toml`, available repository
Skills, and applicable `codex mcp list`, `codex plugin list`, `codex plugin
marketplace list`, and `codex features list` results.

For each relevant tool, MCP, plugin, or Skill, evaluate phase relevance,
quality gain, context/token cost, selection noise, side-effect risk,
reproducibility, and whether built-in shell or repository scripts are better.
Choose the minimum sufficient toolset for that phase; do not preserve or disable
tools by habit.

ChatGPT Planner must then issue a dedicated Codex Luna configuration prompt
before the production prompt. Use project-scoped configuration where supported,
disable unused MCP servers/tools by their actual discovered IDs, avoid global
uninstall when project scope is sufficient, and restart/stop before production
if configuration changes require reload. Re-audit at every phase transition;
the current geometry toolset is not permanent.

The latest pushed GitHub state is the ChatGPT↔Codex handoff boundary.
