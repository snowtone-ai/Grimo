"""Continue v003 with the Human's approved left-profile nose as the target.

Only the compact nose/philtrum area is edited. A smooth nose cap and short
philtrum share the existing head's keys, animation and composition controls.
The original head topology and ordinary relative deformations survive.
"""
import sys
sys.dont_write_bytecode=True
import bpy,math,json,hashlib,importlib.util,subprocess,shutil
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('previous_muzzle',Path(__file__).with_name('refine-shushu-v003-muzzle.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
a,r,v=m.a,m.r,m.v
BASE='530f75c4cc7e4fbc06545c420b337155e67c8212'
OUT=v.OUT/'nose-reference-revision'
BACK=ROOT/'.git/shushu-v003-reference-nose-530f75c'
REFERENCE=ROOT/'assets/grimo/source/shushu/tripo-generation-pose/shushu_bodyonly_left.png'
HUMAN_SCREENSHOT=Path('C:/Users/chidj/OneDrive/画像/Screenshots/スクリーンショット (525).png')
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(name,value):
 OUT.mkdir(parents=True,exist_ok=True);(OUT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def snapshot():
 BACK.mkdir(parents=True,exist_ok=True)
 if (BACK/'inputs.json').exists():return
 paths=[v.ASSET,v.PROOF,v.STATIC.with_suffix('.fbx'),v.STATIC.with_suffix('.glb')]
 protected=json.loads((v.OUT/'muzzle-revision/protected-inputs.json').read_text(encoding='utf-8'))
 for p in paths:
  rel=p.relative_to(ROOT).as_posix();data=subprocess.run(['git','show',BASE+':'+rel],cwd=ROOT,capture_output=True,check=True).stdout
  if data.startswith(b'version https://git-lfs.github.com/spec/v1'):
   data=subprocess.run(['git','lfs','smudge'],input=data,cwd=ROOT,capture_output=True,check=True).stdout
  dest=BACK/p.name;dest.write_bytes(data);assert sha(dest)==sha(p)
  protected[rel]=sha(p)
 (BACK/'inputs.json').write_text(json.dumps(protected,indent=2)+'\n')
 write('authority.json',{'base':BASE,'latest_human_request':'鼻はこんなふうになる。これにぴったりにして。',
  'screenshot_path':str(HUMAN_SCREENSHOT),'screenshot_sha256':sha(HUMAN_SCREENSHOT),
  'approved_left_profile':REFERENCE.relative_to(ROOT).as_posix(),'reference_sha256':sha(REFERENCE),
  'approved_front_profile':'assets/grimo/source/shushu/tripo-generation-pose/shushu_bodyonly_front.png',
  'unapproved_27_used':False,'Human':'PENDING','Tripo':'HOLD'})
def displacement(p):
 x,y,z=p
 w=(1-v.smooth(.027,.046,abs(x)))*v.smooth(.602,.612,z)*(1-v.smooth(.635,.650,z))*v.smooth(-.235,-.258,y)
 if w<=0:return 0.
 # Remove the inherited irregular relief beneath the new embedded cap.
 bed=-.268+.10*(z-.620)+7*x*x
 return (bed-y)*w
def barycentric(p,a,b,c):
 u=b-a;w=c-a;q=p-a;uu=u.dot(u);uw=u.dot(w);ww=w.dot(w)
 den=uu*ww-uw*uw;assert abs(den)>1e-20
 s=(ww*q.dot(u)-uw*q.dot(w))/den;t=(uu*q.dot(w)-uw*q.dot(u))/den
 return (1-s-t,s,t)
def nose_cap(head):
 keys=head.data.shape_keys.key_blocks;basis=[p.co.copy() for p in keys['Basis'].data];tris=[]
 for face in head.data.polygons:
  for j in range(1,len(face.vertices)-1):tris.append((face.vertices[0],face.vertices[j],face.vertices[j+1]))
 tree=BVHTree.FromPolygons(basis,tris,all_triangles=True)
 def anchor(x,z):
  point,normal,i,distance=tree.ray_cast(Vector((x,-1,z)),Vector((0,1,0)))
  assert point is not None and point.y<-.24,('Nose anchor must be on the front surface',x,z,list(point) if point is not None else None)
  tri=tris[i];return point,tri,barycentric(point,*(basis[j] for j in tri))
 points=[Vector((0,-.274-.25*.0095,.6455))];faces=[];segments=48;latitudes=16
 for j in range(1,latitudes):
  t=math.pi*j/latitudes;s=math.cos(t)
  for k in range(segments):
   angle=math.tau*k/segments;points.append(Vector((.0175*math.sin(t)*math.cos(angle)*(1+.28*s),-.274-.25*.0095*s+.012*math.sin(t)*math.sin(angle),.636+.0095*s)))
 bottom=len(points);points.append(Vector((0,-.274+.25*.0095,.6265)))
 for k in range(segments):faces.append((0,1+k,1+(k+1)%segments))
 for j in range(latitudes-2):
  lo=1+j*segments;hi=lo+segments
  for k in range(segments):q=(k+1)%segments;faces.append((lo+k,hi+k,hi+q,lo+q))
 last=1+(latitudes-2)*segments
 for k in range(segments):faces.append((bottom,last+(k+1)%segments,last+k))
 cap_count=len(points)
 # The short philtrum is embedded into the head, reaching the actual upper
 # aperture region; its sampled relative keys follow the existing smile/open.
 tube_start=len(points);tube_sides=8;tube_rows=17
 for j in range(tube_rows):
  z=.6272+(.6014-.6272)*j/(tube_rows-1);p,tri,weights=anchor(0,z)
  for k in range(tube_sides):
   angle=math.tau*k/tube_sides;points.append(Vector((.0007*math.cos(angle),p.y-.00065+.0007*math.sin(angle),z)))
 for j in range(tube_rows-1):
  for k in range(tube_sides):
   q=(k+1)%tube_sides;lo=tube_start+j*tube_sides;hi=lo+tube_sides;faces.append((lo+k,hi+k,hi+q,lo+q))
 faces.append(tuple(tube_start+k for k in range(tube_sides)))
 faces.append(tuple(tube_start+(tube_rows-1)*tube_sides+k for k in reversed(range(tube_sides))))
 bindings=[anchor(p.x,p.z)[1:] for p in points]
 mesh=bpy.data.meshes.new('Shushu_ReferenceNoseSurface');mesh.from_pydata(points,[],faces);mesh.update()
 nose=bpy.data.objects.new('Shushu_Nose',mesh);bpy.context.collection.objects.link(nose);nose.matrix_world=head.matrix_world.copy();nose.parent=head.parent
 for polygon in mesh.polygons:polygon.use_smooth=True
 mesh.materials.append(v.clay)
 for key in keys:
  created=nose.shape_key_add(name=key.name);created.slider_min=key.slider_min;created.slider_max=key.slider_max;created.interpolation=key.interpolation
  for i,(tri,weights) in enumerate(bindings):
   delta=sum((weight*(key.data[j].co-basis[j]) for j,weight in zip(tri,weights)),Vector())
   created.data[i].co=points[i]+delta
 for key in keys:nose.data.shape_keys.key_blocks[key.name].relative_key=nose.data.shape_keys.key_blocks[key.relative_key.name]
 old_ad=head.data.shape_keys.animation_data
 if old_ad:
  ad=nose.data.shape_keys.animation_data_create()
  if old_ad.action:ad.action=old_ad.action;ad.action_slot=old_ad.action_slot
  for source in old_ad.drivers:
   f=nose.data.shape_keys.driver_add(source.data_path,source.array_index) if source.array_index else nose.data.shape_keys.driver_add(source.data_path)
   f.driver.type=source.driver.type;f.driver.expression=source.driver.expression
   for variable in source.driver.variables:
    nv=f.driver.variables.new();nv.name=variable.name;nv.type=variable.type
    for old,new in zip(variable.targets,nv.targets):
     new.id_type=old.id_type;new.id=old.id;new.data_path=old.data_path;new.bone_target=old.bone_target;new.transform_type=old.transform_type;new.transform_space=old.transform_space
 r.compose(nose);modifier=nose.modifiers.new('Reference nose smooth surface','SUBSURF');modifier.levels=1;modifier.render_levels=1
 nose['ReferenceNose']='Human left-profile + approved front; compact rounded upper-wide nose and short philtrum'
 nose['CapVertexCount']=cap_count;nose['HeadAnchorTriangles']=json.dumps([tri for tri,w in bindings]);nose['HeadAnchorWeights']=json.dumps([w for tri,w in bindings])
 v.character.append(nose)
 return {'object':nose.name,'source_vertices':len(points),'cap_vertices':cap_count,'philtrum_vertices':len(points)-cap_count,'keys':len(keys),'attachment':'Barycentric relative deformations; existing head pose compositions, action and drivers'}
def refine():
 head=v.parts['Head'];keys=head.data.shape_keys.key_blocks;basis=keys['Basis'];ids=[];max_move=0.
 for i,p in enumerate(basis.data):
  delta=displacement(p.co)
  if abs(delta)<1e-10:continue
  ids.append(i);max_move=max(max_move,abs(delta))
  for k in keys:
   if not k.name.startswith(('Head','Corrective.Compose.')):k.data[i].co.y+=delta
 r.compose(head)
 cap=nose_cap(head)
 return {'changed_head_vertices':len(ids),'total_head_vertices':len(basis.data),'max_depth_move':max_move,
  'scope':{'abs_x_lt':.046,'z_range':[.602,.650],'y_lt':-.235},'xz_changed':False,
  'nose_cap':{'center_z':.636,'half_height':.0095,'half_width':.0175,'upper_width_factor':.28,'center_y':-.274,'depth_radius':.012,'profile_tilt':-.25,'saved_object':cap},
  'preserved':'Original topology, relative facial/seat deltas, mouth aperture; head compositions recomputed'}
def colour():
 if 'Shushu_Nose' not in bpy.data.objects:
  m.diagnostic_colour();return
 a.colour();head=v.parts['Head'];keys=head.data.shape_keys.key_blocks
 attr_names=[getattr(n,'attribute_name',getattr(n,'layer_name','')) for mat in head.data.materials if mat and mat.node_tree for n in mat.node_tree.nodes if n.type in ('ATTRIBUTE','VERTEX_COLOR')]
 attr=next(head.data.color_attributes[name] for name in attr_names if name in head.data.color_attributes)
 for loop in head.data.loops:
  i=loop.vertex_index;p=keys['Basis'].data[i].co;original=head.data.vertices[i].co
  if abs(original.x)<.025 and .620<original.z<.647 and original.y<-.25:attr.data[loop.index].color=(.90,.86,.81,1)
 if 'Shushu_Nose' in bpy.data.objects:
  nose=bpy.data.objects['Shushu_Nose'];mat=bpy.data.materials.get('Reference nose diagnostic burgundy') or bpy.data.materials.new('Reference nose diagnostic burgundy')
  mat.diffuse_color=(.13,.035,.055,1);mat.use_nodes=True;shader=mat.node_tree.nodes.get('Principled BSDF');shader.inputs['Base Color'].default_value=mat.diffuse_color;shader.inputs['Roughness'].default_value=.30
  nose.data.materials.clear();nose.data.materials.append(mat)
def render(name,view,kind='clay',state='neutral'):
 a.pose(state)
 if kind=='colour':colour()
 cam=v.cam;target=Vector((0,-.130,.635) if view=='side' else (0,-.060,.635));direction=Vector(r.VIEWS[view]).normalized()
 cam.location=target+direction*3;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=.36
 sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=16;sc.cycles.use_denoising=True;sc.render.resolution_x=640;sc.render.resolution_y=640;sc.render.resolution_percentage=100
 (OUT/'renders').mkdir(parents=True,exist_ok=True);sc.render.filepath=str(OUT/'renders'/f'{name}-{view}.png')
 if not ('--reuse-before-clay' in sys.argv and name=='before-neutral-clay' and Path(sc.render.filepath).exists()):bpy.ops.render.render(write_still=True)
 return {'direction':list(r.VIEWS[view]),'target':list(target),'ortho_scale':.36,'resolution':[640,640],'engine':'CYCLES','samples':16,'kind':kind,'state':state}
def preview():
 a.load(BACK/v.ASSET.name);info=refine();write('candidate-local-edit.json',info)
 tasks=[('side','colour','smile'),('3q','colour','smile')] if '--preview-side' in sys.argv else [('front','colour','smile'),('side','colour','smile'),('3q','colour','smile'),('side','clay','neutral')]
 for view,kind,state in tasks:
  a.load(BACK/v.ASSET.name);refine();render('candidate-'+state+'-'+kind,view,kind,state)
 print('REFERENCE_NOSE_PREVIEW_COMPLETE',flush=True)
def apply():
 inputs=json.loads((BACK/'inputs.json').read_text());previous=json.loads((OUT/'continuity.json').read_text()) if (OUT/'continuity.json').exists() else {}
 for p in [v.ASSET,v.PROOF]:
  rel=p.relative_to(ROOT).as_posix();allowed={inputs[rel],previous.get('saved',{}).get(rel,{}).get('after')}
  assert sha(p) in allowed,('Concurrent saved asset change; refuse overwrite',rel)
 saved={}
 for p in [v.ASSET,v.PROOF]:
  a.load(BACK/p.name);info=refine();bpy.context.scene['NoseReferenceRevision']='Human-specified approved left profile: rounded cap / continuous short philtrum; Human PENDING; Tripo HOLD'
  bpy.ops.wm.save_as_mainfile(filepath=str(p));saved[p.relative_to(ROOT).as_posix()]={'before':inputs[p.relative_to(ROOT).as_posix()],'after':sha(p),'local_edit':info}
 write('continuity.json',{'base':BASE,'Human':'PENDING','Tripo':'HOLD','saved':saved})
 a.load(v.ASSET);v.character=[o for o in v.character if not o.hide_render];v.export_static();shutil.copy2(v.OUT/'static-roundtrip.json',OUT/'static-roundtrip.json')
 print('REFERENCE_NOSE_SAVED_COMPLETE',flush=True)
def final_renders():
 cameras={}
 tasks=[('neutral','clay',q) for q in r.VIEWS]+[('smile','colour',q) for q in r.VIEWS]+[('small','colour','3q'),('full','colour','3q')]
 for version in ['before','after']:
  for state,kind,view in tasks:
   a.load((BACK/v.ASSET.name) if version=='before' else v.ASSET)
   name=f'{version}-{state}-{kind}';cameras[name+'-'+view]=render(name,view,kind,state)
 write('cameras.json',cameras);print('REFERENCE_NOSE_RENDERS_COMPLETE',flush=True)
if __name__=='__main__':
 snapshot()
 if '--preview' in sys.argv or '--preview-side' in sys.argv:preview()
 elif '--apply' in sys.argv:apply()
 elif '--render' in sys.argv:final_renders()
 else:raise RuntimeError('Choose --preview / --apply / --render')
