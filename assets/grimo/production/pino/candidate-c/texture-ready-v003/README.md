# Pino C Texture Ready v003 候補

**HOLD / Human Pre-Texture Gate=PENDING / Texture GO=NO。**

- `pino-c-texture-ready-v003-HOLD.blend`: 編集Master。保存時は元の開いた笑顔Basis。正式Game Neutralは未決定。
- 同名`.glb`: 4 mesh / 70骨 / LBS4 / Morph POSITION・NORMAL / UVを含む受渡し候補。Texture・animationなし。
- `pino-c-v003-uv-layout.png`: 共通atlasのUV wire。Texture画像ではない。

[REVIEW](../../../../../../docs/production/pino/evidence/texture-ready-v003/REVIEW.md)と[所有・制御契約](../../../../../../docs/production/pino/evidence/texture-ready-v003/TEXTURE_CONTRACT.md)を先に読む。ファイルSHAは同Evidenceの`file-manifest.json`。

原本FBX/GLB、Rig v001、Face v002は保全。Basis形状を変更せず局所表情・遮蔽・法線を追加し、UVと材質を割り当てた。Masterも受渡しと同じLBS4。元DQとの全Motion一致は保証しない。

Blender標準再importはMorph法線を自動駆動しないため、提供の再importスクリプトでBridgeを再構築する。GLBを単純に再exportして同一と見なさない。

顔の可愛さ・閉眼/口遷移の自然さ、必須の両前肢接触・低休息、細かなUV島の制作性はHuman確認待ち。深い休息の床貫通をPASSとしない。本番Textureや最終Motionへ自動継続しない。
