# Shushu v003 — 開口した下側の口縁・顎の局所修正

2026-10-14。開始HEAD `b92aa7683beb2c1ca7d0c7a4e0173c5ee32773d9`、実branch `codex/grimo-motion-zero-based-design-20261011`。**Human=PENDING / Tripo=HOLD**。

最新Human判断は、先行参照比較のsaved Sideで「開口した下顎の口の部分が前に出て尖っている」「リファレンスのようになだらかな曲線」「他の部分は一切変えず」「Frontも可愛さを維持」。承認済みLeft/Front、スクリーンショット(525)を継続参照し、#27は使用していない。

## 保存候補の比較

- [参照 / 修正前 / 保存後：Front・Side](00-reference-before-after.png)
- [同一カメラの開口笑顔：Front・Side・3Q](01-colour-before-after.png)
- [Side：Clay・小開口・大開口](02-clay-openings-side.png)
- [原寸640×640](renders/)、[カメラ](cameras.json)、[画像hashと比較条件](review-manifest.json)

6組の前後比較。先行保存候補の同条件カラー3視点はその原寸画像を再利用し、追加条件と修正後は保存モデルを読んでレンダーした。参照も3Dレンダーもレタッチ・形状warpなし。

## 原因と局所変更

従来の開口は下側の口縁を下へ移す一方、奥行きがほぼ一定だった。その結果、側面の下側口縁が顎の本来の丸い面より前へ残り、先端で曲率が急変した。

`MouthOpen` / `MouthDonorOpen` の**下側だけ**を、固定した上側口元から顎へ後退する滑らかな奥行き曲線へ変更。Headの対象域は元Basisで `|X|<.074 / .525<Z<.601 / Y<−.180`、実際に開口で下へ動く頂点だけ。口内の下側にも対応する奥行き変更を適用し、舌・口内が前へ残ることを避けた。閉口Basis、GentleSmileの元形状、口幅X・開口高さZは変更していない。既存頭姿勢との合成補正だけを再計算した。

保存後に照合したHeadの変更頂点は180（小開口136、大開口180）、対応口内384。Headの最大後退量は小開口.005486、大開口.024748 **scene unit**。実寸mm換算の校正値としては扱わない。

最初の試作は後退量が大きく、顎へのつながりに別の折れ目が出たため不採用。後退曲線を穏やかにし、下側の尖りを除きながら本来の丸い顎へ連続する候補を保存した。Front/3Qでは既存の幅・高さと笑顔を保持し、Sideで下側の突出を解消することを目視確認した。

鼻・鼻下・上側口元、目・まぶた、耳、身体・座位、支持・接触・復帰機構を変更する再制作ではない。編集可能な既存v003を継続した。

## 保存成果と対象別検証

[保存後検証](targeted-checks.json)、[保存hash](continuity.json)、[保護入力hash](protected-inputs.json)、[静的出力の往復](static-roundtrip.json)。

- asset / proofを再読込し、全Action曲線、object inventory、topology、制御・driver・modifier・weightを開始時と比較。対象Head・口内以外の全shape座標をbyte単位で照合。
- Head/口内も閉口と対象外キーは完全同一。変更は小/大開口キーと、その頭姿勢合成キーに限定。通常開口のX/Zは完全同一。開始モデルから同じ局所処理を再現し、保存座標と照合。
- Neutral / 小 / 大 / 笑顔の評価面で新規collapse・Front投影winding反転なし。有限座標と評価X/Zの保持を確認。
- 小/大開口、笑顔、閉眼笑顔、中間座位＋頭回転、着座＋頭傾げを含む7組で口内rayを確認。285フレームproofの代表Neutral復帰5点、releaseと復帰後のprop非表示を確認。
- Canonical・承認画像・元Donor・ユーザー差分56ファイルをhash照合。FBX/GLBの静的往復を再確認。Neutral形状は今回変更していない。

## Human判断と限界

**Sideの下側口縁・顎の丸さとFrontの可愛さはHuman再判定待ち。Human=PENDING。Tripo=HOLD。** 数値チェックを外観の承認へ置き換えない。

参照は2Dイラストで、実寸の校正尺度・同一3Dカメラがない。したがって「ミリ単位でも見た目の差がない」ことを数値証明したとは報告しない。今回の対象輪郭を拡大比較できる保存候補を示した。上側口周辺の既存横境界、最終毛並み/材質・最終Rig/runtimeは変更していない。

課金・Tripo操作・main一括統合なし。remote mainは `d655f9606b2785ac8be7484e5f22b84dbaee9f55` と照合済み。Goal√mapの変更なし。

## 再現

Blender 5.2.1、`refine-shushu-v003-lower-mouth.py -- --apply` / `-- --render`、`verify-shushu-v003-lower-mouth.py`。ボードはbundled Python/Pillowの `board-shushu-v003-lower-mouth.py`。開始資産は `.git/shushu-v003-lower-mouth-b92aa76/` に保持。保存資産の予期しない並行変更を検知した場合は上書きを拒否する。
