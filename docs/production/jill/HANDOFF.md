# Jill — NOW

**2026-10-18 / NOW v007: 口Human GO、Canonical腿クローバーOK、角は変更不要・現状維持。完全完成GOALは未達。** [v007 Evidence](clover-v007/Evidence.md) / [実全身PNG](clover-v007/runtime-body.png)。 [最新Evidence/差分/残作業](mouth-integration-v006/Evidence.md) / [口比較](mouth-integration-v006/mouth-detail.jpg) / [保存6状態×4視点](mouth-integration-v006/saved-states.jpg) / [実PlayCanvas閉口](mouth-integration-v006/runtime-mouth-closed.png) / [成果README](../../../assets/grimo/production/jill/tripo/mouth-integration-v006/README.md)。

branch `codex/jill-texture-return-v005-20261017`、開始 `74596c9673434f4120b300ec0c96fb9c663fc4d0` / remote一致 / clean（開始時）。最新main fetch `8b9d736abca118de5bd1e2e1f64b961e25f0ba42`。最新Human GOALはTexture込みJillがMotion/表情/中間/復帰でも承認外観を保ち、口周囲の派生不具合を解消した完全完成。技術PASSをHuman品質GOへ置換しない。

根本原因は元Wと後付けmouth-skin/口腔の別境界・位置ずれ。Textureだけ/追加上縁だけの移動は前回試作で不足。元v005から鼻下〜口の局所511 polygonと重複口外皮/口腔を共有境界の一体面へ置換。961vertex追加、歯8点をWへ追従。新しい口UVは削除owner島を再利用/分割。残存30,425 faceの3UV・既存weights・130骨/39ch/20Morph/16anchor・packed Textureは保持。開口/左右smileの3driverに閉口優先ゲート。元v005/v004・Canonical/Body-only・他checkoutのuser変更は保護。

保存blendの閉/小/大/combined/neutral/復帰をFront/Side/左右3Qで実レンダー。15同時入力中間、左右smile/頬接触/頭yaw-nod-tilt/呼吸との組合せを確認。前試作のcream帯・口角しわ・Side口腔露出は今回範囲で見えない。復帰は4視点画素一致。全39ch min/0/max有限/復帰と個別端点実画像を保存。fresh static GLBは使用30,880頂点被覆・10顔状態差最大3.073e-7m。実PlayCanvas2.22.2は13代表状態+neutral・連続再生/復帰、23skin/20Morph/16anchor/4K UV0、Morph差最大9.537e-7。

**Human決定:** 口の外観GO。腿クローバーはCanonical側だけ追加しHuman「クローバーはOK」（2026-10-18）。角は元v005から一切変えておらず、Human「変える必要はない」で現状維持。static GLBの15同時入力・21段階の連続開閉・復帰も実PlayCanvasで一致。4Morph用consumer controller同梱。

**残作業/HOLD:** Humanがv007赤線画像で、眼の外側に肌との境界線がありその外にも眼球が残る不自然さを指定。「線を消すか、線より顔の外側の眼に皮膚膜」を希望。これを次の局所原因調査/修正対象にする。既存閉眼の外眼角/瞼縁も同じ境界原因との関係を確認。口/クローバー/角は保護。全Motion量産・実機mobileは今回の限定認証範囲外。完成モデルと自己認定しない。

最新候補 `mouth-integration-v006/jill-textured-rig-v006.blend/.glb`、別bounded QA clipあり。元形状正本v004はHuman GO、元v005TextureはHuman HOLDのまま。[v004履歴](mouth-profile-v004/Evidence.md) / [v005移植履歴](texture-return-v005/Evidence.md) / [前回失敗試作](texture-return-v005/upper-w-local/REVIEW.md)。前回の失敗候補を完成品として再採用しない。[Manifest](mouth-integration-v006/Manifest.json) / [remote照合](mouth-integration-v006/RemoteReceipt.json)。

最新保存候補 `clover-v007/jill-textured-rig-v007.blend/.glb`。4K局所画素のみ、v006の全Geometry/UV/weights/Morph/driver/骨/anchor完全一致、口5状態Front画素一致。保存/GLB再import/実PlayCanvasを再確認。v006承認口公開 `d4e73c1`（remote一致）。v007 commit/remoteは[receipt](clover-v007/RemoteReceipt.json)。
