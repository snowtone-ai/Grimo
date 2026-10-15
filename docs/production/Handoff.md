# Grimo — Handoff (last verified, not live authority)

このファイルは`main`のローカル作業案内。実行時のNOWは実際の制作ブランチ/HEAD、未コミット変更、制作StateとEvidenceで必ず再確認する。正式な仕様やHuman承認を上書きしない。

## Pino: verified 2026-10-15
- Branch `codex/pino-base-rig-v001-20261015`、開始 `81432f9`。新Tripo Mixamo FBXを別入力として保全し、65骨を保持した基礎Rig候補へ尾5骨・左右閉眼・支持Skin/IKを追加。Geometry Master・元GLB・Neutral Basisは保護。
- [Rig v001 REVIEW・4本のGIF・保存検証](pino/evidence/rig-v001/REVIEW.md)。尾の限定bendと低いHigh-five到達を確認。閉眼の柔らかさ、両前肢接触、深い低休息は未成立。深い失敗姿勢は不採用、浅い荷重を低休息PASSにしない。
- **Human Rig/Geometry Gate PENDING / production HOLDで停止。** 最終Motion・Texture・Tripo再生成なし。保存40姿勢とNeutral復帰を確認し、復帰途中の足IK解除による床貫通を修正。次は外観/可動域のHuman判断を踏まえた局所補修。下のShushu欄は以前の確認履歴。

## Last verified: 2026-10-13 / Codex
- **Production branch:** `codex/grimo-motion-zero-based-design-20261011`
- **Published artifact revision:** `6a1dfec6909f379a5cd93c6fbb2c248aef5a3c1c`。公開時のremote HEADを確認済み。後続の文書コミットと制作変更は実行時に再確認する。
- **Shushu v003:** 中断成果を引き継いだGeometryレビュー候補を公開。編集用Geometry/285フレームの変形proof、静的FBX/GLB、同一カメラ比較・表情・座位/接触ボードとGIFあり。**Human Geometry Gate PENDING / Tripo HOLD**。最終Rig・Motion演技・スマホruntimeは今回の成果に含めない。
- **Evidence:** [v003 REVIEW・資産・検証・研究への入口](https://github.com/snowtone-ai/Grimo/blob/6a1dfec6909f379a5cd93c6fbb2c248aef5a3c1c/docs/production/shushu/evidence/geometry-v003/REVIEW.md)。原本Candidate B FBX/GLBはハッシュ一致。保存ファイル再読込、限定範囲の閉眼/斜め視点・支持/接触・Neutral復帰、静的再importを検証済み。技術検証は可愛さ・生命感・自然さの承認ではない。
- **残る外観確認:** 目周りと半閉/閉眼の柔らかさ、側面の鼻・口・頬の本人らしさ、座位の腿〜足と腹部/お尻の重さ。注視の最終印象は無着色Geometryだけでは未確定。
- **Shushu v002:** 限定的Technical PASSだがHuman Visual FAIL（側面顔の奥行き、座位の腹部・短脚シルエット）。Technical PASSは外観品質の代替にならない。
- **保護した判断/資産:** Canonical・承認済み参照#01–26を維持。修正版#27はUNKNOWN。v001/v002を造形ドナーにせず、既存のローカル変更を保存。`main@526a1b3`の3文書方針を確認し、制作ブランチへmainを一括マージ/リベースしていない。
- **Tripo:** upload・Texture・Auto Rig・課金・無料試行を実行していない。Studio適合性・アカウント/クレジットはUNKNOWN。ローカルFBX/GLB往復だけでGOにしない。

## Pino C — 2026-10-15 / Codex

- **Branch:** `codex/pino-c-geometry-gate-20261015`。FBXを唯一のGeometry Master、元GLBを正式なNeutral外観基準とするHuman判断を記録。原本2ファイルはハッシュ不変。
- **Evidence:** [Pino C REVIEW](pino/evidence/geometry-c-v001/REVIEW.md)。Master派生GLBは元GLBと属性・法線・材質および9視点ピクセル一致。4種類の実変形試験182フレームを複製で実行し、GIF・3視点極値・保存再読込証拠あり。
- **Gate:** Human Geometry Gate **PENDING / Tripo HOLD**。尾の3重殻・根元接続は未解決。前肢の両手接触と低い休息の試験はFAIL。閉眼の自然さ・重心・未試験Rig方式はUNKNOWN。内部補修は採用せず、失敗した変形を完成品へ適用していない。
- **Appearance lock:** 制作ブランチ`2abea76fad57`と同一AGENTS blobをmain `8e4996c63c6d`経由で安全に統合。別checkoutのShushu等の未コミット成果を保護。Tripo・課金・UV/Texture・最終Rig/Motion量産は未実行。
- **次のHuman判断:** Pino REVIEWのNeutral維持・眼・前肢接触・低休息の実映像と未解決の尾根を確認する。Technical PASSを本人らしさ・可愛さの承認にしない。

## Next
**次のHuman操作:** Shushuは既存REVIEWの本人らしさ・まぶた・座位、PinoはPino C REVIEWの実映像と未解決事項を確認する。Codexは承認を捏造せず次のGeometry Gateへ進める。Pinoの外観固定条件を維持し、Tripo操作には別途明示承認が必要。Goal√mapは制作WHY、製品仕様・Canonicalは別の正本。Handoffの更新は重要な進捗・承認・障害・担当変更時のみ行い、履歴はGitとEvidenceへ残す。

**Migration:** 今後の3ファイルの正本は`main`上のローカルパス。旧`coord/grimo-ai-handoff`は履歴用であり、制作を始めるたびに取得しない。進行中の制作ブランチは勝手にマージしない。
