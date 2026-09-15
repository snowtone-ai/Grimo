# Grimo Design Contract

Status: normative current baseline. Updated for Phase 0 on 2026-09-15 JST.

Grimo is a smartphone-first PWA with a pale, calm product shell and a future full-3D character experience. This document governs visible UI quality; it does not claim that unimplemented 3D behavior already exists.

## Authority

1. Current explicit product instruction
2. Canonical identity image for Carol, Jill, Pino, or Shushu
3. This document for UI and interaction design
4. Durable repository decisions
5. Measured implementation behavior
6. External references and archived research

Pokémon Trading Card Game Pocket is a grammar reference for frontend hierarchy, and Pokémon Let's Go is a reference for character interaction quality. Grimo must use its own assets, copy, and character identity.

## Product shell

- One screen has one dominant visual hero and one primary action.
- The shell uses a pale cool canvas, near-white elevated surfaces, blue-gray ink, soft borders, and aqua interaction accents.
- Primary navigation is Tasks / Grimo / Calendar. Settings is secondary navigation. Collection is a planned surface, not a Phase 0 feature.
- Frequent actions remain reachable in the bottom safe area and have at least a 44×44 CSS pixel hit target.
- Root/list contexts retain navigation; future immersive character contexts may suppress nonessential chrome without trapping the user.
- Handle safe-area insets, keyboard overlap, semantic labels, contrast, loading/empty/success/error states, and reduced motion.

## Baseline tokens

```css
:root {
  --g-canvas: #eef7fb;
  --g-surface-1: #fbfeff;
  --g-surface-2: #f3f9fc;
  --g-ink-1: #354457;
  --g-ink-2: #5c7187;
  --g-border: #d9e8f1;
  --g-action: #2bd4d3;
  --g-action-pressed: #18bec1;
  --g-action-ink: #173f4a;
  --g-notify: #f35b84;
  --g-success: #4ad9a5;
  --g-scrim: rgba(41, 61, 78, .26);
}
```

Use a 4px base grid, 16–24px phone gutters, 18px cards, 24px modals, 28px sheets, and 52–56px primary actions. Prefer color hierarchy and restrained elevation over heavy borders or decorative effects.

## Character direction

The formal character baseline is full 3D. Blender is the authoring environment, GLB/glTF is the interchange/shipping format, and PlayCanvas is the planned browser runtime. React will own route/UI/app state and the viewport host; the future 3D runtime must not own task persistence or routing.

Phase 0 deliberately contains no character renderer, model, animation, touch map, or fake production UI. Canonical identity images remain the only current visual authority until 3D production references are explicitly approved.

Future character work must preserve identity first, then touch causality, uniqueness, face/attention, timing/weight/settle, secondary motion, and only then optional VFX. Human Gate in a full-screen Chrome review is the final aesthetic acceptance authority.

## Quality boundaries

- Keep Task / Calendar behavior stable while the character architecture changes.
- Do not add reward, collection, or character databases before a dedicated product decision and migration plan.
- Effects are punctuation, not a substitute for readable body/face motion.
- Reduced motion removes amplitude first while retaining semantic state changes.
- Measure mobile browser behavior and runtime performance before optimizing or expanding scope.

## Phase 0 acceptance

The reset is complete when the active branch builds without the obsolete character runtime, `/grimo` remains a neutral route, preserved integrations/data/PWA/icon/canonical assets are verified, and no current documentation presents the old runtime as official.
