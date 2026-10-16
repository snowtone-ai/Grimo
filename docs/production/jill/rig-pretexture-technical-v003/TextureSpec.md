# Jill v003 — Texture specification

2026-10-16。技術候補の塗装契約。正式Texture、配色承認、Human最終GOではない。

[v002仕様](../rig-pretexture-v002/TextureSpec.md)のCanonical、承認Body-only、桃色horn、クローバー、柔らかな緑の肌/葉、クリームの腹/膜、眼/口内の意図を継承する。体型・シルエット・眼の大きさ・葉/翼/足/尾を描き換えない。角の領域maskとクローバーの左右位置・輪郭は正式生成前にHuman確認が必要。未承認RGB swatchは作らない。

UV契約はv003へ置換する。Rigのactive/UV0は `Jill_Texture_UV0_v003`。UV1はv002 active、UV2は元sourceを完全保存した履歴であり、返却BaseColorの参照先ではない。入力FBX/GLBにはUV0一層のみ。UVを再packしたので、v002画像をUV名だけ変えて流用しない。

4Kが画像往復まで実証した基準。8Kは余白/密度の測定上候補で、maskと転写をその解像度で再生成・照合してから受入れる。2Kは余白のみPASS、細部paint未実証。1KはHOLD。重複共有なし。眼と左右クローバーの固有配色が可能。

| 所有領域 | 画像処理契約 |
|---|---|
| eye_L/R | 独立した実眼面だけに眼/瞳。左右の対応を確認。瞼/顔へ開眼を印刷しない |
| lids-L/R / mouth-skin | 承認肌色で連続充填。閉眼への眼、閉口への口内/舌/歯の固定印刷を排除 |
| mouth-inner / tongue / teeth | 実立体内部だけに承認口腔色/舌色/歯色。肌ownerへ漏らさずMorph遷移で確認 |
| wing L/R front/back/edge | 表裏・端に固有atlas領域。法線分類にはframeも入るので、膜クリーム/骨格緑のart maskは実面を見て別確認 |
| leaf owners / body_skin | 葉根・裏面はneutralからの可視性を仮定しない。owner maskで欠落補充。頭葉根はsurface内、尾葉は継承R component内。黒い焼き込みで接合を隠さない |

全polygonの所有は [material-ownership](material-ownership.json)、画素IDは [paint-owner-mask](paint-owner-mask.json)。材質分割はpaint受渡し用、異なる見た目の再設計ではない。23clay材質を返却時に不用意に1枚へ統合しない。1枚のBaseColorを23ownerへ同じUV0で明示参照させる。

`sanitize-jill-return-v003.py` の承認色充填を必須とする。4K画像、対応するowner mask、6ownerの明示RGBが必要。診断色 `synthetic-fills.json` は試験専用で、本番へ流用禁止。隠れ面の色とMorph状態が一致するか、closed/mid/open、blink/mid/open、翼表裏・根の実レンダーを開いて確認する。

BaseColorはsRGB。Normal/ORMは非色データ、ORMの各chは実返却で確認。今回の証明はBaseColorのみ。UVを変えた返却のtangent-space Normalをそのまま元UVへ貼らない。bake/継ぎ目/軟らかさを別途確認するまでHOLD。強い鱗、金属、焼き込み陰影、葉を骨/棘に変えるNormalを加えない。

受入れ時はCanonical/Body-onlyのfront/side/back、顔3QとMorph遷移を実レンダーで比較しHuman判定する。現候補の外観OKは新しいTextureや全poseの承認を兼ねない。
