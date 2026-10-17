# 再現 — v004 別名候補

Windows / Blender 5.2.1 LTS / Node 24 / Python 3.13 / PlayCanvas 2.22.2 / Chrome PC。使用branchはREVIEW参照。制作元v003と承認済みv004はread-only。USBなし、ADB/実機操作を含まない。

## 資材

Git LFSでv003 author/proof/GLB、承認済み `shushu-v006-production-rig-v004-proof.blend`、既存final-v003の `muzzle-retopo.npz` を実体化する。既存node_modulesまたはプロジェクトの固定依存を用意する。ffmpegをPATHに置く。下のコマンドはrepo rootから実行する。納品候補を保護したい場合は再生成用の別checkoutを使う。

```powershell
$blender = 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe'
# 元の症状とtriangle/skin-isolationを再採取（新Evidenceのみ）
& $blender -b -t 4 --python-exit-code 1 --python scripts/blender/diagnose-shushu-abc-v004.py
& $blender -b -t 4 --python-exit-code 1 --python scripts/blender/probe-shushu-abc-structure-v004.py
# 元v003から別名v004へ構築。元ファイルは保存しない。
& $blender -b -t 4 --python-exit-code 1 --python scripts/blender/repair-shushu-abc-v004.py
& $blender -b -t 4 --python-exit-code 1 --python scripts/blender/audit-shushu-abc-v004.py
& $blender -b -t 4 --python-exit-code 1 --python scripts/blender/audit-shushu-preservation-v004.py
& $blender -b -t 4 --python-exit-code 1 --python scripts/blender/audit-shushu-fk-contract-v004.py
# 1本の診断clipを書き出し、保存GLBを再読込して検証
& $blender -b -t 4 --python-exit-code 1 --python scripts/blender/prove-shushu-abc-v004.py -- --export
& $blender -b -t 4 --python-exit-code 1 --python scripts/blender/prove-shushu-abc-v004.py -- --verify
& $blender -b -t 4 --python-exit-code 1 --python scripts/blender/audit-shushu-contact-v004.py
& $blender -b -t 4 --python-exit-code 1 --python scripts/blender/compare-shushu-surface-v004.py
& $blender -b -t 4 --python-exit-code 1 --python scripts/blender/inspect-shushu-surface-v004.py
```

`--arms-only`等の修理用switchは反復調査のためのもの。全再現には上のsourceからのbuildを使う。特に`--corrective-field-only`を完成assetへ重ねて適用しない。Blender内部データ/圧縮/書き出しでバイナリhashが変わる場合は、納品hashと区別し、座標・保護特徴・制御・再読込を再検証する。

```powershell
# 640×640の実フレーム画像。動画は157枚、24fps。
& $blender -b -t 4 --python-exit-code 1 --python scripts/blender/render-shushu-abc-v004.py
& $blender -b -t 4 --python-exit-code 1 --python scripts/blender/render-shushu-abc-v004.py -- --video
& $blender -b -t 4 --python-exit-code 1 --python scripts/blender/render-shushu-abc-v004.py -- --saved
& $blender -b -t 4 --python-exit-code 1 --python scripts/blender/render-shushu-abc-v004.py -- --saved --video
& $blender -b -t 4 --python-exit-code 1 --python scripts/blender/render-shushu-abc-v004.py -- --approved
& $blender -b -t 4 --python-exit-code 1 --python scripts/blender/render-shushu-abc-v004.py -- --source
# 端末Aで127.0.0.1のみの限定serverを起動
node scripts/3d/review-shushu-abc-v004.mjs --serve
# 端末B。専用headless Chrome/CDP 9231でPC製品経路を採取
node scripts/3d/capture-shushu-abc-v004.mjs
```

`http://127.0.0.1:8771/docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v004/index.html` で比較を見る。runtime.htmlは保存GLBの診断Viewerであり、PC製品経路の証拠はcaptureが実loader/controllerへ切り替えた後のPNG/動画/JSON。raw制御検査ではPaw Morphを一度zeroにしてから9入力を与え、baked clip値だけを見て成功する偽陽性を避ける。`.set(null)`で元clipへ戻ることも照合する。

通常Morphと製品deformation-v003の8-weight経路が必要。v004 GLBのHold Anchorはv004 loaderの`pose-space-normal-v004`契約を要求する。旧arm FKだけのclipには対応しない。任意の4-weight Viewerや任意小物へ拡張しない。

大きい中間NPZと動画用157枚×2のPNGは再生成可能な作業データ。Gitには診断JSON・原寸の代表画像・連続動画・再現script・最終assetを納め、再生成データを大量追加しない。`delivery-manifest.json`のfilesは納品bytesの対応であり、Human承認印ではない。
