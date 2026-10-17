# Shushu Motion Implementation Brief — Blender / GLB / PlayCanvas

**Status:** DESIGN / HANDOFF ONLY, no code or animation production authorized by this document. **Date:** 2026-10-18 JST. **Goal:** implement the [Shushu Motion Bible v002](../../grimo/knowledge/character-experience/SHUSHU_MOTION_BIBLE_V002.md) **after** [human-reviewed poseboards](SHUSHU_MOTION_POSEBOARD_SPEC.md), preserving approved donor and real app architecture. [Camera Guide](../../grimo/knowledge/character-experience/SHUSHU_CAMERA_LANGUAGE_AND_SHOT_GUIDE.md) governs front readability. No production animation or GLB built during this docs task.

## 0. Runtime and approval baseline

- Human-specific Shushu decision: **no Tripo Animation generation**. Proposed authoring is original Blender clip/pose action + lightweight real PlayCanvas reaction controls, chosen by feasibility. Do not assume shipped C1 Motion GO.
- Approved Shushu body v004, sole pads and later accepted head flower v002 are appearance authorities; donor evidence is on codex/shushu-abc-motion-repair-v004-20261017 at c5bed8b7cf0e7963388f9d20699fedd2c08c2c44. Existing diagnostic 821-frame Action is **not** a living idle or final locomotion clip. The old Arm FK path is not an approved replacement for current Paw controls.
- Planned C1 current product branch is codex/grimo-shushu-runtime-c1-v001; exact live head, dirty state and installed packages require **fresh executor verification**. Original C1 plan [SHUSHU_APP_RUNTIME_C1_PLAN.md](SHUSHU_APP_RUNTIME_C1_PLAN.md); C2 [SHUSHU_LIVING_MOTION_C2_PLAN.md](SHUSHU_LIVING_MOTION_C2_PLAN.md). C1 loader may have custom eight-influence skin, normal calculation, Seat, Wrist and Paw purpose channels. **Never** silently overwrite or merge the donor, animation, C1/C2 branches or their source binaries. The current main is shared documents, not active rig state.
- Docs define a **behavioral contract** for 35 entries, **not** a request to implement 35 clips/252 variants immediately. Rig/channel inventory, exact bone IDs, morph controls and masking path are UNKNOWN until inspected.
- Source hierarchy: Canonical/Human/Goal√map → approved donor / actual C1 and C2 production evidence → Motion Bible/Camera/Poseboard (authoring semantics) → older DRAFTs. Human Motion, phone and release GO must remain separate.

## 1. Design-level architecture (not a forced technical framework)

**Primary concept:** a **small hierarchical contact-aware behavior controller**, with PlayCanvas Anim state graph for validated clip transitions and masked/additive layers, plus only the necessary light custom controls for actual morphs/contact/attention. The layer count is a planning envelope; group tracks if the installed runtime and donor require it. Do not create an abstraction merely to satisfy a diagram.

| Logical layer / owner | Valid content | PlayCanvas implementation candidate | Must not own |
| --- | --- | --- | --- |
| L0 Lower-body/base support | Sit/stand/lie transition, footplants and world locomotion, torso weight/seat contact | Base full-body Anim graph (override) with contact-aware external locomotion/root controller | Free hand gift/emotion override before forepaw unload |
| L1 Upper torso/head performance | Attention, supported reach, careful turn of head, local upper torso | Bone-mask where available + weighted additive or authored override with exclusive control | Feet, rump release, root travel, pelvis support |
| L2 Face | Eye targets, lids/blink, subtle mouth/cheek if actual channels exist | Dedicated face tracks or deterministic morph/shape controller; do **not** assume bone mask covers glTF morph-target weight tracks | Ground contacts, arbitrary global mesh warp |
| L3 Ear/head-flower secondary | Ear root lag and blossom attachment with tiny optional independent delay | Local additive bones/controlled attachment, only when validated | Head transform itself, unconditional flower spin or face obstruction |
| L4 Settle/afterglow/breath | Very small support-safe residual chest/ear/face motions and purposeful stillness | Context-aware additive clips or direct bounded controls | Independent support foot movement, nonphysical root breathing |

**IMPORTANT PlayCanvas distinction:** official Anim state graphs support states, transitions, weights, layers and per-layer **bone hierarchy masks**; default overlapping layers overwrite earlier values, while additive can combine. A mask is **not a promise** that arbitrary material, morph targets or custom Paw controllers blend additively. Verify actual installed PlayCanvas API/runtime with current v004 asset; add explicit safe adapter only if necessary. With overlapping upper face/root property writes, the default must be single-owner with priorities. If mask or additive behavior differs from expectation, record evidence and choose a smaller verified mixer; never assert all layers work because official docs show humanoid sample.

**Official references:** [State graph/layer blending](https://developer.playcanvas.com/user-manual/animation/anim-state-graph-assets/), [Anim component and masks](https://developer.playcanvas.com/user-manual/editor/scenes/components/anim/), [Anim layer mask guide](https://developer.playcanvas.com/user-manual/animation/anim-layer-masking/), [current AnimComponent API](https://api.playcanvas.com/engine/classes/AnimComponent.html). Exact custom project version/asset loader must be verified on execution; this design is **not** a verified integration implementation.

## 2. State grouping and transition graph

**Body state classes (choose one at a time):**
- STABLE_SIT: B01/B02, supported B06, seated I04/I05/I06 where prop/hand is real.
- STABLE_STAND: B03/B04, locomotion pending, idle gaze/expressions.
- STABLE_LIE: B05, sleepy supported rest.
- TRANSITION: T01/T02/T03/T04/T05; a transition changes contacts and owns support until the new base is valid.
- LOCOMOTION: L01→L02/L03→L04, plus supported L05/L06; root/feet are phase-owned.
- RESTRICTED_ACTION: reach/offer where support, item attachment and camera frames are explicitly validated; otherwise use only face ACK, mark BLOCKED.

**Separate non-exclusive semantic intentions (face/head layers):** IDLE, OBSERVE(E01), THINK(E06), SHY(E03), HAPPY(E02), SLEEPY(E04), GENTLE_SURPRISE(E05), TOUCH_L/R(I03), LOOK_USER(I01), afterglow(A05), breathing(A06). The implementation must not implement these as an explosion of state×emotion×posture×camera product combinations. More precisely: keep a small body graph, parametric emotion/action envelopes, and audited ownership locks.

**Example safe diagram (policy, not API spec):**

StableSit ↔ [T01 support: forepaw plant→rump unload→hind gather] ↔ StableStand ↔ [WalkStart→WalkCalm/WalkCurious→WalkStop] → StableStand;
StableSit ↔ [SitLie/LieSit contact] ↔ StableLie;
StableStand → [Turn/SmallAdjust/StepBack with planted-paw arbitration] → StableStand.
A local cheek touch may set face ACK at any time; a large paw action waits until body state reports SAFE_FREE_PAW.

**No arbitrary jump** from lying to walking / standing directly. Use confirmed transition paths or immediate face-only acknowledgment. APP_SHUTDOWN cancels gameplay input/motion, releases renderer and does not schedule another animation frame.

## 3. Contact and paw ownership protocol

Each animation sample must be able to answer:
- support set currently bearing real weight (rump, belly, FL, FR, HL, HR);
- planted paw positions/rotations in **world coordinates** and actual foot pad contact flags;
- which paw is free and whether it owns Offer/Hold/SelfContact/locomotion;
- current target gaze and scene object provenance;
- COM proxy relative to viable supports (**qualitative**, not physics-engine force claim);
- who owns pelvis, torso, head, eyes, ears, head flower and any object anchor.

**Authoring rule:** establish **new** support BEFORE releasing old. T01 must show forepaw brace before rump lifts; T02 must show rump load before free-paw presentation; walk has stance lock and swing arc; T05 uses separate support replant instead of pivoting static planted shoes. Actual 3D constraints/contact correction cannot be inferred from 2D generated poseboard. Only apply measured world locks on saved model/runtime. A deliberately slipping variant would need its own explicit narrative and separate approval; default surfaces are dry/static with grip.

**Priority / arbitration:**

1. App lifecycle and invalid-state safety (destroy/hidden/context loss).
2. Contact/seat/stance and real item attachments.
3. Planned body TRANSITION or locomotion next-safe-foot landing.
4. Local directed user response (touch ACK) and already-safe free paw action.
5. Attention gaze, head and face expressive overlay.
6. Secondary ear, blossom, breath, settle/afterglow.

This is a **priority of ownership and preemption**, not necessarily numeric layer order: L0 must own foot contacts; a later mask may not override L0 feet. An arm doing Hold cannot also participate as planted locomotion forepaw. Restore exact pose values after clip completion; never layer unbounded additive offsets on each tick.

## 4. Additive blend / mask strategy [proposal subject to proof]

- L0 body base: normalized current base pose, contact-aware root and foot corrections; no addon writes to unsupported pelvis/feet.
- L1 upper: mask tested head/neck and only torso segments that can deform safely while L0 remains stable. If a shoulder joint also bears forepaw stance, leave it in L0 until contact releases. Use **one effective owner per transform** or a proved blending rule.
- L2 face: blink and eye darts bound to current gaze; shape-key/morph path if exported/supported; if unavailable record missing channel, **do not** simulate through pupil texture deletion or large head rotate.
- L3 ear/flower: parent head transform first, delayed soft response second. A rigid flower head attachment is safer than an invented independent petal joint. Test L/R ears separately if actual rig offers them.
- L4 settle: residual movement starts from actual latest pose, at contact-compatible phase; afterglow not permanent additive bias. Breathing only local chest, no root-wide sine/squash.
- Fade-in/out weights are context-driven bounded scalars, not a fixed always-playing 5-layer oscillator. Proposed **initial testing** blend-in 0.10–0.25s for gaze/face, 0.20–0.45s for calm body overlay, settle 0.35–1.10s; if this pops or lags, adjust by actual evidence. Do not claim zoological measurement.
- Mask hierarchy paths MUST be taken from the real imported v004 hierarchy. A bone called Head in v001 notes is not proof the same active production API exports the property today. Inspect morph target inventory, glTF import and custom eight-influence renderer.

**Critical layering test:** stand on 4 feet → upper attention → blink → ear+flower delayed → release all overlays → base pose unchanged; then sit with one free forepaw → touch opposite side → current pose retained without snap or 2-paw floor release. Verify in saved GLB + actual PlayCanvas, not isolated Blender posing only.

## 4.1 Experience-directed behavior orchestration — ship feelings, not animation counts

**Human-directed adopted design goal:** on first view the character is immediately adorable and unhurried; on touch she understands the specific location; while waiting she is content on her own; a rare soft invitation shows genuine agency; repeated encounters remain recognizably the same Shushu. See [Bible v002 §2.3–2.6](../../grimo/knowledge/character-experience/SHUSHU_MOTION_BIBLE_V002.md) and [Poseboard emotional storyboards SB01–SB07](SHUSHU_MOTION_POSEBOARD_SPEC.md). This is a **contract for animation orchestration**, not an authorization to change product inventory, rewards, memory or login rules.

**Two conceptually separate state holders:**

1. **Physical state:** support posture, planted foot/contact, actual world-locked root, available free forepaw, enabled morph/bone channels. Stable transitions and locomotion have exclusive support ownership.
2. **Social/expressive state:** attention target/hold, user head/cheek touch intent, gesture type (tap/poke, slow pet, continuous stroke, back-and-forth pet), emotional intensity bounded to approved face, self-selected thought, small afterglow and safe intention to invite. This state **never invents items/rewards nor overrides physics**.

**Control sequence:** real input or independent, justified Shushu intention → evaluate support and actual target → choose **lowest safe readable gesture** → local ACK where possible → stage coherent gaze/hold/body commitment → real contact/prop if applicable → settle and meaningful quiet. Strong emotion spends more channels only if justified; ordinary calm is valuable. No periodic 35-motion carousel.

| Situation / action state | Cue and intended user reading | Selection / guard logic | Re-entry and cancellation |
| --- | --- | --- | --- |
| APP_VISIBLE_ENTER | “She's here, happily herself” | Load actual supported last safe/default pose; bounded slight recognition or calm independent gaze, do not run a compulsory multi-second welcome | Component visibility/loaded model required; route exit destroys owned timers and renderer |
| IDLE_SELF_OCCUPIED | “She is comfortable without me” | Select rare tiny gaze or ear/chest from semantic scene/user context; preserve long quiet intervals; no sound/VFX crutch | Local touch preempts immediately at face ACK level |
| TOUCH_ACK(zone, gesture) | “She felt my finger on *this* side” | Spatial hit-test with gesture and side; eyes/cheek first; support-safe head lean for slow pet; sustained stroke changes hold, **does not restart clip every frame** | Opposite side redirects from current pose; if body busy, face response without foot release |
| INTENT_INVITE | “She is asking rather than obeying” | Enter only from peaceful, stable supported pose with an available free paw or cheek presentation and no input conflict. Face and gesture visible together; no pressure | Enter WAIT, no requested response assumed |
| WAIT_FOR_RECIPROCITY | “She is patient” | Hold supported gesture ~1.5–4s *starting trial* with breathing/lid variation but no loop pulse or continuous baiting | Real reciprocal touch → warm local ACK and shared beat; timeout/ignored → nonjudgmental recover-to-idle |
| GENTLE_BOUNDARY | “She has preferences but is kind” | Upon rapid repeated poke or disfavored semantic zone (if supported), small eye/head avoidance; do not interpret touch noise as aggression | Recovery to neutral comfort, not mood penalty, affection meter or lockout |
| ACTUAL_ITEM_ACTION | “What she chooses has meaning” | Resolve product event ID, object existence, kind (Food/Wear/Secret/Gift) and compatible anchor **before** entering item stage | If invalid/unavailable, no simulated item motion or inventory change; keep simple attention |
| LEAVE_AND_RETURN | “I can come back anytime” | No fictional all-night wait or negative absence emotion; return recognized with subtle contextual variation | Task/Calendar navigation stays immediate; no extra eager 3D fetch outside /grimo |

**Selection policy:** First choose **semantic intent** (quiet/notice/ack/invite/recover/item) and **current safe posture**, then select minimal fitting repertoire primitives. Bound repeated identical gesture patterns *only when alternatives remain authentic*, not by selecting random emotion. No undocumented persistent intimacy/mood meter; short-lived pose/attention memory is animation continuity, not user-profile tracking. The permanent product contract explicitly forbids affection points and neglect penalties.

**Gesture classification boundary:** input normalization must account for portrait display dimensions, CSS pixel scales/DPR and touch speed; do not bake human thresholds into the Bible as physical ground truth. A slow pet only becomes a lean after safe hit target and resolved direction. Do not leak contact coordinates to rewards. A rapid poke can produce gentle preference feedback but never stop basic navigation or punish.

**Session-scale proof** (from real running app, not render still): (1) 0–10s open/recognition; (2) one 10–30s gentle touch→release; (3) self-initiated invite→WAIT→response and ignored variant separately; (4) at least 10 mixed short interactions without snap/copied cadence; (5) 2–5min autonomous quiet with occasional specific intention; (6) leave for Task and return without shame/friction; (7) item and Gift only when actual product event is implemented. These are **QA scenarios**, not fixed timelines or scripted in-game cutscenes.

**Release-slice rules:** Stage one can ship emotional B01/B02 + I03 + E01/E06 + localized additives on the existing stable body without requiring a fresh Sit→Stand if it would threaten current identity. However do not claim full Companion Gate until autonomous INTENT_INVITE/WAIT/reciprocation and richer gesture semantics have actual evidence. The T01 mechanical support probe remains mandatory **before** exposing sit-to-four-stand or locomotion as user-visible motion. No secret forced 3D prop dependency from a Canonical bouquet image.

## 5. Clip, state and evidence naming

**Naming principle:** short stable ASCII snake_case filenames, no ambiguous side or variant, with prefix and source ID. Examples are **proposed names**, not existing files.

| Resource | Pattern | Example |
| --- | --- | --- |
| Animation clip / GLB action | shs_{class}_{motion}_{variant}_vNNN | shs_t_sit_to_stand_default_v001 |
| Body graph state | SHS_{B/T/L}_{ID}_{UPPER_SNAKE} | SHS_T01_SIT_TO_STAND |
| Emotive envelope/controller | shs_e_{emotion}_vNNN | shs_e_thinking_v001 |
| Additive track | shs_a_{channel}_vNNN | shs_a_flower_lag_v001 |
| Pose image board | SHS-{Bible ID}-{variant}-VNNN-Pxx-F/S/Q/C/P | SHS-T01-DEFAULT-V001-P04-S |
| Evidence capture | shs_{ID}_{candidate}_{shot}_{context} | shs_T01_v001_side_rump_unload |

**Rules:** Distinguish _l / _r as **anatomical** left/right, not image mirroring; never use state names containing "." because dotted paths have special meaning in PlayCanvas asset assignment; use loop suffix only when truly seamless, and do not assume smooth blending across unpaired footfall phases. Keep duration in asset metadata/evidence and motion contract, not in clip name. Export as few distinct 3D clip assets as necessary; L02/L03 can share contact locomotion kernel with different gaze/tempo envelopes when visually valid.

**Every produced clip** gets lineage: source Canonical/donor SHA, poseboard decision, target Bible version, authored Blender Action IDs, contact interval map, export SHA, runtime import QA, a real video and explicit HUMAN/PERF/PHONE statuses. No duplicate binary rebuild of a 60MB+ donor simply to change one expression without a good reason.

## 6. Interruptibility, attention and interaction

**Tap path:** UI hit-test detects semantic left cheek/right cheek/head → small visible face-local ACK target 0–100ms [DIR target, not guarantee] → attention eyes → optional short head/cheek response only with compatible support → release from current pose → settle 0.35–1.10s. Touch screen gesture capture and mobile scroll/overlay handling must remain safe. If walking or stand-up: face ACK now, wait until safe foot plant, then full-body reaction (or politely remain local). No queued dozen touch animations after repeated taps.

**Opposite-side touch while active:** recalculate from live actual gaze/head/face/current contact; do not restart neutral or repeat beginning. New stimulus can alter target without changing protected support set. If same paw cannot reach while bearing load, suppress paw part, not contact constraints. Idle stochastic variation only affects event timing/selection inside approved bound. User inactivity never triggers punishment or arbitrary affinity decline.

**Control arbitration proof** tests: touch during T01 rump unload, touch mid L02 swing, touch mid B06 Offer, opposite left-right touch within 200ms, pause/visibility change mid blink, route exit mid walk, canceled gesture/rapid touch. Expected invariant is not maximum responsiveness of all parts; it is immediate comprehensible ACK where safe and never popping or losing contact.

## 7. Implementation order and approval gates

| Phase | Smallest acceptable candidate | GO evidence / stop |
| --- | --- | --- |
| 0. Preflight | read **actual** current donor and active C1 branch; enumerate surviving bones, rest poses, morphs, eye/ear/flower and paw/seat controllers; inspect current installed PlayCanvas behavior | produce channel availability table + identity/rig HOLD findings; no invented API |
| 1. Key-pose images | first SB01/SB02 emotional scenes on the frozen Canonical and donor, with critical F/C and S support; in parallel a separately gated T01 support probe with F/S/Q/P | HUMAN_POSE_GO for the specific family/scenario before corresponding animation; no blanket MOTION GO |
| 2. Low-risk living slice | C2-A 15–30s calm idle with meaningful silence; genuine gaze/blink/controlled soft breath/ear/flower channels **where feasible** | real product animation and identity/Human slice gate; independently of large transitions |
| 3. Mechanical hero | T01 SIT_RUMP→FORE_BRACE→RUMP_UNLOAD→HIND_GATHER→STAND_FOUR, full continuity; no new model | front/side/3Q/contact video + approved poseboard + HUMAN_MOTION_GO; if mechanics fail repair support capability only |
| 4. Return and locomotion | T02 reverse first; L01 + L02 2–4 steps + L04 stop with contact phase | stable foot plant, no slide; side and front in saved GLB + actual PlayCanvas |
| 5. Reciprocal agency | I03 gentle cheek touch + E01/E06 + A01/A02/A05, then B06/I05 invitation→WAIT→reciprocation/ignored recovery where support permits | local ACK, context-appropriate agency with gentle boundaries, no guilt, opposite-side redirection; Human judges emotional intent |
| 6. Optional expansion | supported T03/T04, L03/L05/L06, T05, I01/I02/I05; then variants/emotions/prop-conditional I04/I06 | per-family poseboard and Human Gate; defer unneeded clips |
| 7. Runtime + device | Integrate only accepted clips within visible /grimo, actual QA | compare device/browser screenshot, frame pacing, task/calendar cold-route isolation and disposal; PHONE UNKNOWN without actual device |

Order of phases **2 and 3 can be parallel in planning, not concurrent mutations of same active rig**; the user-facing C2 idle may remain a separately scoped production effort. Human poseboard needs to precede **its corresponding new motion**, not unrelated already existing approved idle evidence. Sequencing is flexible where it improves throughput without creating conflicts.

## 8. Verification matrix — minimal sufficient real evidence

**Before motion acceptance:** exact source neutral in approved camera matches donor, no eye/cheek/flower degradation; key support changes shown in continuous 1× speed front/side/3Q video (no hidden discontinuity); feet pins and rump contact visible; layer interference at peak/start/end and interrupt; GLB export/reimport and PlayCanvas screen match; post-action quiet hold. Check only change-relevant states/poses, not full regression suites for doc-only tasks.

**Runtime checks when reached:** real app /grimo canvas and state graph; no duplicate rAF while idle or destroyed; hidden tab pause/resume coherent; component disposed on route exit; Task/Calendar cold route no PlayCanvas/GLB fetch; texture materials, pads, flower and custom 8-influence/CPU normals stay consistent. Mobile performance 60fps aspirational, 30fps graceful fallback, inspect real p50/p95 frame time, additional CPU and leaks; never promote desktop simulation to Xiaomi PASS. Avoid modifying Vercel config, deploy, backend/storage or app UI shell solely for a Motion experiment.

**HOLD triggers:**
- Canonical facial/plush identity sacrificed to make bone/rig easier;
- eye/flower/hand channels claimed but missing;
- blended eye track overdrives existing gaze; flower detaches in half-turn;
- planted paw slides or rump never touches during sit;
- exported animation drops custom skinning/normal data;
- runtime contradicts Blender, camera hides contact or user tap jumps neutral;
- unapproved prop/reward appears;
- phone not tested but labelled PASS;
- Human review says unnatural, unsettling, uncanny or not Shushu.
No invented evidence. Human owns last visual/experience approval.

## 9. Handoff package and file pointers

The **four-file contract** is [Motion Bible](../../grimo/knowledge/character-experience/SHUSHU_MOTION_BIBLE_V002.md), [Camera Language](../../grimo/knowledge/character-experience/SHUSHU_CAMERA_LANGUAGE_AND_SHOT_GUIDE.md), [Poseboard](SHUSHU_MOTION_POSEBOARD_SPEC.md), **this Brief**. Historical evidence remains in [Shushu bear-cub research v001](../../grimo/knowledge/character-experience/SHUSHU_BEAR_CUB_MOTION_RESEARCH_AND_DIRECTION.md); production truth requires actual donor and active execution branch. Spec is complete for design, **NOT Human Motion/PlayCanvas/Phone PASS**.

An executor reports: inspected branch+HEAD/working tree, source donor SHA and protected assets, poseboard IDs/status, actual available channel/unsupported flags, minimal implementation decision, evidence URLs, scoped commit+push, next Human gate and GO/HOLD. Avoid external image copies, chargeable Tripo, branch blind merge/rebase, or copying this document as code-generated assertions.

## 10. References

- [PlayCanvas official Anim State Graph / blending](https://developer.playcanvas.com/user-manual/animation/anim-state-graph-assets/).
- [PlayCanvas official Layer Masks](https://developer.playcanvas.com/user-manual/animation/anim-layer-masking/).
- [PlayCanvas official Anim Component](https://developer.playcanvas.com/user-manual/editor/scenes/components/anim/).
- [Motion Bible v002 + references](../../grimo/knowledge/character-experience/SHUSHU_MOTION_BIBLE_V002.md).
- [Grimo Shushu C2 planned Motion scope](SHUSHU_LIVING_MOTION_C2_PLAN.md).
- [Character Production Architecture](../../grimo/knowledge/GRIMO_CHARACTER_PRODUCTION_ARCHITECTURE.md).
