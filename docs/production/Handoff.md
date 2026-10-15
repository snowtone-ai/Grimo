# Grimo — Handoff (last verified, not live authority)

実行時のNOWはbranch/HEAD、未コミット差分、保存成果とEvidenceで再確認。Goal・Canonical・Human承認を上書きしない。

## Last verified: 2026-10-15 / Codex

- **Shushu口B専用候補:** 開始HEAD `d5e9882dd644ca35c6944ed9e1c7b4163944890a`、branch `codex/shushu-v004-mouth-b-20261015`。生成閉口モデル→局所閉/小/中/大造形→局所Textureの順。別名 `shushu-v004-mouth-b-v001.blend` / `-proof.blend` / `.glb` を保存。[比較・原寸・再現・GO/HOLD](shushu/evidence/production-rig-v004-mouth-b/REVIEW.md)。Head既存境界で接触W字の閉口とし、MouthInterior/OralBowl/Tongueを局所再作成。Head対象外全shape、UV/topology/weight、口以外10object、骨rest/親を保持。Head Textureの87,481texel（約2.086%）を局所変更し旧ピンクを除去。元画像11本の圧縮バイト保持。
- **口B Gate:** authored / saved GLB / PlayCanvas localで4開口×Front/Side/3Q、実動画、座位/閉口優先/復帰を比較。保存位置差約9.39e-7H、実GPU口位置差最大4.92e-5H。数値を外観PASSとしない。閉口のピンクは消えたが、小開口のW形、口角の陰影、真横で頬に隠れる口内の見え方、Front可愛さ/Side自然さはHuman確認。**Human mouth=PENDING、原本置換・Motion量産HOLD。** Tongueは0.55開口を伴う専用契約、既存全clip互換未承認。169fは診断のみ。Human指定「今回はPC比較まで」、候補phone未検証。
- **v004承認とA:** 2026-10-15 Human PASSはレビュー済み顔全体・外観・座位に限定。[元承認](shushu/evidence/production-rig-v004/REVIEW.md)。同日の追加前肢A/B ReviewはHOLD。[局所8互換・原本実機・A原因/B旧比較](shushu/evidence/production-rig-v004-skin-compat/REVIEW.md)。3mesh局所8は互換試作として保持。Aは全8参照でも残り、Blender評価面との法線乖離がある。今回Aは変更なし。A専用修正とA/B両方のHuman再判定が必要。
- **保護:** 元v004・他キャラ・開始時ユーザー変更3PNG/未追跡モデル/18–27参照を保持。3,507入力hashと終了照合は口B Evidence。Handoffのみ状態更新として区別。main一括統合なし。
- **v006静的承認:** 2026-10-14 Humanがv006外観PASSを明示、SHA256 `9c479122…34f10f`。[口v006履歴](shushu/evidence/tripo-mouth-depth-v006/REVIEW.md)をRig/Motion/runtime承認へ拡張しない。
- **先行offline候補:** [lowpoly v001](shushu/evidence/tripo-rigprep-v006-lowpoly/REVIEW.md) は99,565tri/6.07MB、Human/Tripo未検証。[毛線v005](shushu/evidence/tripo-fur-seam-v005/REVIEW.md) はHuman PENDING。v004毛線の旧PASSは耳→肩線の再指摘で撤回。[目囲みv002](shushu/evidence/tripo-eye-outline-v002/REVIEW.md) はHuman「完璧」、他候補/正式Rigの承認ではない。
- **先行Geometry v003:** production branch `codex/grimo-motion-zero-based-design-20261011`。[下側口縁から顎の修正・検証・限界](shushu/evidence/geometry-v003/lower-mouth-revision/REVIEW.md) はHuman PENDING/Tripo HOLD。上側口周辺横境界を含む履歴として保持し、今回Authorityとして参照。過去成果は上書きしない。

## Next

口B候補の閉口を最優先にHumanが判定し、小/中/大・Side/3Q・連続動画へ進む。顔全体の可愛さ・承認済みBody/座位を守る。Aは別の局所法線/変形課題として修正。原本置換とMotion量産は両局所Human再判定までHOLD。座位Game Neutralは未決定。候補phone比較は今回対象外。
