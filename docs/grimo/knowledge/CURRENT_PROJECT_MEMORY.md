# Grimo — Current Project Memory

This file contains durable decisions and routing only. Mutable Carol candidate,
Human Gate, evidence, blockers, and next-step facts belong exclusively to
[`CAROL_PRODUCTION_STATE.md`](../production/carol/CAROL_PRODUCTION_STATE.md).

## Durable product and architecture decisions

- Grimo is a smartphone-first PWA with four fixed main areas: Task, Calendar,
  Grimo, and Collection.
- The character architecture is Full 3D + Blender-centered production +
  GLB/glTF + PlayCanvas runtime. Archived PixiJS/2D/2.5D material is not
  current architecture.
- Carol is the first vertical slice; the remaining canonical identities follow
  only after the pipeline is validated.
- Human Gates govern visual identity, geometry, motion quality, and promotion.
  Technical checks and evidence cannot override a Human decision.

## Carol authority and routing

Current Carol production truth:
`docs/production/carol/CAROL_PRODUCTION_STATE.md`

Current-version evidence: follow the evidence path named by
`CAROL_PRODUCTION_STATE.md`.

Geometry authority:
`assets/grimo/source/carol/approved-3d/authority.json` and
`docs/production/carol/CAROL_GEOMETRY_PARAMETERS.md`.

The current authority is four FINAL / LOCKED Normal Front, Normal Side, Skin
Front, and Skin Side references plus the parameter contract, producing one
model from which Back / Top / 3Q are derived. Do not promote derived views,
historical evidence, or generated assets into authority.

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
