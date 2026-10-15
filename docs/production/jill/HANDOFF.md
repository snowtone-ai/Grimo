# Jill Geometry — 2026-10-15

状態：**v002 Human Geometry Gate / HOLD / Human判定待ち**。HOLD解除未達。Tripo操作・upload・消費0、Texture / Auto Rig未着手。GOはHumanだけが決定。

[v002レビュー・実画像・残存欠陥・判定事項](evidence/smartmesh25k-v002/REVIEW.md) / [v002正本の説明](../../../assets/grimo/production/jill/tripo/smartmesh25k-v002/README.md)。

- branch `codex/jill-smartmesh25k-inspection-20261015`、開始HEAD `e513dc7c5c605ab1b6a0f9c85597520667e61490`、開始時clean。既存Jill worktreeのみ使用。他作業場所のShushu差分は不変。
- 唯一の既存正本 `v001/jill-geometry-master.blend` から `v002/jill-geometry-master-v002.blend` へ別名継続。原本/v001/承認参照219ファイルhash一致。12三角形板除去を継承。v001を採用置換していない。
- Neutralは眼内部64・下口縁24頂点だけ局所変更。身体・翼・葉・尾・足、面構成、bounds、transformは不変。28,050頂点 / 28,809面 / 54,361三角形換算。v002 SHA256 `8c2ded49ec7108c420fead87d01b3ff26deb43e479d14479afc50e6aafd67a97`。
- 仮材質比較で無彩色の読みにくさとGeometry残課題を分離。仮材質はcapture限定、保存正本に正式Textureなし。眼窩の隙間・浅い眼、口縁の粗さは残HOLD。
- 診断キーの翼/腕/尾weightと経路を局所補修。翼/腕の交差候補と腕伸びは減るが、翼Openの伸びは増えるtradeoff。尾根候補は3/1のまま。根のGeometry無干渉は未達。正式Rig/Motionではない。
- Codexが実レンダー比較板34枚を開き、Canonical/承認Body-only4方向、v001とFront/左右Side/Back/左右3Q、顔/根/膜裏/肩/葉/尾/足底、12ケースの中間/極値/復帰を目視。比較板・5点診断GIF3本を保存。Neutralの既存体型は保持して見えるが、眼・翼根/首葉・肩・尾根は外観HOLD。可愛さ/本人性はHuman未承認。
- 12ケースのNeutral復帰差0、対象外最大1.49e-8（1e-7内、完全0ではない）、新規退化0。技術確認を外観/Motion/runtime PASSに昇格しない。34枚Motion画像は未承認のまま。

## 2026-10-15：基礎Rig投入準備（最新Human方針）

**基礎Rig → BlenderでRig/Geometry共同調整 → Texture → 最終調整**へ。静的Geometryだけで翼根/肩/尾を修復し続けず実際の骨格/weightsで再評価する。ただし今回の許可は準備のみ。Tripo操作・upload・消費0、Geometry Gate HOLD、外観Human未承認を維持。

[投入候補・往復検証・公式調査・Human操作手順・部位補完計画](evidence/tripo-input-v002/REVIEW.md)。開始HEAD `709cddb`、clean。最新取得main `8e4996c` のAGENTS/Goal/Handoff確認、一括mergeなし。v002を保存せずNeutralメッシュ1個だけ出力。`assets/grimo/production/jill/tripo/smartmesh25k-v002/tripo-input/jill-v002-neutral-tripo.fbx`推奨、同名GLB予備。FBX全頂点world差0・面座標集合一致。GLBは三角化/面未使用16頂点省略、表面差2.666e-7以下。Shape Keys/animation/原本/除去板の面なし。保護220ファイルhash不変。実レンダーfront/side/3Qの比較板あり。G3実Rig検証→G2独立した翼/葉/尾/前肢→G1本人性保護を狙う。

Studio公式はFBX/GLB等≤150MB。Helpのhumanoid T-pose/標準四足制限とAPI7種対応は区別。Jill適合・翼/葉/尾対応、ログイン後UI/費用/出力権限はUNKNOWN。API25 creditsをStudio費用と断定しない。次はHumanが手順の費用/適合を確認し、実行可否を判断する。取得できた基礎Rigは別名保管し、v002系譜へ骨格/weightsを取り込みrestと実変形で確認する。Neutral/面編集が必要なら差分を示してHuman判断。全身Remesh/比率変更、原本再生成をしない。

[v001履歴](evidence/smartmesh25k-v001/REVIEW.md)は保持。
