# Shushu v004 — Motion Ready 再審査候補

**判定：Human外観HOLD／PC技術確認済み（下記範囲）／スマホUNKNOWN。** 元v003の腕・口・腹は今回のHuman FAILとして扱う。新候補の可愛さ・自然さ・承認外観との一致を自己承認しない。原本置換・Motion量産HOLD。

[原寸画像と3経路の連続比較](index.html) ／ [原因・棄却案](METHOD.md) ／ [再現](REPRODUCE.md) ／ [hash対応](delivery-manifest.json)

制作branch：`codex/shushu-abc-motion-repair-v004-20261017`。元branch `codex/shushu-v004-motion-ready-v003-20261016` の `56ffdc6356c8b3367990d30d6b50d6fcc011126e` から隔離。原本・他キャラ・ユーザー差分は編集せず、別名assetとv004 loaderだけを納品する。

## 修正

- **腕：** Spine2は搬送として残し、左右各438 Shapeの形状生成を肩の小回転＋分布する肘曲げ＋厚みを運ぶ中心線へ再設計。Purpose中間の実形状も再構成。旧whole-arm移動や単純endpoint合わせを棄却した。Hold Anchorは一定前方offsetから姿勢面の法線offsetへ実修正し、v004 loaderと対にした。
- **口：** 古いHead.MouthCloseによる顎側の二重加算を除去。W境界256頂点は全Shapeで差0、鼻下紐なしを維持。口内・OralBowl・舌と複合表情の閉→開→閉を確認した。
- **腹と全身の凹凸：** 発生Torso三角形とTrueSeat補正を特定し、実posed面とcorrective変位場を修復。頭・両耳・胴・両前肢の細かな面も保護mask付きで修正し、全14Meshを検査対象にした。追加の強い平滑化は輪郭を悪化させたため棄却。形状修正後に法線を再計算し、UV・画像・色・topology・weight・骨rest/parentは保存した。Basisには意図した局所修正があるため、中立同一とは主張しない。

元スクショの整数秒から一意のframeは断定できない。[SOURCE](SOURCE.json)に元動画hash、時刻範囲、実制御値、前後姿勢を残した。f1089/1101/1113と隣接遷移を中心に比較する。

## 検証結果

| 確認 | 最終候補の結果 | 限界 |
|---|---|---|
| 全身/口 | 14Mesh×12状態、口81段階、W全境界/全key差0 | 有限値や保存座標は美観GOではない |
| 腕の制御格子 | 左右264件、Torso/Headで確認されたdistal内部点0、無効driver0 | 内部付け根は意図した接合。任意全連続入力の証明ではない |
| 接触球/Anchor | 半径0.030球の最小余裕 0.000337887H、author Anchor差最大 8.7e-08H | 任意の小物形状は未検証 |
| 保存GLB | 14Mesh位置差最大 9.23e-07、7 Anchor行列差 8.94e-07 | 固定UV対応/選択姿勢で照合 |
| 実三角形接触 | 保存GLBの左右102件でdistal交差0 | BVH＋segment検査、意図したroot接合は除外 |
| PC製品raw入力 | 27姿勢、CPU現在面の位置 4.38e-07、法線成分 5.04e-06、7 Anchor 3.2e-05 | engine 2.22.2、640px、PC。実機性能へ拡張しない |
| GPU readback | f1089/1113のTorso＋2 Paw、6件でGL error 0。raw位置 8.3e-05、法線 0.0362° | GPU Morph精度を含む。skin-only差 8.15e-08 |
| 割込み解除 | raw overrideを解除してclipへ戻り位置/Anchor差0 | Purpose/Wrist/Seatの既存呼出契約 |

前腹部の同じ辺を各version自身のBasis長で正規化した比較は[実形状比較](physical-surface-comparison.json)。腹の変位場の逆LBS目標再評価差は最大 5.94e-08H。[GPU readback](pc/gpu-1089.json)、[製品入力](pc/product-raw-controller.json)、[lifecycle](pc/lifecycle.json)、[全身inventory](all-mesh-surface-audit.json)を併記する。体積proxyは 0.991〜1.153であり、自然な厚みを自動承認する指標ではない。

Blender author・GLB再読込は原寸640pxの前/横/左右3Q、背面/上面、口拡大と157枚連続24fps。PC収録は診断Viewerから実製品loader/controllerへ切替後の原寸画像・実時間動画。左右、Purpose中間/極限、Wrist、立位/座位、顔＋保持/割込み/復帰を含む。過去のXiaomi記録を新候補のPASSに流用していない。ADB/実機操作なし。

## Human確認と残るGate

1. Canonical/承認済みv004と比べ、顔・眼・W・耳・短肢・足・腹・色の同一性と可愛さを保てているか。
2. 肩から肘、手先まで肉と厚みが自然につながり、中間でも硬い塊に見えないか。左右差・頬下の余裕・保持の向きも確認する。
3. 閉口/微開/開口/舌/複合表情で顎と下口縁が一体に見えるか。保持/割込み/復帰の一瞬も確認する。
4. 指摘部以外も含む頭/頬/耳根/背中/脇/腹下縁/足/前肢の不要な凹凸が残らないか。意図したplush volumeとの区別はHumanが判定する。未観測の組合せで見つかった欠陥も修正対象であり、全連続空間の無欠陥は宣言しない。
5. 臀部支持と足の前出し、重さ、接地、座位からの復帰が自然か。

**旧arm FKは引き続き未対応**（[実検査](legacy-fk-contract.json)）。Purpose/Wrist/Seatを使用する。全画面採用、任意小物、スマホ性能/熱/GPU時間は今回未検証。新候補のスマホ再検証は後続GateのUNKNOWN。

共通知識はmainへ独立commit `8b5d13bc38061c0d574444416a039e70b9c61930` で[1fileへ統合](https://github.com/snowtone-ai/Grimo/blob/main/docs/grimo/knowledge/character-production/GRIMO_CREATURE_DEFORMATION_AND_MOTION_PRINCIPLES.md)。観察/公式出典/推論/未検証を区別した。その後のmainのCarol廃止編集は保持し、古い4キャラ行を復元していない。
