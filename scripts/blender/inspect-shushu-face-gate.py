import bpy,sys,json
from pathlib import Path
import numpy as np
sys.dont_write_bytecode=True
root=Path(__file__).resolve().parents[2];out=root/'docs/production/shushu/evidence/production-rig-v004-motion-ready'
bpy.ops.wm.open_mainfile(filepath=str(root/'assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v004-motion-gate-v001.blend'))
o=bpy.data.objects['ShushuStatic_Head'];o.data.calc_loop_triangles()
print('FACE_META',o.data.has_custom_normals,[(m.name,[(l.from_node.type,l.from_socket.name,l.to_node.type,l.to_socket.name) for l in m.node_tree.links]) for m in o.data.materials],flush=True)
data={k.name:np.array([v.co for v in k.data]) for k in o.data.shape_keys.key_blocks}
data['tri']=np.array([t.vertices[:] for t in o.data.loop_triangles])
np.savez_compressed(out/'face-source.npz',**data)
