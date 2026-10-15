"""Read the existing sole master; never save it."""
import bpy, sys, json, hashlib
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[7]
OLD=ROOT/'assets/grimo/production/jill/tripo/smartmesh25k-v001'
OUT=ROOT/'docs/production/jill/evidence/smartmesh25k-v002'
OUT.mkdir(parents=True,exist_ok=True)
(OUT/'renders').mkdir(exist_ok=True)
sys.path.insert(0,str(OLD/'scripts'))
from audit_common import components
o=bpy.data.objects['JILL_GEOMETRY_MASTER']; m=o.data
bpy.context.scene.frame_set(1)
xyz=np.array([tuple(o.matrix_world@v.co) for v in m.vertices])
parts=components(m)
report={'source':bpy.data.filepath,'matrix':list(map(list,o.matrix_world)),
 'parts':[{'id':i,'v':len(p['v']),'f':len(p['f']),
 'min':xyz[p['v']].min(0).tolist(),'max':xyz[p['v']].max(0).tolist()} for i,p in enumerate(parts) if p['f']],
 'objects':[{'name':x.name,'type':x.type,'hide_render':x.hide_render} for x in bpy.data.objects],
 'shape_keys':[k.name for k in m.shape_keys.key_blocks],
 'modifiers':[x.name for x in o.modifiers]}
(OUT/'inspection.json').write_text(json.dumps(report,indent=2),encoding='utf8')
np.savez_compressed(OUT/'inspection.npz',xyz=xyz,edges=np.array([list(e.vertices) for e in m.edges]))
protected=[p for folder in [OLD,ROOT/'assets/grimo/source/jill',ROOT/'docs/production/jill/evidence/smartmesh25k-v001'] for p in folder.rglob('*') if p.is_file() and '__pycache__' not in str(p)]
(OUT/'protected-inputs.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in protected},indent=2),encoding='utf8')
print(json.dumps(report))
