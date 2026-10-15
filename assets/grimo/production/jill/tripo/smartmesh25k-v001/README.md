# Jill Smart Mesh 25K — single editing lineage

**Human Geometry Gate: HOLD / Human判定待ち。** [レビューと証拠](../../../../../../docs/production/jill/evidence/smartmesh25k-v001/REVIEW.md) を先に読む。

正式な入力は `input/cute dragon 3d model (1).fbx` 一つ。Quadを保持するため採用。もう一つのGLB入力は不変保管・照合専用。

`FBX原本 → jill-geometry-master.blend → jill-repaired-neutral.glb`

- **唯一の編集正本：jill-geometry-master.blend**。原本FBXコレクションと除去した板を非表示で保持。保持する全頂点座標・面を変更せず、10 polygon / 12 triangleだけ除外。Basisに修復Neutralを保存。
- `TEST_ONLY_` の8 shape keyとframe1–289は診断限定。最終Rig・承認Motionではない。frame1は全診断キー0。再生には翼左右・尾左右・前肢左右・左右翼同時・複合の12ケースを含む。
- `jill-repaired-neutral.glb` はこの正本だけから書き出した静止レビュー用派生物。Texture・Tripo・Auto Rigへ進む承認はない。
- `jill-original-inspection.blend` は原本2形式の比較保存であり、補修していない。編集を継続するファイルではない。
- input2ファイルは不変。元アップロードを含むSHA-256はレビューに記載。

スクリプトはfresh/background Blenderで実行する。開いているユーザーのBlenderシーンを操作しない。監査後 `select_authority.py` の結果を先に確認してから `build_master.py`、正本を開いて `deformation_proof.py`、保存済み正本を開いて `verify_master.py`。撮影用 `capture_review.py` / `appearance_lock.py` / `visibility_details.py` は正本を保存しない。`package_review.py` はPillowで既存PNGを配置するだけ。

通常レビューのために再実行する必要はない。`build_master.py` は正本を再構築するため、Humanが加えた後続編集のある正本には実行しない。初期監査の `analyze.py` / `raw_check.py` にあるQuad対Triangleの直接集合比較は中間診断であり、正式な整合判定には使わない。
