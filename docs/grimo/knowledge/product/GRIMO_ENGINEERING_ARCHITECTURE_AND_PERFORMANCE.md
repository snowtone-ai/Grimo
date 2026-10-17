# Grimo Engineering Architecture, Performance & UI Fidelity Contract

**Decision date:** 2026-10-17. **Status:** Implementation architecture and QA contract for new local-only, non-commercial Shushu-first Grimo. Supersedes no visual, reward or 3D canonical. This is **not** evidence that target metrics have already passed.

## 0. Hierarchy and sources

Human decisions > Canonical / Human-approved Shushu > `Goal√map.md` / `GRIMO_PRODUCT_NORTH_STAR_AND_MINIMUM_REQUIREMENTS.md` > `GRIMO_PRODUCT_FEATURE_SPEC.md` / `GRIMO_DATA_MODEL_SPEC.md` > `DESIGN.md` (UI/UX contract) > `GRIMO_LOCAL_FIRST_ARCHITECTURE.md` (persistence/deployment) > this **engineering optimization contract** > current implementation.

The latest Human preference is strong fidelity to **Pokémon TCG Pocket's whole app-shell, interaction rhythm and tactile quality**; do not substitute a generic "Pokepoke-like" skin. The already detailed `DESIGN.md` is the formal implementation authority: colors, spatial tokens, bottom nav, sheet/card/chest flows, sound, haptics, animation and QA. This engineering file defines cost/performance and modular boundaries **without replacing its tokens or accepting proprietary Pokémon assets**.

### External primary references (research, not evidence of implementation success)
1. Google Web Vitals (LCP/INP/CLS p75): https://web.dev/articles/vitals
2. Google INP / main-thread work: https://web.dev/articles/optimize-inp and https://web.dev/articles/optimize-long-tasks
3. Next.js App Router lazy loading & production: https://nextjs.org/docs/app/guides/lazy-loading and https://nextjs.org/docs/app/guides/production-checklist
4. PlayCanvas performance, GPU/memory and DPR: https://developer.playcanvas.com/user-manual/optimization/ and https://developer.playcanvas.com/user-manual/optimization/runtime-devicepixelratio/ and https://developer.playcanvas.com/user-manual/optimization/guidelines/
5. Dexie short transactions: https://dexie.org/docs/Tutorial/Best-Practices
6. MDN origin storage/eviction: https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria
7. Vercel CDN/versioned assets: https://vercel.com/docs/caching/cache-control-headers
8. The Pokémon Company, TCG Pocket tactile collecting (sound/vibration): https://corporate.pokemon.co.jp/en/topics/detail/t-28/
9. CEDEC 2025 developer presentation on TCG Pocket digital-card sound: https://cedec.cesa.or.jp/2025/timetable/detail/s67add00c6e635/

Reference-based design values are **not** claims about Pokémon's proprietary internal CSS/assets. The product may draw on observable design principles; do not ship Pokémon proprietary images, icons, card artwork, extracted sounds, font files, logos, or copied source.

## 1. Selected architecture — minimal modular monolith in the client

- **Use existing Next.js 16 / React / TypeScript app**, deployed via the existing Vercel `grimo` project. No rewrite into another SPA framework, microservices, GraphQL, online account system, managed database, realtime server or user-specific Vercel Functions.
- `src/app/` and `src/components/`: route-level UI presentation and lifecycle. Four independently navigable screens **Task / Calendar / Grimo / Collection**. Settings is secondary.
- `src/domain/`: deterministic task schedule, completion occurrence, reward eligibility, catalog, rarity and inventory transition rules. No import of Next, DOM, PlayCanvas, Dexie or components. Render representation (sprite/3D) is catalog metadata, never core reward semantics.
- `src/data/`: `GrimoLocalV1` Dexie IndexedDB, versioned migrations for future Grimo updates, unique event IDs, transactional commands, user-data backup. Transaction result, not a frame or animation, is source of truth. Grimo may need targeted observable database queries but avoid introducing global state tooling without measured necessity.
- `src/integrations/`: optional Google/Gemini boundaries isolated from core startup and offline operations. No speculative network work. **Existing root `src/app/layout.tsx` eagerly includes Google's external sign-in script**; profile and defer it until a user visits/activates relevant optional feature if feasible, rather than penalizing every core screen (separate frontend task).
- `src/3d/` or narrow feature directory: PlayCanvas **Shushu-only 3D host** with renderer, input-hit volumes, expression and motion controller; no import into task/date/domain/core layout. Canvas mount/unmount/dispose must release frame listeners, GPU resources, model/texture handles and observers.
- 2D UI and premium 2D/2.5D surroundings use React/CSS/SVG/optimized original images where fitting; world-anchored food/prop sprites may use PlayCanvas screen/world-space projections. Reserve true 3D props for justified body attachment, physical contact/occlusion or 3D ball.
- UI calls app commands and reads **saved projections**; Shushu reacts to semantic events, never awards items directly or decides durable inventory. UI can reflect a pending save immediately only if errors are reversible and surfaced.

Tradeoff rejected: a shared per-frame React store of model poses; server-central reward decisions; duplicating task state in localStorage/IndexedDB; 3D rendering to create ordinary app icons/cards; blanket canvas renderer across all screens. Future Jill/Pino are selected through character config/content, not copy-pasted screens or active three-character bundles.

## 2. Fast path — Task and Calendar are always lightweight

1. Initial navigation to Task/Calendar/Collection MUST NOT request PlayCanvas JS, GLB, 3D rig decoder or equipment; no hidden offscreen 3D rendering, perpetual requestAnimationFrame or automatic giant Shushu prefetch.
2. Render route shell/layout and relevant local data without waiting for `/grimo` 3D, optional integrations, audio decode or image catalogs that the route does not show.
3. On Grimo route, mount 3D client-only and import 3D modules **after route entry**. Display a real progress/fallback state until the validated model actually responds; never fake a loaded/interactive frozen Shushu.
4. Use versioned asset URLs + safe browser/Serwist caching with coherent invalidation. **Distinguish HTTP asset caching from IndexedDB user state**; never include user data in a public CDN response.
5. If `/grimo` fails (network/unsupported GPU/memory/GLB LFS pointer), Task/Calendar/Collection still work and data remains intact. Navigate away/back, browser visibility changes and reload must not duplicate models/listeners or accumulate GPU resources.
6. Avoid costly eager module-level effects and third-party scripts. Keep CSS/SVG interactions light; prefer opacity/transform to layout-triggering animation where appearance stays faithful to DESIGN.md.
7. Avoid one-time post-mount `getAllTasks().toArray()` as a long-lived monthly-calendar strategy when counts grow. For small data, keep simple; as real tests warrant, optimize by indexed date range plus recurrence candidates / derived projections without O(n) per frame or gratuitous state copies.
8. No broad premature refactor for “scalability”. Validate using baseline profiling, then optimize the measured bottleneck. All perf tuning must preserve canonical Shushu appearance and interaction.

## 3. Engineering targets and release measurement gates

### Google/industry external reference targets (not measured for Grimo yet)

- LCP <= **2.5 s**, INP <= **200 ms**, CLS <= **0.1** at **75th percentile** on representative mobile observations. These are Google's Web Vitals thresholds and are **not absolute guarantees** from local tests. Small personal/family traffic will not give statistically strong field p75; use repeated reproducible lab traces as evidence and label sample size.
- `DESIGN.md`: visual press acknowledgment about **16–33ms** target and SE onset target <=50ms where supported. These are **Grimo design goals**, not independently verified hardware guarantees.
- Shushu interaction **60 fps preferred**, graceful **30 fps fallback** without sacrificing eye/face, signature silhouette or touch causality. Frame-time equivalents: ~16.7ms or ~33.3ms total budget including CPU/GPU/render; benchmark 30-second idle, touch/petting, sit/return, reward/prop reveal, 5-minute revisit and route transition.
- Pixel 7a-class minimum target and Xiaomi 14T Pro owner QA. Each gate reports browser, OS, device, network profile (cold/warm/offline), DPR, frame-time distribution, jank, loading delays, battery/thermal observations, memory/resource trends and comparator before/after where available.
- Set concrete **initial bundle, image/GLB transfer, memory, paint and interaction budgets** only after representative baseline measurement. Unmeasured numbers and desktop-only results cannot be called mobile PASS. First invariant budget: **zero 3D code/GLB requests from non-Grimo screens**.
- Avoid automated 60fps “proof” from snapshots, pass/fail assertions on a lone run or comparing assets by compressed bytes alone. Record median/p95 on reproducible scenario where appropriate, separating network download/decode/upload/canvas activation.

### Technical QA gates (minimum meaningful evidence)

- **Startup:** cold/warm PWA; Task usable while Shushu uncached/offline; check root third-party scripts; mobile layout/CLS and IME on task input.
- **Input:** fast typing; repeated complete/uncomplete; quick navigation; Touch start/end vs scroll; no long main-thread stall while decoding; audio/haptic never block route or save.
- **Data:** recurrent completion key correctness and duplicate rewards across tabs; failure rollback; IndexedDB QuotaExceededError; reload and backup; no old DB import. Use short Dexie transactions and unique IndexedDB constraints; network/fetch/animation never awaited within a transaction.
- **Render:** Shushu v004 identity / Human-approved paw+flower retained under shade and motion, mouth/face readability; check GLB source hash and response magic, not Git LFS pointer. Current candidate ~62.6 MB plus equipment **is a first-class performance risk**; test preservation-safe optimization separately after baseline, never alter approved asset silently.
- **Resource lifecycle:** open/close Grimo 10 times and verify no growing live canvas, GPU texture/mesh resource inventory, listeners or recurring timers; validate device thermal/peak memory and context-loss recovery.
- **Layout fidelity:** `DESIGN.md §33` evidence is independent of perf score: matched reference viewport, pale blue-white material / 4-item nav, subtle cyan, shadows, recessed slots, cards, sheets, bottom close, pressed depth, micro glint, SFX, haptics, reduced motion, accessible text and usable focus order. Compare observation/inference/Grimo tokens honestly.
- **Storage:** Site data is origin-scoped; PWA reinstall, browser profile/domain changes, clearing data and quota eviction can lose local data. Vercel Preview hostnames are **different origins**, so users must not treat previews as holding their Production task data. Restore/export must be explicitly user-controlled. `navigator.storage.persist()` may reduce eviction but cannot replace backups.
- **Offline versioning:** Test service-worker update while an old client is still open; avoid mixing incompatible GLB/JS/cache/DB schema across releases. Use content-addressed or fixed-version asset manifest keys and backward-compatible Grimo migrations.
- **Vercel:** Confirm linked repo/production branch/build config and preview URL. CI PASS alone does not confirm deployment performance, local storage safety or Human UI quality. Release only after preview-device QA + explicit Human product GO.

## 4. Fidelity-driven frontend sequence (separate from next data task)

**Design authority:** `DESIGN.md` already contains precise Grimo CSS tokens and UX targets; do not reinvent a different theme. The current `src/app/globals.css` uses cream/green instead of specified pale blue, bottom nav only has 3 destinations, and Collection is absent. These are **verified gaps**, not permission to override the spec.

Frontend work sequence after/alongside data and Shushu foundations:
1. Extract exact DESIGN tokens into global reusable styles/primitives with minimum necessary components; correct **4 primary nav destinations** `Task | Calendar | Grimo | Collection` and shell/safe area.
2. Task and Calendar interactions remain useful, keyboard/accessible and responsive. Add task editing and real calendar navigation in their own feature tasks, preserving recurring semantics and no duplicate events.
3. Collection grid: 2 columns default on portrait, recessed undiscovered slots vs subtly raised found cards; accessible filter/sort, detailed bottom sheet, rarity and lasting discoverability.
4. Chest and reward reveal: tangible deliberate open + auto-open bypass; on task list, immediate completion feedback regardless of audio/reveal duration; original visuals/sounds.
5. Grimo screen: **front-facing Shushu remains hero**, minimal overlay, reliable touch hit routing, world-anchored Food 2.5D layers, do not obscure face/eyes, no default orbit camera.
6. Run phone-sized **side-by-side visual gate + 60fps interaction video gate** per major screen, as DESIGN §33 requires. Quality means high similarity of common UX grammar, not copied Pokémon proprietary graphics. No gate auto-passes based solely on color hex values or screenshots.

### “Almost full copy” interpretation

Replicate the **interaction structure and soft-material/tactile feel described in DESIGN.md**, including designed spacing, surface depth, pressing animation, navigation affordances, layering, collectible card rhythm and audio/haptic roles with high fidelity. Do not silently turn this into generic Tailwind/Material/dark RPG styling. A literal copyrighted sprite/sound/logo/font extraction is **not** authorized, even for a noncommercial family build. Actual pixel-level equivalence requires validated, licensed reference material and visible Human review; a prompt cannot assert similarity from prose alone.

## 5. Incremental architecture change policy

- Do **not** create service abstractions before a second use case; do not copy/paste character-specific code when meaning truly is shared; use stable IDs/immutable catalog definitions as the expansion seam for future Jill/Pino.
- Favor a small few reusable contracts (`TaskCommand`, `RewardEvent`, `CharacterEvent`, `ItemCatalogEntry`, `MediaDescriptor`) only where current code requires it; **avoid a full enterprise event bus** and speculative plugin interfaces.
- Apply observability in dev/QA first (browser performance profiling, PlayCanvas AppStats/MiniStats when compatible with installed v2.22.2, IndexedDB timing) without shipping analytics trackers or persistent sensitive telemetry by default.
- Separate three axes of readiness: **technical**, **visual Human**, **actual phone/runtime**. Any UNKNOWN is a HOLD for that axis; do not mistake CI or desktop GLB validation for production-ready.
- CI and limited per-PR tests; release gate only after app-sized scenario. No growing general-purpose full-suite burden with every change.

## 6. Next-Codex scope / model and merge

- **Now:** docs-only architecture/fidelity contract PR can be merged after diff review and CI; no app behavior, 3D or deployment.
- **Next executable Codex task:** use **GPT-6.1 Sol / Medium**, **new session**, no `/compact`. Start from current `main` and read `AGENTS.md`, `Goal√map.md`, `docs/production/Handoff.md`, Local-first Architecture and the relevant product data spec. **Bounded Gate B:** isolated `GrimoLocalV1`, Task/Calendar repos, atomic task create/complete with PENDING reward events (no reward roll or UI overhaul), targeted database concurrency/recurrence tests; commit/push dedicated PR-ready branch, no self merge.
- User's new media/fidelity/perf contract should **not** make this DB-only task load all of DESIGN.md or start editing 3D/UI. For the later frontend task, DESIGN.md + this performance file are mandatory.
- **Merge data task to main** after CI + actual task/date/recurrence/transaction integrity + changed-file inspection; perform separate frontend and Shushu route PRs. **Never bulk merge character production branch or push unverified work straight to the existing Vercel production branch.**
- Sol / High is a contingency for a concrete hard blocker, not a default token setting; no unrequested extra agent, research loop or repeated full build.
