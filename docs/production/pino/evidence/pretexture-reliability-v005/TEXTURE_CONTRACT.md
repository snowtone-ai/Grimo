# Pino v005 — TEXTURE_CONTRACT

**Human Pre-Texture Gate: PENDING。実Tripo互換: UNVERIFIED。**
Human確認後の次工程はTripo Texture。4Mesh対応は今回の前提で、実サービス上の取込は操作していない。

## 次に使う入力と保存資産

Tripo Textureの入力は次の1ファイル:
[**pino-c-v005-tripo-input.glb**](../../../../../assets/grimo/production/pino/candidate-c/pretexture-reliability-v005/pino-c-v005-tripo-input.glb)

同じディレクトリに保存したもの:

| ファイル | 用途 |
| --- | --- |
| pino-c-pretexture-v005.blend | 編集用の既存Rig Master。画像未適用。返却先の正本 |
| pino-c-v005-tripo-input.glb | Neutral、4Mesh、Rigなし、画像なし。次のTexture入力 |
| pino-c-v005-rigged-review.glb | 4Mesh、既存skin/Morphを保持したレビュー用。Tripo入力にしない |
| pino-c-v005-return-map.npz | v005のloop/vertex/UV/所有対応。v004 mapと混用禁止 |
| pino-c-v005-diagnostic-proof.blend | 仮色・Checker・模擬返却画像をpackした診断用。完成Textureではない |

4MeshはPINO_C_BASE_RIG_V001、PinoSoftLids_L、PinoSoftLids_R、PinoOralLiner。
5つの使用材質はPino_Skin、Pino_Eye_L、Pino_Eye_R、Pino_LidSkin、Pino_OralInterior。
Skin/左右眼はmainのface材質で所有、lidsとoralは別Mesh。未使用slotは原本のまま。
mapのmesh indexはmain、L lid、R lid、oralの順。GLBのnode順をこの番号と同一と仮定しない。
共通UVはPinoUV_v005。材質/頂点/cornerの既存IDは保持するが、実TripoがIDを返す保証はない。

## 画像だけ返す手順

1. 実donorを新しい保存先へ退避してSHAを記録。入力GLBとMasterを上書きしない。
2. Neutral位置、三角形、材質所有、UV、画像設定を照合する。Mesh数だけで返却可能とは判定しない。
3. UV維持なら元の所有材質にBaseColor画像を接続。UV変更なら下記の対応確認/再samplingを使う。
4. Masterのコピーで既存材質のBaseColorにsRGB画像を接続し、Geometry/Rig/Weight/Morph/normal/所有を保持する。
5. [REVIEWの代表描画](REVIEW.md)と同じNeutral、瞬き/Wink、口開閉、接触、中間、休息、尾で色境界/伸びを再確認。最終画像とレンダリングはHumanが判定する。

対応確定は「材質名 + 三角形の全3頂点」の一致。1µm量子化keyと頂点距離検査を用いるため境界付近では保守的にHOLDとなる。
custom ID欠落、頂点split、頂点/primitive並べ替え、UV変更はこの対応が確定する場合に処理可能。
三角形不足/追加、曖昧な重複、再topology、形状移動、材質名変更/merge、非identity階層変換、posed/skinned donorはHOLD。
近傍面に自動投影しないため、口内や近接した3重尾殻へ取り違えない。
対応が取れない実donorはTexture返却時に所有/殻別の明示対応を確定する必要がある。既存Rigをdonorで置換しない。

repo rootで次のCLIを使う（PythonにNumPy/Pillowが必要）:

~~~powershell
python scripts/3d/pino-pretexture-v005-return.py --source assets/grimo/production/pino/candidate-c/pretexture-reliability-v005/pino-c-v005-tripo-input.glb --donor "<saved-donor.glb>" --output "<returned-basecolor.png>" --size 4096
~~~

PNGと同名stemの.return.jsonにsource/donor/output SHAと対応範囲を保存する。
入力はGLB内のembedded画像または同じ保存先以下のlocal画像。ネットワーク取得や親フォルダ参照はしない。
対応するのはTEXCOORD_0、Texture transformなし、白のBaseColor factor、opaqueのstandard BaseColor画像だけ。
factor/alpha/拡張の見た目を焼き込んだと推定しない。未対応設定は別途検証/正規化するまでHOLD。
PBR/roughness/metallic/normal map返却は未検証。

## 隠れ面と材質所有

oralとlidsにはdonor色を転写せず、既存所有に基づく明示fallbackを返す。
診断ではoral RGB(57,27,39)、lid RGB(150,201,242)を使い、毒色が混入しないことを確認した。
これは承認paletteではない。実Texture返却ではCanonical/承認色をHuman確認したうえでfallbackを設定し、口開閉と閉眼で確認する。
3重尾殻は対応する三角形を別々に扱う。近接距離やrayの最初のhitで殻を決めない。
MeshやRig、shape key、材質所有、normal bridgeをdonorから持ち込まない。

## 残る限界とgate

4Kで外周6px、chart間最低12px。低解像度とmipでの漏れを保証しない。高contrast/細線は再samplingで損失が出る。
模擬UV変更ではSkin継ぎ目の20/255超が2辺、局所色差も残る。実Textureで描画確認が必要。
実Tripoの4Mesh受理、topology/UV/材質保持、生成模様品質は未検証。ローカル模擬donor成功と区別する。
v004のmorph-normal bridge / pose corrective契約は継承。Texture適用後のruntime/mobileや自然な連続Motionは別gate。

**このcommitはTexture開始のHuman承認ではない。Human Pre-Texture Gate=PENDING。**
