# Pino C Texture Handoff v004 — Pre-Texture Review

2026-10-16 JST。独立worktree / `codex/pino-texture-handoff-v004-20261016`。実物の起点はv003 `1dd7980f57419dd3a4ee5fbb4adc9c1dfac207b2`。共有規則・Goal√map・Handoff・Body-only登録は`main@73617ce2d3c724c86aed82dfc2a09cd220e5d194`を確認した。Canonicalと承認Body-onlyは外観Authority、34枚のMotion参照はHuman PENDINGであり同じ承認状態として扱わない。

**Human Pre-Texture Gate=PENDING / Texture GO=NO。総合はHuman確認待ちのHOLD。** 入力・編集・逆対応の受渡し資産を確定した。今回の代表変形ではTopology/UVを破壊する修正を必要とせず、Rig/Weight/Morph/Normalの修正で問題を分離できた。ただし、可愛さ・本人らしさ・自然な深い休息まで達成済みとは判定しない。**次工程の予定はHuman判定後のTripo Texture。Tripo・課金・Texture生成は実行していない。**

## 最初に見るもの

- [Canonical / 承認Body-only / v003・v004 Neutral比較](identity-comparison.png)
- [閉眼の全段階・3視点](face-stages.png)、[往復Blink GIF](blink-cycle.gif)、[Wink・複合表情](wink-combined.png)、[口の3視点](expressions.png)、[口の往復GIF](mouth-cycle.gif)
- [接触・支持・太尾の中間と極値](body-probes.png)、[身体往復GIF](body-cycle.gif)、[保存GLBのPlayCanvas描画](runtime-comparison.png)
- [Tripo入力GLB](../../../../../assets/grimo/production/pino/candidate-c/texture-handoff-v004/pino-c-v004-tripo-input.glb)、[編集Blend](../../../../../assets/grimo/production/pino/candidate-c/texture-handoff-v004/pino-c-texture-handoff-v004.blend)、[Rig付きレビューGLB](../../../../../assets/grimo/production/pino/candidate-c/texture-handoff-v004/pino-c-v004-rigged-review.glb)
- [UV・材質・逆対応契約](TEXTURE_CONTRACT.md)、[ファイルSHA](file-manifest.json)

GIFは評価済み中間状態を往復表示する診断サンプル。最終演技のフレーム列、連続衝突保証、完成Motionではない。数値probeは接触13、休息13、尾11サンプル。全Motionを量産していない。

## 原因の分離とTexture前の対応

| 部位 / v003の未達 | 原因と採用対応 | 構造上の分類 |
|---|---|---|
| 顔・閉眼：中間の厚い帯、退避中の塊、線が薄れる | 外付けcapを細くしてから眼を退避する制御が原因。さらにcapを増やす方法は採用せず、既存眼面を連続的に弧へ縮める`PinoSquint_L/R`へ変更。旧瞼keyは0で残す。口はv003の閉鎖・Lift・内張り同期を維持。 | **今回の候補はMorph/Normalで成立。新Topology/UV不要。** 瞼が虹彩を覆う解剖的Blinkではなく、様式化したSquint/閉眼線。横からの眼の厚み・影、笑顔との本人らしさはHuman PENDING。候補を承認形と偽装しない。 |
| 肩・前肢：胸のつぶれ、板状の陰影 | 胸の頂点を遠位Handへ引くWeight、短い前肢に不適合な接触目標、LBSでの体積減少、変形に追従しないpreview法線を分離。胴を保持した局所Weight、Arm主体の短い前肢、対応Pose補正と法線場へ変更。 | **Weight / Pose / Morph / Normal。** 先にTopologyを切り直す根拠は得られず。接触だけで可愛さPASSにしない。脇の局所伸び・滑らかな肩の肉付きは後述の残リスク。 |
| 骨盤・支持：深い屈みで床下64.9mm | 脚の可動長・足の固定・中央の支持面が骨盤Weightで沈む問題を分離。体内の支持骨起点を調整し、伸長なしの2骨解で足を保持。中央支持部の圧縮をPose専用Morphで表現し、中間4段の補正を保存。 | **Rig / Weight / Pose Morph。** 足だけを固定した浮いた屈みではなく、後方の下部体表も床近傍へ。ただし数点が近いことは尻の柔らかな荷重・自然な休息の証明ではない。真の尻支持の品質はHuman HOLD。腹ばい・横寝まで一般化しない。 |
| 太尾：3重殻・根元 | 全殻のWeightを滑らかな共通方向の場に変更、5骨の左右bendを各9°、累積±45°で検証。LBS体積用の小さな補正を同梱。 | **限定範囲はWeight/Morphで対応。** 3重殻を削除・融合してNeutralを損なう方式は不採用。最適化・殻除去はTexture後に安全な修正とは扱わない。大捻り・強い床圧縮・任意MotionはUNKNOWN。 |
| 保存・再import・runtimeの陰影差 | BlenderのFREE custom normalが骨変形に追従しないことを確認。実際のSkin法線計算を明示previewし、GLBにcorner対応のNORMAL Morphを埋め込む。 | **Normal / export / runtime。** Geometryの薄さと陰影だけの薄さを混同しない。BlenderではPose編集後にbridge呼出しが必要。 |

前肢を胴に近づけるだけの案は、UV伸びが少し減っても掌が腹へ埋まったため不採用。[配置の因果比較](contact-placement-cause.json)。採用配置では左右掌の交差開始点を二分探索し、微小な間隔を残した。[接触位置の解](contact-separation-solve.json)。支持Morphは接触による局所圧縮そのものであり、「床下を検出しなくなった」ことを自然な座位の承認に読み替えない。

## 保存物からの検証

| 項目 | 結果と限界 |
|---|---|
| 原本・承認物保全 | 元FBX/GLB、Rig v001、Face v002、v003 Blend/GLB、Canonical、承認Body-onlyの16ファイルでSHA一致。[source-protection](source-protection.json)。共有checkout・他キャラの未コミット成果に変更なし。 |
| Neutralと契約保全 | 全4meshのBasis座標、頂点/面/corner順、UV、材質面所有、元corner normalのSHAがv003と一致。[保存監査](saved-rest-contract.json)。400px同条件描画は正面/3Q差0、側面1pixel・1channel値差。[描画差分](neutral-render-difference.json)。Canonicalとの可愛さ一致はHuman判断。 |
| 接触 | 13サンプルで掌同士の三角形交差0。端点の掌頂点→相手表面距離約0.442mm。頂点間最短距離だけを接触判定に使わない。単一の胸前接触候補であり、物体把持・頬接触・すべての掌面の圧力を証明しない。[body-probes](body-probes.json)。 |
| 低い支持姿勢 | 13サンプルで1mm以上床下0。端点：足領域144頂点、後方下部体表6頂点が床から3mm以内。後方下部体表最小1.24mm、尾最小2.48mm。Neutral復帰位置差は最大6.86×10⁻⁸m。床接触の数値から「自然な深い休息」を自動PASSにしない。 |
| 太尾 | 左右±45°までの11サンプル。元3殻を含む符号付き体積比は約1.0000〜1.0010。全身1mm以上床下0。休息への追従では同じ体積比の最低約0.9957。角度や体積は丸さ・重さのHuman承認ではない。 |
| UV / 入力 | 保存した静的GLBの50,763三角形で正面積UV重複0、ゼロ面積0。編集正本への位置差<10⁻⁵m、UV差<10⁻⁶を検証。Skin/Morph/animationがないことも実物で確認。[入力監査](glb-input-uv-audit.json)。TripoがこのUVを維持するかは未試行。 |
| GLB Validator | 静的入力：error0 / warning0。Rig付きレビュー：error0 / warning4（skinned meshがarmatureの子という既知の配置）。[Validator](glb-validator.json)。元12cornerのゼロ法線はexporter fallbackを維持。 |
| 保存GLB再import | 12状態×4mesh＝48比較。最大位置差2.264×10⁻⁵m（約0.023mm）、normal差1.54×10⁻⁴、UV差2.99×10⁻⁸。[再import監査](reimport-audit.json)。GLBに保存した法線からpreviewを再構成。Blender標準import単独でのMorph法線追従は保証しない。 |
| PlayCanvas | 2.22.2 / desktop Chromium。保存GLBの6描画instanceにSkin/Morph、全targetでNORMAL。10代表状態の実Skin行列は元の世界変形差分と最大2.87×10⁻⁶の差。アプリerror0。[runtime-probe](runtime-probe.json)。スマホ、性能、別エンジン、全MotionはUNKNOWN。 |

静的入力は約6.14MB、編集Blend約7.91MB、Rig付きレビューGLB約48.08MB。レビューGLBは140,001分割頂点、50,763三角形、4mesh / 5使用材質 / 70骨。対応IDとMorph法線を明示保持した検証資産で、配信最適化済みのスマホ完成品ではない。

## 残リスクとTexture後の修正計画

1. **G1 / G2のHuman Gate：** 閉眼がSquint方式でよいか、側面の眼面・影、口角、小開口、接触中の短肢らしさ、低姿勢の腹/足境界と重さを判断する。現状の脇の伸びと下腹の折れを隠さない。Human visual PASSは今回代行しない。
2. **前肢の表面伸び：** 接触端点の辺長比p99は約2.72、最大約7.68。小さい元辺を含む局所最大であり、画像の歪み評価の代用ではない。Texture後は既存の骨・Weight勾配とPose補正を調整し、同じUVのまま肩/脇の丸さと画像の伸びを改善する。contactのbind空間補正は最大約103mmなので、対応するPoseから外して単独再利用しない。必要なら補正Poseを追加する。これは今回の接触の最終品質PASSではない。
3. **支持と休息：** 現在は床近傍の体表を持つ限定の低い支持候補。重量感・ゆっくりした荷重移動・接地圧・腹の柔らかさは後工程のRig/Weight/Pose Morphで調整する。正式Motionが現在より大きい腹ばい・寝返り・極端な尾の圧縮を要求する場合は、同じUVでの変形成立を別途確認する。現段階でその全域の手戻り不要を保証しない。
4. **Textureの返却：** 画像だけを既存UVへ返す。Tripo出力をGeometry/Rig置換に用いない。UVが変わった場合は材質所有別のdonor転写と未露出面の補完が必要。転写実行・Tripoの品質/互換性は未試行であり、対応不能なら受入HOLD。[手順と対応表](TEXTURE_CONTRACT.md)。
5. **変更禁止の境界：** Texture後の通常調整は骨/Pose/Weight/Morph/Normal・材質/画像。殻融合、広域retopology、UV再pack、承認外のNeutral再造形は含まない。今回の代表範囲でそれらが必須だという欠陥は確認していないが、未承認の全Motion範囲まで安全と断定しない。

今回の受渡しでは、既知のUV破壊を必須とする欠陥は検出されず、代表的な問題を保持Geometry上で修正できる資産を提出した。**Humanがこの外観・必要可動域を受け入れた後の次工程はTripo Texture。** 判定がFAILなら、その指摘を同じTopology/UVでの局所補正へ戻す。新しい必須Motionが既存Topologyで成立しない証拠が出た場合はTexture開始前にHOLDを維持して再分類する。無条件GOにはしない。

## 再検証

Blender 5.2.1：`scripts/blender/pino-texture-handoff-v004.py -- --build` → `-delivery.py`と`-proof.py` → Pythonの`scripts/3d/package-pino-texture-handoff-v004.py` → Blenderの`-reimport.py`。PNGと中間normal bankは`artifacts/pino-texture-v004/`へ。ボード/GIF/SHAは`scripts/3d/assemble-pino-texture-handoff-v004.py`。旧版を上書きしない。

ローカルviewerは既存`serve-pino-texture-ready-v003.py --engine-root <既存playcanvas/build> --port 8794`で配信し、`/scripts/3d/pino-texture-handoff-v004-runtime.html`を開く。`window.proof.state('contact'|'rest'|'closed'|'wink'...)`と`view('front'|'side'|'3q', face)`。`scripts/3d/probe-pino-texture-handoff-v004.js`はPlaywright CLI `run-code --filename`用。最終Motionはファイルへ追加していない。

FREE custom normalの挙動は[Blender公式manual](https://docs.blender.org/manual/en/5.2/modeling/geometry_nodes/mesh/write/set_mesh_normal.html)と実測を照合。PlayCanvasの法線式は使用したローカルEngine 2.22.2の`normalCore.js`を確認した。外部サービスの仕様推測を受入根拠にしていない。
