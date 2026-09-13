# Pokémon TCG Pocket — UI Reference Analysis

Source: **7 user-supplied mobile screenshots captured 2026-09-13**. The screenshots themselves are third-party copyrighted media and are **not included in this repository import pack**. This document contains only derived UI observations.

## Screens observed

1. Home: very pale blue/white field, compact top utilities/profile, a large pack hero card, two smaller action cards, bottom navigation, restrained red notification dots, a missions affordance.
2. Collection (“自分のカード”): title, rounded utility/filter buttons, search/filter controls, dense card grid, persistent bottom navigation.
3. Battle landing: large hero illustration, two prominent mode cards, a few small utility actions, bottom navigation.
4. Side drawer: blurred/dimmed page underneath; large white rounded overlay sheet; profile/ID on top; vertically spaced secondary navigation items.
5. Settings: large rounded white sheet over a pale background; grouped settings, generous whitespace, teal toggles/sliders/radio controls.
6. Pack opening: immersive light-blue gradient, one large centered pack, compact top resources, one large pill CTA; chrome minimized.
7. Pack results: resource/EXP feedback at top, centered result grid, one large “next” pill, follow-up progress/challenge hint.

## Transferable design principles for Grimo

- Prefer an **airy, pale, soft-material interface** over the old dark-fantasy presentation when building the new Grimo-facing shell.
- Make the **character or current task/reward content the visual hero**; UI chrome should be sparse.
- Use generous whitespace, rounded cards/sheets, soft shadows, translucent blur where useful, and minimal hard borders.
- Keep bottom navigation for primary destinations only. Move secondary features into a drawer or overlay sheet instead of overloading the bottom bar.
- Use small notification dots sparingly for actionable state.
- For immersive Grimo/reward screens, minimize navigation chrome and center the interactive subject.
- Use consistent rounded pill CTAs for the primary next action.
- Stage reward feedback instead of showing everything at once: `action → reveal/result → resource increment → next`.
- Keep resource/status information compact (small pills/toasts) instead of building a dense game HUD.
- Settings and secondary menus should feel like lightweight sheets layered over the current context, not full visual resets.

## What not to copy

Do not copy Pokémon card art, pack art, icons, exact layouts, exact colors, branding, text, or proprietary UI assets. Use the principles above as hierarchy and interaction references only.
