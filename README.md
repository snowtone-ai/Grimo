# Grimo

Grimo is a smartphone-first task-management PWA built around four original
living companions: Carol, Jill, Pino, and Shushu.

## Product direction

The product is judged by the companion experience, not by technical 3D purity.
Carol is the first vertical slice; the current character-production baseline is
**Full-Spatial 3D Living Character Architecture with View-Weighted Polish**.

```text
Experience → Valid Probe → Observe → Correct → Integrate → Observe → Productionize
```

Blender-centered authoring → GLB/glTF → PlayCanvas remains the current
implementation hypothesis. Character geometry is full-spatial by default: exterior
form must remain coherent through practical Front/3Q/Side/Rear exposure, while
visual polish is weighted toward the front Hero experience. The implementation
path remains subordinate to the Product North Star and may change through
Architecture Review when evidence requires it.

## Read before character-production work

- `docs/grimo/knowledge/GRIMO_PROJECT_KNOWLEDGE_INDEX.md`
- `docs/grimo/knowledge/GRIMO_PRODUCT_NORTH_STAR_AND_MINIMUM_REQUIREMENTS.md`
- `docs/grimo/knowledge/GRIMO_CHARACTER_EXPERIENCE_SPEC.md`
- `docs/grimo/knowledge/GRIMO_CHARACTER_PRODUCTION_ARCHITECTURE.md`
- `docs/grimo/knowledge/GRIMO_PRODUCTION_OPERATING_SYSTEM.md`
- `docs/production/carol/CAROL_PRODUCTION_STATE.md` — mutable Carol truth

Historical research and superseded production Bibles are retained under
`docs/archive/`; they are provenance, not current workflow authority.

## Main screens

- `/tasks` — Tasks
- `/calendar` — Calendar
- `/grimo` — Grimo
- Collection is a planned product surface.

## Development

```text
pnpm install
pnpm dev
```

Use targeted validation for the changed risk. `pnpm check:full` / `pnpm verify`
are broad PR/release/troubleshooting checks, not the default local completion
ritual. Specialized 3D/browser checks remain opt-in.

See `AGENTS.md` for repository execution rules.
