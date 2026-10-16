# Jill — NOW

2026-10-16 / `codex/jill-pretexture-technical-v003-20261016`。**4K BaseColor基準のPre-Texture Technical GO候補を実装。Human最終GO PENDING、Tripo実行HOLD。** 現候補へのHuman「見た目はOK」は保持し、全poseの承認へ広げない。

継承 `3de7b2e46b839a4ec970f58d8c5e8a99c4580f9e`、確認main `73617ce2d3c724c86aed82dfc2a09cd220e5d194`。旧Jill worktreeは開始時clean、元checkoutの並行Shushu変更を保護。専用worktree `C:/Users/chidj/.codex/worktrees/jill-pretexture-technical-v003/Grimo`。旧正本/旧Evidence/元UV/他キャラは不変。

[投入候補・Rig派生](../../../assets/grimo/production/jill/tripo/rig-pretexture-technical-v003/README.md) / [EvidenceとHOLD分類](rig-pretexture-technical-v003/Evidence.md) / [SHA・絶対パス](rig-pretexture-technical-v003/Manifest.json) / [remote照合](rig-pretexture-technical-v003/RemoteReceipt.json)。Rig blend SHA `ad9f867e87a6006259aec5d8b01e1981fc823ae97bc92a87dc49a906770a9050`。

変更は必要箇所のUV再投影・島再配置・同外観の23paint owner分割。Geometry/topology/normal/Rigの再制作なし。130骨/39ch/20 Morph/16 anchor、Basis/全Morph/weights/drivers/anchorsの契約一致、8代表状態の評価頂点差0。元activeと元source UVはUV1/UV2へ完全保存、新UV0は `Jill_Texture_UV0_v003`。

UVは63 overlap pair→0、縮退UV0、61,321三角形/2,203島。4K最小島間23.894px、tile端20.144px。1KはHOLD、2Kは余白PASS・細部paint UNKNOWNで主候補外、8Kは測定上候補（実画像往復は4Kのみ）。微小な旧sliver伸びとGeometry縮退1枚は残し、細密図柄の品質を保証しない。

[顔front/side/3Q遷移](rig-pretexture-technical-v003/face-review.jpg) / [翼fold/open比較](rig-pretexture-technical-v003/wing-regression.jpg) / [診断色](rig-pretexture-technical-v003/diagnostic-review.jpg)を開いて確認。24対のclay最大差4/255、最大6画素/480²、翼6対はpixel一致。新しい外観回帰は見当たらない。厚い蓋状瞼/side隙間、板状顎/二重口縁、口内造形、根の層、0.30rad sweepのみのfoldは保持。これらは現形状凍結の範囲で塗装後へ延期可能だが、品質承認はUNKNOWN。Humanが形状/面接続変更を求める場合はTexture前へ戻し本候補GO失効。

FBX/GLB合成返却→画像だけ元Rigへ→packed blend保存再読込→Rig GLB fresh importを実証。UV0/1/2、baseColor texCoord=0、130骨/20 Morphを確認。UV変更の合成GLBも全61,321三角形を一意対応し元UV0へ転写、5,252,720画素の差0。実返却remesh/異なる三角形化/Normalの保証ではない。既存305frameを重複実行せず、全Motion/mobileは別gate。

[Texture仕様](rig-pretexture-technical-v003/TextureSpec.md) / [Tripo引渡し・停止条件](rig-pretexture-technical-v003/TripoHandoff.md)。閉口肌/瞼は承認paletteでowner充填し開口/開眼印刷を排除。隠れ口内・翼裏・葉根もmaskで補う。承認palette/角mask/クローバー、実UI/対応解像度/Original UV/料金/実返却は未確認。Original UV不可やowner/geometry対応不明なら停止。upload・課金・正式Textureは未実施。Human最終GOを代行しない。

継承資料は [v002 Evidence](rig-pretexture-v002/Evidence.md)、さらに旧状態は [v001 Evidence](rig-other-v001/Evidence.md)。旧資料のHOLD文言は履歴として残し、NOWはこの文書とv003 Evidenceで判定する。
