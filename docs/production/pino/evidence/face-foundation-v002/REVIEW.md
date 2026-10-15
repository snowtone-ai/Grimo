# Pino Face Foundation v002 — Human Face Gate

**Human Face Gate=PENDING / Production=HOLD。2改善パスで停止。自然な閉口・完全な瞼被覆は未成立。**

起点 `codex/pino-base-rig-v001-20261015@80ed1a9c1335b520e50190059410f23126c61762`。成果branch `codex/pino-face-foundation-v002-20261015`。共有checkoutは開始時 `codex/shushu-v004-mouth-b-20261015@d5e9882`、Shushu等の未コミット変更があり、別の小さいsparse worktreeで作業した。原本・Rig v001を置換しない診断候補である。

## 最初に見る証拠

- [元GLB / v002 / GLB再importのBasis、同条件Front・Side・3Q](basis-comparison.png)
- [閉口・大開口・半閉眼・眼と口の同時動作](face-representatives.png) / [約6.6秒の実変形GIF](face-proof.gif)
- [現物3視点と使い捨てコピーの切断面](source-audit.png) / [元三角形から計算した口断面](mouth-sections.png)
- [不採用の第1パス閉口](rejected-pass1.png)

GIF/表情静止画の濃青眼は、眼と瞼の所有・露出を読むための一時的な単色材質。**Textureではなく、保存Blend/GLBに含めていない。** 通常の基準外観は灰色のBasis比較で見る。GIFは保存proofを再読込した41サンプル、121f/24fpsの診断で、最終演技ではない。

## 口の現物監査

**事実:** 元GLBのUV・画像・Texture・Morphは0。口は頭本体component 0につながる立体的なくぼみで、上側の口吻/口縁、下側U字縁、奥面・底面を持つ。断面には近接する複数層が見える。口のcomponent 0に限定したROI内の境界辺/過接続辺は0。今回、元メッシュの三角形は変更していない。[native GLB](native-glb.json)、[元構造](source-audit.json)、[局所トポロジー](mouth-topology.json)。

**UNKNOWN:** 多層面の意味と口腔の密閉性、口底の一部が舌を意図するか、上/下口縁の物理的接触、全補間の自己貫通。独立した舌componentは見当たらず、独立した口内材質もない。内腔を「欠落」と断定せず、今回は新しい内腔・舌・広域Remeshを足していない。Shushuの固定開口絵柄をPinoの欠陥とは扱わない。

## 試作と判定

| 項目 | 結果 | 判定 |
|---|---|---|
| 既存Basis/本人の基準形 | 元メッシュの座標・三角形・corner法線・材質、Skin、70骨rest、既存Blinkキーを保持。v001と同条件3視点の画素一致 | 保持の技術PASS。Canonical品質のHuman承認とは別 |
| 独立Blink/Wink | 左右それぞれ858頂点の上下瞼で、動かさない眼パッチを覆う。Half/Closedを補間しL/R片閉・両閉・復帰を保存 | 独立性PASS。外周の眼露出と側面の被覆欠けが残り、自然な全閉はFAIL/HOLD |
| 第1パス閉口 | 口内と下縁を大きく縦収縮。口角下に三角状の崩れ。法線再計算診断でも残る | FAIL、不採用 |
| 第2パス閉口 | 既存くぼみを局所口吻面へ寄せ、小さい下縁移動へ制限。大崩れは減ったがU字輪郭が残る | 自然な上下口縁閉鎖FAIL/HOLD。正規Game Neutralにしない |
| 連続口動作 | 閉口候補→小→元Basis相当の中→大→閉口候補。眼+口同時動作も109fに保存 | 実Morphと復帰PASS、形状品質は上記HOLD |
| 保存/GLB | authoring/proof再読込、約1.97 MB GLB、全MorphとSkinを再import。代表11時点の位置差最大2.82e-7。Head所有面の4°Skin診断も最大2.71e-7以下 | 限定技術PASS |
| GLB基準描画 | 480px同条件でv002 Blendとの差はFront 1,429 / Side 1,554 / 3Q 1,640画素、最大35/40/50階調。局所の陰影差を確認 | 外観の完全一致は未達/HOLD。位置一致で外観PASSにしない |
| 首/全身互換 | 一時的な4°Head診断で既存DQ SkinとGLBの首付近に最大1.31e-4の差 | 全身Motion互換は未成立。尾/前肢/休息を修正しない |
| 貫通・穴・Z-fighting | 口ROIの元トポロジーと多層面を保持。瞼外周に露出/不連続が残る | 完全排除はUNKNOWN、総合PASSにしない |
| PlayCanvas/スマホ | 即利用できるPinoプレビューを確認できず、実装を拡大しなかった | UNKNOWN |

原単位の全高は約0.999512。mmとして読まない。基準比較は480pxのWorkbenchで、元GLB対v002はFront/Side一致、3Qのみ3画素・最大1階調の差。これはTexture完成時の印象を保証しない。[画素](pixels.json)、[保存/凍結範囲](saved-checks.json)、[再import](glb-reimport.json)。

## Texture前の契約とHuman判断

[短いTexture/変形面所有契約](TEXTURE_CONTRACT.md)を今回の成果とする。実際の口内色の面分離・UV/Texture制作はまだ行わない。

上位AuthorityはローカルAGENTS/Goal、[Pino Canonical](../../../../../assets/grimo/source/pino/pino-Identity-canonical.png)、承認Body-only、Motion-to-Anatomy Q01/Q09、[Rig v001 REVIEW](../rig-v001/REVIEW.md)。承認Body-only Front/SideとCanonicalを実見した。34枚のMotion画像はHuman未承認で、閉眼・閉口の最終正解には使っていない。

Humanへは、開いた笑顔Basisの保持、閉口候補のU字残り、半閉/全閉の眼外周を提出する。正式Game NeutralはHuman未決定のまま。**無理な形状変更を採用せずHOLD。Texture/最終Rig/全Motion/Tripoへ進まない。**

[資産・再現](../../../../../assets/grimo/production/pino/candidate-c/face-foundation-v002/README.md) / [保護入力と成果hash](manifest.json)。
