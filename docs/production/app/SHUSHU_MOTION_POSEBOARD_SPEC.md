# Shushu Motion Poseboard — Key-Pose Image Generation Contract

**2026-10-18 · DESIGN / HUMAN POSE REVIEW PENDING.** Implements [Motion Bible v002](../../grimo/knowledge/character-experience/SHUSHU_MOTION_BIBLE_V002.md) and [Camera Guide](../../grimo/knowledge/character-experience/SHUSHU_CAMERA_LANGUAGE_AND_SHOT_GUIDE.md). This is an **image-generation plan**, not permission to generate images, 3D assets, or claim Human GO.

## 1. Authority, input package and failure boundary

Attach to EVERY image prompt: original Shushu Canonical Identity + approved body-only views actually present in assets/grimo/source/shushu and the multiview manifest + approved donor v004 render of the matching pose/view where available + approved flower v002 appearance + this exact beat. Record provenance and version. **Never feed only the previous AI image as a source**: that amplifies geometric drift. The Canonical bouquet, ambient flowers and butterflies are not automatically props; the blossom attached to the head is not the held bouquet. An image may depict a separate flower **only** after a real prop is approved. Body image must have no extra limbs, floating ornaments, typography or new costume. Preserve eye/socket, pink cheek, muzzle depth, short feet/legs, pads, plush rump and head blossom.

All images are **proposals**. Generated front, side and 3Q drawings cannot prove physical geometry, rig contact or 3D equivalence. If they disagree with canonical/donor, do **not** silently change source geometry; reject/revise the drawing and log uncertainty. Preserve originals and file hashes. Never import copyright frames from Pokémon, Paddington or Disney into this repository.

Side convention: L/R = **Shushu anatomical side**; Front faces user. Camera scale/projection consistent within board; transparent body-only art; optional flat ground/contact grid exists as a review overlay **separate** from PNG body. No black-backdrop requirement. Review labels, contact dots and timestamps are stored outside artwork.

**Mapping hazard:** The registered shushu_bodyonly_left.png/right.png denote **nose direction on the image** (screen-left versus screen-right), *not* automatically Shushu anatomical left/right! Establish actual camera-axis mapping from asset/rig before labelling a board S-left or S-right; never silently flip an approved view and call it proven anatomy. See the multiview asset register.

## 2. Pose and shot definitions

**F** = Front full-body identity and body control. **S** = Side full-body depth and real support. **Q** = 3/4 L or R (30–45° suggested for depth, not a fixed anatomical truth). **C** = face close of eyes, lids, head flower, cheek and muzzle. **P** = feet/rump/belly contact tight crop with known ground plane. For hero support changes F/S/Q/C/P collectively required; low-risk additive facial behaviors normally need F+C only, unless 3D issues emerge.

**Board naming:** SHS-{ID}-{variant}-V001; frame naming SHS-{ID}-{variant}-V001-Pnn-{F|S|Q|C|P}. First key-pose always P0. One **master image per named pose in F**, plus additional chosen inspection angles. Counts are **image candidates**, not clip counts or mandatory all-family generation. P and S should be placed at maximum load-transfer risk; do not generate redundant 5 angles × every frame.

**Sidecar fields:** source canonical path + approved checksum, donor commit and exact asset, source view, motion ID and pose/frame ID, phase/time in seconds [DIR], eye target (user, physical hand, actual prop, walk destination), anatomical orientation, support set [rump/belly/FL/FR/HL/HR], foot planted/swing world position (if measured; else UNKNOWN), visible flower/face/eye checklist, prop provenance, generated hash, author, date, reviewer, DRAFT/HUMAN_POSE_GO/REJECTED. Do not manufacture measurements or Human signatures.

## 3. Full 35-entry poseboard inventory

Table: **F master poses** / required **additional** S,Q,C,P / **Total** review images. Each named pose is sequential, not an equal fraction of total time. Use per-motion durations/phase intervals from Bible v002.

### A. Base postures

| ID / motion | Named F key poses (P0 onward) | F | S | Q | C | P | Total | Review hazard |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| B01 Sit Neutral | seated support → resting forepaws → restful face | 3 | 1 | 0 | 1 | 1 | 6 | true rump support, no fake four-paw squat |
| B02 Sit Attentive | sit → eye lift → slight chin raise → attentive hold | 4 | 0 | 1 | 1 | 0 | 6 | blossom not occluding eyes |
| B03 Stand Neutral | last planted step → four planted pads → stable gaze | 3 | 1 | 1 | 0 | 1 | 6 | no floating soles |
| B04 Stand Curious | stand → eye target → torso shift → watch | 4 | 1 | 1 | 1 | 1 | 8 | all body weight still supported |
| B05 Lie Rest | lowering → torso support → head nestle → rest | 4 | 2 | 1 | 0 | 1 | 8 | belly or side contact really exists |
| B06 Offer / Reach | seat → support check → paw extend → hold → retract | 5 | 1 | 1 | 1 | 1 | 9 | free paw is not load-bearing |

### B. Posture transitions — inspect critical intermediate frames, not endpoints alone

| ID | Named F key poses | F | S | Q | C | P | Total | Non-negotiable close view |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| T01 Sit→Stand | P0 rump sit; P1 intentional gaze; P2 first forepaw land; P3 both forepaws brace; P4 rump unload; P5 hind feet gather; P6 four-limb extend; P7 upright four-stand settle | 8 | 5 | 2 | 1 | 2 | 18 | S at P0/P2/P4/P5/P7; P before/after rump unload |
| T02 Stand→Sit | stand → check seat area → hindquarters lower/forebrace → first rump touch → load rump → release hands → settled | 7 | 4 | 2 | 0 | 2 | 15 | S+P seat first contact and support switch |
| T03 Sit→Lie | sit → brace forepaws → lower torso → belly/side plant → tuck limbs → rest | 6 | 4 | 1 | 0 | 2 | 13 | side/body first contact, no head dive |
| T04 Lie→Sit | lie → wake eyes → forepaw brace → raise torso → rump contact → relax paws → sit | 7 | 4 | 2 | 1 | 2 | 16 | P contact at push and at loaded rump |
| T05 Turn in Place | stand/sit → eyes rotate → select loaded side → first foot replace → second support → front-facing settle | 6 | 3 | 2 | 1 | 2 | 14 | Q from both sides; no planted paw swivel |

### C. Locomotion — world contact and body advance must agree

| ID | Named F key poses | F | S | Q | C | P | Total | Review hazard |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| L01 Walk Start | stand → destination glance/load → first swing → first plant → weight transfer | 5 | 3 | 1 | 0 | 2 | 11 | no instant full-speed root slide |
| L02 Walk Loop Calm | first contact → swing → passing → next plant → weight transfer → next swing → loop seam | 7 | 4 | 2 | 0 | 3 | 16 | annotate trial LH→LF→RH→RF; NOT an animal fact |
| L03 Walk Loop Curious | moving → glance → short step → plant → secure observe pause → resume step → cycle seam | 7 | 4 | 2 | 1 | 2 | 16 | no observing with unloaded paw |
| L04 Walk Stop | moving → decide → last swing → last plant → decelerate → settle | 6 | 3 | 1 | 0 | 2 | 12 | land before stopping, no frame freeze |
| L05 Small Adjust | stable → alternate support load → lift free paw → short move → new plant | 5 | 2 | 1 | 0 | 2 | 10 | paw not lifted under body mass |
| L06 Step Back / Hesitate | stable → uncertain glance → pre-load → rear swing → land → gentle look again | 6 | 3 | 1 | 1 | 2 | 13 | backstep not a rigid jump; 0-step hesitant variant possible |

### D. Interaction — face/intent and free-paw contact

| ID | Named F key poses | F | S | Q | C | P | Total | Preconditions |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| I01 Look Up | neutral → pupils notice → chin lift → held eye contact | 4 | 0 | 1 | 2 | 0 | 7 | gaze target exists, eye socket correct |
| I02 Approach User Slightly | four-stand → notice user → one step → second plant → near-user settled | 5 | 3 | 1 | 1 | 2 | 12 | camera stays fixed; safe-area crop proof |
| I03 Happy Touch Receive | neutral → local left/right cheek ACK → follow gaze/head → response hold → released afterglow | 5 | 1 | 1 | 3 | 0 | 10 | separately assess left→right redirect; no snap |
| I04 Flower Cuddle | seated + approved separate prop → inspect → cradle → hold → release | 5 | 2 | 1 | 1 | 1 | 10 | **BLOCKED unless actual separate flower/prop exists**; head ornament remains attached |
| I05 Paw Offer / Tiny High-Five | sit → user focus → support shift → free paw up → tiny hand meet → recover | 6 | 1 | 1 | 2 | 1 | 11 | target contact only if real; arm short |
| I06 Present / Gift-like Offer | sit + real item → verify prop → brace → present → wait → retract | 6 | 2 | 1 | 1 | 1 | 11 | **BLOCKED until actual item + product contract**; non-object gesture is B06 |

### E. Emotion — no unsupported movement of planted feet

| ID | Named F key poses | F | S | Q | C | P | Total | Facial intent |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| E01 Curious | notice → pupil targeting → head tilt → hold | 4 | 0 | 1 | 2 | 0 | 7 | actual stimulus, not random |
| E02 Delighted | recognize → eyes soften → small smile → brief happy hold → recover | 5 | 0 | 1 | 2 | 0 | 8 | no exaggerated grin/jump |
| E03 Shy | face user → eye avert → chin shy dip → sideways return | 4 | 0 | 1 | 2 | 0 | 7 | avoid face disappearing |
| E04 Sleepy | attentive → slow lids → supported head lower → doze → slight waking glance | 5 | 1 | 0 | 2 | 0 | 8 | head not buried in torso |
| E05 Soft Startled | stable → pupils react → tiny recoil → support-safe recover → hold | 5 | 1 | 1 | 2 | 0 | 9 | not fearful airborne jolt |
| E06 Thinking | listen → eyes shift → held thought → tiny decision → ready | 5 | 0 | 1 | 2 | 0 | 8 | no dramatic hand-on-chin |

### F. Additive — localized shots, normal rig context

| ID | Named F key poses | F | S | Q | C | P | Total | Layer risk |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| A01 Blink | open → closing → shut → opening → open | 5 | 0 | 0 | 3 | 0 | 8 | genuine lids instead of eye disappearance |
| A02 Eye Dart | first target → shift → fixate → lid catch-up | 4 | 0 | 1 | 3 | 0 | 8 | matched pupils and socket |
| A03 Ear Lag | head initiates → ear follows → damping → rest | 4 | 1 | 2 | 1 | 0 | 8 | attachment stable |
| A04 Flower Lag | head intent → head moves/blossom follows → small optional petal lag → damp → settle | 5 | 1 | 2 | 2 | 0 | 10 | no blossom floating, cannot invent joint |
| A05 Settle / Afterglow | prior action peak → stable support → head trails → ear/flower damping → quiet | 5 | 1 | 1 | 1 | 1 | 9 | P only where preceding support changes |
| A06 Breathing / Chest Softness | relaxed → local inhale → small held chest → exhale → quiet | 5 | 2 | 1 | 1 | 1 | 10 | no global squash, planted paws stable |

**Inventory priority — product feeling first:** first create the minimum images for **B01/B02 + I03 + E01/E06 + A01/A05** that show the opening, recognition, local touch and peaceful release; obtain Human design review. In parallel use **T01** critical P0/P2/P3/P4/P5/P7 Front, selected Side at P2/P4/P5, P at P3/P4 and one face control as a **separate mechanical hero gate**; it is NOT a prerequisite for feeling alive in a supported seated pose. Only when an actual safe free paw is available should **B06/I05 invitation → WAIT → optional user response** move to production. Human gates are slice-scoped and never imply remaining families GO.

## 3.7 Emotional storyboards — human feeling is the review target (new, no independent clip count)

Existing 35 motions are **primitives**, not the audience's story. Produce the following **minimal** storyboards by composing already approved poses. Every shot uses the same immutable Canonical and real donor, including the open-eyed neutral approved 3D geometry. Seconds are proposed performance beats; do not force the user through a fixed 60-second cutscene.

| Board / felt experience to validate | Selected stills and views before making motion | Target performance/causality | Human fail cue |
| --- | --- | --- | --- |
| SB01 “初めて見て安心する” | 4 master F: B01 supported seat, self-directed gaze, user recognition, peaceful hold; 1 C eye close, 1 S rump support | 0–3s real quiet; eyes notice ~0.12–0.3s, head follows; no mandatory smile | face unrecognizable, stare/bob, sitting is fake, looks abandoned |
| SB02 “頬に触ると伝わる” | 5 F: pre-touch, contact-side local ACK, eyes/head follow, touch hold, afterglow; 3 C at ACK/hold/recovery; 1 Q for cheek depth | side-specific contact with no root jump; hold while stroking; opposite-side redirection starts from live pose | left/right swapped, eye/flower clipping, forced reset, global bounce |
| SB03 “向こうから誘ってくれた” | 5 F: independent rest, user look, **free** paw or cheek offer, WAIT, optional reciprocal response; 1 S and 1 P at raised-paw support | eyes decide → stable-supported offer → WAIT without animation loop restarting → responds **only if** player reciprocates | hand in floor while offering, artificial smiling demand, fake gift item |
| SB04 “誘いを断っても平気だった” | 3 F: invited hold, unresponded gentle withdraw, self-content quiet; 1 C recovery | ignored gesture does not imply sadness or punishment; return to peaceful autonomous attention | guilt inducing, aggressive gesture repetition, negative expression |
| SB05 “何度も撫でても同じ操り人形ではない” | 4 F sampled from 2–5min behavior: first response, later smaller response, quiet between, end; 2 C for face; optional short S if head/body affects support | personality stable, selected variation from **meaningful context**; no constant novelty | all gestures identical or random, twitching, fake tired/hunger meter |
| SB06 “タスクから戻って会えた” | 3 F: independent activity, recognition, soft welcome; 1 C for returning gaze | entry not the same pre-recorded hello every time; absence never produces negative emotion | guilt for not opening app, forced multi-second interruption |
| SB07 “食べ物・Giftと本当に心が通じる” | **Only after actual item is product-valid**: 5 F (notice, inspect, valid contact, preference/decision, afterglow) + 2 C + 1 P if paw/item bearing | eating class and preference 1–5 composited correctly; actual rare Gift separate from paw invitation | imaginary item, reward granted by decorative gesture, food dislike still consumed incorrectly |

**Storyboards are not new numbered Motion families** and share approved pose images. Initial compulsory **design review scope** is SB01/SB02, followed by SB03/SB04 when rig supports safe one-paw invitation; SB05/SB06 are runtime session acceptance; SB07 remains blocked until product items/props and semantics exist. Do not pre-generate full SB07 content or assert a mobile Human gate. The rare Gift is not mechanically equivalent to the beautiful **flower bouquet in Canonical Identity**. A bouquet must be modeled/registered as a separate asset to be held; the approved head flower is not removed or detached.

**Emotional self-test for every board:** With mute/VFX off, can a viewer correctly infer what she noticed, which cheek they touched, what she wanted, whether she felt comfortable, and why she returned to quiet? If the answer is not clear without a text label, revise the staging **before** adding extra effects or clips.

## 4. Generation instruction template

**Inputs (named and reattached):** Canonical identity exact reference, approved body-only known views, latest approved actual 3D donor comparison, exact target row and motion phase, optional prior approved pose as **continuity only**, not identity authority.

**Scene:** one original Shushu white/sakura pink cub, body only, clean transparent output with constant orthographic-like view. **Immutable features:** eyes, eye patches and socket volume, round muzzle, ear shapes, head-fixed flower v002, short limbs, plantar pads, real rump and belly shape, color/paint. **Only intentional changes:** the particular named key-pose and explicitly stated gaze/contact; do not lengthen limbs or rotate the entire character as a fake pose. **Pose record:** source posture → target posture, anatomical side, support set, planted feet, swing feet, floor orientation, eye target, motion intent, tension and delayed elements. **Negative:** missing contact, extra limb/finger, invented object, copied Pokémon/Paddington motion, new mouth/eye identity, floating blossom/flowers, glows/VFX/text. One image per targeted shot; add labels only in post-generation review board, not on character.

## 5. Human review, triage, and implementation handoff

**Before Human image gate:** overlay Canonical side-by-side for face/flower/color, donor side-by-side for body/rump/feet at comparable scale; inspect front, side and 3Q for coherent volume; indicate exact foot/seat planted timeline and phase timestamps; flag object availability. If a generated image appears pretty but uses unsupported weight, mark REJECTED. Poses with clip/camera deception cannot pass. Review contact changes in order: create support → transfer load → release old support; not the reverse.

**Deliverable manifest** to Codex after individual HUMAN_POSE_GO: approved image paths/hashes, view calibration, immutable source asset, phase/second positions [DIR], support set before/after, gaze target, anticipated secondary, known blocked operations, rejection examples and Human note. Codex must test on actual saved 3D GLB/Blender geometry: 2D art is **not** an alternate morphology source. Infeasible pose without shortening/lengthening approved limbs → design HOLD and poseboard revision, not mesh mutation.

**Review gates:** DRAFT → IMAGE_REVIEW → HUMAN_POSE_GO (design only) → BLENDER_MOTION_CANDIDATE → PLAYCANVAS_CANDIDATE → HUMAN_MOTION_GO → DEVICE/APP when available. The first positive gate never implies later acceptance.

## 6. Source links

[Motion Bible v002](../../grimo/knowledge/character-experience/SHUSHU_MOTION_BIBLE_V002.md) · [Camera Guide](../../grimo/knowledge/character-experience/SHUSHU_CAMERA_LANGUAGE_AND_SHOT_GUIDE.md) · [bear cub motion evidence v001](../../grimo/knowledge/character-experience/SHUSHU_BEAR_CUB_MOTION_RESEARCH_AND_DIRECTION.md) · [Body-only register](../../grimo/knowledge/character-production/GRIMO_BODY_ONLY_MULTIVIEW_ASSET_REGISTER.md) · [Implementation Brief](SHUSHU_MOTION_IMPLEMENTATION_BRIEF.md).
