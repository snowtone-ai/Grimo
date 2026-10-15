# Jill v002 — Tripo transfer contract / execution HOLD

2026-10-15 JST。**現状はupload不可のレビュー成果物。Pre-Texture Technical GO候補には未到達、最終GOはHuman専権。** 実装・比較・入出力対応を保存した。Tripoへのupload、課金、正式Texture生成、AutoRig/retopology/Smart UVは一切実行していない。

## 入力と保管

正本は `assets/grimo/production/jill/tripo/rig-pretexture-v002/jill-rig-pretexture-v002.blend`、sampled proofは同名GLB。Texture投入専用は `jill-texture-input-neutral-v002.glb` と `.fbx`。どちらも同じ保存Rigを全39ch=0のニュートラルにして評価した面・active UVから作成し、骨・Morph・anchor・animationを含まない。検査用clay材質だけを含む。実形状とUVの再読込対応は `roundtrip-validation.json`、絶対パス・SHA256は `Manifest.json`。

Texture入力のニュートラルはCanonicalに対応する開眼・小さな笑顔。生成のために口を塗りつぶす、閉口形状に開口画像を固定印刷する、元Rigを返却モデルで置き換えることは禁止。顔の連続性とUVのHOLDが解消するまで入力ファイルも実行に使用しない。

## 公開資料で確認できた範囲

不足していたOriginal UVの扱いだけ追加確認した。[Tripo公式8K案内](https://www.tripo3d.ai/blog/tripo-8k-texture) は外部モデルのTexture処理で **Use Original UV** を選ぶ導線を記載している。これは全機能・全plan・実アカウントで選べることの確認ではない。[公式Texture API資料](https://developers.tripo3d.ai/en/docs/models-texture) はFBX/GLB等の入力に言及するが、元の骨・Morph・頂点順序を保持する契約とは読めない。

[Smart UV公式説明](https://www.tripo3d.ai/blog/smart-uv) はUVを再構成する別処理。元Rigへ画像を戻す契約と異なるため、自動適用しない。必要になれば変更前後のUVを明示して再評価する。

**未確認**：実ログインUI、選択中plan、Original UV checkboxの現在の表示名/位置/対象機能、FBX/GLBの選択による差、同時に強制されるremeshやUV再生成の有無、実アカウントの見積credit/料金/税/解像度上限、実返却物の構造。公開 [Studio料金](https://www.tripo3d.ai/pricing) と [API billing](https://platform.tripo3d.ai/docs/billing) を混同しない。ここでは具体的費用を確定していない。Humanが許可した将来の実行時に、送信前のUIと最終見積を保存する必要がある。今回の依頼はその実行を許可していない。

## 原RigへのTexture転写

1. Humanの承認後も、別の作業コピーと原RigのSHAを先に保存。Geometry、Rig、Skin、20 Morph、16 anchorの原本を保管する。Texture専用入力を用い、AutoRig/全身再生成/一括remeshを選ばない。
2. 実UIでOriginal UVを選べるか確認し、その画面・input hash・機能名・実見積を記録。選べない/UV変更が強制される場合はその条件をHOLDとして扱う。
3. 返却データを別フォルダーへ保存しhashを記録。**骨・Morph・UVの保持は仮定しない。** 画像の枚数/チャンネル/色空間、UV、Geometryの位置・スケール・対応、左右の眼/翼/口内を検査する。
4. 形状とactive UVが一致した場合は、返却画像を元Rigの材質へ割り当てる。返却メッシュ、骨、weights、Morph、anchorは採用しない。第2層の旧UVへ誤って画像を結び付けない。
5. UVのみ変わり形状が一致する場合は、返却メッシュをsource、元Rigのニュートラルをtargetにして、部位別にselected-to-active bake/再投影する。眼・瞼・口内/舌・翼両面・重なった葉を分け、近接面への誤投影を避けるcageとray距離を調整。画像を元active atlasへ焼き、継ぎ目と隠れ面を補修する。自動成功を前提にしない。
6. 形状が変わった/対応が曖昧な場合はHOLD。返却形状を原Rigへ上書きせず、形状対応と転写可否をHumanへ提示する。
7. Texture適用後に保存blend/GLB再読込、Skin/Morph/UV/anchor、閉→小→中→大→閉、開眼→半閉→閉眼→開眼、根と複合の3視点再生を確認。Humanが外観と実行可否を判断する。

現状のHOLD理由は [Evidence.md](Evidence.md)。Original UV利用の公開案内があることは、Geometry・外観・価格・返却互換のGOを意味しない。
