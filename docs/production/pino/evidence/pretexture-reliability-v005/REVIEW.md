# Pino C Pre-Texture Reliability v005 — REVIEW

2026-10-17 JST。作業branch: codex/pino-pretexture-reliability-v005-20261017。
出発点: v004 fe39c6d8aab1e550ee31823ca29e85b9b2658632。
共有規則・Goal・Handoffの最終確認元: main 28c1505b7aadf63db25f1be97eba8b99cd332cee。
作業開始時のmain 8b5d13bc38061c0d574444416a039e70b9c61930から進んだ共有規則を再照合し、G1/G2・Pinoの判断に変更がないことを確認した。

**Codexの今回範囲は完了。Human Pre-Texture Gate = PENDING。Human visual GOは未取得。**
次工程はHuman確認後のTripo Texture。実Tripoの4Mesh取込・UV/形状/材質保持・生成品質・返却互換はUNVERIFIED。
今回の限定検証で新たな構造的阻害は検出していないが、G1/G2の承認を技術結果から推定しない。

## 見るもの

- [Canonical / Body-onlyとNeutralの正面・側面・3Q](01-identity-and-neutral.png)
- [Blink/Wink、口開閉の正面・側面](02-face.png)
- [接触・低い休息・尾の仮色とChecker](03-body-checker.png)
- [UV変更donorから画像だけ返却した比較](04-return.png)
- [同じカメラでNeutral→中間→極値→中間→Neutralを再生](diagnostic-cycles.gif)
- [v004 UV](uv-islands-v004.png) → [v005 UV](uv-islands.png)
- [Texture返却契約・次の入力](TEXTURE_CONTRACT.md)

青、クリーム、頬のピンク、眼・口内はCanonicalを参照した**診断用仮色**。完成Texture・承認paletteではない。
Neutralは既存の口を開いたBasis。GIFは3点の姿勢サンプルの往復であり、連続Motionや自然な接地の証明ではない。
Blender Cycles 12 samples + denoiseの描画。Checkerは64px周期。
接触時の腕・脇の伸び、低い休息での腹・足の支持、閉眼の側面厚み、尾の既存殻/小さな暗い割れ目はv004由来のHuman visual HOLD。
休息を「臀部支持の自然な座り」と承認しない。色の大きな誤所有は今回の代表描画では認めなかったが、これらの変形品質はTextureで解決しない。

## UVの診断と必要箇所の変更

v004は5,066 islands、顔・眼も概ね524px/m @4Kで、眼の幅は約55px相当。
継ぎ目の数と眼/頬の描き込み余地が問題になるため、前面Skinの2,194 polygonsだけAngle Basedで展開し直し、3つの顔chartを優先した。
眼の投影/球面展開試行は重なりが出たため採用せず、既存63 chartsの形を保って3倍に拡大。
その他のchartは形状を維持し、全4Meshで共通atlasへ再配置した。Smart UV、Mesh統合、Geometry変更は行っていない。
UV座標は全体で変わるためv004用画像/返却mapとの混用は禁止。

| 診断領域 | v004中央値 px/m | v005中央値 px/m | v005異方性 p95 / max |
| --- | ---: | ---: | ---: |
| 顔 | 524 | 1,790 | 1.157 / 1.747 |
| 眼 | 524 | 2,104 | 1.018 / 1.027 |
| 頬 | 524 | 1,746 | 1.060 / 1.197 |
| 口周囲 | 524 | 1,295 | 1.269 / 1.747 |
| 腹 | 524 | 701 | 1.017 / 1.035 |
| 前肢 | 524 | 701 | 1.019 / 1.049 |
| 尾 | 524 | 702 | 1.018 / 1.034 |

領域は座標による診断maskで、厳密な解剖学的区分ではない。密度はNeutral上のUV面積と実面積から算出。
顔は密度とchart連続性を得る代わりに局所歪みが増した。数値だけで改善と断言せず、顔の色境界・極値描画を併記する。

v005は4,852 islands（main 4,501 / 左右lid 各2 / oral 347）。
UV三角形の面積重なり0、範囲外0、ゼロ面積0。
配置は4Kで外周6px、chartのbounding box間は最低12px。raster上の1/2/4/8pxの軸・対角近傍に他chartを検出しなかった。
これは正確な全segment間距離や全mipでの無漏れを保証しない。2Kでは余白も半減する。
占有は17.08%→47.13%だが、目的は占有率ではなく顔と眼の実効解像度・色の連続性。

## 仮色と画像返却の結果

細い髭chartがsubpixelとなり、pixel中心だけの塗りで青い欠落が出た。
頂点・辺中点・重心の保守的なgutter支持を追加し、元の仮色のSkin継ぎ目15,674辺で20/255超の差は0、最大10.48/255となった。
眼の継ぎ目も20/255超は0。完成模様や高周波の毛、全mipの検証ではない。

ローカルGLB donorで、UV維持と「90度回転＋0.84倍」のUV変更を模擬。
custom ID削除・primitive順変更を含む。材質所有付きのNeutral三角形全体で対応を確定し、画像だけを既存Rigへ接続した。
近傍投影・ray投影・donor Rig/Geometryの採用はしない。
UV維持のSkin/左右眼の三角形中心サンプル差は0。
UV変更時のRGB絶対差平均はSkin 0.030/255、眼L 0.472/255、眼R 0.527/255。
眼の最大channel差p95は2.57/2.59、最大8.06/7.66。Skinの局所最大は42.35。
UV変更返却のSkin継ぎ目は最大21.93/255、20超が2辺残る。再samplingによる色差を「完全転写」としない。

oral 627三角形とlid 12,288三角形の中心は、donorの毒色を使わず材質所有に基づく明示fallbackと完全一致。
fallbackのRGBは診断用であり最終承認色ではない。
3重尾殻はmanifold辺の連結で実際の3面（各1,476三角形）を分離し、殻別sentinelの中心で誤転写0。
全体のoral/lid画像差は意図したfallback置換を含むので、転写品質の誤差として解釈しない。

材質をEye_L→Skinへ変えたdonor、2mmのGeometry変化はHOLD。
未対応の変換階層、Texture transform、非白BaseColor factor等もHOLDとして扱う。
実Tripoが再topology/所有変更する場合は、本ツールの自動返却範囲外。返却時に明示対応を確定するまで既存Rigへ適用しない。

## 保存資産と保護確認

[編集資産](../../../../../assets/grimo/production/pino/candidate-c/pretexture-reliability-v005/README.md)にはplain Master、4Mesh入力GLB、RigレビューGLB、返却map、画像をpackした診断Blendを収録。
仮色・Checker・模擬返却の3画像は未使用でも保存する設定にし、診断Blendの再読込後にpacked画像のSHA一致を確認した。
入力/レビューGLBのPOSITION、NORMAL、skin、morph/normalのbinaryはv004と同一で、変更binaryはTEXCOORDだけ。UV名とmetadataもv005へ同期した。
MasterのBasis、polygon、Shape、Weight、Rig rest/parent、材質所有、normal属性、modifier等を保存前後で照合。
無着色Neutralの同一カメラ正面・側面・3Qはv004に対して変更pixel 0。
Canonical/Body-onlyとv004原本の計9ファイルはSHA一致。v001〜v004や他キャラの資産を変更していない。

再importは4MeshのUV・材質所有を照合。位置差はstatic 0、rig最大0.000000250m、UV差最大0.000000030。
Khronos validatorはstatic errors/warnings 0/0、rig 0/4（v004由来のNODE_SKINNED_MESH_NON_ROOT）。
画像未接続UVのinfoは想定内。最終metadata修正はbinaryを変えず、validatorを最終版で再実行。
v004のmorph-normal bridgeとpose corrective契約は継続。UV以外のpayloadを保持したため全Motion/runtime試験は重複実行していない。
Texture適用後のPlayCanvas/mobile、PBR/normal map、連続接触・全Motionは未検証。

主な機械証拠:
[UV](uv-audit.json) /
[重なり](uv-overlap.json) /
[Master保護](master-preservation.json) /
[GLB同期](delivery-consistency.json) /
[再import](saved-reimport.json) /
[返却試験](return-simulation.json) /
[Validator](glb-validator.json) /
[原本保護](source-protection.json) /
[SHA manifest](file-manifest.json)。

## 再現と停止条件

Blender 5.2.1、NumPy/Pillowを使用。対象のLFS原本を取得する。
scripts/blender/pino-pretexture-v005-uv.py → pino-pretexture-v005.py --inspect --candidate →
scripts/3d/pino-pretexture-v005-atlas.py → delivery.py → simulate.py → return-audit.py →
Blender側 pino-pretexture-v005.py --proof → reimport.py → 3d側 assemble.py の順。
省略名の各Pythonファイルは同じpino-pretexture-v005-接頭辞。raw画像/donorはignored artifacts内に再生成される。
v004監査は候補指定なしの --inspect → atlas.py で生成し、uv-audit.json / uv-islands.pngをv004名で別保存してから候補を検査する。
重なりは既存scripts/3d/pino-uv-overlap.pyのoverlaps関数にsurface.npzのqを渡し、範囲外は同じqの0〜1条件で確認した。

**Human Pre-Texture Gate=PENDINGで停止。**
今回の成果はG1/G2の確認を容易にするTexture入力・返却基盤。実Tripo、課金、完成Texture生成、全Motion修正は行っていない。
