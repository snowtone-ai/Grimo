# Grimo — DESIGN.md

**ステータス:** アプリ全体に適用する正式Design Contract  
**更新日:** 2026-09-15 JST  
**対象:** Task / Calendar / Grimo / Collection、global navigation、reward surface、3D viewport chrome、UI motion、sound、haptics、accessibility、visual QA  
**主要UI/UX Benchmark:** Pokémon Trading Card Game Pocket（ポケポケ）  
**Character Runtime:** Full 3D / Blender → GLB/glTF → PlayCanvas / smartphone-first PWA

---

# 0. Design North Star

Grimoのapp shellは、**Pokémon Trading Card Game Pocketで観察できるinteraction grammarと触覚的な操作感を、実用上可能な限り高い精度で再現する**。

ただし、実際にshipするcharacter / image / icon / audio / effect / copyはGrimo独自でなければならない。

目標は「Pokémonに影響を受けた一般的なpastel mobile app」ではない。

目標は次である。

> **Grimo固有のcharacterとcontentを一旦取り除いても、情報階層、spacing rhythm、soft material language、navigation behavior、button depth、押下感、micro-interaction、screen transition tempo、sound feedback、Collection presentation、reward pacingから、ポケポケと同等のproduct-design disciplineを強く感じられる状態。**

これはアプリ全体へ適用する。

```text
visual design
+ layout
+ typography character
+ iconography grammar
+ pressed feel
+ micro-motion
+ sound effects
+ haptics
+ navigation consistency
+ reward reveal
+ collection completion pressure
```

Pokémonのlogo、card art、character art、UI image asset、proprietary icon file、抽出したsound recording、licenseのないproprietary fontはshipしない。

再現する対象は、観察可能なdesign原理とinteraction roleである。

---

# 1. 権威順位

visible productのdecisionが競合する場合は、次の順で優先する。

1. 現在のユーザー明示指示。
2. 承認済みGrimo canonical character asset / 承認済み3D production reference。
3. 本 `DESIGN.md`。
4. `GRIMO_PRODUCT_FEATURE_SPEC.md`。
5. `GRIMO_DATA_MODEL_SPEC.md`。
6. `GRIMO_EXPERIENCE_MOTION_BIBLE.md`。
7. `GRIMO_3D_BLENDER_PRODUCTION_BIBLE.md`。
8. 現在のrepository decisionと実測implementation behavior。
9. 外部reference research。
10. archive / legacy資料。

旧PixiJS / 2D / 2.5D UI前提は権威を持たない。

---

# 2. ポケポケReferenceのEvidence Model

推測値を「Pokémon内部の正確な値」として扱わない。

実装時は、次の3分類で考える。

- **OBSERVED / 観察済み** — 現行または最近のscreenshot、footage、official support、official developer materialで確認できる。
- **INFERRED / 推定** — screenshot / footageからreverse-engineeringした値。実装参考にはするが、内部値とは断言しない。
- **GRIMO DECISION / Grimo決定値** — 再現性を高めるため、Grimo実装として固定する具体token。

現在のresearch baselineから、次の特性を正式referenceとして採用する。

- white〜pale-blue-grayを中心とするbase surface。
- chromatic colorが占める面積は非常に小さい。
- raised / recessedをsoftに使うneumorphic surface。
- harsh blackではなくdark blue-grayのline / icon / text。
- cyan / tealを主要interaction accentとし、pink / yellowは限定的に使用。
- primary navigation surfaceではtext量が少ない。
- bottom-navのselected iconはoutline / raised appearanceからfilled / darker figure-ground stateへ変わる。
- Collectionのempty slotはrecessedに見える。
- 主要page title直下に細いiridescent / rainbow accent lineがある。
- back / cancel affordanceの位置が非常に一貫している。
- 広いdismiss領域と直接的transitionでfrictionを減らしている。
- tap地点にsubtleなiridescent / rainbow micro-feedbackがある。
- physical / digital interactionがsoundとvibrationで補強される。
- reference productでは30/60fpsやhaptics等のperformance settingが用意される。

2026年時点のUI observationでも、このsoft-material languageを主要基準として扱う。

---

# 3. Product Navigationは固定

4つのmain screenは次で固定する。

```text
Task
Calendar
Grimo
Collection
```

これらはprimary bottom navigation上で同格とする。

Settingsはsecondary navigationであり、5つ目のprimary destinationにはしない。

## 3.1 Bottom Navigation順序

Grimo決定値：

```text
Task | Calendar | Grimo | Collection
```

将来のusability testで明確に優れた並びが証明された場合のみ、明示的product decisionとして変更する。

selected tabはポケポケ的figure / ground inversionを使用する。

```text
inactive = 細いdark blue-gray outline / soft raised field
active   = compact filled dark blue-gray glyph / より強いvisual weight
```

通常selected stateに大きなsaturated color背景を使わない。

## 3.2 Bottom Navigation Geometry

```css
--nav-content-h: 58px;
--nav-icon-box: 40px;
--nav-glyph: 23px;
--nav-safe-bottom: env(safe-area-inset-bottom);
```

- Navigationは視覚的に軽く保つ。
- heavyなtop dividerは使わない。
- surface / light-shadow separationを使う。
- hit targetは最低48×48 CSS px。
- iconだけで意味が明確かつ検証済みならlabel省略可。labelを使う場合はsmall / low-contrast。
- colorだけに依存せずselected stateが理解できること。

---

# 4. App全体のVisual Material

## 4.1 Material Principle

app shellは、**1枚の淡いsoft materialからcontrolが盛り上がり、slotが沈み込んでいる**ように見せる。

```text
background material
→ raised card / button
→ pressed / recessed state
```

すべてのcomponentを「白rectangle + gray border」として設計しない。

構造表現はborderよりもlight / shadow / shallow gradientを優先する。

## 4.2 Primary Palette

以下は観察したポケポケpaletteから導いた**Grimo実装token**であり、Pokémon内部値を主張するものではない。

```css
:root {
  --g-canvas-0: #edf6fb;
  --g-canvas-1: #e4f0f7;
  --g-surface-0: #f7fbfd;
  --g-surface-1: #eef7fb;
  --g-surface-2: #e5f1f8;
  --g-recess: #dceaf3;

  --g-ink-strong: #40566c;
  --g-ink: #596f84;
  --g-ink-soft: #8094a7;
  --g-ink-faint: #afbfcc;

  --g-cyan: #0bc9c7;
  --g-cyan-pressed: #08b8b8;
  --g-sky: #78bced;
  --g-pink: #f74486;
  --g-yellow: #ffc33d;

  --g-success: #2ecf9f;
  --g-warning: #ffc33d;
  --g-danger: #f05a78;
  --g-info: #70b9ec;

  --g-scrim: rgba(61, 79, 98, .22);
  --g-scrim-strong: rgba(52, 69, 88, .34);
  --g-light: rgba(255,255,255,.92);
  --g-light-soft: rgba(255,255,255,.62);
  --g-shadow: rgba(77,111,137,.18);
  --g-shadow-soft: rgba(83,115,139,.11);
}
```

### Color Rule

画面の**80–92%をpale neutral material**で構成する。

chromatic accentは、primary CTA、active toggle、notification badge、reward rarity、special state、character/content artなどに集中させる。

UIがCarol / Jill / Pino / Shushuより目立ってはいけない。

---

# 5. Background / Gradient

plain flat whiteだけではsterileすぎる。逆に強いillustrated backgroundはcharacterと競合する。

基本背景は非常に淡いgradientを使う。

```css
--g-bg-main:
  linear-gradient(180deg, #edf7fc 0%, #e8f3f9 48%, #f4f9fc 100%);
```

hero card付近のみ、必要に応じて局所的なwarm / cool tintを追加できる。

```css
radial-gradient(circle at 30% 20%, rgba(255,190,210,.18), transparent 45%),
radial-gradient(circle at 78% 12%, rgba(117,195,241,.18), transparent 42%);
```

特別なreward / hero eventを除き、page全面に高彩度色を敷かない。

---

# 6. Typography

referenceでは、日本語にRodin系gothic、数値等にFutura系geometric treatmentの傾向が観察される。

これはlicense前提ではなく**style target**として扱う。

## 6.1 Grimo Font Strategy

現実的な基準：

```text
Japanese UI: M PLUS 1p / Noto Sans JP fallback
Latin body: 可能なら同family
Timer / level / compact number: Jost等のlicense済みgeometric sans
```

licenseが明確なRodin系fontを将来使える場合は、既定fontを置き換える前にvisual A/B gateを行う。

license証明なしにproprietary font fileを同梱しない。

## 6.2 Weight

```text
Regular body      500
Secondary         500
Button            600
Page title        700
Critical number   600–700
```

ultra-thin textは避ける。referenceの質感はsoftであり、fragileではない。

## 6.3 CSS Scale

約360–430 CSS px幅のphoneを基準とする。

```css
--type-xxs: 10px;
--type-xs: 11px;
--type-sm: 12px;
--type-body: 14px;
--type-body-lg: 15px;
--type-button: 14px;
--type-title: 17px;
--type-hero: 20px;
```

line-height：

- compact control: 1.10–1.20
- body: 1.45–1.60
- modal copy: 1.50–1.65

textを小さくして詰め込むより、word countを減らす。

---

# 7. Spacing / Geometry

4px base unitを使用する。

```css
--sp-1: 4px;
--sp-2: 8px;
--sp-3: 12px;
--sp-4: 16px;
--sp-5: 20px;
--sp-6: 24px;
--sp-8: 32px;
--sp-10: 40px;
--page-gutter: clamp(16px, 4.6vw, 22px);
```

## 7.1 Corner Radius

```css
--r-xs: 8px;
--r-sm: 12px;
--r-md: 16px;
--r-lg: 20px;
--r-xl: 24px;
--r-pill: 999px;
```

Reference feel：

- small chip / tab: pill
- icon button: 12–16pxまたはcircle
- main tile / card: 16–22px
- bottom sheet / modal: 22–28px

すべてをfull pill形状にはしない。

---

# 8. Neumorphic Elevation System

light sourceはupper-leftから当たるように統一する。

## 8.1 Raised

```css
box-shadow:
  -4px -4px 10px rgba(255,255,255,.78),
   4px  6px 12px rgba(76,108,134,.16);
```

## 8.2 Soft Raised

```css
box-shadow:
  -2px -2px 7px rgba(255,255,255,.66),
   2px  4px 8px rgba(76,108,134,.11);
```

## 8.3 Recessed / Slot

```css
box-shadow:
  inset 3px 3px 7px rgba(79,111,137,.13),
  inset -3px -3px 7px rgba(255,255,255,.72);
```

## 8.4 Pressed

pressed stateを単なる「色を暗くする」にしてはいけない。

```css
transform: translateY(1px) scale(.985);
box-shadow:
  inset 3px 3px 7px rgba(74,104,129,.17),
  inset -3px -3px 7px rgba(255,255,255,.66);
```

同じmaterial自体が押し込まれたように感じること。

---

# 9. Button System — 「押した感」は必須

reference productの強さはstatic screenshotだけではなく、controlが即座に応答し、押した感覚がある点にある。

## 9.1 Interaction Phase

意味のあるbuttonは次のphaseを持つ。

```text
REST
→ PRESS
→ ACTIVATE / CANCEL
→ RELEASE
→ RESULT
```

### REST

soft raised surface。heavy borderなしでもaffordanceが分かること。

### PRESS

pointer downの次のrendered frameから視覚反応を開始する。

目標：

```text
visual acknowledgement ≤ 16–33ms
```

適用：

- 約1px沈み込み
- `scale(.985)` 前後
- raised shadow → inset shadow
- 必要に応じてaccent saturationをわずかに上げる

### ACTIVATE

有効なpointer-up / click時：

- route / actionを即時開始
- soundを鳴らす
- 対応・有効化されていればhaptic
- dead timeなしでresult / loading stateを出す

### CANCEL

pointerが外へ出たままreleaseされた場合：

- RESTへ復帰
- success sound / hapticは出さない

### RELEASE

約100–130msでRESTへ戻す。

通常UIでspringyな `1.08` overshootは使わない。

## 9.2 Timing

```css
--motion-press: 80ms;
--motion-release: 120ms;
--motion-micro: 160ms;
--motion-screen: 200ms;
--motion-sheet: 240ms;
--ease-out: cubic-bezier(.2,.8,.2,1);
--ease-press: cubic-bezier(.2,.7,.3,1);
```

## 9.3 Primary CTA

標準height：`52–56px`。

- pillまたはstrong rounded
- cyan→skyのsubtle gradient
- thick outlineなし
- 重要CTAのみvery soft exterior glow可

```css
background: linear-gradient(90deg, #65d9e7 0%, #72c5f4 100%);
```

## 9.4 Secondary Button

pale surface + dark-blue-gray text/icon。

RESTではraised、PRESSではrecessed。

## 9.5 Destructive Button

巨大な常設red blockは使わない。

destructive colorは局所化し、不可逆data lossにはconfirmationを要求する。

---

# 10. Global Tap Micro-Feedback

referenceで観察できるtap地点のsubtle rainbow / iridescent feedbackを、Grimo独自effectとして再現する。

## 10.1 `tap_glint`

有効なdiscrete tap時：

```text
small iridescent point / ring
→ 10–18pxへexpand
→ soft cyan / pink / yellow fringe
→ fade
```

Duration：`160–220ms`。  
Peak opacity：`0.12–0.22`。

以下では出さない。

- scroll中
- pointermoveごと
- text field
- petting中のcontinuous event
- reduced motion要求時

意識して眺めるeffectではなく、触った感覚として知覚される程度にする。

---

# 11. Header Grammar

主要page header：

```text
centered page title
optional help icon at top-right
thin iridescent line directly below title region
```

```css
background:
  linear-gradient(90deg,
    #f74486 0%,
    #ffc33d 35%,
    #70d6d3 68%,
    #78bced 100%);
```

line height：1–2px。

sheenを追加する場合もslow / subtleとし、reduced motionでは停止または簡略化する。

---

# 12. Iconography

- simple line icon
- rounded corner / endcap
- blue-gray
- low detail
- 22–24px前後でもfigure / groundが明瞭

thin line icon、heavy emoji、異なるstroke systemを混在させない。

active bottom navはsaturated backgroundではなく、fill / figure-ground inversionで表現する。

Notification badge：

- small pink / coral circle
- high contrast
- 最小限の `!` またはcount
- control右上へoverlap

---

# 13. Card / Tile

home-like functional tileは次の構造を基本とする。

```text
large soft rectangle
pale gradient
large simple icon
short label
optional tiny status / timer
```

phone portraitの2-column tile gapは12–16px。

tile radiusは18–22px。

RESTでraised shadow。

1つのtileに長い説明文を入れない。

---

# 14. Tab / Segmented Control / Toggle

segmented tabはlow-height pill container + recessed material。

selected stateは以下の組み合わせで表現可能。

- slightly raised pale surface
- darker text
- thin accent

active toggle：

- cyan / teal track
- light circular thumb
- shallow shadow
- thumb motion 約140–180ms

ON / OFFでは関連するが区別できるSFXを使用する。

---

# 15. Collection Grammar

Collectionはinventoryの付録ではなく、first-class main screen。

referenceから、**empty positionそのものがcompletion pressureを生む**原理を採用する。

## 15.1 Grid

phone portrait：

```text
richなGrimo reward card → 2 columns
text readabilityを完全維持できる場合のみ3 columns
```

密度より「集めたくなる見え方」を優先する。

## 15.2 Undiscovered Slot

```text
recessed material slot
faint index / silhouette / rarity hint
no noisy lock illustration
```

物理的に空いているslotのように感じること。

## 15.3 Discovered Card

slotからわずかにraisedして見せる。

high rarityでは、Grimo独自表現として以下を限定的に使える。

- restrained gradient
- animated gloss
- iridescent edge
- small parallax-like response

Pokémon card graphic自体は模倣しない。

## 15.4 Detail

Collection entryを開いた時は「所有物をinspectしている」感覚を作る。

- large art / 3D thumbnail
- compact metadata
- 4体のreaction-discovery status
- primary use CTA
- consistent bottom-centered close / back affordance

---

# 16. Modal / Sheet Grammar

soft sheet / modalと、非常に一貫したback / cancel配置を使用する。

## 16.1 Standard Sheet

- contextをdimするscrim
- pale rounded surface
- top radius 24–28px
- short centered title
- generous whitespace
- primary actionはbottom付近
- 適切な場合はbottom centerにcircular `×` close control

## 16.2 Dismiss Behavior

安全なsheetでは、以下を可能にする。

- backdrop tap
- swipe down
- close button

routine sheetでtiny corner `×` を探させない。

不可逆destructive confirmationはbackdrop tapで誤dismissしない。

---

# 17. Screen Transition Grammar

referenceではperceived immediacyを優先する。

## 17.1 Navigation Transition

目標：

```text
activationからroute transition開始 ≤ 100ms
主要visible transition 約160–220ms
```

shallow crossfade + slight vertical / scale changeを使う。

通常navigationで長いcinematic motionを使わない。

## 17.2 Sheet

```text
scrim fade 約160ms
sheet enter 約220–260ms
```

## 17.3 Directness

harmless actionへ不要な中間confirmation menuを追加しない。

頻繁なdestinationは、navigation costを下げるなら複数entry pointを持ってよい。

---

# 18. Sound Design — UIを無音にしない

Grimoが目標とするtactile qualityにはaudioを含む。

Pokémon側のofficial developer materialでも、physical pack opening感をsoundとvibrationで補強する設計原理が説明されている。

Grimoではその原理を次のように採用する。

> **soundはcontrolに物理感を与える。ただしcontentより大きく・重要になってはいけない。**

Pokémonのsound recordingを抽出・sample・exact copyしない。

同じinteraction roleを担うoriginal Grimo SFXを制作する。

## 18.1 Audio Bus

logical busを分離する。

```text
MASTER
BGM
UI_SE
CHARACTER
REWARD
```

user-facing settingsでは統合してもよいが、最低でも `BGM` と `SE` は別controlにする。

## 18.2 UI SFX Palette

### `ui_tap_soft`

小さいutility icon、low-stakes navigation。

```text
35–70ms
dry / soft transient
rounded high-mid click
ほぼtailなし
```

### `ui_confirm`

primary CTA、save / accept、task追加確定。

```text
70–130ms
soft physical click + short bright upper layer
わずかなupward pitch implication
```

### `ui_back`

back / cancel / close-sheet。

```text
60–110ms
confirmより少しlower / darker
short downward pitch implication
```

### `ui_tab`

bottom navigation / segmented tab。

```text
40–80ms
very small / clean / low-fatigue
```

### `ui_toggle_on` / `ui_toggle_off`

同familyの2音。

ONは少しbright / high、OFFは少しlower / soft。

### `ui_disabled`

原則silence。

feedbackが必要な場合のみ、very-low-levelのdull tick。

positive confirm soundを使わない。

### `ui_error`

```text
100–180ms
muted two-part rejection
harsh buzzer禁止
```

### `ui_sheet_open` / `ui_sheet_close`

soft material / air movement、約90–160ms。

closeはopenよりshort / lower。

## 18.3 Sound Timing

有効activationでは次を目標とする。

```text
visual press     immediately
SE onset         activationから目標 ≤ 50ms
haptic onset     対応deviceでは目標 ≤ 50ms
route / result   sound完了待ちを入れない
```

audioがnavigationをblockしてはいけない。

## 18.4 Repetition Control

- scrollでは鳴らさない。
- pointermoveでは鳴らさない。
- high-frequency tapはrate-limit。
- continuous Grimo pettingで同じUI tickをpointer eventごとに鳴らさない。
- dense repeated actionではvolume variationを下げてfatigueを防ぐ。

## 18.5 Loudness Hierarchy

相対的perceived hierarchy：

```text
tab / minor tap       1.0
ordinary confirm      1.2
task completion       1.4
collection discovery  1.6
reward chest          1.8
rare reward           2.2
character hero beat   scene-dependent; never clips
```

SFX間で驚くようなvolume jumpを作らない。

---

# 19. Task / Reward SFX

Task completionはproductivityとGrimo reward loopを結ぶため、generic checkboxより少しだけemotional weightを持たせる。

## 19.1 Task Checked

```text
press
→ immediate local check sound
→ visual completion
→ reward生成時のみ別のreward-ready cue
```

checkboxとrewardを1つの大きなjingleへまとめない。

### `task_complete`

```text
180–320ms
soft click / pop + restrained bright tail
```

## 19.2 Reward Ready

### `reward_ready`

```text
180–350ms
short rising shimmer
```

意味は「何かが受け取れる状態になった」であり、full revealではない。

## 19.3 Chest Open

### `chest_open`

Grimo独自family：

```text
physical latch / pop
→ airy bright reveal
→ rarity layer
```

Common reward：~300–500ms。  
Rare reward：~700–1200ms。

auto-open有効時の日常task managementで長いreveal待ちを強制しない。

---

# 20. Collection SFX

### `collection_new`

初発見時のみ。

```text
200–400ms
clean glassy / soft digital shimmer
```

### `collection_open`

short material / UI inspection sound。

### Rarity Layering

一貫した1 familyで構成する。

- 同じbase transient
- rarityが高いほどharmonic tailをrichにする
- high rarityのみspatial / iridescent layer追加

5レア度を完全に別jingleにしない。

---

# 21. Character Audio

Character soundはMotion Bibleへ従い、ordinary UI soundとは分離する。

## 21.1 Rule

```text
body acting単独で意味が伝わる
↓
audioは既に読めるphysical eventを補強する
```

character vocal / foleyでdead animationを隠してはいけない。

## 21.2 Carol

- soft breathy / nonverbal acknowledgement
- gentle fleece / soft-body foley
- hoof soundはsparse / heavier
- harsh angry cueではなくtiny protest
- moon / star chimeはrare / special beatのみ

## 21.3 Touch Audio

pointer frequencyではなくsemantic event単位で鳴らす。

```text
contact_begin
meaningful_local_ack
primary_reaction_peak
contact_release
settle_special
```

continuous pettingではvery quietなmaterial textureを使ってよいが、click-click-clickの連続音は禁止。

## 21.4 Spatialization

companion presentationはfront-facingなので：

- left / right contactへsubtle stereo localization
- exaggerated binaural movementは禁止
- bodyが明確にoffsetする場合を除きcharacter vocal identityはcenter寄り

---

# 22. Haptics

reference productではvibrationをphysical interaction補強に使用する。

Grimoも対応browser / deviceでは同じ原理を使う。

hapticsは**progressive enhancement**であり、core meaningをhapticに依存させない。

推奨intent mapping：

```text
minor UI tap        none or very light
primary confirm     light
task complete       light short pulse
reward ready        light
chest open          medium short
rare reward         two-part restrained pulse
Grimo local touch   meaningful acknowledgementのみ
error               distinct short pulse, aggressive禁止
```

以下ではvibrateしない。

- scroll
- petting sampleごと
- blink / micro-motionごと
- autonomous character behavior

browser / PWAのhaptic supportはplatformごとに異なる。capability detectionし、unsupported時はsilent fallbackする。

---

# 23. 3D Grimo Screen — ポケポケShell × Living Companion

Grimo screenはcard referenceと最も異なる画面だが、**UI shell grammarはポケポケを維持**し、hero contentだけをfull-3D living characterへ置き換える。

## 23.1 Hero Priority

```text
1. Grimo character
2. current immediate interaction affordance
3. minimal status / utility controls
4. primary bottom navigation
```

reference appでpack / cardがcompositionのheroになるように、Grimo screenではcharacter自身をheroにする。

## 23.2 Camera

user-facing companion viewpointはfront-facing固定を基準とする。

side / back assetはproduction correctness用。

3Dだからという理由だけでorbit controlを追加しない。

## 23.3 Canvas / DOM Split

```text
DOM / React overlay
  title, controls, sheets, Collection/reward UI, accessibility

PlayCanvas canvas
  character, environment, character VFX, semantic touch hit volume
```

通常app textをWebGL内に描画しない。

## 23.4 Touch Priority

UI overlay hit regionが3D hit regionより優先。

UI外のtouchはsemantic 3D interactionへroutingする。

modal scrim表示中はcharacter touchをblockする。

scroll gestureで誤ってpettingが発火しないこと。

## 23.5 Safe Character Area

明示的なface safety boxを持つ。

routine controlを以下へ被せない。

- face / eyes
- major touch zone
- signature motif
- characterが差し出しているinteraction body part

controlはtop edge / lower cornerへ寄せる。

## 23.6 Background

character backgroundはpale / low-detail。

許可：

- soft blue / white gradient
- subtle character-specific tint
- shallow floor / contact shadow
- restrained environmental accent

attachmentやtouch readability、performanceを改善すると証明されるまではbusy room sceneを作らない。

---

# 24. 3D Performance / Visual Integration

minimum target device classはPixel 7a。

## 24.1 Frame-rate Design

```text
60fps preferred interaction
30fps graceful fallback where required
```

どちらも安全と仮定せず実測する。

3D framerateが落ちてもUI press feedbackは即時でなければならない。

## 24.2 Degradation Order

```text
reduce invisible / secondary cost
→ reduce effect density
→ reduce expensive shading
→ reduce secondary simulation
→ reduce resolution carefully
```

最初に削ってはいけない：

- facial readability
- local touch acknowledgement
- key authored motion
- canonical silhouette

## 24.3 Loading

full 3D asset読み込み完了前にapp shellを表示する。

- interactiveに見せかけたfake frozen character imageは禁止。
- compact / clear progress state。
- 可能ならaggressive full-screen spinnerを避ける。

---

# 25. Task Screen

Taskはproductivity SaaS dashboardではなく、ポケポケのfunctional listに近い軽いUIとする。

## 25.1 Structure

```text
page title
thin iridescent line
compact date / context
task list
bottom-reachable add action
bottom nav
```

## 25.2 Task Row

raised pale row。

含める要素：

- title
- optional time / category
- completion control
- minimal metadata

completed stateをgray dead textだけにしない。

checkboxのrecess / confirm、gentle text deemphasis、reward生成時のdistinct cueを使う。

以下は禁止：

- dense table
- left rail
- heavy card stack
- enterprise dashboard pattern

---

# 26. Calendar Screen

Calendarも同じsoft-material languageを使う。

## 26.1 Month Header

previous / current / next controlをcompactにする。

## 26.2 Day Cell

mostly flat / recessed。

- selected dayのみgentle raisedまたはcyan accent
- task存在はtiny dot / mark
- categoryごとのrainbow color codingはしない

## 26.3 Daily Detail

bottom sheetまたはcalendar下listを使う。

trivial inspectionのためにroute nestingを増やさない。

---

# 27. Collection Screen

Collectionはポケポケreferenceを最も直接的に活かす画面。

必須：

- centered title + iridescent line
- compact filter / sort region
- recessed empty slot
- card grid
- search icon
- filter / sort control
- selected filterはcyan accent
- detail sheet + consistent bottom close

目標感覚：

> **「空いている場所を埋めたい。見つけたものを開いて眺めたい。」**

---

# 28. Reward / Chest Experience

Product Specではchest-based reward revealを使用する。

referenceのpack openingで優れている「ユーザーが開封に参加している感覚」を原理として使う。ただしpack自体はcopyしない。

## 28.1 User Agency

可能な範囲で：

```text
reward is ready
→ user taps chest
→ inputに対するphysical response
→ reveal
```

単なるrandom popupではなく、自分が開けた感覚を作る。

## 28.2 Reveal Hierarchy

Common：

- fast
- low VFX
- short sound

Rare：

- longer anticipation
- richer light
- stronger but restrained haptic
- richer audio tail

rarityをcolorだけで伝えない。

---

# 29. UI Motion System

## 29.1 Rule

- motionはstate changeを説明するために使う。
- ordinary navigationはfast。
- tactile pressはimmediate。
- reward motionは比較的slowでもよい。
- idle UIを常時floatさせない。
- ornamental motionはGrimo characterと競合しない。

## 29.2 Reduced Motion

`prefers-reduced-motion` 時：

- `tap_glint` expansion削除またはopacity-only
- nonessential parallax削除
- sheet travel量削減
- pressed stateとsemantic feedbackは保持
- character meaningを削る場合は必ずalternate cueを用意

---

# 30. Sound Settings UX

Settingsで最低限次をcontrolできるようにする。

```text
BGM
SE
Haptics（capabilityがある場合）
```

optional：

```text
Character voice / foley
```

reference-likeなsimple slider / toggleを使う。

sound slider変更時は短いsafe previewをrate-limit付きで再生する。

Muteはreward / character-special sequenceも含めてglobalに尊重する。

---

# 31. Web Audio Implementation Contract

low-latency PWA UI soundの実装規約：

- user gestureから `AudioContext` をinitialize / resumeする。
- 最初のinteraction後にcore UI SFXをpreload / decodeする。
- ordinary UI SFXは非常に小さなassetにする。
- button press後に初めてfetch / decodeしない。
- pointer handler + click handlerでduplicate playbackしない。
- 必要に応じてpage visibility change時にBGMをstop / attenuateする。
- user volume / mute settingをpersistする。
- audio failureでrequested actionをblockしない。

---

# 32. Accessibility

ポケポケ再現はusability低下の免罪符ではない。

要件：

- minimum practical target 44×44 CSS px、原則48×48推奨
- icon-only controlにはsemantic label
- selected / error stateをcolorだけに依存させない
- reward / Collection stateへscreen-reader label
- reasonableなkeyboard / focus viability
- safe-area support
- text zoom resilience
- reduced motion
- audio mute
- haptic optionality

neumorphismはlow contrastになりやすいため、icon / text contrastとstate changeを意図的に強くする。

---

# 33. QA — Reproduction Fidelity Gate

visible UIはcode reviewだけで合格にしない。

major screenごとに、matched phone proportionのcuratedポケポケreference setと比較する。

## 33.1 Static Visual Gate

確認：

- overall whiteness / pale-blue balance
- chromatic color面積
- surface depth
- shadow direction
- card / tile radius
- typography scale
- title position
- bottom-nav weight
- whitespace
- icon weight

## 33.2 Interaction Gate

60fps captureで確認：

- pointer-down acknowledgement
- press depression
- release
- `tap_glint`
- route start latency
- sheet open / close
- selected-nav inversion
- toggle motion

## 33.3 Audio Gate

clean screen recording / direct audio captureで確認：

- visual activationより明確に遅れない
- clippingなし
- repeated tab tapが疲れない
- confirm / backを聞き分けられる
- task-complete / reward-readyが別signal
- muteで期待busすべてが消音される

## 33.4 3D Integration Gate

確認：

- characterがvisual heroを維持
- UIがface / touch zoneを隠さない
- touch→character causalityが読める
- 3D負荷でUI pressがhitchしない
- sound / VFX OFFでもcharacter actingが成立

---

# 34. Research Reference Set

implementation review用に小さなreference indexを維持する。

著作権上の利用根拠がないPokémon screenshotをproduction bundleへ同梱しない。

本contractのresearch basisには次を含む。

- 2026時点のPokémon TCG Pocket App Store / Google Play presentation
- official Pokémon TCG Pocket website / support material
- The Pokémon Company developer articleで説明されたphysical-card feel、digital expression、sound、vibration
- pale neumorphic shell、bottom navigation、Collection grid、modal、cyan active controlを示すcurrent / recent screenshot
- typographyを計測しRodin / Futura-like characterを指摘する2026 UI analysis
- consistent bottom cancel / back、subtle rainbow tap feedback、direct transition、broad dismiss affordanceに関するUI observation
- Grimo Product Feature Spec / Data Model Spec
- Grimo Experience Motion Bible
- Grimo 3D / Blender Production Bible

reference app側にmaterialなUI changeがあった場合は、このcontractを変更する前に再調査する。

---

# 35. Hard “Never Do” List

1. dark fantasy / parchment / RPG-book stylingへ戻さない。
2. generic Material Design cloneにしない。
3. pale soft shellを全面saturated gradientへ置き換えない。
4. すべてのcardへheavy black borderを付けない。
5. すべてのcontainerをpure-white + 同一drop shadowにしない。
6. buttonをflatかつ無反応にしない。
7. press feedbackを色変更だけにしない。
8. SFX完了待ちでnavigationを遅延させない。
9. scroll / pointermoveでUI soundを鳴らさない。
10. continuous pettingでUI clickを連打しない。
11. hapticだけで意味を伝えない。
12. decorative UIでGrimo faceを隠さない。
13. defaultで3D orbit controlを追加しない。
14. 通常app textをPlayCanvas内に描画しない。
15. particlesで弱いcharacter actingを隠さない。
16. rarity animationでroutine task completionを遅くしない。
17. sampled / extracted Pokémon soundをshipしない。
18. Pokémon icon / logo / card asset / proprietary artをshipしない。
19. license証明なしにproprietary fontをbundleしない。
20. motion / audio / haptics / tactile responseを無視した状態で「ポケポケ風」と呼ばない。

---

# 36. One-Page Implementation Summary

```text
LOOK
pale blue-white material
+ soft upper-left light
+ restrained cyan / pink / yellow accents
+ dark blue-gray ink
+ small iridescent hooks
+ minimal text

SHAPE
large rounded soft surfaces
+ raised controls
+ recessed empty slots
+ stable bottom navigation

PRESS
next-frame visual depression
+ inset shadow
+ tiny scale / down shift
+ short original UI SFX
+ optional light haptic
+ immediate result

NAVIGATION
direct
fast
consistent back / cancel placement
large dismiss areas
selected icon figure-ground inversion

COLLECTION
recessed empties
+ desirable discovered cards
+ filter / search
+ inspectable detail
+ discovery audio

GRIMO
front-facing 3D hero
+ minimal DOM chrome
+ UI avoids face / touch zones
+ semantic character sound
+ no orbit by default

QUALITY
reference screenshot comparison
+ 60fps interaction capture
+ audio latency check
+ real mobile browser check
+ Human Gate
```

将来の実装がtechnically cleanでも、この**静かで、触感があり、磨かれ、高応答なproduct feel**を再現できていない場合は、本Design Contract上FAILとする。
