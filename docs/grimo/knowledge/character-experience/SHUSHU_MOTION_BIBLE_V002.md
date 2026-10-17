# Shushu Motion Bible v002 — Zero-Base Performance Contract

**Status:** DESIGN CONTRACT / candidate timing; Human Motion GO pending. **Date:** 2026-10-18 JST. **Scope:** Shushu only; design of full repertoire, not authorization to build all clips. **Evidence labels:** [OBS] animal keeper observation; [SCI] biomechanical study; [CRAFT] animation/game production; [LOCAL] approved Grimo state; [DIR] proposed Shushu direction; [UNKNOWN] not inspected or measured.

## 0. Authority and migration

1. Human decisions, Shushu Canonical and approved donor appearance outrank this document. Current source for identity is assets/grimo/source/shushu/ and the body-only register; approved v004 donor body/soles and subsequently accepted head-flower v002 are protected. The decorative blossom worn on the head is **not** the separate bouquet/ambient flowers seen in some Canonical artwork.
2. Higher product goals: Goal√map → GRIMO_CHARACTER_EXPERIENCE_SPEC → character production architecture → this design contract → Poseboard/Camera/Implementation Brief. Existing SHUSHU_BEAR_CUB_MOTION_RESEARCH_AND_DIRECTION.md (v001) remains the **evidence record**, not a competing full-family inventory. DRAFT four-character documents and diagnostic 821-frame Action are inspiration/test history, **not approved animation**.
3. This file is the unified **authoring specification** for new Shushu poses and motion. It does **not** declare Human animation approval, rig capabilities, phone results or release readiness. C1/C2 app contracts and live branch evidence govern actual implementation readiness; do not merge/rebase other active production branches.
4. Explicit Human decision: no Tripo Animation generation for Shushu. Create original Motion through Codex/Blender and suitable runtime controllers. No Tripo consumption.

## 1. Research plan → red team → adopted plan

**Initial v0:** review cute cub clips → borrow movie/game performance → assign durations → generate ~35 clips. **Rejected** because edited infant stumbling becomes a default gait, borrowed biped acts ruin support, precise timings would be fabricated, and clip count would exceed review capacity.

**Attack:** (a) Age/species: 3-month panda, adult grizzly, black-bear cub and fictional Shushu are different evidence classes. (b) Mechanics: pleasing front images can conceal floating paws, unsupported COM, and pelvis rising before forelimb plants. (c) Copying: Paddington, Koda and partner Eevee cannot supply Shushu-specific poses or sequences. (d) Scale: 35 entries are behavioral vocabulary, not 35 mandatory GLB files. (e) Readability: face, palms and flower require front performance but foot transition needs side/3Q. (f) Runtime: direct overlapping overrides and unavailable mask/morph channels cause pops. (g) Image handoff: synthetic poseboards can silently redesign identity and invent third limbs.

**Adopted v1:**
1. Pin identity, donor evidence, product and runtime boundary; distinguish approved and uninspected channels.
2. Retain species/age-qualified observations and cinema/game craft as separately tagged sources.
3. Define semantic posture, support and gaze contracts before timing.
4. Specify full **35-entry repertoire** as reusable behaviors and a small number of transition archetypes; time values are [DIR] intervals.
5. For every entry produce only the necessary prompt-ready views in SHUSHU_MOTION_POSEBOARD_SPEC.md; no images/animation in this documentation task.
6. Validate one hero transition and walking contacts before expanding. Stop at Human gates; revise hypotheses without modifying Canonical.
**Research limit:** Full edited zoo/movie/game videos have not been independently frame-calibrated in this v002 pass; no animal frame counts, species means or exact camera focal lengths are claimed.

## 2. Character identity and design grammar

**Shushu [DIR]:** white and Sakura-pink panda-like fantasy cub, rounded plush body with real face depth, large gentle eyes, very short arms/legs, visible pads, soft stable rump sitting, quiet curiosity and affectionate attention. She may enjoy a pause; she must not look impaired, constantly fall down, hyperactively bounce or mimic human biped locomotion. Primary facial grammar: notice → think (tiny held beat) → commit/support → action → settle → **quiet afterglow**. Use deliberate stillness. Flower v002 follows **head-local** support, with bounded independently delayed follow-through only after attachment is verified. Hands never phase through bouquet/head/abdomen.

**Evidence boundary:** Smithsonian keeper notes that walking panda cubs gather all four feet underneath before tentative steps, and surface grip varies; this is NOT a measured adult gait template. Adult bear studies supply qualitative load/plantigrade concerns, not Shushu angles. Framestore's restrained thought-first Paddington acting, Disney staging/anatomy/weight principles, and Pokémon partner interaction provide **craft language**, not motion frames.

### 2.1 Support and pose vocabulary (implementation names, not asserted donor bone names)

| Semantic state | Required physical support | Exclusions |
| --- | --- | --- |
| SIT_RUMP | Rump/rear thighs genuinely supported; forepaws resting or free; torso balances over seat | Four-paw squat disguised as sitting |
| SIT_ATTENTIVE | Same seat support with small upper torso/head attention | Float rump or lift both bearing paws |
| STAND_FOUR | Four plantigrade paws, weight within useful contacts, rounded trunk | Human upright or stretched legs |
| STAND_CURIOUS | STAND_FOUR with gaze-led small head/body angle | Hovering forepaw without support redistribution |
| LIE_REST | Torso/side or belly supported plus appropriate limbs | Belly and four paws hovering together |
| SEAT_OFFER | SIT_RUMP, one forepaw free, other paw/rump supports; real prop only if available | Offer while the same paw bears floor load |
| FORE_BRACE | One then both forepaws contact; rump or hindpaws still support | Rump airborne before front plant |
| HIND_GATHER | Rump unload → hindpaws come beneath torso sequentially | Both hindfeet slide while planted |
| REORIENT | Eyes/head first, individual support steps rotate body | Turntable root spin with sliding pads |
| STEP_CONTACT | Distinguish planted fore/hind paws from swing foot; record world lock | Paws moving with root while bearing weight |

Global notation: L/R from **Shushu anatomical perspective**, not screen side. Plan each shot with support set {rump, belly, FL, FR, HL, HR}; eyes target {user/camera, hand, actual object, destination}. COM proxy is a **qualitative implementation proxy**, not measured physical mass: keep projected mass plausibly over viable supports; contact markers and rendered shadow must corroborate.

### 2.2 Timing / motion notation and invariant

Each repertoire row defines **Purpose | Entry→Exit and total [DIR] | phases/key poses in order | gaze and body channel order | secondary and tone | camera / FAIL / variants**. Fractions of total are named **I** intent 0–15%, **A** preparation 15–35%, **K** principal action 35–75%, **S** settle 75–90%, **H** hold/afterglow 90–100%; shift phase boundaries to actual contacts, not the reverse. Rows with explicit P1/P2/P3 describe action beats, not 1:1 frame placement. 24fps is an optional authoring time grid; execution uses seconds and actual time delta. A static Base/loop uses these phases for **entry into** the posture, then holds; no forced restart when time runs out.

Universal order: eyes select relevant target → head/neck responds if needed → torso shifts only if intent/support requires → support feet place/unload before root migration → ear/head flower lag safely → settled expression. For touch, a localized ACK can legitimately precede gaze. Facial, flower, breathing and ear motion are **secondary, conditional, maskable and interruptible**; no random all-channel sinusoids. Eyes must remain in sockets, cheek and muzzle depth must survive, flower never occludes eyes. During a planted foot's contact its world position stays stable until release. Root translation occurs only when travel or physically motivated weight shift is needed. No global non-articulated squash.

## 3. Base posture library (6)

The defined **entry** is the shortest stable adjacent support state; a cold app load must preserve existing approved canonical neutral rather than teleport to a new base. These are destination poses, not mandatory standalone clips.

| ID / purpose | Entry → exit; total | Phases / key pose sequence | Gaze; head→torso→limb order | Secondary / emotion | Camera; FAIL; variant |
| --- | --- | --- | --- | --- | --- |
| B01 Sit Neutral — safe comfortable home | SIT_RUMP→SIT_RUMP; enter 0.45–0.90s, hold indefinite | I relaxed → A hip settle → K rump+rear thigh plant → S forepaws relax → H quiet | user at ease → soft hand glance optional; head calm, pelvis fixed, forepaws last | tiny breath, ear/flower follow; serene | front whole/side; FAIL squat/no rump pad; variant slight paw-rest asymmetry |
| B02 Sit Attentive — a listener | SIT_RUMP→SIT_ATTENTIVE; 0.50–0.90s, hold | I notice → A pupil lift → K tiny chin/chest tilt → S seat unchanged → H listen | eyes user→head→chest; legs/rump fixed | optional blink, 0.1–0.25s ear lag; warm curious | front medium; FAIL body levitates; variant left/right target |
| B03 Stand Neutral — ready to walk | STAND_FOUR→STAND_FOUR; 0.40–0.85s, hold | I stop → A final stance → K all four pads plant → S chest balanced → H still | destination→user optional; eyes/head then shoulder/trunk; feet planted | little tissue/breath, flower lag; steady | side + front; FAIL elongated limbs/pad skid; variant support width |
| B04 Stand Curious — explore safely | STAND_FOUR→STAND_CURIOUS; 0.55–1.15s, hold | I spot → A gaze → K mild head pitch/forequarter shift → S redistribute to all supports → H observe | target→down to step if needed; eyes→head→shoulder→minimal paw placement | ear follows, tiny flower overshoot; gently inquisitive | 3Q + feet; FAIL root lunge; variants object-height |
| B05 Lie Rest — release tension | LIE_REST→LIE_REST; 0.65–1.30s, hold | I relax → A paw tuck → K belly/side contacts floor → S muzzle relaxes → H doze | user→low ahead→rest; torso descends with support then forepaws tuck, head last | breathing and slow lids; cozy sleepy | side + front; FAIL belly float/face hidden; variant belly vs side-support after independent QA |
| B06 Offer / Reach — intentional paw gesture | SIT_RUMP/confirmed 3-point STAND→SEAT_OFFER/return; 0.80–1.55s | I choose target → A secure rump/other supports → K free paw extends → S hold offering → H retract | eyes target→paw→user; eyes→head, support torso then **free** wrist | blink/flower lag, shy kind | front medium + contact; FAIL unload bearing paw/arm stretch; variant tiny reach vs actual item conditional |

## 4. Transition library (5)

All moving support changes require a support timeline and one **side feet-contact evidence frame before rump unload**. Approximate phase windows are directorial proposals, not panda averages.

| ID / purpose | Entry → exit; total | Phases / key pose sequence | Gaze and motion chain | Secondary / emotion | Camera; FAIL; variant |
| --- | --- | --- | --- | --- | --- |
| T01 Sit→Stand — self-initiated rise | SIT_RUMP→STAND_FOUR; 2.5–3.1s | I notice 0–0.24 → A forward brace 0.20–0.52 → K front contact 0.45–0.94 → K rump unload 0.83–1.40 → K hind gather 1.16–1.72 → S four plant 1.58–2.12 → H 2.05–3.1 | eyes target→glance to planned forepaws→target; head small forward, forepaws plant, pelvis and hindfeet follow, torso rises **after** contact | ear→flower trailing, determined gentle | front/side/feet/3Q; FAIL unsupported pelvis rise/slide; fast 1.0–1.6s **only** if forepaws already planted and feet gathered |
| T02 Stand→Sit — choose seat | STAND_FOUR→SIT_RUMP; 1.9–2.9s | I decide → A look/set hind supports → K rear hips descend while front remains braced → K rump makes contact → S release front support and rest paws → H relaxed | eyes check landing→user; hind joints/hips load down, forepaws free **after** seat | cheeks settle, flower last; secure | side/front/feet; FAIL sit by merely folding foreknees or rump hovering; variant deliberate vs fatigued |
| T03 Sit→Lie — comfortable rest | SIT_RUMP→LIE_REST; 1.35–2.25s | I yawn/choose → A place forepaw → K torso lowers to belly/side contact → S tuck hind/forepaws → H eyes soften | low floor→down gaze→optional camera; front contact before seat release, torso lowers then head nestles | ears soften, quiet breath; sleepy | side/3Q contact; FAIL unsupported head dive; variant side lean with verified side contact |
| T04 Lie→Sit — wake with support | LIE_REST→SIT_RUMP; 1.65–2.70s | I blink awake → A forepaws brace → K upper torso pushes up → K pelvis rolls onto rump → S forepaws free → H watch | open eyes→hand contact→user; forepaws first, torso then rump balance then head | blink, flower lag; tender | side/front/feet; FAIL airborne push-up/abdomen collapse; variant sleepy +0.3–0.7s |
| T05 Turn in Place — redirect attention | STAND_FOUR or SIT_RUMP→same support class with yaw 10–35° proposed; 0.75–1.55s | I look → A select supporting side → K individually lift/replant paws or limited seated trunk orientation → S stabilize → H return front readability | eyes to destination→head→shoulders→stepping feet→pelvis; never rigid spindle | ear/flower phase lag; observant | front and overhead/contact +3Q; FAIL planted-paw spin/face lost; limit turn extent in touch camera |

## 5. Locomotion library (6)

**Walking contract [DIR]:** low, deliberate four-paw gait; start with a lateral-sequence candidate **LH→LF→RH→RF**, but verify actual rig, support, footfall and anatomy rather than enforce as zoological fact. Preliminary same-foot cycle 1.25–1.75s; stride 0.08–0.18 character height H; lift 0.015–0.045H. Stance contact remains world-stable, swing foot clears floor, root travels consistent with paw landing. No default hopping/trotting or repeated tumbles. These values are prototypes, not measured pandas.

| ID / purpose | Entry → exit; total | Phases / key pose sequence | Gaze; kinetic order | Secondary / emotion | Camera; FAIL; variant |
| --- | --- | --- | --- | --- | --- |
| L01 Walk Start — purposeful first step | STAND_FOUR→WALK; 0.45–1.00s | I pick target → A lean into safe supporting paws → K swing first foot short arc/plant → S transfer to planted paw → H cycle onset | eyes destination→brief placement→forward; head then support set, root accelerates **after** secure plant | ears/flower lag, focused | side+feet/3Q; FAIL instant full-speed/root skating; left/right step candidate |
| L02 Walk Loop Calm — slow padded wander | WALK→WALK; cycle 1.25–1.75s | I heading→A transfer→K each swing contact/passing/plant→S overlap body recovery→H new contact | gaze route with occasional foot check; fore/hind support sequence and torso weight are phase-linked | short chest lag/flower; calm | side, 3Q, feet; FAIL same-phase parallel limbs/dog trot/loop pop; cycle timing adjust to model |
| L03 Walk Loop Curious — pause-aware exploring | WALK→WALK; cycle 1.35–1.95s | I notice something → A head/gaze survey → K 1–2 measured short steps → S micro pause **with paws planted** → H resume | eyes side target→step spot→front; head and shoulder small rotation then body feet | micro ear response, inquisitive | front 3Q/side+feet; FAIL head turns cause legs to skate; variant curiosity triggers discrete hold not arbitrary cycle warp |
| L04 Walk Stop — settle into support | WALK→STAND_FOUR; 0.35–0.75s | I decide to stop → A choose next plant → K land swing paw → S root decelerates/contact stabilized → H gaze settle | eyes target, feet contact **before** face turns back; trunk then head | flower/ear overshoot, tranquil | side + foot close; FAIL freezing mid-swing or gliding last 10cm; phase-aware variant |
| L05 Small Adjust — one stabilizing step | STAND_FOUR/SIT_RUMP→same class; 0.35–0.85s | I feel imbalance → A load other contacts → K unweight/replant one free paw → S redistribute → H hold | glance to moved paw→user; support→paw→torso | tiny ear settle; unobtrusive | foot 3Q, side; FAIL lifts sole bearing entire load; variants FL/FR/HL/HR only feasible supports |
| L06 Step Back / Hesitate — reconsider | STAND_FOUR→STAND_FOUR; 0.75–1.45s | I pause → A small head recoil → K shift balance and replant one hind/fore paw back → S stabilize → H consider | object→foot landing→user; eyes/head before foot, torso backs up only after grip | ear held, flower delayed; cautious not fearful | 3Q + side feet; FAIL automatic jump backward/heel slide; 0-step hesitation variant |

## 6. Interaction library (6)

Rules: no backend rewards, inventory or intimacy score is implied; camera/touch and real object availability determine whether an interaction can be offered. Touch ACK target 0–100ms (design objective, not guaranteed measured performance); a body motion may defer while contact is unsafe.

| ID / purpose | Entry → exit; total | Phases / key pose sequence | Gaze; motion order | Secondary / emotion | Camera; FAIL; variant |
| --- | --- | --- | --- | --- | --- |
| I01 Look Up — recognize user | stable SIT/STAND→same; 0.40–0.95s | I tiny eye notice → A pupils up → K chin/head tilt → S face softens → H hold | eyes upper user→head, torso only if needed; planted paws untouched | one soft blink/flower lag; affectionate | front face+medium; FAIL giraffe neck/eyes outside lids; variant seated vs standing |
| I02 Approach User Slightly — shrink social distance | STAND_FOUR→STAND_FOUR near camera; 1.45–2.70s | I gaze user → A secure support → K two short planted steps → S stop before safe frame edge → H look up | eyes user→placement→user; feet drive root not camera zoom | head/flower settle; inviting | front medium plus side feet QA; FAIL hand/flower cropped/overreach; variant one step if viewport tight |
| I03 Happy Touch Receive — touch is understood | SIT/STAND stable→same; 0.55–1.55s including visible settle | local ACK 0–0.10s → gaze 0.10–0.33 → K gentle cheek/head lean 0.25–0.75 → S return 0.2–0.55 after release → H +0.35–1.10 | touched cheek→user; localized cheek/lid, eyes→head→tiny torso only with stable feet | blink, ear/flower lag, pleasure | front face/medium; FAIL repeated re-trigger/snap/unsupported head dip; left/right redirection from **current** pose |
| I04 Flower Cuddle — affectionate object contact | SIT_RUMP→SIT_RUMP, ONLY if **separate real/approved prop** exists; 1.20–2.35s | I inspect prop → A one/both free forepaws arrange → K cradle near chest without clipping → S hold → H release | prop→own paw→user; seat stays loaded, free paws reach then head admires | soft blink/head blossom follows head; protective | front medium+side paw/prop contact; FAIL treat head flower as detachable/extra phantom bouquet; if no prop: **BLOCKED**, not fake hand clasp |
| I05 Paw Offer / Tiny High-Five — gentle social reply | SIT_RUMP→SIT_RUMP; 0.90–1.70s | I notice raised user target → A support check → K free paw rises a small distance → S brief contact/offer hold → H retract and settle | hand target→user→paw; eyes→head→free wrist; trunk stays seat-supported | tiny ear twitch/flower; delighted reserved | front full/hand close; FAIL unnaturally long arm, floating other paw; high-five requires actual target/hit response |
| I06 Present / Gift-like Offer — goodwill without imaginary reward | SIT_RUMP→SIT_RUMP; 1.35–2.55s | I check actual item → A secure item in verified anchor → K present in reachable range → S wait for response → H return | item→user; eyes/head then free arms, seat stable | soft tilt/blink; giving | front full + side item visibility; FAIL real inventory claim/no prop/clipping; without item use **non-object offer** distinct from gift |

## 7. Emotion library (6)

Emotion is a **behavioral intention + expression envelope** composed atop a valid Base and not a new locomotion state. No unsupported face controls may be assumed.

| ID / purpose | Entry → exit; total | Phases / key poses | Gaze; motion order | Secondary / tone | Camera; FAIL; variant |
| --- | --- | --- | --- | --- | --- |
| E01 Curious — inspect safely | any stable base→same; 0.65–1.45s | I see → A eyes dart → K mild head lean → S hold observation → H unwind | actual stimulus→user optional; eyes→head→tiny shoulder | one ear/flower delayed; interested | front face/3Q; FAIL random darts; standing/sitting masks |
| E02 Delighted — restrained joy | stable base→same; 0.65–1.35s | I recognize → A eyes soften → K small smile/cheek brighten and optional safe paw → S brief hold → H calm | user→hand if touched→user; face first, seat/feet unchanged unless supported | blinking/ear lag, warm | front face+full; FAIL extreme grin/jump/eye deform; intensity 0.4/0.7 proposed |
| E03 Shy — kind reticence | stable base→same; 0.80–1.55s | I attention → A gaze a little away → K chin dip → S short hold → H return sideways glance | user→diagonal down→user; pupils→lids/head, torso late | ear fold/head flower follows; gentle | 3Q face; FAIL vanish gaze for whole scene; never punitive refusal |
| E04 Sleepy — quiet state | SIT/LIE→same; 1.20–2.50s | I attention fades → A slower lids → K low head settle over supported torso → S breathing hold → H occasional glance | user→low/horizon; lids then neck/head, forepaws remain safe | low amplitude breath, ears relax | front face+side; FAIL head falls through chest, instant knockout; no involuntary periodic snap |
| E05 Soft Startled — brief surprise | stable base→same; 0.45–1.05s | I stimulus → A pupil/ear alert → K tiny head recoil with support stable → S recover → H look again | stimulus→user; eyes/ears first, head next, torso optional | flower follows with dampening; gentle not scared | front medium+side; FAIL screaming/violent leap/feet jump; stimulus strength cap |
| E06 Thinking — thought preceding action | stable base→same; 0.75–1.75s | I ambiguous input → A gaze hold → K micro head turn or little blink → S decisional stillness → H continue action | problem/target→user; eyes then tiny head, no compulsory limb | single ear lag, contemplative | front face/3Q; FAIL theatrical finger-on-chin or constant eye roll; can bridge to T/L/I |

## 8. Additive / secondary library (6)

These are **reusable expressive tracks**, not independent actions that change support; durations apply to a single event or cycle. Entry and exit are current valid Base pose with matching ownership restored.

| ID / purpose | Entry → exit; total | Phases / key poses | Gaze; channel order | Secondary / emotion | Camera; FAIL; variant |
| --- | --- | --- | --- | --- | --- |
| A01 Blink — moist living eyes | current pose→same; 0.14–0.32s | I steady→A lid descent→K natural close→S open→H restored | hold active gaze; lids only, tiny cheek allowed | calm or reactive | face close; FAIL iris vanishes/lids intersect; slow sleepy 0.25–0.50 |
| A02 Eye Dart — focus new intention | current pose→same; 0.12–0.30s | I choose → A pupillary move → K fixation → S micro lid response → H watch | actual target; pupils first, head only if held target requires | inquisitive | face close; FAIL independent eye disagreement/no semantic target; bounded degrees unverified |
| A03 Ear Lag — transmitted inertia | current pose→same; 0.16–0.48s | I head trigger→A root remains attached→K small delayed bend→S return→H still | gaze remains owned by triggering track; ear joints only | gentle response | front+3Q head; FAIL twitch orchestra/head detach; left/right context |
| A04 Flower Lag — wearable after-motion | current head pose→same; 0.20–0.62s | I head rotates → A attachment follows exactly → K small secondary petal tilt **only if rig supports** → S damp → H held attachment | gaze inherited; blossom must not become face aim | graceful | front+side head; FAIL flower floats/covers eyes/clips ear; no separate joint => rigid head-follow |
| A05 Settle / Afterglow — causal release | action last pose→new stable pose; 0.35–1.10s | I stop intent→A residual torso/facial return→K small overshoot→S damp→H quiet | last target→user optional; body support first, then head, ears, flower | tranquil | front full+side where contact; FAIL neutral snap/oscillation loop; response-dependent intensity |
| A06 Breathing / Chest Softness — life without bob | stable SIT/STAND/LIE→same; cycle 3.0–5.5s proposed | I relaxed→A inhale local upper chest→K gentle volume→S exhale→H rest pause | gaze independent; only anatomical chest/tiny torso deformation, paws/root lock | soft | side/front full; FAIL whole-body scale/floating rump; slower in sleepy state |

## 9. Composition, transition and variation contract

- **Primary states:** stable seated, attentive seated, four-stand, curious stand, rest lie, supported offer. **Transit** changes contact set; **Locomotion** alone owns moving feet/root; **Interaction** can reserve a free paw; **Emotion** modifies gaze/face/head within safe support; **Additive** uses only available isolated channels.
- Arbitration priority: immediate app dispose/safety → world contact and prop constraints → state-changing transition/footplant → directed interaction → gaze/head/face intentional act → blink/ears/flower/breath/afterglow. Never animate the same property in two unrestricted overrides. Contact-bearing paws cannot be borrowed for offering until unloaded.
- **Interruption:** Touch during locomotion gets rapid visible local ACK but cannot teleport to Sit or yank planted paw; complete next safe plant/stop then respond, or face-only response. Re-touch the other side crossfades from **current actual pose**, not default neutral.
- Variants share skeleton/key contacts, differ only in intent, target, phase stretch, restrained intensity or safe lateral preference. Do not generate all combinations as files; create variants when Human review finds repetition. No idle timer punishes neglect or silently reduces affinity.
- **Screen-safe:** For Grimo /grimo interaction, preserve front readability, face and flower and free paws; side/3Q are **review**, not mandatory runtime switching. See SHUSHU_CAMERA_LANGUAGE_AND_SHOT_GUIDE.md.
- **Animation-to-image gate:** All 35 entries have exact minimal views and contact annotations in docs/production/app/SHUSHU_MOTION_POSEBOARD_SPEC.md; generated illustrations remain DRAFT and cannot override geometry.

## 10. Fail conditions / Human review gates

| Gate | STOP/HOLD when | Minimum proof |
| --- | --- | --- |
| Identity | eye/socket, mouth, cheeks, soft face depth, pink/white impression, head flower, paw pads deviate from approved reference | same-angle canonical/approved-to-render comparison, neutral & action peak |
| Physics | planted foot slides, rump hangs without support, root changes before plant, belly/limb intersections, no meaningful support | side and feet-contact pose sequence + uninterrupted actual animation |
| Acting | invisible motivation, mechanical eye darts, excessive squash/bounce, no quiet, emotion always smile | front real-time sequence with anticipation and afterglow |
| Temporal | popping at loop seams, sudden state handoff, out-of-sync blink/flowers, excessive retrigger | interruption and loop videos from actual state |
| Production | inferred bone/morph API doesn't exist, parent blend overwrites, 8-influence/normal/material mismatch | channel audit and actual saved GLB→PlayCanvas output |
| Human | motion is technically correct yet not child-bear-like, comforting or cute | Human-specific **HOLD**, not self-certified GO |
| Phone | performance/lifecycle/device review absent | PHONE UNKNOWN, never silently PASS |

Reviewer questions: Can the child-bear's **decision** be read? Does each change of support precede weight transfer? Is rump sitting real? Do eyes, flower, paws and face stay lovable **from front and side**? Does she finish an act and return to self-directed quiet? Is this still pleasant after ten repeats? Any negative answer blocks that motion only; untouched families remain design-only.

## 11. Implementation sequencing (not clip-count target)

**First** small living idle/eyes/local touch only where verified feasible (existing C2 contract); **parallel preflight** prove SIT_RUMP→FORE_BRACE→HIND_GATHER→STAND_FOUR using same donor and poseboard (without production animation until relevant Human pose approval); **then** reverse sit and 2–4 steps→stop; **then** look/approach/safe free paw; **then** rest/emotion/prop-dependent gestures. Each step separately: image poseboard → Human image gate → genuine Blender poses/contacts → actual PlayCanvas continuity → Human motion gate → optional smartphone/release gate. No full-library implementation without demonstrated usefulness.

## 12. References and factual limits

- [LOCAL] [Shushu bear-cub v001 research/evidence ledger](SHUSHU_BEAR_CUB_MOTION_RESEARCH_AND_DIRECTION.md) — detailed zoo / science / craft evidence, status and traceable original links.
- [LOCAL] [Eevee full-source camera-frame analysis](../research/camera-framing/GRIMO_PARTNER_EEVEE_CAMERA_FRAMING_ANALYSIS_FULL_SOURCE.md) — measurements of **Eevee footage**, not Shushu approved framing.
- [OBS] Smithsonian Zoo, [Xiao Qi Ji Takes His First Steps](https://nationalzoo.si.edu/animals/news/pandastory-xiao-qi-ji-takes-his-first-steps) and [Xiao Qi Ji Is On The Move](https://nationalzoo.si.edu/animals/news/pandastory-xiao-qi-ji-move).
- [SCI] [Shine et al., grizzly walking study, JEB](https://doi.org/10.1242/jeb.121806): **adult grizzlies, not panda cubs**.
- [CRAFT] [Framestore on Paddington acting](https://www.framestore.com/news/paddington-2-how-find-characters-performance); [Disney Animation principles](https://www.disneyanimation.com/process/animation/).
- [CRAFT] [Pokémon official partner interaction](https://www.pokemon.co.jp/ex/pika_vee/story/180910_02.html).
- [TECH] [PlayCanvas Anim State Graph](https://developer.playcanvas.com/user-manual/animation/anim-state-graph-assets/) and [Anim layer masks](https://developer.playcanvas.com/user-manual/animation/anim-layer-masking/).
- [UNKNOWN] No directly timed uncut cub rump→four-paw video, no cub gait-derived fixed durations, no approved production face-channel inventory; all proposed times are [DIR]. Do not claim external footage/art assets are owned by Grimo.

**Linked implementation contracts:** [Camera Guide](SHUSHU_CAMERA_LANGUAGE_AND_SHOT_GUIDE.md) · [Poseboard Spec](../../../production/app/SHUSHU_MOTION_POSEBOARD_SPEC.md) · [Implementation Brief](../../../production/app/SHUSHU_MOTION_IMPLEMENTATION_BRIEF.md).
