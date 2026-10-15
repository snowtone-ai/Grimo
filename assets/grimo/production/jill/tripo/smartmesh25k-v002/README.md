# Jill Smart Mesh 25K — v002 local repair candidate

**Human Geometry Gate: HOLD / Human PENDING。GOはHumanのみ。Tripo操作・消費なし。** [目視レビュー・比較板・GIF・残存欠陥](../../../../../../docs/production/jill/evidence/smartmesh25k-v002/REVIEW.md)を先に読む。

編集系統は既存の一系統だけ：

`v001/jill-geometry-master.blend → v002/jill-geometry-master-v002.blend`

v001正本を入力にした別名保存。原本/v001を変更せず、FBX/GLBから新しい修正版を作っていない。今回の継続候補はv002で、v001との並行編集を意図しない。Humanが採用を判断するまでv001を置換しない。

- Neutral変更は眼内部64・下口縁24の計88頂点。身体・翼・葉・尾・足、面構成、bounds、transformはv001と同じ。28,050 vertices / 28,809 polygons / 54,361 triangles換算。
- `TEST_ONLY_`8キーとframe1–289の12ケースは限定診断。翼・腕・尾のweight/pivot/経路を補修したが根のGeometry問題は残る。正式Rig/Motionでも承認可動域でもない。
- frame1で全診断キー0。隠し未編集入力と板除去archiveを継承。元1材質、UV0、画像0、Armature0。仮材質はcapture限定で保存blendにはない。
- v002 SHA-256: `8c2ded49ec7108c420fead87d01b3ff26deb43e479d14479afc50e6aafd67a97`。
- 2026-10-15：Human指定で[基礎Rig投入候補FBX/GLB](tripo-input/)をNeutralから準備。[検証・公式根拠・UI手順](../../../../../../docs/production/jill/evidence/tripo-input-v002/REVIEW.md)。推奨FBXは面構成保持、GLBは三角化/孤立頂点省略あり。正本不変。Tripo操作・upload・消費は未許可/未実行、Geometry Gate HOLD。

scriptsは証拠再現用。fresh/background Blender 5.2.1、NumPy、比較板はPillowを使用し、ユーザーの開いているBlenderには接続しない。通常のHumanレビューに再実行は不要。

`inspect_master.py`/`diagnose_face.py`はv001監査と仮色診断。`repair_v002.py`はv001からv002を再生成するため、**後続のHuman編集があるv002には再実行しない。** `gate_capture.py`は保存候補の評価と撮影、`capture_only.py`は保存済み候補を撮影するだけ、`verify_preservation.py`は保存候補と保護入力照合、`package_gate.py`は実レンダー配置とGIF化だけ。最初の棄却案/preview.logは最終提出判定ではない。
