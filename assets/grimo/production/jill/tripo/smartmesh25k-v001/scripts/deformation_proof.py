"""Bounded diagnostic shape controls on the sole FBX-derived master; not a production rig."""
import sys,json,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from audit_common import *
from mathutils import Matrix
o=bpy.data.objects['JILL_GEOMETRY_MASTER'];m=o.data;scene=bpy.context.scene
scene.frame_set(1)
if m.shape_keys:
    assert all(k.name=='Basis' or k.name.startswith('TEST_ONLY_') for k in m.shape_keys.key_blocks)
    assert all(tuple(a.co)==tuple(b.co) for a,b in zip(m.vertices,m.shape_keys.key_blocks['Basis'].data))
    o.shape_key_clear()
    for vg in list(o.vertex_groups):
        if vg.name.startswith('DIAGNOSTIC_'):o.vertex_groups.remove(vg)
xyz=np.array([tuple(o.matrix_world@v.co) for v in m.vertices]); inv=o.matrix_world.inverted()
parts=components(m);n=len(xyz)
def smooth(a,b,x):
    t=np.clip((x-a)/(b-a),0,1);return t*t*(3-2*t)
base=np.array([tuple(v.co) for v in m.vertices]); masks={}
for name,indices in [('WingL',[2,4]),('WingR',[1])]:
    w=np.zeros(n);ids=[v for i in indices for v in parts[i]['v']];w[ids]=smooth(.055,.14,np.abs(xyz[ids,0]));masks[name]=w
body=np.zeros(n);body[parts[0]['v']]=1
for name,sgn in [('ArmL',1),('ArmR',-1)]:
    masks[name]=body*smooth(.48,.53,sgn*xyz[:,0]+.8*xyz[:,2])*smooth(.29,.34,xyz[:,2])*(1-smooth(.49,.525,xyz[:,2]))*(1-smooth(-.07,-.035,xyz[:,1]))
tail_base=body.copy()
tail_components=[]
for i,p in enumerate(parts):
    if not p['f'] or i==0:continue
    q=xyz[p['v']]
    if q[:,1].min()>.09 and q[:,2].max()<.52:
        tail_base[p['v']]=1;tail_components.append(i)
masks['Tail']=tail_base*smooth(.09,.23,xyz[:,1])*(1-smooth(.49,.53,xyz[:,2]))
write_json('diagnostic-masks.json',{'coordinate_system':'Blender world: +X anatomical left, -Y front, +Z up',
 'purpose':'Local test envelopes only. No production skinning, no anatomy edits.',
 'wing_component_ids':{'WingL':[2,4],'WingR':[1]},'tail_leaf_components':tail_components,
 'vertices':{k:np.where(v>0)[0].tolist() for k,v in masks.items()},
 'weights':{k:[[int(i),float(v[i])] for i in np.where(v>0)[0]] for k,v in masks.items()}})

# Auditable control masks as vertex groups and colored review renders.
for name,w in masks.items():
    vg=o.vertex_groups.new(name='DIAGNOSTIC_'+name)
    for i in np.where(w>0)[0]:vg.add([int(i)],float(w[i]),'REPLACE')
original_slots=list(m.materials);orig_index=[p.material_index for p in m.polygons]
gray=bpy.data.materials.new('ReviewMaskNeutral');gray.diffuse_color=(.58,.68,.55,1)
red=bpy.data.materials.new('ReviewMaskActive');red.diffuse_color=(.95,.12,.08,1)
m.materials.clear();m.materials.append(gray);m.materials.append(red)
scene.display.shading.color_type='MATERIAL'
for name,w in masks.items():
    for p in m.polygons:p.material_index=int(max(w[list(p.vertices)])>0)
    render(scene,'mask-'+name+'-front',(1,-2,.35),(0,0,.5),1.16)
    render(scene,'mask-'+name+'-rear',(1,2,.35),(0,0,.5),1.16)
m.materials.clear()
for mat in original_slots:m.materials.append(mat)
for p,i in zip(m.polygons,orig_index):p.material_index=i
scene.display.shading.color_type='OBJECT'

basis=o.shape_key_add(name='Basis',from_mix=False)
specs=[('WingL_Open','WingL',-12,'Z',(.075,.015,.56)),('WingL_Close','WingL',20,'Z',(.075,.015,.56)),
       ('WingR_Open','WingR',12,'Z',(-.075,.015,.56)),('WingR_Close','WingR',-20,'Z',(-.075,.015,.56)),
       ('Tail_Left','Tail',-12,'Z',(0,.09,.22)),('Tail_Right','Tail',12,'Z',(0,.09,.22)),
       ('ArmL_Offer','ArmL',-25,'X',(.13,-.13,.44)),('ArmR_Offer','ArmR',-25,'X',(-.13,-.13,.44))]
keys={}
for name,region,angle,axis,pivot in specs:
    key=o.shape_key_add(name='TEST_ONLY_'+name,from_mix=False);keys[name]=key
    for i in np.where(masks[region]>0)[0]:
        p=Vector(xyz[i]);center=Vector(pivot)
        p=center+Matrix.Rotation(math.radians(angle)*float(masks[region][i]),3,axis)@(p-center)
        key.data[int(i)].co=inv@p
    key.value=0
o['diagnostic_control_note']='8 bounded test shape keys only; all default to zero. No final rig. Angles are diagnostic probes, not approved motion ranges.'
cases=[(s[0],[s[0]]) for s in specs]+[
 ('BothWings_Open',['WingL_Open','WingR_Open']),('BothWings_Close',['WingL_Close','WingR_Close']),
 ('Combined_Left',['WingL_Close','ArmL_Offer','Tail_Left']),('Combined_Right',['WingR_Close','ArmR_Offer','Tail_Right'])]
scene.frame_start=1;scene.frame_end=1+24*len(cases);scene.render.fps=24
for key in keys.values():key.value=0;key.keyframe_insert('value',frame=1)
for ci,(name,active) in enumerate(cases):
    start=1+24*ci
    for frame,value in [(start,0),(start+6,.5),(start+12,1),(start+18,.5),(start+24,0)]:
        for kn,key in keys.items():key.value=value if kn in active else 0;key.keyframe_insert('value',frame=frame)
    scene.timeline_markers.new(name,frame=start+12)
if m.shape_keys.animation_data and m.shape_keys.animation_data.action:
    m.shape_keys.animation_data.action.name='DIAGNOSTIC_ONLY_12_BOUNDED_CASES'
    for layer in m.shape_keys.animation_data.action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for fc in bag.fcurves:
                    for point in fc.keyframe_points:point.interpolation='LINEAR'

# Quantify target-only motion, protected face/feet, continuity, and neutral return.
m.calc_loop_triangles(); tris=np.array([list(t.vertices) for t in m.loop_triangles]);edges=np.array([list(e.vertices) for e in m.edges])
edge0=np.linalg.norm(xyz[edges[:,1]]-xyz[edges[:,0]],axis=1)
def area(p):return np.linalg.norm(np.cross(p[tris[:,1]]-p[tris[:,0]],p[tris[:,2]]-p[tris[:,0]]),axis=1)*.5
area0=area(xyz);protected=(xyz[:,2]>.64)|(xyz[:,2]<.10)
report={'specs':[{'key':s[0],'region':s[1],'degrees':s[2],'axis':s[3],'pivot':s[4]} for s in specs],
        'method':'Local angle-weighted test shapes, linear key value sweeps; immutable Basis. A sampled diagnostic, not rig or collision certification.',
        'cases':[],'collision_scope':'Visual review plus moving-versus-stationary triangle overlap changes; see collision report. No continuous collision guarantee.'}
evaluated_positions={}
for ci,(name,active) in enumerate(cases):
    start=1+24*ci;allowed=np.zeros(n,dtype=bool)
    for kn in active:allowed|=masks[next(s[1] for s in specs if s[0]==kn)]>0
    samples=[]
    for frame in [start,start+6,start+12,start+18,start+24]:
        scene.frame_set(frame);bpy.context.view_layer.update()
        ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());em=ev.to_mesh()
        p=np.array([tuple(o.matrix_world@v.co) for v in em.vertices]);ev.to_mesh_clear()
        displacement=np.linalg.norm(p-xyz,axis=1);length=np.linalg.norm(p[edges[:,1]]-p[edges[:,0]],axis=1)
        ratios=length[edge0>1e-7]/edge0[edge0>1e-7];ar=area(p);valid=area0>1e-10
        samples.append({'frame':frame,'max_displacement':float(displacement.max()),
                        'max_non_target_displacement':float(displacement[~allowed].max()),
                        'max_face_and_feet_displacement':float(displacement[protected].max()),
                        'edge_length_ratio_min':float(ratios.min()),'edge_length_ratio_max':float(ratios.max()),
                        'new_degenerate_triangles':int(np.sum((ar<1e-10)&valid)),
                        'triangle_area_ratio_min':float((ar[valid]/area0[valid]).min())})
        if frame==start+12:evaluated_positions[name]=p
    report['cases'].append({'name':name,'active_keys':active,'samples':samples,
                            'neutral_return_max':samples[-1]['max_displacement']})
    scene.frame_set(start+12)
    for view,d in [('front',(0,-1,0)),('rear',(1,2,.35)),('side',(1,0,0))]:
        render(scene,'proof-'+name+'-'+view,d,(0,0,.5),1.16)
    if 'Wing' in name:
        side=-1 if 'WingR' in name else 1
        render(scene,'proof-'+name+'-root',(side,1,.2),(.18*side,.06,.52),.48)
    if name.startswith('Tail'):
        render(scene,'proof-'+name+'-root',(1,1,.15),(0,.19,.29),.64)
scene.frame_set(1)
render(scene,'proof-neutral-return-front',(0,-1,0),(0,0,.5),1.16)
write_json('deformation-validation.json',report)
np.savez_compressed(EVIDENCE/'diagnostic-positions.npz',neutral=xyz,triangles=tris,**evaluated_positions)
bpy.context.view_layer.objects.active=o;bpy.ops.object.select_all(action='DESELECT');o.select_set(True)
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(ASSET/'jill-geometry-master.blend'))
print('DIAGNOSTIC_PROOF_COMPLETE',len(cases))
