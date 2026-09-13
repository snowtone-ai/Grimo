# Grimo Asset Manifest — Human-authored Reference Set

更新: 2026-09-13

## Rule

- `canonical` = 唯一のidentity正解
- 生成した8画像 = implementation reference
- 補助画像間で矛盾した場合はcanonicalへ戻る
- 補助画像の新規デザイン要素をcanonicalへ逆輸入しない

## Status

ユーザー確認:
- Carol: 8/8 完了
- Jill: 8/8 完了
- Pino: 8/8 完了
- Shushu: 8/8 完了

合計: **32/32**

## Physical import status

2026-09-13: all 32 implementation references were imported into the repository at
`assets/grimo/source/<character>/refs/`, using the filenames in `manifest/assets.json`.
The four existing `canonical.png` files were preserved unchanged. The companion
reference notes are in `docs/grimo/references/`.

## Per-character asset contract

各キャラに以下を持つ:

| No. | Filename | Purpose |
|---|---|---|
| 00 | `canonical.png` | identityの唯一の正式基準 |
| 01 | `01-rig-neutral.png` | deformation / pivot / part構造の基準 |
| 02 | `02-opposite-3q.png` | 反対側・隠れ構造の補助 |
| 03 | `03-occlusion-parts-sheet.png` | 完全形パーツ / occlusion補完 |
| 04 | `04-expression-sheet.png` | facial preset |
| 05 | `05-facial-components-sheet.png` | blink / eye / mouth等の構成要素 |
| 06 | `06-reaction-keyposes.png` | reaction peak/key pose |
| 07 | `07-layer-separation-sheet.png` | z-order / layer decomposition |
| 08 | `08-touch-map-reference.png` | touch zone設計 |

## Recommended repo layout

```text
assets/grimo/source/
  carol/
    canonical.png
    refs/
      01-rig-neutral.png
      02-opposite-3q.png
      03-occlusion-parts-sheet.png
      04-expression-sheet.png
      05-facial-components-sheet.png
      06-reaction-keyposes.png
      07-layer-separation-sheet.png
      08-touch-map-reference.png
  jill/
  pino/
  shushu/
```

派生runtime assetはsourceと分離:

```text
assets/grimo/derived/<character>/
public/grimo/<character>/
```

## Touch-map color semantics

- GREEN = 好き
- YELLOW = 普通
- RED = 嫌い
- CYAN = 特殊Reaction
- GRAY = 入力除外

実装では色pixelそのものをruntime hit-testへ直接使う必要はない。  
画像は視覚的source of truthであり、Codexがpolygon / mask / semantic zoneへ変換してよい。

## Asset QA

各補助画像をruntimeへ使う前に:
- canonicalと同一個体か
- 目/瞳ハイライト
- head/body ratio
- palette
- unique motif
- 左右パーツ数
- anatomyとatmosphereの混同
- 透明境界
- 生成artifact
を確認する。

不一致assetは「生成済み」でも採用しない。
