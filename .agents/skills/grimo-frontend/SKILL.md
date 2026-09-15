---
name: grimo-frontend
description: Grimo-specific frontend implementation and QA rules. Use for React, Next.js, Storybook, DOM motion, accessibility, responsive UI, and visual regression work.
---

# Grimo Frontend

- `DESIGN.md` is the visual and interaction authority. This summary does not replace it.
- Build smartphone-first, touch-first UI for the four equal primary screens: Task, Calendar, Grimo, Collection. Settings is secondary navigation.
- Grimo is a game-like, reward-rich collection product, not a generic SaaS dashboard. Preserve pale blue-white material, clear information hierarchy, tactile press feedback, restrained accents, and human review of feel.
- Use Motion for React only for DOM UI: transitions, dialogs, cards, reward reveals, collection states, and navigation. Use PlayCanvas for Carol and all other 3D character/scene animation.
- Reuse behavior and accessibility mechanics, not a generic visual system: shared behavior does not imply shared appearance. Do not add MUI, Chakra, Ant Design, Bootstrap, Mantine, or the full shadcn/ui library. Add only a directly-needed unstyled accessible primitive, preferably Radix, and style it with Grimo CSS/Tailwind.
- Touch targets, keyboard focus, labels, reduced motion, safe-area insets, loading/result feedback, and interruption behavior are part of the feature.
- Every new or changed UI component gets a focused Storybook story with meaningful states and interaction coverage. Storybook is component-state QA; Playwright is screen/E2E QA.
- Run Storybook interaction and a11y checks, the Vercel React/Next.js performance review, the Vercel web-design review, and Playwright mobile screen checks. Automated a11y and screenshots are evidence, not Human Gate approval.
- `pixel-7a-like` is a viewport/performance-class target only. Never call it physical-device verification. `xiaomi-14t-pro-like` is also a browser viewport profile; physical Xiaomi 14T Pro QA must be explicitly run and reported separately.
- Initial screenshot baselines are opt-in until the relevant product screen is stable. Use `VISUAL_BASELINES_READY=1 pnpm test:visual -- --update-snapshots` to create/update them deliberately.
