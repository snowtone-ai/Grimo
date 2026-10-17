# Jill — NOW

**2026-10-17 上口W local fix：未達 / 修正候補FAIL・HOLD。** [最新原因/残欠陥/比較/再現](texture-return-v005/upper-w-local/REVIEW.md)。開始HEAD `c4043471dbac3e58a39603802ecd18794a2bb9d6`、同branch。cream帯の主因は元Wと追加mouth-skin上辺のずれ。texture単独/面隠し単独では裏の旧口内/歯が露出。別名 `jill-upper-w-local-v005.blend/.glb` と局所alpha maskを保存したが、閉/小開口の口角・下側追加面のしわ/交差、Side口腔面が残る。正式な修正版として採用しない。元v005/v004・元body全21key・UV/Rig/130骨39ch20Morph16anchor保持。fresh GLBと実PlayCanvasでも欠陥を確認、単なるHuman承認待ちではない。次は元v005から上口可視境界/閉口接触を再検討し、下側追加面をWへ大きく持ち上げる今回案を繰り返さない。全Motion量産HOLD。

2026-10-17 / `codex/jill-texture-return-v005-20261017`。**Human v004形状GOを継承し、Tripo 4K Texture付きblend / GLB / 限定PlayCanvas候補を完成。新Textureの正式外観はHOLD。全Motion量産へ進まない。**

[Evidence・残課題](texture-return-v005/Evidence.md) / [顔6状態×3視点](texture-return-v005/candidate-face-review.jpg) / [Canonical比較](texture-return-v005/authority-comparison.jpg) / [実PlayCanvas全閉眼](texture-return-v005/jill-v005-blink.png) / [成果README](../../../assets/grimo/production/jill/tripo/texture-return-v005/README.md) / [Gate](texture-return-v005/Gate.json) / [SHA](texture-return-v005/Manifest.json) / [remote照合](texture-return-v005/RemoteReceipt.json)。

形状源は `codex/jill-mouth-profile-v004-20261016` / `3e40a529cee78c521b1de703c2257953e7e4f6f1`。Rig SHA `df3891bbd11c522631202e0dd32945a788ff370477731568514261a5e4100cb7`。元Rig/Canonical/他キャラdirtyは保護。開始main `8b5d13bc38061c0d574444416a039e70b9c61930`。旧v004形状PENDINGは今回のHuman指定でGOとなったがTexture GOは含まない。

返却実名 `jill-texture-input-neutral-v004.glb.glb`（指定の括弧付き名は不在）、5,055,892 bytes / SHA `e5a76605ca3e6a6f43bc6dc9875d88923cfe3e07b44f3439a9c05e987b1cc117`。返却原本と無変換4K JPEGをsourceへ別名不変保管。材質1/50,698頂点への統合は、軸同一・均一倍率1.00048863888・UV1/4096量子化・seam分割差。位置だけの最近傍ではなくUV/corner/winding/face全被覆を双方向照合し61,321faceの単一対応、23owner復元を証明。微小UV縮退は残るため細部完全復元の主張なし。

返却mesh/UVは採用せず正本UVへ画像のみ転写。23材質へUV0明示。v004 host口肌mask / v003 owner mask・瞼・眼周囲・口腔/舌/歯・翼裏/葉根coverageを使用。固定の開眼/開口/二重印刷線を除去し角は桃色の局所候補へ。実JPEG/Canonical採色は暫定、承認RGB/診断paletteではない。

保存blend再読込でGeometry・全UV・130骨/39ch/20 Morph/16 anchor・owner/weights/driversの差0。fresh static GLB importは全31,696 source頂点被覆、顔7状態（復帰含む）の位置差最大3.073e-7m。Front/Side/3Qの顔・翼/尾/複合と裏面をactual renderで開いた。PlayCanvas 2.22.2 WebGL2で23skin/20morph/16anchor/4K UV0と9代表状態・短い連続再生・neutral復帰を確認。確認clipは5.875秒、汎用39ch solver/全Motion/mobile認証ではない。

**HOLD:** 全閉眼の盛り上がる瞼縁/外眼角の暗い隙間は保持形状に残る。Canonical腿クローバーは返却にもBody-onlyにもなく左右/位置/輪郭のHuman判断が必要。桃色角のmask境界/色、肌green/cream連続性もHuman確認待ち。勝手に造形変更/クローバー創作/外観GOへ進めない。

旧形状経緯は [v004 Evidence](mouth-profile-v004/Evidence.md)、塗装契約は [v003 TextureSpec](rig-pretexture-technical-v003/TextureSpec.md) / [v004 TripoHandoff](mouth-profile-v004/TripoHandoff.md)。最新候補はv005、形状正本はv004を維持。
