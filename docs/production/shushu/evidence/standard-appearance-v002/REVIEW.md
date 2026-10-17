# Shushu 花飾り v002 — 厚み・質感の修正

**足裏 Human PASS。v001花はHuman FAIL、改修v002花はHuman PENDING。既存v004比較ページのHuman外観PASSは維持。phone UNKNOWN、原本置換・Motion量産はHuman GOまでHOLD。**

Humanの「足裏はOK」「花アイテムが…ペラペラ感があって安っぽい。もっとプルプルでリッチな質感がほしい。改善して」を記録。v001の承認待ちを上書きする新しい判断であり、v002を自己承認しない。

[修正前後の比較](index.html) · [製品loader・標準装備ON](runtime.html) · [3D構造契約](STRUCTURE.md) · [一次資料](../standard-appearance-v001/SOURCES.md) · [納品hash](delivery-manifest.json)

## 変更

主花2輪＋小さい中央意匠＋5葉の配置と輪郭を保持し、花弁の中央に柔らかな厚み、縁に連続した丸みを持つ閉じた曲面へ変更。色の境界を滑らかにし、淡い中央と濃桃の縁を残した。中央の反射が尖る箇所を直し、広いサテン光沢へ調整。花芯は控えめな丸みを持つ黄色のまま、増した花弁厚に埋もれない高さへ補正した。葉の曲面・表裏の厚みと裏側の短い接続も整えた。

足裏PNGはSHA256 `f5c4aa2969b9b4971e3926dfede7c56cc8211091b9c074a9c67bb0738a2f21fe` の承認済み資産を再利用。元v004 GLB・proof Blend、頭/耳/身体の形・UV・Shape・weightを保護。独立花GLB/編集Blend、新しい装備proofとruntime wrapperを別名納品する。

## 検証と限界

先行blockoutをFront/Side/両3Qで確認後に精細化。Blender author→独立GLB再読込→PCの実v004 loader既定ONで、Front/Side/両3Qと頭左右・傾き・瞬き・左右耳・座位・復帰を比較した。author/savedは同じ固定camera/light、PC内のv001/v002比較も同じ身体・照明・cameraを使う。PCでは全身640²に加えて頭部を960²で収録。異なるrenderer間のpixel同一やHuman美観PASSは主張しない。

各画像のframe/view/hashはauthor/saved/pc ledger、再読込差は[roundtrip-comparison](roundtrip-comparison.json)、元14Mesh保存は[preservation](preservation.json)、承認PNGのpacked bytes一致は[author-texture-pack](author-texture-pack.json)、花GLB検証は[validator](flower-glb-validation.json)を参照。

最終収録はauthor 28枚・保存GLB 28枚、PC 40枚（現装備28・OFF 2・拡大3・旧花比較7）。author/savedのRGB平均絶対差は最大0.063152/255。元14Meshは全一致。10姿勢の可視花/葉の最小近接距離は約0.01352H、内向き1mm超の頂点0。192サンプルのAnchor誤差・GL errorは0、PC例外0、材質復帰と二重disposeを確認した。

GLB validatorのcore error/warningは0（未使用UV info 4）。同梱validatorはclearcoat/specular/sheen拡張の追加検証を持たず、stderrにMissing optional extensionを出す。この部分の見え方はBlender再読込と実PlayCanvas 2.22.2の描画で確認し、validatorだけで保証しない。

[192 clip sampleのHead-local追従](pc/attachment-and-toggle.json)、材質の切替・[解放](pc/lifecycle.json)、[PC例外](pc/errors.json)を記録。[花/葉とHead/耳の頂点近接](visible-clearance.json)は10姿勢での有限検査で、裏側の意図した接点を除く。厳密な三角形交差や任意入力の証明ではない。既承認の足裏構造に新しい面やMotionは追加していない。

Human確認点は、正面の大小・傾き・色・切れ込みを保ちながら、Side/両3Qで安い板感が解消され、柔らかく弾力のありそうな厚みと上品な艶に見えるか。頭/耳可動時の浮き・刺さり・眼遮蔽も比較画像で確認する。動的なぷるぷる揺れは未追加。

## 再現

repo rootでBlender 5.2.1を使う。`blender -b -t 4 --python-exit-code 1 --python scripts/blender/build-shushu-equipment-v002.py -- --blockout`、続いて同scriptを引数なしで実行。独立Blendはobjects libraryから `finalize-shushu-flower-blend-v002.py` で編集sceneをリンクして保存する（この環境でScene library直接保存がBlender native crashとなったため処理を分離）。

`verify-shushu-equipment-v002.py -- --author`、引数なし、`audit-shushu-equipment-v002.py`を順に実行。`node scripts/3d/review-shushu-equipment-v001.mjs`でlocalhost:8772を起動、`node scripts/3d/capture-shushu-equipment-v002.mjs`でCDP9234のPC収録。`node scripts/3d/validate-glb.mjs <v002花GLB>`で構造検査後、`package-shushu-equipment-v002.py`が現ledgerにある資産だけを梱包する。

USB/ADB/phone操作、課金/Tripo、他キャラ・原本置換、Motion量産は実施していない。v001の納品manifestはcommit `151d8718` 時点の履歴として保持する。
