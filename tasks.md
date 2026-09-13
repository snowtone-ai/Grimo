# Current task

Updated: 2026-09-13 JST

## Current position
Milestone 0 — Foundation bootstrap prepared locally for the new `snowtone-ai/Grimo` repository.

## Acceptance state
- [x] New product/repo naming fixed to Grimo
- [x] New-repo architecture and context rules established
- [x] Task/Calendar compatibility layer scaffolded from the old repo's proven behavior
- [x] `/`, `/tasks`, `/grimo`, `/calendar`, `/settings` routes scaffolded
- [x] Startup page preference (`tasks` or `grimo`) scaffolded
- [x] PixiJS 8 / Dexie / Serwist / Playwright dependencies declared
- [x] Google/Gemini integration boundaries scaffolded
- [x] CI and unified verify command declared
- [ ] `pnpm install` / lockfile generation (requires package registry access)
- [ ] `pnpm verify` on an environment with dependencies installed
- [ ] Push bootstrap commit to GitHub (connector write was blocked; local artifact is ready)
- [ ] User adds secret environment values locally/Vercel

## Next operation
After the repository files are present in GitHub/local clone: run `corepack enable`, `pnpm install`, `pnpm verify`; fix any version/API drift revealed by the actual install. Then configure Google authorized origins and Vercel environment values.

## Assumptions
- Existing `NEXT_PUBLIC_GOOGLE_CLIENT_ID` and `GEMINI_API_KEY` will be reused.
- Old production data migrates via the legacy JSON backup importer unless the final deployment intentionally reuses the exact old origin.
- No Grimo reward schema is added before the first vertical slice proves the loop.

## Verification
Verified: context entry points pass; pure Task/Calendar TypeScript compile check passes; 8/8 pure-domain compatibility tests pass under Node 22 type stripping. Full dependency install/lint/Next production build remains unverified because this isolated container cannot access the package registry.
