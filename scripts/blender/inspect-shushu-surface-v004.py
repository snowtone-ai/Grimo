import bpy,sys,importlib.util,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[2];D=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v004'
sp=importlib.util.spec_from_file_location('repair',R/'scripts/blender/repair-shushu-abc-v004.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
bpy.ops.wm.open_mainfile(filepath=str(m.ASSET));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');scene,cam=m.b.setup_review(640,8);scene.render.engine='BLENDER_EEVEE';cam.data.type='ORTHO';cam.data.ortho_scale=1.18
mat=bpy.data.materials.new('Geometry diagnostic only');mat.diffuse_color=(.5,.5,.5,1);mat.use_nodes=True;mat.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.5,.5,.5,1);mat.node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.65
for o in bpy.data.objects:
 if o.type=='MESH' and o.name.startswith('ShushuStatic_'):
  for i in range(len(o.data.materials)):o.data.materials[i]=mat
for label,state in [('neutral',{}),('seat',{'Seat':1,'Hold.L':1,'Hold.R':1}),('mid',{'Seat':.35})]:
 m.b.state(rig,state)
 for view,loc in {'3q':(-2,-2.5,.65),'back':(0,3,.5)}.items():
  cam.location=loc;cam.rotation_euler=(Vector((0,0,.5))-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(D/f'geometry-{label}-{view}.png');bpy.ops.render.render(write_still=True)
print('CLAY_DIAGNOSTIC_COMPLETE',flush=True)
