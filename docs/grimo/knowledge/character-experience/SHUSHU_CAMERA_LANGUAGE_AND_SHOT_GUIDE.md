# Shushu Camera Language & Shot Guide — Interaction-first 3D

**Status:** SHUSHU DESIGN CONTRACT / capture-dependent numerical proposals, **not Human camera approval**. **Date:** 2026-10-18. Main implementation destination: mobile /grimo Shushu interaction; Side, 3Q and contact views are **authoring/review evidence**, not proof the runtime camera must move.

## 1. Source-based principles and their limits

### 1.1 What the official Pokémon partner interaction establishes [CRAFT/FACT]

The Pokémon Company describes a deliberate partner interaction mode, pet/feed/tickle inputs, affectionate approach, high-five and gifts, and an expressive partner face. Source: [official Let's Go partner feature](https://www.pokemon.co.jp/ex/pika_vee/story/180910_02.html). These support an **intimate user-to-companion interaction vocabulary**; they do **not** establish Shushu camera focal length or justify cloning unique poses, props, reward systems, UX or shots. Shushu's existing independent, local-only product architecture remains authoritative.

### 1.2 Grimo's pre-existing source-video measurement [LOCAL OBSERVATION]

[Full-source partner Eevee study](../research/camera-framing/GRIMO_PARTNER_EEVEE_CAMERA_FRAMING_ANALYSIS_FULL_SOURCE.md) measured three 1920×1080 / 30fps Eevee recordings. In two ordinary full-body interaction videos: neutral visible character width 0.617–0.672 of frame; face horizontal center ~0.493–0.503; neutral face vertical center 0.398–0.463. Typical interaction width 0.581–0.693; observed more expansive frames approach 0.745–0.779. In the rare close interaction a visible width 0.82–0.924 **already clips the silhouette**; this is **not** a safe default. Camera background registration showed no clear large camera following/zoom during comparable interaction segments. These are measurements on **landscape Eevee recordings**, not measured Shushu lens, view-size or modern mobile UI.

**Design inference:** borrow stable frame, strong front character attention, natural in-character forward movement, and legible close social distance. **Do not borrow** intentional Eevee ear cropping: Shushu's flower and both eyes must not be accidentally clipped. Do not transpose landscape width ratios unchanged to a portrait screen. Confirm Grimo screenshot safe areas with actual phone UI.

### 1.3 Complementary studio craft [CRAFT]

[Disney Animation](https://www.disneyanimation.com/process/animation/) prioritizes readable staging, anticipation, timing, follow-through, anatomy and weight. [Framestore Paddington performance](https://www.framestore.com/news/paddington-2-how-find-characters-performance) demonstrates thought beats, slight eye/lid decisions and selective stillness; this is **not evidence** for Shushu quadruped gait. Camera should reveal intention/eye response without replacing the character's own action with arbitrary zooms.

## 2. Shushu camera grammar [DIR]

**Primary experience rule:** **FRONT FIXED** for all normal user touching/idle/gifts. Camera orientation, FOV and center do not actively chase gaze or steps during normal interactions. Character movement and performance supply most screen-space motion. The viewer should be able to meet both eyes and read palms/flower. A natural side/3Q body turn remains physically valid, but should generally end facing the companion viewer.

**Priority order:** expressive face/eyes → head flower visibility → intentional hand or real gift interaction → full body and rump support when relevant → dramatic framing. **Exception:** locomotion and seat-change review MUST prioritize feet contact and weight even when the face becomes smaller. Changing camera framing must never hide a physical defect.

### 2.1 User camera vocabulary

| Shot ID | Use | Orientation/behaviour | Required visible features | No |
| --- | --- | --- | --- | --- |
| SH01 FRONT_HERO | Default /grimo idle, sit, look, touch | Locked perspective or orthographic-like gentle perspective; slight non-distorting downward look only if approved | Both eyes, round cheeks, flower v002, hands, feet or seat when action needs them | Zoom to fake approach; wide-angle muzzle inflation |
| SH02 FRONT_MEDIUM | Intent, joy, gaze, touch, offer | Same fixed camera or an explicitly approved **separate** medium layout; no per-frame auto-follow | Eye shape, cheek response, both free hands and blossom | Hand occluded behind head, blossom cut |
| SH03 FACE_DETAIL | Pre-production eyes, blink, shy, thinking | Crop/review camera only; optional controlled close interaction variant after UI QA | Eye sockets and upper/lower lids, mouth, flower silhouette | Use as substitute for showing unsupported foot transitions |
| SH04 FRONT_FULL_SUPPORT | Sit/stand/lie/reach, product-like hero performance | Straight-ahead full-body including rump/pads | Body outline, both forepaws, rump or soles, flower | "Cute" pose with invisible rump support |
| SH05 SIDE_CONTACT | All seat, lie and gait transitions: QA | Fixed side orthographic or long-lens perspective; no parallax ambiguity | Fore/hind contact heights, actual rump/belly floor, silhouette/profile | Perspective distortion that hides foot slide |
| SH06 FRONT_3Q_L / R | Volume, mouth, belly, wrist and bloom occlusion QA | Fixed ±30–45° **candidate** views, same normalized scale | Both eyes if plausible, cheek volume, supporting feet | One-sided proof only |
| SH07 FOOT_CONTACT | Critical stance / slide QA | Low-ish side/3Q tight shot with ground grid or marked sole contacts | All load-bearing pads/shadows and measured marks | Studio floor removed, camera shake, prop hides feet |
| SH08 TURN_PATH | Turn/small approach and screen-safe QA | Fixed front + overhead/contact inset if necessary | Before/after yaw, step re-plant, facing restoration | Root yaw without support, face off-screen |

**Naming:** SH01–SH04 are presentation/acting cameras; SH05–SH08 are **inspection** cameras. A single runtime camera may implement SH01/SH02 as UI configurations only after Human acceptance. Camera titles do not imply implementation.

### 2.2 Suggested mobile framing hypotheses (capture tests required)

All ratios below describe the **available 3D character viewport after actual header/footer, tab bar, overlays, cutouts and safe-area insets**, not the physical phone pixels. Proposed starting tests [DIR], **NOT derived quantitative Eevee facts**:

| Measurement | Proposal for Shushu | What must be validated |
| --- | --- | --- |
| Main view | portrait viewport, face X center 0.50 ±0.06 | actual UI controls do not overlay ears/flower |
| Neutral face center Y | ~0.37–0.47 (top=0) | direct eye contact, torso visibly present |
| Whole hero body visible height | 0.72–0.88 of available viewport | flower and lowest pads both stay inside |
| Primary safe visual margin | minimum ~0.04–0.07 of viewport at extreme relevant body points | hair/flower/paws not cropped during entire Motion |
| Normal interaction yaw | keep within about ±15° from front if enough facial readability | face and blossom legibility; not immutable rig limit |
| 3Q review yaw | ±35–45° | proves depth/volume rather than cheating view |
| Perspective vertical FOV | test e.g. 30–45° **only if using perspective** | avoid forehead/nose distortion, capture actual projection |
| Orthographic scale | no fixed world value before measured Shushu bounds | consistent centimeter / unit relation and UI safe frame |

If a proposed range conflicts with a real approved Canonical look, prioritize Human review over numerical adherence. Focal length in mm cannot be specified without sensor/frustum assumptions. Do not equate FOV with physical lens length. Aspect ratio changes (portrait, tablet/landscape) must preserve intentional visible features, not mechanically preserve landscape Eevee ratios.

## 3. Shot-by-motion matrix (all repertoire coverage)

B/T/L/I/E/A keys are defined in [Motion Bible v002](SHUSHU_MOTION_BIBLE_V002.md). Camera below states the **primary product shot**, then the required special review angle if any. Face detail means an authoring close shot, not an automatic runtime cut.

| Motion group and IDs | Product shot | Required review complementary shot | Framing condition |
| --- | --- | --- | --- |
| B01 Sit Neutral; B02 Sit Attentive | SH01 | SH04/SH05 once for seat | rump support and flower visible |
| B03 Stand Neutral; B04 Stand Curious | SH01 | SH05, SH07 | all paws planted; face not flat |
| B05 Lie Rest | SH04 | SH05 and contact | belly/rump actually loaded |
| B06 Offer/Reach | SH02 | SH06/SH07 if in stand | hand must not hide eyes |
| T01 Sit→Stand; T02 Stand→Sit | SH04 | SH05 + SH07 + both SH06 | show **pre-unload** contact |
| T03 Sit→Lie; T04 Lie→Sit | SH04 | SH05 + SH07 | transition has continuous support |
| T05 Turn in place | SH01 | SH06 L/R + SH08 | avoid turntable motion |
| L01 Start; L02 Calm; L03 Curious | SH01 only where movement remains visible | SH05 + SH07 + SH06 | full stride/landing readable |
| L04 Stop; L05 Adjust; L06 Step back | SH01 | SH05 + SH07 | no final sliding |
| I01 Look Up; I03 Touch; I05 High-Five | SH02 (fixed user view) | SH03; SH06 for gesture | attention and touched side can be seen |
| I02 Approach Slightly | SH01 | SH05 + SH08 | character approaches, camera does not fake move |
| I04 Flower Cuddle; I06 Gift-like Offer | SH02 when actual prop exists | SH06 + hand/prop contact | head blossom ≠ object; no unowned virtual item |
| E01 Curious; E02 Delighted; E03 Shy | SH02 | SH03/SH06 | catch intent and held beat |
| E04 Sleepy; E05 Soft Startled; E06 Thinking | SH01/SH02 | SH03 and SH05 for head support | avoid exaggerated head travel |
| A01 Blink; A02 Eye dart | SH02 | SH03 | eyes within sockets; no pupil jump |
| A03 Ear lag; A04 Flower lag | SH01 | SH03 + SH06 | attachments intact, no facial occlusion |
| A05 Settle; A06 Breathing | SH01 | SH05 + SH03 as affected | support and chest volume don't oscillate globally |

## 4. Framing rules by temporal phase

**Neutral / Intent:** show both eyes, dominant flower and the real supported pose. Eye target should match visible stimulus (viewer, hand, existing object, floor destination). **Anticipation:** avoid camera push-in; allow eyes/head to prepare within the same composition. **Commit:** if rump unload or foot landing matters, retain full feet at least in SH04; image QA additionally SH05/SH07. **Peak:** verify maximum hand/ear/flower silhouette stays visible without stretching short limbs. **Afterglow:** hold a 0.35–1.10s [DIR] unforced stable composition; no abrupt cut to default before the expression resolves.

- The active touch area is spatially consistent on the phone; camera crop must not shift tap target under the finger during a held touch.
- If SH01 cannot fit whole character without losing facial engagement, choose a **documented separate authored viewport configuration** for seat/loco sequences rather than continuous zoom. Human must accept the transition.
- Prop-based gestures remain **blocked** without a verified prop and interaction semantics. A blossom on her head is never a free floating object.
- Never insert unrelated decorative particles or black background as the sole proof of 3D quality. Source canonical ambient flowers/butterflies are art direction, not required moving prop geometry.

## 5. Human-review capture and measurable QA

For a candidate Motion, record: motion ID/variant; specific donor SHA; target version; image poseboard IDs; viewport CSS dimensions and DPR; safe insets; camera type/transform/FOV or ortho extent; target framing; clip speed; shot labels; contact set; actual 3D asset version; test device; PASS/FAIL/UNKNOWN. A static screenshot and real-time uninterrupted video must come from **saved, loaded candidate geometry**; generated 2D keyframes alone cannot clear runtime gate.

**Frame test:** neutral → intent → first relevant contact → peak → settle → one post-action quiet hold; compare identical camera before/after. Product SH01/SH02 views answer cuteness/interaction, SH05/SH07 answer mechanics. Screen masks show safe-area edges/overlay rectangles on screenshot review, not in public product.

**Fail conditions:** chopped bloom, eyes hidden or perspective-flattened, palm/flower off-screen, head/cheek deformation, shape visibly differs from Canonical, foot contact omitted from inspection, camera auto-tracking hides slide, view jump changes apparent size during touch, zoom used instead of actual approach, landscape Eevee percentages presented as mobile Shushu measurements. Any causes review **HOLD** with smallest relevant follow-up capture.

## 6. Authority / source links

1. [Pokémon Let's Go official Japanese partner interaction](https://www.pokemon.co.jp/ex/pika_vee/story/180910_02.html) [FACT/CRAFT].
2. [Full-source measured Eevee camera study in Grimo](../research/camera-framing/GRIMO_PARTNER_EEVEE_CAMERA_FRAMING_ANALYSIS_FULL_SOURCE.md) [LOCAL STUDY], with documented clipping/unknown camera model; apply inference only.
3. [Disney Animation character work](https://www.disneyanimation.com/process/animation/) [CRAFT].
4. [Framestore performance craft](https://www.framestore.com/news/paddington-2-how-find-characters-performance) [CRAFT].
5. [Shushu Motion Bible](SHUSHU_MOTION_BIBLE_V002.md) [DESIGN].
6. [Shushu Poseboard](../../../production/app/SHUSHU_MOTION_POSEBOARD_SPEC.md) and [Implementation Brief](../../../production/app/SHUSHU_MOTION_IMPLEMENTATION_BRIEF.md) [IMPLEMENTATION HANDOFF].
