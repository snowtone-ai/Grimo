# Shushu v003 — 側面の口 / v006改善候補

2026-10-14。開始HEAD `d9704fa36050c138594651709dd6d0d5e7944f0b`、branch `codex/grimo-motion-zero-based-design-20261011`。**技術検証PASS、外観完了は未達。v006は未採用の比較候補、Human Gate=PENDING。**

## 問題と保存した変更

承認済みBody-onlyでは、側面でも丸い開口・舌・下側口縁が見える。v005では口が薄い斜めの赤線へ潰れる。保存GLBを調べると、開口と舌は主にHead Textureの描画で、独立MouthInteriorは上縁付近の浅い帯だった。口角に続く頬の断面による遮蔽が主要因と判断した。参考資料とこの判断の区別は[RESEARCH.md](RESEARCH.md)に記録した。

独立v006では、Headの口角〜隣接する頬/顎の奥行きと、対応するMouthInteriorの奥行きだけを滑らかに後退させた。中心の口と正面の幅/高さを維持し、既存法線を局所変形に追従させた。Headの実座標変更12,254頂点、法線マスク12,266頂点、最大奥行き変更0.0148775 GLB単位。MouthInteriorは44頂点。詳細な頂点マスクと境界は[geometry-validation.json](geometry-validation.json)。新規口腔やトポロジーは追加していない。

- [保存GLB v006](../../../../../assets/grimo/production/shushu/tripo/geometry-v003/texture-cleanup/shushu-geometry-v003-tripo-mouth-candidate-v006.glb)
- SHA256 `9c479122232170f65a0f5976cf2c07180cf342c08f37a95d50b53a90ff34f10f`
- 比較元v005 SHA256 `a9c1681c5c245d15e0266002c2a618d607d1f6844cfe2bbecfa97827ca536982`
- 元GLB SHA256 `338ad5f8c67906917579ddbb804a4f7f51d8fec6c42328bb545adc87c1bf077b`

## 実画像による判断

保存v006を独立に読み込み、同じカメラの正面・左右3/4・左右側面・左右67.5度、計7角度をv005と比較した。1024²原寸レンダーと拡大比較を実際に開いた。元の材質を使った768²の同条件照明5角度も確認した。参照には承認済みBody-only左右とCanonical Identityを使った。

- [7角度：v005 / v006 / 差分×4](01-seven-angle-before-v006-difference.png)
- [左右の拡大：承認済みBody-only / v005 / v006](02-reference-mouth-closeups.png)
- [元材質・同条件照明5角度](03-shaded-five-angle-before-v006.png)
- [棄却した強い変形と陰影の問題](04-rejected-trials.png)
- 原寸は[renders](renders)、照明付き原寸は[shaded](shaded)。比較画像は切り出し・等方拡大・配置のみ。モデル画像の修整はしていない。

正面の花柄の瞳・ハイライト・ピンク目囲み・チーク・笑顔は保持され、斜めの笑顔も可愛い。左右の側面では上側口角の曲線と開口が見えやすくなった。最終候補の顎側には、先行試作で現れた明るい段差が見られない。

ただし、**真横の下側口縁はまだ参照より細く、下端が尖って見える。参照の丸い開口と舌の見え方までは再現できていない。** 元材質の照明では上縁付近の浅い別メッシュの帯も見える。これは全方位で自然な立体口腔を確立した結果ではない。参照は2D画像で、完全に校正された投影ではないが、この見た目の差を投影差だけとしてPASSにはしない。「不自然さなく100%可愛い」の完了条件は未達として保存する。

奥行きを強く変えた試作は、3/4の奥側口縁や舌が隠れたため棄却した。急な法線変化や顎側の補間端による陰影も棄却し、滑らかな断面を取り直した。v006はその改善を比較できる候補に留める。今後の修正では、側面の下側口縁の丸みと、3/4で奥側口縁が残ることの両方を満たす必要がある。新しい口腔・Rigの導入へ無断で範囲を広げない。

## 対象別検証と保護

[targeted-checks.json](targeted-checks.json)は保存後のGLBを独立に再読込して検証した結果。

- X/Y座標・UV・全12 Textureの圧縮バイト・インデックス・GLTF JSON（材質/ノード/メタデータを含む）一致。局所位置/法線マスク外の変更バイト0。他10メッシュの属性一致。
- 正面の両目領域は画素一致。正面全体は30画素だけ、最大RGB差3/255。カメラ条件一致。口元のサンプリング差を完全一致とは記載しない。
- 変更面は非退化、正面の符号付き投影不変、法線は有限かつ単位長。変更面の最小面積比はHead 0.0252。全方向の自己交差や将来のRig変形安全性を証明する値ではない。
- 保護949入力のSHA256一致。元GLB・v001〜v005・正式Blender Geometry/Rig/Shape Keys・285f proof・他キャラ・既存ユーザー差分を保持。正式資産の置換はない。
- 全体build/test、外部Tripo、課金、mainマージは実施していない。静的候補の局所検証であり、Motion/runtimeの完成判定ではない。

## 再現

repo直下で `python -B scripts/3d/adjust-shushu-mouth-depth-v006.py --output assets/grimo/production/shushu/tripo/geometry-v003/texture-cleanup/shushu-geometry-v003-tripo-mouth-candidate-v006.glb`。

同じrepoの `scripts/blender/review-shushu-tripo-texture-v003.py` を `--render --eye-config docs/production/shushu/evidence/tripo-mouth-depth-v006/repair-config.json`（比較元）および末尾に `--asset assets/grimo/production/shushu/tripo/geometry-v003/texture-cleanup/shushu-geometry-v003-tripo-mouth-candidate-v006.glb`（候補）で実行する。元材質照明は `scripts/blender/review-shushu-mouth-shaded-v006.py` の比較元と `--candidate`。Blender CLIではスクリプト引数を `--` の後に渡す。最後に `python -B scripts/blender/board-shushu-mouth-v006.py`。Blenderは別プロセスのfactory sceneで読み込み、正式作業シーンを開かない。
