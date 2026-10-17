"""Canonical two-blossom head item and hind-sole-only UV pads. Source is read-only.

--blockout renders the four cheap projections first. Final output has closed,
curved petals, underside calyces, attached leaf blades and short petioles.
"""
import bpy,sys,math,json,hashlib,importlib.util
from pathlib import Path
import numpy as np
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[2]
D=R/'docs/production/shushu/evidence/standard-appearance-v001'
A=R/'assets/grimo/production/shushu/equipment/standard-v001'
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
root=bpy.data.objects.new('Shushu_HeadFlower_v001',None);scene.collection.objects.link(root)
root.location=(.08,-.105,.916);bpy.context.view_layer.update()
def linear(c):return c/12.92 if c<=.04045 else ((c+.055)/1.055)**2.4
def material(name,color,vcol=False):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=tuple(linear(x) for x in color)+(1,);p.inputs['Roughness'].default_value=.86;p.inputs['Specular IOR Level'].default_value=.18
 if vcol:
  n=m.node_tree.nodes.new('ShaderNodeVertexColor');n.layer_name='CanonicalColor';m.node_tree.links.new(n.outputs['Color'],p.inputs['Base Color'])
 return m
petalmat=material('Shushu_Sakura_Matte',(1,.75,.8),True)
leafmat=material('Shushu_Leaf_Matte',(.58,.72,.24),True)
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
 b=basis(normal);segments=16 if block else 48;rings=3 if block else 9
 # Small central overlap remains only 0.34 of either principal blossom diameter.
 count=3 if small else 5
 for petal in range(count):
  a=angle+petal*2*math.pi/(5 if small else count);ca,sa=math.cos(a),math.sin(a)
  verts=[];faces=[];colors=[]
  # Each petal is a cupped disk with its own rim and a shallow terminal notch.
  for k in range(rings+1):
   t=k/rings
   for j in range(segments):
    theta=j*2*math.pi/segments;wrapped=min(theta,2*math.pi-theta)
    bx=.49*r*math.sin(theta);by=.5*r*(1+math.cos(theta))-.105*r*math.exp(-(wrapped/.22)**2)
    x=bx*t;y=.45*r+(by-.45*r)*t
    z=r*(.035+.32*(y/r)**2+.12*(x/(.49*r))**2+.025*math.sin(3*theta)*(y/r))+petal*.00035
    verts.append(point(c,b,x*ca-y*sa,x*sa+y*ca,z))
    edge=max(0,(t-.78)/.22);tip=max(0,y/r-.68)
    cream=np.array([1,.80,.83]);pink=np.array([.95,.32,.51]);mix=min(.96,.16+.80*edge+.1*tip)
    colors.append(tuple(cream*(1-mix)+pink*mix))
  for k in range(rings):
   for j in range(segments):
    p=k*segments+j;q=k*segments+(j+1)%segments
    faces.append((p,q,q+segments,p+segments))
  mesh(f'{name}_Petal_{petal+1:02}',verts,faces,petalmat,colors,.0015 if not small else .0008)
 # Restrained pollen centre, no long radiating decorative stamens.
 def ball(label,pos,scale,mat):
  bpy.ops.mesh.primitive_uv_sphere_add(segments=12 if block else 20,ring_count=6 if block else 10,location=pos)
  o=bpy.context.object;o.name=label;o.scale=scale;o.data.materials.append(mat)
  for p in o.data.polygons:p.use_smooth=True
  o.parent=root;o.matrix_parent_inverse=root.matrix_world.inverted();pieces.append(o);return o
 center=point(c,b,0,0,.006)
 o=ball(name+'_Pollen',center,(r*.21,r*.21,r*.07),yellow);o.rotation_euler=b[2].to_track_quat('Z','Y').to_euler()
 if not small and not block:
  for j in range(9):
   a=j*math.tau/9;ball(name+f'_Anther_{j:02}',point(c,b,r*.17*math.cos(a),r*.17*math.sin(a),.010),(r*.025,)*3,yellow)
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
  for j in range(20):
   a=j*math.tau/20;verts.append(top+b[0]*math.cos(a)*r*.20+b[1]*math.sin(a)*r*.20)
  verts.append(top)
  for j in range(20):faces.extend([(0,1+(j+1)%20,1+j),(21,1+j,1+(j+1)%20)])
  mesh(name+'_Receptacle',verts,faces,stemmat)
  curve=bpy.data.curves.new(name+'_Pedicel','CURVE');curve.dimensions='3D';curve.bevel_depth=.0023;curve.bevel_resolution=2
  sp=curve.splines.new('BEZIER');sp.bezier_points.add(2)
  for p,co in zip(sp.bezier_points,[point(c,b,0,0,-.008),point(c,b,0,-.012,-.025),Vector((.080,-.095,.918))]):p.co=co;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
  o=bpy.data.objects.new(name+'_Pedicel',curve);scene.collection.objects.link(o);curve.materials.append(stemmat);o.parent=root;o.matrix_parent_inverse=root.matrix_world.inverted();pieces.append(o)
 return b
def leaf(name,start,tip,width):
 s=Vector(start);t=Vector(tip);axis=t-s;n=Vector((0,-.85,.53));cross=axis.normalized().cross(n).normalized();verts=[];colors=[];faces=[]
 steps=6 if block else 18
 for i in range(steps+1):
  f=i/steps;w=width*math.sin(math.pi*f)**.8
  for j in [-1,0,1]:
   p=s+axis*f+cross*w*j+n*(.005*math.sin(math.pi*f)*(1-abs(j))+.004*f*f)
   verts.append(p);colors.append((.48+.15*(1-abs(j)),.64+.11*(1-abs(j)),.20+.08*(1-abs(j))))
 for i in range(steps):
  for j in range(2):faces.append((i*3+j,i*3+j+1,(i+1)*3+j+1,(i+1)*3+j))
 mesh(name,verts,faces,leafmat,colors,.0012)
 # Petiole reaches the shared backing rather than ending in space.
 curve=bpy.data.curves.new(name+'_Petiole','CURVE');curve.dimensions='3D';curve.bevel_depth=.0012;curve.bevel_resolution=1
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
 bpy.ops.export_scene.gltf(filepath=str(A/'shushu-head-flower-v001.glb'),export_format='GLB',use_selection=True,export_animations=False,export_extras=True,export_apply=True)
 itemscene=bpy.data.scenes.new('Shushu_HeadFlower_v001')
 for o in [root]+pieces:itemscene.collection.objects.link(o)
 bpy.data.libraries.write(str(A/'shushu-head-flower-v001.blend'),{itemscene},fake_user=True,compress=True);bpy.data.scenes.remove(itemscene)
 # UV paint lives on the exact existing sole surface. No new pad geometry,
 # weights or morphs, and no projected paint on forepaws or the foot upper.
 torso=bpy.data.objects['ShushuStatic_Torso'];mat=torso.data.materials[0].copy();torso.data.materials[0]=mat
 node=next(n for n in mat.node_tree.nodes if n.type=='TEX_IMAGE');original=node.image;image=original.copy();image.name='Shushu_HindSolePads_v001';node.image=image
 w,h=image.size;pixels=np.empty(w*h*4,dtype=np.float32);image.pixels.foreach_get(pixels);pixels=pixels.reshape(h,w,4);before=pixels.copy();mask=np.zeros((h,w),dtype=bool)
 me=torso.data;me.calc_loop_triangles();points=np.array([torso.matrix_world@v.co for v in me.vertices]);uv=me.uv_layers.active
 scene.frame_set(103);ev=torso.evaluated_get(bpy.context.evaluated_depsgraph_get());em=ev.to_mesh();seatpoints=np.array([ev.matrix_world@v.co for v in em.vertices]);ev.to_mesh_clear();scene.frame_set(1)
 for tri in me.loop_triangles:
  p=points[list(tri.vertices)]
  if p[:,2].min()>.045 or abs(p[:,0].mean())<.05:continue
  if np.cross(p[1]-p[0],p[2]-p[0])[2]>=0:continue
  tex=np.array([uv.data[i].uv[:] for i in tri.loops])*[w,h]-.5
  lo=np.maximum(0,np.floor(tex.min(0)).astype(int));hi=np.minimum([w-1,h-1],np.ceil(tex.max(0)).astype(int))
  if np.any(hi<lo):continue
  xx,yy=np.meshgrid(np.arange(lo[0],hi[0]+1),np.arange(lo[1],hi[1]+1));q=np.stack([xx,yy],-1)
  matrix=np.column_stack([tex[1]-tex[0],tex[2]-tex[0]])
  if abs(np.linalg.det(matrix))<1e-9:continue
  bc=(q-tex[0])@np.linalg.inv(matrix).T;inside=(bc[...,0]>=-1e-5)&(bc[...,1]>=-1e-5)&(bc.sum(-1)<=1.00001)
  xyz=p[0]+bc[...,0,None]*(p[1]-p[0])+bc[...,1,None]*(p[2]-p[0])
  # Canonical sole exposure is seated. Define the smooth ovals on that actual
  # evaluated surface, then pull them back through the unchanged original UV.
  # Painting rest-space circles alone produced polygonal seated pads: rejected.
  posed=seatpoints[list(tri.vertices)];surface=posed[0]+bc[...,0,None]*(posed[1]-posed[0])+bc[...,1,None]*(posed[2]-posed[0])
  side=1 if p[:,0].mean()>0 else -1;cx=.167*side;dx=surface[...,0]-cx;y=surface[...,2]
  shapes=[(0,.070,.043,.049),(-.038,.148,.014,.018),(0,.169,.015,.021),(.038,.148,.014,.018)]
  distance=np.full(xx.shape,100.)
  for sx,sy,rx,ry in shapes:distance=np.minimum(distance,np.sqrt(((dx-sx)/rx)**2+((y-sy)/ry)**2))
  valid=inside&(xyz[...,2]<.045)&(distance<1.025)
  alpha=np.clip((1.025-distance)/.05,0,1)*valid
  region=pixels[lo[1]:hi[1]+1,lo[0]:hi[0]+1];color=np.zeros_like(region[...,:3]);color[:]=[1,.73,.77]
  region[...,:3]=region[...,:3]*(1-alpha[...,None])+color*alpha[...,None];mask[lo[1]:hi[1]+1,lo[0]:hi[0]+1]|=alpha>0
 image.pixels.foreach_set(pixels.ravel());image.filepath_raw=str(A/'shushu-hind-sole-pads-v001.png');image.file_format='PNG';image.save()
 # Image.copy() retains the original packed-file bytes. Reload the written PNG
 # before packing, otherwise author reload silently restores the unpainted sole.
 painted=bpy.data.images.load(str(A/'shushu-hind-sole-pads-v001.png'),check_existing=False);painted.name='Shushu_HindSolePads_Packed_v001';painted.pack();node.image=painted
 if image.users==0:bpy.data.images.remove(image)
 (D/'pad-texture-audit.json').write_text(json.dumps({'method':'sole-only UV raster on existing Torso; original UV/geometry/skin/morph untouched','changedTexels':int(mask.sum()),'outsideMaskDifference':float(np.max(np.abs(pixels[~mask]-before[~mask]))),'size':[w,h],'centralPlusUpperSmallPadsPerHindFoot':[1,3],'forepawAddition':False},indent=2))
 # Save separately, with a real Head-bone parent preserving the authored world pose.
 rig=bpy.data.objects['Shushu_ProductionRig_v004'];world=root.matrix_world.copy();root.parent=rig;root.parent_type='BONE';root.parent_bone='mixamorig:Head';bpy.context.view_layer.update();root.matrix_world=world;bpy.context.view_layer.update()
 bpy.ops.wm.save_as_mainfile(filepath=str(A/'shushu-standard-appearance-v001-proof.blend'),compress=True)
 after=geometry_signature();assert protected==after,'Approved body geometry changed';assert hashlib.sha256(source.read_bytes()).hexdigest()==source_hash
 (D/'preservation.json').write_text(json.dumps({'sourceSha256':source_hash,'geometryUVShapeWeightsBefore':protected,'geometryUVShapeWeightsAfter':after,'all14MeshesExact':protected==after,'sourceFileUnchanged':True,'authorizedMaterialChange':'Torso cloned material, separate sole-only PNG; all other original materials retained'},indent=2))
sp=importlib.util.spec_from_file_location('gate',R/'scripts/blender/shushu-v004-motion-gate.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
for o in list(bpy.data.objects):
 if o.type in {'LIGHT','CAMERA'} or o.name.startswith('DiagnosticGround'):bpy.data.objects.remove(o,do_unlink=True)
scene,cam=g.r.b.setup_review(640,8);scene.render.engine='BLENDER_EEVEE';cam.data.type='ORTHO';cam.data.ortho_scale=1.22
folder=D/('blockout' if block else 'author');folder.mkdir(exist_ok=True);ledger=[]
for f in ([1] if block else [1,103,189,197,205,221,229,405,413,589,1089,1113,1149]):
 scene.frame_set(f)
 for view,xyz in {'front':(0,-3,.52),'side':(-3,0,.52),'3q':(-2,-2.5,.65),'3qR':(2,-2.5,.65)}.items():
  if not block and f not in [1,103,1089,1113,1149] and view not in ['front','3qR']:continue
  cam.location=xyz;cam.rotation_euler=(Vector((0,0,.52))-cam.location).to_track_quat('-Z','Y').to_euler();path=folder/f'f{f}-{view}.png';scene.render.filepath=str(path);bpy.ops.render.render(write_still=True);ledger.append({'file':path.relative_to(R).as_posix(),'frame':f,'view':view})
(D/('blockout-ledger.json' if block else 'author-ledger.json')).write_text(json.dumps(ledger,indent=2))
print('SHUSHU_EQUIPMENT_COMPLETE', 'blockout' if block else 'final',flush=True)
