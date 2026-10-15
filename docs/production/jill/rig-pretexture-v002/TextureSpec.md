# Jill Pre-Texture v002 — Texture specification / HOLD

2026-10-15。これは入力仕様で、正式Textureでも配色承認でもない。Human承認前のTripo upload・課金・生成を許可しない。

Authorityは `assets/grimo/source/jill/jill-Identity-canonical.png` と承認Body-only front/left/right/back。未承認Motion画像は使っていない。角の色については今回のHuman指示「桃色horn」がCanonicalの淡い角色に優先する。体型、顔、目の大きさ、葉・翼・足・尾の外形はTextureで変更しない。[比較](00-authority-comparison.jpg)。

| 部位 | 指定 | 境界・禁止事項 |
|---|---|---|
| 体・頭・四肢・尾 | Canonicalの柔らかい明るい葉緑。ぬいぐるみ状の穏やかな粗さ | 筋肉線、金属光沢、硬い鱗、焼き込みの強い陰影を加えない |
| 腹・胸・翼膜 | Canonicalの淡いクリーム寄り。緑の骨格・外周と明瞭に区別 | 肩・膜根・葉の裏面を隠す黒塗りで接合不良を覆わない |
| horn | 既存の一対の角を柔らかい桃色。葉や翼の支柱を桃色へ広げない | horn用領域の部位マスクは正式生成前にHuman確認。別形状の角を描き足さない |
| クローバー | Canonicalの大腿のクローバー意匠・位置・葉数と輪郭を維持 | 追加の花、体模様、背景の葉を体へ転写しない。裏側へ勝手に複製しない |
| 葉・首葉・尾葉 | Canonicalの緑の濃淡。根と裏面にも連続した色 | 葉を骨・髪・棘に見せる強いNormal禁止。根を暗くして隙間を隠さない |
| 眼 | 独立した実立体の眼面に濃い緑の眼・瞳。Canonicalの柔らかい印象 | 顔や閉眼面に開眼を印刷しない。ハイライトを過剰に焼き込まず、左右対応を確認 |
| 瞼・口外側・顎 | 体の緑と同じ連続色。閉眼・閉口で外側は肌面 | 開口模様の固定印刷は禁止。閉口面への赤い口内・歯・舌の描画は禁止 |
| 口腔・舌・歯 | 実立体の口腔だけ暗い温かな赤、短い舌は穏やかな桃色、小さな牙はクリーム | 閉口時は内部へ収まる。色でGeometryの貫通・隙間・重複を隠さない |

色名はCanonicalの観察に基づく仕様。数値swatchは未承認なので捏造しない。初回はBaseColorを優先し、Normal/Roughnessは外形・顔・葉の柔らかさを損なわない強さで別評価する。ORMはOcclusion/Roughness/Metalnessの各チャンネルと色空間を返却実物で確認する。BaseColorはsRGB、Normal/ORMは非色データとして扱う。

## UV・隠れ面

Rig正本のactiveは `Tripo_Input_UV`。継承アイランドは `u,v → .006 + .88*(u,v)`、追加面は右帯。元UVは第2層 `v002_Source_UV_Preserved` に保持。継承UVの縮退三角形1枚のみactiveで別の小島に局所補修した。正確な対象は `repair-report.json` の `local_uv_repairs`。

右帯の瞼L/R、口縁/口内、舌、舌端、歯は独立領域。口内・瞼の密度と補間による伸びは [UV checker](05-uv-checker.jpg) でHOLD。入力のニュートラルでは閉眼面・口腔の奥・舌裏・膜裏が十分見えないため、Tripoが全てを正しく塗るとは仮定しない。生成後はこれらの島を部位マスクで同系色充填/転写し、閉眼・閉口・大開口・翼両面で再確認する。checker画像は診断専用で、正式Texture・入力素材として含めない。

## 受入条件

Canonical/Body-onlyと同じ条件の4視点、Front/Side/3Qの顔遷移、翼・葉・尾の裏面、UV継ぎ目を実レンダーで比較する。角桃色とクローバーの配置をHumanが確認する。RigのSkin/Morph/anchorを保つ原本へ画像のみ割り当て、同じ動作を再生する。外観・Geometry・UVに未解消問題があればHOLDを継続する。
