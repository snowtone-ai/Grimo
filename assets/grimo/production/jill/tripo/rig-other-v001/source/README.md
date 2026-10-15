# Immutable source intake

These are byte copies, not converted/resaved inputs. Original root files were left in place.

| Copy | Origin | SHA256 |
|---|---|---|
| `tripo-other-original.fbx` | `tripo_convert_77a7aeee-faff-4d3b-8082-d15dddbe9fc8.fbx` in the user's original checkout | `1d9ecfae60f0fcb1a8bbffeb81fd2a931b1dba0907af43487bf0d1f1e3a7dc14` |
| `tripo-other-original.glb` | `jill-v002-neutral-tripo.fbx.glb` in the user's original checkout | `a93cd56d4b9658596284288ef8f5ebabffae0d3c5f7024e591269ce95eff0378` |
| `jill-v002-authority-donor.blend` | v002 master on Jill authority branch `7f16127322685216bbd8bb93065cb3de4203568c` | `8c2ded49ec7108c420fead87d01b3ff26deb43e479d14479afc50e6aafd67a97` |

FBX was first candidate: indexed polygons match v002, and normalization leaves maximum indexed position error `1.631e-7`. FBX contributes original UV and locally remapped weights/joint locations; final body Basis is the unchanged v002 surface.

The source GLB has one raw mesh, 78 joints and no animation. Its 46,003 seam-split raw vertices match the v002 surface within `2.706e-7` after the same normalization and axis conversion. Its imported bind placement differs; that bind was not adopted. The initial import observation of an Icosphere is not evidence of a second raw GLB mesh. See `source-glb-comparison.json` for the corrected raw-file audit.

The other newly added FBX (`tripo_convert_e41db652-3438-43d9-b501-1000972256cf.fbx`, 18,858 vertices / 65 joints) was excluded and left untouched.
