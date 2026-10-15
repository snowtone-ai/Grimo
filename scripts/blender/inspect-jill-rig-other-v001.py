"""Read-only intake in an isolated Blender process. Does not save any blend."""
import bpy, json, hashlib, struct
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
LOCAL=Path('C:/Users/chidj/project/プロダクト/Grimo')
OUT=ROOT/'docs/production/jill/rig-other-v001'
OUT.mkdir(parents=True,exist_ok=True)
rows=[]
for name in ['tripo_convert_77a7aeee-faff-4d3b-8082-d15dddbe9fc8.fbx','tripo_convert_e41db652-3438-43d9-b501-1000972256cf.fbx','jill-v002-neutral-tripo.fbx.glb']:
    p=LOCAL/name
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if p.suffix=='.fbx':bpy.ops.import_scene.fbx(filepath=str(p))
    else:bpy.ops.import_scene.gltf(filepath=str(p))
    r={'path':str(p),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'meshes':[],'armatures':[]}
    for o in bpy.data.objects:
        if o.type=='MESH':
            xyz=np.array([tuple(o.matrix_world@v.co) for v in o.data.vertices]);o.data.calc_loop_triangles()
            r['meshes'].append({'name':o.name,'vertices':len(xyz),'triangles':len(o.data.loop_triangles),'bounds':[xyz.min(0).tolist(),xyz.max(0).tolist()],'uv':[x.name for x in o.data.uv_layers],'materials':[x.name for x in o.data.materials],'groups':len(o.vertex_groups)})
        if o.type=='ARMATURE':
            r['armatures'].append({'name':o.name,'bones':[{'name':b.name,'parent':b.parent.name if b.parent else None,'head':list(o.matrix_world@b.head_local),'tail':list(o.matrix_world@b.tail_local)} for b in o.data.bones]})
    rows.append(r)
(OUT/'intake-inspection.json').write_text(json.dumps(rows,indent=2,ensure_ascii=False),encoding='utf8')
print('INTAKE',json.dumps([{**{k:v for k,v in r.items() if k not in ['armatures']},'bones':[len(x['bones']) for x in r['armatures']]} for r in rows]))
