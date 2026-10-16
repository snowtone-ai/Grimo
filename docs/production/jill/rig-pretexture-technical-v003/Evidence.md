# Jill v003 — Pre-Texture Technical GO候補

2026-10-16。**4K/8K BaseColor用の技術候補を実装済み。Human最終GOはPENDING、Tripo実行はHOLD。** 現候補へのHuman「見た目はOK」を保護する。全pose承認、Motion完成、正式Texture承認を意味しない。

G3のUV・画像受渡しを成立させ、G2の塗装後手戻りを減らす。G1の本人性・可愛さを変えず、G0の愛着を損なう再設計はしない。旧正本・旧Evidenceは上書きしていない。

## Authority / NOW

- 開始時の元checkout: `codex/shushu-v004-motion-ready-gate-20261015` / `a4a90851c1ff85e584671f7c3decd7561e2baea1`。既存のShushu PNG変更とuntrackedを保護。
- Jill元worktree: `codex/jill-pretexture-v002-20261015` / `3de7b2e46b839a4ec970f58d8c5e8a99c4580f9e`、開始時clean。これを継承した専用worktree・別branch `codex/jill-pretexture-technical-v003-20261016` で実装。
- fetch済みmain `73617ce2d3c724c86aed82dfc2a09cd220e5d194` のAGENTS、Goal√map、production/Handoffを確認。Jill HANDOFF、v002 Evidence/TextureSpec/TripoHandoff/Manifest、Canonicalと承認Body-onlyも確認。未承認poseを承認参照にしていない。
- 入力・成果物の絶対パス、bytes、SHA-256は [Manifest](Manifest.json)。入力候補は [asset README](../../../../assets/grimo/production/jill/tripo/rig-pretexture-technical-v003/README.md)。角の桃色指示など既存仕様は [TextureSpec](TextureSpec.md) を継承。

## 残HOLDの分類

| 論点 | 分類 / 現在 | 理由・条件 |
|---|---|---|
| 意図不明UV重複、追加瞼・口内の強い伸び、余白 | Texture前必須 / 今回補修 | 塗装の混線・滲みは後から画像だけで救済しにくい。63 overlap pairを0へ。下表の解像度制限を守る |
| 眼/瞼、閉口肌/口腔/舌/歯、翼表裏/端、葉根の所有 | Texture前必須 / 今回確定 | 23 owner、全polygonを一意に割当。全ownerにatlas画素あり。隠れ面の生成品質は別問題 |
| 閉口肌への開口印刷、瞼への開眼印刷 | Texture前必須 / 防止経路を実証 | owner単位の明示色充填と4px gutter。実返却を受入れる際に承認paletteで必ず再実施。未承認色で正式塗装しない |
| Rigへ戻す際のUV0/UV1誤参照、material混線 | Texture前必須 / 合成FBX・GLBで実証 | 画像のみ戻す。UV0を明示。保存blend再読込・Rig GLB fresh importまで確認 |
| 厚い蓋状瞼、半閉眼side隙間、板状顎/二重口縁、口内の造形 | 安全に延期 / 現形状凍結の範囲のみ | 既存の外観を変えず塗装できる独立領域とMorph一致を確保。品質自体は改善・承認していない。Humanが面接続/形状修正を要求する場合は延期不可、Textureを止めて別名派生・再検証 |
| wing foldの0.30rad後方sweep、膜の柔らかさ、葉根の層・weightの自然さ | 安全に延期 / 現topology・UVのままpose調整する範囲のみ | Texture所有は分離済み。自然な収納poseや全Motionの完成とは言わない。膜追加/根の作り直しが必要ならGO失効、Texture前へ差し戻す |
| 全poseの可愛さ、承認済み閉眼/閉口/fold極値参照 | UNKNOWN / Human判定待ち | 現候補の外観OKは全poseへの委任ではない。技術一致で解除しない |
| 実Tripo UI/Original UV選択可否/対応解像度/料金/実返却品質 | UNKNOWN | upload・課金・生成を一切していない。旧公開案内を現UIの実証と扱わない |
| 実返却のremesh/異なる三角形化、Normal/tangent、全Motion・mobile | UNKNOWN | 今回のUV-only・BaseColorの範囲外。既存305frameを再実行していない |

「安全に延期」は造形品質のPASSではなく、現候補を凍結したままBaseColorを作る技術上の順序判断。形状変更が必要かHumanが決められない場合はUNKNOWN/HOLDのまま実行しない。

## UV測定と必要最小限の補修

[before](before-uv-audit.json) / [after](after-uv-audit.json) / [補修対象polygon](uv-repair.json) / [atlas前](before-atlas.png) / [atlas後](after-atlas.png)。Blender 5.2.1 LTS。Shapely三角形交差面積 `>1e-12 UV²`、同じposition+UV edgeによる島、島polygon間の距離で測定。重複を意図的共有と推定しない。今回の許可共有は0。

| 測定 | v002 | v003 |
|---|---:|---:|
| 三角形 / 島 | 61,321 / 2,111 | 61,321 / 2,203 |
| 正面積overlap pair / UV縮退三角形 | 63 / 0 | **0 / 0** |
| 最小島間距離UV | 0 | .0058335241 |
| tile端距離UV | audit参照 | .0049179383 |
| atlas union面積 | 34.012% | 31.323% |

元Geometry縮退三角形1枚は残る。collinearな既存quadへ凸UVを与えて交換時のUV縮退を避けたが、ゼロ面積Geometryの塗装ディテールを保証しない。形状・topologyを削除していない。

| 解像度 | 最小島間px | tile端px | 島間8px未満pair | 密度 p05 / median / p95 (px/m) | 判定 |
|---|---:|---:|---:|---|---|
| 1024 | 5.974 | 5.036 | 3,864 | 283.9 / 303.1 / 316.7 | HOLD、4px両側gutterを満たさない |
| 2048 | 11.947 | 10.072 | 0 | 567.8 / 606.2 / 633.3 | 余白PASS、顔・細部の実塗装はUNKNOWN。主候補外 |
| 4096 | 23.894 | 20.144 | 0 | 1135.5 / 1212.5 / 1266.6 | 技術候補。4px充填を実証 |
| 8192 | 47.788 | 40.288 | 0 | 2271.0 / 2425.0 / 2533.2 | 測定上の技術候補。画像pipelineは4Kのみ実証、8K実画像は返却時再検証 |

8pxは今回のBaseColor両側4px充填の判定値で、全mipmap/圧縮/Normal用途を保証する規格値ではない。密度はrest pose三角形のUV面積/実面積平方根、伸びは接平面からUVへの主伸長比。pose中の再unwrapはしない。

追加瞼L/Rのanisotropy p95は94.20/94.33→1.164/1.142、口肌24.76→1.137、口腔24.94→1.063、舌21.21→1.156。元領域p95は1.290、最大100.282の極小sliverが残る（伸び>4の面積比0.0001388%）。そこへの細密図柄は対象外。同系色充填で受け、細密paint要求ならHOLD。翼L/Rのp95は1.260/1.297。眼には約2倍の線密度を配分。部位別全値はauditに保存。

追加顔面と重複に関係した元50polygonだけ再投影。他の元島は相似変換・再配置。左/右体と眼に重ね共有なし、左右固有クローバーを描ける。クローバーの意匠/配置が正しいかは正式画像でHuman確認。

## Material / 隠れ面

[全polygon所有](material-ownership.json) / [uint16 owner mask](paint-owner-mask.png) / [IDと画素数](paint-owner-mask.json)。23材質は既存clayからの同外観コピー。body_skin、eye_L/R、lids-L/R、mouth-skin/inner、tongue、teeth、wing L/R front/back/edge、leaf head/neck/tail ownerへ分割。翼の表裏はrest法線Yで分類しframeも含むため、膜/骨格の最終配色マスクとは別。葉根は既存leaf bone weight平均<.5で分類。頭葉はsurface owner内に根も含み、tailは継承componentのR ownerに連続する。新しい左右/根を捏造せず、全polygonがどのownerで塗られるかを確定した。

4Kで歯323、舌3,638、口腔10,015、瞼L/R 10,079/10,318画素など、23ownerすべて0画素なし。これでUV上の塗装先は存在するが、neutral視点から隠れた膜裏・葉根・口内までTripoが塗るとは証明していない。返却後はmask充填または対応UV転写で補い、裏面poseを実レンダーで開く。

`sanitize-jill-return-v003.py input.png output.png fills.json` は瞼L/R、口外肌、口腔、舌、歯の明示RGBを必須とし、4pxまで充填。隣の所有面へ触れる場合や解像度が4096と違う場合は停止。[充填試験](protected-fill-proof.json)は診断色のみで全対象PASS。承認済みswatchを捏造せず、実返却は承認色を与えるまで受入れHOLD。眼を肌へ、口内を閉口面へ焼かない。8Kはmask再生成・解像度/余白の再検証が必要。

## Rig保持・実レンダー

[保存契約](preservation-proof.json): Basis、polygon順、20 Morph全座標、weight/group、130 bones rest/parent、drivers、39ch、16 anchorの契約が一致。元activeとsource UVをそれぞれ第1/第2保存層へbit一致で保持。neutral、mouth close .5/1、open 1、blink .5/1、wing fold/openの8状態で全評価頂点差0。

新active/UV0は `Jill_Texture_UV0_v003`、保存層はUV1 `v002_Previous_Active_Preserved`、UV2 `v002_Source_UV_Preserved`。Texture入力はUV0だけ、Rigは3層を維持する。

[顔のfront/side/3Q遷移](face-review.jpg) / [翼fold/open前後比較](wing-regression.jpg) / [診断色](diagnostic-review.jpg)を実レンダーで保存し開いて確認した。24対のclay比較は最大4/255、1枚480²中最大6画素差（材質分割後の境界に限る）、翼6対はpixel一致。[差分の全値](render-regression.json)。pixel完全一致とは記していない。新しい形状・見た目の回帰は見当たらず、既存の厚い瞼・顎・隙間はそのまま残る。Humanのpose承認を代行しない。各状態は39chを独立resetして評価した。連続した極値→回復の今回の再生検証や全Motionは再実行していない。

## 保存・reimport・画像返却の実証

[FBX/GLB proof](transfer-proof.json): 同じneutral surfaceからTexture専用FBX/GLBを作成。診断画像を持つ合成返却をfresh importし、owner+座標+UV cornerを双方向照合。GLB位置差0、UV差2.98e-8、FBX位置差1.744e-7m、UV差0。両形式で4096²画像のdecode差0。画像だけを元Rig派生へ戻し、packed blend保存・再読込、neutral Rig GLBをexport/fresh import。130骨/20 Morph、TEXCOORD_0/1/2、baseColor texCoord=0を確認。再import位置差最大3.073e-7m、UV差2.98e-8。

保存返却Rigから[GLB閉口](renders/returned-glb-closed.png)/[閉眼](renders/returned-glb-blink.png)、[FBX閉口](renders/returned-fbx-closed.png)/[閉眼](renders/returned-fbx-blink.png)をrenderし実画像を開いた。外肌・口内・眼・瞼の所有が保持される。診断色を正式配色と扱わない。Rig solverがglTFへ移植された証明ではない。

[UV変更proof](uv-changed-transfer-proof.json): U反転UV+反転画像の合成GLBを保存・fresh import。全61,321三角形をownerとGeometryで一意対応し、barycentricで元UV0へ焼き戻し。曖昧/欠落/UV縮退0、5,252,720画素で元診断画像との差0。隣接する眼/瞼/口へray投影を飛ばさない。**同じGeometryと三角形構成のUV変更だけ**を実証。実返却remesh・異なる三角形化・変形・owner欠落には自動適用しない。Normal/tangent再bakeは未実証。

## Gate / 次の停止条件

技術候補は4Kを基準、8Kは測定上成立。実UI・解像度・Original UV・承認palette・部位マスク・実返却後検査が揃わなければ実行/受入れHOLD。[TripoHandoff](TripoHandoff.md)に停止条件と転写手順を固定した。Human最終GOは未取得。upload/料金発生/正式Texture作成は未実施。commit・push後の照合は [RemoteReceipt](RemoteReceipt.json) に保存する。
