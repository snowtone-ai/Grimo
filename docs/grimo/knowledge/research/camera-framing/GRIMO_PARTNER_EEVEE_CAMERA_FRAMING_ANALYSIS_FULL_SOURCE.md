# GRIMO_PARTNER_EEVEE_CAMERA_FRAMING_ANALYSIS

## 1. Executive Conclusion

### 結論

Partner Eevee 3動画を、外部知識を使わず添付MP4そのものだけで確認した。

最重要結論は以下。

1. **通常の全身ふれあい構図（Video 01 / 06）は、顔をほぼ水平中央に置き、Neutral時の face center Y は約 `0.40–0.46`。**
3. **通常全身構図の幅占有率は、Neutralで約 `0.62–0.67`、大きな通常反応で約 `0.75–0.78`。**
4. **Video 02（ハイタッチ）は別camera cutというより、同一interaction scene内の“近接/前寄り状態”として観察されるが、左・上・下でsilhouetteが継続的にclipしている。** そのため、通常camera基準ではなく `rare / close framing outlier` として扱うべき。
5. 背景の固定ランドマークを比較すると、採用interaction区間では**camera追従・zoom変化を示す明確な画面変化は確認できない**。キャラクターのroot / pose / forward leanによるscreen-space変化で説明できる範囲が大きい。

## 2. Video Corpus

全ファイルは `1920 × 1080 / 30 fps`。

| ID | Source | Duration | Frames | Benchmark use |
|---|---|---:|---:|---|
| 01 | `01_【ピカブイ】イーブイとのふれあい【ポケモン Let's Go! イーブイ】_1080p30(2).mp4` | 208.733 s | 6262 | 通常全身interactionの主要基準 |
| 02 | `02_【ピカブイ】イーブイとのハイタッチがかわいい！【ポケモン Let's Go! イーブイ】_1080p30(3).mp4` | 128.167 s | 3845 | 近接 / forward framing outlier |
| 06 | `06_【ピカブイ】イーブイのほっぺすりすり【ポケモンレッツゴー イーブイ】_1080p30(2).mp4` | 120.400 s | 3612 | 通常全身interactionの主要基準 |

### Excluded regions

- Video 01: 冒頭black / dialogue overlayはcamera benchmarkの代表frameから除外。
- Video 02: 冒頭black / empty background / dialogue導入を除外。
- Video 06: 冒頭menu、および約4–6秒付近の別構図intro close-upを除外。全身interactionへ入った後を正式benchmarkに使用。

---

## 3. Measurement Method

### Source-only rule

測定値は添付MP4から直接取得した。Pokémonに関する一般知識、3D cameraの既知値、外部動画は使用していない。

### Scan procedure

1. 各MP4を開始から終了まで時系列にdecode。
2. 全durationを2秒間隔でoverview scan。
3. Neutral / Typical / Maximum候補周辺を追加で確認。
4. 採用frameを元解像度 `1920 × 1080` 座標で測定。
5. cursor、VFX、音符、ハート、menu icon等はcharacter boundsから除外。
6. Video 06の花・リボン等は可能な範囲でEevee本体silhouetteと分離して評価。完全分離不能箇所はuncertaintyへ反映。

### Bounding box definition

```text
left_px   = visible Eevee body の最左端
right_px  = visible Eevee body の最右端
top_px    = visible Eevee body の最上端
bottom_px = visible Eevee body の最下端
```

frame外へ身体が続いている場合は、visible boundをframe edge (`0` / `1919` / `1079`) とし、`clipped` と明記する。

### Normalization

```text
left_ratio   = left_px / 1920
right_ratio  = right_px / 1920
top_ratio    = top_px / 1080
bottom_ratio = bottom_px / 1080

character_width_ratio  = (right_px - left_px) / 1920
character_height_ratio = (bottom_px - top_px) / 1080

top_margin_ratio    = top_px / 1080
bottom_margin_ratio = (1080 - bottom_px) / 1080
left_margin_ratio   = left_px / 1920
right_margin_ratio  = (1920 - right_px) / 1920
```

### Landmark convention

- `face_center`: eyes / nose / mouthで構成されるfacial feature massの中心。
- `eye_line`: 左右眼中心の平均Y。closed-eye frameは見えているeye-lineを使用。
- `body_center`: torso / ruff massの視覚中心。bbox中心ではない。
- `ground/contact_line`: 足底とforeground/contact surfaceが読める場合のみ記録。

### Measurement uncertainty

この資料は自動segmentationのpixel-perfect ground truthではなく、original frame上の手動silhouette tracingによるbenchmark。

- unobstructed contour: おおむね `±10–15 px`
- VFX / accessory / edge clippingを含むframe: おおむね `±20–30 px`
- frame edgeでclipしている場合、**visible boundは確定できても、true anatomical extentは推定不可**。

ratio換算ではおおむね `±0.005–0.015` 程度の不確かさを見込む。

---

## 4. Frame Selection Table

| Frame ID | Video | Time | Approx. frame | Scene class | Use | Clipping |
|---|---:|---:|---:|---|---|---|
| E01-N | 01 | 120.0 s | 3600 | Neutral | 通常全身Neutral | top clip |
| E01-T | 01 | 30.0 s | 900 | Typical Interaction | 頭を下げる中程度反応 | bottom near-edge |
| E01-M | 01 | 70.0 s | 2100 | Maximum Practical Extent | 大きな喜び・耳横展開 | bottom near-edge |
| E02-Q | 02 | 120.0 s | 3600 | Quiet-close | 近接状態のquiet sample。Neutral-Aには不採用 | left/top clip |
| E02-T | 02 | 10.0 s | 300 | Typical-close | 顔周辺interaction | left/top/bottom clip |
| E02-M | 02 | 115.0 s | 3450 | Maximum observed clipped extent | 横耳 + close state | left/top clip; true extent unknown |
| E06-N | 06 | 100.0 s | 3000 | Neutral | 通常全身Neutral | top/bottom near-edge |
| E06-T | 06 | 50.0 s | 1500 | Typical Interaction | 中程度の喜び反応 | top/bottom near-edge |
| E06-M | 06 | 35.0 s | 1050 | Maximum Practical Extent | 耳横展開 | bottom near-edge |

### Important classification

Video 02には、Missionで定義した

> 「通常正面待機 + 大きなMotionなし + 身体全体が確認できる」

を同じcamera状態で満たすframeが確認できない。

したがってVideo 02をNeutral統計へ混ぜない。

---

## 5. Raw Pixel Measurements

### Character bounds

| Frame | left | right | top | bottom | width | height | uncertainty |
|---|---:|---:|---:|---:|---:|---:|---|
| E01-N | 205 | 1495 | 0 | 1030 | 1290 | 1030 | ±15 px; top clipped |
| E01-T | 160 | 1490 | 240 | 1079 | 1330 | 839 | ±15 px |
| E01-M | 120 | 1550 | 40 | 1079 | 1430 | 1039 | ±20 px; VFX excluded |
| E02-Q | 0 | 1575 | 0 | 1030 | 1575 | 1030 | ±20 px; left/top clipped |
| E02-T | 0 | 1605 | 0 | 1079 | 1605 | 1079 | ±20 px; 3 edges clipped |
| E02-M | 0 | 1775 | 0 | 1030 | 1775 | 1030 | ±25 px; true width > visible possible |
| E06-N | 305 | 1490 | 0 | 1079 | 1185 | 1079 | ±20 px; top clipped |
| E06-T | 385 | 1500 | 0 | 1079 | 1115 | 1079 | ±20 px; top clipped |
| E06-M | 235 | 1730 | 110 | 1079 | 1495 | 969 | ±20 px |

### Key landmarks

| Frame | face center (x,y) | eye line y | body center (x,y) | ground/contact y |
|---|---|---:|---|---:|
| E01-N | (947, 500) | 448 | (930, 760) | 1007 |
| E01-T | (1028, 704) | 659 | (960, 875) | 1030 |
| E01-M | (965, 402) | 360 | (950, 735) | 1015 |
| E02-Q | (870, 590) | 532 | (730, 820) | 未測定 / 推定不可 |
| E02-T | (900, 615) | 504 | (710, 835) | 未測定 / 推定不可 |
| E02-M | (910, 620) | 525 | (730, 820) | 未測定 / 推定不可 |
| E06-N | (965, 430) | 385 | (930, 760) | 1005 |
| E06-T | (925, 435) | 410 | (915, 760) | 1007 |
| E06-M | (920, 540) | 509 | (930, 800) | 1005 |

Video 02では前景 / body cropにより足底とground contactの分離ができないため、ground lineを逆算していない。

---

## 6. Normalized Measurements

| Frame | L | R | T | B | width occ. | height occ. | face X | face Y | eye Y |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| E01-N | 0.107 | 0.779 | 0.000 | 0.954 | 0.672 | 0.954 | 0.493 | 0.463 | 0.415 |
| E01-T | 0.083 | 0.776 | 0.222 | 0.999 | 0.693 | 0.777 | 0.535 | 0.652 | 0.610 |
| E01-M | 0.062 | 0.807 | 0.037 | 0.999 | 0.745 | 0.962 | 0.503 | 0.372 | 0.333 |
| E02-Q | 0.000 | 0.820 | 0.000 | 0.954 | 0.820 | 0.954 | 0.453 | 0.546 | 0.493 |
| E02-T | 0.000 | 0.836 | 0.000 | 0.999 | 0.836 | 0.999 | 0.469 | 0.569 | 0.467 |
| E02-M | 0.000 | 0.924 | 0.000 | 0.954 | 0.924 | 0.954 | 0.474 | 0.574 | 0.486 |
| E06-N | 0.159 | 0.776 | 0.000 | 0.999 | 0.617 | 0.999 | 0.503 | 0.398 | 0.356 |
| E06-T | 0.201 | 0.781 | 0.000 | 0.999 | 0.581 | 0.999 | 0.482 | 0.403 | 0.380 |
| E06-M | 0.122 | 0.901 | 0.102 | 0.999 | 0.779 | 0.897 | 0.479 | 0.500 | 0.471 |

### Margin ratios

| Frame | top margin | bottom margin | left margin | right margin |
|---|---:|---:|---:|---:|
| E01-N | 0.000 | 0.046 | 0.107 | 0.221 |
| E01-T | 0.222 | 0.001 | 0.083 | 0.224 |
| E01-M | 0.037 | 0.001 | 0.062 | 0.193 |
| E02-Q | 0.000 | 0.046 | 0.000 | 0.180 |
| E02-T | 0.000 | 0.001 | 0.000 | 0.164 |
| E02-M | 0.000 | 0.046 | 0.000 | 0.076 |
| E06-N | 0.000 | 0.001 | 0.159 | 0.224 |
| E06-T | 0.000 | 0.001 | 0.201 | 0.219 |
| E06-M | 0.102 | 0.001 | 0.122 | 0.099 |

---

## 7. Neutral Framing

正式Neutral比較はVideo 01 / 06のみ。

### Observed

| Metric | Video 01 | Video 06 | Median | Range |
|---|---:|---:|---:|---:|
| character width ratio | 0.672 | 0.617 | 0.645 | 0.617–0.672 |
| character height ratio | 0.954 | 0.999 | 0.976 | 0.954–0.999 |
| face center X | 0.493 | 0.503 | 0.498 | 0.493–0.503 |
| face center Y | 0.463 | 0.398 | 0.431 | 0.398–0.463 |
| top margin | 0.000 | 0.000 | 0.000 | 0.000 |
| bottom margin | 0.046 | 0.001 | 0.024 | 0.001–0.046 |

### Interpretation

**Fact:** faceはほぼ画面水平中央に置かれる。

**Fact:** Neutralでも長い耳は上端でclipしている。

**Fact:** body / feetは画面下端に非常に近い。

**Inference:** Partner Eeveeでは「全silhouetteを常にsafe areaへ完全収納」よりも、**face readabilityとlarge on-screen presenceを優先**している。

---

## 8. Interaction Framing

### Ordinary full-body interaction

Video 01 / 06のTypical代表frame：

| Metric | Median | Min | Max |
|---|---:|---:|---:|
| width occupancy | 0.637 | 0.581 | 0.693 |
| height occupancy | 0.888 | 0.777 | 0.999 |
| face center X | 0.509 | 0.482 | 0.535 |
| face center Y | 0.527 | 0.403 | 0.652 |

face Yのrangeが大きいのはcamera movementではなく、Eevee自身が頭を下げる / 上げるため。

### Close interaction / forward state

Video 02代表frame：

| Metric | Median | Min | Max |
|---|---:|---:|---:|
| width occupancy | 0.836 | 0.820 | 0.924 |
| height occupancy | 0.954 | 0.954 | 0.999 |
| face center X | 0.469 | 0.453 | 0.474 |
| face center Y | 0.569 | 0.546 | 0.574 |
| left margin | 0.000 | 0.000 | 0.000 |

**Fact:** close stateでは常時silhouetteが複数edgeへclipする。

---

## 9. Maximum Safe Envelope

### Ordinary interaction maximum — Video 01 / 06

大きな喜び、耳横展開などの代表frame：

| Metric | Median | Min | Max |
|---|---:|---:|---:|
| width occupancy | **0.762** | 0.745 | **0.779** |
| height occupancy | **0.930** | 0.897 | 0.962 |
| top margin | 0.069 | 0.037 | 0.102 |
| left margin | 0.092 | 0.062 | 0.122 |
| right margin | 0.146 | 0.099 | 0.193 |

### Practical range

通常全身interactionのrepresentative sample全体では：

```text
character_width_ratio  ≈ 0.58–0.78
character_height_ratio ≈ 0.78–1.00
```

ただしheight ≈ 1.00は「完全に余白ゼロで安全」という意味ではない。

**Eeveeがframe edgeで意図的にclipされているため、visible occupancyが1.00に達している。**

### Typical framing

```text
Neutral width:  0.62–0.67
Typical width:  0.58–0.69
Face Y neutral: 0.40–0.46
Face X:         ≈ 0.50
```

### Ordinary interaction safe envelope

Eeveeの実映像上のordinary maximumは概ね：

```text
width  ≈ 0.78
height ≈ 0.96–1.00 visible frame use
```

### Rare outlier

Video 02のclose stateではvisible widthが `0.92` に達し、左端でさらに身体がframe外へ続く。

したがって：

```text
rare close-up observed visible width >= 0.92
true full silhouette extent = unknown
```

これはdefault safe envelopeから除外する。

---

## 10. Camera Stability Analysis

### Observable

採用interaction区間で背景の固定物を比較すると、背景位置は実質固定。

background-onlyに近いROIをframe間比較した結果、位相相関による見かけ上のshiftは、cleanな比較frameで概ね `0–1 px` 程度だった。

例：

```text
Video 01 right-background ROI:
  representative clean pairs ≈ x -0.08 px / y +0.4–0.5 px

Video 02 right-background ROI:
  representative clean pairs ≈ x 0.0 px / y +0.5 px

Video 06 left-background ROI:
  representative clean pairs ≈ x +0.5 px / y 0.0 px
```

この程度はencoding / subpixel registration誤差の範囲として扱う。

### Strong inference

- interaction中のcameraは**完全固定に近い**。
- head / body / earsのscreen-space移動は、camera追従よりcharacter animation / root movementで説明できる。
- face位置を一定に戻すような明瞭なdynamic camera correctionは確認できない。
- zoom changeを示す背景のscale変化は視認できない。

### Unknown

映像だけでは以下を断定できない。

- internal camera controllerが完全にdisabledか
- camera transformがfloat精度で完全固定か
- subtle subpixel camera motionが内部的に存在するか
- character root translationとcamera translationの内部寄与率

したがってruntime内部仕様は `unknown`。

---

## 11. Cross-video Statistics

### A. Ordinary full-body benchmark only — Video 01 + 06

| Scene | Metric | Median | Min | Max | Practical interpretation |
|---|---|---:|---:|---:|---|
| Neutral | width occ. | 0.645 | 0.617 | 0.672 | default body size |
| Neutral | height occ. | 0.976 | 0.954 | 0.999 | ear/feet clipping込み |
| Neutral | face Y | 0.431 | 0.398 | 0.463 | strongest reusable landmark |
| Typical | width occ. | 0.637 | 0.581 | 0.693 | medium interaction |
| Typical | height occ. | 0.888 | 0.777 | 0.999 | pose依存が大きい |
| Maximum | width occ. | 0.762 | 0.745 | 0.779 | ordinary wide reaction |
| Maximum | height occ. | 0.930 | 0.897 | 0.962 | ears horizontal時など |

### B. Close-framing outlier — Video 02

| Metric | Median | Min | Max |
|---|---:|---:|---:|
| width occ. | 0.836 | 0.820 | 0.924 |
| height occ. | 0.954 | 0.954 | 0.999 |
| face Y | 0.569 | 0.546 | 0.574 |
| left margin | 0.000 | 0.000 | 0.000 |

### Recommended statistical treatment

```text
primary benchmark  = Video 01 + Video 06 ordinary full-body
secondary benchmark = Video 02 close / forward behavior
```

とする。

Video 02をprimary medianへ混ぜない。

---

## 14. Unknowns / Cannot Infer

以下はこの3本の2D映像だけからは決定しない。

推奨calibration procedure：

2. screen-space bbox / face centerを自動計測。
3. `0.58 width / 0.76 height / faceY 0.40`へ合わせる。
4. 最大ordinary Motion setをbatch render。
5. 全frameが `x=0.10–0.90 / y=0.08–0.94` を満たすか検証。
6. 逸脱するMotionだけroot amplitude / framingを局所修正。
7. それでも収まらない場合にのみ3D camera FOV / distanceを再設計。

---

## 15. Evidence Appendix

### Video 01 — full-duration observations

- 冒頭以降、主interaction cameraは同じ背景構図を維持。
- upright earsでは上端clipが繰り返し発生。
- 頭を下げるreactionではtop marginが大幅に増えるが、cameraは追従しない。
- 大きな喜びでears horizontalになるとwidth occupancyが増える。
- feet / lower bodyは長時間screen bottom近傍に置かれる。
- item tray / right-side menuが出てもcharacter root framing自体は変化しない。

Representative evidence：

```text
120.0s Neutral          : width 0.672 / faceY 0.463
30.0s  Typical reaction : width 0.693 / faceY 0.652
70.0s  Maximum ordinary : width 0.745 / faceY 0.372
```

### Video 02 — full-duration observations

- interaction開始後からEeveeが大きく前面へ出たclose composition。
- body / tail / earが左・上・下frame edgeへ継続的にclip。
- high-fiveで前脚が大きく動くが、背景ランドマークはほぼ固定。
- quiet状態へ戻ってもfull-body framingには戻らない。
- したがってこの動画はdefault cameraではなくclose / forward state benchmark。

Representative evidence：

```text
120.0s quiet close   : width 0.820 / faceY 0.546
10.0s  active close  : width 0.836 / faceY 0.569
115.0s widest visible: width 0.924 / true full extent unknown
```

### Video 06 — full-duration observations

- 0s付近はmenu。
- 約4–6sは別構図intro close-upのため除外。
- full-body interaction開始後はcamera/backgroundが安定。
- Neutralではupright earsがtop edgeへ達する。
- ears horizontal reactionでは左右marginが縮み、width occupancy ≈0.78。
- feetは下端近くに固定される。

Representative evidence：

```text
100.0s Neutral          : width 0.617 / faceY 0.398
50.0s  Typical reaction : width 0.581 / faceY 0.403
35.0s  Maximum ordinary : width 0.779 / faceY 0.500
```

### Evidence hierarchy

```text
Observed fact:
  frame pixels / source metadata / visible background stability

Strong inference:
  interaction camera is effectively fixed;
  character motion produces most framing change

Unknown:
  exact internal 3D camera parameters / controller implementation
```

---

## Production Decision Summary

最終採用値：

```text
HEIGHT target      0.76   range 0.70–0.86
WIDTH  target      0.58   range 0.50–0.76
FACE Y target      0.40   range 0.36–0.46
TOP margin min     0.08
BOTTOM margin min  0.06
LR margin min      0.10 / side
```
