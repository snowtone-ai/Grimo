# 操作と再現

`shushu-v006-production-rig-v001.blend`を別途開く。Rig選択→Object Properties→Custom Properties。Neutralは全numeric property = 0。保存されたsourceはdriver/constraintを保持し、`-proof.blend`には能力系列のmarkerと操作値Actionがある。既存の開いているユーザーBlender sceneを上書きしていない。

| 制御 | 範囲 / 意味 |
|---|---|
| HeadYaw / Pitch / Roll | -1..1。yaw ±18°、pitch/roll ±12° |
| NeckPitch / Ear.L/R | -1..1。neck ±10°、耳 ±12°。Restに小低頭が付加 |
| Blink.L/R | 0開眼、0.5半目、1全閉。左右独立 |
| GazeX/Y.L/R | -1..1、左右独立。全閉の隠れphaseだけ眼球の視線変形を抑制し、再開時復帰 |
| Smile / Joy / Surprise / Hesitate / Discomfort | 0..1の小さな感情layer。任意の全layer最大同時加算は未検証 |
| MouthClose / MouthOpen / Tongue | 0..1。CloseがOpen/Tongueに優先。Neutralには元のv006の描かれた口/舌がある |
| CheekPressure.L/R / BellyPressure / Breath | 0..1。左右頬・前腹・小呼吸の局所形状 |
| Seat / Rest | 0..1。Seat=1は低い臀支持姿勢。Restは眠気/低頭layerで、Game Neutral決定ではない |
| WeightShift | -1..1、骨盤X ±0.024。両足targetはworldに固定 |
| FootLift.L/R | 0..1、最大0.040上げ。実証では先に反対側へWeightShift |
| FootSide/Forward.L/R | -1..1、最大±0.025。足向きはCTRL_Foot.L/Rのrotationで編集。実証支持domain以外は再検査 |
| Offer / Hold / SelfContact.L/R | 0..1。**各Pawで一つのreach目的を選ぶ**。左右は別目的を併用可能。保持と反対側接触を実証 |
| Wrist.L/R | -1..1、小さな手の向き。±約20° |

骨のBody / Head / Left arm / Right arm collectionを分け、互換finger骨を非表示にしている。Spine/Hips/腕/腿/膝はFK編集可能。ただし足骨はworld pin制約に従うため、足はプロパティ/CTRL_Footで操作する。FKやtarget rotationを直接編集した場合、Neutral復帰にはそれらも保存時の姿勢へ戻す。任意FKで支持を崩した場合はRigの自動床保証範囲外。

7 Anchor：`ANCHOR_Hold.L/R`（現Paw面から校正した半径0.030fixture中心）、`ANCHOR_Crown`（head所有の冠参照）、`ANCHOR_WearEar.L/R`、`ANCHOR_WearChest`、`ANCHOR_Mouth`。新規itemのgeometry/clearanceを検査して使用する。body-owned Anchorをruntimeで再評価する実装は今回含まない。

以下をrepo rootで実行する。Blender 5.2.1 LTS / Python 3.13 / numpy / Pillow使用。buildは別名候補だけを上書きし、保護入力hashを検査する。再生成した成果を既存のHuman承認と解釈しない。

```powershell
$taskBlender = 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe'
& $taskBlender -b --factory-startup --python-exit-code 1 --python scripts/blender/build-shushu-production-rig-v001.py -- --extract
& $taskBlender -b --factory-startup --python-exit-code 1 --python scripts/blender/build-shushu-production-rig-v001.py -- --build
& $taskBlender -b --factory-startup --python-exit-code 1 --python scripts/blender/prove-shushu-production-rig-v001.py -- --audit
& $taskBlender -b --factory-startup --python-exit-code 1 --python scripts/blender/prove-shushu-production-rig-v001.py -- --proof
& $taskBlender -b --factory-startup --python-exit-code 1 --python scripts/blender/prove-shushu-production-rig-v001.py -- --fixture-check
python scripts/3d/report-shushu-production-rig-v001.py --restore
& $taskBlender -b --factory-startup --python-exit-code 1 --python scripts/blender/prove-shushu-production-rig-v001.py -- --roundtrip
& $taskBlender -b --factory-startup --python-exit-code 1 --python scripts/blender/prove-shushu-production-rig-v001.py
& $taskBlender -b --factory-startup --python-exit-code 1 --python scripts/blender/prove-shushu-production-rig-v001.py -- --names head-left,head-right
& $taskBlender -b --factory-startup --python-exit-code 1 --python scripts/blender/prove-shushu-production-rig-v001.py -- --approved
& $taskBlender -b --factory-startup --python-exit-code 1 --python scripts/blender/prove-shushu-production-rig-v001.py -- --reimport --names neutral,closed,seat,seat-rest,hold-L-touch-R,seat-hold-interrupt,tongue,mouth-open-max,mouth-close,mouth-close-override,neutral-return
& $taskBlender -b --factory-startup --python-exit-code 1 --python scripts/blender/prove-shushu-production-rig-v001.py -- --fixture --names hold-L,hold-L-touch-R,seat-hold-interrupt,hold-resume,release,neutral-return
python scripts/3d/report-shushu-production-rig-v001.py --boards
python scripts/3d/report-shushu-production-rig-v001.py
```

各commandのexit code 0を確認する。`--restore`は元画像バイト・材質定義の復元と監査を行う必須工程。原数値buffer viewを変更せず画像を再packし、14mesh中の元12materialを復元する。GLBはSkin、Morph、Animationで再importした結果を確認してから採用する。保護manifestには、この作業checkoutのユーザー未追跡ファイルも含む。別checkoutでそれらが欠ける場合、保護照合は失敗するため、同じ保護範囲を用意して実行する。

比較画像は同一camera/light/world/floor/640×640/24samples。板は原寸画像の縮小・並べ替え・ラベルのみで、生成AI/retouchによる身体補修をしていない。外部資料・画像生成は今回不要と判断した。
