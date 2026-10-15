# Jill Geometry — 2026-10-15

状態：**Human Geometry Gate / HOLD / Human判定待ち**。Tripo Texture・Auto Rig未着手。判断者はHuman。

[レビュー・欠陥・承認項目](evidence/smartmesh25k-v001/REVIEW.md) と [正本の説明](../../../assets/grimo/production/jill/tripo/smartmesh25k-v001/README.md) を参照。

- 唯一の編集入力はFBX。原本GLB / FBXはSHA-256記録済み・不変。FBXの25,554 Quad + 3,265 TriangleはGLBの54,373三角形と頂点・面領域で整合。
- 板状異物は12三角形（FBX10面）。「5非連結成分」は再現せず3辺接続パッチ、下部は身体と頂点3・4を共有するため面だけを削除。頂点・保持面は全て保護した。
- 編集正本は `jill-geometry-master.blend` 一つ。未編集FBX・除去面を隠して保存。補修後54,361三角形換算。派生Neutral GLBはこの正本からのみ出力。
- 同条件Front / 左右Side / Back / 3Q、翼裏・根、尾根、足底、顔を保存。12限定変形ケースの中間・極値・復帰とFront / Side / 3Q画像あり。左右翼・左右前肢・尾の診断対象外移動0、Neutral復帰差0。
- 翼根・肩・尾葉の交差候補、前肢根元の局所伸び、元の目・口の粗さ、葉の継ぎ目が残る。Identityと可愛さは未承認。ポーズ参照は未承認であり、技術確認をMotion合格へ昇格しない。
- `2abea76fad578281f74b9fa628987a80b56ad6dc` のCharacter appearance lockを適用し、リモート制作履歴をfast-forwardで統合済み。元作業場所のShushu作業・アップロードを保持した。

次はHumanが除去範囲、顔・翼・葉・尾・体型、限定補修すべき箇所、承認pose reference、Texture開始可否を判断する。承認前にTexture / Auto Rigへ進めない。新しい可動域・補修を行う場合は正本から続け、GLB原本から別修正版を作らない。
