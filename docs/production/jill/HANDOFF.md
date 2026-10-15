# Jill — NOW

2026-10-15 / branch `codex/jill-rig-other-v001-20261015` / **Rig review candidate、完成承認HOLD**。

最新main authorityは`8e4996c`。Jill v002の直前正本/状態は別枝`7f16127`の[HANDOFF](https://github.com/snowtone-ai/Grimo/blob/7f16127322685216bbd8bb93065cb3de4203568c/docs/production/jill/HANDOFF.md)と[v002 REVIEW](https://github.com/snowtone-ai/Grimo/blob/7f16127322685216bbd8bb93065cb3de4203568c/docs/production/jill/evidence/smartmesh25k-v002/REVIEW.md)。本枝はmain基点で、それらを一括mergeしていない。Geometry v002を承認済みに昇格しない。

外部研究→[Plan](rig-other-v001/Plan.md)を`832e1e8`で先にcommit→実装。FBX/GLB原本とv002 donorは新規sourceへbyte copy、原本hash不変。v002 body Basis 28,050頂点は座標差0、FBX UV差0。130骨、94葉骨、39意味ch、左右瞼を含む20morph、16anchor。六肢/尾/葉/頭首/顔の制御と局所correctiveを実装した。

[成果物](../../../assets/grimo/production/jill/tripo/rig-other-v001/README.md) / [Evidence・残課題](rig-other-v001/Evidence.md) / [比較画像](rig-other-v001/00-overview.jpg)。Blender再読込、直接ch再操作、GLB fresh importの同時刻比較を実施。GLBはsampled proofを再現するが、driver/IK自体は移植されない。任意runtime制御はmappingとsolverの実装が別途必要。

**阻害条件**：閉眼面が丸い塞ぎに見え、眼窩と自然につながらない。小口の完全閉鎖/内側の仕上がり、翼根/首葉/尾葉の接合・重なりはHOLD。接触nodeは骨所属で、任意poseの厳密な接触/装備fitは未保証。真の座位、全Motion、正式Texture、スマホ/PlayCanvasは未成立/対象外。承認済み極値pose参照もない。Human外観判定はPENDING。

続行時はEvidenceの拡大画像から眼窩/瞼の局所接合と根の重なりを修正し、承認poseに照らして再評価する。体型/顔の再設計やv002正本上書きで解決しない。他キャラの並行作業/元checkoutは触らない。
