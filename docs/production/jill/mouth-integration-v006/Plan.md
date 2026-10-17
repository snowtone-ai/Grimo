# Jill 完成モデルへの方針 — 2026-10-17

Humanの最新GOAL：Texture込みのJillがMotion・表情変化・中間・復帰で承認外観を保ち、口周囲の派生不具合も根本解決した完成モデル。旧「鼻下だけ」の作業単位を完成条件にしない。可愛さ・本人性を損なう修正は不採用。Human視覚GOと技術検証は独立。

開始 `74596c9673434f4120b300ec0c96fb9c663fc4d0` clean、main fetch `336997db2b95244c17774258e2f5ff874a2adbc1`。原本v005/v004・返却画像・他checkoutのuser変更を保護。別名v006で開発。

## 逆算

1. 口上辺W、閉/小/大開口・smile・頬接触・同時入力の中間を破綻なく成立させる。既存skin重複を整理し、口腔/歯/舌と接触する境界を統一する。
2. 顔全体/全身の比較でidentityとTexture境界を確認。瞼等の既知HOLDを未解決一覧から消さず、必要な部位だけ調査する。根拠のない新模様/配色は創作しない。
3. 保存blend再読込・全39chの対象範囲sweep・代表組合せ・実連続Motionを確認。130骨/39ch/20Morph/16anchor維持。輸送検証と見た目を混同しない。
4. GLB再import、実PlayCanvasで同じ状態・遷移・復帰を確認。描画差/Normal/skin/Morphを切り分ける。mobileは実確認できなければUNKNOWN。
5. レビュー可能な完成候補、比較、残課題、Evidence/HANDOFF、commit/push/remote照合。Human承認を自己発行しない。

## 選択肢と判断

- Texture/maskのみ：重複立体面が残り、旧口内/歯を露出。前回実試験により不足。
- 追加口面だけをWへ移動：上唇へは接続するが閉口時に別々の面が交差。前回不採用。
- **既存の局所skin境界へ口腔を直接接続**：追加外皮の重なりを除き、下唇の変形を周辺skinへ連続させる。最初に試作してFront/Side/3Qで評価する。
- 全顔再造形/全Rig再作成/Texture再生成：承認外観と既存資産への影響が大きく、現時点の根本原因に不要。

局所Topology/Morph調整も、元の顔比率・W字マズル・鼻・目・silhouetteを守るための手段に限る。試作に欠陥があれば、保存済みという理由では採用しない。

## 2026-10-18 実施後

一体化案で指定のW/閉/小/大/復帰を実画像で確認。保存/GLB輸送、39ch有限・端点画像、頬/頭/呼吸の複合を検証。Blender driverを運べないstatic GLB用に4Morphだけの閉口優先controllerを追加し、baked clipに依存しない実PlayCanvas直接入力も照合した。元Geometry/Textureは不変保護、局所差分をEvidenceへ明示。

口のHuman外観判断とclover Authorityを非同期で質問済み。未回答をGOとして扱わない。口修正の候補保存/検証/commitを終えても完全完成GOALを縮小せず、瞼/角/模様・全Motion/実機mobileなど残条件を追う。

## 2026-10-18 Human回答反映

口の外観GO。腿cloverはCanonical準拠で追加を指示。v006承認口を先に保存・pushし、別派生で模様を局所追加する。未表示側/背面への複製はしない。全Motion量産・実機mobileは元依頼の限定検証範囲と区別し、新たな必須要件を作らない。
