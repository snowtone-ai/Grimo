"""Fresh-process authoring replay and GLB reimport, bounded to the saved proof.

No input/source writes. Set comparison tolerates glTF seam splits and unused verts.
It does not certify appearance or arbitrary runtime control logic.
"""
import bpy,json,struct,sys,hashlib
from pathlib import Path
import numpy as np
from mathutils import Vector
from mathutils.kdtree import KDTree

ROOT=Path(__file__).resolve().parents[2]
A=ROOT/'assets/grimo/production/jill/tripo/rig-other-v001'
E=ROOT/'docs/production/jill/rig-other-v001'
contract=json.loads((E/'control-contract.json').read_text())
schedule=json.loads((E/'proof-schedule.json').read_text())
validation=json.loads((E/'pose-validation.json').read_text())
proof=np.load(E/'proof-positions.npz');bind=np.load(E/'rig-bind-data.npz')
components=np.load(E/'authority-parts.npz')['component']
def write(name,x):(E/name).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def coords(o):
    ob=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ob.to_mesh()
    out=np.array([tuple(o.matrix_world@v.co) for v in m.vertices]);ob.to_mesh_clear();return out
def update():rig.update_tag();bpy.context.view_layer.update()
def tree(a):
    k=KDTree(len(a))
    for i,p in enumerate(a):k.insert(Vector(p),i)
    k.balance();return k
def distance(a,b):
    k=tree(b);d=np.array([k.find(Vector(p))[2] for p in a])
    return {'max':float(d.max()),'p99':float(np.quantile(d,.99)),'mean':float(d.mean())}
def anchor_positions(names):
    result={};missing=[]
    for name in names:
        ob=bpy.data.objects.get(name)
        if ob:result[name]=np.array(ob.matrix_world.translation)
        else:
            found=False
            for arm in [o for o in bpy.data.objects if o.type=='ARMATURE']:
                if name in arm.pose.bones:
                    result[name]=np.array((arm.matrix_world@arm.pose.bones[name].matrix).translation);found=True;break
            if not found:missing.append(name)
    return result,missing

bpy.ops.wm.open_mainfile(filepath=str(A/'jill-rig-other-v001.blend'))
s=bpy.context.scene;rig=bpy.data.objects['JILL_RIG'];body=bpy.data.objects['Jill_Body']
channels=list(contract['authoring_properties']);names=[x['name'] for x in contract['anchors']]
driver_map=[]
for datablock,label in [(rig,'JILL_RIG'),(body.data.shape_keys,'Jill_Body.shape_keys')]+[(bpy.data.objects['Jill_Lids.'+side].data.shape_keys,'Jill_Lids.'+side+'.shape_keys') for side in ['L','R']]:
    for fc in datablock.animation_data.drivers:
        driver_map.append({'owner':label,'data_path':fc.data_path,'index':fc.array_index,'expression':fc.driver.expression,
          'variables':[{'name':v.name,'type':v.type,'id':t.id.name if t.id else None,'data_path':t.data_path} for v in fc.driver.variables for t in v.targets]})
write('runtime-mapping.json',{'coordinates':contract['coordinates'],'semantic_properties':contract['authoring_properties'],'drivers':driver_map,
 'bone_rest_matrices':{b.name:[list(row) for row in b.matrix_local] for b in rig.data.bones},
 'ik_targets':{o.name:{'matrix_world':[list(row) for row in o.matrix_world]} for o in bpy.data.objects if o.name.startswith('CTRL_')},
 'constraints':[{'bone':b.name,'type':c.type,'target':c.target.name if c.target else None,'chain_count':getattr(c,'chain_count',None),'use_stretch':getattr(c,'use_stretch',None),'owner_space':c.owner_space,'target_space':c.target_space} for b in rig.pose.bones for c in b.constraints],
 'runtime_limit':'Exact Blender authoring expressions/rest matrices for porting. No JavaScript IK implementation included; GLB proof samples are portable, arbitrary runtime compositions are not certified.'})
used=np.array(sorted(set(i for p in body.data.polygons for i in p.vertices)))
# The raw GLB source accessor is compared independently of its imported skin pose.
source_blob=(A/'source/tripo-other-original.glb').read_bytes()
sl,st=struct.unpack_from('<II',source_blob,12);sg=json.loads(source_blob[20:20+sl])
sa=sg['accessors'][sg['meshes'][0]['primitives'][0]['attributes']['POSITION']];sv=sg['bufferViews'][sa['bufferView']]
sp=np.frombuffer(source_blob,dtype='<f4',count=sa['count']*3,offset=28+sl+sv.get('byteOffset',0)+sa.get('byteOffset',0)).reshape(-1,3).astype(float)
sp=sp[:,[0,2,1]];sp[:,1]*=-1
corr=json.loads((E/'source-correspondence.json').read_text());sp=sp*corr['scale_fbx_to_authority']+corr['offset_fbx_to_authority']
write('source-glb-comparison.json',{'raw_glb_meshes':len(sg['meshes']),'raw_glb_animations':len(sg.get('animations',[])),
 'raw_glb_joints':len(sg['skins'][0]['joints']),'raw_glb_vertices':len(sp),'glb_to_v002_surface':distance(sp,bind['basis'][used]),
 'v002_surface_to_glb':distance(bind['basis'][used],sp),'method':'Raw accessor glTF Y-up converted to Blender Z-up and verified FBX uniform normalization. Independent of source skin pose. Unused donor vertices excluded.',
 'source_bind_status':'Imported source bind placement differs; not adopted. Rebuilt from verified FBX/v002 rest.'})
refs={};blend_rows=[]
cases=[('neutral',1,'neutral')]
for c in schedule:
    cases.append((c['name']+'-peak',c['peak'],c['name']+'-10'))
    if c['name'] in ['both-wings-fold','blink','combined-left','low-support']:
        cases.extend([(c['name']+'-half',c['half'],c['name']+'-5'),(c['name']+'-return',c['return'],c['name']+'-20')])
for label,frame,key in cases:
    s.frame_set(frame);update();p=coords(body)
    ap,missing=anchor_positions(names)
    refs[label]={'body':p[used],'lids':{side:coords(bpy.data.objects['Jill_Lids.'+side]) for side in ['L','R']},'anchors':ap}
    blend_rows.append({'case':label,'frame':frame,'saved_proof_max_delta':float(np.linalg.norm(p-proof[key],axis=1).max()),'missing_anchors':missing})

# Disable the proof action and operate semantic properties again after file reopen.
rig.animation_data.action=None
replay=[];independence=[]
for c in validation['cases']:
    for ch in channels:rig[ch]=0.
    rig.pose.bones['DEF_pelvis'].location=(0,0,0)
    for ch,val in c['values'].items():
        if ch=='pelvis_down':rig.pose.bones['DEF_pelvis'].location=rig.data.bones['DEF_pelvis'].matrix_local.to_3x3().inverted()@Vector((0,0,-val))
        else:rig[ch]=float(val)
    update();p=coords(body)
    replay.append({'case':c['name'],'direct_control_vs_saved_peak_max_delta':float(np.linalg.norm(p-proof[c['name']+'-10'],axis=1).max())})
    stationary=None
    if c['name'].startswith('wing-L'):stationary=~np.isin(components,[2,4])
    if c['name'].startswith('wing-R'):stationary=components!=1
    if c['name'].startswith('tail-'):stationary=(bind['basis'][:,1]<-.20)|(np.isin(components,[1,2,4,98,99]))
    if c['name'].startswith('paw-') and 'offer' in c['name']:stationary=np.isin(components,[1,2,4,98,99])|(bind['basis'][:,2]<.11)
    if stationary is not None:
        independence.append({'case':c['name'],'stationary_vertices':int(stationary.sum()),'stationary_max_delta':float(np.linalg.norm((p-bind['basis'])[stationary],axis=1).max())})
for ch in channels:rig[ch]=0.
rig.pose.bones['DEF_pelvis'].location=(0,0,0);update()
blend_return=float(np.linalg.norm(coords(body)-bind['basis'],axis=1).max())

# Parse the delivered GLB itself before importing it into a completely empty scene.
blob=(A/'jill-rig-other-v001.glb').read_bytes();length,kind=struct.unpack_from('<II',blob,12)
assert kind==0x4e4f534a
gltf=json.loads(blob[20:20+length]);nodes=gltf['nodes']
portable={'sha256':hashlib.sha256(blob).hexdigest(),'bytes':len(blob),'skins':[{'name':x.get('name'),'joints':len(x['joints'])} for x in gltf.get('skins',[])],
 'meshes':[{'name':m.get('name'),'primitives':len(m['primitives']),'morph_names':m.get('extras',{}).get('targetNames',[]),'vertices':sum(gltf['accessors'][p['attributes']['POSITION']]['count'] for p in m['primitives'])} for m in gltf.get('meshes',[])],
 'animations':[{'name':a.get('name'),'channels':len(a['channels']),'paths':sorted(set(c['target']['path'] for c in a['channels']))} for a in gltf.get('animations',[])],
 'anchor_nodes':[n.get('name') for n in nodes if n.get('name','').startswith('ANCHOR_')],
 'authoring_boundary':'Custom-property drivers and IK are not portable glTF logic. Sampled transforms/morph weights reproduce the proof; runtime arbitrary control mapping remains separate.'}
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.scene.render.fps=30
bpy.ops.import_scene.gltf(filepath=str(A/'jill-rig-other-v001.glb'))
s=bpy.context.scene;s.render.fps=30
body=next((o for o in bpy.data.objects if o.type=='MESH' and (o.name=='Jill_Body' or o.data.name.startswith('Jill_v002_PreservedSurface'))),None)
assert body and body.type=='MESH'
roundtrip=[]
for label,frame,key in cases:
    # The delivered accessor starts at 1/30 s, retaining authored frame 1.
    # Set fps BEFORE import because its action keys are created in frame units.
    import_frame=frame;s.frame_set(import_frame);bpy.context.view_layer.update();p=coords(body);ref=refs[label]
    ap,missing=anchor_positions(names)
    ar={name:float(np.linalg.norm(ref['anchors'][name]-ap[name])) for name in ap if name in ref['anchors']}
    lids={side:distance(coords(next(o for o in bpy.data.objects if o.type=='MESH' and (o.name=='Jill_Lids.'+side or o.data.name.startswith('Jill_CurvedLids.'+side)))),ref['lids'][side]) for side in ['L','R']}
    roundtrip.append({'case':label,'authoring_frame':frame,'import_frame':import_frame,'seconds':frame/30,'import_to_blend':distance(p,ref['body']),'blend_to_import':distance(ref['body'],p),
      'lids':lids,'anchor_max_delta':max(ar.values()) if ar else None,'missing_anchors':missing,'anchor_deltas':ar})

# Reimported geometry rendered with the same neutral diagnostic palette/cameras.
s.frame_set(1);bpy.context.view_layer.update();p=coords(body)
k=tree(bind['basis']);source_ids=np.array([k.find(Vector(x))[1] for x in p])
def material(name,c):
    m=bpy.data.materials.new('CAPTURE_ONLY_'+name);m.diffuse_color=(*c,1);return m
skin=material('skin',(.59,.69,.53));eye=material('eye',(.035,.065,.04));mouth=material('mouth',(.20,.055,.065))
body.data.materials.clear()
for m in [skin,eye,mouth]:body.data.materials.append(m)
for poly in body.data.polygons:
    idx=source_ids[poly.vertices[0]];poly.material_index=1 if components[idx] in [98,99] else 0
    q=p[list(poly.vertices)].mean(0)
    if (q[0]/.044)**2+((q[2]-.605)/.037)**2<.85 and -.392<q[1]<-.33:poly.material_index=2
for side in ['L','R']:
    ob=next(o for o in bpy.data.objects if o.type=='MESH' and (o.name=='Jill_Lids.'+side or o.data.name.startswith('Jill_CurvedLids.'+side)));ob.data.materials.clear();ob.data.materials.append(skin)
s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=720;s.render.resolution_y=720;s.render.resolution_percentage=100
s.world=bpy.data.worlds.new('Roundtrip_ReviewWorld');s.world.color=(.80,.80,.80);s.view_settings.view_transform='Standard'
sh=s.display.shading;sh.light='STUDIO';sh.studiolight_rotate_z=.4;sh.color_type='MATERIAL';sh.show_shadows=True;sh.show_cavity=True;sh.cavity_type='BOTH';sh.background_type='WORLD'
cam=bpy.data.objects.new('Roundtrip_ReviewCamera',bpy.data.cameras.new('Roundtrip_ReviewCamera'));s.collection.objects.link(cam);s.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=1.18
for label,frame in ([] if '--no-render' in sys.argv else [('neutral',1),('blink',next(c['peak'] for c in schedule if c['name']=='blink')),('combined-left',next(c['peak'] for c in schedule if c['name']=='combined-left'))]):
    s.frame_set(frame);bpy.context.view_layer.update()
    for view,d in {'front':(0,-1,0),'side':(1,0,0),'3q':(1,-2,.15)}.items():
        target=Vector((0,0,.5));cam.location=target+Vector(d).normalized()*5;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
        s.render.image_settings.file_format='PNG';s.render.filepath=str(E/'renders'/f'glb-{label}-{view}.png');bpy.ops.render.render(write_still=True)
tol=1e-5
ok=all(r['import_to_blend']['max']<tol and r['blend_to_import']['max']<tol and not r['missing_anchors'] and r['anchor_max_delta']<tol and all(x['max']<tol for x in r['lids'].values()) for r in roundtrip)
ok=ok and all(r['saved_proof_max_delta']<tol for r in blend_rows) and all(r['direct_control_vs_saved_peak_max_delta']<tol for r in replay) and blend_return<tol
write('roundtrip-validation.json',{'tolerance':tol,'bounded_roundtrip_pass':bool(ok),'blender_reopen':blend_rows,'direct_control_replay':replay,
 'direct_reset_delta':blend_return,'independence':independence,'glb_structure':portable,'glb_reimport':roundtrip,'human_visual':'PENDING / see Evidence.md, numeric agreement is not visual approval'})
print('ROUNDTRIP_COMPLETE',json.dumps({'bounded_pass':ok,'body_max':max(r['import_to_blend']['max'] for r in roundtrip),'anchor_max':max(r['anchor_max_delta'] or 0 for r in roundtrip)}))
if not ok:sys.exit(2)
