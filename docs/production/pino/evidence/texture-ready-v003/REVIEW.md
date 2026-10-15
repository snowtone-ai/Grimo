# Pino C Texture Ready v003 — Human Pre-Texture Review

2026-10-16 JST。起点は`codex/pino-face-foundation-v002-20261015@07ffa41d9079952b6af83e8d70a71cb2da992150`。制作は独立worktree / `codex/pino-texture-ready-v003-20261015`。

**総合HOLD。Human Pre-Texture Gate=PENDING / Texture GO=NO。全要件を満たす本番Texture Readyとは判定しない。** 顔の遮蔽と受渡しの問題を改善した編集候補を提示する。半閉/閉眼の柔らかさ、口遷移の本人らしさ、必須の身体可動域とUV制作性はHuman判断が残る。

## 資産と見る順序

- [編集Blend](../../../../../assets/grimo/production/pino/candidate-c/texture-ready-v003/pino-c-texture-ready-v003-HOLD.blend)、[受渡しGLB](../../../../../assets/grimo/production/pino/candidate-c/texture-ready-v003/pino-c-texture-ready-v003-HOLD.glb)、[UV wire](../../../../../assets/grimo/production/pino/candidate-c/texture-ready-v003/pino-c-v003-uv-layout.png)。無着色placeholder、画像Textureなし、animationなし。正式Game Neutralは選んでいない。
- [Canonical / 承認Body-only / v003全身](identity-comparison.png)、[v002 / v003の同条件Basis比較](neutral-comparison.png)。前者は外観判断用で、2D絵と3Dのピクセル一致試験ではない。
- [口の連続開閉GIF](mouth-cycle.gif)、[左右独立Blink・Wink・複合遷移GIF](eyes-combined.gif)。正面/側面/3Q、診断用の濃青眼・暗い口内。最終演技や製品Textureではない。
- [閉眼段階と残存問題](eye-closure-stages.png)、[身体の成立範囲と失敗](body-boundaries.png)、[法線がU字残りを作る因果比較](normal-cause.png)、[PlayCanvas 3/4閉眼](runtime-three-quarter.png)、[Wink](runtime-wink.png)、[複合表情](runtime-combined.png)、[Skin実変形](runtime-head-probe.png)。
- [UV・材質・制御の所有契約](TEXTURE_CONTRACT.md)、[配布ファイルSHA](file-manifest.json)、[保存物・証拠の整合監査](delivery-consistency.json)。

## 受入条件の監査

| 項目 | 判定と証拠 |
|---|---|
| 原本・Basis保全 | **PASS（数値）**。元FBX/GLB、Rig v001、Face v002、Canonicalの保護対象は全SHA一致。本体18,858頂点、三角形、元corner normalは保存後も差0。[source-protection](source-protection.json) / [保存監査](saved-master-audit.json)。 |
| ① 閉口と内部遮蔽 | **限定PASS（描画）/ 自然さUNKNOWN**。閉→小/中→元の開口→大→閉を3視点で確認。全閉で口内面を非表示にしても3視点の差は0ピクセル。正面の口内色は閉0、小339、中565、Basis795、大1,081ピクセル。固定した開口色を頭に割り当てない。[遮蔽検証](visibility-probes.json)。小開口の口角/内側の形と閉じ際の印象はHuman確認待ち。 |
| ② 左右眼と複合変形 | **FAIL（自然な遷移形）/ 限定PASS（独立性・全閉被覆）**。両眼全閉は3視点で眼色0ピクセル。正面のWinkでは閉じた側0、反対側は通常と同じ3,240/3,293ピクセル。半閉は上下の帯状に見え、b=.925で小さな瞼の塊、b=.95で閉眼線がまだ現れない区間が残る。全閉線も細い。[段階比較](eye-closure-stages.png)。外周の再露出解消を自然な閉眼の成立と扱わない。承認形・柔らかさはHuman PENDING。 |
| ③ 尾根元・3重殻 | **限定範囲のみ確認 / 全域UNKNOWN**。元の3重殻を保持。Rig v001の左右限定bendでは新しい破綻を認めず、LBS4と元DQの最大位置差は約0.132mm。大角度、接触、全Motionに拡張しない。必要性が証明されない殻統合や広域Remeshは行わない。 |
| ③ 前肢・低休息 | **FAIL（既存stress姿勢）**。低い片前肢差し出しは確認できるが、両前肢を寄せる姿勢で胴/肩がつぶれる。元DQにも失敗があり、LBS4差は最大42.8mm。深い低休息は床下64.9mm、1,752頂点が1mm以上貫通。浅い屈みを真の尻支持の休息PASSにしない。[身体診断](body-diagnostic.json)。 |
| ③ Texture後の形状手戻り | **UNKNOWN / UV本番凍結HOLD**。失敗はPose/Weightの影響を含み、現時点で広域形状変更が必要とは証明できない。必須の接触範囲・支持姿勢が未承認のため、UV破壊を伴う修正が不要とも断定できない。対象姿勢の承認後、最小のWeight/補正で解けるかを先に確認する。 |
| ④ UVと材質所有 | **PASS（構造）/ 制作性UNKNOWN**。共通0–1 atlas、全50,763三角形で正面積重複0、UV面積0の三角形0。Blenderのoverlap選択も全meshで0。70面のUV局所chartだけを補修し、本体Topologyは不変。島が細かいため数値PASSをペイントしやすさの承認にしない。[UV監査](uv-audit.json) / [面・UV SHA](delivery-contract.json)。 |
| ④ 保存・再import | **限定PASS（Bridge付き）**。9状態×4meshをprovenance IDで比較。b=.75/.925/.95、複合表情と頭骨6°のSkin変形を含め最大位置差2.51e-6、法線ベクトル差8.99e-5、UV差2.99e-8。[再import監査](reimport-audit.json)。Blender標準importだけではMorph法線が追従せず陰影FAIL。付属Bridgeの要件を隠さない。 |
| ④ PlayCanvas | **限定PASS / 実運用UNKNOWN**。2.22.2 / desktop Chromeで同じSHAのGLBをロード。6描画instanceすべてSkin/Morph、全MorphでNORMAL有効。頭骨6°で2つのSkin行列が変化、アプリerrorなし。[runtime検証](runtime-probe.json)。スマホ・性能・全身Motion・任意のroot操作は未検証。 |
| ⑤ Canonicalとの外観 | **Human PENDING**。元の顔/眼/頬/口吻/短肢/巨大尾のBasisを保全。同条件400pxレンダー差は正面161、側面13、3Q168ピクセル、最大channel差4/7/3。主に元面へ5µm重ねた内張りの陰影差であり、ピクセル完全一致とは報告しない。[差分](neutral-render-difference.json)。数値差0の形状も表情の本人らしさを証明しない。 |

## 切り分けと採用方式

| 観測 / 比較 | 採用した方式と制約 |
|---|---|
| 縦方向だけの口縁移動は局所fanを引きつらせる。細分化案はBasis描画を変えた。奥行きだけの閉鎖では中間の口内色がずれる。 | 元Topologyのまま局所的な閉鎖と中間開口Liftを併用。内張りも同期し、閉じ際だけ奥へ退避。大きな顔の作り直しを採用しない。 |
| 閉じた位置でも元custom normalがU字を残す。GLBの同位置cornerを一括mergeすると再発する。内張りの分離頂点をそのまま法線計算すると変形時に面が角張る。 | Basis normal + 局所pose normal差分。内張りは変形法線のみ同位置で平均。GLBはcorner provenanceを保持し、NORMAL morphを明示格納。[normal patch](glb-normal-patch.json)。 |
| 外付けの丸い全閉capは貼り付いた円盤になり、二重の稜線は硬く見える。眼を早く沈めると浮いた帯が残る。瞼を先に細くすると眼外周が再露出する。 | 中間形を2段追加し、ほぼ閉じた後に眼と瞼を同量退避、その後で全閉の細い帯へ移行する。頭皮は局所補正。外周再露出は解消したが、退避途中の小さな塊と線の現れ方が未達。Basis固定と未承認の閉眼形を独断で変更しない条件下で、Humanの目標形判断が必要。 |
| DQのままではGLBのLBSと肩/首の変形が一致しない。UVのsmart projectionだけでは小さな重複が残る。 | 配布MasterとGLBをLBS4で統一し、原本DQを別保護。元の6 influenceのうち452頂点を4へ正規化。UVはunwrapと独立した面積重複検出により局所chartを修正。姿勢品質とUV制作性のHuman判断は別に残す。 |

GLBは24,539,128 bytes（約24.54MB）、140,001 export頂点、50,763三角形、4mesh / 5材質 / 70骨。corner normalと対応IDを守る分割を優先した診断受渡しで、最適化済みのスマホproduction assetではない。[実構造](gltf-structure.json)。glTF Validatorはerror0、warning4（skinned meshがarmatureの子）。UV未使用のinfoは画像Texture未割当による。[validator](glb-validator.json)。12個の元ゼロ法線cornerはexporterのfallbackであり、元のcorner配列を改変していない。

## Human判断と解除条件

1. Canonical/Body-only、GIFと閉眼段階比較を見て、口角・小開口・閉じ際の本人らしさと、半閉〜全閉の目標形を判断する。現状の瞼の帯・退避中の塊・線が薄れる区間を自動承認せず、目標形をもとに局所修正して再検証する。
2. 必須の両前肢接触範囲と真の低休息の支持/重さを決める。[34枚のMotion参照](../../../../../assets/grimo/production/pino/references/REVIEW.md)はすべてHuman PENDING。失敗Poseを完成形へ採用せず、承認範囲に対する局所修正を検証する。形状変更が必要ならTexture開始より先に候補UVを更新する。
3. UV島の制作性とnormal/同期制御の受渡し条件を確認する。これらのHOLD解除前に本番UV凍結やTexture GOを宣言しない。正式Game NeutralはHumanが別途決める。

[AGENTSの外観固定規則](../../../../../AGENTS.md)は「If visual mismatch remains or pose references are missing, report HOLD and seek Human judgment; never self-approve.」と定める。本候補でHuman判定を代行しない。Texture生成・Tripo・課金・他キャラ編集・サブエージェント・最終Motion量産は実行していない。

## 再検証の入口

Blender 5.2.1で、`pino-texture-ready-v003.py`（source検査→`--build`）、`-delivery.py`、Pythonの`package-pino-texture-ready-v003.py`、`-proof.py`、`-reimport.py`の順に使用する。身体診断は最初のscriptの`--body`、ボード/JSON集約は`assemble-pino-texture-ready-v003.py`、最終整合検査は`pino-texture-ready-v003-audit.py`。全て`scripts/blender/`または`scripts/3d/`。原本を上書きせず、`artifacts/pino-texture-v003`をscratchに使う。

連続GIFは`pino-texture-ready-v003-gif.py -- --gif-python <Pillow/numpyを含むPython>`で作成する。1枚の一時PNGを上書きしながらstreamし、フレーム群を保存せずメモリ上でencodeする。配布Blendへanimationを加えない。

PlayCanvasは`serve-pino-texture-ready-v003.py --engine-root <既存playcanvas/build>`でローカルviewerを開く。新しいpackageを導入しない。`window.proof.state(c,l,bL,bR)`と`view('front'|'side'|'3q')`で同じ制御を確認できる。証拠画像だけの確認をSkin実行確認の代わりにしない。
