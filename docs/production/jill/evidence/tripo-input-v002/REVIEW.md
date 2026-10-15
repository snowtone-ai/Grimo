# Jill v002 — Tripo基礎Rig投入準備

2026-10-15。**Geometry Gate HOLD / Human visual PENDING**。基礎Rig試験のためのローカル投入候補と検証計画。Tripo操作・upload・クレジット消費0。正式Rig・Texture・Motion・runtimeは未制作/未検証。

## Authority / 系譜

開始HEAD `709cddb570fa806112139161a6b3084c51665425`、branch `codex/jill-smartmesh25k-inspection-20261015`、Jill worktree clean。共有workspaceはShushu作業中のため使わない。取得確認したmain `8e4996c63c6d8fbb41954a2aa5cb5d892e45f01b` のAGENTS / Goal√map / Handoff、Jill HANDOFF / [v002 REVIEW](../smartmesh25k-v002/REVIEW.md)、[Canonical・承認Body-only4方向の比較板](../smartmesh25k-v002/boards/00-authority-v002.jpg)を確認。

最新Human判断：**基礎Rig → BlenderでRig/Geometry共同調整 → Texture → 最終調整**。今回の投入準備はGate解除、Tripo実行、形状変更の許可ではない。task → G3骨格を使った局所再評価 → G2翼/葉/尾/前肢の独立した生命感 → G1可愛さ・本人性 → G0再訪したくなる体験。静的数値の改善で外観を損なわない。

唯一の編集系譜は `smartmesh25k-v002/jill-geometry-master-v002.blend`。正本を保存せず背景Blender 5.2.1で開き、frame 1・全診断キー0・Basis一致を確認。メッシュのメモリ複製からShape Keys、animation、vertex groupsを除き、メッシュ1個だけを選択出力。非表示原本、除去板archive、camera、TEST_ONLYデータを投入しない。全身再構築・比率/Neutral座標/面編集、正式Textureなし。

## 投入候補とローカル検証

資産位置：`assets/grimo/production/jill/tripo/smartmesh25k-v002/tripo-input/`

- **推奨 `jill-v002-neutral-tripo.fbx`**：DCC往復、元のpolygon構成を保つ。Y-up / -Z forwardへの形式変換、global scale 1、unit適用、mesh modifiers/animation無効。
- **予備 `jill-v002-neutral-tripo.glb`**：単一ファイル、Y-up、skins/morphs/animations/extras無効。glTF仕様により三角化され、頂点が法線等で分裂し得る。編集正本への昇格不可。

正確なbytes / SHA256 / bounds / 往復差 / 構成は [roundtrip.json](roundtrip.json)。[再現script](../../../../../scripts/blender/prepare-jill-v002-tripo-input.py)。通常の投入時は再実行不要。派生ファイルを上書きするため、後続Human編集後に無条件で再実行しない。

最終検証はfactory-empty sceneから各1回再読込（先行試行はGLBの孤立頂点差のassertで停止、最終記録はその区別を修正した実行）。FBXは28,050頂点 / 28,809面 / 54,361三角形換算、world全頂点差0、polygon座標集合（小数6桁）一致。GLBは28,059頂点 / 54,361三角形、面使用頂点の両方向差最大2.666e-7 model unit。元に面未使用16頂点があり、GLBは省略するため全頂点基準では0.082711の差になる。FBXはこれをそのまま保持し、面のない16頂点は除去板の面混入ではない。GLBは三角化/法線等で頂点分裂もあり、編集面構成保持を意味しない。

両候補mesh object 1、Armature/actions/Shape Keys/vertex groups/modifiers/images 0。GLBはJSON payloadからskins/animations/morph targetsなしも確認。入力はUV0・画像0・元1材質であり、正式な緑色Textureや眼表現は含まない。原本/v001/承認参照等219ファイルとv002正本の計220ファイルのSHA256不変。FBX 1,062,508 bytes / GLB 1,000,880 bytes。正本Neutral・面を編集していない。

同一camera・Workbench・480pxで正本Neutralと再読込FBX/GLBのfront/side/3Qを描画。[比較板](roundtrip-board.jpg)。向きはBlender world +Z up、顔は-Y側。スケールと位置は元のまま。実寸のデザイン承認やStudio側の自動スケール保持はUNKNOWN。

Codexが比較板を開き目視。今回の3方向では全身silhouette、顔/眼/口、足、翼膜、首葉、巻尾の位置と体積に出力由来の目立つ差を認めなかった。側面腹/尾根の陰影境界や浅い眼など元の見え方も残る。Canonical/承認4方向の既存比較板も確認したが、新たな本人性承認はしていない。これはNeutralのローカル搬送確認だけで、posed deformationの外観・接触・可愛さやHuman Visual PASSを証明しない。

## 公式調査（2026-10-15閲覧、ログイン/操作なし）

| 確認範囲 | 根拠と判断 |
|---|---|
| Studio投入 | [公開Rigページ](https://studio.tripo3d.ai/workspace/rigging?open=login)のUpload 3D ModelはOBJ / FBX / STL / GLB、≤150MB。今回候補は上限未満 |
| Studio操作 | [公式Help](https://www.tripo3d.ai/help/features/is-it-possible-to-upload-my-existing-model-for-animation)はGenerate ModelのUpload → Animate → Auto Rig → downloadと案内。公開UIはRig/Animate別入口もある。ログイン後の正確な配置はUNKNOWN |
| Studio対象制限 | 同HelpはT-pose humanoid / standard standing quadrupedのみと記載。現Neutralは短肢・翼・巻尾を持つ非標準ドラゴン。適合・骨数・追加部位対応はUNKNOWN。T-poseに直して本人性を壊さない |
| 宣伝との幅 | [公式機能ページ](https://www.tripo3d.ai/features/ai-auto-rigging)はhumans/quadrupeds/stylized/mechanicalを掲げるが、Jillの部位別対応保証ではない |
| API別仕様 | [公式API Rig](https://developers.tripo3d.com/en/models/rig)はbiped / quadruped / hexapod / octopod / avian / serpentine / aquatic、GLB/FBX出力、Rig Check 0 / Auto Rig 25 creditsと記載。Studioへの同一展開・価格・無料Check提供はUNKNOWN。APIを実行しない |
| 費用 | [Studio Pricing](https://www.tripo3d.ai/pricing)でRigging & Animationを掲げるが今回の単発消費量は確認できずUNKNOWN。ログイン中アカウントの残高、使用可能プラン、出力可否、公開範囲、商用条件、失敗/再試行課金もUNKNOWN |

## Humanが後日試すときの手順

1. StudioのRig入口（上記公開URL）またはGenerate ModelのUploadを開く。アカウントの契約、残高、公開/商用条件、外部モデルのRig機能とdownload権限を確認する。
2. 推奨FBXを1個選ぶ。Import previewで全身/足/翼/葉/尾が揃い、上下・正面・寸法に大きな差がないことを確認。形状変更、Remesh/Retopo、Texture処理は選ばない。FBXが受理されない場合のみGLBを使う。
3. Rig / Animate内のAuto Rigを確認。対応type/モデルversion、Checkの有無と費用、実行直前に表示される消費credits、失敗/再試行/出力費用を記録する。APIの25 creditsをStudio価格と見なさない。
4. 適合しない、別の姿勢を要求される、費用/出力条件が不明なら、その画面情報を残して止める。今回の準備は実行許可を含まない。後日のHuman判断で実行する場合は結果をFBX（可能なら比較用GLBも）でdownloadし、入力と別名・別フォルダで保管する。

## 基礎Rig取得後の最小検証とBlender補完

最初に返却fileを別sceneへ読み、restでv002と同一視点比較。座標/面数/材質、bone hierarchy、weights、縮尺/向き、自動Geometry変更の有無を確認。返却Geometryが変わった場合は正本を置換せず、v002複製へrest alignmentを確認した骨格とweightのみ移す方法を検討する。距離ベース転送を無検証で採用しない。

| 部位 | Auto Rigが不足/誤認した場合のBlender補完 |
|---|---|
| 翼 | 胴から独立した左右の翼根・翼端chainを追加。膜・根のweightsを局所調整し、首葉の引きずり、膜裏の潰れ、根の伸びを確認 |
| 前肢 | 腕/肩/手のchain・接続位置を体型に合わせる。肩weightを局所調整し、手先の取り残し・顔/葉の巻き込みを防ぐ |
| 尾 | 巻いた尾に沿う複数boneを追加/調整し、尾葉へ追従weight。根の折れ、胴貫通、先端の体積変化を確認 |
| 葉 | 頭/首/尾の葉を所属boneへ追従。必要な揺れだけ補助boneを追加し、全葉一括の自動weightによる顔や翼への引きずりを避ける |

Neutral → 小振幅 → 中間 → 暫定極値 → Neutralで、左右翼開閉、片腕offer、尾左右を各1回、その後必要な複合1例を確認する。以前のTEST_ONLY角度/診断キーは承認可動域にしない。front/side/3Qと局所の実レンダーで顔・柔らかな体積・肩/翼根/首葉/尾根の連続性・交差を判定し、Neutral復帰と不要部位の独立性も確認する。未知をPASSにしない。

必要なら同じv002系譜の派生編集blendでbone位置・weights・pose-dependent局所補正を共同調整する。今回はNeutral・面構成を変更しない。後日Neutralや面の変更が必要と分かったら差分と外観影響を提示しHuman判断を求める。外観/可愛さのHuman承認、実Rig変形、Texture、最終Motion/runtimeの判定は独立。**Geometry GateはHOLD維持**。
