"""Explicitly bound intentional mouth geometry/UV/morph changes; no global equality claim."""
import ast,json,hashlib
from pathlib import Path
from collections import Counter
import bpy,numpy as np
ROOT=Path(__file__).resolve().parents[2];E=ROOT/'docs/production/jill/mouth-integration-v006';A=ROOT/'assets/grimo/production/jill/tripo'
tree=ast.parse((ROOT/'scripts/blender/jill-texture-review-v005.py').read_text(encoding='utf8'))
ns={'__file__':str(ROOT/'scripts/blender/jill-texture-review-v005.py')}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef)) or isinstance(n,ast.Assign) and not any(isinstance(t,ast.Name) and t.id=='cmd' for t in n.targets)],type_ignores=[]),'<helpers>','exec'),ns)
def capture(path):
    o,r=ns['openfile'](path);m=o.data
    return {'contract':ns['contract'](o,r),'keys':{k.name:np.array([v.co[:] for v in k.data]) for k in m.shape_keys.key_blocks},'faces':[(tuple(p.vertices),m.materials[p.material_index].get('paint_owner'),[[tuple(m.uv_layers[u].data[i].uv) for i in p.loop_indices] for u in range(len(m.uv_layers))]) for p in m.polygons], 'weights':[[(g.group,g.weight) for g in v.groups] for v in m.vertices], 'images':{im.name:hashlib.sha256(bytes(im.packed_file.data)).hexdigest() for im in bpy.data.images if im.packed_file},'vertices':len(m.vertices),'polygons':len(m.polygons)}
src=capture(A/'texture-return-v005/jill-textured-rig-v005.blend');dst=capture(A/'mouth-integration-v006/jill-textured-rig-v006.blend')
regions=np.load(ROOT/'docs/production/jill/rig-pretexture-v002/surface-contract.npz')['regions'];probe=json.loads((E/'cut-probe.json').read_text());removed=set(probe['removed'])
kept=[i for i in range(len(src['faces'])) if i not in removed and regions[i] not in ['mouth-skin','mouth-inner']]
face_lookup={f[0]:f for f in dst['faces']};face_diffs=[i for i in kept if src['faces'][i]!=face_lookup.get(src['faces'][i][0])]
key_deltas={}
for key,coords in src['keys'].items():
    delta=np.linalg.norm(dst['keys'][key][:len(coords)]-coords,axis=1);ids=np.flatnonzero(delta>1e-7)
    key_deltas[key]={'changed_original_vertices':ids.tolist(),'max_delta_m':float(delta.max()),'source_bounds':{'min':coords[ids].min(axis=0).tolist(),'max':coords[ids].max(axis=0).tolist()} if len(ids) else None}
    if len(ids):
        base=src['keys']['Basis'][ids]
        print('CHANGED',key,len(ids),base.min(axis=0),base.max(axis=0),flush=True)
        assert np.all((abs(base[:,0])<.085)&(base[:,1]<-.25)&(base[:,2]>.53)&(base[:,2]<.66)),(key,'change outside mouth')
c0=src['contract'];c1=dst['contract'];equal_fields=['bones','anchors','channels','groups'];assert all(c0[k]==c1[k] for k in equal_fields)
driver_deltas=[{'before':a,'after':b} for a,b in zip(c0['drivers'],c1['drivers']) if a!=b]
assert len(driver_deltas)==3 and all(any(k in d['after'][0] for k in ['FACE_MouthOpen','FACE_Smile.L','FACE_Smile.R']) for d in driver_deltas)
assert src['images']==dst['images'],'Texture data changed'
assert src['weights']==dst['weights'][:src['vertices']],'Existing skin weights changed'
assert not face_diffs,face_diffs
assert len(c1['bones'])==130 and len(c1['channels'])==39 and len(c1['keys'])==21 and len(c1['anchors'])==16
mesh=bpy.data.objects['Jill_Body'].data;edge=Counter(tuple(sorted((a,b))) for p in mesh.polygons for a,b in zip(p.vertices,list(p.vertices)[1:]+[p.vertices[0]]))
new_edges={tuple(sorted((a,b))) for p in mesh.polygons if any(i>=src['vertices'] for i in p.vertices) for a,b in zip(p.vertices,list(p.vertices)[1:]+[p.vertices[0]])}
bad=[(e,edge[e]) for e in new_edges if edge[e]!=2];assert not bad,bad
report={'pass':True,'scope':'Explicit local topology replacement; global geometry/UV equality is NOT claimed','source_vertices':src['vertices'],'candidate_vertices':dst['vertices'],'source_polygons':src['polygons'],'candidate_polygons':dst['polygons'],'removed_original_polygons':len(removed),'removed_auxiliary_regions':['mouth-skin','mouth-inner'],'unchanged_surviving_faces_and_all_uvs':len(kept),'surviving_face_uv_differences':face_diffs,'new_patch_vertices':dst['vertices']-src['vertices'],'new_patch_edge_incidence_errors':bad,'unchanged':equal_fields+['existing_weights','packed_texture_bytes'],'morph_deltas':key_deltas,'texture_hashes':dst['images'],'new_patch_uv':'Unique UV islands from removed mouth owner faces reused/split; three UV sets preserved; retained face UV loops unchanged.'}
report['driver_deltas']=driver_deltas
(E/'local-preservation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({k:v for k,v in report.items() if k not in ['morph_deltas','texture_hashes']},indent=2),flush=True)
