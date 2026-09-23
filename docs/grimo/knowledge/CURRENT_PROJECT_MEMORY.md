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

## Role-separated execution model

The production loop is operated by three explicit roles. Do not blur them.

### ChatGPT Planner — decide what must be learned next

- Audit the latest pushed GitHub state before every materially new task class.
- Restate the user-visible Product Goal and the current **decision question**.
- Convert uncertainty into a ranked risk / unknown map.
- Choose the cheapest falsifiable probe that can change a production decision.
- Define evidence, PASS / FAIL criteria, attempt limit, and the decision that
  follows each possible result **before** implementation begins.
- Prefer final-use evidence: Hero camera, representative motion, provisional
  fleece/deformation, early runtime framing, and device evidence when relevant.
- After Codex or Human evidence, decide whether to continue, target a specific
  blocker, downgrade it, or trigger Architecture Review.
- ChatGPT Planner does not treat the existence of an artifact as a reason to
  keep polishing that artifact.

### Codex Executor — build the bounded experiment or implementation

- Execute the Planner's bounded task; do not silently redefine the Product Goal
  or Architecture.
- Make the minimum sufficient implementation needed to answer the decision
  question.
- Preserve authority files and unrelated work; avoid opportunistic refactors,
  extra tests, and unrequested polish.
- Produce only the evidence needed for the specified decision, run targeted
  validation, then commit and push when allowed.
- Report factual results and uncertainty. Codex must not self-approve Human
  identity, cuteness, life, naturalness, or final companion quality.
- If the attempt limit is exhausted or evidence invalidates the premise, stop
  and hand back to ChatGPT Planner rather than starting another local attempt.

### Human — judge perceptual experience

- Judge what ultimately requires human perception: canonical identity, cuteness,
  appeal, life/presence, causal readability, naturalness, personality, and
  whether repetition or artifacts are objectionable in representative use.
- Review the closest practical evidence to the final experience: motion,
  interaction, Hero framing, and real-device runtime rather than isolated
  technical diagnostics whenever possible.
- Human FAIL overrides automated PASS for user-visible quality.
- Human should not be asked to grade permanently hidden implementation details
  unless they create a visible, motion, interaction, or runtime consequence.

### Role-separated Goal-Backward loop

```text
PRODUCT GOAL
   |
   v
[ChatGPT Planner]
Define acceptance scene / decision question / highest-risk unknown
   |
   v
[ChatGPT Planner]
Choose cheapest falsifiable probe + PASS/FAIL + attempt limit
   |
   v
[Codex]
Build bounded integrated prototype / evidence
   |
   +---------------- technical or factual evidence ----------------+
   |                                                               |
   v                                                               |
[Human]                                                            |
Judge user-visible experience when perception is required           |
   |                                                               |
   +---------------------------+-----------------------------------+
                               |
                               v
                      [ChatGPT Planner]
                 Interpret evidence and decide
                   /          |           \
                  /           |            \
       target blocker      downgrade      Architecture Review
              |                |                 |
              +----------------+-----------------+
                               |
                               v
                            [Codex]
                   next bounded implementation
                               |
                               v
                 early motion / fleece / runtime
                               |
                               v
                            [Human]
                     experience review again
                               |
                               v
                     production convergence
                               |
                               v
                  Carol Companion Gate (Human)
                               |
                               v
                  architecture freeze / expansion
```

This is a spiral, not a waterfall. Geometry, rigging, fleece, animation, export,
runtime, and device work may be revisited whenever final-use evidence exposes a
material risk.

### Gate order

Use three gate classes:

1. **Experience Gate** — highest authority for visible companion quality.
2. **Functional Gate** — deformation, interaction, export, runtime, and device
   behavior required for the experience.
3. **Technical Hygiene** — topology cleanliness, ideal hidden surfaces, and
   similar implementation quality; mandatory only when it protects Experience
   or Functional requirements.

Technical Hygiene must never become an independent reason to block downstream
probes when its final-use consequence is unknown. In that case, prototype the
final-use condition first.

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
