"""Read-only local mouth topology/shape/UV extraction; never saves source."""
import bpy, json, sys, importlib.util
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/production-rig-v004-mouth-b'
SRC=ROOT/'assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v006-production-rig-v004.blend'
sys.dont_write_bytecode=True
bpy.ops.wm.open_mainfile(filepath=str(SRC))
rows=[]; data={}
for role in ['Head','MouthInterior','OralBowl','Tongue']:
    o=bpy.data.objects['ShushuStatic_'+role];m=o.data;m.calc_loop_triangles()
    p=np.array([v.co for v in m.vertices]);ks=o.data.shape_keys
    data[role+'__base']=p
    data[role+'__tri']=np.array([list(t.vertices) for t in m.loop_triangles])
    data[role+'__uv']=np.array([[m.uv_layers.active.data[i].uv[:] for i in t.loops] for t in m.loop_triangles]) if m.uv_layers.active else np.zeros((0,3,2))
    if ks:
        for k in ks.key_blocks:
            data[role+'__'+k.name]=np.array([v.co for v in k.data])
    rows.append({'role':role,'bounds':[p.min(0).tolist(),p.max(0).tolist()],'matrix':list(map(list,o.matrix_world)), 'keys':list(ks.key_blocks.keys()) if ks else [],'modifiers':[{'name':x.name,'type':x.type} for x in o.modifiers], 'drivers':[{'path':x.data_path,'expression':x.driver.expression} for x in ks.animation_data.drivers] if ks and ks.animation_data else []})
np.savez_compressed(OUT/'mouth-source.npz',**data)
(OUT/'mouth-source.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
