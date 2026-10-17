"""Reimport both real GLBs and the same pad PNG; fixed-camera roundtrip evidence."""
import bpy,sys,json,importlib.util,hashlib
from pathlib import Path
from mathutils import Vector
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[2];D=R/'docs/production/shushu/evidence/standard-appearance-v001';A=R/'assets/grimo/production/shushu/equipment/standard-v001'
sp=importlib.util.spec_from_file_location('gate',R/'scripts/blender/shushu-v004-motion-gate.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
author='--author' in sys.argv
if author:
 bpy.ops.wm.open_mainfile(filepath=str(A/'shushu-standard-appearance-v001-proof.blend'))
 image=next(n.image for n in bpy.data.objects['ShushuStatic_Torso'].data.materials[0].node_tree.nodes if n.type=='TEX_IMAGE')
 assert image.packed_file,'Author sole texture must be packed'
 packed=hashlib.sha256(bytes(image.packed_file.data)).hexdigest();png=hashlib.sha256((A/'shushu-hind-sole-pads-v001.png').read_bytes()).hexdigest()
 assert packed==png,'Packed author image differs from actual shipped sole PNG'
 (D/'author-texture-pack.json').write_text(json.dumps({'packedSha256':packed,'shippedPngSha256':png,'exact':True},indent=2))
 if '--validate-only' in sys.argv:sys.exit(0)
else:
 g.GLB=R/'assets/grimo/production/shushu/tripo/geometry-v003/rigging/shushu-v004-motion-gate-v004.glb';g.imported();scene=bpy.context.scene;scene.frame_set(1)
 before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(A/'shushu-head-flower-v001.glb'));objects=set(bpy.data.objects)-before
 root=next(o for o in objects if o.name=='Shushu_HeadFlower_v001');rig=next(o for o in before if o.type=='ARMATURE');world=root.matrix_world.copy();root.parent=rig;root.parent_type='BONE';root.parent_bone='mixamorig:Head';bpy.context.view_layer.update();root.matrix_world=world
 torso=bpy.data.objects['ShushuStatic_Torso'];mat=torso.data.materials[0].copy();torso.data.materials[0]=mat;node=next(n for n in mat.node_tree.nodes if n.type=='TEX_IMAGE');node.image=bpy.data.images.load(str(A/'shushu-hind-sole-pads-v001.png'))
# The editable proof retains old review lights/ground; GLB import starts empty.
# Remove that presentation only, then build one identical rig for both routes.
for o in list(bpy.data.objects):
 if o.type in {'LIGHT','CAMERA'} or o.name.startswith('DiagnosticGround'):bpy.data.objects.remove(o,do_unlink=True)
scene,cam=g.r.b.setup_review(640,8);scene.render.engine='BLENDER_EEVEE';cam.data.type='ORTHO';cam.data.ortho_scale=1.22;folder=D/('author' if author else 'saved');folder.mkdir(exist_ok=True);ledger=[]
for f in [1,103,189,197,205,221,229,405,413,589,1089,1113,1149]:
 scene.frame_set(f)
 for view,xyz in {'front':(0,-3,.52),'side':(-3,0,.52),'3q':(-2,-2.5,.65),'3qR':(2,-2.5,.65)}.items():
  if f not in [1,103,1089,1113,1149] and view not in ['front','3qR']:continue
  cam.location=xyz;cam.rotation_euler=(Vector((0,0,.52))-cam.location).to_track_quat('-Z','Y').to_euler();path=folder/f'f{f}-{view}.png';scene.render.filepath=str(path);bpy.ops.render.render(write_still=True);ledger.append({'file':path.relative_to(R).as_posix(),'frame':f,'view':view,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
(D/('author-ledger.json' if author else 'saved-ledger.json')).write_text(json.dumps({'route':'equipped Blender author' if author else 'original saved v004 GLB + separately reimported flower GLB + sole PNG','captureSettings':{'engine':scene.render.engine,'size':[640,640],'orthoScale':1.22,'lights':[{'name':o.name,'energy':o.data.energy,'location':list(o.location)} for o in bpy.data.objects if o.type=='LIGHT'],'groundCount':sum(o.name.startswith('DiagnosticGround') for o in bpy.data.objects),'viewTransform':scene.view_settings.view_transform,'look':scene.view_settings.look,'exposure':scene.view_settings.exposure},'images':ledger},indent=2))
print('EQUIPMENT_ROUNDTRIP_COMPLETE',flush=True)
