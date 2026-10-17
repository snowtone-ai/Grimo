# Shushu app runtime C1 v001 — implementation and evidence

2026-10-18 JST. Branch `codex/grimo-shushu-runtime-c1-v001`, isolated from latest GitHub main `534694dae8087dec852de0f26b472a6dcd26ca70`. Donor `codex/shushu-abc-motion-repair-v004-20261017` at `c5bed8b7cf0e7963388f9d20699fedd2c08c2c44`. No donor branch merge, model conversion, production deployment or Vercel settings change.

## Gates

| Scope | Result | Evidence / remaining decision |
| --- | --- | --- |
| Local C1 technical | **GO for the tested neutral-display slice** | Real bytes/SHA, dedicated loader, approved equipment, production PWA lazy loading, ten full mount/unmount cycles, failure/retry/context loss/download cancellation |
| Vercel delivery | **HOLD / UNKNOWN** | No deployment requested or performed. Fixed GitHub asset URLs return CORS-enabled real binaries; the app served from a Vercel hostname has not been tested |
| Human app-stage appearance | **HOLD / PENDING** | Existing body/sole/flower approval preserved. New app framing, lighting/compositing and surroundings need Human review; front capture is evidence, not self-approval |
| Xiaomi performance | **HOLD / UNKNOWN** | USB model `2407FPN8ER` detected (Xiaomi 14T Pro). Automatic approval review rejected the ADB action to open the app, with reason only `blocked by policy`. No app/device load, fps, memory or thermal PASS claimed |
| Overall C1 / merge / release | **HOLD** | Vercel and phone evidence plus Human app-stage review remain. No main merge. Living idle, motion library and release are outside C1 |

## Adopted source and delivery

Only four donor runtime modules are adopted. Eight-weight skinning, paw normals, geometry, UVs, textures and attachment transforms remain intact. App adaptations require explicit equipment URLs, use an abortable/hash-verified reader, check cancellation after native parsing, and record timings. [Runtime provenance](evidence/shushu-runtime-c1/runtime-provenance.json) records original and adopted SHA256; deformation source is byte-identical after Git LF normalization. Historical PENDING strings in donor metadata do not override the C1 plan's later Human flower approval.

| Asset | Bytes | SHA256 |
| --- | ---: | --- |
| v004 body | 62,567,088 | `a082195104713c21b9a219ff19bd9d37702486aaa4cdf2bbf2e9f0ad58b5c91f` |
| flower v002 | 1,279,984 | `ed474a714105d9a8a853d5caf1db0268acb86890589d3354e322bd9351490e41` |
| sole pads v001 | 2,582,567 | `f5c4aa2969b9b4971e3926dfede7c56cc8211091b9c074a9c67bb0738a2f21fe` |

[Delivery verification](evidence/shushu-runtime-c1/delivery.json) contains exact immutable URLs, HTTP 200, response lengths, magic, CORS and hashes. Body/flower LFS objects were fetched into the existing shared Git LFS store and their local SHA256 checked too. No extra 62MB checkout/public duplicate and no build-time LFS assumption. GLBs use `media.githubusercontent.com`; the ordinary Git PNG uses `raw.githubusercontent.com`. These are external versioned static assets usable by a Vercel-hosted app, **not proof of Vercel delivery**. The remote origin remains an availability dependency; failure is visible and retryable.

## Runtime and ownership

`ShushuStage` imports the renderer only from its mounted effect on `/grimo`; Task/Calendar/layout/data have no renderer import. Serwist explicitly excludes engine/donor chunks, including concatenated webpack modules. Cold browser tests include an active production Service Worker. The small Grimo route wrapper can be prefetched; engine, loader and 3D assets cannot.

The camera is fixed at the donor front view, with responsive orthographic fit and original ambient/key/tone mapping. Approved flower/pads are enabled by default. Pads are connected through the donor torso material; this standing front view does not expose both soles for a new visual approval. Neutral display uses no animation clip and no recurring app RAF. The pale gradient/layered floor and projected contact shadow use DOM/CSS. No touch/idle/reward functionality is represented as working.

Each mount owns its canvas, device, assets, observers and listeners. Exit/failure aborts fetches and removes the canvas/listeners/observer. PlayCanvas native parsing has no cancellation API: its device is retained only until that parse settles, then unloaded; ownership is serialized to prevent a second renderer from overlapping it. Teardown disposes donor equipment/deformation/entity/assets, drains internal device textures, destroys the Application and explicitly loses its exclusive WebGL context. The last step is necessary because Engine 2.22.2 otherwise leaves backbuffer/VAO allocations to browser GC. No user-data storage is touched.

## Verification

- Next 16.3.4 production webpack build including TypeScript: PASS. Focused ESLint: PASS. Existing local data foundation: **9/9 PASS**. Task/Calendar/DB source unchanged.
- [Production PWA lifecycle](evidence/shushu-runtime-c1/lifecycle.json): cold Task and Calendar request **zero engine/loader/GLB/equipment resources**, and both have an active Service Worker. Generated SW manifest also excludes both 3D chunks.
- Ten actual complete renders: each has one active context and 67 textures. Every exit has zero canvas, active context, live tracked buffer/texture/shader/program/framebuffer/renderbuffer/VAO/query, observer and RAF. Relevant listener count returns to baseline 2 (app-shell/browser listeners). Context counters count historical handles; `activeContexts`/`isContextLost` distinguish released GPU contexts from JavaScript handles retained by QA.
- [Fault scenarios](evidence/shushu-runtime-c1/faults.json): real HTTP 503 and HTTP 200 LFS pointer rejection, visible fallback, successful retry, forced WebGL loss/retry, and exit during a held download: PASS, no uncaught page errors. A fresh PWA profile and context-level network interception are required so the successful SW asset cache cannot mask fault injection.
- Windows desktop Chrome 155.0.8059.79, 412×915 CSS px, DPR 2, no network/CPU throttle, local production app + remote GitHub binaries. First sample: total **6.590 s**; body download **2.717 s**, body SHA **0.107 s**, GLB contract decode **0.021 s**, container parse **0.662 s**, deformation setup **0.299 s**, flower download **1.205 s**, pads download **0.205 s**, first frame submission **1.218 s**. Frame submission includes upload/shader/CPU submission; GPU-completion time is UNKNOWN. One desktop sample is neither a mobile budget nor field p75/p95.
- Sampled JS heap after exits ~202–223MB, without forced GC and including QA instrumentation. This is not process/GPU memory or proof of flat total memory. Deterministic owned GPU/context/listener disposal passes; actual phone memory/thermal/fps remain UNKNOWN. A static on-demand scene does not establish animated 30/60fps performance.

Reproduce locally with `pnpm build`, then `pnpm start --hostname 127.0.0.1 --port 3187`, then `node scripts/qa/shushu-runtime-c1.mjs`. Chrome must be installed. `C1_FAULTS_ONLY=1` reruns only recovery cases; the recorded ten-cycle artifact is separate because an earlier page-level fault injection was masked by SW cache. No extra ten-cycle run was needed after fixing the test harness.

Review [app front](evidence/shushu-runtime-c1/front.png) and [failure UI](evidence/shushu-runtime-c1/failure.png). The app front was inspected alongside [the donor approved-source front](https://github.com/snowtone-ai/Grimo/blob/c5bed8b7cf0e7963388f9d20699fedd2c08c2c44/docs/production/shushu/evidence/standard-appearance-v002/pc/f1-front.png); this does not approve the new stage or unseen views.

For phone handoff, use this same production build, USB port reverse or a reviewed Preview URL, and a fresh test origin/profile. Measure cold/warm network and parsing separately, 30s UI cadence and 5min memory/thermal trend, repeated navigation and offline failure. Record device/OS/Chrome/DPR/network and actual visible appearance. Do not clear the user's existing origin data or publish to production to obtain these measurements.
