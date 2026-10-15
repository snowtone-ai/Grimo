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

次はHumanが顔の局所変更、残HOLD、追加局所補修範囲、承認pose reference、Geometry Gate/Tripo Texture開始可否を判断する。追加形状変更は止めた。Human承認前にTripoへ進めない。FBX/GLB派生は不要なため未出力。次の編集もこの一系統を継続し、原本再生成や全身Remesh/Decimate/比率変更をしない。

[v001履歴](evidence/smartmesh25k-v001/REVIEW.md)は保持。
