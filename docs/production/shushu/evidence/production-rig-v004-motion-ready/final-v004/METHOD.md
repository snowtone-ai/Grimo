# Shushu v004 — 原因・構造・適用限界

この記録のv004は別名の再審査候補。v003の技術PASSは、今回の腕・口・腹についてのHuman FAILを取り消さない。追加指示により、腹以外も含めた全身の意図しない凹凸と潜在的な姿勢依存の面の乱れを対象とした。意図した耳・頬・短肢の丸みまで平坦化することは目的としない。

## Authorityと再現

開始点は制作branch `codex/shushu-v004-motion-ready-v003-20261016` の `56ffdc6356c8b3367990d30d6b50d6fcc011126e`。最新mainのAGENTS/Goal√map/Handoff、Canonical、Human承認済みv004、final-v003のREVIEW/METHOD、実Blend/GLB、製品loader/controllerを照合した。原本・他キャラ・並行差分は編集せず、隔離checkoutで新しい名前だけを作成した。

添付580/581/582の整数秒表示だけでは単一フレームを確定できない。元desktop動画は640×640、MediaRecorderの実時間と診断24fpsのフレーム番号は一致しない。元動画・収録ledger・Blend制御値を突き合わせ、腹の座位移行、両Hold＋開口、片側SelfContact＋MouthCloseの前後を特定した。中心の検査姿勢はf1089/1101/1113、隣接はf1085/1095/1107/1117/1119/1125。対応の確度と画像hashはSOURCE.jsonに記載する。

## 腕 — carrierの役割と形状生成を分離

**観察：** v003はSpine2 carrierに左右各438 Shapeを加算する方式。全体を肩から回すような形と、中間組合せの補正が、短い厚い前肢を硬い塊に見せる。旧arm FKはこのcarrier方式の有効な変形入力ではない。

**採用：** carrierと既存438名・入力書式は搬送/補間の契約として残し、形状の生成則を作り直した。肩の小さな回転に、長さ方向に分布する肘の屈曲を組み合わせる。513点の単位接線積分で中心線を作り、断面をparallel transportして厚みを運ぶ。内部の付け根capには根元の遷移を付ける。Wristは末端側へ分布させる。2 Purposeの中点は実際の中間パラメータから生成し、単純なendpoint平均との差をpair Shapeへ保存する。

**棄却：** 固定根元から手先だけを合わせるcubic方式は中間で体積減少・接触悪化を生んだ。肩一軸の大きな円弧も頬/頭への交差を生む。旧438個を名前だけ維持して同じ動きを微調整する案は採用しない。旧Arm FK互換の回復も、この変更で達成したとは主張しない。

**Hold Anchorの実修正：** 旧一定前方0.031オフセットでは、半径0.030の接触用球が実面へ入る状態があった。v004は実表面点＋0.031×姿勢空間の表面法線へ変更。Basis法線と438個の法線差をGLB extrasに保存し、Blender driverと製品controllerの両方で同じ重みを使う。export時に頂点順序が変わるため、製品側は保存したrest座標で対応点を探す。bone parentのtail offsetも補正した。法線オフセットは節点間では補間近似であり、任意小物の接触を保証しない。

製品は `shushu-v004-loader-v004.mjs` とこのv004 GLBを対で使用する。Hold>SelfContact>Offerの優先、左右Purpose/Wrist/Seat、解除してclipへ戻る契約は維持。旧v003 loader/assetは残した。7 Anchorの存在・再読込・製品追従を別々に確認した。

## 口 — 古い閉口chin変位の二重加算

**観察：** 別Meshの下顎が脱落したのではない。Headの古い`MouthClose`が、W口を保持したまま5821頂点の顎側へ最大約0.0286Hの変位を加えていた。一方、開口・口内・舌の閉じる優先制御は既に存在した。閉口の一瞬で古い顎面だけが突出し、下口縁が離れたように見える。

**採用：** Head.MouthCloseの古い加算変位をBasisへ戻した。閉口は既存のMouthOpen抑制・口内制御に任せる。Human OKのW境界256頂点は全Shapeで元座標を維持し、鼻下紐を復活させない。Head/MouthInterior/OralBowl/Tongueを実評価し、81段階の閉→開→閉にSmile/Joy/Tongueと左右Purposeを重ねた。有限値だけでは分離なしの視覚証明にならないため、口の原寸拡大と連続動画を併記する。

## 腹と全身の凹凸 — 実座標の修正

**原因の切分け：** 元のTorso三角形と頂点を保持して調べた。例はv1561/1590のtri5664、v2406/2411周辺tri3646..3656、v2577/2583周辺tri3565..3586（全列挙はbelly-cause-witness/triangle記録）。TrueSeat correctiveをmuteしたraw Skinと比較し、座位補正が局所的に変位を急変させることを実証した。material/影の除去だけ、custom normalの解除だけ、診断上の頂点weldだけでは原因を解消しなかった。これらを修正として採用していない。

**採用：** UV相当の重複点を計算上まとめて隣接面をfairingし、実頂点へ変位を戻す。Basis変更は対応する全Shapeへ同じ差分を与える。HeadのW/眼/鼻、Torsoの足裏接地を保護する。Head・両耳・Torso・両Pawを対象にし、残る全Meshもinventoryと評価検査へ入れる。48個のTrueSeat節点では、接地帯を保護しながら実際のposed面をfairingし、逆LBSでShapeへ戻す。

面のfairingだけで残る腹の変位急変には、同じ姿勢のraw Skinとの差（corrective変位場）を隣接4段で低域化し、前腹部の局所mask内で最大0.012Hの実変位として再構成した。逆LBSの目標と再評価形状も照合する。形状修正の後にのみ、古いcustom normal/sharp属性を外し、修正済み三角形から角度加重法線を再計算する。非表示、material置換、照明変更で欠陥を隠す修正は行わない。粘土表示は診断用で、納品assetには元material/画像/UVを残す。

最終全身確認で残る面も再調査し、強い追加Taubin平滑化、足裏近くまでの平滑化、全体boundsへ戻す強い平滑化を診断別名で比較した。眼周辺や足の承認形状を悪化させたため棄却した。最終rest修正は24/32/48段の局所low-passと滑らかなtanh上限に絞り、孤立した未使用頂点を隣接処理から除く。posed面は別のbalanced passで処理する。W境界は計算上の重複頂点平均だけでは微小に動いたため、同位置のUV相当頂点まで最後に実座標を厳密固定し、検査で全key差0を必須にした。

`physical-surface-comparison.json`は同じ元前腹部の辺を各version自身のBasis長で正規化する。修正後の短くなったBasisを元の長さだけで割る比較は採用しない。Laplacian、面積、体積proxyは意図した曲率やUV境界も含むため、美観の自動合否には使わない。

## Gateの読み方

Blender→保存GLBの14Mesh座標と7 Anchor、PC製品経路の実現在面・法線・7 Anchor、raw Purpose入力と解除復帰を照合した。元の8-weight Torso経路と2 Paw現在面法線処理を継続利用する。三角形交差検査は内部付け根の意図した接合を除いたdistal領域、ray parityは選んだ制御格子で実施する。接触球の余裕、体積proxy、有限値を「全ての連続入力が欠陥なし」へ拡張しない。

Humanは承認済みv004/Canonicalと比較し、短肢の厚み、肩から肘の柔らかさ、左右差、頬下の余裕、閉口と複合表情、腹・背中・足・耳・頭の微細な面、座位の重さ、保持/割込み/復帰を判定する。見つかった意図しない凹凸は追加修正対象。Human外観GOは未取得。スマホは新候補未検証UNKNOWN。原本置換とMotion量産はHOLD。
