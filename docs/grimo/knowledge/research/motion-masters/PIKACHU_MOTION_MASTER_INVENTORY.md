# PIKACHU_MOTION_MASTER_INVENTORY

> **Status:** COMPLETE — cross-video normalization of the six finished Partner Pikachu Motion Inventories.  This file does **not** re-analyze MP4 footage and does **not** add motions from outside the six formal sources.

## 0. Source / Evidence Rules

- Formal evidence is restricted to the six completed `PIKACHU_MOTION_INVENTORY_*` Markdown inventories listed in §1.
- No Web, YouTube, Partner Eevee, Pokémon general knowledge, prior consolidated Pikachu analysis, Grimo Project Knowledge, Carol specifications, or unlisted motion is used to add a Family/Variant/Occurrence.
- Source evidence labels such as `[V1]`, `[V2]`, and `[U]` are retained through source Confidence fields and are not upgraded.
- Anatomical left/right is not inferred when a source uses `screen-left` / `screen-right`.
- VFX/audio/UI are never treated as body-motion channels. System/UI-only transitions remain in the corpus only because source inventories explicitly retain them for full-video coverage.
- Duplicate exports are not separate videos. V4 duplicate copies found in Library were de-duplicated before this Master.
- Master taxonomy is `Motion Family → normalized source-grounded Variant cluster → source Occurrence(s)`. A broad local Family can be split across Master Families only when its own source already records separable phases/variants (e.g. V3 feeding/gift).

## 1. Source Corpus

| Video | Source label | Formal inventory | Local Families | Materialized size |
| --- | --- | --- | --- | --- |
| V1 | ふれあい | PIKACHU_MOTION_INVENTORY_1_【ピカブイ】ピカチュウとのふれあい【ポケモンレッツゴー ピカチュウ】_1080p30.md | 16 | 66,184 bytes |
| V2 | 怒らせると... | PIKACHU_MOTION_INVENTORY_2_【ピカブイ】ピカチュウを怒らせると...【ポケモンレッツゴー ピカチュウ】_1080p30.md | 15 | 79,869 bytes |
| V3 | ハイタッチ！ | PIKACHU_MOTION_INVENTORY_3_【ピカブイ】ピカチュウとのハイタッチ！【ポケモンレッツゴー ピカチュウ】_1080p30.md | 12 | 68,538 bytes |
| V4 | 変顔 | PIKACHU_MOTION_INVENTORY_4_【ピカブイ】ピカチュウの変顔【ポケモンレッツゴー ピカチュウ】_1080p30.md | 20 | 97,486 bytes |
| V5 | あまえる | PIKACHU_MOTION_INVENTORY_5_【ピカブイ】ピカチュウのあまえる【ポケモンレッツゴー ピカチュウ】_1080p30.md | 17 | 81,604 bytes |
| V6 | ほっぺすりすり | PIKACHU_MOTION_INVENTORY_6_【ピカブイ】ピカチュウのほっぺすりすり【ポケモンレッツゴー ピカチュウ】_1080p30.md | 18 | 71,881 bytes |

**Source inventory count:** 6  
**Total local Family candidates before Master normalization:** 98  
**Duplicate source videos counted:** 0

## 2. Executive Findings

- **Master Motion Families:** **47**. The corpus contains a compact shared core (neutral moving hold, blink, positive touch, feeding, gift, large delight) plus many single-video special/negative/autonomous phrases.
- **Normalized Master Variant clusters:** **103**. This count treats a source-local performance cluster as a Master Variant when exact cross-video clip identity cannot be proven; local subvariant labels remain verbatim in the Variant table.
- **Front-view readability:** **HIGH 34 / MEDIUM 10 / LOW 3** Master Families.
- **Most cross-video-stable mechanics:** intentional stillness/low-motion hold, face-led positive response, large bilateral forelimb delight, feeding hold→completion reaction, and bilateral gift presentation→release.
- **Most source-specific mechanics:** negative rear/side warning states, stern two-forelimb head-dip sequence, tail-region local response, close-pass/entry sequences, and several autonomous pose phrases.
- **Important non-motion:** WAIT and intentional stillness are preserved as social/state behavior rather than deleted for “not moving enough.”

## 3. Master Taxonomy Rules

1. Family identity is decided by observable mechanics + social/causal function + temporal grammar, not by name similarity.
2. L/R, amplitude, duration, expression intensity, local contact location, and settle differences stay as Variants unless mechanics/function change materially.
3. Different social function can justify separate Families even when silhouette is similar (e.g. one-paw local acknowledgement vs one-paw social WAIT offer).
4. A local Family that bundled multiple separable phases may map to more than one Master Family; the split is always documented in §33/§36.
5. Exact clip identity is never inferred across videos. Therefore Master Variants are conservative source-grounded performance clusters, not claims of shared animation assets.

## 4. Master Motion Family Catalog

| Global ID | Master Family | Category | Observable Definition | Key Variants | Video Coverage | Occurrence Count | Initiation | Lead Channel | Main Channels | Quiet Channels | Root / COM | Support | Tail Role | Temporal Form | Front View | Representative Sources | Confidence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PIKA-MF-001 | Neutral attentive intentional-stillness / low-motion moving hold | O. Intentional stillness | Front-facing or seated/standing baseline held with only subtle body/head/ear/tail corrections; not treated as a frozen frame. | 6 | 6/6 (COMMON) | V1/F02: 10 macro segments; V2/F01: 7; V3/PF-02: 7; V4/MF-01: 9; V5/F13: 9 windows; V6/F02: 4 macro + many short resets | AUTONOMOUS / SYSTEM / UNKNOWN | state / no fixed lead | eyes, head, torso, ears; tail may micro-move | forelimbs/feet usually quiet | minimal / centered | PLANTED or crop-unknown | QUIET or INDEPENDENT_MICRO | moving_hold / hold | HIGH | V1/F02; V2/F01; V3/PF-02; V4/MF-01; V5/F13; V6/F02 | V1/V2 (source qualifiers retained) |
| PIKA-MF-002 | Spontaneous isolated blink | A. Living / physiological | Brief eyelid close→reopen that the source explicitly separates from larger expression acting. | 3 | 3/6 (RECURRING) | V1/F01: ≥1 clean; V2/F02: ≥2; V3/PF-03: 2 confirmed isolated spontaneous blinks | AUTONOMOUS | eyelids | eyelids / eyes | root, limbs, torso | none | PLANTED / quiet | QUIET | pulse | HIGH | V1/F01; V2/F02; V3/PF-03 | V1 / source-direct unless noted |
| PIKA-MF-003 | Expression-linked eyelid close / half-lid / reopen transition | Q. Other | Short eyelid transition embedded in a larger expression; source explicitly does not equate these with physiological blinks. | 1 | 1/6 (SINGLE-VIDEO) | V5/F15: ≥20 embedded transitions | BOTH / UNKNOWN | eyelids | eyelids, often mouth/head/ears through parent motion | parent-dependent | none independently | parent-dependent | QUIET | pulse / transition | HIGH | V5/F15 | V1 with retained V2/U qualifiers |
| PIKA-MF-004 | Independent tail ambient micro / sweep / oscillation | C. Ear / tail micro | Tail changes position or oscillates while feet/root and most major body channels remain comparatively quiet. | 3 | 3/6 (RECURRING) | V1/F14: ≥4 clean idle repositions; V2/F03: 2 intervals; V5/F17: 2 long windows | AUTONOMOUS / BOTH | tail | tail; sometimes small root/head/ear coexistence | forelimbs/feet usually quiet | centered / low sway | PLANTED | PRIMARY_ACTION / INDEPENDENT_MICRO | moving_hold / loop-like / pulse | MEDIUM | V1/F14; V2/F03; V5/F17 | V1/V2 (source qualifiers retained) |
| PIKA-MF-005 | Ear orientation micro-correction | C. Ear / tail micro | Ear orientation changes that are retained as a micro-family when the source can separate them from larger motion. | 1 | 1/6 (SINGLE-VIDEO) | V1/F15: recurrent | BOTH | ears | ears; sometimes head | root/feet | none | PLANTED | QUIET | pulse / moving_hold | HIGH | V1/F15 | V1 / source-direct unless noted |
| PIKA-MF-006 | Sustained positive-contact content hold / soften | H. Positive touch | Positive contact state dominated by eye-close/soften, mouth state and small head/torso motion, sustained longer than a brief acknowledgement pulse. | 2 | 2/6 (LIMITED) | V1/F03: ≥29 cycles; V6/F04: 3+ | PLAYER_TRIGGERED | face / eyelids | eyelids, mouth, head, torso; ears/tail may follow | root/feet usually quiet | small / planted | PLANTED or crop-unknown | FOLLOW_THROUGH / QUIET | hold / moving_hold | HIGH | V1/F03; V6/F04 | V1 / source-direct unless noted |
| PIKA-MF-007 | Positive-touch facial response pulse / delight completion cycle | H. Positive touch | Contact-linked face-led response with eyelid/mouth change, optional head/torso recruitment, visible peak, then reopen/settle. Large full-body variants are split to PIKA-MF-024. | 8 | 6/6 (COMMON) | V1/F04: **29**; V2/F05: 11; V3/PF-04: 22 episodes including non-touch afterglow variants; 19 are touch-linked response episodes; V4/MF-04: 18; V4/MF-08: 11; V5/F02: 5; V5/F05: 7; V6/F03: at least 11 clear macro cycles | PLAYER_TRIGGERED / AFTERGLOW | face / eyelids / mouth | face, head, torso, ears/tail; forelimbs/root only in larger variants | feet/root often quiet | minimal to small | PLANTED mostly | QUIET / FOLLOW_THROUGH / AMPLIFIER | anticipation_action_settle / pulse | HIGH | V1/F04; V2/F05; V3/PF-04; V4/MF-04; V4/MF-08; V5/F02; V5/F05; V6/F03 | V1/V2 (source qualifiers retained) |
| PIKA-MF-008 | Touch-positive closed-eye head-lower content bow | D. Posture / balance / COM | Positive-contact bow-like phrase: eyes close, head lowers, ears/upper torso follow, then return; no step confirmed. | 1 | 1/6 (SINGLE-VIDEO) | V6/F05: at least 2 | PLAYER_TRIGGERED | head / eyelids | head, ears, eyelids, torso | feet/tail secondary | small forward/down | PLANTED | FOLLOW_THROUGH | anticipation_action_settle | HIGH | V6/F05 | V1 / source-direct unless noted |
| PIKA-MF-009 | Deep lateral positive-content lean with ear rotation | D. Posture / balance / COM | Head-led lateral lean under contact with strong ear reorientation and torso/COM follow, ending through recenter/settle. | 2 | 2/6 (LIMITED) | V4/MF-06: 1; V6/F08: 2 | PLAYER_TRIGGERED | head / face | head, ears, torso, forelimbs, root/COM, eyelids/mouth | feet stay quiet | lateral WEIGHT_SHIFT | PLANTED | FOLLOW_THROUGH | sequence / anticipation_action_settle | HIGH | V4/MF-06; V6/F08 | V1/V2 (source qualifiers retained) |
| PIKA-MF-010 | Two-paw cheek press / face-mug sequence | E. Forelimb / hand-like gesture | Both paws gather/press around cheek/face while facial acting changes; held as distinct from open-arm delight or cheek-level stretch. | 1 | 1/6 (SINGLE-VIDEO) | V4/MF-05: 6 | PLAYER_TRIGGERED | forelimbs / paws | both paws, face, head, torso small | feet/root | small | PLANTED | QUIET / FOLLOW | sequence | HIGH | V4/MF-05 | V1 / source-direct unless noted |
| PIKA-MF-011 | Bilateral cheek-level ecstatic stretch / head-back expansion | M. Large emotional / hero | Both forelimbs rise toward cheek/head level while face closes/opens positively and head/chest expand upward/back before a long recovery. | 1 | 1/6 (SINGLE-VIDEO) | V6/F09: 1 | PLAYER_TRIGGERED | forelimbs + face | forelimbs, head, ears, face, torso/root | feet | up/back expansion | PLANTED | FOLLOW_THROUGH | anticipation_action_settle | HIGH | V6/F09 | V1/V2 (source qualifiers retained) |
| PIKA-MF-012 | One-forelimb local acknowledgement / raise | E. Forelimb / hand-like gesture | Single forelimb/paw lifts or arcs toward the interaction side as a compact acknowledgement; not a prolonged social WAIT offer. | 4 | 4/6 (RECURRING) | V2/F12: 2; V3/PF-11: 2; V4/MF-03: 5; V6/F07: at least 3 lifts | PLAYER_TRIGGERED / UNCERTAIN | one forelimb / paw | paw, forelimb, shoulder, head/face small | other limb/root/feet | minimal to small lateral | PLANTED or crop-unknown | QUIET / FOLLOW | pulse / short sequence | HIGH | V2/F12; V3/PF-11; V4/MF-03; V6/F07 | V1 with retained V2/U qualifiers |
| PIKA-MF-013 | Interaction-linked open-mouth lateral body sway | H. Positive touch | Visible interaction accompanies open-mouth head/torso/root side-to-side sway without large arm action. | 1 | 1/6 (SINGLE-VIDEO) | V2/F13: 1 | PLAYER_TRIGGERED / interaction-linked | head/torso/root | mouth, head, torso, COM, ears, tail | forelimbs/feet | alternating lateral | PLANTED | FOLLOW_THROUGH / AMPLIFIER | sequence | HIGH | V2/F13 | V1 with retained V2/U qualifiers |
| PIKA-MF-014 | Contact-linked facial sensitivity / displeased warning state | I. Negative / boundary touch | Contact-linked narrowed/squeezed/downturned or head-away facial state; may recruit ears/head but remains distinct from a large whole-upper-body recoil. | 3 | 3/6 (RECURRING) | V2/F06: 8 intervals; V4/MF-09: 3; V5/F06: 4 | PLAYER_TRIGGERED | face / mouth / eyelids | face, head, ears; torso small | forelimbs/feet mostly quiet | minimal / small head-away | PLANTED or crop-unknown | QUIET / UNCLEAR | hold / pulse / sequence | HIGH | V2/F06; V4/MF-09; V5/F06 | V1 with retained V2/U qualifiers |
| PIKA-MF-015 | Boundary upper-body recoil / compression / withdrawal | I. Negative / boundary touch | Face-led warning progresses into a visibly larger head/upper-torso compression or withdrawal, with ears/forelimbs/tail following while support remains grounded. | 2 | 2/6 (LIMITED) | V1/F05: 2; V2/F07: 3 | PLAYER_TRIGGERED | face → head/upper torso | face, head, ears, torso, forelimbs; tail follows | hindlimbs/feet mostly quiet | down/lateral compression | PLANTED | FOLLOW_THROUGH | anticipation_action_settle | HIGH | V1/F05; V2/F07 | V1/V2 (source qualifiers retained) |
| PIKA-MF-016 | Compression → open-arm negative hero reaction | I. Negative / boundary touch | Strong negative phrase: upper body/forelimbs compress and gather, then torso/arms explosively expand/open; VFX may begin after body commit. | 1 | 1/6 (SINGLE-VIDEO) | V2/F08: 1 | PLAYER_TRIGGERED | forelimbs + torso | face, head, torso, forelimbs, root, ears, tail | hindfeet relatively quiet/occluded | large vertical compression→expansion | PLANTED / support exactness unclear | FOLLOW_THROUGH / AMPLIFIER | anticipation_action_hold | HIGH | V2/F08 | V1 with retained V2/U qualifiers |
| PIKA-MF-017 | Rear/side eyes-closed disengaged moving hold | O. Intentional stillness | Side/back-oriented eyes-closed interaction-linked hold with only small head/body corrections; front-facing meaning is weak. | 1 | 1/6 (SINGLE-VIDEO) | V2/F09: 3 | PLAYER_TRIGGERED state | none dominant | posture, head small, tail silhouette | limbs/root quiet | minimal | PLANTED | held / UNCLEAR | moving_hold | LOW | V2/F09 | V1 / source-direct unless noted |
| PIKA-MF-018 | Rear-contact glance-back warning and turn-away | I. Negative / boundary touch | From side/back contact state, visible eye opens/narrows as head turns back briefly, then closes/turns away. | 1 | 1/6 (SINGLE-VIDEO) | V2/F10: 2 | PLAYER_TRIGGERED | head / eyes | eye, head, slight upper torso, ears | limbs/tail mostly quiet | minimal rotational | PLANTED | QUIET | sequence | LOW | V2/F10 | V1/V2 (source qualifiers retained) |
| PIKA-MF-019 | Side/back → front reorientation | P. Transition | Whole-body/root and head rotate from side/back staging to front; exact foot stepping may be occluded. | 1 | 1/6 (SINGLE-VIDEO) | V2/F11: 1 | PLAYER_TRIGGERED / TRANSITION | root/torso + head | head, torso, pelvis/root, feet, ears, tail | — | rotational | TURN / support sequence partly unclear | FOLLOW_THROUGH | single_transition | MEDIUM | V2/F11 | V1 with retained V2/U qualifiers |
| PIKA-MF-020 | Attention / gaze / head tracking-turn | B. Attention / gaze | Head/gaze orientation follows visible hand/pointer or interaction direction; may include one forelimb/ear/tail participation. | 2 | 2/6 (LIMITED) | V1/F07: 6 macro; V5/F07: 2 | PLAYER_TRIGGERED / visual association | eyes/head | eyes, head, neck, ears; optional paw/tail | root/feet generally quiet | small yaw/lean | PLANTED or crop-unknown | QUIET / AMPLIFIER | moving_hold / sequence | MEDIUM | V1/F07; V5/F07 | V1/V2 (source qualifiers retained) |
| PIKA-MF-021 | One-paw social offer and moving WAIT | J. Reciprocal social interaction | Character presents one paw and keeps it available in a moving WAIT before contact/completion; exact hidden trigger remains unknown. | 2 | 2/6 (LIMITED) | V3/PF-05: 3 offers within parent O006; V5/F03: 2 | CHARACTER_INITIATED_SOCIAL / RECIPROCAL | forelimb/paw | paw, forelimb, shoulder, face/head | root/other limb relatively quiet | minimal | crop-unknown / grounded | QUIET | prepare→present→WAIT→contact/completion | HIGH | V3/PF-05; V5/F03 | V1/V2 (source qualifiers retained) |
| PIKA-MF-022 | Presented-paw contact acknowledgement pulse | J. Reciprocal social interaction | Visible hand-paw contact is followed by compact paw/face acknowledgement; may continue the WAIT or retract afterward. | 2 | 2/6 (LIMITED) | V3/PF-06: 2 grouped acknowledgement episodes; multiple contact pulses inside O006b are not exact-counted; V5/F04: 4 | RECIPROCAL | contact locus / paw → face | presented paw, eyelids, mouth, head | root/other limb | minimal | crop-unknown / grounded | QUIET | contact→ack→hold/retract→settle | HIGH | V3/PF-06; V5/F04 | V1 / source-direct unless noted |
| PIKA-MF-023 | Two-forelimb lift + head-dip stern sequence | I. Negative / boundary touch | Both forelimbs and head coordinate into a stern-looking dip/lift sequence; same/similar performance appears both interaction-linked and autonomous in its source. | 1 | 1/6 (SINGLE-VIDEO) | V1/F06: 3 | BOTH | forelimbs + head | forelimbs, eyelids, ears, torso; tail follows | feet/root | upper-body dip | PLANTED | FOLLOW_THROUGH | sequence | HIGH | V1/F06 | V1 / source-direct unless noted |
| PIKA-MF-024 | Large positive bilateral open-arm whole-body delight | M. Large emotional / hero | Large positive full-body commitment using torso/root and bilateral forelimb opening/expansion; variants differ in crouch/rise/support and preceding context. | 5 | 5/6 (COMMON) | V1/F08: 1; V2/F04: 3; V3/PF-04: 22 episodes including non-touch afterglow variants; 19 are touch-linked response episodes; V4/MF-10: 1; V6/F06: 1 | PLAYER_TRIGGERED / SYSTEM-UNKNOWN | face/torso/forelimbs or root/COM | face, torso, both forelimbs, root/COM, ears, tail; feet may participate | few channels quiet at peak | large rise/compression→expansion | PLANTED to possible SUPPORT_CHANGE depending variant | FOLLOW_THROUGH / EMOTION_AMPLIFIER | anticipation_action_settle | HIGH | V1/F08; V2/F04; V3/PF-04; V4/MF-10; V6/F06 | V1/V2 (source qualifiers retained) |
| PIKA-MF-025 | Autonomous bilateral forelimb-open body pulse | F. Autonomous idle | No visible contact: both forelimbs open outward with face/mouth change and a small grounded whole-body pulse, then settle. | 2 | 2/6 (LIMITED) | V1/F13: 1; V5/F14: 1 | AUTONOMOUS / UNKNOWN | forelimbs + face | both forelimbs, mouth, eyelids, torso/root, head/ears | feet | small upward/forward | PLANTED / support unclear in crop | FOLLOW_THROUGH / secondary | pulse / anticipation_action_settle | HIGH | V1/F13; V5/F14 | V1 / source-direct unless noted |
| PIKA-MF-026 | Autonomous closed-eye side-lean hold | F. Autonomous idle | Autonomous eyes-closed head/torso side lean with small COM displacement and restrained follow-through. | 1 | 1/6 (SINGLE-VIDEO) | V1/F11: 1 | AUTONOMOUS | head/torso | eyelids, head, torso, ears, tail | forelimbs/feet | small lateral | PLANTED / seated | FOLLOW_THROUGH | moving_hold | MEDIUM | V1/F11 | V1 / source-direct unless noted |
| PIKA-MF-027 | Autonomous drowsy lateral sway with eyelid/mouth cycling | F. Autonomous idle | No visible input: eyelids/mouth lead into alternating head/torso/root lateral sway before recovery. | 2 | 2/6 (LIMITED) | V2/F14: 1; V4/MF-14: 2 | AUTONOMOUS | eyelids/mouth → head | eyes, mouth, head, torso/root, ears, tail | feet | alternating lateral WEIGHT_SHIFT | PLANTED | FOLLOW_THROUGH / AMPLIFIER | sequence / moving_hold | HIGH | V2/F14; V4/MF-14 | V1 / source-direct unless noted |
| PIKA-MF-028 | Autonomous clasped-paw side-to-side bow/sway | F. Autonomous idle | Eyes close, paws remain clasped/gathered and head/torso sweep/bow side-to-side autonomously; feet remain planted. | 1 | 1/6 (SINGLE-VIDEO) | V4/MF-13: 2 | AUTONOMOUS | head/torso | eyelids, head, torso, forelimbs, root/COM | feet | WEIGHT_SHIFT | PLANTED | FOLLOW_THROUGH | sequence | HIGH | V4/MF-13 | V1 / source-direct unless noted |
| PIKA-MF-029 | Prolonged closed-eye rest / doze moving hold | A. Living / physiological | Long eyes-closed state with tiny head/torso drift or slow sway, distinct from a blink and from short recovery. | 2 | 2/6 (LIMITED) | V1/F12: 1; V4/MF-16: 1 | AUTONOMOUS | eyelids/head | eyelids, mouth, head, torso; ears/tail source-dependent | limbs/feet mostly quiet | minimal / slow sway | PLANTED / seated | QUIET / FOLLOW / occasional independent micro | moving_hold | HIGH | V1/F12; V4/MF-16 | V1 / source-direct unless noted |
| PIKA-MF-030 | Autonomous head/neck arc-sway | F. Autonomous idle | Autonomous head/neck arc through upward/back and lateral orientation with only small upper-body compensation. | 1 | 1/6 (SINGLE-VIDEO) | V3/PF-07: 1 | AUTONOMOUS / AFTERGLOW UNCERTAIN | head/neck | head, neck, eyes, ears, upper torso | root/limbs | small upper-body | grounding quiet | FOLLOW_THROUGH / UNCLEAR | sequence | HIGH | V3/PF-07 | V1/V2 (source qualifiers retained) |
| PIKA-MF-031 | Autonomous turn-and-bow-like compression gesture | F. Autonomous idle | No visible contact at onset: head/torso/root yaw/lean down with forelimbs clasped, then return upright; social meaning remains unconfirmed. | 1 | 1/6 (SINGLE-VIDEO) | V3/PF-12: 1 | AUTONOMOUS / CHARACTER_INITIATED_SOCIAL UNCERTAIN | head/torso | head, neck, torso, root, forelimb clasp, ears | feet quiet | TURN / WEIGHT_SHIFT | PLANTED | FOLLOW_THROUGH | sequence | MEDIUM | V3/PF-12 | V1/V2 (source qualifiers retained) |
| PIKA-MF-032 | Autonomous self-touch / pondering lateral tilt | F. Autonomous idle | No visible contact: face/head shift, one paw rises toward cheek/chin/chest, ears/torso follow into a held tilt, then recover. | 2 | 2/6 (LIMITED) | V4/MF-15: 1; V6/F18: 1 | AUTONOMOUS / visual context | face/head → forelimb | face, head, ears, one/both forelimbs, torso/root | feet/tail | lateral WEIGHT_SHIFT or small planted tilt | PLANTED | QUIET / FOLLOW | sequence | HIGH | V4/MF-15; V6/F18 | V1/V2 (source qualifiers retained) |
| PIKA-MF-033 | Touch-interrupted doze → wake/startle expansion → recovery | J. Reciprocal social interaction | Player touch interrupts an eyes-closed doze; face/head and full body expand/startle, then recover. | 1 | 1/6 (SINGLE-VIDEO) | V4/MF-17: 1 | PLAYER_TRIGGERED / RECIPROCAL | face/head → full body | eyelids, face, head, torso/root, forelimbs, ears | feet remain support | WEIGHT_SHIFT | PLANTED | FOLLOW_THROUGH | state_interrupt→action→recovery | HIGH | V4/MF-17 | V1/V2 (source qualifiers retained) |
| PIKA-MF-034 | Feeding orient / mouth-contact hold / item-disappearance transition | K. Feeding | Visible food approaches the muzzle/mouth area, character attends/holds, and item may disappear; bite/chew/swallow mechanics are not asserted. | 5 | 5/6 (COMMON) | V1/F09: 2; V3/PF-09: 1 macro feeding sequence; V4/MF-11: 1; V5/F09: 1; V6/F12: 2 | PLAYER_TRIGGERED / SYSTEM | external item + head/mouth attention | eyes, head, mouth, ears; object/UI | forelimbs/root mostly quiet | minimal | PLANTED or crop-unknown | QUIET | approach→hold→disappearance/pause | MEDIUM | V1/F09; V3/PF-09; V4/MF-11; V5/F09; V6/F12 | V1/V2 (source qualifiers retained) |
| PIKA-MF-035 | Feeding-completion positive delight | K. Feeding | After item disappearance/feeding phase, face leads into closed-eye/open-mouth positive response with head/torso/ears/tail recruitment, then settle. | 5 | 5/6 (COMMON) | V1/F10: 2; V3/PF-09: 1 macro feeding sequence; V4/MF-12: 1; V5/F10: 1; V6/F13: 2 | PLAYER_TRIGGERED / feeding consequence | face | eyelids, mouth, head, torso, ears; tail source-dependent | feet/root mostly quiet | small expansion | PLANTED / crop-unknown | QUIET / AMPLIFIER / FOLLOW | pulse / anticipation_action_settle | HIGH | V1/F10; V3/PF-09; V4/MF-12; V5/F10; V6/F13 | V1/V2 (source qualifiers retained) |
| PIKA-MF-036 | Bilateral gift/item presentation moving hold | L. Gift / item | Object is held/presented by both forelimbs/paws in front of torso; character remains grounded in a sustained presentation/WAIT-like state. | 4 | 4/6 (RECURRING) | V3/PF-10: 1 macro item sequence with 2 phases; V4/MF-18: 1; V5/F11: 1; V6/F15: 1 | SYSTEM / CHARACTER_INITIATED_SOCIAL / UNKNOWN | forelimbs/item posture | both forelimbs/paws, object, head/eyes, torso | feet/root stable | minimal | PLANTED | QUIET | hold / moving_hold | MEDIUM | V3/PF-10; V4/MF-18; V5/F11; V6/F15 | V1/V2 (source qualifiers retained) |
| PIKA-MF-037 | Gift/item release / forelimb opening / positive completion | L. Gift / item | Presentation resolves as object disappears or is no longer visible, paws/forelimbs open or lower, positive face may peak, then settle. Transfer recipient/mechanism is not asserted. | 4 | 4/6 (RECURRING) | V3/PF-10: 1 macro item sequence with 2 phases; V4/MF-19: 1; V5/F12: 1; V6/F16: 1 | SYSTEM / CHARACTER_INITIATED_SOCIAL / UNKNOWN | face + forelimbs | forelimbs, eyelids, mouth, head, torso; object state | feet | small expansion / stable | PLANTED | QUIET / FOLLOW | sequence | HIGH | V3/PF-10; V4/MF-19; V5/F12; V6/F16 | V1 with retained V2/U qualifiers |
| PIKA-MF-038 | Closed-eye content afterglow / low-motion settle | N. Recovery / settle / afterglow | After action/interaction, positive face remains eyes-closed/soft with low-amplitude head motion before reopen/neutral. | 2 | 2/6 (LIMITED) | V5/F08: 3; V6/F17: 1 | RECIPROCAL / PLAYER_TRIGGERED / SYSTEM-UNKNOWN | eyelids/face | eyelids, mouth, head; retracting limb source-dependent | root/torso quiet | minimal | PLANTED / crop-unknown | QUIET | moving_hold / settle | HIGH | V5/F08; V6/F17 | V1 / source-direct unless noted |
| PIKA-MF-039 | Half-lidded / droopy facial recovery settle | N. Recovery / settle / afterglow | After a stronger action, amplitude drops and face enters half-lidded/mouth-down or droopy configuration before neutral; not a blink. | 3 | 2/6 (LIMITED) | V3/PF-08: at least 10 clearly sampled appearances; V6/F10: at least 5 likely; V6/F17: 1 | AFTERGLOW / UNKNOWN | face/eyelids | eyelids, mouth, head small; ears/torso occasionally | root/feet quiet | minimal | PLANTED | QUIET | hold / settle | HIGH | V3/PF-08; V6/F10; V6/F17 | V1/V2 (source qualifiers retained) |
| PIKA-MF-040 | General active-pose return-to-neutral settle / recovery | N. Recovery / settle / afterglow | Explicitly cataloged recovery family where active pose decays back toward neutral; lead depends on parent motion. | 2 | 2/6 (LIMITED) | V1/F16: recurrent; V2/F15: 9 child phases | BOTH / SYSTEM | varies | root, torso, head, face, ears/tail or parent channels | — | excursion decays / returns centered | returns PLANTED | late finish possible | single_transition / settle | HIGH | V1/F16; V2/F15 | V1 / source-direct unless noted |
| PIKA-MF-041 | System/UI/menu/item-mode transition without reliable body motion | P. Transition | Menu, black/loading, item-selection, iris/fade or overlay transition in which body motion is absent, obscured, or not the primary event. | 4 | 3/6 (RECURRING) | V3/PF-01: 2 macro occurrences; V4/MF-20: 2; V6/F11: 1; V6/F14: 2 | SYSTEM | UI / screen state | UI; character body minor/absent | body unreliable | — | — | — | single_transition | LOW | V3/PF-01; V4/MF-20; V6/F11; V6/F14 | V1 with retained V2/U qualifiers |
| PIKA-MF-042 | Visible screen-relative character entry / exit transition | P. Transition | Character visibly rises/appears or dips/exits relative to frame; camera contribution may be inseparable, so this is kept separate from body-authored motion. | 1 | 1/6 (SINGLE-VIDEO) | V3/PF-01: 2 macro occurrences | SYSTEM / TRANSITION | screen-relative full body | eyes/head/torso when visible | — | screen-relative translation | UNCLEAR | UNCLEAR | single_transition | MEDIUM | V3/PF-01 | V1/V2 (source qualifiers retained) |
| PIKA-MF-043 | Close-up entry head-dip / smile-open-mouth expression sequence | M. Large emotional / hero | Opening close-up: eyelids close, head/upper torso dip/lean, mouth shifts to smile/open shape, then returns toward baseline; lower-body COM is unavailable. | 1 | 1/6 (SINGLE-VIDEO) | V5/F01: 1 | SYSTEM / UNKNOWN | eyelids/face → head | eyelids, mouth, head, ears, upper torso | lower body off-frame | small visible displacement; true COM unknown | off-frame | UNCLEAR | state_entry→peak→settle | HIGH | V5/F01 | V1/V2 (source qualifiers retained) |
| PIKA-MF-044 | Foreground close-pass → close-up content hold | M. Large emotional / hero | Large screen/depth traversal into a close-up eyes-closed positive hold; root/depth change is visible but camera contribution is not fully separable. | 1 | 1/6 (SINGLE-VIDEO) | V6/F01: 1 | SYSTEM / UNKNOWN | full-body/root screen-relative | root, torso, head, ears, tail, face | limbs partly cropped later | large translation | UNCLEAR | FOLLOW_THROUGH | sequence / moving_hold | MEDIUM | V6/F01 | V1 / source-direct unless noted |
| PIKA-MF-045 | Closed-eye gathered-paw head/torso lower-and-lean | D. Posture / balance / COM | Eyes close while paws gather and head/upper torso lower/lean; source contains entry, touch-associated and broad-lean variants, so social meaning is not unified. | 1 | 1/6 (SINGLE-VIDEO) | V4/MF-02: 9 | BOTH / UNKNOWN | head/upper torso | eyelids, head, torso, forelimbs; root/COM varies | feet mostly quiet | small–medium lowering/lean | PLANTED / WEIGHT_SHIFT | FOLLOW_THROUGH | sequence | HIGH | V4/MF-02 | V1/V2 (source qualifiers retained) |
| PIKA-MF-046 | Brief closed-eye open-mouth smile pulse from neutral | F. Autonomous idle | From neutral with no direct contact visible, face closes/opens positively with a small vertical head/torso pulse, then half-lid/neutral; initiation source is unknown. | 1 | 1/6 (SINGLE-VIDEO) | V5/F16: 1 | UNKNOWN / autonomous-looking | face | eyelids, mouth, head, torso/root | forelimbs/feet | small vertical pulse | PLANTED | secondary / unclear | pulse | HIGH | V5/F16 | V1 with retained V2/U qualifiers |
| PIKA-MF-047 | Tail-region contact → local tail displacement/sweep with body lean | C. Ear / tail micro | Contact around tail/rear region produces a tail-led local displacement/sweep, sometimes with body lean and later smile/VFX; retained separately from autonomous tail micro. | 1 | 1/6 (SINGLE-VIDEO) | V4/MF-07: 3 | PLAYER_TRIGGERED | tail / tail+torso | tail, torso/root, face later | feet remain support | small–medium WEIGHT_SHIFT | PLANTED | PRIMARY_ACTION / LOCAL_RESPONSE → FOLLOW_THROUGH | sequence | MEDIUM | V4/MF-07 | V1/V2 (source qualifiers retained) |

## 5. Family → Variant → Occurrence Mapping

The table below is the authoritative Master-Variant trace. `Defining Difference` preserves each source Family’s own variant wording; split-phase qualifiers are added only when the local source itself contains separable phases.

| Variant ID | Parent Family | Defining Difference | Source Videos | Source Local IDs | Occurrences | Representative Timestamp | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PIKA-MF-002-V01 | PIKA-MF-002 | source local variants: clean idle blink | V1 | V1/F01 | ≥1 clean | 03:06.77 | V1 |
| PIKA-MF-001-V01 | PIKA-MF-001 | source local variants: closed-eye opening; open-eye neutral | V1 | V1/F02 | 10 macro segments | 02:37.7 | V1 |
| PIKA-MF-006-V01 | PIKA-MF-006 | source local variants: head/chest/side/extended rub | V1 | V1/F03 | ≥29 cycles | 00:08.6 | V1 |
| PIKA-MF-007-V01 | PIKA-MF-007 | source local variants: standard, extended, hero precursor, phase-B | V1 | V1/F04 | **29** | 00:10.4 | V1 |
| PIKA-MF-015-V01 | PIKA-MF-015 | source local variants: upper-face press; similar later bow | V1 | V1/F05 | 2 | 00:16.5 | V1 |
| PIKA-MF-023-V01 | PIKA-MF-023 | source local variants: triggered; autonomous repeat | V1 | V1/F06 | 3 | 02:46.1 | V1 |
| PIKA-MF-020-V01 | PIKA-MF-020 | source local variants: one-forelimb; tail-sweep extended | V1 | V1/F07 | 6 macro | 00:32–00:39 | V1 |
| PIKA-MF-024-V01 | PIKA-MF-024 | source local variants: single observed strong variant | V1 | V1/F08 | 1 | 02:11.0–02:11.8 | V1/V2 support |
| PIKA-MF-034-V01 | PIKA-MF-034 | source local variants: feed #1/#2 | V1 | V1/F09 | 2 | 02:23.2 | V1 |
| PIKA-MF-035-V01 | PIKA-MF-035 | source local variants: feed #1/#2 | V1 | V1/F10 | 2 | 02:28.4 | V1 |
| PIKA-MF-026-V01 | PIKA-MF-026 | source local variants: single | V1 | V1/F11 | 1 | 03:13.4–03:15.1 | V1 |
| PIKA-MF-029-V01 | PIKA-MF-029 | source local variants: single long | V1 | V1/F12 | 1 | 03:26.0–03:42.2 | V1 |
| PIKA-MF-025-V01 | PIKA-MF-025 | source local variants: single | V1 | V1/F13 | 1 | 04:05.8–04:06.5 | V1 |
| PIKA-MF-004-V01 | PIKA-MF-004 | source local variants: idle micro; reaction follow-through | V1 | V1/F14 | ≥4 clean idle repositions | 03:01–03:09 | V1 |
| PIKA-MF-005-V01 | PIKA-MF-005 | source local variants: idle micro; flatten/spread in reactions | V1 | V1/F15 | recurrent | 00:16.1 | V1 |
| PIKA-MF-040-V01 | PIKA-MF-040 | source local variants: fast reset; gradual settle | V1 | V1/F16 | recurrent | 00:10.9 | V1 |
| PIKA-MF-001-V02 | PIKA-MF-001 | source local variants: 7 segmented contexts | V2 | V2/F01 | 7 | 108.50–122.45 | V1 |
| PIKA-MF-002-V02 | PIKA-MF-002 | source local variants: 1 observed variant | V2 | V2/F02 | ≥2 | ~111.5 | V1 |
| PIKA-MF-004-V02 | PIKA-MF-004 | source local variants: 2 segmented contexts | V2 | V2/F03 | 2 intervals | 118.50–122.40 | V1 |
| PIKA-MF-024-V02 | PIKA-MF-024 | source local variants: 3 | V2 | V2/F04 | 3 | 91.10–93.00 | V1; support V2 |
| PIKA-MF-007-V02 | PIKA-MF-007 | source local variants: ≥9 named variants | V2 | V2/F05 | 11 | 76.65–79.15 | V1; cause V2 |
| PIKA-MF-014-V01 | PIKA-MF-014 | source local variants: 7 named states | V2 | V2/F06 | 8 intervals | 24.80–32.75 | V1; cause V2 |
| PIKA-MF-015-V02 | PIKA-MF-015 | source local variants: 2 structural variants | V2 | V2/F07 | 3 | 32.85–34.55 | V1; support V2 |
| PIKA-MF-016-V01 | PIKA-MF-016 | source local variants: 1 | V2 | V2/F08 | 1 | 48.60–49.57 | V1; trigger/support V2/U |
| PIKA-MF-017-V01 | PIKA-MF-017 | source local variants: 3 segmented | V2 | V2/F09 | 3 | 59.50–63.95 | V1 |
| PIKA-MF-018-V01 | PIKA-MF-018 | source local variants: 2 | V2 | V2/F10 | 2 | 58.55–59.50 | V1; cause V2 |
| PIKA-MF-019-V01 | PIKA-MF-019 | source local variants: 1 | V2 | V2/F11 | 1 | 67.20–68.15 | V1; feet U |
| PIKA-MF-012-V01 | PIKA-MF-012 | source local variants: 2 | V2 | V2/F12 | 2 | 106.30–106.85 | V1; exact contact U/V2 |
| PIKA-MF-013-V01 | PIKA-MF-013 | source local variants: 1 | V2 | V2/F13 | 1 | 97.60–100.10 | V1; trigger/tail-lead U/V2 |
| PIKA-MF-027-V01 | PIKA-MF-027 | source local variants: 1 | V2 | V2/F14 | 1 | 122.45–126.55 | V1 |
| PIKA-MF-040-V02 | PIKA-MF-040 | source local variants: multiple | V2 | V2/F15 | 9 child phases | 92.55–93.00 | V1 |
| PIKA-MF-042-V01 | PIKA-MF-042 | visible entry-rise/exit-dip phases only; source local variants: entry-rise+eye-open; exit-dip; black/menu/loading transition | V3 | V3/PF-01 | 2 macro occurrences | 2.63–5.77; 152.07–156.13 | V1/V2 |
| PIKA-MF-041-V01 | PIKA-MF-041 | black/menu/loading transition component only; source local variants: entry-rise+eye-open; exit-dip; black/menu/loading transition | V3 | V3/PF-01 | 2 macro occurrences | 2.63–5.77; 152.07–156.13 | V1/V2 |
| PIKA-MF-001-V03 | PIKA-MF-001 | source local variants: close-up neutral hold; wide standing hold; UI-occluded hold | V3 | V3/PF-02 | 7 | 6.77–9.50; 53.50–58.30; 125.50–152.07; 160.75–164.60; 166.50–168.00; 183.00–186.20; 188.40–190.87 | V1 |
| PIKA-MF-002-V03 | PIKA-MF-002 | source local variants: full blink; partial blink not independently confirmed | V3 | V3/PF-03 | 2 confirmed isolated spontaneous blinks | 128.20–128.30; 140.40–140.47 | V1 |
| PIKA-MF-007-V03 | PIKA-MF-007 | small/medium face-led, prolonged content response variants; source local variants: A small face-led acknowledge; B large closed-eye open-mouth delight; C prolonged closed-eye content hold; D wide-view full-body compression/expansion | V3 | V3/PF-04 | 22 episodes including non-touch afterglow variants; 19 are touch-linked response episodes | 10.45–19.90; 31.50–90.10; 114.20–124.50; 165.25–166.30; 168.00–181.30 | V1 |
| PIKA-MF-024-V03 | PIKA-MF-024 | wide full-body compression/expansion variant D only; source local variants: A small face-led acknowledge; B large closed-eye open-mouth delight; C prolonged closed-eye content hold; D wide-view full-body compression/expansion | V3 | V3/PF-04 | 22 episodes including non-touch afterglow variants; 19 are touch-linked response episodes | 10.45–19.90; 31.50–90.10; 114.20–124.50; 165.25–166.30; 168.00–181.30 | V1 |
| PIKA-MF-021-V01 | PIKA-MF-021 | source local variants: screen-right paw; screen-left paw; longer repeated-contact hold | V3 | V3/PF-05 | 3 offers within parent O006 | 20.25–22.50; 22.75–28.25; 28.75–31.50 | V1/V2 |
| PIKA-MF-022-V01 | PIKA-MF-022 | source local variants: round-mouth recoil; closed-eye smile acknowledgement | V3 | V3/PF-06 | 2 grouped acknowledgement episodes; multiple contact pulses inside O006b are not exact-counted | 22.00–22.50; 24.50–26.75 | V1 |
| PIKA-MF-030-V01 | PIKA-MF-030 | source local variants: single observed variant | V3 | V3/PF-07 | 1 | 90.20–98.20 | V1/V2 |
| PIKA-MF-039-V01 | PIKA-MF-039 | source local variants: short half-lid; half-lid plus head tilt | V3 | V3/PF-08 | at least 10 clearly sampled appearances | ~36.8–37.2; ~41.8–42.6; ~45.4–45.8; ~60.4–60.8; ~64.8–65.2; 98.7–100.0; ~114.9–115.2; ~123.7–124.2; ~165.9–166.2; ~174.4–174.7; ~180.9–181.1 | V1 |
| PIKA-MF-034-V02 | PIKA-MF-034 | approach/presentation + item disappearance phases O024/O025; source local variants: single observed food object event | V3 | V3/PF-09 | 1 macro feeding sequence | 101.80–115.20 | V1 for approach/disappearance; V2 for 'consume' interpretation |
| PIKA-MF-035-V02 | PIKA-MF-035 | post-food delight phase O026; source local variants: single observed food object event | V3 | V3/PF-09 | 1 macro feeding sequence | 101.80–115.20 | V1 for approach/disappearance; V2 for 'consume' interpretation |
| PIKA-MF-036-V01 | PIKA-MF-036 | two-paw hold/presentation phase O031; source local variants: presentation hold; release/joy child phase | V3 | V3/PF-10 | 1 macro item sequence with 2 phases | 156.20–160.25 | V1/V2 |
| PIKA-MF-037-V01 | PIKA-MF-037 | object release/joy phase O032; source local variants: presentation hold; release/joy child phase | V3 | V3/PF-10 | 1 macro item sequence with 2 phases | 156.20–160.25 | V1/V2 |
| PIKA-MF-012-V02 | PIKA-MF-012 | source local variants: forward acknowledgement; lower local paw adjustment | V3 | V3/PF-11 | 2 | 172.00–174.80; 181.75–183.00 | V1 |
| PIKA-MF-031-V01 | PIKA-MF-031 | source local variants: single observed variant | V3 | V3/PF-12 | 1 | 186.20–188.40 | V1/V2 |
| PIKA-MF-001-V04 | PIKA-MF-001 | source local variants: short post-recovery hold; long neutral hold | V4 | V4/MF-01 | 9 | 201–210.75, 213–219.5, 224–228.75 | V1 |
| PIKA-MF-045-V01 | PIKA-MF-045 | source local variants: entry bow; touch-associated lean; broad side lean; brief posture correction | V4 | V4/MF-02 | 9 | 0.25–1.75, 7.75–10.25, 13.75–15.5 | V1/V2 |
| PIKA-MF-012-V03 | PIKA-MF-012 | source local variants: face-side raise; open-mouth raise; stronger bilateral-adjacent preparation | V4 | V4/MF-03 | 5 | 5.25–6.25, 12.25–12.75, 66.5–69 | V1/V2 |
| PIKA-MF-007-V04 | PIKA-MF-007 | source local variants: closed-eye smile; open-mouth delight; narrowed-release; low-amplitude head dip | V4 | V4/MF-04 | 18 | 35–38, 38.5–41.5, 54–57.5 | V1/V2 |
| PIKA-MF-010-V01 | PIKA-MF-010 | source local variants: closed-eye-first; open-mouth peak; narrowed-face middle; amplitude differences | V4 | V4/MF-05 | 6 | 17–19.5, 30.5–34.75, 78–80.75 | V1 |
| PIKA-MF-009-V01 | PIKA-MF-009 | source local variants: single observed clear variant | V4 | V4/MF-06 | 1 | 85.5–88.25 | V1/V2 |
| PIKA-MF-047-V01 | PIKA-MF-047 | source local variants: sweep-dominant; lean-dominant; tail response into smile/VFX | V4 | V4/MF-07 | 3 | 91–93, 94.5–97.75, 98–101.75 | V1/V2 |
| PIKA-MF-007-V05 | PIKA-MF-007 | source local variants: small closed-eye smile; open-mouth smile; amplitude/timing differences | V4 | V4/MF-08 | 11 | 20.5–23.5, 24–27.75, 47–49.75 | V1/V2 |
| PIKA-MF-014-V02 | PIKA-MF-014 | source local variants: brief narrowed-eye; stronger squeezed/downturned mouth; mixed lean variant | V4 | V4/MF-09 | 3 | 69.5–71, 118–121.75, 142.5–145.75 | V1; affect label U |
| PIKA-MF-024-V04 | PIKA-MF-024 | source local variants: single clear occurrence | V4 | V4/MF-10 | 1 | 129.75–131.75 | V1/V2 |
| PIKA-MF-034-V03 | PIKA-MF-034 | source local variants: one observed sequence | V4 | V4/MF-11 | 1 | 146.25–153.75 | V1; consume inference V2 |
| PIKA-MF-035-V03 | PIKA-MF-035 | source local variants: single observed sequence | V4 | V4/MF-12 | 1 | 152.9–153.75 | V1/V2 |
| PIKA-MF-028-V01 | PIKA-MF-028 | source local variants: two visually highly similar occurrences | V4 | V4/MF-13 | 2 | 211–213, 229.25–231 | V1 |
| PIKA-MF-027-V02 | PIKA-MF-027 | source local variants: 219–223.75; 302.5–306.0 with small timing/amplitude differences | V4 | V4/MF-14 | 2 | 219.75–223.75, 302.5–306 | V1 |
| PIKA-MF-032-V01 | PIKA-MF-032 | source local variants: single clear occurrence | V4 | V4/MF-15 | 1 | 235.25–237.25 | V1 |
| PIKA-MF-029-V02 | PIKA-MF-029 | source local variants: single clear long hold | V4 | V4/MF-16 | 1 | 247.5–257.5 | V1 |
| PIKA-MF-033-V01 | PIKA-MF-033 | source local variants: single clear occurrence | V4 | V4/MF-17 | 1 | 257.75–261.75 | V1/V2 |
| PIKA-MF-036-V02 | PIKA-MF-036 | source local variants: neutral-face hold; closed-eye smile hold | V4 | V4/MF-18 | 1 | 287–291.25 | V1 |
| PIKA-MF-037-V02 | PIKA-MF-037 | source local variants: single observed sequence | V4 | V4/MF-19 | 1 | 290.25–291.25 | V1; handoff mechanism U |
| PIKA-MF-041-V02 | PIKA-MF-041 | source local variants: hard-cut/menu interval; large UI occlusion interval | V4 | V4/MF-20 | 2 | 282.6–286.9, 291.75–295.25 | V1/U for hidden body |
| PIKA-MF-043-V01 | PIKA-MF-043 | source local variants: 1 | V5 | V5/F01 | 1 | 0.40–4.10 | V1/V2 |
| PIKA-MF-007-V06 | PIKA-MF-007 | source local variants: 5 | V5 | V5/F02 | 5 | 8.45–23.15; 63.70–66.90 | V1 |
| PIKA-MF-021-V02 | PIKA-MF-021 | source local variants: 2 | V5 | V5/F03 | 2 | 23.30–24.80; 27.40–31.50 | V1/V2 |
| PIKA-MF-022-V02 | PIKA-MF-022 | source local variants: 4 | V5 | V5/F04 | 4 | 23.75–25.30; 27.90–31.50 | V1 |
| PIKA-MF-007-V07 | PIKA-MF-007 | source local variants: ≥7 visible variants/pulses | V5 | V5/F05 | 7 | 25.90–27.20; 34.20–37.30; 57.20–62.80; 77.70–84.50; 96.70–101.40 | V1 |
| PIKA-MF-014-V03 | PIKA-MF-014 | source local variants: 4 | V5 | V5/F06 | 4 | 40.20–56.60; 84.50–89.20 | V1/V2 |
| PIKA-MF-020-V02 | PIKA-MF-020 | source local variants: 2 | V5 | V5/F07 | 2 | 67.00–72.80; 89.25–92.20 | V1/V2 |
| PIKA-MF-038-V01 | PIKA-MF-038 | source local variants: 3 | V5 | V5/F08 | 3 | 31.60–33.15; 101.40–104.90; 130.65–131.25 | V1 |
| PIKA-MF-034-V04 | PIKA-MF-034 | source local variants: 1 | V5 | V5/F09 | 1 | 113.25–117.25 | V1 |
| PIKA-MF-035-V04 | PIKA-MF-035 | source local variants: 1 | V5 | V5/F10 | 1 | 117.25–119.00 | V1/V2 |
| PIKA-MF-036-V03 | PIKA-MF-036 | source local variants: 1 | V5 | V5/F11 | 1 | 127.00–129.00 | V1 |
| PIKA-MF-037-V03 | PIKA-MF-037 | source local variants: 1 | V5 | V5/F12 | 1 | 129.00–130.65 | V1/V2 |
| PIKA-MF-001-V05 | PIKA-MF-001 | source local variants: multiple contextual variants | V5 | V5/F13 | 9 windows | 4.10–8.45; 72.80–77.70; 137.10–153.33 | V1/V2 |
| PIKA-MF-025-V02 | PIKA-MF-025 | source local variants: 1 | V5 | V5/F14 | 1 | 143.60–144.55 | V1 |
| PIKA-MF-003-V01 | PIKA-MF-003 | source local variants: full close, half-lid, reopen | V5 | V5/F15 | ≥20 embedded transitions | throughout interaction sections | V1; physiology U |
| PIKA-MF-046-V01 | PIKA-MF-046 | source local variants: 1 | V5 | V5/F16 | 1 | 136.25–137.10 | V1/U trigger |
| PIKA-MF-004-V03 | PIKA-MF-004 | source local variants: continuous | V5 | V5/F17 | 2 long windows | 137.10–143.60; 144.55–153.33 | V1/V2 |
| PIKA-MF-044-V01 | PIKA-MF-044 | source local variants: 1 | V6 | V6/F01 | 1 | 0.6–3.4 | V1 |
| PIKA-MF-001-V06 | PIKA-MF-001 | source local variants: 2+ | V6 | V6/F02 | 4 macro + many short resets | 110.0–116.6; 118.7–124.1 | V1 |
| PIKA-MF-007-V08 | PIKA-MF-007 | source local variants: 4+ | V6 | V6/F03 | at least 11 clear macro cycles | 9.7–11.8 etc. | V1 |
| PIKA-MF-006-V02 | PIKA-MF-006 | source local variants: 2 | V6 | V6/F04 | 3+ | 16.0–18.9 | V1 |
| PIKA-MF-008-V01 | PIKA-MF-008 | source local variants: 2 | V6 | V6/F05 | at least 2 | 19.4–19.9 | V1 |
| PIKA-MF-024-V05 | PIKA-MF-024 | source local variants: 1 | V6 | V6/F06 | 1 | 19.9–20.6 | V1 |
| PIKA-MF-012-V04 | PIKA-MF-012 | source local variants: 1+ | V6 | V6/F07 | at least 3 lifts | ~26.5, ~37.2, ~39.7 | V1 |
| PIKA-MF-009-V02 | PIKA-MF-009 | source local variants: 2 | V6 | V6/F08 | 2 | 32.7–34.3; 62.4–64.1 | V1 |
| PIKA-MF-011-V01 | PIKA-MF-011 | source local variants: 1 | V6 | V6/F09 | 1 | 41.2–43.9 | V1/V2 |
| PIKA-MF-039-V02 | PIKA-MF-039 | source local variants: 1+ | V6 | V6/F10 | at least 5 likely | 42.4–43.4 etc. | V1/V2 |
| PIKA-MF-041-V03 | PIKA-MF-041 | source local variants: 1 | V6 | V6/F11 | 1 | 75.8–79.5 | V1 |
| PIKA-MF-034-V05 | PIKA-MF-034 | source local variants: 2 | V6 | V6/F12 | 2 | 79.5–84.7; 87.0–91.2 | V1/V2 |
| PIKA-MF-035-V05 | PIKA-MF-035 | source local variants: 1 | V6 | V6/F13 | 2 | 84.7–85.6; 91.2–92.1 | V1 |
| PIKA-MF-041-V04 | PIKA-MF-041 | source local variants: 2 | V6 | V6/F14 | 2 | 95.4–99.5; 104.4–108.2 | V1 |
| PIKA-MF-036-V04 | PIKA-MF-036 | source local variants: 1 | V6 | V6/F15 | 1 | 99.9–101.9 | V1 |
| PIKA-MF-037-V04 | PIKA-MF-037 | source local variants: 1 | V6 | V6/F16 | 1 | 102.0–103.7 | V1 |
| PIKA-MF-038-V02 | PIKA-MF-038 | initial closed-eye positive post-gift afterglow; source local variants: 1 | V6 | V6/F17 | 1 | 108.2–109.7 | V1 |
| PIKA-MF-039-V03 | PIKA-MF-039 | subsequent droopy/half-lidded settle phase; source local variants: 1 | V6 | V6/F17 | 1 | 108.2–109.7 | V1 |
| PIKA-MF-032-V02 | PIKA-MF-032 | source local variants: 1 | V6 | V6/F18 | 1 | 116.6–118.7 | V1/V2 |

## 6. Living / Physiological Master

| Family | Name | Category Role | Coverage | Initiation | Front View |
| --- | --- | --- | --- | --- | --- |
| PIKA-MF-001 | Neutral attentive intentional-stillness / low-motion moving hold | SECONDARY | 6/6 | AUTONOMOUS / SYSTEM / UNKNOWN | HIGH |
| PIKA-MF-002 | Spontaneous isolated blink | PRIMARY | 3/6 | AUTONOMOUS | HIGH |
| PIKA-MF-004 | Independent tail ambient micro / sweep / oscillation | SECONDARY | 3/6 | AUTONOMOUS / BOTH | MEDIUM |
| PIKA-MF-027 | Autonomous drowsy lateral sway with eyelid/mouth cycling | SECONDARY | 2/6 | AUTONOMOUS | HIGH |
| PIKA-MF-029 | Prolonged closed-eye rest / doze moving hold | PRIMARY | 2/6 | AUTONOMOUS | HIGH |

## 7. Attention / Gaze Master

| Family | Name | Category Role | Coverage | Initiation | Front View |
| --- | --- | --- | --- | --- | --- |
| PIKA-MF-005 | Ear orientation micro-correction | SECONDARY | 1/6 | BOTH | HIGH |
| PIKA-MF-014 | Contact-linked facial sensitivity / displeased warning state | SECONDARY | 3/6 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-018 | Rear-contact glance-back warning and turn-away | SECONDARY | 1/6 | PLAYER_TRIGGERED | LOW |
| PIKA-MF-020 | Attention / gaze / head tracking-turn | PRIMARY | 2/6 | PLAYER_TRIGGERED / visual association | MEDIUM |
| PIKA-MF-030 | Autonomous head/neck arc-sway | SECONDARY | 1/6 | AUTONOMOUS / AFTERGLOW UNCERTAIN | HIGH |
| PIKA-MF-034 | Feeding orient / mouth-contact hold / item-disappearance transition | SECONDARY | 5/6 | PLAYER_TRIGGERED / SYSTEM | MEDIUM |

## 8. Ear / Tail Micro Master

| Family | Name | Category Role | Coverage | Initiation | Front View |
| --- | --- | --- | --- | --- | --- |
| PIKA-MF-004 | Independent tail ambient micro / sweep / oscillation | PRIMARY | 3/6 | AUTONOMOUS / BOTH | MEDIUM |
| PIKA-MF-005 | Ear orientation micro-correction | PRIMARY | 1/6 | BOTH | HIGH |
| PIKA-MF-020 | Attention / gaze / head tracking-turn | SECONDARY | 2/6 | PLAYER_TRIGGERED / visual association | MEDIUM |
| PIKA-MF-047 | Tail-region contact → local tail displacement/sweep with body lean | PRIMARY | 1/6 | PLAYER_TRIGGERED | MEDIUM |

## 9. Posture / Balance / COM Master

| Family | Name | Category Role | Coverage | Initiation | Front View |
| --- | --- | --- | --- | --- | --- |
| PIKA-MF-008 | Touch-positive closed-eye head-lower content bow | PRIMARY | 1/6 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-009 | Deep lateral positive-content lean with ear rotation | PRIMARY | 2/6 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-013 | Interaction-linked open-mouth lateral body sway | SECONDARY | 1/6 | PLAYER_TRIGGERED / interaction-linked | HIGH |
| PIKA-MF-015 | Boundary upper-body recoil / compression / withdrawal | SECONDARY | 2/6 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-019 | Side/back → front reorientation | SECONDARY | 1/6 | PLAYER_TRIGGERED / TRANSITION | MEDIUM |
| PIKA-MF-024 | Large positive bilateral open-arm whole-body delight | SECONDARY | 5/6 | PLAYER_TRIGGERED / SYSTEM-UNKNOWN | HIGH |
| PIKA-MF-026 | Autonomous closed-eye side-lean hold | SECONDARY | 1/6 | AUTONOMOUS | MEDIUM |
| PIKA-MF-027 | Autonomous drowsy lateral sway with eyelid/mouth cycling | SECONDARY | 2/6 | AUTONOMOUS | HIGH |
| PIKA-MF-028 | Autonomous clasped-paw side-to-side bow/sway | SECONDARY | 1/6 | AUTONOMOUS | HIGH |
| PIKA-MF-030 | Autonomous head/neck arc-sway | SECONDARY | 1/6 | AUTONOMOUS / AFTERGLOW UNCERTAIN | HIGH |
| PIKA-MF-031 | Autonomous turn-and-bow-like compression gesture | SECONDARY | 1/6 | AUTONOMOUS / CHARACTER_INITIATED_SOCIAL UNCERTAIN | MEDIUM |
| PIKA-MF-032 | Autonomous self-touch / pondering lateral tilt | SECONDARY | 2/6 | AUTONOMOUS / visual context | HIGH |
| PIKA-MF-033 | Touch-interrupted doze → wake/startle expansion → recovery | SECONDARY | 1/6 | PLAYER_TRIGGERED / RECIPROCAL | HIGH |
| PIKA-MF-045 | Closed-eye gathered-paw head/torso lower-and-lean | PRIMARY | 1/6 | BOTH / UNKNOWN | HIGH |
| PIKA-MF-047 | Tail-region contact → local tail displacement/sweep with body lean | SECONDARY | 1/6 | PLAYER_TRIGGERED | MEDIUM |

## 10. Forelimb / Paw Gesture Master

| Family | Name | Category Role | Coverage | Initiation | Front View |
| --- | --- | --- | --- | --- | --- |
| PIKA-MF-010 | Two-paw cheek press / face-mug sequence | PRIMARY | 1/6 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-011 | Bilateral cheek-level ecstatic stretch / head-back expansion | SECONDARY | 1/6 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-012 | One-forelimb local acknowledgement / raise | PRIMARY | 4/6 | PLAYER_TRIGGERED / UNCERTAIN | HIGH |
| PIKA-MF-020 | Attention / gaze / head tracking-turn | SECONDARY | 2/6 | PLAYER_TRIGGERED / visual association | MEDIUM |
| PIKA-MF-021 | One-paw social offer and moving WAIT | SECONDARY | 2/6 | CHARACTER_INITIATED_SOCIAL / RECIPROCAL | HIGH |
| PIKA-MF-022 | Presented-paw contact acknowledgement pulse | SECONDARY | 2/6 | RECIPROCAL | HIGH |
| PIKA-MF-024 | Large positive bilateral open-arm whole-body delight | SECONDARY | 5/6 | PLAYER_TRIGGERED / SYSTEM-UNKNOWN | HIGH |
| PIKA-MF-032 | Autonomous self-touch / pondering lateral tilt | SECONDARY | 2/6 | AUTONOMOUS / visual context | HIGH |

## 11. Autonomous Idle Master

| Family | Name | Category Role | Coverage | Initiation | Front View |
| --- | --- | --- | --- | --- | --- |
| PIKA-MF-001 | Neutral attentive intentional-stillness / low-motion moving hold | SECONDARY | 6/6 | AUTONOMOUS / SYSTEM / UNKNOWN | HIGH |
| PIKA-MF-004 | Independent tail ambient micro / sweep / oscillation | SECONDARY | 3/6 | AUTONOMOUS / BOTH | MEDIUM |
| PIKA-MF-023 | Two-forelimb lift + head-dip stern sequence | SECONDARY | 1/6 | BOTH | HIGH |
| PIKA-MF-025 | Autonomous bilateral forelimb-open body pulse | PRIMARY | 2/6 | AUTONOMOUS / UNKNOWN | HIGH |
| PIKA-MF-026 | Autonomous closed-eye side-lean hold | PRIMARY | 1/6 | AUTONOMOUS | MEDIUM |
| PIKA-MF-027 | Autonomous drowsy lateral sway with eyelid/mouth cycling | PRIMARY | 2/6 | AUTONOMOUS | HIGH |
| PIKA-MF-028 | Autonomous clasped-paw side-to-side bow/sway | PRIMARY | 1/6 | AUTONOMOUS | HIGH |
| PIKA-MF-029 | Prolonged closed-eye rest / doze moving hold | SECONDARY | 2/6 | AUTONOMOUS | HIGH |
| PIKA-MF-030 | Autonomous head/neck arc-sway | PRIMARY | 1/6 | AUTONOMOUS / AFTERGLOW UNCERTAIN | HIGH |
| PIKA-MF-031 | Autonomous turn-and-bow-like compression gesture | PRIMARY | 1/6 | AUTONOMOUS / CHARACTER_INITIATED_SOCIAL UNCERTAIN | MEDIUM |
| PIKA-MF-032 | Autonomous self-touch / pondering lateral tilt | PRIMARY | 2/6 | AUTONOMOUS / visual context | HIGH |
| PIKA-MF-045 | Closed-eye gathered-paw head/torso lower-and-lean | SECONDARY | 1/6 | BOTH / UNKNOWN | HIGH |
| PIKA-MF-046 | Brief closed-eye open-mouth smile pulse from neutral | PRIMARY | 1/6 | UNKNOWN / autonomous-looking | HIGH |

## 12. Autonomous Social Master

| Family | Name | Category Role | Coverage | Initiation | Front View |
| --- | --- | --- | --- | --- | --- |
| PIKA-MF-021 | One-paw social offer and moving WAIT | SECONDARY | 2/6 | CHARACTER_INITIATED_SOCIAL / RECIPROCAL | HIGH |
| PIKA-MF-025 | Autonomous bilateral forelimb-open body pulse | SECONDARY | 2/6 | AUTONOMOUS / UNKNOWN | HIGH |
| PIKA-MF-031 | Autonomous turn-and-bow-like compression gesture | SECONDARY | 1/6 | AUTONOMOUS / CHARACTER_INITIATED_SOCIAL UNCERTAIN | MEDIUM |
| PIKA-MF-032 | Autonomous self-touch / pondering lateral tilt | SECONDARY | 2/6 | AUTONOMOUS / visual context | HIGH |
| PIKA-MF-036 | Bilateral gift/item presentation moving hold | SECONDARY | 4/6 | SYSTEM / CHARACTER_INITIATED_SOCIAL / UNKNOWN | MEDIUM |

## 13. Positive Touch Master

| Family | Name | Category Role | Coverage | Initiation | Front View |
| --- | --- | --- | --- | --- | --- |
| PIKA-MF-006 | Sustained positive-contact content hold / soften | PRIMARY | 2/6 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-007 | Positive-touch facial response pulse / delight completion cycle | PRIMARY | 6/6 | PLAYER_TRIGGERED / AFTERGLOW | HIGH |
| PIKA-MF-008 | Touch-positive closed-eye head-lower content bow | SECONDARY | 1/6 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-009 | Deep lateral positive-content lean with ear rotation | SECONDARY | 2/6 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-010 | Two-paw cheek press / face-mug sequence | SECONDARY | 1/6 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-011 | Bilateral cheek-level ecstatic stretch / head-back expansion | SECONDARY | 1/6 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-012 | One-forelimb local acknowledgement / raise | SECONDARY | 4/6 | PLAYER_TRIGGERED / UNCERTAIN | HIGH |
| PIKA-MF-013 | Interaction-linked open-mouth lateral body sway | PRIMARY | 1/6 | PLAYER_TRIGGERED / interaction-linked | HIGH |
| PIKA-MF-022 | Presented-paw contact acknowledgement pulse | SECONDARY | 2/6 | RECIPROCAL | HIGH |
| PIKA-MF-024 | Large positive bilateral open-arm whole-body delight | SECONDARY | 5/6 | PLAYER_TRIGGERED / SYSTEM-UNKNOWN | HIGH |
| PIKA-MF-033 | Touch-interrupted doze → wake/startle expansion → recovery | SECONDARY | 1/6 | PLAYER_TRIGGERED / RECIPROCAL | HIGH |
| PIKA-MF-035 | Feeding-completion positive delight | SECONDARY | 5/6 | PLAYER_TRIGGERED / feeding consequence | HIGH |
| PIKA-MF-038 | Closed-eye content afterglow / low-motion settle | SECONDARY | 2/6 | RECIPROCAL / PLAYER_TRIGGERED / SYSTEM-UNKNOWN | HIGH |
| PIKA-MF-045 | Closed-eye gathered-paw head/torso lower-and-lean | SECONDARY | 1/6 | BOTH / UNKNOWN | HIGH |
| PIKA-MF-047 | Tail-region contact → local tail displacement/sweep with body lean | SECONDARY | 1/6 | PLAYER_TRIGGERED | MEDIUM |

## 14. Negative / Boundary Master

| Family | Name | Category Role | Coverage | Initiation | Front View |
| --- | --- | --- | --- | --- | --- |
| PIKA-MF-014 | Contact-linked facial sensitivity / displeased warning state | PRIMARY | 3/6 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-015 | Boundary upper-body recoil / compression / withdrawal | PRIMARY | 2/6 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-016 | Compression → open-arm negative hero reaction | PRIMARY | 1/6 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-017 | Rear/side eyes-closed disengaged moving hold | SECONDARY | 1/6 | PLAYER_TRIGGERED state | LOW |
| PIKA-MF-018 | Rear-contact glance-back warning and turn-away | PRIMARY | 1/6 | PLAYER_TRIGGERED | LOW |
| PIKA-MF-023 | Two-forelimb lift + head-dip stern sequence | PRIMARY | 1/6 | BOTH | HIGH |

## 15. Reciprocal Social Interaction Master

| Family | Name | Category Role | Coverage | Initiation | Front View |
| --- | --- | --- | --- | --- | --- |
| PIKA-MF-021 | One-paw social offer and moving WAIT | PRIMARY | 2/6 | CHARACTER_INITIATED_SOCIAL / RECIPROCAL | HIGH |
| PIKA-MF-022 | Presented-paw contact acknowledgement pulse | PRIMARY | 2/6 | RECIPROCAL | HIGH |
| PIKA-MF-033 | Touch-interrupted doze → wake/startle expansion → recovery | PRIMARY | 1/6 | PLAYER_TRIGGERED / RECIPROCAL | HIGH |
| PIKA-MF-038 | Closed-eye content afterglow / low-motion settle | SECONDARY | 2/6 | RECIPROCAL / PLAYER_TRIGGERED / SYSTEM-UNKNOWN | HIGH |

## 16. Feeding Master

| Family | Name | Category Role | Coverage | Initiation | Front View |
| --- | --- | --- | --- | --- | --- |
| PIKA-MF-034 | Feeding orient / mouth-contact hold / item-disappearance transition | PRIMARY | 5/6 | PLAYER_TRIGGERED / SYSTEM | MEDIUM |
| PIKA-MF-035 | Feeding-completion positive delight | PRIMARY | 5/6 | PLAYER_TRIGGERED / feeding consequence | HIGH |
| PIKA-MF-041 | System/UI/menu/item-mode transition without reliable body motion | SECONDARY | 3/6 | SYSTEM | LOW |

## 17. Gift / Item Master

| Family | Name | Category Role | Coverage | Initiation | Front View |
| --- | --- | --- | --- | --- | --- |
| PIKA-MF-036 | Bilateral gift/item presentation moving hold | PRIMARY | 4/6 | SYSTEM / CHARACTER_INITIATED_SOCIAL / UNKNOWN | MEDIUM |
| PIKA-MF-037 | Gift/item release / forelimb opening / positive completion | PRIMARY | 4/6 | SYSTEM / CHARACTER_INITIATED_SOCIAL / UNKNOWN | HIGH |
| PIKA-MF-038 | Closed-eye content afterglow / low-motion settle | SECONDARY | 2/6 | RECIPROCAL / PLAYER_TRIGGERED / SYSTEM-UNKNOWN | HIGH |

## 18. Large Emotional / Hero Master

| Family | Name | Category Role | Coverage | Initiation | Front View |
| --- | --- | --- | --- | --- | --- |
| PIKA-MF-007 | Positive-touch facial response pulse / delight completion cycle | SECONDARY | 6/6 | PLAYER_TRIGGERED / AFTERGLOW | HIGH |
| PIKA-MF-011 | Bilateral cheek-level ecstatic stretch / head-back expansion | PRIMARY | 1/6 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-016 | Compression → open-arm negative hero reaction | SECONDARY | 1/6 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-024 | Large positive bilateral open-arm whole-body delight | PRIMARY | 5/6 | PLAYER_TRIGGERED / SYSTEM-UNKNOWN | HIGH |
| PIKA-MF-025 | Autonomous bilateral forelimb-open body pulse | SECONDARY | 2/6 | AUTONOMOUS / UNKNOWN | HIGH |
| PIKA-MF-035 | Feeding-completion positive delight | SECONDARY | 5/6 | PLAYER_TRIGGERED / feeding consequence | HIGH |
| PIKA-MF-037 | Gift/item release / forelimb opening / positive completion | SECONDARY | 4/6 | SYSTEM / CHARACTER_INITIATED_SOCIAL / UNKNOWN | HIGH |
| PIKA-MF-043 | Close-up entry head-dip / smile-open-mouth expression sequence | PRIMARY | 1/6 | SYSTEM / UNKNOWN | HIGH |
| PIKA-MF-044 | Foreground close-pass → close-up content hold | PRIMARY | 1/6 | SYSTEM / UNKNOWN | MEDIUM |
| PIKA-MF-046 | Brief closed-eye open-mouth smile pulse from neutral | SECONDARY | 1/6 | UNKNOWN / autonomous-looking | HIGH |

## 19. Recovery / Settle / Afterglow Master

| Family | Name | Category Role | Coverage | Initiation | Front View |
| --- | --- | --- | --- | --- | --- |
| PIKA-MF-003 | Expression-linked eyelid close / half-lid / reopen transition | SECONDARY | 1/6 | BOTH / UNKNOWN | HIGH |
| PIKA-MF-006 | Sustained positive-contact content hold / soften | SECONDARY | 2/6 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-007 | Positive-touch facial response pulse / delight completion cycle | SECONDARY | 6/6 | PLAYER_TRIGGERED / AFTERGLOW | HIGH |
| PIKA-MF-008 | Touch-positive closed-eye head-lower content bow | SECONDARY | 1/6 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-009 | Deep lateral positive-content lean with ear rotation | SECONDARY | 2/6 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-011 | Bilateral cheek-level ecstatic stretch / head-back expansion | SECONDARY | 1/6 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-012 | One-forelimb local acknowledgement / raise | SECONDARY | 4/6 | PLAYER_TRIGGERED / UNCERTAIN | HIGH |
| PIKA-MF-014 | Contact-linked facial sensitivity / displeased warning state | SECONDARY | 3/6 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-015 | Boundary upper-body recoil / compression / withdrawal | SECONDARY | 2/6 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-023 | Two-forelimb lift + head-dip stern sequence | SECONDARY | 1/6 | BOTH | HIGH |
| PIKA-MF-024 | Large positive bilateral open-arm whole-body delight | SECONDARY | 5/6 | PLAYER_TRIGGERED / SYSTEM-UNKNOWN | HIGH |
| PIKA-MF-026 | Autonomous closed-eye side-lean hold | SECONDARY | 1/6 | AUTONOMOUS | MEDIUM |
| PIKA-MF-027 | Autonomous drowsy lateral sway with eyelid/mouth cycling | SECONDARY | 2/6 | AUTONOMOUS | HIGH |
| PIKA-MF-028 | Autonomous clasped-paw side-to-side bow/sway | SECONDARY | 1/6 | AUTONOMOUS | HIGH |
| PIKA-MF-029 | Prolonged closed-eye rest / doze moving hold | SECONDARY | 2/6 | AUTONOMOUS | HIGH |
| PIKA-MF-031 | Autonomous turn-and-bow-like compression gesture | SECONDARY | 1/6 | AUTONOMOUS / CHARACTER_INITIATED_SOCIAL UNCERTAIN | MEDIUM |
| PIKA-MF-032 | Autonomous self-touch / pondering lateral tilt | SECONDARY | 2/6 | AUTONOMOUS / visual context | HIGH |
| PIKA-MF-033 | Touch-interrupted doze → wake/startle expansion → recovery | SECONDARY | 1/6 | PLAYER_TRIGGERED / RECIPROCAL | HIGH |
| PIKA-MF-035 | Feeding-completion positive delight | SECONDARY | 5/6 | PLAYER_TRIGGERED / feeding consequence | HIGH |
| PIKA-MF-037 | Gift/item release / forelimb opening / positive completion | SECONDARY | 4/6 | SYSTEM / CHARACTER_INITIATED_SOCIAL / UNKNOWN | HIGH |
| PIKA-MF-038 | Closed-eye content afterglow / low-motion settle | PRIMARY | 2/6 | RECIPROCAL / PLAYER_TRIGGERED / SYSTEM-UNKNOWN | HIGH |
| PIKA-MF-039 | Half-lidded / droopy facial recovery settle | PRIMARY | 2/6 | AFTERGLOW / UNKNOWN | HIGH |
| PIKA-MF-040 | General active-pose return-to-neutral settle / recovery | PRIMARY | 2/6 | BOTH / SYSTEM | HIGH |
| PIKA-MF-043 | Close-up entry head-dip / smile-open-mouth expression sequence | SECONDARY | 1/6 | SYSTEM / UNKNOWN | HIGH |
| PIKA-MF-046 | Brief closed-eye open-mouth smile pulse from neutral | SECONDARY | 1/6 | UNKNOWN / autonomous-looking | HIGH |

## 20. Intentional Stillness / WAIT Master

| Family | Name | Category Role | Coverage | Initiation | Front View |
| --- | --- | --- | --- | --- | --- |
| PIKA-MF-001 | Neutral attentive intentional-stillness / low-motion moving hold | PRIMARY | 6/6 | AUTONOMOUS / SYSTEM / UNKNOWN | HIGH |
| PIKA-MF-006 | Sustained positive-contact content hold / soften | SECONDARY | 2/6 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-017 | Rear/side eyes-closed disengaged moving hold | PRIMARY | 1/6 | PLAYER_TRIGGERED state | LOW |
| PIKA-MF-021 | One-paw social offer and moving WAIT | SECONDARY | 2/6 | CHARACTER_INITIATED_SOCIAL / RECIPROCAL | HIGH |
| PIKA-MF-029 | Prolonged closed-eye rest / doze moving hold | SECONDARY | 2/6 | AUTONOMOUS | HIGH |
| PIKA-MF-034 | Feeding orient / mouth-contact hold / item-disappearance transition | SECONDARY | 5/6 | PLAYER_TRIGGERED / SYSTEM | MEDIUM |
| PIKA-MF-036 | Bilateral gift/item presentation moving hold | SECONDARY | 4/6 | SYSTEM / CHARACTER_INITIATED_SOCIAL / UNKNOWN | MEDIUM |
| PIKA-MF-038 | Closed-eye content afterglow / low-motion settle | SECONDARY | 2/6 | RECIPROCAL / PLAYER_TRIGGERED / SYSTEM-UNKNOWN | HIGH |
| PIKA-MF-044 | Foreground close-pass → close-up content hold | SECONDARY | 1/6 | SYSTEM / UNKNOWN | MEDIUM |

## 21. Transition Master

| Family | Name | Category Role | Coverage | Initiation | Front View |
| --- | --- | --- | --- | --- | --- |
| PIKA-MF-018 | Rear-contact glance-back warning and turn-away | SECONDARY | 1/6 | PLAYER_TRIGGERED | LOW |
| PIKA-MF-019 | Side/back → front reorientation | PRIMARY | 1/6 | PLAYER_TRIGGERED / TRANSITION | MEDIUM |
| PIKA-MF-034 | Feeding orient / mouth-contact hold / item-disappearance transition | SECONDARY | 5/6 | PLAYER_TRIGGERED / SYSTEM | MEDIUM |
| PIKA-MF-037 | Gift/item release / forelimb opening / positive completion | SECONDARY | 4/6 | SYSTEM / CHARACTER_INITIATED_SOCIAL / UNKNOWN | HIGH |
| PIKA-MF-040 | General active-pose return-to-neutral settle / recovery | SECONDARY | 2/6 | BOTH / SYSTEM | HIGH |
| PIKA-MF-041 | System/UI/menu/item-mode transition without reliable body motion | PRIMARY | 3/6 | SYSTEM | LOW |
| PIKA-MF-042 | Visible screen-relative character entry / exit transition | PRIMARY | 1/6 | SYSTEM / TRANSITION | MEDIUM |
| PIKA-MF-043 | Close-up entry head-dip / smile-open-mouth expression sequence | SECONDARY | 1/6 | SYSTEM / UNKNOWN | HIGH |
| PIKA-MF-044 | Foreground close-pass → close-up content hold | SECONDARY | 1/6 | SYSTEM / UNKNOWN | MEDIUM |
| PIKA-MF-045 | Closed-eye gathered-paw head/torso lower-and-lean | SECONDARY | 1/6 | BOTH / UNKNOWN | HIGH |

## 22. Emotion / Motion Propagation Patterns

| Pattern | Observed propagation | Families / sources | What remains quiet |
| --- | --- | --- | --- |
| Positive contact | face / eyelids / mouth → head/torso → ears/tail as late follow-through; large variants may recruit forelimbs/root | PIKA-MF-006/007/024; V1 F03/F04/F08, V2 F05/F04, V4 MF04/MF10, V5 F02/F05, V6 F03/F06 | feet/root often remain quiet in small/medium responses |
| Boundary escalation | face warning → head/ears → torso compression/withdrawal → forelimbs/tail follow | PIKA-MF-014/015/016; V1 F05, V2 F06/F07/F08, V5 F06 | feet/hindlimbs usually retain support |
| Reciprocal paw exchange | paw presentation → WAIT → visible contact → facial acknowledgement → continue/retract/settle | PIKA-MF-021/022; V3 PF05/PF06, V5 F03/F04 | root/other paw comparatively quiet |
| Feeding | item approach / attention → mouth-area hold/disappearance → delayed face-led delight → settle | PIKA-MF-034/035; V1 F09/F10, V3 PF09, V4 MF11/MF12, V5 F09/F10, V6 F12/F13 | forelimbs/root generally quiet |
| Gift/item | bilateral presentation hold → face/forelimb release/opening → positive afterglow / droopy settle | PIKA-MF-036/037/038/039; V3 PF10, V4 MF18/MF19, V5 F11/F12/F08, V6 F15/F16/F17 | feet/support remain stable |
| Autonomous affect | face/head or forelimbs lead → torso/root follows → held pose/sway → staged recovery | PIKA-MF-025–032,046 | feet commonly stay planted; tail is behavior-specific rather than universal |

## 23. Grounding / Support Patterns

| Grounding pattern | Observed use | Representative Families | Evidence boundary |
| --- | --- | --- | --- |
| PLANTED baseline | Most stillness, touch, feeding, gift, and autonomous phrases retain support | 001,006,007,009–015,021–023,025,027–040,046–047 | Direct where feet visible; crop-unknown is never upgraded |
| WEIGHT_SHIFT without step | Deep lateral lean, drowsy sway, self-touch tilt, turn/bow phrases | 009,027,028,031,032,033,047 | Feet remain planted in sources that show them |
| TURN / rotational root | Side/back→front reorientation and autonomous turn/bow | 019,031 | Exact stepping can be occluded |
| Possible SUPPORT_CHANGE | Largest positive hero variants in V1/V2 | 024 | Source labels retain V2/U support uncertainty |
| Screen-relative/camera-ambiguous | Entry/exit and foreground close-pass | 042,044 | Not treated as authored root locomotion with certainty |

## 24. Tail Role Master

| Tail Role | Master use | Representative Families / sources |
| --- | --- | --- |
| PRIMARY_ACTION / LOCAL_RESPONSE | Tail itself is the principal local response | 047 / V4 MF07 |
| INDEPENDENT_MICRO | Tail moves while major body remains quiet | 004 / V1 F14, V2 F03, V5 F17 |
| FOLLOW_THROUGH | Tail follows head/torso/root commitment | 006,009,015,024,026–029,033,037 |
| EMOTION_AMPLIFIER | Tail contributes to larger affect after lead channels commit | 007,013,016,024,035 |
| QUIET | Feeding, paw WAIT/ack, gift hold, several self/face gestures keep tail non-primary | 012,021,022,034,036,039 |
| UNCLEAR / crop unavailable | Close-up sources cannot safely assign tail role | 003,008,014,043 |

## 25. Repetition / Variation

### Cross-video repetition

| Family | Coverage | Frequency | Variant clusters | Repetition risk |
| --- | --- | --- | --- | --- |
| PIKA-MF-001 | 6/6 | COMMON | 6 | HIGH |
| PIKA-MF-007 | 6/6 | COMMON | 8 | HIGH |
| PIKA-MF-024 | 5/6 | COMMON | 5 | HIGH |
| PIKA-MF-034 | 5/6 | COMMON | 5 | HIGH |
| PIKA-MF-035 | 5/6 | COMMON | 5 | HIGH |
| PIKA-MF-012 | 4/6 | RECURRING | 4 | MEDIUM |
| PIKA-MF-036 | 4/6 | RECURRING | 4 | MEDIUM |
| PIKA-MF-037 | 4/6 | RECURRING | 4 | MEDIUM |
| PIKA-MF-002 | 3/6 | RECURRING | 3 | MEDIUM |
| PIKA-MF-004 | 3/6 | RECURRING | 3 | MEDIUM |
| PIKA-MF-014 | 3/6 | RECURRING | 3 | MEDIUM |
| PIKA-MF-041 | 3/6 | RECURRING | 4 | MEDIUM |
| PIKA-MF-006 | 2/6 | LIMITED | 2 | LOW |
| PIKA-MF-009 | 2/6 | LIMITED | 2 | LOW |
| PIKA-MF-015 | 2/6 | LIMITED | 2 | LOW |
| PIKA-MF-020 | 2/6 | LIMITED | 2 | LOW |
| PIKA-MF-021 | 2/6 | LIMITED | 2 | LOW |
| PIKA-MF-022 | 2/6 | LIMITED | 2 | LOW |
| PIKA-MF-025 | 2/6 | LIMITED | 2 | LOW |
| PIKA-MF-027 | 2/6 | LIMITED | 2 | LOW |
| PIKA-MF-029 | 2/6 | LIMITED | 2 | LOW |
| PIKA-MF-032 | 2/6 | LIMITED | 2 | LOW |
| PIKA-MF-038 | 2/6 | LIMITED | 2 | LOW |
| PIKA-MF-039 | 2/6 | LIMITED | 3 | LOW |
| PIKA-MF-040 | 2/6 | LIMITED | 2 | LOW |
| PIKA-MF-003 | 1/6 | SINGLE-VIDEO | 1 | LOW |
| PIKA-MF-005 | 1/6 | SINGLE-VIDEO | 1 | LOW |
| PIKA-MF-008 | 1/6 | SINGLE-VIDEO | 1 | LOW |
| PIKA-MF-010 | 1/6 | SINGLE-VIDEO | 1 | LOW |
| PIKA-MF-011 | 1/6 | SINGLE-VIDEO | 1 | LOW |
| PIKA-MF-013 | 1/6 | SINGLE-VIDEO | 1 | LOW |
| PIKA-MF-016 | 1/6 | SINGLE-VIDEO | 1 | LOW |
| PIKA-MF-017 | 1/6 | SINGLE-VIDEO | 1 | LOW |
| PIKA-MF-018 | 1/6 | SINGLE-VIDEO | 1 | LOW |
| PIKA-MF-019 | 1/6 | SINGLE-VIDEO | 1 | LOW |
| PIKA-MF-023 | 1/6 | SINGLE-VIDEO | 1 | LOW |
| PIKA-MF-026 | 1/6 | SINGLE-VIDEO | 1 | LOW |
| PIKA-MF-028 | 1/6 | SINGLE-VIDEO | 1 | LOW |
| PIKA-MF-030 | 1/6 | SINGLE-VIDEO | 1 | LOW |
| PIKA-MF-031 | 1/6 | SINGLE-VIDEO | 1 | LOW |
| PIKA-MF-033 | 1/6 | SINGLE-VIDEO | 1 | LOW |
| PIKA-MF-042 | 1/6 | SINGLE-VIDEO | 1 | LOW |
| PIKA-MF-043 | 1/6 | SINGLE-VIDEO | 1 | LOW |
| PIKA-MF-044 | 1/6 | SINGLE-VIDEO | 1 | LOW |
| PIKA-MF-045 | 1/6 | SINGLE-VIDEO | 1 | LOW |
| PIKA-MF-046 | 1/6 | SINGLE-VIDEO | 1 | LOW |
| PIKA-MF-047 | 1/6 | SINGLE-VIDEO | 1 | LOW |

### Variant axes preserved

- side / screen-side; amplitude; duration; initial state; eyelid/mouth state; ear orientation; forelimb recruitment; torso/COM recruitment; tail role; contact location; interaction phase; settle; afterglow; autonomous vs player-triggered cause.
- VFX/audio/UI differences alone never create a body-motion Variant.

## 26. Temporal Structure Patterns

| Grammar | Families | Observed phases |
| --- | --- | --- |
| Positive touch | 006/007/008/009/010/011/012/013 | contact or visible interaction → onset → optional build/anticipation → peak/hold → follow-through → settle |
| Boundary | 014/015/016/017/018 | contact/state → face warning → optional body withdrawal/compression → hold/hero peak → recovery or disengaged hold |
| Reciprocal paw | 021/022 | prepare → present → WAIT → contact → acknowledgement → continuation/completion → retract/afterglow |
| Large positive | 024 | initial state → compression/anticipation → torso/root/forelimb commit → open peak → lower/recenter → settle |
| Feeding | 034/035 | item approach → mouth-area hold → disappearance/pause → delayed positive reaction → settle |
| Gift | 036/037/038/039 | presentation hold → expression transition → item disappearance/release → forelimb opening → positive afterglow → neutral/droopy settle |
| Autonomous state | 025–032,046 | neutral/stillness → local onset → bounded action/hold → staged return; exact trigger usually unknown |

## 27. Front-View Readability Matrix

| Family | Front View | Why / limiting factor |
| --- | --- | --- |
| PIKA-MF-001 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-002 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-003 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-004 | MEDIUM | Readable but side/depth/tail/camera ambiguity reduces certainty |
| PIKA-MF-005 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-006 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-007 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-008 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-009 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-010 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-011 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-012 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-013 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-014 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-015 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-016 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-017 | LOW | Depends on rear/side or UI/system state rather than front-facing body action |
| PIKA-MF-018 | LOW | Depends on rear/side or UI/system state rather than front-facing body action |
| PIKA-MF-019 | MEDIUM | Readable but side/depth/tail/camera ambiguity reduces certainty |
| PIKA-MF-020 | MEDIUM | Readable but side/depth/tail/camera ambiguity reduces certainty |
| PIKA-MF-021 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-022 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-023 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-024 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-025 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-026 | MEDIUM | Readable but side/depth/tail/camera ambiguity reduces certainty |
| PIKA-MF-027 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-028 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-029 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-030 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-031 | MEDIUM | Readable but side/depth/tail/camera ambiguity reduces certainty |
| PIKA-MF-032 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-033 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-034 | MEDIUM | Readable but side/depth/tail/camera ambiguity reduces certainty |
| PIKA-MF-035 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-036 | MEDIUM | Readable but side/depth/tail/camera ambiguity reduces certainty |
| PIKA-MF-037 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-038 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-039 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-040 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-041 | LOW | Depends on rear/side or UI/system state rather than front-facing body action |
| PIKA-MF-042 | MEDIUM | Readable but side/depth/tail/camera ambiguity reduces certainty |
| PIKA-MF-043 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-044 | MEDIUM | Readable but side/depth/tail/camera ambiguity reduces certainty |
| PIKA-MF-045 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-046 | HIGH | Face/silhouette/forelimb mechanics are directly readable |
| PIKA-MF-047 | MEDIUM | Readable but side/depth/tail/camera ambiguity reduces certainty |

**Count:** HIGH 34 / MEDIUM 10 / LOW 3. LOW Families are retained, not deleted.

## 28. Cross-Video Source Matrix

| Master Family | Name | V1 | V2 | V3 | V4 | V5 | V6 | Coverage |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PIKA-MF-001 | Neutral attentive intentional-stillness / low-motion moving hold | F02 | F01 | PF-02 | MF-01 | F13 | F02 | 6/6 |
| PIKA-MF-002 | Spontaneous isolated blink | F01 | F02 | PF-03 | — | — | — | 3/6 |
| PIKA-MF-003 | Expression-linked eyelid close / half-lid / reopen transition | — | — | — | — | F15 | — | 1/6 |
| PIKA-MF-004 | Independent tail ambient micro / sweep / oscillation | F14 | F03 | — | — | F17 | — | 3/6 |
| PIKA-MF-005 | Ear orientation micro-correction | F15 | — | — | — | — | — | 1/6 |
| PIKA-MF-006 | Sustained positive-contact content hold / soften | F03 | — | — | — | — | F04 | 2/6 |
| PIKA-MF-007 | Positive-touch facial response pulse / delight completion cycle | F04 | F05 | PF-04 | MF-04, MF-08 | F02, F05 | F03 | 6/6 |
| PIKA-MF-008 | Touch-positive closed-eye head-lower content bow | — | — | — | — | — | F05 | 1/6 |
| PIKA-MF-009 | Deep lateral positive-content lean with ear rotation | — | — | — | MF-06 | — | F08 | 2/6 |
| PIKA-MF-010 | Two-paw cheek press / face-mug sequence | — | — | — | MF-05 | — | — | 1/6 |
| PIKA-MF-011 | Bilateral cheek-level ecstatic stretch / head-back expansion | — | — | — | — | — | F09 | 1/6 |
| PIKA-MF-012 | One-forelimb local acknowledgement / raise | — | F12 | PF-11 | MF-03 | — | F07 | 4/6 |
| PIKA-MF-013 | Interaction-linked open-mouth lateral body sway | — | F13 | — | — | — | — | 1/6 |
| PIKA-MF-014 | Contact-linked facial sensitivity / displeased warning state | — | F06 | — | MF-09 | F06 | — | 3/6 |
| PIKA-MF-015 | Boundary upper-body recoil / compression / withdrawal | F05 | F07 | — | — | — | — | 2/6 |
| PIKA-MF-016 | Compression → open-arm negative hero reaction | — | F08 | — | — | — | — | 1/6 |
| PIKA-MF-017 | Rear/side eyes-closed disengaged moving hold | — | F09 | — | — | — | — | 1/6 |
| PIKA-MF-018 | Rear-contact glance-back warning and turn-away | — | F10 | — | — | — | — | 1/6 |
| PIKA-MF-019 | Side/back → front reorientation | — | F11 | — | — | — | — | 1/6 |
| PIKA-MF-020 | Attention / gaze / head tracking-turn | F07 | — | — | — | F07 | — | 2/6 |
| PIKA-MF-021 | One-paw social offer and moving WAIT | — | — | PF-05 | — | F03 | — | 2/6 |
| PIKA-MF-022 | Presented-paw contact acknowledgement pulse | — | — | PF-06 | — | F04 | — | 2/6 |
| PIKA-MF-023 | Two-forelimb lift + head-dip stern sequence | F06 | — | — | — | — | — | 1/6 |
| PIKA-MF-024 | Large positive bilateral open-arm whole-body delight | F08 | F04 | PF-04 | MF-10 | — | F06 | 5/6 |
| PIKA-MF-025 | Autonomous bilateral forelimb-open body pulse | F13 | — | — | — | F14 | — | 2/6 |
| PIKA-MF-026 | Autonomous closed-eye side-lean hold | F11 | — | — | — | — | — | 1/6 |
| PIKA-MF-027 | Autonomous drowsy lateral sway with eyelid/mouth cycling | — | F14 | — | MF-14 | — | — | 2/6 |
| PIKA-MF-028 | Autonomous clasped-paw side-to-side bow/sway | — | — | — | MF-13 | — | — | 1/6 |
| PIKA-MF-029 | Prolonged closed-eye rest / doze moving hold | F12 | — | — | MF-16 | — | — | 2/6 |
| PIKA-MF-030 | Autonomous head/neck arc-sway | — | — | PF-07 | — | — | — | 1/6 |
| PIKA-MF-031 | Autonomous turn-and-bow-like compression gesture | — | — | PF-12 | — | — | — | 1/6 |
| PIKA-MF-032 | Autonomous self-touch / pondering lateral tilt | — | — | — | MF-15 | — | F18 | 2/6 |
| PIKA-MF-033 | Touch-interrupted doze → wake/startle expansion → recovery | — | — | — | MF-17 | — | — | 1/6 |
| PIKA-MF-034 | Feeding orient / mouth-contact hold / item-disappearance transition | F09 | — | PF-09 | MF-11 | F09 | F12 | 5/6 |
| PIKA-MF-035 | Feeding-completion positive delight | F10 | — | PF-09 | MF-12 | F10 | F13 | 5/6 |
| PIKA-MF-036 | Bilateral gift/item presentation moving hold | — | — | PF-10 | MF-18 | F11 | F15 | 4/6 |
| PIKA-MF-037 | Gift/item release / forelimb opening / positive completion | — | — | PF-10 | MF-19 | F12 | F16 | 4/6 |
| PIKA-MF-038 | Closed-eye content afterglow / low-motion settle | — | — | — | — | F08 | F17 | 2/6 |
| PIKA-MF-039 | Half-lidded / droopy facial recovery settle | — | — | PF-08 | — | — | F10, F17 | 2/6 |
| PIKA-MF-040 | General active-pose return-to-neutral settle / recovery | F16 | F15 | — | — | — | — | 2/6 |
| PIKA-MF-041 | System/UI/menu/item-mode transition without reliable body motion | — | — | PF-01 | MF-20 | — | F11, F14 | 3/6 |
| PIKA-MF-042 | Visible screen-relative character entry / exit transition | — | — | PF-01 | — | — | — | 1/6 |
| PIKA-MF-043 | Close-up entry head-dip / smile-open-mouth expression sequence | — | — | — | — | F01 | — | 1/6 |
| PIKA-MF-044 | Foreground close-pass → close-up content hold | — | — | — | — | — | F01 | 1/6 |
| PIKA-MF-045 | Closed-eye gathered-paw head/torso lower-and-lean | — | — | — | MF-02 | — | — | 1/6 |
| PIKA-MF-046 | Brief closed-eye open-mouth smile pulse from neutral | — | — | — | — | F16 | — | 1/6 |
| PIKA-MF-047 | Tail-region contact → local tail displacement/sweep with body lean | — | — | — | MF-07 | — | — | 1/6 |

## 29. Cross-Video Shared Families

### 6/6

`PIKA-MF-001` Neutral attentive intentional-stillness / low-motion moving hold, `PIKA-MF-007` Positive-touch facial response pulse / delight completion cycle

### 5/6

`PIKA-MF-024` Large positive bilateral open-arm whole-body delight, `PIKA-MF-034` Feeding orient / mouth-contact hold / item-disappearance transition, `PIKA-MF-035` Feeding-completion positive delight

### 4/6

`PIKA-MF-012` One-forelimb local acknowledgement / raise, `PIKA-MF-036` Bilateral gift/item presentation moving hold, `PIKA-MF-037` Gift/item release / forelimb opening / positive completion

### 3/6

`PIKA-MF-002` Spontaneous isolated blink, `PIKA-MF-004` Independent tail ambient micro / sweep / oscillation, `PIKA-MF-014` Contact-linked facial sensitivity / displeased warning state, `PIKA-MF-041` System/UI/menu/item-mode transition without reliable body motion

### 2/6

`PIKA-MF-006` Sustained positive-contact content hold / soften, `PIKA-MF-009` Deep lateral positive-content lean with ear rotation, `PIKA-MF-015` Boundary upper-body recoil / compression / withdrawal, `PIKA-MF-020` Attention / gaze / head tracking-turn, `PIKA-MF-021` One-paw social offer and moving WAIT, `PIKA-MF-022` Presented-paw contact acknowledgement pulse, `PIKA-MF-025` Autonomous bilateral forelimb-open body pulse, `PIKA-MF-027` Autonomous drowsy lateral sway with eyelid/mouth cycling, `PIKA-MF-029` Prolonged closed-eye rest / doze moving hold, `PIKA-MF-032` Autonomous self-touch / pondering lateral tilt, `PIKA-MF-038` Closed-eye content afterglow / low-motion settle, `PIKA-MF-039` Half-lidded / droopy facial recovery settle, `PIKA-MF-040` General active-pose return-to-neutral settle / recovery

## 30. Unique-to-Video Families

### Video 1 only

`PIKA-MF-005` Ear orientation micro-correction, `PIKA-MF-023` Two-forelimb lift + head-dip stern sequence, `PIKA-MF-026` Autonomous closed-eye side-lean hold

### Video 2 only

`PIKA-MF-013` Interaction-linked open-mouth lateral body sway, `PIKA-MF-016` Compression → open-arm negative hero reaction, `PIKA-MF-017` Rear/side eyes-closed disengaged moving hold, `PIKA-MF-018` Rear-contact glance-back warning and turn-away, `PIKA-MF-019` Side/back → front reorientation

### Video 3 only

`PIKA-MF-030` Autonomous head/neck arc-sway, `PIKA-MF-031` Autonomous turn-and-bow-like compression gesture, `PIKA-MF-042` Visible screen-relative character entry / exit transition

### Video 4 only

`PIKA-MF-010` Two-paw cheek press / face-mug sequence, `PIKA-MF-028` Autonomous clasped-paw side-to-side bow/sway, `PIKA-MF-033` Touch-interrupted doze → wake/startle expansion → recovery, `PIKA-MF-045` Closed-eye gathered-paw head/torso lower-and-lean, `PIKA-MF-047` Tail-region contact → local tail displacement/sweep with body lean

### Video 5 only

`PIKA-MF-003` Expression-linked eyelid close / half-lid / reopen transition, `PIKA-MF-043` Close-up entry head-dip / smile-open-mouth expression sequence, `PIKA-MF-046` Brief closed-eye open-mouth smile pulse from neutral

### Video 6 only

`PIKA-MF-008` Touch-positive closed-eye head-lower content bow, `PIKA-MF-011` Bilateral cheek-level ecstatic stretch / head-back expansion, `PIKA-MF-044` Foreground close-pass → close-up content hold

> `single-video` is a corpus-frequency label only; it is not an importance judgment.

## 31. Implementation-Relevant Classification

| Family | Scale | Spatial Scope | Grounding | Temporal Form | Primary Driver | Front View |
| --- | --- | --- | --- | --- | --- | --- |
| PIKA-MF-001 | MICRO | FULL_BODY | PLANTED or crop-unknown | moving_hold / hold | state / no fixed lead | HIGH |
| PIKA-MF-002 | MICRO | LOCAL | PLANTED / quiet | pulse | eyelids | HIGH |
| PIKA-MF-003 | MICRO | LOCAL | parent-dependent | pulse / transition | eyelids | HIGH |
| PIKA-MF-004 | MICRO–SMALL | LOCAL | PLANTED | moving_hold / loop-like / pulse | tail | MEDIUM |
| PIKA-MF-005 | MICRO | LOCAL | PLANTED | pulse / moving_hold | ears | HIGH |
| PIKA-MF-006 | SMALL | REGIONAL | PLANTED or crop-unknown | hold / moving_hold | face / eyelids | HIGH |
| PIKA-MF-007 | SMALL–MEDIUM | REGIONAL | PLANTED mostly | anticipation_action_settle / pulse | face / eyelids / mouth | HIGH |
| PIKA-MF-008 | MEDIUM | REGIONAL | PLANTED | anticipation_action_settle | head / eyelids | HIGH |
| PIKA-MF-009 | MEDIUM | FULL_BODY | PLANTED | sequence / anticipation_action_settle | head / face | HIGH |
| PIKA-MF-010 | MEDIUM | REGIONAL | PLANTED | sequence | forelimbs / paws | HIGH |
| PIKA-MF-011 | LARGE | FULL_BODY | PLANTED | anticipation_action_settle | forelimbs + face | HIGH |
| PIKA-MF-012 | SMALL | LOCAL | PLANTED or crop-unknown | pulse / short sequence | one forelimb / paw | HIGH |
| PIKA-MF-013 | MEDIUM | FULL_BODY | PLANTED | sequence | head/torso/root | HIGH |
| PIKA-MF-014 | SMALL–MEDIUM | REGIONAL | PLANTED or crop-unknown | hold / pulse / sequence | face / mouth / eyelids | HIGH |
| PIKA-MF-015 | MEDIUM | FULL_BODY | PLANTED | anticipation_action_settle | face → head/upper torso | HIGH |
| PIKA-MF-016 | LARGE | FULL_BODY | PLANTED / support exactness unclear | anticipation_action_hold | forelimbs + torso | HIGH |
| PIKA-MF-017 | SMALL | FULL_BODY | PLANTED | moving_hold | none dominant | LOW |
| PIKA-MF-018 | SMALL | REGIONAL | PLANTED | sequence | head / eyes | LOW |
| PIKA-MF-019 | MEDIUM | FULL_BODY | TURN / support sequence partly unclear | single_transition | root/torso + head | MEDIUM |
| PIKA-MF-020 | SMALL–MEDIUM | REGIONAL | PLANTED or crop-unknown | moving_hold / sequence | eyes/head | MEDIUM |
| PIKA-MF-021 | MEDIUM | REGIONAL | crop-unknown / grounded | prepare→present→WAIT→contact/completion | forelimb/paw | HIGH |
| PIKA-MF-022 | SMALL | LOCAL | crop-unknown / grounded | contact→ack→hold/retract→settle | contact locus / paw → face | HIGH |
| PIKA-MF-023 | MEDIUM | REGIONAL | PLANTED | sequence | forelimbs + head | HIGH |
| PIKA-MF-024 | LARGE | FULL_BODY | PLANTED to possible SUPPORT_CHANGE depending variant | anticipation_action_settle | face/torso/forelimbs or root/COM | HIGH |
| PIKA-MF-025 | MEDIUM | FULL_BODY | PLANTED / support unclear in crop | pulse / anticipation_action_settle | forelimbs + face | HIGH |
| PIKA-MF-026 | SMALL–MEDIUM | REGIONAL | PLANTED / seated | moving_hold | head/torso | MEDIUM |
| PIKA-MF-027 | MEDIUM | FULL_BODY | PLANTED | sequence / moving_hold | eyelids/mouth → head | HIGH |
| PIKA-MF-028 | MEDIUM | FULL_BODY | PLANTED | sequence | head/torso | HIGH |
| PIKA-MF-029 | SMALL | FULL_BODY | PLANTED / seated | moving_hold | eyelids/head | HIGH |
| PIKA-MF-030 | MEDIUM | REGIONAL | grounding quiet | sequence | head/neck | HIGH |
| PIKA-MF-031 | MEDIUM | FULL_BODY | PLANTED | sequence | head/torso | MEDIUM |
| PIKA-MF-032 | MEDIUM | FULL_BODY | PLANTED | sequence | face/head → forelimb | HIGH |
| PIKA-MF-033 | LARGE | FULL_BODY | PLANTED | state_interrupt→action→recovery | face/head → full body | HIGH |
| PIKA-MF-034 | SMALL | REGIONAL | PLANTED or crop-unknown | approach→hold→disappearance/pause | external item + head/mouth attention | MEDIUM |
| PIKA-MF-035 | MEDIUM | REGIONAL | PLANTED / crop-unknown | pulse / anticipation_action_settle | face | HIGH |
| PIKA-MF-036 | SMALL–MEDIUM | REGIONAL | PLANTED | hold / moving_hold | forelimbs/item posture | MEDIUM |
| PIKA-MF-037 | MEDIUM | REGIONAL | PLANTED | sequence | face + forelimbs | HIGH |
| PIKA-MF-038 | SMALL | LOCAL | PLANTED / crop-unknown | moving_hold / settle | eyelids/face | HIGH |
| PIKA-MF-039 | SMALL | LOCAL | PLANTED | hold / settle | face/eyelids | HIGH |
| PIKA-MF-040 | SMALL–MEDIUM | FULL_BODY | returns PLANTED | single_transition / settle | varies | HIGH |
| PIKA-MF-041 | MICRO | FULL_BODY | — | single_transition | UI / screen state | LOW |
| PIKA-MF-042 | LARGE | FULL_BODY | UNCLEAR | single_transition | screen-relative full body | MEDIUM |
| PIKA-MF-043 | MEDIUM | REGIONAL | off-frame | state_entry→peak→settle | eyelids/face → head | HIGH |
| PIKA-MF-044 | LARGE | FULL_BODY | UNCLEAR | sequence / moving_hold | full-body/root screen-relative | MEDIUM |
| PIKA-MF-045 | MEDIUM | FULL_BODY | PLANTED / WEIGHT_SHIFT | sequence | head/upper torso | HIGH |
| PIKA-MF-046 | SMALL | REGIONAL | PLANTED | pulse | face | HIGH |
| PIKA-MF-047 | MEDIUM | REGIONAL | PLANTED | sequence | tail / tail+torso | MEDIUM |

## 32. Quantitative Master Summary

| Metric | Value |
| --- | --- |
| Total Master Motion Families | 47 |
| Total normalized Master Variant clusters | 103 |
| Total source-local Family candidates mapped | 98 |
| Families observed in 1 / 2 / 3 / 4 / 5 / 6 videos | 22 / 13 / 4 / 3 / 3 / 2 |
| Autonomous-capable Families (initiation field contains AUTONOMOUS) | 11 |
| Interaction/social-triggered Families | 26 |
| Primary intentional-stillness Families | 2 |
| Primary large/hero Families | 4 |
| Primary forelimb-dominant Families | 2 |
| Tail-primary / tail-micro primary Families | 3 |
| Front-view HIGH / MEDIUM / LOW | 34 / 10 / 3 |
| Unresolved direct source conflicts | 0 |
| Source-bound ambiguities retained | 9 |

**Occurrence aggregation rule:** a single global exact occurrence total is **not claimed**. The six source inventories mix exact counts, lower bounds (`≥N`, `at least N`), recurrent/unbounded micro-motion, parent sequences, child phases, and overlapping channel-specific events. Family-level source counts are preserved verbatim in §4/§5 instead of converting heterogeneous evidence into a false exact total.

## 33. Conflict / Ambiguity Ledger

| Topic | Source A | Source B | Master treatment | Confidence |
| --- | --- | --- | --- | --- |
| Physiological blink vs expression closure | V1/F01, V2/F02, V3/PF-03 confirm isolated blinks | V5/F15 explicitly says expression-linked closure and physiological identity unconfirmed | Kept as PIKA-MF-002 vs PIKA-MF-003 | HIGH |
| Positive touch family breadth | V1 separates sustained content hold F03 from completion burst F04 | V2/V3/V4/V5/V6 often package face response phases differently | Master separates sustained hold PIKA-MF-006, pulse/cycle PIKA-MF-007, and full-body hero PIKA-MF-024 | HIGH |
| Large delight support change | V1/F08 and V2/F04 contain uncertain/probable support change | V4/MF-10 and V6/F06 show planted support in their variants | Retained as variant-specific grounding, not one universal support rule | HIGH |
| Tail role during positive touch | Some sources show amplifier/follow-through | Others show quiet tail or crop-unobservable tail | Tail role retained per variant/source; no universal happy-tail rule inferred | HIGH |
| V3 PF-04 broad family | PF-04 contains small face responses and a wide full-body response | Other videos separate those mechanics into different local families | Split PF-04 across PIKA-MF-007 and PIKA-MF-024 with traceability retained | HIGH |
| V3 feeding family breadth | PF-09 includes approach, disappearance and post-food delight | Other inventories split hold vs completion reaction | Split PF-09 across PIKA-MF-034 and PIKA-MF-035 | HIGH |
| V3 gift family breadth | PF-10 combines hold/presentation and release/joy | Other inventories split hold and completion | Split PF-10 across PIKA-MF-036 and PIKA-MF-037 | HIGH |
| System-transition front-view rating | V3 visible entry can be HIGH while black/menu is LOW; V4 catalog keeps transition family with HIGH metadata; V6 system transition is LOW | Character-visible transition PIKA-MF-042 is separated from body-unreliable system/UI PIKA-MF-041 | MEDIUM |
| Anatomical left/right | Multiple sources explicitly avoid anatomical side claims in front-facing/occluded views | Some source variants use screen-left/screen-right only | Master preserves screen-relative wording and does not convert to anatomical side | HIGH |

**Unresolved direct conflict count: 0.** The ledger above contains retained taxonomy/evidence ambiguities, not contradictions requiring one source to be declared wrong.

## 34. Unresolved / Unconfirmed

- Exact shared animation-clip identity across videos: **unconfirmed / not inferred**.
- Anatomical L/R where sources only support screen-relative side: **unconfirmed**.
- Exact support change / airborne frames for some large hero variants: **source V2/U qualifiers retained**.
- Bite / chew / swallow mechanics in feeding: **unconfirmed**; item disappearance is not anatomical proof.
- Transfer recipient/mechanism for gift/item disappearance: **unconfirmed**.
- Whether some no-contact visible phrases are autonomous vs system-triggered: **unconfirmed** where source says UNKNOWN.
- Breathing periodicity as a clean physiological cycle: **not established across this corpus**.
- Physiological identity of V5 expression-linked eyelid transitions: **unconfirmed**; kept separate from isolated blink.

## 35. Final Compact Master Inventory

| Global ID | Master Family | Primary Category | Coverage | Variants | Initiation | Front View |
| --- | --- | --- | --- | --- | --- | --- |
| PIKA-MF-001 | Neutral attentive intentional-stillness / low-motion moving hold | O. Intentional stillness | 6/6 | 6 | AUTONOMOUS / SYSTEM / UNKNOWN | HIGH |
| PIKA-MF-002 | Spontaneous isolated blink | A. Living / physiological | 3/6 | 3 | AUTONOMOUS | HIGH |
| PIKA-MF-003 | Expression-linked eyelid close / half-lid / reopen transition | Q. Other | 1/6 | 1 | BOTH / UNKNOWN | HIGH |
| PIKA-MF-004 | Independent tail ambient micro / sweep / oscillation | C. Ear / tail micro | 3/6 | 3 | AUTONOMOUS / BOTH | MEDIUM |
| PIKA-MF-005 | Ear orientation micro-correction | C. Ear / tail micro | 1/6 | 1 | BOTH | HIGH |
| PIKA-MF-006 | Sustained positive-contact content hold / soften | H. Positive touch | 2/6 | 2 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-007 | Positive-touch facial response pulse / delight completion cycle | H. Positive touch | 6/6 | 8 | PLAYER_TRIGGERED / AFTERGLOW | HIGH |
| PIKA-MF-008 | Touch-positive closed-eye head-lower content bow | D. Posture / balance / COM | 1/6 | 1 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-009 | Deep lateral positive-content lean with ear rotation | D. Posture / balance / COM | 2/6 | 2 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-010 | Two-paw cheek press / face-mug sequence | E. Forelimb / hand-like gesture | 1/6 | 1 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-011 | Bilateral cheek-level ecstatic stretch / head-back expansion | M. Large emotional / hero | 1/6 | 1 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-012 | One-forelimb local acknowledgement / raise | E. Forelimb / hand-like gesture | 4/6 | 4 | PLAYER_TRIGGERED / UNCERTAIN | HIGH |
| PIKA-MF-013 | Interaction-linked open-mouth lateral body sway | H. Positive touch | 1/6 | 1 | PLAYER_TRIGGERED / interaction-linked | HIGH |
| PIKA-MF-014 | Contact-linked facial sensitivity / displeased warning state | I. Negative / boundary touch | 3/6 | 3 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-015 | Boundary upper-body recoil / compression / withdrawal | I. Negative / boundary touch | 2/6 | 2 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-016 | Compression → open-arm negative hero reaction | I. Negative / boundary touch | 1/6 | 1 | PLAYER_TRIGGERED | HIGH |
| PIKA-MF-017 | Rear/side eyes-closed disengaged moving hold | O. Intentional stillness | 1/6 | 1 | PLAYER_TRIGGERED state | LOW |
| PIKA-MF-018 | Rear-contact glance-back warning and turn-away | I. Negative / boundary touch | 1/6 | 1 | PLAYER_TRIGGERED | LOW |
| PIKA-MF-019 | Side/back → front reorientation | P. Transition | 1/6 | 1 | PLAYER_TRIGGERED / TRANSITION | MEDIUM |
| PIKA-MF-020 | Attention / gaze / head tracking-turn | B. Attention / gaze | 2/6 | 2 | PLAYER_TRIGGERED / visual association | MEDIUM |
| PIKA-MF-021 | One-paw social offer and moving WAIT | J. Reciprocal social interaction | 2/6 | 2 | CHARACTER_INITIATED_SOCIAL / RECIPROCAL | HIGH |
| PIKA-MF-022 | Presented-paw contact acknowledgement pulse | J. Reciprocal social interaction | 2/6 | 2 | RECIPROCAL | HIGH |
| PIKA-MF-023 | Two-forelimb lift + head-dip stern sequence | I. Negative / boundary touch | 1/6 | 1 | BOTH | HIGH |
| PIKA-MF-024 | Large positive bilateral open-arm whole-body delight | M. Large emotional / hero | 5/6 | 5 | PLAYER_TRIGGERED / SYSTEM-UNKNOWN | HIGH |
| PIKA-MF-025 | Autonomous bilateral forelimb-open body pulse | F. Autonomous idle | 2/6 | 2 | AUTONOMOUS / UNKNOWN | HIGH |
| PIKA-MF-026 | Autonomous closed-eye side-lean hold | F. Autonomous idle | 1/6 | 1 | AUTONOMOUS | MEDIUM |
| PIKA-MF-027 | Autonomous drowsy lateral sway with eyelid/mouth cycling | F. Autonomous idle | 2/6 | 2 | AUTONOMOUS | HIGH |
| PIKA-MF-028 | Autonomous clasped-paw side-to-side bow/sway | F. Autonomous idle | 1/6 | 1 | AUTONOMOUS | HIGH |
| PIKA-MF-029 | Prolonged closed-eye rest / doze moving hold | A. Living / physiological | 2/6 | 2 | AUTONOMOUS | HIGH |
| PIKA-MF-030 | Autonomous head/neck arc-sway | F. Autonomous idle | 1/6 | 1 | AUTONOMOUS / AFTERGLOW UNCERTAIN | HIGH |
| PIKA-MF-031 | Autonomous turn-and-bow-like compression gesture | F. Autonomous idle | 1/6 | 1 | AUTONOMOUS / CHARACTER_INITIATED_SOCIAL UNCERTAIN | MEDIUM |
| PIKA-MF-032 | Autonomous self-touch / pondering lateral tilt | F. Autonomous idle | 2/6 | 2 | AUTONOMOUS / visual context | HIGH |
| PIKA-MF-033 | Touch-interrupted doze → wake/startle expansion → recovery | J. Reciprocal social interaction | 1/6 | 1 | PLAYER_TRIGGERED / RECIPROCAL | HIGH |
| PIKA-MF-034 | Feeding orient / mouth-contact hold / item-disappearance transition | K. Feeding | 5/6 | 5 | PLAYER_TRIGGERED / SYSTEM | MEDIUM |
| PIKA-MF-035 | Feeding-completion positive delight | K. Feeding | 5/6 | 5 | PLAYER_TRIGGERED / feeding consequence | HIGH |
| PIKA-MF-036 | Bilateral gift/item presentation moving hold | L. Gift / item | 4/6 | 4 | SYSTEM / CHARACTER_INITIATED_SOCIAL / UNKNOWN | MEDIUM |
| PIKA-MF-037 | Gift/item release / forelimb opening / positive completion | L. Gift / item | 4/6 | 4 | SYSTEM / CHARACTER_INITIATED_SOCIAL / UNKNOWN | HIGH |
| PIKA-MF-038 | Closed-eye content afterglow / low-motion settle | N. Recovery / settle / afterglow | 2/6 | 2 | RECIPROCAL / PLAYER_TRIGGERED / SYSTEM-UNKNOWN | HIGH |
| PIKA-MF-039 | Half-lidded / droopy facial recovery settle | N. Recovery / settle / afterglow | 2/6 | 3 | AFTERGLOW / UNKNOWN | HIGH |
| PIKA-MF-040 | General active-pose return-to-neutral settle / recovery | N. Recovery / settle / afterglow | 2/6 | 2 | BOTH / SYSTEM | HIGH |
| PIKA-MF-041 | System/UI/menu/item-mode transition without reliable body motion | P. Transition | 3/6 | 4 | SYSTEM | LOW |
| PIKA-MF-042 | Visible screen-relative character entry / exit transition | P. Transition | 1/6 | 1 | SYSTEM / TRANSITION | MEDIUM |
| PIKA-MF-043 | Close-up entry head-dip / smile-open-mouth expression sequence | M. Large emotional / hero | 1/6 | 1 | SYSTEM / UNKNOWN | HIGH |
| PIKA-MF-044 | Foreground close-pass → close-up content hold | M. Large emotional / hero | 1/6 | 1 | SYSTEM / UNKNOWN | MEDIUM |
| PIKA-MF-045 | Closed-eye gathered-paw head/torso lower-and-lean | D. Posture / balance / COM | 1/6 | 1 | BOTH / UNKNOWN | HIGH |
| PIKA-MF-046 | Brief closed-eye open-mouth smile pulse from neutral | F. Autonomous idle | 1/6 | 1 | UNKNOWN / autonomous-looking | HIGH |
| PIKA-MF-047 | Tail-region contact → local tail displacement/sweep with body lean | C. Ear / tail micro | 1/6 | 1 | PLAYER_TRIGGERED | MEDIUM |

## 36. Coverage / Traceability Audit

### Source Family → Master Family mapping

| Video | Source Family | Source Name | Master Family(s) | Source Variants | Source Occurrences |
| --- | --- | --- | --- | --- | --- |
| V1 | F01 | isolated blink / close–reopen | PIKA-MF-002 | clean idle blink | ≥1 clean |
| V1 | F02 | seated neutral moving hold | PIKA-MF-001 | closed-eye opening; open-eye neutral | 10 macro segments |
| V1 | F03 | touch-induced content hold | PIKA-MF-006 | head/chest/side/extended rub | ≥29 cycles |
| V1 | F04 | touch-induced delight completion burst | PIKA-MF-007 | standard, extended, hero precursor, phase-B | **29** |
| V1 | F05 | boundary compression / withdrawal | PIKA-MF-015 | upper-face press; similar later bow | 2 |
| V1 | F06 | two-forelimb lift + head-dip stern sequence | PIKA-MF-023 | triggered; autonomous repeat | 3 |
| V1 | F07 | head/ear-side attention turn | PIKA-MF-020 | one-forelimb; tail-sweep extended | 6 macro |
| V1 | F08 | full-body open-arm upright delight | PIKA-MF-024 | single observed strong variant | 1 |
| V1 | F09 | feeding mouth-contact acceptance hold | PIKA-MF-034 | feed #1/#2 | 2 |
| V1 | F10 | post-feed delight burst | PIKA-MF-035 | feed #1/#2 | 2 |
| V1 | F11 | autonomous closed-eye side lean | PIKA-MF-026 | single | 1 |
| V1 | F12 | long closed-eye open-mouth slow sway hold | PIKA-MF-029 | single long | 1 |
| V1 | F13 | autonomous open-arm burst | PIKA-MF-025 | single | 1 |
| V1 | F14 | tail micro-reposition / sway | PIKA-MF-004 | idle micro; reaction follow-through | ≥4 clean idle repositions |
| V1 | F15 | ear orientation micro-correction | PIKA-MF-005 | idle micro; flatten/spread in reactions | recurrent |
| V1 | F16 | settle / recovery to neutral | PIKA-MF-040 | fast reset; gradual settle | recurrent |
| V2 | F01 | Planted neutral / quiet moving hold | PIKA-MF-001 | 7 segmented contexts | 7 |
| V2 | F02 | Isolated blink | PIKA-MF-002 | 1 observed variant | ≥2 |
| V2 | F03 | Independent broad tail sweep | PIKA-MF-004 | 2 segmented contexts | 2 intervals |
| V2 | F04 | Crouch/expand open-arm full-body delight | PIKA-MF-024 | 3 | 3 |
| V2 | F05 | Closed-eye/open-mouth positive touch response | PIKA-MF-007 | ≥9 named variants | 11 |
| V2 | F06 | Narrow-eye/downturned-mouth displeased frontal hold | PIKA-MF-014 | 7 named states | 8 intervals |
| V2 | F07 | Closed-eye upper-body recoil/compression | PIKA-MF-015 | 2 structural variants | 3 |
| V2 | F08 | Compression→open-arm negative hero reaction | PIKA-MF-016 | 1 | 1 |
| V2 | F09 | Rear/side eyes-closed disengaged moving hold | PIKA-MF-017 | 3 segmented | 3 |
| V2 | F10 | Rear-contact glance-back warning | PIKA-MF-018 | 2 | 2 |
| V2 | F11 | Side/back→front reorientation | PIKA-MF-019 | 1 | 1 |
| V2 | F12 | One-forelimb lift/forward arc + lean | PIKA-MF-012 | 2 | 2 |
| V2 | F13 | Open-mouth lateral body sway during visible interaction | PIKA-MF-013 | 1 | 1 |
| V2 | F14 | Autonomous closed-eye lateral sway with mouth shaping | PIKA-MF-027 | 1 | 1 |
| V2 | F15 | Active-pose return-to-neutral settle/recovery | PIKA-MF-040 | multiple | 9 child phases |
| V3 | PF-01 | screen-relative entry / exit / scene transition | PIKA-MF-042, PIKA-MF-041 | entry-rise+eye-open; exit-dip; black/menu/loading transition | 2 macro occurrences |
| V3 | PF-02 | neutral attentive moving hold / intentional stillness | PIKA-MF-001 | close-up neutral hold; wide standing hold; UI-occluded hold | 7 |
| V3 | PF-03 | spontaneous blink | PIKA-MF-002 | full blink; partial blink not independently confirmed | 2 confirmed isolated spontaneous blinks |
| V3 | PF-04 | positive interaction response — face-led smile / eye-close / body delight | PIKA-MF-007, PIKA-MF-024 | A small face-led acknowledge; B large closed-eye open-mouth delight; C prolonged closed-eye content hold; D wide-view full-body compression/expansion | 22 episodes including non-touch afterglow variants; 19 are touch-linked response episodes |
| V3 | PF-05 | one-paw social offer-and-wait | PIKA-MF-021 | screen-right paw; screen-left paw; longer repeated-contact hold | 3 offers within parent O006 |
| V3 | PF-06 | paw-contact acknowledgement pulse | PIKA-MF-022 | round-mouth recoil; closed-eye smile acknowledgement | 2 grouped acknowledgement episodes; multiple contact pulses inside O006b are not exact-counted |
| V3 | PF-07 | autonomous head/neck arc-sway | PIKA-MF-030 | single observed variant | 1 |
| V3 | PF-08 | half-lidded mouth-down facial settle | PIKA-MF-039 | short half-lid; half-lid plus head tilt | at least 10 clearly sampled appearances |
| V3 | PF-09 | food approach / mouth presentation / consume-like event | PIKA-MF-034, PIKA-MF-035 | single observed food object event | 1 macro feeding sequence |
| V3 | PF-10 | two-paw item/gift hold, presentation, and release | PIKA-MF-036, PIKA-MF-037 | presentation hold; release/joy child phase | 1 macro item sequence with 2 phases |
| V3 | PF-11 | short one-paw touch acknowledgement / forelimb adjustment | PIKA-MF-012 | forward acknowledgement; lower local paw adjustment | 2 |
| V3 | PF-12 | autonomous turn-and-bow-like compression gesture | PIKA-MF-031 | single observed variant | 1 |
| V4 | MF-01 | Neutral forward intentional-stillness / low-motion hold | PIKA-MF-001 | short post-recovery hold; long neutral hold | 9 |
| V4 | MF-02 | Closed-eye gathered-paw head/torso lower-and-lean | PIKA-MF-045 | entry bow; touch-associated lean; broad side lean; brief posture correction | 9 |
| V4 | MF-03 | Single-forelimb raise / acknowledgement adjustment | PIKA-MF-012 | face-side raise; open-mouth raise; stronger bilateral-adjacent preparation | 5 |
| V4 | MF-04 | Contact-evoked closed-eye/open-mouth smile response cycle | PIKA-MF-007 | closed-eye smile; open-mouth delight; narrowed-release; low-amplitude head dip | 18 |
| V4 | MF-05 | Two-paw cheek press / face-mug sequence | PIKA-MF-010 | closed-eye-first; open-mouth peak; narrowed-face middle; amplitude differences | 6 |
| V4 | MF-06 | Head/ear-region touch → lateral lean/open-mouth response | PIKA-MF-009 | single observed clear variant | 1 |
| V4 | MF-07 | Tail-region contact → tail displacement/sweep with body lean | PIKA-MF-047 | sweep-dominant; lean-dominant; tail response into smile/VFX | 3 |
| V4 | MF-08 | Upper-head/hat pat → closed-eye smile cycle | PIKA-MF-007 | small closed-eye smile; open-mouth smile; amplitude/timing differences | 11 |
| V4 | MF-09 | Contact-linked narrowed/squeezed facial compression transient | PIKA-MF-014 | brief narrowed-eye; stronger squeezed/downturned mouth; mixed lean variant | 3 |
| V4 | MF-10 | Large bilateral-arm whole-body delight expansion | PIKA-MF-024 | single clear occurrence | 1 |
| V4 | MF-11 | Feeding mouth-contact hold + item-disappearance consume transition | PIKA-MF-034 | one observed sequence | 1 |
| V4 | MF-12 | Post-feed closed-eye open-mouth delight | PIKA-MF-035 | single observed sequence | 1 |
| V4 | MF-13 | Autonomous closed-eye clasped-paw side-to-side bow/sway | PIKA-MF-028 | two visually highly similar occurrences | 2 |
| V4 | MF-14 | Autonomous drowsy lateral sway with eyelid/mouth cycling | PIKA-MF-027 | 219–223.75; 302.5–306.0 with small timing/amplitude differences | 2 |
| V4 | MF-15 | Autonomous one-paw chin/cheek self-touch with head tilt | PIKA-MF-032 | single clear occurrence | 1 |
| V4 | MF-16 | Autonomous eyes-closed doze moving hold | PIKA-MF-029 | single clear long hold | 1 |
| V4 | MF-17 | Touch-interrupted doze → wake/startle expansion → recovery | PIKA-MF-033 | single clear occurrence | 1 |
| V4 | MF-18 | Two-paw item presentation moving hold | PIKA-MF-036 | neutral-face hold; closed-eye smile hold | 1 |
| V4 | MF-19 | Item disappearance → empty-paw smile and settle | PIKA-MF-037 | single observed sequence | 1 |
| V4 | MF-20 | System/menu transition and visibility interruption | PIKA-MF-041 | hard-cut/menu interval; large UI occlusion interval | 2 |
| V5 | F01 | Closed-eye head-dip / smile-open-mouth entry expression sequence | PIKA-MF-043 | 1 | 1 |
| V5 | F02 | Forehead/top-head contact positive facial pulse | PIKA-MF-007 | 5 | 5 |
| V5 | F03 | One-paw presentation and moving WAIT | PIKA-MF-021 | 2 | 2 |
| V5 | F04 | Presented-paw contact acknowledgement | PIKA-MF-022 | 4 | 4 |
| V5 | F05 | Lower-face/upper-torso positive touch facial pulse | PIKA-MF-007 | ≥7 visible variants/pulses | 7 |
| V5 | F06 | Muzzle/cheek/chin sensitivity response with ear flatten/head-away | PIKA-MF-014 | 4 | 4 |
| V5 | F07 | Pointer-led gaze/head tracking | PIKA-MF-020 | 2 | 2 |
| V5 | F08 | Closed-eye content afterglow / settle | PIKA-MF-038 | 3 | 3 |
| V5 | F09 | Food-at-muzzle orient/attend hold | PIKA-MF-034 | 1 | 1 |
| V5 | F10 | Post-item disappearance positive food response | PIKA-MF-035 | 1 | 1 |
| V5 | F11 | Two-forelimb bouquet/item presentation hold | PIKA-MF-036 | 1 | 1 |
| V5 | F12 | Item-presentation completion/release with forelimb opening | PIKA-MF-037 | 1 | 1 |
| V5 | F13 | Neutral moving hold / low-amplitude idle | PIKA-MF-001 | multiple contextual variants | 9 windows |
| V5 | F14 | Autonomous two-forelimb outward/open body pulse | PIKA-MF-025 | 1 | 1 |
| V5 | F15 | Expression-linked eyelid closure/reopen micro-transition | PIKA-MF-003 | full close, half-lid, reopen | ≥20 embedded transitions |
| V5 | F16 | Brief closed-eye open-mouth smile pulse from neutral | PIKA-MF-046 | 1 | 1 |
| V5 | F17 | Autonomous tail oscillation with low-amplitude full-body idle | PIKA-MF-004 | continuous | 2 long windows |
| V6 | F01 | Foreground close-pass → close-up content hold | PIKA-MF-044 | 1 | 1 |
| V6 | F02 | Neutral front-facing planted hold / stillness | PIKA-MF-001 | 2+ | 4 macro + many short resets |
| V6 | F03 | Touch-positive closed-eye/open-mouth smile | PIKA-MF-007 | 4+ | at least 11 clear macro cycles |
| V6 | F04 | Forehead-stroke content soften | PIKA-MF-006 | 2 | 3+ |
| V6 | F05 | Closed-eye head-lower content bow | PIKA-MF-008 | 2 | at least 2 |
| V6 | F06 | Bilateral forelimb-open whole-body delight | PIKA-MF-024 | 1 | 1 |
| V6 | F07 | One-forelimb acknowledgement | PIKA-MF-012 | 1+ | at least 3 lifts |
| V6 | F08 | Deep lateral content lean + ear rotation | PIKA-MF-009 | 2 | 2 |
| V6 | F09 | Bilateral cheek-level ecstatic stretch | PIKA-MF-011 | 1 | 1 |
| V6 | F10 | Half-lidded/droopy recovery | PIKA-MF-039 | 1+ | at least 5 likely |
| V6 | F11 | Item-mode / food-selection transition | PIKA-MF-041 | 1 | 1 |
| V6 | F12 | Feeding orient-and-hold / processing pause | PIKA-MF-034 | 2 | 2 |
| V6 | F13 | Feeding-completion positive delight | PIKA-MF-035 | 1 | 2 |
| V6 | F14 | System/UI transition | PIKA-MF-041 | 2 | 2 |
| V6 | F15 | Bilateral gift/item presentation hold | PIKA-MF-036 | 1 | 1 |
| V6 | F16 | Gift release into open-arm joy | PIKA-MF-037 | 1 | 1 |
| V6 | F17 | Post-gift positive afterglow → droopy settle | PIKA-MF-038, PIKA-MF-039 | 1 | 1 |
| V6 | F18 | Autonomous pondering/concern lateral tilt + self-hold | PIKA-MF-032 | 1 | 1 |

### Audit checklist

- [x] Video 1の全source Familyを回収 — 16/16
- [x] Video 2の全source Familyを回収 — 15/15
- [x] Video 3の全source Familyを回収 — 12/12
- [x] Video 4の全source Familyを回収 — 20/20
- [x] Video 5の全source Familyを回収 — 17/17
- [x] Video 6の全source Familyを回収 — 18/18
- [x] source Occurrenceはsource Family / Master Variantから逆引き可能
- [x] duplicate exportを別動画として二重計上していない
- [x] V4の同一内容duplicate exportsを1 source videoとして扱った
- [x] parent/child occurrenceをMasterの単一global exact totalへ不正に二重countしていない
- [x] VFX/audio/UIをbody MotionとしてFamily化していない（system transition metadataは別扱い）
- [x] source uncertaintyを勝手に確定化していない
- [x] LOW front-view Familyを削除していない
- [x] single-video Familyを削除していない
- [x] broad local Familiesのphase splitはsource内の明示phase/variantに限定

**Master Coverage Confidence: HIGH**

Reason: all **98 / 98** source-local Family candidates from the six formal inventories map to at least one Master Family; all six videos are represented; duplicate exports are excluded; evidence uncertainty and non-additive occurrence semantics are retained rather than normalized away.

---

**Boundary:** This Master is a normalized observation reference for the six Partner Pikachu inventories only. It does not decide Carol/Grimo adoption, motion counts, rig design, Blender clips, PlayCanvas implementation, or comparisons with Partner Eevee.
