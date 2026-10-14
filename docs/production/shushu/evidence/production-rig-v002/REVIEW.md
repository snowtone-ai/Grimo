# Shushu Production Rig v002 — 2026-10-15

**編集可能Rigと、測定したS01–S26の能力domainは技術PASS。Human可愛さ・正式採用はPENDING。実item/商品実装/スマホと、PlayCanvas標準loaderの完全Skin・外観適合はHOLD。** 未測定を完成扱いしない。S/Q別の範囲は[CAPABILITY-MAP](CAPABILITY-MAP.md)、操作・境界は[README](README.md)、Human原典の分類は[AUTHORITY](AUTHORITY.md)。

開始branch `codex/grimo-motion-zero-based-design-20261011` / HEAD `24c11ff6d47fdf85720c7c277ed753259a25695b`。既存のユーザー差分を保護してv001を別名継承。Wikiは明示的 `/wiki` 後に最新main `281f7950d1b916dbaa4dcd19a0a4022a5431464b` のAGENTS/workflow/選択原典を読取専用で照合した。全件検索や未取得画像の判断は代替していない。

## 改善と前後比較

腹下端〜臀/腿の折れに8個のSeat中間補正を追加。同位置のUV seamを補正計算の中だけで共有し、mesh・UV・Textureを作り直さず、元の足world pinと足裏を保護した。[座位正面](01-seat-front.png) / [側面と途中](02-seat-side.png)では、局所輪郭の折れを緩める控えめな改善をCodexが観察した。脚の長さ・体型・全面の造形を変えて座位を作り直していない。腹/臀/腿/足の自然さの最終Human判定は未受領。

半目の実効Blinkを0.39、Restの瞼量を0.40へ調整し、半開の鋭い補正を弱めた。Joy最大は明瞭な閉眼笑顔にした。[顔拡大の前後](03-face-before-after.png)には低頭と左右荷重も含む。[五方向合成](04-five-view-composition.png)で正面・両3Q・両側面を確認。Neutralだけを合格材料にしていない。

[v001直接継承照合](v001-inheritance.json)では14meshのBasis座標/UV/topology、67boneのrest行列が完全一致。NeutralとJoyを加えないBlink最大の評価頂点差は全meshで0。花柄瞳、口、元のTexture・UV、閉眼終点を保持。[承認v006静的/v001/v002比較](00-neutral-identity.png)は承認範囲を混同せず並べた。

同側reachはHold > SelfContact > Offerの残余量をtarget、肩/IK、paw補正へ一緒に適用。4局所stroke域（額/頬L/頬R/腹）を追加し、ownerに追従する押圧中心を連続補間する。両手には固定spanの一つのrigid proxyを使い、小さな遠位接面補正をSeat 3×WeightShift 9条件から補間。[保持・対側接触・反転・復帰](05-composition-return.png)、[proxy比較](06-proxy-contact.png)を保存した。

## 対象を絞った証明

数値は高さ約1の正規化Blender座標。実寸・力・摩擦の証明ではない。最小proofは24 fps、81 witness、961 frame（GLB最終時刻40.041668秒）。DRAFTの26全Motionを演技として制作したものではない。

| 検査 | 保存結果 / 根拠 |
|---|---|
| 継承能力の回帰 | [capability-numeric](capability-numeric.json): 603支持条件、頭/腕/顔/足の独立、左右耳、FKの保護域、閉眼/閉口ray、復帰。骨数・元12画像・材質/UVを保持 |
| 座位中間と接地 | [v002-capability](v002-capability.json): 243条件で床−0.001以下0頂点、sole XY drift最大4.974×10⁻⁷。proof全961 frameの床最小−1.069×10⁻⁷ |
| stroke | 4域×21点で局所変位が活動し、他ownerへの漏れ<10⁻⁶。押圧重心移動は額0.194/頬L0.0594/頬R0.0293/腹0.322。保持・支持・低頭と共存。域越境や任意裏面はHOLD |
| 同側競合・復帰 | 12比較で単独ownerと競合要求のgeometry/hold Anchor差0、Neutral復帰差0。待機/予約等のevent実装をRigのPASSに含めない |
| 合成した顔/口 | [composed-face-occlusion](composed-face-occlusion.json): Joy/低頭/左右荷重/閉眼/極端合成の閉眼ray露出0。MouthClose優先の口内/舌ray露出0。魅力はHuman PENDING |
| 両手rigid proxy | [grip-audit](grip-audit.json)と[proxy-contact](proxy-contact.json): fixed span 0.336562、途中含む36 frameのhandle→Anchor差最大0.000272。item scaleは1。異なるspan/Wrist/regraspは再fitが必要 |
| Foodの接点 | 同じ口周辺のHead/Tongue/OralBowl/Noseを合成面として108 frameで検査。閉口・舌後退・傾きを含む外側球probeの隙間0.000100。[全4面のclearance](proxy-clearance.json)もPASS。5styleの全item本体/容器/残量/液体/消費はHOLD |
| 焼き出し | [bake-verification](bake-verification.json): 81時点の評価頂点差最大7.683×10⁻⁷。編集可能proofを保存してから、通常joint/morph/Anchor channelへbake |
| 再import GLB | [glb-roundtrip](glb-roundtrip.json): 14mesh×81時点の最大world頂点差1.143×10⁻⁶、rest対応差3.629×10⁻⁷。全961 frameのfloor/7 Anchor、単手fixture/両手/Food軌跡を照合 |
| Anchor / proxy保存 | [Anchor](anchor-roundtrip.json)最大行列差1.609×10⁻⁶、[単手](fixture-roundtrip.json)1.013×10⁻⁶、[両手/Food](contact-roundtrip.json)1.192×10⁻⁷ |
| Texture/数値保持 | [restoration](texture-material-restoration.json): 全3 GLBの元12画像byte一致、全accessor hash一致。空のextensionsUsed除去はmetadataのみ。数値往復測定時のSHAと最終SHAはこの処理のため異なるが、数値データは同一 |
| 画像往復 | [Blender/GLB比較](07-blender-glb.png): 同条件640²/16 samples/固定camera/light。7状態×5方向のRGB平均絶対差0.000457〜0.001030 /255。[数値](render-roundtrip-difference.json)。画像一致だけでSkinを判定していない |
| glTF schema | [main](validator.json) / [単手](validator-proof.json) / [接点](validator-contacts.json): error 0。各14 warningはskinned meshの非root親。現在のjoint/world変換は往復と実runtimeで別途照合。任意親変換を保証しない |

元v001の単手sphereは、解放後にworld座標を凍結する診断規約を継承する。proxy比較板に浮いて見える大きい球は、その解放済みfixture。Food接点は口近傍の小さい球。物理落下、商品所有移管、1Wear交換や在庫の意味を代行しない。

## PlayCanvas最小受入と残HOLD

PWAに触れず、保存GLBを読み込む独立HTMLとPlaywright CLIで検査。[runtime-acceptance](runtime-acceptance.json): PlayCanvas 2.22.2/WebGL2、14 skinned mesh・67 joints・12 Texture・7 Anchor、81時点のworld行列差最大7.857×10⁻⁶、morph差3.052×10⁻⁵、欠落0、時刻/進行有限。頭と左前腕の2非root jointで時間進行とworld行列変化を実測。**loading/clip/morph/Anchor/Textureのbounded受入PASS**。

**完全Skin・runtime外観はHOLD。** Installed loaderがJOINTS_0/WEIGHTS_0だけを使い、JOINTS_1/WEIGHTS_1を省くことを[ソースと数値](runtime-weight-limit.json)で確認。Paw L15/Paw R8/Torso280、計303頂点に追加weightがあり、最大和0.0880。既存の6影響weightを黙って削らない。[seat-joy実render](08-playcanvas-seat-joy.png)には面の筋/陰影差があり、[Neutral](09-playcanvas-neutral.png)も独立保存。NORMALを含むmorphを出力しているが、陰影差の全原因は未確定。読み込みPASSを外観PASSに拡張しない。正式採用前にruntime用Skin/normal適合とスマホ性能を解決・再承認する必要がある。

実Food/Gift/束/Wearの形状と接面、任意stroke面、物理COM、任意FK支持、全clip組合せ、Product state/data/PWA、スマホ性能はHOLD。Humanのv006静的PASSは、v002 Rig/Motion/runtimeの承認ではない。

## 保存・棄却・保全

編集Rig SHA256 `90b5ba95da879fb186b8774fac42722de00be041267bc8cf78895c00841bd90f`、主GLB `862f23c23d9abda706fa452a090242090ed15da4e9d436c2307c8b359d226606`。全成果は[delivery-manifest](delivery-manifest.json)で結ぶ。Handoffは重要な差分とHOLDだけを更新し、Goalは不変。[protected-input-verification](protected-input-verification.json)で、開始時3,146入力のうち許可したHandoffと本作業生成logの移動以外の変更0を確認する。

過度な下半身体積の減少、腹下端の突起、UV seam裂け、proxyの軸/口位置、閉口途中の接点入り込みは棄却した。`iterations/`と過去attempt logは失敗の記録であり、最終PASSの根拠に使わない。最終根拠は上記JSON、`*-final.log`、`proof-release-02.log`、`proxy-clearance-release.log`、`food-transition-preflight.log`。

局所補正には[Blender relative shape keys](https://docs.blender.org/manual/en/5.2/animation/shape_keys/introduction.html)と[公式glTF export](https://docs.blender.org/manual/en/5.1/addons/import_export/scene_gltf2.html)の原理だけを用いた。全面再造形、追加骨、外部課金、全Motion/PWA改修、Wiki書込み、他キャラ改修なし。再現手順はREADME、Human判定は比較板を用いて別途行う。
