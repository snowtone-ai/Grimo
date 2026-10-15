# Pino Face Foundation v002

**Human Face Gate=PENDING / Production=HOLD。** 2改善パスを終えた診断候補。口縁の自然な閉鎖、瞼外周の完全被覆は未成立。原本、Rig v001、正式Game Neutralを置換しない。

- `pino-face-foundation-v002.blend`: 全制御0、元の開いた笑顔Basisを保持。試作口Morphと別meshの立体上下瞼。未承認キーは製品採用しない。
- `pino-face-foundation-v002-proof.blend`: 1–121f/24fps。閉口候補→小/中/大→閉口、左右半閉/Wink/両閉、同時動作、復帰。尾/前肢/休息の演技なし。
- `pino-face-foundation-v002-diagnostic.glb`: 約1.97 MB。70 joints、口と左右瞼Morph。画像/UVなし。インポータはMorphのActionを別々のミュート済みNLAトラックへ保管するため、本体/左瞼/右瞼を同期有効化する。最終配信clipではない。

[REVIEW・静止画・短いGIF](../../../../../../docs/production/pino/evidence/face-foundation-v002/REVIEW.md)。GIFの濃青眼は一時的な所有診断色で、保存Blend/GLBにはない。

再現はBlender 5.2.1 LTSとPython+numpy/Pillow。必要なPino入力をhydrateしたcheckoutで、以下の同名Pythonを`blender --background --factory-startup --python`で実行する。

`scripts/blender/pino-face-foundation-v002.py` の順: 引数なし（元監査）、`-- --build`（保存済み第2パス方式）、`-- --owners`、`-- --proof`、`-- --source-compare`、`-- --reimport`、`-- --check-frozen`。引数はBlenderの`--`後。

最後にPythonで `scripts/3d/package-pino-face-foundation-v002.py --finalize`。レビュー後`--clean`でこのタスクの一時画像だけを除去できる。再生成は既存の派生成果を上書きするので、別checkoutで行う。第1パス不採用画像は履歴証拠として保持。
