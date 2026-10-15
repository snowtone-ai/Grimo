"""Read-only spatial intake for the isolated Jill pretexture derivative."""
import bpy, json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'docs/production/jill/rig-pretexture-v002';E.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'assets/grimo/production/jill/tripo/rig-other-v001/jill-rig-other-v001.blend'))
o=bpy.data.objects['Jill_Body'];o.animation_data_clear()
r=bpy.data.objects['JILL_RIG'];r.animation_data.action=None
for k in json.loads((ROOT/'docs/production/jill/rig-other-v001/control-contract.json').read_text())['authoring_properties']:r[k]=0.
r.update_tag();bpy.context.view_layer.update()
v=np.array([tuple(x.co) for x in o.data.vertices]);c=np.load(ROOT/'docs/production/jill/rig-other-v001/authority-parts.npz')['component']
o.data.calc_loop_triangles();t=np.array([tuple(x.vertices) for x in o.data.loop_triangles])
uv=np.array([tuple(x.uv) for x in o.data.uv_layers[0].data])
np.savez_compressed(E/'intake.npz',v=v,tri=t,component=c,uv=uv,polyloop=np.array([p.loop_start for p in o.data.polygons]),loopvert=np.array([x.vertex_index for x in o.data.loops]))
parts=[]
for ci in range(int(c.max())+1):
 q=v[c==ci]
 if len(q):parts.append({'i':ci,'n':len(q),'min':q.min(0).tolist(),'max':q.max(0).tolist(),'center':q.mean(0).tolist()})
report={'parts':parts,'objects':[{'name':x.name,'type':x.type,'vertices':len(x.data.vertices) if x.type=='MESH' else None} for x in bpy.data.objects],
 'morphs':[x.name for x in o.data.shape_keys.key_blocks], 'materials':[x.name for x in o.data.materials],
 'uv':{'name':o.data.uv_layers[0].name,'min':uv.min(0).tolist(),'max':uv.max(0).tolist()},
 'mouth_vertices':[(int(i),v[i].tolist()) for i in np.flatnonzero((abs(v[:,0])<.055)&(v[:,1]<-.34)&(v[:,2]>.558)&(v[:,2]<.64))]}
(E/'intake.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print('JILL_INTAKE',json.dumps({k:v for k,v in report.items() if k not in ['mouth_vertices','parts','objects']}))
print('PARTS',json.dumps([p for p in parts if p['i'] in [0,1,2,4,98,99]]))
