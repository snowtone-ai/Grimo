# 再現手順と証拠の読み方

Git LFSの実データを取得したcheckoutで、Blender 5.2.1 LTSのPython（NumPy含む）と、通常のPythonでNumPy / Pillow / Matplotlibを使用する。アプリの依存関係・コードは変更しない。今回の追加Pythonパッケージはcheckout外に置いた。Tripo・外部生成・課金は不要。manifestのバイナリは生バイトのSHA-256、テキストはGitの改行変換を考慮してLFへ正規化したSHA-256。

各スクリプトはリポジトリルートで実行する。Blenderはfactory-startupを使い、開いている制作シーンに触れない。以下の`blender`と`python`を使用環境の実行ファイルへ置き換える。

```powershell
blender --background --factory-startup --threads 4 --python-exit-code 1 --python scripts/blender/audit-pino-c-geometry.py
blender --background --factory-startup --threads 4 --python-exit-code 1 --python scripts/blender/compare-pino-c-originals.py
blender --background --factory-startup --threads 4 --python-exit-code 1 --python scripts/blender/export-pino-c-master.py
blender --background --factory-startup --threads 4 --python-exit-code 1 --python scripts/blender/exercise-pino-c-geometry.py
blender --background --factory-startup --threads 4 --python-exit-code 1 --python scripts/blender/package-pino-c-replay.py
blender --background --factory-startup --threads 4 --python-exit-code 1 --python scripts/blender/frame-pino-c-rest.py
blender --background --factory-startup --threads 4 --python-exit-code 1 --python scripts/blender/verify-pino-c-export.py
blender --background --factory-startup --threads 4 --python-exit-code 1 --python scripts/blender/verify-pino-c-saved.py
python scripts/3d/assemble-pino-c-motion.py
python scripts/3d/report-pino-c-geometry.py
python scripts/3d/finalize-pino-c-gate.py
```

`master-decision.json`は今回のHuman回答の記録であり、別の候補・改変された原本へ流用しない。原本ハッシュが異なれば停止する。

`prove-pino-c-geometry.py`のmainは、Master一本化前のGLB予備診断を再実行するもの。**正式工程として再実行しない。** 現在の試験は同ファイルの計測・レンダー関数をimportするだけで、隔離されたGLB改変のmainは呼ばない。既存の予備データを、Master由来の試験として読み替えない。

実レンダーは`motion/`、静的9視点は`renders/`。GIFはそれらの連続フレームから作成した。再生.blendは実測サンプルを形状キーとして保存し、182フレームに配置している。これは診断の再生用で、製品Rig・承認済み演技ではない。保存ファイルを再読込して全フレームを評価した結果は`saved-file-verification.json`。サンプル間の補間を新しい可動域のPASSと見なさない。

最初の実行で低休息のゼロ強度計算に微小な浮動小数点残差があり、端点を原本座標の直接コピーへ統一した。非ゼロ150サンプルのfloat64ハッシュを再照合し、既存の実試験を保全した。最初の狭い画角で低休息の破綻部が画面外になったため、同じ25サンプルだけを広い固定画角で再描画した。形は修正していない。`replay-verification.json`と`rest-framing.json`参照。

Human確認は`REVIEW.md`から始める。`gate-status.json`は機械可読の集計、`manifest.json`はファイルのハッシュ一覧。実行ログ・途中progressはローカルの診断用で、最終判定の正本には含めない。
