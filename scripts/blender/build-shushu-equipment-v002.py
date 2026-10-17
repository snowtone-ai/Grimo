"""Canonical two-blossom head item and hind-sole-only UV pads. Source is read-only.

--blockout renders the four cheap projections first. Final output has rounded petal volumes and satin response. Human-approved sole PNG is reused.
"""
import bpy,sys,math,json,hashlib,importlib.util
from pathlib import Path
import numpy as np
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[2]
D=R/'docs/production/shushu/evidence/standard-appearance-v002'
A=R/'assets/grimo/production/shushu/equipment/standard-v002'
D.mkdir(parents=True,exist_ok=True);A.mkdir(parents=True,exist_ok=True)
block='--blockout' in sys.argv
source=R/'assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v004-motion-gate-v004-proof.blend'
bpy.ops.wm.open_mainfile(filepath=str(source));scene=bpy.context.scene;scene.frame_set(1)
source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
def geometry_signature():
 result={}
 for o in bpy.data.objects:
  if o.type!='MESH' or not o.name.startswith('ShushuStatic_'):continue
  h=hashlib.sha256()
  for k in (o.data.shape_keys.key_blocks if o.data.shape_keys else []):h.update(np.array([v.co[:] for v in k.data],dtype=np.float32).tobytes())
  h.update(np.array([v.co[:] for v in o.data.vertices],dtype=np.float32).tobytes())
  if o.data.uv_layers.active:h.update(np.array([v.uv[:] for v in o.data.uv_layers.active.data],dtype=np.float32).tobytes())
  h.update(str([tuple(p.vertices) for p in o.data.polygons]).encode());h.update(str([[(g.group,g.weight) for g in v.groups] for v in o.data.vertices]).encode());result[o.name]=h.hexdigest()
 return result
protected=geometry_signature()
head=bpy.data.objects['ShushuStatic_Head'];headtree=BVHTree.FromPolygons([head.matrix_world@v.co for v in head.data.vertices],[tuple(p.vertices) for p in head.data.polygons],all_triangles=False)
pieces=[]
root=bpy.data.objects.new('Shushu_HeadFlower_v002',None);scene.collection.objects.link(root)
root.location=(.08,-.105,.916);bpy.context.view_layer.update()
def linear(c):return c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4
def material(name,color,vcol=False):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=tuple(linear(x) for x in color)+(1,);p.inputs['Roughness'].default_value=.86;p.inputs['Specular IOR Level'].default_value=.18
 if vcol:
  n=m.node_tree.nodes.new('ShaderNodeVertexColor');n.layer_name='CanonicalColor';m.node_tree.links.new(n.outputs['Color'],p.inputs['Base Color'])
 return m
petalmat=material('Shushu_Sakura_SoftSatin_v002',(1,.78,.84),True)
p=petalmat.node_tree.nodes.get('Principled BSDF');p.inputs['Roughness'].default_value=.43;p.inputs['Specular IOR Level'].default_value=.5;p.inputs['Coat Weight'].default_value=.12;p.inputs['Coat Roughness'].default_value=.45;p.inputs['Sheen Weight'].default_value=.10;p.inputs['Sheen Roughness'].default_value=.65
leafmat=material('Shushu_Leaf_Soft_v002',(.58,.72,.24),True);leafmat.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.52
yellow=material('Shushu_Pollen_Soft',(.99,.79,.30))
stemmat=material('Shushu_Petioles',(.40,.57,.19))
def mesh(name,verts,faces,mat,colors=None,thickness=0):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);me.materials.append(mat)
 for p in me.polygons:p.use_smooth=True
 if colors:
  attr=me.color_attributes.new(name='CanonicalColor',type='FLOAT_COLOR',domain='POINT')
  for i,c in enumerate(colors):attr.data[i].color=tuple(linear(x) for x in c)+(1,)
 if thickness:
  mod=o.modifiers.new('Closed thin botanical shell','SOLIDIFY');mod.thickness=thickness;mod.offset=-1;mod.use_rim=True
 o.parent=root;o.matrix_parent_inverse=root.matrix_world.inverted();pieces.append(o);return o
def basis(normal):
 n=Vector(normal).normalized();u=Vector((1,0,0));u=(u-n*u.dot(n)).normalized();v=n.cross(u).normalized();return u,v,n
def point(c,b,x,y,z):return Vector(c)+b[0]*x+b[1]*y+b[2]*z
def blossom(name,c,r,normal,angle=0,small=False):
 b=basis(normal);segments=20 if block else 64;rings=4 if block else 14
 # Two actual surfaces share a rounded perimeter. Lens thickness tapers into
 # the notched rim; it is not a flat sheet offset or a uniformly inflated petal.
 count=3 if small else 5
 for petal in range(count):
  a=angle+petal*2*math.pi/(5 if small else count);ca,sa=math.cos(a),math.sin(a);verts=[];faces=[];colors=[]
  def sample(t,theta,side):
   wrapped=min(theta,2*math.pi-theta)
   bx=.49*r*math.sin(theta);by=.5*r*(1+math.cos(theta))-.105*r*math.exp(-(wrapped/.22)**2)
   x=bx*t;y=.45*r+(by-.45*r)*t
   cup=r*(.035+.32*(y/r)**2+.12*(x/(.49*r))**2+.025*math.sin(3*theta)*(y/r)*t*t)+petal*.00055
   # About 0.014H maximum depth, tapering smoothly at the original silhouette.
   lens=r*.17*math.sqrt(max(0,1-t*t))*(.80+.20*math.sin(math.pi*max(0,min(1,y/r))))
   z=cup+lens*(.67 if side>0 else -.33)
   verts.append(point(c,b,x*ca-y*sa,x*sa+y*ca,z))
   edge=max(0,min(1,(t-.45)/.55));mix=.08+.82*edge**1.6
   cream=np.array([1,.79,.85]);pink=np.array([.94,.38,.56])
   if side<0:cream=np.array([.98,.73,.80])
   colors.append(tuple(cream*(1-mix)+pink*mix));return len(verts)-1
  frontCenter=sample(0,0,1);backCenter=sample(0,0,-1);front=[];back=[]
  for k in range(1,rings+1):
   t=k/rings;row=[sample(t,j*math.tau/segments,1) for j in range(segments)];front.append(row)
   back.append(row if k==rings else [sample(t,j*math.tau/segments,-1) for j in range(segments)])
  for j in range(segments):
   n=(j+1)%segments;faces.extend([(frontCenter,front[0][n],front[0][j]),(backCenter,back[0][j],back[0][n])])
  for k in range(rings-1):
   for j in range(segments):
    n=(j+1)%segments;faces.append((front[k][j],front[k][n],front[k+1][n],front[k+1][j]));faces.append((back[k][j],back[k+1][j],back[k+1][n],back[k][n]))
  mesh(f'{name}_Petal_{petal+1:02}',verts,faces,petalmat,colors)
 # Restrained pollen centre, no long radiating decorative stamens.
 def ball(label,pos,scale,mat):
  bpy.ops.mesh.primitive_uv_sphere_add(segments=12 if block else 20,ring_count=6 if block else 10,location=pos)
  o=bpy.context.object;o.name=label;o.scale=scale;o.data.materials.append(mat)
  for p in o.data.polygons:p.use_smooth=True
  o.parent=root;o.matrix_parent_inverse=root.matrix_world.inverted();pieces.append(o);return o
 center=point(c,b,0,0,.012)
 o=ball(name+'_Pollen',center,(r*.21,r*.21,r*.10),yellow);o.rotation_euler=b[2].to_track_quat('Z','Y').to_euler()
 if not small and not block:
  for j in range(9):
   a=j*math.tau/9;ball(name+f'_Anther_{j:02}',point(c,b,r*.17*math.cos(a),r*.17*math.sin(a),.018),(r*.025,)*3,yellow)
 # Five compact sepals and the short rear stalk connect into the hidden mount.
 if not small:
  for j in range(5):
   a=angle+(j+.5)*math.tau/5
   vs=[point(c,b,0,0,-.005),point(c,b,.014*math.cos(a-.3),.014*math.sin(a-.3),-.004),point(c,b,.033*math.cos(a),.033*math.sin(a),-.006),point(c,b,.014*math.cos(a+.3),.014*math.sin(a+.3),-.004)]
   mesh(name+f'_Sepal_{j}',vs,[(0,1,2,3)],stemmat,thickness=.001)
 if not small:
  # A compact receptacle sits on the actual approved head surface. The thin
  # petal shell keeps its curvature; depth comes from the cup, not balloon mass.
  contact,normal,_,gap=headtree.find_nearest(Vector(c)-b[2]*.04)
  bottom=contact+normal*.0004;top=point(c,b,0,0,-.004);verts=[bottom];faces=[]
  for t,width in [(.18,.08),(.50,.20),(.80,.24),(1,.20)]:
   for j in range(24):
    a=j*math.tau/24;verts.append(bottom.lerp(top,t)+b[0]*math.cos(a)*r*width+b[1]*math.sin(a)*r*width)
  verts.append(top)
  for j in range(24):
   n=(j+1)%24;faces.extend([(0,1+n,1+j),(97,73+j,73+n)])
  for k in range(3):
   for j in range(24):
    n=(j+1)%24;faces.append((1+k*24+j,1+k*24+n,1+(k+1)*24+n,1+(k+1)*24+j))
  mesh(name+'_Receptacle',verts,faces,stemmat)
  curve=bpy.data.curves.new(name+'_Pedicel','CURVE');curve.dimensions='3D';curve.bevel_depth=.0023;curve.bevel_resolution=2
  sp=curve.splines.new('BEZIER');sp.bezier_points.add(2)
  for p,co in zip(sp.bezier_points,[point(c,b,0,0,-.008),bottom.lerp(top,.45),bottom]):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
  o=bpy.data.objects.new(name+'_Pedicel',curve);scene.collection.objects.link(o);curve.materials.append(stemmat);o.parent=root;o.matrix_parent_inverse=root.matrix_world.inverted();pieces.append(o)
 return b
def leaf(name,start,tip,width):
 s=Vector(start);t=Vector(tip);axis=t-s;n=Vector((0,-.85,.53)).normalized();cross=axis.normalized().cross(n).normalized();verts=[];colors=[];faces=[]
 steps=8 if block else 20;columns=8
 for side in [1,-1]:
  for i in range(steps+1):
   f=i/steps;w=width*math.sin(math.pi*f)**.8
   for j in range(columns+1):
    u=j/columns*2-1;dome=.0038*math.sin(math.pi*f)*math.sqrt(max(0,1-u*u))
    ridge=.002*math.sin(math.pi*f)*math.exp(-(u/.12)**2)
    p=s+axis*f+cross*w*u+n*(.006*math.sin(math.pi*f)+.004*f*f+dome*(.67 if side>0 else -.33)+ridge)
    verts.append(p);vein=max(0,1-abs(u)/.12)*.025;colors.append((.49+.10*(1-abs(u))-vein,.65+.08*(1-abs(u))-vein,.21+.05*(1-abs(u))))
 stride=columns+1;layer=(steps+1)*stride
 for i in range(steps):
  for j in range(columns):
   a=i*stride+j;faces.append((a,a+1,a+stride+1,a+stride));faces.append((a+layer,a+stride+layer,a+stride+1+layer,a+1+layer))
 # Weld the coincident perimeter to get a continuous, rounded leaf edge.
 o=mesh(name,verts,faces,leafmat,colors);bpy.context.view_layer.objects.active=o;o.select_set(True)
 bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.remove_doubles(threshold=.00001);bpy.ops.mesh.normals_make_consistent(inside=False);bpy.ops.object.mode_set(mode='OBJECT');o.select_set(False)
 curve=bpy.data.curves.new(name+'_Petiole','CURVE');curve.dimensions='3D';curve.bevel_depth=.0012;curve.bevel_resolution=2
 sp=curve.splines.new('POLY');sp.points.add(1)
 for p,co in zip(sp.points,[Vector((.09,-.13,.916)),s]):p.co=(*co,1)
 o=bpy.data.objects.new(name+'_Petiole',curve);scene.collection.objects.link(o);curve.materials.append(stemmat);o.parent=root;o.matrix_parent_inverse=root.matrix_world.inverted();pieces.append(o)
blossom('Sakura_Main_Crown',(.025,-.115,.955),.081,(0,-.82,.57),-.10)
blossom('Sakura_Main_Ear',(.163,-.171,.884),.077,(.22,-.91,.35),.20)
blossom('Sakura_CentralOverlap',(.099,-.163,.924),.026,(.08,-.88,.46),.45,True)
for args in [
 ('Leaf_01_UpperLeft',(-.024,-.090,.945),(-.089,-.087,.975),.021),
 ('Leaf_02_UpperRight',(.091,-.080,.949),(.130,-.055,1.001),.023),
 ('Leaf_03_CentralLower',(.104,-.120,.917),(.078,-.174,.860),.023),
 ('Leaf_04_Right',(.183,-.126,.877),(.245,-.138,.850),.023),
 ('Leaf_05_Lower',(.166,-.125,.864),(.188,-.173,.804),.025)]:leaf(*args)
bpy.context.view_layer.update()
if not block:
 # Curves must become meshes for a portable glTF item. Only new pieces selected.
 bpy.ops.object.select_all(action='DESELECT')
 for o in pieces:o.select_set(True)
 bpy.context.view_layer.objects.active=pieces[0];bpy.ops.object.convert(target='MESH')
 pieces=list(bpy.context.selected_objects)
 # Keep semantic parts editable without paying one draw for every anther.
 groups=[]
 for name in ['Sakura_Main_Crown','Sakura_Main_Ear','Sakura_CentralOverlap']:
  groups.append((name+'_Petals',[o for o in pieces if o.name.startswith(name+'_Petal_')]))
  groups.append((name+'_PollenCentre',[o for o in pieces if o.name.startswith(name+'_Pollen') or o.name.startswith(name+'_Anther_')]))
 groups.append(('Shushu_BotanicalBacking',[o for o in pieces if any(s in o.name for s in ['Sepal','Petiole','Pedicel','Receptacle'])]))
 for name,group in groups:
  if not group:continue
  bpy.ops.object.select_all(action='DESELECT')
  for o in group:o.select_set(True)
  bpy.context.view_layer.objects.active=group[0];bpy.ops.object.join();bpy.context.object.name=name
 pieces=list(root.children)
 bpy.ops.object.select_all(action='DESELECT');root.select_set(True)
 for o in pieces:o.select_set(True)
 bpy.context.view_layer.objects.active=root
 bpy.ops.export_scene.gltf(filepath=str(A/'shushu-head-flower-v002.glb'),export_format='GLB',use_selection=True,export_animations=False,export_extras=True,export_apply=True)
 # A Scene library write crashes Blender 5.2.1 here; write the item objects,
 # then finalize its editable scene in a separate, isolated Blender process.
 bpy.data.libraries.write(str(A/'shushu-head-flower-v002.blend'),set([root]+pieces),fake_user=True,compress=True)
 # Approved hind-sole PNG is reused byte-for-byte, never regenerated here.
 pads=R/'assets/grimo/production/shushu/equipment/standard-v001/shushu-hind-sole-pads-v001.png';pads_hash=hashlib.sha256(pads.read_bytes()).hexdigest()
 assert pads_hash=='f5c4aa2969b9b4971e3926dfede7c56cc8211091b9c074a9c67bb0738a2f21fe'
 torso=bpy.data.objects['ShushuStatic_Torso'];mat=torso.data.materials[0].copy();torso.data.materials[0]=mat
 node=next(n for n in mat.node_tree.nodes if n.type=='TEX_IMAGE');painted=bpy.data.images.load(str(pads),check_existing=False);painted.pack();node.image=painted
 (D/'approved-pads.json').write_text(json.dumps({'human':'PASS: latest Human says 足裏はOK','sha256':pads_hash,'unchanged':True,'source':pads.relative_to(R).as_posix()},ensure_ascii=False,indent=2),encoding='utf-8')
 # Save separately, with a real Head-bone parent preserving the authored world pose.
 rig=bpy.data.objects['Shushu_ProductionRig_v004'];world=root.matrix_world.copy();root.parent=rig;root.parent_type='BONE';root.parent_bone='mixamorig:Head';bpy.context.view_layer.update();root.matrix_world=world;bpy.context.view_layer.update()
 bpy.ops.wm.save_as_mainfile(filepath=str(A/'shushu-standard-appearance-v002-proof.blend'),compress=True)
 after=geometry_signature();assert protected==after,'Approved body geometry changed';assert hashlib.sha256(source.read_bytes()).hexdigest()==source_hash
 (D/'preservation.json').write_text(json.dumps({'sourceSha256':source_hash,'geometryUVShapeWeightsBefore':protected,'geometryUVShapeWeightsAfter':after,'all14MeshesExact':protected==after,'sourceFileUnchanged':True,'authorizedMaterialChange':'Torso cloned material, separate sole-only PNG; all other original materials retained'},indent=2))
sp=importlib.util.spec_from_file_location('gate',R/'scripts/blender/shushu-v004-motion-gate.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
for o in list(bpy.data.objects):
 if o.type in {'LIGHT','CAMERA'} or o.name.startswith('DiagnosticGround'):bpy.data.objects.remove(o,do_unlink=True)
scene,cam=g.r.b.setup_review(640,8);scene.render.engine='BLENDER_EEVEE';cam.data.type='ORTHO';cam.data.ortho_scale=1.22
folder=D/('blockout' if block else 'author');folder.mkdir(exist_ok=True);ledger=[]
for f in [1]:
 scene.frame_set(f)
 for view,xyz in {'front':(0,-3,.52),'side':(-3,0,.52),'3q':(-2,-2.5,.65),'3qR':(2,-2.5,.65)}.items():
  if not block and f not in [1,103,1089,1113,1149] and view not in ['front','3qR']:continue
  cam.location=xyz;cam.rotation_euler=(Vector((0,0,.52))-cam.location).to_track_quat('-Z','Y').to_euler();path=folder/f'f{f}-{view}.png';scene.render.filepath=str(path);bpy.ops.render.render(write_still=True);ledger.append({'file':path.relative_to(R).as_posix(),'frame':f,'view':view})
(D/('blockout-ledger.json' if block else 'author-ledger.json')).write_text(json.dumps(ledger,indent=2))
print('SHUSHU_EQUIPMENT_COMPLETE', 'blockout' if block else 'final',flush=True)
