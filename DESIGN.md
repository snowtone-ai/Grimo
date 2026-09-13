# Grimo Design System

Status: **Normative design contract**  
Baseline: **2026-09-13 JST**  
Applies to: `snowtone-ai/Grimo`

This document defines the visual, interaction, motion, and quality contract for Grimo. It is intentionally more normative than the research notes. Implementation may improve internal architecture, but visible behavior should not drift from this contract without an explicit product/design decision.

---

## 0. Authority and evidence labels

### 0.1 Authority order

When sources conflict, use this order:

1. Current explicit user instruction
2. Character canonical image for character identity
3. This `DESIGN.md` for frontend / interaction design
4. Locked product/character/technical decisions in repo docs
5. Current working implementation and measured runtime behavior
6. External references and research notes
7. Legacy Grimoire behavior

`DESIGN.md` does **not** override canonical identity, data integrity/security contracts, or explicit later user decisions.

### 0.2 Reference roles

- **Pokémon Trading Card Game Pocket**: primary frontend visual/UX grammar benchmark.
- **Pokémon Let's Go Pikachu/Eevee**: primary direct-character-interaction and reaction-story benchmark.
- **Pokémon-Amie / Pokémon Refresh**: secondary benchmark for touch-zone semantics, petting, liked/disliked contact, and relationship behaviors.
- **Grimo canonicals**: only identity authority for Carol / Jill / Pino / Shushu.

The goal is high fidelity to the **design grammar and experiential qualities**, not copying Pokémon artwork, branding, icons, text, audio, card frames, or proprietary animation assets.

### 0.3 Evidence labels

Use these labels when adding or revising numeric values:

- **CONFIRMED** — directly established by Grimo locked decisions or clearly observed reference behavior.
- **HIGH-CONFIDENCE ESTIMATE** — triangulated from multiple reference screens/behaviors.
- **ESTIMATE** — plausible working value derived from references but not source-exact.
- **ENGINEERING TARGET** — Grimo-specific measurable acceptance target, not claimed to be a Pokémon internal value.
- **OPEN** — do not silently freeze; instrument and validate first.

---

# 1. Non-negotiable design rules

1. **Pocket is the frontend grammar authority; Pokémon assets are not Grimo assets.**
2. Primary navigation is exactly **Tasks / Grimo / Calendar** unless explicitly changed.
3. Default shell is **pale cool canvas + near-white elevated surfaces + blue-gray ink + aqua interaction accent**.
4. Default geometry target: **20px page gutter / 18px card radius / 24px modal radius / 28px sheet radius / 52–56px primary CTA**.
5. A root viewport has **one dominant visual hero**, not several equally weighted focal points.
6. Browseable root/list contexts keep navigation; immersive character/reward/editor contexts suppress nonessential chrome.
7. Tasks and Calendar must feel like functions inside Pocket's product grammar, not a SaaS todo app or Google Calendar clone.
8. Meaningful rewards use `ack → anticipation → reveal → settle → increment → next`; trivial success stays fast and non-blocking.
9. Character touch is **local-first**. Visible touch acknowledgment target is **≤100ms**, then anticipation → propagation → settle → afterglow.
10. Canonical identity, accessibility, Pixel-7a-class performance, and human aesthetic approval outrank reference imitation.

---

# 2. Core visual principles

## 2.1 Contextual density

Pocket-like quality is not achieved by making every screen sparse. Density changes by context:

- **Home/root**: low density, large hero, restrained utilities.
- **Collection/inventory**: calm shell + denser payload region.
- **Reward/interaction**: reduced chrome, single focal object/character.
- **Settings**: grouped controls with generous whitespace.

Do not apply one density level globally.

## 2.2 Material hierarchy

Default visual stack:

```text
pale cool canvas
  → near-white surface
    → soft border / weak shadow
      → content / hero
        → small local accent
```

Avoid heavy borders, dark chrome, glassmorphism everywhere, and decorative gradients on routine controls.

## 2.3 One focal hierarchy

On any viewport, visual priority should normally be:

1. current hero/content
2. current task/action
3. supporting metadata
4. navigation/utilities

Navigation should feel available, not dominant.

## 2.4 Effects are punctuation

Particles, glows, symbols, haptics, and celebratory motion are punctuation. They must not compensate for weak motion or unclear hierarchy.

---

# 3. Design tokens

The values below are Grimo normative defaults. They are reconstructed design tokens, not claims about Pocket source code.

## 3.1 Color

| Token | Value | Status | Usage |
|---|---:|---|---|
| `--g-canvas` | `#EEF7FB` | HIGH-CONFIDENCE ESTIMATE | app background |
| `--g-surface-1` | `#FBFEFF` | HIGH-CONFIDENCE ESTIMATE | primary cards/sheets |
| `--g-surface-2` | `#F3F9FC` | HIGH-CONFIDENCE ESTIMATE | secondary containers |
| `--g-surface-pressed` | `#E9F5F8` | ESTIMATE | quiet pressed state |
| `--g-ink-1` | `#354457` | HIGH-CONFIDENCE ESTIMATE | primary text |
| `--g-ink-2` | `#5C7187` | accessibility-adjusted | secondary readable text |
| `--g-ink-3` | `#8294A6` | ESTIMATE | tertiary labels |
| `--g-border` | `#D9E8F1` | HIGH-CONFIDENCE ESTIMATE | soft borders/dividers |
| `--g-action` | `#2BD4D3` | ESTIMATE | primary interactive accent |
| `--g-action-pressed` | `#18BEC1` | ESTIMATE | primary pressed state |
| `--g-action-ink` | `#173F4A` | Grimo accessibility rule | text/icon on bright aqua |
| `--g-notify` | `#F35B84` | HIGH-CONFIDENCE ESTIMATE | notification/accent only |
| `--g-success` | `#4AD9A5` | ESTIMATE | success/progress positive state |
| `--g-warning` | `#F1B85B` | ENGINEERING TARGET | warning, sparingly |
| `--g-danger` | `#D85A67` | ENGINEERING TARGET | destructive confirmation only |
| `--g-scrim` | `rgba(41,61,78,.26)` | ESTIMATE | modal/sheet backdrop |

Recommended CSS baseline:

```css
:root {
  --g-canvas: #eef7fb;
  --g-surface-1: #fbfeff;
  --g-surface-2: #f3f9fc;
  --g-surface-pressed: #e9f5f8;
  --g-ink-1: #354457;
  --g-ink-2: #5c7187;
  --g-ink-3: #8294a6;
  --g-border: #d9e8f1;
  --g-action: #2bd4d3;
  --g-action-pressed: #18bec1;
  --g-action-ink: #173f4a;
  --g-notify: #f35b84;
  --g-success: #4ad9a5;
  --g-warning: #f1b85b;
  --g-danger: #d85a67;
  --g-scrim: rgba(41, 61, 78, .26);
}
```

### Color rules

- Do not use pure black for normal text.
- Do not use white text on `--g-action` unless contrast is verified for the actual token.
- Notification pink/red is local punctuation, not a broad brand color.
- Character-specific colors may appear inside the Grimo viewport or character-specific item surfaces, but must not replace the global shell palette.

## 3.2 Typography

Use a Japanese-safe system sans stack unless a licensed product font is intentionally introduced later.

| Role | Size / line-height | Weight | Status |
|---|---|---:|---|
| Hero | `28 / 34px` | 700 | ENGINEERING TARGET |
| Page title | `24 / 30px` | 700 | ENGINEERING TARGET |
| Section | `19 / 26px` | 700 | ENGINEERING TARGET |
| Body | `15 / 22px` | 500 | ENGINEERING TARGET |
| Button | `15 / 20px` | 700 | ENGINEERING TARGET |
| Label | `13 / 18px` | 600 | ENGINEERING TARGET |
| Caption | `12 / 16px` | 500 | ENGINEERING TARGET |

Rules:

- Avoid dense all-caps English styling for Japanese UI.
- Primary content should not require tiny text to fit.
- Dynamic type / browser text scaling must not break core controls.

## 3.3 Spacing

Base grid: **4px**. Dominant rhythm: **8px**.

```text
4 / 8 / 12 / 16 / 20 / 24 / 32 / 40 / 48 / 64
```

Normative defaults:

- narrow phone gutter: **16px**
- normal phone gutter: **20px**
- wide phone gutter: **24px**
- card inner padding: **16–20px**
- section gap: **24–32px**
- compact row gap: **8–12px**

## 3.4 Radius

| Surface | Radius | Status |
|---|---:|---|
| compact chip | `999px` | HIGH-CONFIDENCE ESTIMATE |
| regular control | `14–18px` | HIGH-CONFIDENCE ESTIMATE |
| card | `18px` | HIGH-CONFIDENCE ESTIMATE |
| hero card | `24px` | ESTIMATE |
| modal | `24px` | HIGH-CONFIDENCE ESTIMATE |
| bottom sheet top | `28px` | HIGH-CONFIDENCE ESTIMATE |

Do not arbitrarily make every rectangle a pill.

## 3.5 Shadow / elevation

Routine surfaces should be separated mostly by color and small elevation.

```css
:root {
  --g-shadow-1: 0 2px 8px rgba(53, 68, 87, .08);
  --g-shadow-2: 0 8px 24px rgba(53, 68, 87, .12);
  --g-shadow-float: 0 14px 36px rgba(53, 68, 87, .16);
}
```

Rules:

- `shadow-1`: cards/rows where border alone is insufficient.
- `shadow-2`: modal/sheet/temporary elevated object.
- `shadow-float`: rare focal/reward element only.
- Never stack strong border + strong shadow + glow on routine surfaces.

## 3.6 Blur / transparency

- sheet/modal backdrop blur baseline: **12px** — ESTIMATE
- backdrop scrim opacity target: **0.20–0.32** — ENGINEERING TARGET
- do not blur the main app continuously.

---

# 4. UI motion tokens

These are normative Grimo defaults reconstructed from the benchmark behavior and tuned for mobile web.

| Token | Duration | Intended use |
|---|---:|---|
| `instant` | **80ms** | micro-state swap only |
| `fast` | **140ms** | press/hover/local acknowledgment |
| `normal` | **200ms** | small control transition |
| `panel` | **260ms** | sheet/card entrance |
| `deliberate` | **340ms** | emphasized but routine transition |
| `reveal` | **600ms** | meaningful reveal |
| `settle` | **820ms** | soft follow-through / emotional settle |

```css
:root {
  --g-motion-instant: 80ms;
  --g-motion-fast: 140ms;
  --g-motion-normal: 200ms;
  --g-motion-panel: 260ms;
  --g-motion-deliberate: 340ms;
  --g-motion-reveal: 600ms;
  --g-motion-settle: 820ms;

  --g-ease-standard: cubic-bezier(.22, .80, .24, 1);
  --g-ease-emphasized: cubic-bezier(.16, 1, .30, 1);
  --g-ease-exit: cubic-bezier(.40, 0, 1, 1);
}
```

### UI motion rules

- Routine panels do **not** spring/bounce.
- Press feedback should begin within one rendered frame where possible.
- Meaningful reward may use one controlled overshoot.
- Routine task completion must not block the user with a long celebration.
- Reduced motion removes translation/scale amplitude first, not semantic state change.

---

# 5. Layout system

## 5.1 Mobile-first viewport

Primary target is smartphone PWA. Pixel 7a-class Android is the minimum acceptance target.

- Use safe-area insets.
- Do not position essential controls under browser/PWA chrome.
- Root content must remain usable at 360px CSS width.
- Prefer one-handed bottom-zone actions for frequent operations.

## 5.2 Bottom navigation

Target height: **64px + safe area** — HIGH-CONFIDENCE ESTIMATE.

Destinations:

1. Tasks
2. Grimo
3. Calendar

Rules:

- No Items fourth tab.
- No Settings primary tab.
- Active destination is clear through icon + label/state, not only color.
- Passive notification dot: **8–10px**.
- Alert/count badge: **16–18px** minimum.

## 5.3 Hero occupancy

On root screens, one hero region should typically occupy **~32–58% of immediately visible vertical content**, depending on route.

For `/grimo`, the character/viewport should occupy roughly **42–58%** of the principal visual viewport in idle state before controls and navigation dominate.

These are composition targets, not rigid clipping rules.

---

# 6. Component contract

## 6.1 Primary button

- height: **52–56px**
- radius: `999px` or visually equivalent high-radius capsule where appropriate
- horizontal padding: **20–24px**
- text: Button token
- background: `--g-action`
- foreground: `--g-action-ink`
- pressed transition: **≤140ms**
- minimum hit target: **44×44 CSS px**

Disabled buttons should look unavailable without collapsing contrast of surrounding text.

## 6.2 Secondary button

- height: **44–48px**
- radius: **14–18px** or capsule based on context
- near-white/secondary surface with soft border
- no strong shadow unless floating

## 6.3 Icon button

- visual icon: usually **20–24px**
- hit target: **44×44px minimum**
- use quiet circular/squircle container when discoverability is needed

## 6.4 Card

Default:

- radius **18px**
- padding **16–20px**
- surface `--g-surface-1`
- border `--g-border` where needed
- shadow `--g-shadow-1` only if color separation is insufficient

Cards should contain one clear action/content purpose.

## 6.5 Sheet

- top radius: **28px**
- open/close transition: around **260ms** baseline
- backdrop blur: **12px** baseline
- swipe/dismiss behavior only when it does not conflict with content gestures

Secondary actions, task detail/edit, filters, and contextual menus prefer sheets over new top-level routes where appropriate.

## 6.6 Modal

- radius: **24px**
- use for focused confirmation or blocking decision only
- destructive confirmation must be visually distinct but not alarmist

## 6.7 Collection/inventory grid

- illustrated items: normally **2 columns** on standard phone
- icon-only compact inventory: may use **3 columns**
- surrounding shell remains airy even when payload is dense

---

# 7. Navigation and screen archetypes

## 7.1 Persistent navigation stays visible when

- the user is browsing a root destination
- leaving the screen does not destroy the current interaction meaning
- content is list/collection/overview oriented

Examples:

- `/tasks`
- `/grimo` idle
- `/grimo/items`
- `/calendar`

## 7.2 Navigation is suppressed when

- a single object/character is the entire interaction focus
- a meaningful reward is being revealed
- feeding or a rare reaction is in progress
- an editor/confirmation requires focused completion

Suppression should not trap the user. A clear exit/back path remains available.

## 7.3 Route mapping

### `/`

Startup gate only. Resolve startup preference quickly. Do not turn this into a dashboard.

### `/tasks`

Benchmark: Pocket Home + Missions grammar.

Composition:

1. Today/progress context
2. one hero task or current focus
3. rounded task cards
4. secondary detail/edit in sheet

Do not use spreadsheet/table-style SaaS task presentation.

### `/grimo`

Benchmark: Let's Go interaction + Pocket immersive hierarchy.

- character is primary hero
- idle state may retain bottom nav
- direct interaction reduces nonessential chrome
- semantic touch zones exist independently of visual overlays

### `/grimo/items`

Benchmark: Pocket collection grammar.

- calm header
- compact filter/sort controls
- denser item payload
- selected character context remains understandable

### `/calendar`

Benchmark: Pocket list/collection hierarchy, not Google Calendar styling.

- month overview + selected-day agenda
- avoid filling every month cell with long event titles
- selected day gets focused payload below/adjacent

### `/settings`

- secondary destination
- grouped sections
- generous whitespace
- pill/segment/toggle controls where appropriate
- no primary bottom navigation

---

# 8. Reward presentation

## 8.1 Sequence

Meaningful reward:

```text
acknowledge
→ short anticipation
→ reveal
→ settle
→ resource/progress increment
→ next/close
```

## 8.2 Timing targets

- routine success feedback usable again: **≤400ms** — ENGINEERING TARGET
- normal meaningful reward: CTA usable at **~0.9–1.3s** — ESTIMATE / target
- rare reward: skippable by **~1.8–2.4s** — ESTIMATE / target
- avoid unskippable sequences > **3s** unless the event is intentionally exceptional

## 8.3 Positive-only philosophy

Never use reward presentation to create guilt, scarcity pressure, punishment for absence, or pseudo-gacha pressure.

---

# 9. Character interaction grammar

## 9.1 Reaction story

Every core reaction should read as a causal story:

```text
Input
→ contact acknowledgment
→ anticipation / intent beat
→ local body response
→ face / gaze response
→ main body propagation
→ secondary motion
→ optional VFX / SFX / haptic
→ overshoot
→ settle
→ emotional afterglow
→ idle / attention
```

Not every reaction needs every stage, but contact causality must be visible.

## 9.2 Local-first propagation

Order:

1. touched part
2. adjacent part
3. face/gaze
4. whole body only if needed
5. secondary structures late

Bad pattern: whole sprite scales/bounces immediately while the touched part has no readable acknowledgment.

## 9.3 Benchmark timing envelope

These values are **Grimo prototype targets**, informed by Let's Go reaction storytelling and existing Grimo research. They are not claimed to be frame-exact Pokémon values.

| Metric | Target | Status |
|---|---:|---|
| pointer/input → first visible local acknowledgment | **50–100ms** | ESTIMATE + ENGINEERING TARGET |
| p95 input → visible acknowledgment | **≤100ms** | ENGINEERING TARGET |
| short anticipation | **180–350ms** | ESTIMATE |
| long anticipation | **350–700ms** | ESTIMATE |
| small reaction peak | **180–450ms** after ack | ESTIMATE |
| large reaction peak | **350–900ms** after ack | ESTIMATE |
| secondary motion lag | **+80–250ms** after primary starts | ESTIMATE |
| settle | **500–1200ms** | ESTIMATE |
| afterglow | **400–1600ms** | ESTIMATE |
| self-initiated invitation hold | **1.5–4.0s** | ESTIMATE |
| idle self-action cadence | roughly **5–10s**, with intentional quiet gaps | CONFIRMED Grimo direction |

## 9.4 Interruption target

New user input must redirect the active reaction rather than queueing clips indefinitely.

Engineering acceptance:

- valid new input should begin affecting visible state within **≤100ms p95**
- stale queued reaction should not begin after interruption
- `pointercancel`, lost capture, blur, or hidden state must release contact without generating an accidental tap

## 9.5 Gesture set

Launch-mandatory gestures:

- tap / poke
- slow pet / stroke
- back-and-forth stroke

`hold` is not a mandatory launch interaction.

Exact classifier thresholds for velocity, distance, reversal count, and duration are **OPEN until instrumented on device**. Implement them as configurable data, log the classifier inputs during prototype QA, and tune from real traces rather than hiding magic constants across event handlers.

## 9.6 Repetition

Target behavior:

- repeated same-zone input may select a different reaction
- use cooldown + recent-history suppression + state/context constraints
- eventual quality target: **3–5 variants** for frequently repeated actions where quality supports it
- one excellent reaction is preferred over five generic recolored motions

---

# 10. Character-specific motion identity

Same runtime does not mean shared animation.

## 10.1 Carol

Personality: **attention-seeking + relaxed**.

Motion propagation identity:

```text
head / cheek / ear local response
→ face/gaze
→ small ear response
→ main body shift
→ large fleece follows late
→ heavy feet remain grounded
→ soft settle
```

Rules:

- fleece is large, soft, and delayed relative to the core body
- hooves/feet feel heavy
- moon/star are special punctuation, not constant flashing
- no rigid-sphere fleece
- no whole-body paper-light bounce

Initial Carol timing bias:

- primary movement should usually use the slower half of the global reaction envelope
- fleece lag target: **120–250ms** after core body motion begins — ENGINEERING TARGET
- fleece settle should typically outlast core settle by **150–450ms** — ENGINEERING TARGET
- hoof/root contact drift during idle should be visually negligible

## 10.2 Jill

Personality: **attention-seeking + energetic**.

```text
chest / upper-body initiation
→ face
→ small wing response
→ tail from heavy root
→ leaf/flower secondary lag
```

Do not lengthen forelegs or turn leaf secondary motion into the primary driver.

## 10.3 Pino

Personality: **energetic + independent**.

```text
cheek / shoulder
→ soft waterbag body compression
→ face
→ heavy tail lag
→ droplets/bubbles late
```

No hollow-balloon scaling or cat-tail-fast wag.

## 10.4 Shushu

Personality: **relaxed + independent**.

```text
face / ear
→ plush compression/sink
→ bouquet-preserving arm/body response
→ ear rebound
→ flowers/petals late
```

Keep the seated center grounded and bouquet relation intact.

---

# 11. Touch-zone semantics

Runtime semantic zones are independent of the visual touch-map PNG.

Common semantics:

- GREEN: likes
- YELLOW: neutral/normal
- RED: mild dislike
- CYAN: special reaction
- GRAY: excluded input

Carol lock:

- GREEN: crown/top of head, cheeks, ear bases
- YELLOW: body fleece, **back**
- RED: tail area, feet
- CYAN: moon, star motifs
- GRAY: pupils/eyes, inside mouth

Mild dislike means avoidance/confusion/discomfort, not anger or punishment.

---

# 12. Feeding interaction

Benchmark: Let's Go staged feeding.

Minimum semantic stages:

```text
whole item
→ bitten
→ remainder
→ gone
```

Prototype target:

- at least **3 visible consumption states** — CONFIRMED direction
- each bite acknowledgment: **250–500ms** — ENGINEERING TARGET
- inter-bite emotional pause: **200–700ms** — ENGINEERING TARGET
- total routine feeding interaction should generally remain **~2–5s**, unless a rare reaction intentionally extends it — ENGINEERING TARGET

Mouth/cheek/body response and a short afterglow should make the item feel consumed rather than instantly deleted.

---

# 13. Self-initiated character behavior

Characters are not passive buttons.

Target behaviors include:

- occasional gaze toward user
- self-initiated “touch me / interact with me” invitation
- eventual gift behavior
- intentional quiet periods

Rules:

- do not stare at the user continuously
- do not trigger invitations every idle cycle
- invitation should remain readable for **1.5–4s** unless interrupted
- new input cancels/redirects invitation cleanly

---

# 14. VFX / SFX / haptic

Use sparingly.

- character-specific particles: yes, restrained
- nonverbal sound/cry: desired if feasible
- haptic: yes where platform permits
- reduced motion: preserve face/state semantics even when body amplitude is reduced

VFX acceptance rule: if the reaction becomes unclear when particles are disabled, the body/face motion is insufficient.

---

# 15. Performance and latency benchmarks

These are **Grimo engineering targets**, not inferred Pocket implementation values.

Primary acceptance device class: **Pixel 7a** or comparable mid-range Android.

## 15.1 Rendering

Target refresh: **60fps** when device/browser permits.

| Metric | Target |
|---|---:|
| nominal frame budget | **16.7ms** |
| active interaction p95 frame time | **≤20ms** |
| active interaction p99 frame time | **≤33.3ms** |
| frames >50ms in a 30s scripted interaction | **<1%** |
| obvious continuous jank during normal interaction | **0 accepted** |

If a device/browser cannot sustain 60fps, preserve input causality and character identity before adding visual effects.

## 15.2 Input response

| Metric | Target |
|---|---:|
| pointer event → visible local ack p50 | **≤70ms** |
| pointer event → visible local ack p95 | **≤100ms** |
| valid interrupt → visible redirect p95 | **≤100ms** |
| accidental action after pointercancel/lost capture | **0** |

Measure from actual event timestamp to the first frame containing the intended visible state change where practical.

## 15.3 Runtime stability

During a scripted **5-minute interaction loop**:

- no uncaught exceptions
- no detached/duplicated Pixi application after route remount
- no monotonic memory growth suggesting a leak
- no accumulating pointer listeners/tickers
- no reaction queue growth

A numeric heap cap is intentionally not frozen until browser/device measurement exists; track warm-up and retained trend instead.

## 15.4 Asset/render discipline

- do not render source PNGs at unnecessarily high DPR
- cap/adjust effective render resolution if measurement shows GPU pressure, while preserving face/detail quality
- avoid re-decoding/recreating textures during repeated reactions
- use a stable asset lifecycle across route mount/unmount

---

# 16. Visual fidelity QA targets

Human approval remains final, but quantitative checks should catch drift early.

These are **engineering QA targets**, not substitutes for Human Gates.

## 16.1 Neutral identity

For neutral Carol capture against the approved composition reference:

- character bounding-box center drift: target **≤2% of viewport width/height** unless intentionally reframed
- neutral overall scale drift: target **≤5%** from the approved baseline
- face center relative to head: target drift **≤2% of head width**
- eye-line rotation drift from approved neutral: target **≤2°**
- grounded hoof/root baseline: target vertical drift **≤3 CSS px** at the reference viewport during neutral idle

If these metrics conflict with a clearly better human-approved result, Human Gate wins and the baseline is updated.

## 16.2 Motion amplitude discipline

For routine idle:

- body translation should generally stay within **~1–2.5% of character height** — ENGINEERING TARGET
- head rotation generally within **~2–5°** — ENGINEERING TARGET
- secondary fleece/ear motion may exceed local amplitude but must not read as independent floating parts

For touch reactions, larger motion is allowed if contact causality remains legible and identity is preserved.

---

# 17. Human Gates + metrics

Metrics narrow the search space; humans approve the feel.

## Gate 1 — Identity

Inputs:

- canonical
- neutral runtime capture
- lightly deformed capture
- quantitative drift checks

Questions:

- same Carol?
- canonical appeal preserved?
- face survives deformation?

Do not proceed to reaction-system breadth if Gate 1 fails.

## Gate 2 — Idle

Show **15–30s** A/B/C candidates where practical.

Record:

- FPS/frame-time stats
- idle action timestamps
- motion amplitude settings
- user preference + discomfort points

## Gate 3 — Touch

Compare the same interaction A/B/C.

Record:

- input-to-ack latency
- anticipation duration
- peak timing
- secondary lag
- settle duration
- subjective judgment: fast/slow, large/small, scary/cute, stiff/soft

Translate feedback into parameter changes, not ad-hoc animation rewrites where possible.

## Gate 4 — Final character set

- four characters clearly distinct
- 5-minute interaction does not collapse mechanically
- repetition controlled
- phone interaction feels natural
- final user approval

---

# 18. Instrumentation contract

Character motion parameters should be observable and tunable.

For prototype/dev builds, support capture/logging of at least:

```text
input timestamp
zone
pointer path summary
classifier result
reaction id / variant
ack timestamp
primary motion start
peak timestamp
secondary motion start
settle start/end
interrupt timestamp/result
frame-time summary
```

Do not ship verbose interaction logs containing sensitive user data. The purpose is local prototype tuning.

Animation parameters should live in coherent typed config/data rather than scattered magic numbers across render callbacks.

---

# 19. Reduced motion and accessibility

Reduced motion must preserve meaning.

When reduced motion is enabled:

- reduce translation/rotation/scale amplitude substantially
- shorten or remove decorative overshoot
- keep facial/gaze/state transition
- keep semantic acknowledgment of touch
- keep reward information order even if the reveal is simplified

Other requirements:

- minimum interactive hit target: **44×44 CSS px**
- do not rely on color alone for selected/error state
- preserve readable contrast
- keyboard/focus semantics for non-canvas UI
- Canvas/Pixi interactions need accessible surrounding controls/state where applicable

---

# 20. Implementation acceptance checklist

A frontend/interaction milestone is not complete unless relevant checks below pass.

## Visual system

- [ ] uses Grimo semantic tokens rather than arbitrary per-screen colors
- [ ] hierarchy matches calm-shell/contextual-density rule
- [ ] one clear focal hero on root screens
- [ ] Tasks does not look like generic SaaS
- [ ] Calendar does not look like a Google Calendar clone
- [ ] immersive context suppresses nonessential chrome

## Character runtime

- [ ] canonical identity preserved
- [ ] touch response begins locally
- [ ] first visible touch acknowledgment p95 ≤100ms on target device class
- [ ] secondary motion is delayed, not simultaneous by default
- [ ] interruption redirects rather than queues
- [ ] pointercancel/lost capture generates no accidental tap
- [ ] reduced motion preserves semantic state

## Performance

- [ ] scripted browser/device test run captured
- [ ] p95/p99 frame-time inspected
- [ ] 5-minute runtime shows no obvious leak/listener/ticker accumulation
- [ ] resize/mobile viewport tested
- [ ] console/runtime errors checked

## Human quality

- [ ] relevant Human Gate completed
- [ ] A/B/C used when subjective timing/amplitude remains uncertain
- [ ] metrics and user feedback both recorded

---

# 21. Benchmark references

Use the current repo reference catalog for canonical URLs and evidence labels.

High-priority Let's Go references:

- Nose touch → pre-sneeze → sneeze → head shake → settle  
  `https://www.youtube.com/watch?v=0KSZwNZ5m1E&list=PLyNPy006ABoGutSw0Tj29MkGIXS-5tH-k&index=2`  
  `00:09–00:18`

- Self-initiated high five  
  same video  
  `00:30–00:45`

- Emotion VFX ♪ / ♡ / ☆  
  `https://www.youtube.com/watch?v=6tJzupfNSN8&list=PLyNPy006ABoGutSw0Tj29MkGIXS-5tH-k&index=1`  
  `00:30–00:34`, `01:16–01:20`, `02:42–02:45`

- Staged feeding  
  same video  
  `01:18–01:27`

- Head shake  
  same video  
  `02:31–02:35`

- Eevee present  
  `https://www.youtube.com/watch?v=KSS6UXwKqPk&list=PLyNPy006ABoGutSw0Tj29MkGIXS-5tH-k&index=3`  
  `03:35–03:45`

Pokémon-Amie / Refresh candidate references remain candidate-only until directly annotated. Do not invent favorite/disliked zones or timestamps from them.

---

# 22. Do / Don't

## Do

- reproduce Pocket-like hierarchy, material softness, proportions, spacing, and restrained motion through Grimo-owned assets/components
- measure motion and performance on actual browser/device contexts
- expose tuneable animation parameters
- use Human Gates for aesthetic approval
- make character responses causal and interruptible
- preserve quiet moments

## Don't

- copy Pokémon logos, art, branded icons, text, sound, card frames, or proprietary animation assets
- use generic “game UI” gradients/glows everywhere
- bounce every panel
- animate the entire character as one sprite when local response is required
- hide weak motion under particles
- freeze gesture thresholds before device traces exist
- parallelize four characters before Carol proves the runtime and quality bar

---

# 23. Change policy

Changes to this document should be rare and evidence-driven.

Update `DESIGN.md` when:

- a Human Gate establishes a better stable timing/amplitude baseline
- cross-character implementation proves a shared design rule should change
- a major frontend design direction changes
- new benchmark evidence materially changes the contract

Do not update it for one-off bugs, temporary experiments, or dependency patch changes.

When a numeric target changes, record whether it changed because of:

- reference evidence
- device measurement
- accessibility
- Human Gate preference
- implementation constraint

This keeps the design system measurable without pretending every reconstructed number is an original Pokémon source value.
