# Grimo frontend production and QA toolchain

更新日: 2026-09-15 JST

この文書は、GrimoのUIを設計・実装・検査するための再現可能なローカル基盤を定義する。`DESIGN.md`、製品仕様、既存のTask/Calendar互換性がこの文書より優先される。今回の導入では本番UIを再設計していない。

## Installed tools

| Tool | Version | Purpose | Status |
| --- | --- | --- | --- |
| Next.js | 16.3.4 | App Router/PWA application runtime | installed |
| React / React DOM | 19.2.8 | UI runtime | installed |
| Tailwind CSS | 4.3.3 | Grimo-owned styling utility layer | installed |
| Storybook | 10.6.0 | isolated component catalog and preview | installed/configured |
| `@storybook/nextjs-vite` | 10.6.0 | Next.js 16 + Vite framework | installed/configured |
| `@storybook/addon-mcp` | 10.6.0 | local Storybook MCP server at `/mcp` | installed/configured |
| `@storybook/addon-vitest` | 10.6.0 | real-browser story interaction/a11y tests | installed/configured |
| `@storybook/addon-a11y` | 10.6.0 | axe-based detectable accessibility checks | installed/configured |
| `@storybook/addon-docs` | 10.6.0 | component documentation | installed/configured |
| Vitest | 4.1.11 | Storybook story test runner | installed/configured |
| Vite | 8.3.0 | Storybook build/test bundler | installed |
| Playwright | 1.63.0 | mobile browser smoke and screen screenshots | installed/configured |
| Motion for React | 13.3.0 | production DOM/React motion only | installed |
| Radix | — | optional behavior primitives | policy only; no package installed |
| Chromatic | — | hosted visual history | intentionally not installed |

All new package versions are exact-pinned in `package.json`; `pnpm-lock.yaml` remains the installation source of truth. Do not use `latest` or automatic major updates.

## Commands

```text
pnpm storybook
pnpm storybook:build
pnpm test:ui
pnpm test:visual
pnpm frontend:doctor
```

`pnpm test:ui` runs Storybook's Vitest browser project. The Storybook preview has `a11y.test = 'error'`, so detectable violations fail the test gate. Keep human review for contrast nuance, interaction feel, timing, density, reward satisfaction, and Grimo identity.

`vitest.config.ts` contains a narrowly scoped Windows compatibility plugin for Storybook's generated story guard. Storybook 10.6.0 emits a file-URL comparison that otherwise misses Vitest's Windows path and reports every story as an empty suite. The compatibility plugin runs only in the Storybook Vitest project and does not affect the application or production bundle.

`pnpm test:visual` always checks the current screen routes. Screenshot comparison is deliberately opt-in until those product screens stabilize:

```powershell
$env:VISUAL_BASELINES_READY = '1'
pnpm test:visual -- --update-snapshots
```

The Playwright projects are `pixel-7a-like` and `xiaomi-14t-pro-like`. Both are browser viewport profiles. The Pixel profile is not a physical Pixel 7a verification. The Xiaomi profile is not a substitute for a physical Xiaomi 14T Pro run; report that real-device QA separately.

Current visual routes are `/`, `/tasks`, `/calendar`, `/grimo`, and `/settings`. Future baseline scope includes `/collection`, reward flow, modal, collection detail, filter/sort, and navigation once those screens exist.

## Storybook MCP

The addon uses the official default endpoint `http://localhost:6006/mcp`. `.storybook/main.ts` enables `features.componentsManifest`, which allows the React framework to expose component documentation to agents. Storybook's runtime toolset is available only while the dev server is running.

The current Codex CLI registration is:

```powershell
codex mcp add storybook --url http://127.0.0.1:6006/mcp
```

If the server already exists, inspect it with `codex mcp list` or `codex mcp get storybook` rather than adding a duplicate. Start `pnpm storybook` from this repository root before using the endpoint. MCP is localhost-only and contains no credentials.

Figma was not reinstalled or reconfigured. The doctor reports whether the existing Codex registration is visible; authentication/read access remains an external account state. Blender, PlayCanvas Editor, and Chrome DevTools MCP registrations are likewise observed only.

## Agent Skills

Repository-local `.agents/skills/` contains:

- `grimo-frontend`: compressed operational rules for Grimo UI work; `DESIGN.md` remains authoritative.
- `stories`, `storybook-setup`, `storybook-init`, `storybook-upgrade`: official Storybook agent skills from `storybookjs/mcp`.
- `vercel-react-best-practices`: official Vercel Engineering React/Next.js implementation-performance review. The current official skill name is `vercel-react-best-practices` (its source path is `skills/react-best-practices`).
- `web-design-guidelines`: official Vercel Web Interface Guidelines review.
- `frontend-design`: existing Codex-provided skill; it remains in place and is not replaced by the Vercel skills.

`skills-lock.json` records the GitHub source paths and content hashes. Review installed skills before use and update them deliberately; do not silently auto-update.

## Responsibility and architecture rules

Motion is a production dependency because it ships only where a component imports it. Storybook, MCP, Vitest, Playwright, and a11y tooling are development-only and must never be imported by the production client. PlayCanvas owns 3D character/scene animation; Motion owns DOM UI animation.

Radix is not a visual design system here. When a real feature needs Dialog, Popover, Dropdown Menu, Tabs, Tooltip, Slider, Switch, or Scroll Area behavior, install only the directly-needed primitive (or the current tree-shakeable `radix-ui` package), exact-pin it, and style it with Grimo-owned CSS/Tailwind. Do not bulk-install primitives and do not adopt Radix's default aesthetic. Shared behavior (press/focus/dialog mechanics) is reusable; Grimo appearance (cards, buttons, rewards, navigation, collection) remains authored.

Chromatic is an optional future choice only if multiple contributors, PR visual approval, or cloud snapshot history becomes necessary. Local Storybook plus Playwright screenshots is the current baseline.

## Upgrade policy

For Next.js, React, Storybook, Motion, PlayCanvas, or MCP updates: use a dedicated `codex/` branch, update exact versions and lockfile, run lint, typecheck, unit tests, production build, Storybook build, Storybook interaction/a11y tests, Playwright smoke/visual checks, PWA checks, and then complete a Human Gate. Do not merge an upgrade on automated green alone.
