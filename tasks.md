# Current task

Updated: 2026-09-13 JST

## Current position

Carol PixiJS 8 layered 2.5D vertical slice — Human Gate 1 approved on `codex/carol-phase1`; Gate 2 idle is next and has not started.

## Acceptance state

- [x] Foundation and production deployment configuration are present
- [x] Root `DESIGN.md` integrated as the normative frontend/interaction contract
- [x] Carol canonical + 8 implementation references visually reviewed
- [x] Canonical-preserving runtime asset pipeline and manifest added
- [x] PixiJS viewport lifecycle and responsive DPR-capped renderer implemented
- [x] Neutral/light Carol deformation and delayed-fleece basis implemented
- [x] Carol semantic-zone config added; back remains YELLOW / normal
- [x] Phase 1 telemetry contracts and frame-time instrumentation added
- [x] Focused renderer-independent tests added
- [x] `pnpm verify`
- [x] Browser QA, 30-second frame capture, route remount, and 5-minute stability loop
- [x] Human Gate 1 neutral/deformed captures and quantitative report
- [x] Human Gate 1 judgment: same Carol, canonical appeal preserved, face survives deformation

## Next operation

Gate 2 idle only: study the visible body mechanics of suitable Pikachu/Eevee gameplay footage, then replace any whole-image breathing impression with localized, grounded Carol motion. Gate 3 touch remains blocked until Gate 2 approval.

## Acceptance criteria

- Canonical identity and face remain intact in neutral/light deformation captures.
- Hooves remain visually grounded; no alpha seam, face drift, z-order, or source-scaling defect is visible.
- Runtime remounts without duplicate Pixi applications/listeners/tickers.
- Phase 1 measured frame summary is recorded; unmeasurable Pixel 7a device metrics are reported, not inferred.
- No tap/pet/reward/other-character scope is implemented before Gate 1 approval.

## Unresolved

- Gate 1 review feedback: the three identity checks passed, but a small whole-image stretch/shrink impression is not acceptable as the finished idle.
- Gate 2 must keep the hooves grounded and make breathing/body/fleece movement read as connected parts rather than uniform image scaling.
- Pixel 7a physical-device performance remains pending unless a target device becomes available.

## Verification

- `pnpm verify`: passed (typecheck, lint, 11 tests, production build).
- Production Chromium, Pixel 7a-like 412×915 at DPR 2.625 (renderer cap 2): 30 s / 1,801 frames, 60.01 fps average, p95 17.1 ms, p99 17.3 ms, frames >50 ms 0%.
- 300.631 s / 254 route remount cycles: active Pixi applications 1, mounts 255, destroys 254, pointer listeners 4, active pointers 0, reaction queue 0, cancel-after-action 0.
- Narrow 360×740, desktop 1280×900, reduced motion, DPR backing-size, safe-area/nav, route remount, console/network, neutral/light deformation visually checked.
- Evidence: ignored `artifacts/grimo-qa/gate-1/`.
