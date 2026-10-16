# 再現手順

専用branch `codex/shushu-v004-motion-ready-v003-20261016` のrepo rootから実行する。既存の別名候補だけが出力先。原本・main・他キャラの置換はしない。記録環境はBlender 5.2.1、Python 3.13（NumPy/SciPy/triangle/Pillow）、Node 24、PlayCanvas 2.22.2、ADB、FFmpeg。新たな課金サービスは使わない。

納品済み候補の確認は最終hash監査とViewer/製品経路captureから始める。下記のBlender roundtrip/実面監査には構築時の中間NPZが必要なため、別途局所修復を再現した場合に実行する。以下の構築は原因と局所修復を再現する必要がある場合だけ行う。LFS対象のv002 Blend/GLBと元v004 proof/GLBは実体を取得しておく。

```powershell
$blenderBin = 'C:/Program Files/Blender Foundation/Blender 5.2/blender.exe'
& $blenderBin -b -t 4 --python-exit-code 1 --python scripts/blender/diagnose-shushu-v004-motion-v003.py -- . docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v003
py -3.13 scripts/3d/plan-shushu-motion-v003.py
py -3.13 scripts/3d/rebuild-shushu-crown-v003.py
py -3.13 scripts/3d/audit-shushu-crown-topology-v003.py
& $blenderBin -b -t 4 --python-exit-code 1 --python scripts/blender/build-shushu-motion-v003.py -- --build
& $blenderBin -b -t 4 --python-exit-code 1 --python scripts/blender/rebuild-shushu-paw-posespace-v003.py
& $blenderBin -b -t 4 --python-exit-code 1 --python scripts/blender/build-shushu-motion-v003.py -- --export
py -3.13 scripts/3d/finalize-shushu-motion-v003.py
```

`diagnostic-source.npz` / `saved-reference.npz` / full decoded frame PNGは再生成する中間物。別の候補や古いhashの中間物を流用しない。構築するたびGLB/Blendのhashが変わり得るため、その成果に対する検証・capture ledgerを新規に作る。今回の最終hashは `delivery-manifest.json`。

```powershell
& $blenderBin -b -t 4 --python-exit-code 1 --python scripts/blender/audit-shushu-motion-v003.py
& $blenderBin -b -t 4 --python-exit-code 1 --python scripts/blender/audit-shushu-paw-space-v003.py
& $blenderBin -b -t 4 --python-exit-code 1 --python scripts/blender/build-shushu-motion-v003.py -- --verify
& $blenderBin -b -t 4 --python-exit-code 1 --python scripts/blender/audit-shushu-contact-v003.py
& $blenderBin -b -t 4 --python-exit-code 1 --python scripts/blender/export-shushu-paw-control-witnesses-v003.py
node scripts/3d/review-shushu-motion-v003.mjs --v003 --validate
```

原寸84枚（21状態×4方向）と4つの連続抜粋を、author / savedで生成する。いずれも同じ固定camera、24fps。録画はmouth 825–897 / arms 477–557 / seat-return 1–169 / composition 993–1149。診断抜粋であり量産Motionではない。

```powershell
& $blenderBin -b -t 4 --python-exit-code 1 --python scripts/blender/render-shushu-motion-v003.py
& $blenderBin -b -t 4 --python-exit-code 1 --python scripts/blender/render-shushu-motion-v003.py -- --video
& $blenderBin -b -t 4 --python-exit-code 1 --python scripts/blender/render-shushu-motion-v003.py -- --saved
& $blenderBin -b -t 4 --python-exit-code 1 --python scripts/blender/render-shushu-motion-v003.py -- --saved --video
node scripts/3d/review-shushu-motion-v003.mjs --v003 --serve
```

Viewerは `http://127.0.0.1:8769/docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v003/runtime.html`。同portの既存serverがあるときは再起動しない。phoneはユーザーが許可した既存Shushu tabだけを対象にする。画面を点灯・ロック解除した状態でChromeを表示し、ADBは端末1台を確認する。captureはnonce付きnavigation、qaReady、frame/24の時刻、frameend counter、visibility、hashを保存する。phone capture同士を並列実行しない。

```powershell
adb devices -l
adb reverse tcp:8769 tcp:8769
adb forward tcp:9223 localabstract:chrome_devtools_remote
node scripts/3d/capture-shushu-motion-v003.mjs --v003 --no-perf
node scripts/3d/capture-shushu-motion-v003.mjs --phone --v003 --no-perf --device-screen
node scripts/3d/capture-shushu-motion-v003.mjs --phone --v003 --production-loader
node scripts/3d/capture-shushu-motion-v003.mjs --phone --v003 --purpose-controls
node scripts/3d/capture-shushu-motion-v003.mjs --phone --v003 --face-diagnostic
node scripts/3d/capture-shushu-motion-v003.mjs --phone --v003 --normal-parity
node scripts/3d/capture-shushu-motion-v003.mjs --phone --v003 --gpu-time
node scripts/3d/capture-shushu-motion-v003.mjs --phone --v003 --perf-only --production-perf --measure
```

135画像には505–541の3-frame間隔×Side/左右3Qを含む。16 WebMは4抜粋×4方向。MediaRecorderは繰返しframeを落とす場合があるため、frame要求の全件ledgerと実デコード更新を別々に保存する。固定24fpsの再生保証へ読み替えない。4件のnative Android PNGは、同poseのcanvas capture後にも時刻が固定されrender counterが進むことを確認する。

`--purpose-controls` は26 witness中16件で、保存済みの非中立姿勢を中立carrier clip＋独立入力から作り直す。単に同じbaked clipを再生しただけのテストにしない。許容位置差1e-5H、法線成分差1e-4、Anchor行列差1e-4H。Applicationの`update`がanimationUpdateの後に来ることをインストール済みEngineソースで確認した。

5分計測では診断側のmesh・deformer・container資源を破棄し、製品loader/controller/deformationだけを動かす。カメラと記録用hookのみを使い、両モデルを同時に更新する計測をしない。比較用v002は既存8768 serverの `final-v002/runtime.html` を使い、同じcapture scriptに `--baseline --perf-only --measure` を渡す。共通993-frame loop、同じ3Q・640 canvas・USB・visible/WakeLockで記録する。開始温度差、単回順次測定、rAF≠GPU時間の制約を明記する。

```powershell
py -3.13 scripts/3d/assemble-shushu-motion-v003.py
py -3.13 scripts/3d/audit-shushu-delivery-v003.py
```

本番呼出側はloaderへ`pc, app, url`を渡し、返された`entity`のbody/face poseと現在のSeatを管理し、`pawControls.set({Seat, 'Hold.L':…, 'SelfContact.R':…, 'Wrist.L':…})`を更新する。通常の入力は直ちに適用され、animation後にも補間を維持する。`{defer:true}`はApplication update前の入力収集に限る。`dispose()`はidempotent。元のarm FK clipを無変更で使う契約は含めない。Human GO前の原本置換・量産はHOLD。
