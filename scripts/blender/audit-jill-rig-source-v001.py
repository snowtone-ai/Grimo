"""Focused source correspondence audit after Plan freeze. No blend writes."""
import bpy,json,hashlib
from pathlib import Path
import numpy as np
from mathutils.kdtree import KDTree
ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'assets/grimo/production/jill/tripo/rig-other-v001/source'
OUT=ROOT/'docs/production/jill/rig-other-v001'
def xyz(o):return np.array([tuple(o.matrix_world@v.co) for v in o.data.vertices])
def components(m):
    p=list(range(len(m.vertices)))
    def root(i):
        while p[i]!=i:p[i]=p[p[i]];i=p[i]
        return i
    for e in m.edges:
        a,b=map(root,e.vertices);p[b]=a
    g={}
    for v in m.vertices:g.setdefault(root(v.index),[]).append(v.index)
    return sorted(g.values(),key=lambda v:-len(v))
bpy.ops.wm.open_mainfile(filepath=str(SRC/'jill-v002-authority-donor.blend'))
o=bpy.data.objects['JILL_GEOMETRY_MASTER'];bpy.context.scene.frame_set(1)
v=xyz(o);faces=[list(p.vertices) for p in o.data.polygons]
parts=components(o.data)
before=set(bpy.data.objects)
bpy.ops.import_scene.fbx(filepath=str(SRC/'tripo-other-original.fbx'))
f=next(x for x in bpy.data.objects if x not in before and x.type=='MESH');q=xyz(f)
# Expected uniform Tripo normalization, verify both indexed and nearest correspondence.
scale=float((v.max(0)-v.min(0))[2]/(q.max(0)-q.min(0))[2]);offset=v.mean(0)-scale*q.mean(0)
aligned=q*scale+offset
report={'donor_sha256':hashlib.sha256((SRC/'jill-v002-authority-donor.blend').read_bytes()).hexdigest(),
 'scale_fbx_to_authority':scale,'offset_fbx_to_authority':offset.tolist(),
 'indexed_position_max_error':float(np.max(np.linalg.norm(aligned-v,axis=1))),
 'topology_indexed_equal':faces==[list(p.vertices) for p in f.data.polygons],
 'authority_bounds':[v.min(0).tolist(),v.max(0).tolist()],
 'parts':[{'id':i,'vertices':len(ids),'bounds':[v[ids].min(0).tolist(),v[ids].max(0).tolist()],'center':v[ids].mean(0).tolist()} for i,ids in enumerate(parts)],
 'donor_groups':[x.name for x in o.vertex_groups],'donor_shapes':[x.name for x in o.data.shape_keys.key_blocks],
 'fbx_matrix':list(map(list,f.matrix_world))}
np.savez_compressed(OUT/'authority-parts.npz',xyz=v,component=np.array([next(c for c,ids in enumerate(parts) if i in ids) for i in range(len(v))]))
(OUT/'source-correspondence.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print('CORRESPONDENCE',json.dumps({k:val for k,val in report.items() if k!='parts'}))
