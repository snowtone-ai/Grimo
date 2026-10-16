# v003 修正範囲と方式選択

v004のHuman承認済み外観・体型・真の座位、Human OKのW、鼻下紐除去を継承する別名候補。元v004/v002、他キャラ、元checkoutのユーザー差分は置換しない。最新main `73617ce2d3c724c86aed82dfc2a09cd220e5d194` のAuthorityを確認し、開始HEAD `a4a90851c1ff85e584671f7c3decd7561e2baea1` から専用worktreeで作業した。

## 顔と頭頂

FACE-01/02は法線だけの問題と扱わず、v002の口retopoを入力として評価面と深度を調べた。Wの全44 key座標を固定し、外側3リングと鼻下の上側サンプルを拘束したthin-plate深度補間、C2境界ブレンドを使用。外側Headの `Corrective.MouthCavity` が加えていた凹みを退役させ、口内は既存の独立Bowlを使う。最大深度変更はBasis 0.0085534H / MouthOpen 0.00909685H。局所領域はX ±0.13155、Z 0.50287–0.67896H。Z 0.630より上を完全不変とする主張はしない。W・鼻・目・耳・Textureは別途保護検査で照合する。

口の境界へ別の高さfadeを掛ける案は、スマホ照明で横向きの陰影を作ったため不採用。上側の拘束点を補間式に含めた。頭部全体のCPU法線置換で隠す方法も採用しない。輪郭・深度の修復とPaw法線の補修を分ける。

CROWN-02の3QピクセルをHead triangle 20283 / vertices 33378,33613,33668へ追跡。元の38頂点だけの移動では、負向き法線と多層の折り返し面が残った。局所楕円（中心XY -0.087,0.037 / 半径0.065,0.11H）を再構築し、190 source trianglesを除去。623頂点・550 disk triangles、98個のT-junction分割で外周へ接続した。全Shape/driver、weights、UVは外周とbarycentric写像から移送。1e-6Hの幾何weldで局所開放境界0・nonmanifold 0。耳の造形変更は行わない。

## 前肢

v002のinverse multi-bone LBS補正式と重ねたGrip補正は、中間のSelfContact/割込みで実形状の突起・潰れ・侵入を作っていた。法線更新だけでは治らない。DQによる旧donorの再評価、固定肩中心のswing、末端だけの移動、root固定、単純なモードLERPを調べた。順にねじれ、棒状の長い輪郭、最大約82%の膨張、約48%の膨張、最大約26%の体積喪失があり不採用。数値だけで良否を決めず実画像と照合した。

採用候補は元のPaw Basis/UV/topology/Textureを保ち、Spine2の単一carrierと通常のShapeを使う。曲線の中心線へ元の断面を運び、Hold/SelfContact/Offer各8段階、Seat 0/0.5/1、Wrist -1/0/1を補間する。1 Pawにつき216 single-purpose、216 pair midpoint volume corrective、6 neutral-Wristの438 targets。Purpose優先はHold > SelfContact > Offer、左右独立。pair補正は回転中点と線形補間の差から作り、端点では0になる。

初回のv003候補は体積・貫通検査を通ったがSelfContactが外側に離れたため棄却した。[棄却画像と元GLB hash](rejected-selfcontact/capture-ledger.json)を保持。最終案は先端を自分の頬下へ向け、実メッシュの先端とHead表面の距離をfitした。方向 (-sign*0.6,-0.5,0.35)、局所移動 (-sign*0.07,+0.095,+0.04) を出発点とし、Torso/Headの前面rayによる一体移動で接触側を保つ。個々の頂点を押し潰さない。全SelfContact時の先端gapは左0.00328H、右0.00255H。これは柔らかい接触の外観をHumanが承認したという意味ではない。

旧arm FKをそのまま再生する互換性は、このPaw経路では提供しない。既存の骨rest/親は保存するが、前肢はPurpose/Wrist/Seatの制御契約を用いる。対象外の任意FKや未検証の全制御空間をPASSとしない。

## 製品へ渡す経路

`assets/grimo/production/shushu/runtime/shushu-v004-loader-v003.mjs` は1回のGLB取得、dense/sparse accessor復号、独立container parse、実体の生成・破棄を所有する。同URLの他実体のcacheを破壊しない。`shushu-v004-deformation-v003.mjs` はTorsoの全8-weight skinをGPUで使い、2 Pawの現在位置からweld付き角度重み法線をCPUで計算し、所有するmesh/materialのNORMALへ送る。骨行列は再利用し、三角形あたりatan2は2回。rAFはGPU時間へ読み替えない。

`candidate.pawControls.set(values)` に現在のPurpose/Wrist/Seatを渡す。body/faceのposeと対応するSeatは呼出側が所有する。Controllerはanimation後に同じ補間を行い、実際のPaw表面からHold anchorを更新する。Blender driver、diagnostic viewer、frame番号、DOMへの依存は製品moduleに含めない。baked endpoint同士のcrossfadeだけではpair補正が抜けるため、連続入力・割込みではControllerを使う。`set(null)` は呼出側animationへ制御を戻し、`dispose()` は所有資源とlistenerを片付ける。

単体GLBを任意の4-weight viewerへ渡すだけで同品質になるとは主張しない。今回の納品は本番へ移せる経路とその実機検証であり、Grimoの全利用画面への採用・原本置換・Motion量産の承認ではない。

## 検査の読み方

101開口、264状態/左右プローブ、保存の代表pose、Front/Side/左右3Qの原寸・連続録画、実GPU readback、5分実機比較を目的別に照合する。signed nearest-triangleだけでは、顎下の外側点を口内縁の法線で内側と判定する場合がある。生の負値を隠さず、ray parity・実三角形の交差・画像を併記する。rootの意図したTorso重なりは遠位の侵入と区別する。

体積はoriented triangle proxy、7 Anchorは座標契約、0交差は検査した範囲の結果であり、可愛さ・質感・重さ・自然な接触のHuman PASSへ拡張しない。技術、Runtime、Humanの最終Gateは [REVIEW.md](REVIEW.md) と [residual-defects.json](residual-defects.json) を参照。
