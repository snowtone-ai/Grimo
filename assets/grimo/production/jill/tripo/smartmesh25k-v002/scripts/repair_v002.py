"""Continue only the saved v001 master. Local face edits and bounded proof corrections.
No import, remesh, decimation, scaling, rig, texture, or external service.
"""
import bpy,sys,json,math,hashlib
from pathlib import Path
import numpy as np
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[7];OLD=ROOT/'assets/grimo/production/jill/tripo/smartmesh25k-v001'
ASSET=ROOT/'assets/grimo/production/jill/tripo/smartmesh25k-v002';E=ROOT/'docs/production/jill/evidence/smartmesh25k-v002'
sys.path.insert(0,str(OLD/'scripts'))
from audit_common import components
assert Path(bpy.data.filepath).resolve()==(OLD/'jill-geometry-master.blend').resolve()
o=bpy.data.objects['JILL_GEOMETRY_MASTER'];m=o.data;s=bpy.context.scene;s.frame_set(1)
inv=o.matrix_world.inverted();base=np.array([tuple(o.matrix_world@v.co) for v in m.vertices]);xyz=base.copy();n=len(xyz)
parts=components(m);adj=[[] for _ in range(n)]
for e in m.edges:
    i,j=e.vertices;adj[i].append(j);adj[j].append(i)
oldkeys={k.name:np.array([tuple(o.matrix_world@v.co) for v in k.data]) for k in m.shape_keys.key_blocks}
oldnorm=[tuple(x.vector) for x in m.corner_normals]
def smooth(a,b,x):
    t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)
# Existing eye surfaces only. Fix boundary and silhouette; small interior convexity.
eye_ids=[]
for c in [98,99]:
    ids=parts[c]['v'];edge_count={}
    for pi in parts[c]['f']:
        for edge in m.polygons[pi].edge_keys:edge_count[edge]=edge_count.get(edge,0)+1
    border={i for edge,count in edge_count.items() if count==1 for i in edge}
    q=base[ids];center=(q.min(0)+q.max(0))/2;radius=(q.max(0)-q.min(0))/2
    for i in ids:
        if i in border:continue
        r2=((base[i,0]-center[0])/radius[0])**2+((base[i,2]-center[2])/radius[2])**2
        xyz[i,1]-=.004*max(0,1-r2)**2;eye_ids.append(i)
# Only the visibly irregular lower mouth rim, one bounded relaxation pass.
mouth_ids=np.where((abs(base[:,0])<.046)&(base[:,1]<-.390)&(base[:,2]>.569)&(base[:,2]<.591))[0]
for i in mouth_ids:
    if not adj[i]:continue
    delta=(base[adj[i]].mean(0)-base[i])*.22
    length=np.linalg.norm(delta)
    if length>.0008:delta*=.0008/length
    xyz[i]+=delta
changed=np.where(np.linalg.norm(xyz-base,axis=1)>1e-10)[0]
for i in changed:
    co=inv@Vector(xyz[i]);m.vertices[int(i)].co=co;m.shape_keys.key_blocks['Basis'].data[int(i)].co=co
m.update()
# Update only local affected normals. Preserve all other imported corner normals.
affected=set(eye_ids)|set(map(int,mouth_ids))
for i in list(affected):affected.update(adj[i])
normal=np.zeros((n,3))
for p in m.polygons:
    vs=list(p.vertices);q=np.array([tuple(m.vertices[i].co) for i in vs])
    area=np.cross(q[1]-q[0],q[2]-q[0])
    for i in vs:
        if i in affected:normal[i]+=area
newnorm=oldnorm.copy()
for p in m.polygons:
    for li,i in zip(p.loop_indices,p.vertices):
        if i in affected and np.linalg.norm(normal[i])>1e-10:newnorm[li]=tuple(normal[i]/np.linalg.norm(normal[i]))
m.normals_split_custom_set(newnorm)
body=np.zeros(n);body[parts[0]['v']]=1;masks={}
for name,cs in [('WingL',[2,4]),('WingR',[1])]:
    w=np.zeros(n);ids=[i for c in cs for i in parts[c]['v']];w[ids]=smooth(.070,.170,abs(xyz[ids,0]));masks[name]=w
# Harmonic shoulder transfer on existing body connectivity. Whole distal paw is fixed at 1.
for name,sgn in [('ArmL',1),('ArmR',-1)]:
    x=sgn*xyz[:,0];domain=(body>0)&(x>.12)&(xyz[:,1]<-.065)&(xyz[:,2]>.24)&(xyz[:,2]<.555)
    seeds=domain&(x>.205)&(xyz[:,1]<-.11)&(xyz[:,2]>.285)&(xyz[:,2]<.50)
    w=np.zeros(n);w[seeds]=1;free=np.where(domain&~seeds)[0]
    # Fixed iteration count is an edit construction, not a pass/fail test.
    for _ in range(240):
        v=w.copy()
        for i in free:
            if adj[i]:v[i]=np.mean(w[adj[i]])
        w=v
    w[w<.0001]=0;masks[name]=w
tail=body*smooth(.09,.23,xyz[:,1])*(1-smooth(.535,.575,xyz[:,2]))
tail_leaves=[]
for ci,c in enumerate(parts):
    q=xyz[c['v']]
    if ci>0 and c['f'] and q[:,1].min()>.09 and q[:,2].max()<.52:
        # Follow the same field as the adjacent tail, avoiding a leaf/root phase offset.
        tail[c['v']]=smooth(.09,.23,q[:,1]);tail_leaves.append(ci)
masks['Tail']=tail
specs=[('WingL_Open','WingL',-12,'Z',(.070,-.125,.49)),('WingL_Close','WingL',20,'Z',(.070,-.125,.49)),
 ('WingR_Open','WingR',12,'Z',(-.070,-.125,.49)),('WingR_Close','WingR',-20,'Z',(-.070,-.125,.49)),
 ('Tail_Left','Tail',-12,'Z',(0,.09,.22)),('Tail_Right','Tail',12,'Z',(0,.09,.22)),
 ('ArmL_Offer','ArmL',-25,'X',(.14,-.19,.465)),('ArmR_Offer','ArmR',-25,'X',(-.14,-.19,.465))]
for name,region,angle,axis,pivot in specs:
    key=m.shape_keys.key_blocks['TEST_ONLY_'+name]
    for i in range(n):
        p=Vector(xyz[i]);w=masks[region][i]
        if w:p=Vector(pivot)+Matrix.Rotation(math.radians(angle)*float(w),3,axis)@(p-Vector(pivot))
        if region.startswith('Wing') and name.endswith('_Open'):p.y+=.040*float(w)
        key.data[i].co=inv@p
    key.value=0
for group in list(o.vertex_groups):
    if group.name.startswith('DIAGNOSTIC_'):o.vertex_groups.remove(group)
for name,w in masks.items():
    g=o.vertex_groups.new(name='DIAGNOSTIC_'+name)
    for i in np.where(w>0)[0]:g.add([int(i)],float(w[i]),'REPLACE')
o['authority']='v002 continuation of the existing v001 sole master; Human Geometry Gate HOLD/PENDING. No Tripo authorization.'
o['repair_v002']='Existing eye interior convexity <=.004; lower mouth rim <=.0008; diagnostic root transfer corrected. Not final rig or motion.'
o['material_note']='Original material retained. TEMP_DIAGNOSTIC materials are capture-only and not formal Texture.'
s.frame_set(1);bpy.context.view_layer.update()
ASSET.mkdir(parents=True,exist_ok=True);bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(ASSET/'jill-geometry-master-v002.blend'))
np.savez_compressed(E/'repair-data.npz',before=base,after=xyz,changed=changed,**{'mask_'+k:v for k,v in masks.items()})
report={'source_master':str((OLD/'jill-geometry-master.blend').relative_to(ROOT)),'source_sha256':hashlib.sha256((OLD/'jill-geometry-master.blend').read_bytes()).hexdigest(),
 'changed_neutral_vertex_ids':changed.tolist(),'eye_interior_vertex_ids':eye_ids,'lower_mouth_vertex_ids':mouth_ids.tolist(),
 'max_neutral_delta':float(np.linalg.norm(xyz-base,axis=1).max()),'vertices':n,'polygons':len(m.polygons),'uv_layers':len(m.uv_layers),
 'local_normals_affected_vertices':sorted(affected),'specs':specs,'tail_leaf_components':tail_leaves,
 'limits':['diagnostic shapes only','not approved pose references','existing root intersections may remain','Human decides GO']}
(E/'repair.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print('V002_SAVED',len(changed),report['max_neutral_delta'])
