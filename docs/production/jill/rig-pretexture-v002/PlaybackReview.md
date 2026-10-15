# Continuous playback — bounded review / HOLD

2026-10-15 JST。対象は保存済み `jill-rig-pretexture-v002.blend` 内の305frame、24fpsの代表確認action。全Motion制作ではない。

[Front / Side / 3Q実レンダー動画](bounded-continuous-front-side-3q.mp4) は全frameを3 cameraでWorkBench renderし、同じframeを横に結合したもの。960×320、24/1fps、12.708333秒、ffprobe decoded frame count **305**。静止画の補間生成や動画AIを使っていない。[0.5秒間隔filmstrip](bounded-continuous-filmstrip.jpg) と各caseの中間/終端/復帰拡大画像を直接開いた。

ローカルChromeの `/playback` で実動画を再生し、再生中のcurrentTime進行と終端12.708秒を確認した。モデルによる観察は再生中/終端のスクリーンショットとfilmstrip、各case実レンダーの直接目視であり、全305frameを一枚ずつ精査したとは言わない。極値の顔・根は高解像度の別画像で評価した。

| 区間（frame、1始まり） | 動作 | 所見 |
|---|---|---|
| 1–25 | 閉→小→中→大→閉 | 口腔の出現と閉鎖は連続するが、顎パッチと上口縁の段差が視認できる。大開口内壁の粗さも残る |
| 29–53 | 開眼→半閉→閉眼→開眼 | 閉じ線を通って復帰。全閉時は蓋状、半閉時は厚い縁。自然な瞼としてHOLD |
| 57–81 | 頭yaw/nod/tilt・復帰 | 顔の体積は大きく崩れないが、葉と首根が硬い部品に見える |
| 85–109 / 113–137 | 翼L / Rの独立開閉 | 左右が別に動く。根の層、膜の板状感は未解消 |
| 141–165 | 両翼の限定fold | 後方スイープに留まり、自然な収納ではない。安全なfold合格にしない |
| 169–193 / 197–221 | 低paw L / R | 差し出しと戻りを確認。肩の接合/重さ/接触はHOLD |
| 225–249 | 尾/葉 | 太い尾の外形と体積を維持。付根の重なりは残る |
| 253–277 / 281–305 | 複合L / Rと復帰 | 可動の同時合成は見える。表情/根の欠陥が残り、任意組合せの貫通なしは未証明 |

case間4frameのつなぎも映像に含む。mouthのclosedからblinkのneutral smileへ戻す遷移も含む。カメラから見えない接合面や微小な瞬間貫通を全て排除した証明ではない。可愛さ/自然さ/本人性の外観HOLDは解除しない。

PlayCanvas実GLB表示は別途 [runtime JSON](playcanvas-runtime.json) と [画面](playcanvas-playback.png) を保存。ブラウザのMediaRecorderは背景制限で17frameしか取れず、`iterations/browser-recording-throttled.*` へ失敗記録として隔離した。この動画を24fps連続性の証拠に流用しない。全frame連続映像は上記Blender実レンダーを用いる。

再現：`playback-jill-pretexture-v002.py` が各cameraの1–305 JPEGを `.proof-frames/{front,side,3q}/` に一時出力。FFmpegで3入力を24fps指定し `hstack=inputs=3`、305frame、H.264/yuv420pへ結合。中間JPEGは最終動画とframe count確認後に削除した。元blendは保存変更しない。
