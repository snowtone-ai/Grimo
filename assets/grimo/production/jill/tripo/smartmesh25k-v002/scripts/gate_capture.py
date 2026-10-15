"""Saved-file geometry gate evidence. Capture-only materials; never saves the blend."""
import bpy,sys,json,hashlib
from pathlib import Path
import numpy as np
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[7];OLD=ROOT/'assets/grimo/production/jill/tripo/smartmesh25k-v001'
E=ROOT/'docs/production/jill/evidence/smartmesh25k-v002'
sys.path.insert(0,str(OLD/'scripts'));import audit_common as a
a.EVIDENCE=E
def jpeg_render(scene,name,direction,target=(0,0,0),scale=3):
    a.setup_camera(scene,direction,target,scale)
    scene.render.image_settings.file_format='JPEG';scene.render.image_settings.quality=96
    scene.render.filepath=str(E/'renders'/f'{name}.jpg')
    bpy.ops.render.render(write_still=True)
a.render=jpeg_render
o=bpy.data.objects['JILL_GEOMETRY_MASTER'];m=o.data;s=bpy.context.scene;s.frame_set(1)
preview='--preview' in sys.argv
def xyz():
    ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());em=ev.to_mesh()
    p=np.array([tuple(o.matrix_world@v.co) for v in em.vertices]);ev.to_mesh_clear();return p
base=xyz();repair=np.load(E/'repair-data.npz');old=np.load(ROOT/'docs/production/jill/evidence/smartmesh25k-v001/diagnostic-positions.npz')
tris=old['triangles'];edges=np.array([list(e.vertices) for e in m.edges]);parts=a.components(m)
proof=json.loads((ROOT/'docs/production/jill/evidence/smartmesh25k-v001/deformation-validation.json').read_text())
def cross(p,moving,stationary):
    A=BVHTree.FromPolygons(p.tolist(),tris[moving].tolist(),all_triangles=True)
    B=BVHTree.FromPolygons(p.tolist(),tris[stationary].tolist(),all_triangles=True)
    return {(int(moving[i]),int(stationary[j])) for i,j in A.overlap(B) if not set(tris[moving[i]])&set(tris[stationary[j]])}
def lengths(p):return np.linalg.norm(p[edges[:,1]]-p[edges[:,0]],axis=1)
def areas(p):return np.linalg.norm(np.cross(p[tris[:,1]]-p[tris[:,0]],p[tris[:,2]]-p[tris[:,0]]),axis=1)*.5
edge0=lengths(base);oldedge=lengths(old['neutral']);area0=areas(base)
report={'source':bpy.data.filepath,'saved_neutral_matches_constructed':bool(np.max(abs(base-repair['after']))<6e-8),
 'topology_same_vertex_face_counts':len(m.vertices)==28050 and len(m.polygons)==28809,
 'basis_matches_mesh':all(tuple(v.co)==tuple(k.co) for v,k in zip(m.vertices,m.shape_keys.key_blocks['Basis'].data)),
 'armatures':len([x for x in s.objects if x.type=='ARMATURE']),'uv_layers':len(m.uv_layers),'images':len(bpy.data.images),
 'cases':[],'collision_method':'Same union of old/new moving vertices per case, triangle surface overlaps, shared-vertex pairs excluded. New pairs relative to each neutral. Not penetration depths or complete self-collision.',
 'visual_status':'PENDING_ACTUAL_IMAGE_REVIEW','human_status':'PENDING','tripo':'NO_OPERATIONS_OR_CREDITS'}
positions={}
prior=None
if '--tail-only' in sys.argv:
    prior=json.loads((E/'saved-gate-validation.json').read_text())
for ci,c in enumerate(proof['cases']):
    if prior and c['name'] not in ['Tail_Left','Tail_Right','Combined_Left','Combined_Right']:
        report['cases'].append(prior['cases'][ci]);continue
    name=c['name'];start=1+24*ci;s.frame_set(start+12);bpy.context.view_layer.update();peak=xyz();positions[name]=peak
    move=(np.linalg.norm(peak-base,axis=1)>1e-8)|(np.linalg.norm(old[name]-old['neutral'],axis=1)>1e-8)
    moving=np.where(np.any(move[tris],axis=1))[0];stationary=np.where(~np.any(move[tris],axis=1))[0]
    newbaseline=cross(base,moving,stationary);oldbaseline=cross(old['neutral'],moving,stationary)
    samples=[]
    region=np.zeros(len(base),dtype=bool)
    for key in c['active_keys']:
        r=next(r for k,r,*_ in json.loads((E/'repair.json').read_text())['specs'] if k==key);region|=repair['mask_'+r]>0
    for offset,level in [(0,0),(6,.5),(12,1),(18,.5),(24,0)]:
        s.frame_set(start+offset);bpy.context.view_layer.update();p=xyz();disp=np.linalg.norm(p-base,axis=1)
        ratio=lengths(p)[edge0>1e-7]/edge0[edge0>1e-7]
        sample={'frame':start+offset,'amplitude':level,'max_nontarget_displacement':float(disp[~region].max()),
         'face_feet_max_displacement':float(disp[(base[:,2]>.64)|(base[:,2]<.10)].max()),
         'edge_ratio_min':float(ratio.min()),'edge_ratio_max':float(ratio.max()),
         'new_degenerate_triangles':int(np.sum((areas(p)<1e-10)&(area0>1e-10)))}
        if offset in [6,12]:
            newpairs=cross(p,moving,stationary)-newbaseline;oldp=old['neutral']+(old[name]-old['neutral'])*level
            oldpairs=cross(oldp,moving,stationary)-oldbaseline
            oldrat=lengths(oldp)[oldedge>1e-7]/oldedge[oldedge>1e-7]
            sample.update({'new_crossing_pairs':len(newpairs),'v001_crossing_pairs_same_union':len(oldpairs),'v001_edge_ratio_max':float(oldrat.max()),
             'new_pair_ids':[list(x) for x in sorted(newpairs)]})
        if level==0:sample['neutral_delta']=float(disp.max())
        samples.append(sample)
    report['cases'].append({'name':name,'samples':samples})
(E/'saved-gate-validation.json').write_text(json.dumps(report,indent=2),encoding='utf8')
if prior:
    previous=np.load(E/'evaluated-positions.npz')
    positions={**{k:previous[k] for k in previous.files if k not in ['neutral','triangles']},**positions}
np.savez_compressed(E/'evaluated-positions.npz',neutral=base,triangles=tris,**positions)
print('VALIDATION',json.dumps([{ 'name':c['name'],'old_new_cross':[c['samples'][2]['v001_crossing_pairs_same_union'],c['samples'][2]['new_crossing_pairs']],
 'old_new_stretch':[c['samples'][2]['v001_edge_ratio_max'],c['samples'][2]['edge_ratio_max']]} for c in report['cases']]),flush=True)
a.setup_render(s)
if '--validate-only' in sys.argv:sys.exit(0)
VIEWS=[('front',(0,-1,0),(0,0,.5),1.16),('left-facing-side',(1,0,0),(0,0,.5),1.16),
 ('right-facing-side',(-1,0,0),(0,0,.5),1.16),('back',(0,1,0),(0,0,.5),1.16),
 ('front-three-quarter',(1,-2,.45),(0,0,.5),1.16),('opposite-front-three-quarter',(-1,-2,.45),(0,0,.5),1.16),
 ('rear-three-quarter',(1,2,.4),(0,0,.5),1.16),('wing-underside',(1,1,-.8),(0,.05,.53),.96),
 ('wing-root-left',(1,1,.2),(.18,.06,.52),.48),('wing-root-right',(-1,1,.2),(-.18,.06,.52),.48),
 ('tail-root',(1,1,.15),(0,.19,.29),.64),('soles',(0,-.3,-1),(0,0,.09),.66),
 ('face-front',(0,-1,0),(0,-.20,.72),.60),('face-three-quarter',(1,-2,.15),(0,-.18,.72),.60),
 ('face-left',(1,0,0),(0,-.20,.72),.60),('face-right',(-1,0,0),(0,-.20,.72),.60),
 ('wing-underside-detail-left',(1,3,-.5),(.25,.04,.56),.55),('wing-underside-detail-right',(-1,3,-.5),(-.25,.04,.56),.55),
 ('shoulder-left',(1,-2,.25),(.16,-.12,.42),.50),('shoulder-right',(-1,-2,.25),(-.16,-.12,.42),.50)]
s.frame_set(1)
if not preview:a.render(s,'v002-neutral-gif-rear',(1,2,.35),(0,0,.5),1.16)
for name,d,t,scale in VIEWS:
    if not preview or name in ['face-front','face-three-quarter','wing-root-left','shoulder-left','tail-root']:a.render(s,'v002-neutral-'+name,d,t,scale)
for ci,c in enumerate(proof['cases']):
    if preview and c['name'] not in ['WingL_Open','WingL_Close','ArmL_Offer','Tail_Left']:continue
    name=c['name'];side=-1 if name in ['WingR_Open','WingR_Close','ArmR_Offer','Combined_Right'] else 1
    for stage,offset in ([('peak',12)] if preview else [('half',6),('peak',12),('return',24)]):
        s.frame_set(1+24*ci+offset)
        views=[('front',(0,-1,0)),('front3q',(1,-2,.45)),('side',(side,0,0))]
        if stage!='return':views.append(('rear',(1,2,.35)))
        if stage=='peak' and not preview:views.extend([('opposite-side',(-side,0,0)),('opposite-front3q',(-1,-2,.45))])
        for v,d in views:a.render(s,f'v002-{stage}-{name}-{v}',d,(0,0,.5),1.16)
        if stage=='return':a.render(s,f'v002-return-{name}-gif-rear',(1,2,.35),(0,0,.5),1.16)
        if stage!='return':
            if 'Wing' in name:
                d=(side,1,.2);t=(.18*side,.06,.52);scale=.48
            elif name.startswith('Tail'):
                d=(1,1,.15);t=(0,.19,.29);scale=.64
            else:d=(side,-2,.25);t=(.16*side,-.12,.42);scale=.50
            a.render(s,f'v002-{stage}-{name}-detail',d,t,scale)
# Transient material diagnosis using existing surfaces. No texture image or UV.
s.frame_set(1)
def mat(name,col):
    v=bpy.data.materials.new('TEMP_DIAGNOSTIC_'+name);v.diffuse_color=(*col,1);m.materials.append(v);return len(m.materials)-1
skin=mat('skin',(.58,.68,.55));eye=mat('eye',(.025,.06,.025));mouth=mat('mouth',(.20,.025,.035));tongue=mat('tongue',(.8,.25,.28))
for p in m.polygons:p.material_index=skin
for c in [98,99]:
    for pi in parts[c]['f']:m.polygons[pi].material_index=eye
for p in m.polygons:
    q=base[list(p.vertices)].mean(0)
    if (q[0]/.044)**2+((q[2]-.605)/.037)**2<.85 and -.392<q[1]<-.33:
        p.material_index=mouth if q[2]>.588 else tongue
s.display.shading.color_type='MATERIAL'
for v,d in [('front',(0,-1,0)),('3q',(1,-2,.15)),('left',(1,0,0)),('right',(-1,0,0))]:a.render(s,'face-material-v002-'+v,d,(0,-.20,.72),.60)
print('CAPTURE_COMPLETE_NO_BLEND_RESAVE',flush=True)
