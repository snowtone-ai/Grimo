# Current task

Updated: 2026-09-14 JST

## Current position

Carol PixiJS 8 layered 2.5D vertical slice — Human Gate 1 is PASSED. The first Phase 2 idle/presence attempt was rejected at Human Gate 2 with 0/100 (motion/presence quality). Its state is preserved at `03a52a5` on `codex/carol-phase2-idle-hg2`. The Eevee-motion recovery is being completed on `codex/carol-phase2-eevee-motion-rebuild`; Human Gate 2 retry is pending human review.

## Acceptance state

- [x] Human Gate 1: PASSED; canonical Carol identity remains authoritative
- [x] Failed Human Gate 2 attempt preserved in Git and pushed
- [x] 11 distinct Pokémon Let's Go Eevee videos visually inspected in the user's YouTube Premium Chrome session
- [x] 33 complete motion episodes recorded with URLs, timestamps, observation confidence, and Carol mappings
- [x] Three-pass analysis completed for seven high-value clips
- [x] Failed constant breathing/spring motion design replaced by source-traceable authored timelines
- [x] Nine motions implemented in an Eevee motion corpus with deterministic A/B/C composition
- [x] Carol hooves remain grounded; head, ears, body, gaze, and delayed fleece use localized mesh regions
- [x] A/B/C 30-second deterministic videos and representative stills generated under ignored QA artifacts
- [x] User-provided `grimo-icon.png` moved to the owned source-asset path and emitted as PWA icon sizes
- [ ] Human Gate 2 retry judgment

## Next operation

Open `/grimo/human-gate-2?idleVariant=A` in Chrome full-screen. The human reviews A, B, and C for 30 seconds each, reports the strongest candidate and any unnatural motion timestamps, and only then decides whether Phase 2 passes. Human Gate 3 and touch reactions remain blocked.

## Acceptance criteria

- Prominent movement is traceable to an inspected Eevee clip and preserves semantic phase order.
- Stillness and quiet gaps carry weight; no generic global bob or constant sine-wave breathing drives the character.
- Partner attention is readable while Carol's face, silhouette, moon/star composition, and grounded hooves remain intact.
- Individual authored clips do not change amplitude between A/B/C; candidates differ by selection, density, and quiet gaps.
- No console/asset error, ticker/listener accumulation, resize/DPR regression, visibility regression, or reduced-motion loss of semantic life.
- Recovery remains on its own pushed branch; `main` is untouched and unmerged.

## Unresolved

- Human Gate 2 retry is deliberately pending; automated checks and self-review cannot replace the required Chrome full-screen judgment.
- The current accepted canonical is one composited texture. Mesh-region deformation can transfer timing, tilt, compression, and secondary lag, but cannot reproduce Eevee eyelid closure, independent paw presentation, or item handling; those limitations are documented and are not expanded into Gate 3.
- Pixel 7a checks use a Chromium emulation viewport (412×915, DPR 2.625 with renderer cap 2), not a physical Pixel 7a.
- `pnpm context:check` has a pre-existing repository failure because `AGENTS.md` is 5,663 bytes against its 5,500-byte budget; this task does not modify `AGENTS.md`.

## Verification

- `pnpm typecheck`: passed.
- `pnpm test`: passed (14/14).
- `GRIMO_QA_BROWSER_CHANNEL=chrome GRIMO_QA_BASE_URL=http://localhost:3001 GRIMO_QA_SAMPLE_MS=30000 pnpm qa:carol:phase2`: passed for deterministic A/B/C; average 59.81–60.01 fps, p95 17.1–17.3 ms, p99 17.4–18.1 ms, one frame over 50 ms in A and none in B/C, no console/network/asset error, one active Pixi application. Start-to-end heap deltas were +0.17–0.24 MB after the intermediate sample peak/GC. Six candidate switches ended at active 1 / mounts 14 / destroys 13 / listeners 4; visibility pause/resume, responsive resize, DPR cap, and reduced motion passed.
- `pnpm verify`: passed (typecheck, lint, 14 tests, production build).
- `pnpm context:check`: failed only on the pre-existing `AGENTS.md` 5,500-byte budget check.
- Visual self-review: 30-second videos, one-second contact sheets, and 2 fps close-up strips checked; head/body ordering, asymmetric ear delay, grounded bow, quiet gaps, and delayed fleece settle are visible without whole-image bobbing.
- Evidence: ignored `artifacts/grimo-qa/gate-2/`.
