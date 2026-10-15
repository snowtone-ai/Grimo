# Pino C v003 — UV・材質・Rig受渡し契約

**候補状態: HOLD / Human Pre-Texture Gate=PENDING / Texture GO=NO。**
正式Game Neutralは未決定。保存時は承認済みの開いた笑顔Basis。閉口をNeutralへ置換しない。画像Texture、Tripo、最終Motionは今回作成しない。

## 編集原本と対応

- 編集対象: `assets/grimo/production/pino/candidate-c/texture-ready-v003/pino-c-texture-ready-v003-HOLD.blend`。
- 受渡し: 同名の`.glb`。4 mesh、70骨、SkinとMorphを含む。アニメーションは含まない。
- 起点: Face v002 `07ffa41d9079952b6af83e8d70a71cb2da992150`。元FBX/GLB、Rig v001、Face v002を上書きしない。
- MasterとGLBはどちらも4 influenceへ正規化したLBS。元RigのDQは別原本として保護する。DQへ戻して同一結果になるとは扱わない。
- GLBはcornerごとの法線を維持するため頂点を分割する。`_PINO_VERTEX_ID`は各Master meshの元頂点、`_PINO_CORNER_ID`は元loopを指す。GLBの頂点数とMasterの頂点数が等しいことを要求しない。
- Basis、面の順序、UV loop値、材質名の実値とSHAは[delivery-contract.json](delivery-contract.json)、ファイルSHAは[file-manifest.json](file-manifest.json)を正とする。IDを消す最適化や再三角化は別の対応検証が必要。

## 面と色の所有

| Mesh / Material | 所有と禁止事項 |
|---|---|
| `PINO_C_BASE_RIG_V001` / `Pino_Skin` | 頭外面・頬・口吻・鼻・胴・四肢・尾。口周辺も皮膚を所有し、固定した開口、暗い穴、舌を頭へ描かない。鼻や腹などの配色はこのUV上で分けられる。 |
| 同mesh / `Pino_Eye_L`, `Pino_Eye_R` | 原本の左右眼componentに限定。眼色やハイライトを頭や瞼へ重複印刷しない。 |
| `PinoSoftLids_L/R` / `Pino_LidSkin` | 皮膚色の可動瞼。眼面を隠す。新しい眼の輪郭や固定閉眼線を頭Textureへ描かない。 |
| `PinoOralLiner` / `Pino_OralInterior` | 元の口面から切り出した可動内張り。開口部の内側色のみを所有し、閉口時は頭皮の後ろへ退避する。頭側に残した空の同名slotへ面を割り当てない。 |

現物は全slotが原本と同じ無着色placeholder。濃青の眼と暗赤の口はEvidenceと診断viewerだけの一時色。独立した舌面は作っていない。ピンク色を必要とする場合はHumanが位置・必要性を判断してから所有を追加する。

## 同期制御

`c=閉口量[0,1]`、`l=大開口量[0,1]`、`bL/bR=閉眼量[0,1]`。ClosedとLargeは同時加算しない。`S(a,b,x)`は区間[a,b]のclamp付きsmoothstep。

| 対象 | 値 |
|---|---|
| 本体 `PinoMouthClosed`, `PinoMouthLarge` | `c`, `l` |
| 本体 `PinoMouthLift` | `.6*c*(1-S(.75,1,c))`。中間開口の位置補正。Basisと全閉では0。 |
| 口内 `OralClosed`, `OralLarge`, `OralLift` | `c`, `l`, 本体Liftと同値 |
| 口内 `OralOcclude` | `S(.85,1,c)`。閉じ際だけ奥へ退避。 |
| 各側の本体 `PinoEyeRetract_s`, `PinoSkinClose_s` | `S(.9,.95,b_s)`。瞼がほぼ閉じてから眼を沈める。 |
| 各側の瞼、`b≤.9` | `b=0/.5/.75/.9`の順に`Basis/LidHalf/LidThreeQuarter/LidAlmostClosed`。隣接する2形状だけを線形補間。Basisのweightは暗黙の残量。 |
| 各側の瞼、`.9<b<.95` | `LidAlmostClosed=1`、`LidRetreat=S(.9,.95,b)`。眼と瞼を同じ60mmだけ退避し、外周を先に縮めて眼を露出させない。 |
| 各側の瞼、`b≥.95` | `t=S(.95,1,b)`。`LidAlmostClosed=LidRetreat=1-t`、`LidClosed=t`。皮膚内部の瞼から細い閉眼帯へ移行する。他の瞼keyは0。 |

旧`PinoBlink_L/R`は保護のため残すが、この制御では常に0。各meshのtrackを同期して使う。口・眼の制御式は[scripts/blender/pino-texture-ready-v003.py](../../../../../scripts/blender/pino-texture-ready-v003.py)の`state()`を参照。

## 法線・保存・再import

Masterは元のcustom corner normalをBasisで保持し、Geometry Nodesで表情別のnormal差分を加算する。GLBは同じ差分を各Morphの`NORMAL`へ格納する。通常の再exportだけではこれを再現できないため、delivery後に`package-pino-texture-ready-v003.py`を実行する。

Blender標準glTF importはMorph法線を自動で制御しない。再import編集では`pino-texture-ready-v003-reimport.py`の`bind_normals()`がGLB内の値から再構築する。Bridgeなしの陰影一致はFAIL。Skin・Morph NORMAL対応runtimeではGLB自体の値を使用する。任意runtime・スマホでの動作保証へ拡張しない。

## UV凍結の境界

全4 meshが共通の`PinoUV_v003`、0–1の非重複atlasを使用する。UV wire PNGはTexture画像ではない。UVが多数の小島に分かれる点は制作性のHuman確認が必要。数値的な非重複をペイント品質の承認にしない。

Human Gateを通すまでは候補UV。通過後は位置/Basis、頂点・面順序、UV、材質所有を固定し、Morph/Weight/Normalのみで修正可能か先に検証する。両前肢接触・深い低休息は未成立で、必要可動域次第では形状/UVの再検討が残る。現在のUVを本番用に凍結したという意味ではない。

解除条件は[REVIEW.md](REVIEW.md)のHuman判断。閉眼の柔らかさ、口の遷移の本人らしさ、必須の前肢/休息範囲、atlas制作性を承認するまでTexture生成へ進まない。
