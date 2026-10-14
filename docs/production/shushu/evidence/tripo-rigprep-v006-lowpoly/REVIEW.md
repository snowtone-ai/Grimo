# Shushu v006 — offline lowpoly / Auto Rig入力候補

2026-10-14。branch `codex/grimo-motion-zero-based-design-20261011`、開始HEAD `6805096e811246401599651cbfaa9fc23834e459`。**今回のHuman明示「v006静的外観PASS」をAuthorityとする。旧v006 REVIEW/HandoffのPENDINGは履歴であり、現承認を上書きしない。** Canonical・承認済みBody-onlyを確認。新しいlowpolyのHuman承認とTripo受入は未検証。

## 成果と判断

- [別名GLB：shushu-v006-rigprep-lowpoly-v001.glb](../../../../../assets/grimo/production/shushu/tripo/geometry-v003/rigprep/shushu-v006-rigprep-lowpoly-v001.glb)
- **523,683 → 99,565 triangles（80.99%削減）**。26,733,860 → 6,071,060 bytes。55,187頂点、12メッシュ/材質/Texture。Rig・skin・animationなし。
- 入力SHA256 `9c479122232170f65a0f5976cf2c07180cf342c08f37a95d50b53a90ff34f10f`
- 出力SHA256 `780f1f9c3ebd6a39050500398f190ff21e6c18c7de4c7c0730040ab1cdf41309`

meshoptimizer 1.2.0の属性考慮simplificationを直接使用。頭部88,639 → 63,619面、胴体408,376 → 9,278面。他10メッシュは全三角形の位置/法線/UVを一致させた。顔・チーク・頭部下端の60,176面を固定し、瞳・目囲み・笑顔/舌・耳下の毛境界を優先。胴体は足首/膝/股/肩付近の断面を保護。全体を再構築せず、元頂点の選択と接続削減のみ。元の12画像の圧縮バイト、材質/Texture/ノード設定は完全一致。UV転写・Texture生成・法線再計算なし。純正GLB、追加の圧縮拡張なし。

## 保存再読込・同条件外観

保存GLBを独立PythonとBlender 5.2.1で再読込。[保存検査](saved-glb-checks.json)、[削減記録](reduction.json)、[glTF Validator](gltf-validator.json)：有限/単位法線、UV、全三角形非退化、保護991入力hash一致。最初の9k胴体試行では足首に退化1面が生じた。面除去は境界を開くため棄却し、半径0.007の元局所を追加固定して再削減。最終は退化0、新しい境界/非多様体辺の増加0、胴体は境界0/非多様体0。元Headの境界675/非多様体62、およびまぶた壁・口内の開いた境界は継承している。全体watertightの証明ではない。

正面・左右3/4・左右側面を全身の元材質照明768²と顔のbase-color emission 1024²で比較。瞳正面・口正面/左右側面を元材質照明1024²で比較。カメラ、照明、露出、samples=16、seed=0は一致。[原寸14組](renders)、[カメラ/出力hash](candidate-render.json)、[画像差](image-differences.json)。

- [全身5方向：v006 / lowpoly / 差分×8](01-body-five-view-comparison.png)
- [顔5方向](02-face-five-view-comparison.png)
- [瞳・口アップ](03-eyes-mouth-closeup-comparison.png)

比較ボードと原寸を実際に確認し、**Codexのv006に対する静的外観保持評価はPASS**。花柄/ハイライト、ピンク目囲み、チーク、笑顔/舌、耳下〜肩の境界、腕脚の曲線に明確な崩れなし。頭頂/後頭部と胴/足の輪郭には微小な差がある。顔5方向の平均絶対RGB差は0.065〜0.090/255、全身は0.115〜0.178/255。正面の左右瞳cropは0.00089/0.00107、口cropは0.00983/255。画素完全一致とはしない。照明画像の差には間接光とray samplingも含む。参照に見える既存の口内帯・側面口形状は改造していない。

## Rig適性と未検証

Y-up、正面+Z、足底Y=0、身長1.0の立位を保持。左右腕は独立した閉メッシュ、脚の下部Y<0.13には横方向0.064575単位の隙間。関節高さ±0.0125の帯には213〜663頂点、胴体edgeの95%は0.02859単位以下。ただし腕と胴の投影範囲には重なりがあり、元の下げた腕のA-like姿勢を維持している。関節帯の数値はスキニング/変形合格を意味しない。

[Tripo公式Help](https://www.tripo3d.ai/help/features/is-it-possible-to-upload-my-existing-model-for-animation)は人型のTポーズを案内。2026-10-14の公開公式Help/Auto Rig/API資料でStudioの正確な三角形上限は確認できなかった。生成/Retopologyのface_limitをRig上限へ流用しない。**人型/Mixamoへの受入、頭部既存構造の適合、Rig変形はUNKNOWN。** 外部Tripo操作・upload・課金・Rig生成なし。もし上限や姿勢で拒否される場合、実際の制限を確認してから、腕の入力専用Tポーズ調整または顔固定領域を狭めた属性考慮削減を別候補で検討し、同じ外観Gateを再適用する。

v006原本、歴代候補、v003 Blender/Shape Keys/285f proof、他キャラ、開始時のユーザー画像3差分と未追跡proof資料は不変。アプリ/正式Geometry採用なし。全体build/網羅的testなし。

## 再現

`node scripts/3d/simplify-shushu-v006-rigprep.mjs` → `python -B scripts/3d/check-shushu-v006-rigprep.py`。factory Blenderで `scripts/blender/review-shushu-v006-rigprep.py` を基準、および `-- --candidate` で各実行 → `python -B scripts/blender/board-shushu-v006-rigprep.py`。正式blendは開かない。commit/pushの最終HEADはGit照合して報告する。
