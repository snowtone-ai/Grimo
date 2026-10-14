# CAROL_NORMAL_SEMANTIC_RECONSTRUCTION_SPEC.md

**Status:** HUMAN-CONFIRMED SEMANTIC SPEC — NUMERIC POLICY REVALIDATED; READY FOR CODEX IMPLEMENTATION PLANNING
**Date:** 2026-10-02
**Scope:** Carol Normal/Fleece semantic reconstruction around the frozen Skin v004 working baseline

---

## 0. Production boundary and authority

This document defines **what Carol's visible 3D form means**. It does not prescribe topology, modifiers, mesh decomposition, or a Blender implementation recipe.

Verified working baseline at the start of this semantic-reconstruction session:

- Repository: `snowtone-ai/Grimo`
- Branch: `codex/carol-skin-default-v004`
- Verified HEAD: `e77b8ef53df7a6dfe6a6c6f47f24b8d0d11d7d8e`
- Working Skin: `assets/grimo/production/carol/blender/carol-skin-default-v004.blend`
- Working Skin SHA256: `c14f15e35af18e17a63506ea1f4c8ec0f69cb4f52882d27cfa22cb01db7e1f7d`
- Skin baseline decision: **freeze Skin v004 for this phase**. Do not reopen Skin-only ear repair here.

Visible-authority priority for this work:

1. `carol-identity-canonical.png` — highest authority for Carol-ness, softness, dream/cloud feeling, overall visual character, and the intended impression of the fleece.
2. Approved `carol_front.png` — highest measurable authority for the final visible Front proportions and outline.
3. Approved `carol_side.png` — highest measurable authority for the final visible Side proportions, front/back flow, and outline.
4. Human semantic decisions collected in this session — authority for what the 2D images mean in unseen 3D, **but any numbers spoken conversationally by Human are qualitative size examples unless Human explicitly declares them locked measurements**.
5. Approved Skin Front / Skin Side — supporting inner-body structure only; Skin does not override the final Normal exterior.
6. `CAROL_GEOMETRY_PARAMETERS.md` — supporting cross-check. Its numeric values must not override a visible mismatch with Identity / approved Normal Front / approved Normal Side.
7. Previous Fleece attempts — **failure evidence only**, never shape authority.

### Numeric-authority rule

Human used approximate numbers during the interview only to communicate relative size feeling. Values such as `1.0`, `0.8–0.9`, `1.25`, `1.5×`, or similar conversational estimates are **not production dimensions, not ratio locks, and not acceptance thresholds**.

When production numbers are needed, derive them from the approved authority images:

- use **Identity** to judge whether the measured result still feels like Carol;
- use **Normal Front / Normal Side** for measurable visible proportions;
- use Human answers to decide semantic relationships that the images cannot directly show;
- use Skin only as the inner structural reference;
- use old parameter numbers only as a sanity check.

If a numeric value and the visible authority disagree, **the visible authority wins**.

Mareep or any other finished character may be used only as a **comparison lesson for solving general 2D→3D problems**. Never copy its geometry, proportions, texture, bones, or character-specific structure into Carol.

---

# 1. Carol全体の一言説明

Carol is a **small, low, compact animal whose body is wrapped in an extremely thick, dream-cloud-like fleece**. The fleece looks visually like many soft clouds joined together, but it is not a pile of independent balls. It behaves as a continuous coat attached to an animal-like inner body.

Internally, the visible fleece can be understood broadly as:

- head / neck fleece
- body fleece

Externally, those two areas must still read as **one living Carol**, not as two disconnected objects.

The overall impression is round, soft, ambiguous, dreamy, and cute. Hard borders, boxiness, mechanical assembly, or obvious geometric construction are incompatible with Carol.

---

# 2. Skinと外側の毛の関係

Skin v004 exists as the internal animal-like body used to make coherent placement and movement of the exterior fleece easier.

The semantic relationship is:

`Skin = internal living body / support`

`Normal fleece = thick continuous coat attached around that body`

The fleece must not be interpreted as floating spheres placed around the Skin. It must also not be treated as a completely separate rigid shell unrelated to the Skin.

The fleece is visually very thick in many regions, but the hidden body remains the reason the final Carol reads as one animal.

### Human-readable thickness map

| Region | Fleece relative to Skin | Meaning |
|---|---|---|
| top of head | very thick | visibly fuller than the cheek-side fleece; exact difference must be read from Identity / approved Normal views, not from the interview multiplier |
| sides of face / cheeks | thick | approximately one medium fluffy-unit of outward fullness; continuous with head fleece |
| direct underside of jaw | **no directly attached fleece** | jaw itself remains bare; the fleece seen below comes from neck/chest behind it |
| around ear root | thin-to-medium locally | enough to hide the root naturally, but not enough to swallow the ear body |
| neck connection | medium, locally narrower | creates a weak narrowing between head and larger body without a visible seam |
| upper / central body | very thick | largest visible body fullness |
| body sides | thick | rounded animal-like section; no box walls |
| belly / near legs | medium and tapering | fleece wraps downward but does not become a flat skirt or touch the ground |
| rump | thick, smoothly reducing toward rear end | remains rounded and animal-like |

**No exact Skin→fleece offset distance is locked here where the authority images do not directly support one.** Exact offsets are implementation-derived targets constrained by the locked visible Front/Side dimensions and this map. False numerical precision is forbidden.

---

# 3. 正面から見た全体

Front must preserve the approved Normal Front identity:

- broad, round, compact overall form
- face centered on the same axis as the body
- small cream face embedded within much larger fleece
- huge eyes unchanged
- broad ears emerging naturally from within head fleece
- short visible legs
- heavy hooves
- crown remains broad and soft rather than tall

The head fleece surrounds the face from the top and sides. The visible fleece below the face belongs primarily to the neck/chest region behind the jaw, not to the jaw itself.

The lower edge of the fleece is not a straight horizontal skirt. It forms a soft rounded underside and opens naturally around the short legs.

---

# 4. 横から見た全体

Side is one of the clearest authorities for the hidden 3D meaning.

Human qualitative front→rear meaning is:

- the head region is rounded and substantial;
- the neck / transition becomes **slightly narrower** than the adjacent head and body;
- the main body becomes the **clearly fullest region**;
- the rump rounds down from that main-body maximum instead of staying tube-like.

The earlier conversational `1.0 → 0.8–0.9 → 1.25 → 1.0` example is retained only as evidence of this ordering. It must **not** be used as a production ratio. Exact relative heights and lengths must be measured from approved Normal Side.

The resulting Side flow is:

`head → weak narrowing around neck → largest rounded body → rounded rear convergence`

The body must never become a uniform tube, a rectangular box, or a chain of equal balls.

The face is in front of the body, and the larger body exists behind it. In 3/4 this front/back relationship must remain obvious without opening a gap between head and body.

---

# 5. 頭のてっぺん

The head-top fleece should be read primarily from **Normal Side + canonical Identity**.

Human decision:

- the head is not one giant single cloud mass
- the head fleece is better understood as being composed mainly from **medium + small fluffy forms**
- those forms together create one large rounded head impression
- the overall outer head remains smooth and cohesive despite this internal visual rhythm

Do not convert this into many equal spheres. Medium and small forms must merge into a continuous coat.

---

# 6. 顔の左右

The fleece at each side of the face belongs to the head fleece.

It should feel approximately like a medium fluffy-unit of side fullness, but **not like one literal sphere attached to each cheek**.

The correct interpretation is:

- medium + small rounded changes
- visually joined to the head-top fleece
- face edge remains readable
- no bead necklace / bead cheek pattern
- no perfect circular ring around the face

---

# 7. 顔の下

This is a hard semantic lock.

**No fleece grows directly from the jaw/chin.**

The fleece seen below the face comes from the neck / upper chest behind and below the head. From Front, this can visually overlap the lower face area. From Side, it must remain understandable that the jaw itself is not carrying a beard/collar.

Correct reading:

`jaw → small clean separation in depth → neck/chest fleece behind`

This separation should not become a conspicuous empty hole. It is a 3D ownership distinction, not a required visible gap.

---

# 8. 耳周辺

The ears originate from the Skin/head, not from the fleece.

Normal appearance:

- ear root is naturally covered by nearby head fleece
- most of the ear body remains clearly visible
- Front and Side both preserve the broad, soft, drooping ear identity
- the ear must look as if it emerges naturally from inside the coat
- do not carve a deep hole in the fleece and insert an ear board
- do not expose the entire mechanical root

Motion-specific Human decision:

- the **ear itself may move independently**
- surrounding fleece should remain almost still
- only minimal local accommodation is allowed if needed to prevent an impossible intersection
- do not make a large patch of head fleece follow the ear

---

# 9. 身体前側

The front-body / chest fleece belongs to the body-side coat while also forming the visible fleece below the head.

It must:

- connect head/neck and body without a collar seam
- avoid a horizontal shelf under the face
- hide enough of the forelegs to keep Carol low and compact
- remain rounded in cross-section

The chest must not project forward farther than the face/nose in a way that turns Carol into a wool ball with a pasted-on face.

---

# 10. 身体中央

The central body is the **largest overall body fullness**.

Human decision for body-fleece rhythm:

- the body coat is composed of **large + medium + small fluffy forms**
- together they form one Carol body coat
- the large forms establish the main body shape
- medium forms create major visible rhythm
- small forms appear selectively and must not become uniform noise

The body center is the visibly fullest Side region. Its exact amount of increase over the head must be taken from approved Normal Side, not from the interview example.

---

# 11. 身体後ろ側

The body gradually reduces from the central maximum toward the rump while staying round.

Rear-side fleece must not be:

- a wall
- a squared-off box corner
- a pile of equal rear balls

Instead, the continuous coat rounds into the rear end.

The rump supports the independent tail contact but must not absorb the tail into its own lobe pattern.

---

# 12. お腹側

The underside is rounded, not planar.

Correct flow:

`chest underside → belly → rear underside`

The coat wraps downward around the body and then naturally lifts/open around leg exits.

Human decision:

- slight extra small-scale detail near the lower edge is acceptable
- the big continuous flow remains dominant
- do not line up repeated small scallops
- do not extend fleece to the ground

---

# 13. 脚・蹄との関係

The legs are structurally connected to Skin, but much of their upper length is hidden inside the body fleece.

Normal visible rule:

- visible leg length remains approximately what the approved authority shows
- upper leg is hidden by fleece
- fleece reduction must never accidentally reveal long legs
- hooves remain large, heavy, planted, and visually important

The fleece opens locally around each leg rather than forming a flat curtain with legs stuck through holes.

---

# 14. 尻尾との関係

**Current Human decision supersedes the older tiny / mostly buried tail reading for the visible Normal tail.**

Desired tail:

- one independent **large-to-extra-large fluffy ball-like tuft** in qualitative read; this wording is NOT a numerical diameter lock
- attached at the rear as a cute, clearly separate expressive part
- almost none of the visible tuft is buried in the rump fleece
- only the actual contact patch is very slightly embedded / blended
- it is not just one of the rump fleece bumps
- it can react with a cute dog-tail-like `pyoko-pyoko` motion
- it must not become a long anatomical dog tail

No numeric tail size is locked by this interview. The words **large-to-extra-large fluffy ball-like tuft** describe the intended visual read relative to the old tiny/triangular-nub interpretation; they are not a ratio and do not authorize arbitrary enlargement. Determine final visible size from Carol Identity + approved Normal context while preserving the Human-decided semantics: a clearly independent fluffy tuft, almost entirely outside the rump fleece, with only the contact patch softly blended.

---

# 15. 月・星との関係

All decisions below are Human-confirmed.

### Moon

- belongs to the body fleece, not the head
- sits on the outer body coat
- only the contact area softly settles into the fleece
- it must not float away from the body

### Stars

- each star belongs to the local fleece region where it appears
- they are not free-floating rigid objects in the final character body
- they follow their local fleece region in gross motion

### Motion

- moon and stars primarily move with the fleece region to which they are attached
- do not create large independent dangling/swinging motion

---

# 16. 白・青・紫系の配置

Carol's palette expresses the same semantic theme as the character: **dream / stars / clouds / softness / ambiguity**.

Human decisions:

- white is dominant
- head is basically white
- head has only a very small amount of blue softly bleeding into it
- body has a more substantial blue area than the head
- blue is not a hard, clearly separated patch
- white and blue should feel **softly blurred / bled into one another**
- there is no requirement for a mathematically defined color boundary

Correct interpretation:

- blue is mainly an intrinsic fleece tint, with lighting/shading also contributing
- do not make every lobe receive the same blue shadow
- do not paint crisp graphic boundaries between blue and white
- do not turn the entire head blue
- transitions should follow the soft visual organization of the fleece rather than an obvious mask edge

Purple/lilac may appear as a very soft intermediate atmospheric tint where supported by Identity, but must remain subordinate to white + soft blue.

---

# 17. 真上から見た補完

Human-confirmed semantic Top shape:

`smaller head region → slightly narrower neck connection → largest body region → rounded taper toward rump`

It should resemble two smoothly connected rounded regions, but **not** a hard figure-eight and **not** one uniform ellipse.

The body section itself should remain rounded / oval and animal-like. No squared shoulders, slab sides, or rectangular top plan.

---

# 18. 真後ろから見た補完

Human-confirmed Rear reading:

- main body appears as one large rounded mass
- center/upper region is broad
- lower region becomes somewhat narrower as the legs emerge
- rump outer edge remains soft and round
- tail is a distinct rounded expressive tuft at/near rear center, almost fully outside the rump fleece except at its tiny contact patch
- both hind legs remain short and weight-bearing below the coat

Do not construct Rear as a grid of circular balls.

---

# 19. 斜めから見た補完

At front 3/4:

- face/head is clearly in front
- larger body is clearly behind
- neck fleece connects them without a visible cut
- face must retain real depth and must not become a flat sticker
- ear root remains naturally covered while the ear body stays readable
- lower-face fleece reads as chest/neck from behind, not jaw fur

At rear 3/4:

- body central fullness transitions into a rounded rump
- tail remains clearly independent
- body side-to-rear transition must remain round, not box-cornered
- hidden far legs may overlap naturally but the support structure must remain believable

---

# 20. 動いたときの関係

### Head turn / small head motion

Human-confirmed:

- face moves with the head
- head-top fleece and cheek-side fleece move with the head as the head region
- neck/body fleece does not rotate as one helmet with the head
- transition remains visually continuous

### Body motion

Human-confirmed correction:

- the **large overall fleece shape moves almost together with the body**
- do not give the whole fleece a visibly delayed jelly-like follow-through
- no broad wobbling cloud-ball behavior

Human-confirmed micro allowance:

- very small local surface softness is allowed
- medium/small fluffy surface forms may show minimal deformation/settling where needed
- this micro softness must never alter the major Carol shape

### Ear motion

- ear moves mostly independently
- surrounding fleece remains nearly still
- only tiny local accommodation if required

### Tail motion

- tail is independently expressive
- cute short `pyoko-pyoko` reactions are desired
- root remains attached; no floating or long-tail whip motion

### Legs

- limb motion originates from the hidden Skin support structure
- fleece continues to hide upper limb regions during small movements
- motion must not suddenly reveal long legs

---

# 21. 数字で固定する場合のルール

## 21.1 Primary measurement source

Production dimensions must be re-derived from the **approved visual authorities**, not from Human's conversational example numbers.

- `carol_front.png`: measure visible Front width, face placement/size, eye placement/size, ear visibility, fleece lower edge, visible leg/hoof proportions, and all other Front-readable relations.
- `carol_side.png`: measure total visible length, head/neck/body/rump flow, face projection, body maximum fullness, belly line, leg exposure, ear visibility, ornament placement, and other Side-readable relations.
- `carol-identity-canonical.png`: use as the highest identity/appeal check. Do not force orthographic measurements from it when perspective or illustration stylization makes that unreliable.

All measurements should be normalized to a common scale such as total Carol height `H = 1.000` only **after** the approved images are measured.

## 21.2 Human interview numbers are non-binding

The following kinds of values mentioned during Q&A were only shorthand for qualitative comparison and are **explicitly non-binding**:

- the `z1 / z2 / z3 / z4` example (`1.0 → 0.8–0.9 → 1.25 → 1.0`)
- the statement that head-top fleece felt roughly `1.5×` cheek-side fleece
- any similar approximate size, thickness, percentage, or multiplier stated to communicate “bigger / smaller / thicker / thinner”

Convert them into ordering constraints only:

- neck transition < adjacent head/body fullness
- main body = largest Side fullness
- head top > cheek-side fleece thickness

Then derive the actual ratios from Identity + approved Normal Front/Side.

## 21.3 Existing geometry-parameter numbers

Numbers already present in `CAROL_GEOMETRY_PARAMETERS.md` may be used as a **cross-check**, not as a higher authority than the images. Before implementation, compare every production-critical value against the approved Normal images. If the number would visibly pull the model away from the authority, discard or revise the number rather than changing Carol to satisfy it.

## 21.4 Inferred depth / unseen dimensions

Depth, thickness, Top, Rear, and 3/4 values that cannot be directly measured from Front/Side must be marked **INFERRED**. Infer them from:

1. Identity and the two approved Normal views,
2. Human-confirmed semantic relationships,
3. the frozen Skin as inner-body support,
4. multi-view continuity.

They must never be presented with false numerical precision. Use a range only when it materially helps implementation, and keep it provisional until visual multi-view validation.


## 21.5 Authority measurement revalidation — 2026-10-02

A dedicated authority-measurement pass was completed after Human clarified that all conversational size numbers were illustrative only.

Use `CAROL_AUTHORITY_MEASUREMENTS.md` as the measurement companion to this semantic spec. Key rules:

- exact approved Normal Front and Normal Side file hashes were verified against repository `authority.json`;
- fresh raster measurement independently supports the existing Front width / eye-scale locks;
- Side threshold measurement is within the existing ±2% soft-edge tolerance of the formal `1.300 H` length lock;
- direct raster measurements are cross-checks, not reasons to override visible authority;
- local Skin PNG copies available to this ChatGPT session did not hash-match repository `authority.json`, so no new production-critical Skin offsets were invented from them;
- Skin v004 `.blend` remains the frozen inner structural baseline;
- Human conversational multipliers remain non-binding.

Current visible-tail semantics supersede the older Normal-tail interpretation that required a tiny / mostly buried external tuft. However, Human words such as “large-to-extra-large” remain qualitative. Absolute tail size is still fitted to Identity + approved Normal visual context.

Current Human motion decision also supersedes older broad-fleece-follow-through wording for this phase: **macro body fleece follows the body nearly directly; only tiny local surface softness is permitted.**

# 22. 絶対禁止の見た目

Human accepted the following major NG set:

1. equally spaced bubble body
2. bead-like cheeks
3. perm-like fleece
4. helmet-like head fleece
5. collar / beard-like lower-face fleece
6. long tube body
7. boxy / squared fleece body
8. face buried deep inside fleece
9. long-looking legs
10. ears that look like flat boards inserted into holes
11. deep ear recesses / sockets created by fleece
12. moon or stars floating away from the coat
13. tail disappearing as just another rear fleece ball
14. hard seam dividing head fleece from body fleece
15. full fleece moving like jelly or a bouncing cloud ball
16. single giant head cloud replacing the medium+small head rhythm
17. perfectly equal cloud-lobe size everywhere
18. hard blue/white graphic patches
19. realistic sheep anatomy, long neck, long limbs, or muscular body
20. Front-correct / Side-correct but broken 3/4 geometry

---

# 23. Humanが明示的に決定した内容

The following are explicit Human decisions from this semantic interview and must not be silently reinterpreted:

- Skin was created as an internal animal-like structure to make coherent fleece construction easier.
- Head/neck fleece and body fleece are internally meaningful regions, but the final exterior looks like one large soft Carol.
- Head ends approximately around the ear region; head→neck→body continues naturally.
- Head and body have a weak narrowing between them, but no hard border.
- Direct jaw/chin has no attached fleece; fleece below the face comes from neck/chest.
- Head-side fleece has a meaningful fluffy thickness, while the head-top is visibly fuller. The earlier `1.5×` wording was only a size-feeling example; exact difference comes from the authority images.
- Head fleece is better read as mainly medium + small forms, not one huge dominant blob.
- Body fleece is composed of large + medium + small forms that together make one coat.
- Fleece is attached like an animal coat; it is not actually a pile of cloud balls.
- Body cross-sections and overall exterior must remain round; box-like sections are wrong.
- Front→rear fullness meaning is: rounded head → slight neck narrowing → clearly fullest main body → rounded reduction toward rump. The earlier numeric sequence was only a qualitative illustration.
- Ear root is hidden naturally by fleece; most of the ear body remains visible in Front and Side.
- Upper legs are substantially hidden; visible legs stay short like the authority.
- Belly underside is rounded and locally opens around legs.
- Tail should become a large-to-extra-large independent fluffy ball-like tuft, almost not buried except at the contact patch.
- Tail can react with cute dog-tail-like `pyoko-pyoko` motion.
- Blue is not a clearly defined hard blue; it softly bleeds through the dreamy white fleece.
- Head is basically white with only a little blue bleeding in.
- Body has a larger blue region than the head.
- Color boundaries remain intentionally ambiguous.
- Moon and stars belong to local fleece and move with it; they do not float independently.
- Top shape: smaller head → slight neck narrowing → larger body → rounded rear.
- Rear shape: broad round body with lower narrowing near legs; tail stays independent.
- When head turns, head-associated fleece moves with the head while body fleece does not rotate with it.
- Macro body fleece moves almost together with the body; do not use obvious delayed full-fleece secondary motion.
- Tiny local surface softness is acceptable.
- Ear can move independently while surrounding fleece stays almost still.
- Existing major NG set is accepted as sufficient.
- Mareep is comparison material only; only general 3D problem-solving ideas may be learned from it.

---

# 24. ChatGPTが画像・既存authorityから推定した内容

These are **inferences**, not direct Human statements. If they ever conflict with Human perception, Human wins.

- Front face should remain centered and strongly framed by fleece without becoming enclosed by a perfect ring.
- 3/4 should show the head clearly in front of the body, preventing the face from reading as pasted onto a single giant sphere.
- Body lobe hierarchy should use a few large anchors, medium transitions, and sparse small accents rather than procedural uniformity.
- Head lobe hierarchy should avoid a single crown blob and instead preserve the Identity/Side's medium+small clustered softness.
- Exact Skin→fleece offset values should be solved by matching the approved Normal views, not invented from pixel overlays across differently framed sources.
- Rear and Top should preserve rounded animal-like cross-sections throughout; any flat planes should be treated as implementation artifacts to remove.
- Blue/lilac should be material/color organization, not geometry segmentation.

---

# Appendix A — 大・中・小の形map

## Head

- **Large:** the overall head-fleece envelope only; do not model it as one visible giant lobe.
- **Medium:** primary visible head-top and cheek/side fluffy forms.
- **Small:** selective connectors / edge softeners that prevent mechanical seams.

## Body

- **Large:** central upper/side/rear body fullness that defines the body as a single rounded animal coat.
- **Medium:** major visible cloud-like changes across back, flank, chest, and lower body.
- **Small:** sparse finishing forms, especially where transitions need softness; never an even repeated border.

Rule: **size hierarchy serves one continuous coat. “Large / medium / small” never means separate free spheres.**

---

# Appendix B — 手前 / 奥 / 隠れ方map

## Front

- face is in front of neck/chest fleece
- head fleece overlaps face perimeter from top/sides
- chest fleece appears below face from behind the jaw
- ear roots sit behind/inside nearby head fleece while ear bodies project outward
- upper legs are behind body fleece; lower short legs and hooves project below it

## Side

- muzzle/face is foremost
- head fleece wraps around/behind the head but must not overtake the nose
- neck/chest fleece begins behind the jaw and connects into body fleece
- body is behind and larger than the head region
- near ear is readable; root is locally covered by fleece
- tail is outside the rump, with contact-only blending

## 3/4

- head and face remain visibly forward of body
- far body partially disappears behind the near head/neck relationship
- far ear/legs may be partially hidden naturally
- chest fleece can appear below the face but must remain spatially behind the jaw

---

# Appendix C — 一つながりmap

```text
HEAD TOP (medium + small rhythm)
  ↓
FACE-SIDE / CHEEK FLEECE
  ↓
EAR-ROOT SURROUND
  ↓
SHORT NECK FLEECE — weak narrowing
  ↓
FRONT BODY / CHEST FLEECE
  ↓
MAIN CENTRAL BODY FLEECE — largest fullness
  ↓
RUMP FLEECE — rounded reduction
  +
INDEPENDENT TAIL TUFT — contact-only attachment
```

This map describes **visual continuity**, not a requirement that all regions be one mesh.

---

# Appendix D — Literal-AI failure simulation

The candidate specification was tested against likely literal misreadings.

| Literal misreading | Prevented by |
|---|---|
| “cloud fleece” → place hundreds of spheres | §§2, 5, 10, Appendix A: continuous animal coat; sizes are surface rhythm, not objects |
| “two regions” → split head and body with a seam | §§1, 4, 9: weak narrowing but continuous exterior |
| “surround face” → make a perfect circular wool ring | §§6–7: irregular medium/small head fleece; lower face belongs to chest/neck |
| “no chin wool” → create an obvious empty hole below jaw | §7: ownership distinction in depth, not mandatory visible gap |
| “ear comes out of fleece” → drill socket and insert flat ear | §8: Skin-rooted ear with natural local overlap; no deep recess |
| “hide legs” → grow fleece to ground | §§12–13: rounded underside opens around short legs; hooves remain visible |
| “large tail ball” → merge a rear body lobe into a tail | §14: tail is independently attached with contact-only blending |
| “large tail” → create long canine tail | §14: large fluffy tuft, not long anatomical tail |
| “soft fleece” → jelly / bounce whole body coat | §20: macro fleece follows body almost directly; only tiny local softness |
| “blue areas” → paint hard blue patches | §16: blurred intrinsic tint; intentionally ambiguous transitions |
| “medium+small head” → create uniform popcorn texture | §5 + Appendix A: continuous outer head with selective hierarchy, not equal repetition |

**Result:** no blocking semantic ambiguity remains after rewrite.

---

# Appendix E — Multi-view contradiction test

## Front — PASS condition

- broad round fleece, centered face, broad ears
- face not buried
- no jaw beard/collar
- legs short

## 15° / 30° — PASS condition

- head begins to show real depth
- body becomes visible behind head without opening a seam
- cheek fleece does not turn into beads
- near ear root remains naturally covered

## 45° — PASS condition

- head is clearly forward, body clearly behind
- neck transition remains weak but present
- face remains volumetric
- chest fleece remains behind jaw

## Side — PASS condition

- authority-matched fullness rhythm: rounded head → slight neck narrowing → largest main body → rounded rear reduction
- rounded body section
- no long tube / no box
- legs remain short

## Rear 3/4 — PASS condition

- main body stays rounded
- rump does not collapse into a wall of balls
- tail reads as separate attached tuft

## Rear — PASS condition

- broad rounded body
- lower narrowing around legs
- independent tail contact

## Top — PASS condition

- smaller head → mild neck narrowing → larger body → rounded rump
- not figure-eight
- not rectangular
- not uniform ellipse

**Simulation result:** semantics are mutually compatible across the full turntable. No additional Human question is currently required.

---

# Appendix F — Motion contradiction test

| Motion | Required semantic behavior | Failure to prevent |
|---|---|---|
| small look left/right | face + head fleece move as head region; body fleece stays body-owned | helmet rotates as separate shell / whole body coat twists |
| small look up/down | head region moves; lower-face fleece remains chest/neck-owned behind jaw | jaw appears to grow beard / chest follows head unnaturally |
| ear flick | ear moves independently; surrounding fleece almost still | large fleece patch dragged by ear |
| small front-leg adjustment | hidden limb moves under coat; short exposed segment remains | long leg suddenly revealed |
| small body bob | macro fleece moves with body nearly as one; tiny local softness only | delayed jelly-body wobble |
| tail reaction | independent short `pyoko-pyoko` tuft motion | tail merges with rump or becomes long whip |

**Simulation result:** the semantic structure supports the intended small-motion set without requiring a change to the static meaning.

---

# Appendix G — Past-failure prevention audit

## v002

Observed historical risk: improved connectivity but still not exact enough as Carol's intended 3D meaning.

**PREVENTED BY:** canonical Identity first; Front+Side locks; Human semantic maps; no donor/past-fleece averaging; explicit Top/Rear/3Q completion.

## v003

Observed failures included helmet-like head fleece, broad shelves around the face, deep ear recesses, and weak/incorrect relief.

**PREVENTED BY:** §§5–8. Head = medium+small continuous fleece, jaw owns no wool, chest wool stays behind jaw, ear root gets soft overlap without socket/recess.

## v004-33

Observed failure: visibly inflated / unnatural fleece and incorrect global 3D read.

**PREVENTED BY:** §§2, 4, 10–12. Fleece is Skin-attached animal coat; front→rear fullness ratio; rounded cross-sections; no box/tube; central body is largest but returns smoothly at rump.

## v004-41

Observed remaining problems included bead-like cheek rhythm, conspicuous lower collar, overly broad dorsal lobes, unresolved ear/fleece junction, and incomplete blue/white grouping.

**PREVENTED BY:** §§5–8, §16, Appendix A/B. Cheeks are continuous medium+small head fleece, no jaw collar, ear root relation is explicit, head is not one giant crown blob, and color is softly bled rather than uniformly shaded.

---

# Appendix H — Research-derived design principles installed in this spec

The external production research conducted before the interview was reduced to these operational principles rather than copied as a style recipe:

- resolve large readable character form before surface detail
- infer unseen views as one coherent spatial character, not per-view cheats
- preserve stylized identity instead of “correcting” toward realistic anatomy
- use hierarchy in large / medium / small visible forms
- avoid uniform procedural repetition
- keep exterior covering related to the hidden support body
- validate the form under small movement, not only in a static turntable

These principles are subordinate to Carol's own authority and Human decisions.

---

# Approval boundary

The Human semantic interview is complete and the numeric-authority policy has been explicitly corrected: conversational Human numbers are size-feeling examples only, while production measurements come from Identity / approved Normal authorities.

This specification has completed:

- structured Human semantic interview
- Skin/fleece meaning map
- head/body connection definition
- Front/Side/Top/Rear/3Q completion
- thickness map
- front/behind/hidden map
- large/medium/small map
- motion relationship map
- forbidden-pattern collection
- Literal-AI failure simulation
- multi-view contradiction test
- motion contradiction test
- past-failure prevention audit

**Next step:** use this Human-confirmed semantic specification together with `CAROL_AUTHORITY_MEASUREMENTS.md` and `CAROL_FLEECE_ACCEPTANCE_CONTRACT.md` to execute the final Codex implementation plan. Final visible acceptance remains a later Human Geometry Gate; this document does not pre-grant that PASS.
