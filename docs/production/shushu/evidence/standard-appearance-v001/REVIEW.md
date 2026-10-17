# Shushu 標準外観 v001 — Human確認候補

**最新Human判定：足裏 PASS、v001花 FAIL（ペラペラ感・安っぽさ）。[改修v002](../standard-appearance-v002/REVIEW.md)はHuman PENDING。既存v004比較ページはHuman外観PASS。phone UNKNOWN、原本置換・Motion量産はHuman GOまでHOLD。**

以下はcommit `151d8718` 時点の制作・検証履歴。v001 delivery-manifestは当時のsnapshotであり、この最新追記のhashを含まない。 技術確認を美観承認に読み替えない。

[比較ページ](index.html) ／ [PC標準装備ON・操作](runtime.html) ／ [構造契約](STRUCTURE.md) ／ [一次出典](SOURCES.md) ／ [納品hash](delivery-manifest.json)

## Authorityと資産

最新main `336997db2b95244c17774258e2f5ff874a2adbc1` のAGENTS・Goal√map・Handoff、制作branch `codex/shushu-abc-motion-repair-v004-20261017` の実物・差分・Review・loaderを照合。装備の正本は既存 `assets/grimo/source/shushu/shushu-Identity-canonical.png`。蝶・浮遊花びら・手持ち花は対象外。赤線添付自体はこの会話から再取得できず、赤線形状を作っていない。

既存承認は [final-v004/REVIEW](../production-rig-v004-motion-ready/final-v004/REVIEW.md) に記録。対象は制作HEAD `8d3235f0b176088f2434ee482aa5d14d7b94ef58` の比較ページと元GLB SHA256 `a082195104713c21b9a219ff19bd9d37702486aaa4cdf2bbf2e9f0ad58b5c91f`。古いmanifest/動画は当時のsnapshotであり、今回の追加装備の承認根拠にはしない。

追加資産は `assets/grimo/production/shushu/equipment/standard-v001/`。編集可能な独立花GLB/Blend、両後足裏のPNG、装備組込みの別名proof Blendを保存。製品は**既存v004 body GLB＋独立花GLB＋肉球PNG**を合成し、元GLBを置換しない。

花/葉は12 Meshを1 item rootに集約。主花2輪各5花弁、小さい中央重なり、5葉、曲面薄殻・裏面萼/花床/柄を持つ。matte roughness 0.86。頭部ローカルAnchorで追従し、通常loaderで自動装備する。`standardAppearance:false`、`equipment.setEnabled(false)`、`equipment.dispose()`で制御可能。Torso材質は複製し既存skin/morph/8weight互換処理を維持、後足裏だけをUV描画。前足に追加なし。

## 制作と検証

4視点blockout投影を先行確認後、花弁曲率・縁・花芯・萼と接点を精細化。側面の取付け部も修正し、最終資産からauthorと再読込を再収録した。blockoutは制作順の記録でありHuman承認ではない。

| 検証 | 結果と証拠 | 適用限界 |
|---|---|---|
| 原本保護 | [preservation](preservation.json): 14 MeshのBasis/全Shape/UV/面/weight一致、source Blend hash不変 | 新Torso複製材質の肉球だけ意図的変更 |
| 肉球UV | [pad audit](pad-texture-audit.json): 2048²、変更103492 texel、mask外差0 | Canonicalへの形/色/向きの最終一致はHuman確認 |
| 保存GLB | 独立GLB再読込、同じ肉球PNGで36枚。validator error/warning 0 | unused UV情報4件。数値は美観承認ではない |
| 同条件の再読込比較 | [36枚のRGB平均絶対差](roundtrip-comparison.json)の最大0.002627/255 | glTFの法線/材質丸め等を含む。PCとのpixel比較ではない |
| author画像梱包 | [packed PNG hash](author-texture-pack.json)が出荷PNGと一致 | 途中のImage.copy由来の旧packed bytes残留を修正し、authorだけ再収録 |
| PC製品経路 | 実v004 loaderの既定ON、36装備ON画像＋2枚OFF、座位/復帰動画 | Engine 2.22.2、640²、PC WebGL。phoneへ拡張しない |
| 頭追従/切替 | 192 clip sampleでHead-local/合成行列誤差0、GL error 0、材質復帰・解放を確認 | Anchor一致だけでは貫通/眼遮蔽を証明しない |
| 花/葉の近接 | [13姿勢の頂点検査](visible-clearance.json)でHead/耳に対する最小近接距離約0.00955H、内向き1mm超の頂点0 | 取付け裏面は接触を意図し除外。厳密な三角形交差/全入力の証明ではない |
| Motionの実姿勢 | 頭左右/傾き＋瞬き、左右耳、座位、左右足上げ、顔複合、座位/保持/復帰を3経路で対照 | 診断clipであり量産Motionの承認ではない |

各画像のframe/view/hashはauthor/saved/pcのledgerを参照。Front/Side/左右3Qは中立・座位・遷移極値、頭/耳/足上げはFrontと右3Q。各経路内はカメラ・light・material条件固定。authorに残っていた旧review用light/groundを表示時だけ除去し、author/saved双方に同じ2灯・1面を生成、ledgerのcaptureSettings一致を検査した。BlenderとPCの別renderer間では照明/色変換差があり、pixel同一を要求していない。肉球は既存面と一体なので別面の浮きやZ-fightingを導入しない。

## Human確認点と残るGate

1. 原画と主花2輪の大小・傾き・重なり・先端切れ込み・濃桃縁/淡中心/黄芯、5葉の見え方が一致するか。中央が第3の大輪に見えないか。
2. Side/両3Qで花弁が板や風船に見えず、萼/柄/葉柄の取付けが自然か。柔らかいIdentityの質感に合うか。
3. 頭左右・傾き・瞬き・耳可動で取付けの浮き/刺さり/眼遮蔽がないか。有限姿勢の画像/頂点近接検査を任意連続入力の保証に拡張しない。
4. 両後足の大中央1＋上側3の形/比率/色/向きをCanonicalと照合。足上げ・接地・座位/復帰で境界が自然か。

今回USB/ADB/phone操作、課金/Tripo、原本置換、他キャラ変更、量産実行なし。追加装備のHuman GOはまだ受け取っていない。

## 再現

repo rootからBlender 5.2で `scripts/blender/build-shushu-equipment-v001.py -- --blockout`、続いて同script（引数なし）を実行。`verify-shushu-equipment-v001.py -- --author` と引数なしでauthor/保存GLB画像、`audit-shushu-equipment-v001.py`で有限姿勢の近接検査を生成する。各scriptは `blender -b -t 4 --python-exit-code 1 --python <script>` で起動する。

`node scripts/3d/review-shushu-equipment-v001.mjs`でlocalhost:8772を起動し、`node scripts/3d/capture-shushu-equipment-v001.mjs`でPC収録（Windows Chrome、CDP9232）。`node scripts/3d/validate-glb.mjs <花GLB>`で構造検証。入力原本は書き換えず、既存の無関係な未追跡ファイルはstage対象から除外する。
