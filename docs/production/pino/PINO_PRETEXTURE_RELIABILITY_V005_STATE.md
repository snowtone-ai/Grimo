# Pino C Pre-Texture Reliability v005 — STATE

2026-10-17 JST。branch: codex/pino-pretexture-reliability-v005-20261017。
source v004: fe39c6d8aab1e550ee31823ca29e85b9b2658632。
共有規則 main（最終確認）: 28c1505b7aadf63db25f1be97eba8b99cd332cee。

**今回のCodex範囲完了 / Human Pre-Texture Gate=PENDING / Human visual GO未取得。**
次工程はHuman確認後のTripo Texture。実Tripo操作・課金・完成Texture生成なし。

[REVIEW](evidence/pretexture-reliability-v005/REVIEW.md) /
[次の入力・画像返却契約](evidence/pretexture-reliability-v005/TEXTURE_CONTRACT.md) /
[編集資産](../../../assets/grimo/production/pino/candidate-c/pretexture-reliability-v005/README.md)。

前面Skinだけ局所unwrap、眼は元chartを拡大し、共通atlasへ再配置。4Mesh維持、Smart UVなし。
4K密度中央値は顔524→1,790、眼524→2,104px/m。顔の局所歪み増加は描画と共に開示。
UV重なり/範囲外/ゼロ面積0。Basis/Geometry/Rig/Morph/normal/材質所有は保護。
保存MasterとGLB/mapのUVを同期し、保存/再import確認。
無着色Neutralの正面・側面・3Qはv004とpixel一致。原本とv001〜v004は未変更。

Canonical参照の仮色/Checkerで表情、接触・低い休息の中間/極値、尾を描画。
UV維持/変更の模擬donorから画像だけ返却。口内/lidの毒色遮断と3重尾殻の所有対応を確認。
形状/所有不一致や未対応設定はHOLD。実Tripoの4Mesh/UV/topology/材質互換はUNVERIFIED。
UV変更の再samplingではSkin継ぎ目2辺に20/255超の差が残り、完成模様・mip/runtimeは未検証。

接触時の腕/脇、休息の腹/足の支持、閉眼側面、尾の既存形状はHuman visual HOLD。
自然な臀部支持の座りや全Motionを承認していない。新たな構造的阻害は限定試験で未検出。
G1/G2のHuman判断を技術PASSで代替せず、このgateで停止する。
