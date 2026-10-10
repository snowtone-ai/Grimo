# CAROL_AUTHORITY_MEASUREMENTS.md

**Status:** FINAL PLANNING MEASUREMENT SET — authority-first, pre-Codex
**Date:** 2026-10-02
**Purpose:** Re-measure the locked Carol visual authorities before Normal/Fleece implementation, and separate direct raster facts from inferred 3D meaning.

---

## 0. Source verification

Repository state was re-verified immediately before this measurement pass:

- Repository: `snowtone-ai/Grimo`
- Baseline branch: `codex/carol-skin-default-v004`
- Baseline HEAD: `e77b8ef53df7a6dfe6a6c6f47f24b8d0d11d7d8e`
- Compare result against that SHA: `identical`, ahead `0`, behind `0`
- Frozen working Skin: `assets/grimo/production/carol/blender/carol-skin-default-v004.blend`
- Frozen working Skin SHA256: `c14f15e35af18e17a63506ea1f4c8ec0f69cb4f52882d27cfa22cb01db7e1f7d`

Authority file hashes were checked against `assets/grimo/source/carol/approved-3d/authority.json`.

| Authority | SHA256 | Verification |
|---|---|---|
| canonical Identity | `63DB4EBA...CB4347CE` | exact match |
| Normal Front | `164A646F...3E024197` | exact match |
| Normal Side | `9484B7AC...A2D829B8` | exact match |

The locally available Skin Front/Side PNGs in this ChatGPT session do **not** hash-match the repository's `authority.json`. Therefore no new production-critical Skin dimensions are derived from those local PNGs. Skin geometry remains defined by the frozen v004 `.blend`, the repository authority package, and the supporting geometry contract. This prevents an accidentally stale Skin image from influencing the new fleece.

---

## 1. Measurement policy

Three classes are used:

- **DIRECT_RASTER** — measured directly from the exact approved Normal image bytes.
- **AUTHORITY_DERIVED_LOCK** — already established in `CAROL_GEOMETRY_PARAMETERS.md` from the approved references and rechecked here against the raster.
- **INFERRED_3D** — cannot be directly measured from Front/Side and must be solved by semantic continuity, then validated in 3/4, Rear, and Top.

Human conversational values such as `1.25`, `0.8–0.9`, `1.5×`, “large,” or “extra-large” are not numerical locks. They communicate ordering/meaning only unless explicitly declared otherwise.

For anti-aliased or soft-edged artwork, a few pixels are not geometric truth. Visible overlay agreement with the authority is more important than forcing a threshold-derived number.

---

## 2. Normal Front — exact authority measurement

Source: `assets/grimo/source/carol/approved-3d/carol_front.png`

- Canvas: `1254 × 1254 px`
- Exact SHA256: `164a646fbb2f335029e875a09ee4c337f52d8a09f650437420a6f1f83e024197`

### 2.1 DIRECT_RASTER outer envelope

Using the alpha channel with a small anti-alias threshold:

- visible subject bbox: `x=38..1221`, `y=148..1161`
- measured visible width: `1184 px`
- measured visible height: `1014 px`
- measured width / height: **`1.1677`**

This independently confirms the existing `overall visible width ≈ 1.171 H` lock to within about `0.3%`. Production should retain the existing nominal `1.171 H` target while using the image overlay as final visible truth.

### 2.2 Face / eye locks

Existing authority-derived locks remain valid:

- face width ≈ `0.530 H`
- face height ≈ `0.324 H`
- eye width ≈ `0.137 H`
- eye height ≈ `0.149 H`
- eye center spacing ≈ `0.324 H`

Fresh raster cross-check of the two eye dark envelopes:

- mean eye width ≈ **`0.1376 H`**
- mean eye height ≈ **`0.1489 H`**
- measured eye-center spacing ≈ **`0.3215 H`**

The differences are small and consistent with soft highlights/outline thresholding. Keep the existing authority-derived locks; do not refit eyes during fleece work.

### 2.3 Centerline rule

Do **not** intentionally reproduce tiny pixel-level asymmetry in the illustration as a shifted face. The explicit production rule remains:

`body/support centerline = face centerline`

Fleece must be built around that intended shared axis.

### 2.4 Hoof lock

Existing visible hoof lock remains:

- hoof width ≈ `0.219 H`
- hoof height ≈ `0.111 H`

A dark-core raster threshold measures roughly `0.209 H × 0.110 H`; the width undercount is expected because it omits lighter anti-aliased/soft outer pixels. Keep the existing visible hoof lock and do not alter hooves in this phase.

### 2.5 Fleece envelope lock

Existing authority-derived values remain the primary nominal anchors:

- max fleece width ≈ `1.161 H`
- overall visible width ≈ `1.171 H`

The final criterion is not numeric optimization alone. The Front overlay must preserve the exact broad, round, low Carol read.

---

## 3. Normal Side — exact authority measurement

Source: `assets/grimo/source/carol/approved-3d/carol_side.png`

- Canvas: `1448 × 1086 px`
- Exact SHA256: `9484b7ac49b9d53a517e7f05af6ca4f67f8cc8907cfbfedffe6d51cda2d829b8`

### 3.1 DIRECT_RASTER outer envelope

Using distance-from-white segmentation on the exact approved raster:

- visible subject bbox ≈ `x=110`, `y=79`, `w=1180`, `h=922`
- threshold-derived length / height ≈ **`1.2798`**

The existing formal Normal Side contract is `length = 1.300 H`. The difference is about `1.6%`, which is within the existing major-value tolerance and expected from white/soft edge thresholding. Therefore:

- **production nominal target remains `1.300 H`**
- **visual overlay to the exact Normal Side remains the final judge**

Do not replace the formal 1.300 target with 1.2798 merely because one raster threshold returned it.

### 3.2 Support-position cross-check

Fresh dark-envelope centers from the exact Side raster give approximately:

- front hoof center from raster subject front ≈ `0.401 H`
- rear hoof center ≈ `0.919 H`
- center-to-center spacing ≈ `0.518 H`

Existing authority-derived locks are:

- front support center ≈ `0.390 H`
- rear support center ≈ `0.920 H`
- spacing ≈ `0.530 H`

These are sufficiently close given soft rendering and the fact that dark hoof centroids are not identical to load/support centers. Keep the existing support locks. Fleece implementation must not move the Skin/hoof support system to chase silhouette overlap.

### 3.3 Side macro-form lock

The numerical values above do not replace the semantic Side requirement:

`rounded head → weak neck narrowing → fullest main body → rounded rump reduction`

This ordering is more important than any conversational Human multiplier. The exact visible amount of each rise/fall must be matched against the approved Side image.

---

## 4. Tail numeric policy

The Human semantic decision changes the interpretation of the visible Normal tail:

- independent fluffy tuft
- clearly readable as a separate expressive tail
- almost entirely outside the rump fleece
- only the contact patch is softly blended
- short `pyoko-pyoko` behavior, never a long dog tail

Human words such as “large-to-extra-large fluffy ball” are **not a numeric diameter command**. They mean “read as a real, separate fluffy tail rather than a tiny triangular nub or another rump bump.”

Therefore the older `0.085 H` / `0.095 H` / `70% hidden` Normal-tail values in `CAROL_GEOMETRY_PARAMETERS.md` must **not** be blindly enforced for the visible fleece shell. Preserve the frozen Skin tail/root unless technically necessary, and fit the final visible tail size to Identity + approved Normal context while preserving the Human semantic decision above.

Tail absolute size remains **VISUAL_AUTHORITY_FIT**, not a new hard ratio invented from the interview.

---

## 5. What is deliberately not assigned a fake number

The following cannot be reliably obtained as direct 3D dimensions from two 2D views and must remain `INFERRED_3D` until the same model passes multi-view validation:

- true fleece depth at the cheek
- true top-of-head depth
- neck cross-section depth
- body cross-section width at each longitudinal position
- Top-view narrowing amount
- Rear-view roundness
- exact Skin→fleece offset at arbitrary surface points
- exact depth overlap around ear roots
- exact moon/star embed depth

Codex must solve these from the semantic spec and frozen Skin, then validate them through Front / 15° / 30° / 45° / Side / Rear-3Q / Rear / Top renders.

---

## 6. Production numeric rule

Use the following precedence whenever a number conflicts with what the authority visibly says:

`Canonical Identity / approved Normal visible intent`
`>`
`authority-derived numeric lock`
`>`
`fresh threshold measurement`
`>`
`Human conversational estimate`
`>`
`implementation convenience`

Numbers are guardrails. They must never become a reason to make Carol visibly less like Carol.
