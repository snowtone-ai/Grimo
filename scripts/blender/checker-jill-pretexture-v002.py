"""Diagnostic checker views only; generated checker never enters production asset."""
import bpy,json,math,sys
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];A=ROOT/'assets/grimo/production/jill/tripo/rig-pretexture-v002';E=ROOT/'docs/production/jill/rig-pretexture-v002'
bpy.ops.wm.open_mainfile(filepath=str(A/'jill-rig-pretexture-v002.blend'))
s=bpy.context.scene;r=bpy.data.objects['JILL_RIG'];b=bpy.data.objects['Jill_Body'];r.animation_data.action=None
channels=list(json.loads((E/'control-contract.json').read_text())['authoring_properties'])
image=bpy.data.images.new('DIAGNOSTIC_UV_GRID_ONLY',1024,1024);image.generated_type='COLOR_GRID';image.filepath_raw=str(E/'uv-checker.png');image.file_format='PNG';image.save()
for m in b.data.materials:
 n=m.node_tree.nodes.new('ShaderNodeTexImage');n.image=image;m.node_tree.links.new(n.outputs['Color'],m.node_tree.nodes.get('Principled BSDF').inputs['Base Color']);m.node_tree.nodes.active=n
s.render.engine='BLENDER_WORKBENCH';s.display.shading.color_type='TEXTURE';s.display.shading.show_cavity=False;s.display.shading.show_shadows=True
s.render.resolution_x=640;s.render.resolution_y=640;s.render.resolution_percentage=100
views={'front':(0,-1,0),'side':(1,0,0),'leftside':(-1,0,0),'3q':(1,-2,.12),'back':(0,1,0),'back3q':(1,2,.1),'top':(0,0,1),'bottom':(0,0,-1)}
states=[('neutral',{},list(views)),('closed',{'mouth_close':1},['front','3q']),('blink',{'blink.L':1,'blink.R':1},['front','3q']),('large-mouth',{'mouth_open':1},['front','side','leftside']),('wing-open',{'wing_open.L':1,'wing_open.R':1},['front','back3q']),('fold',{'wing_open.L':-1,'wing_open.R':-1},['side','back3q']),('paw-palms',{'paw_offer.L':1,'paw_offer.R':1},['3q','bottom'])]
for name,values,vs in states:
 for k in channels:r[k]=float(values.get(k,0))
 r.update_tag();bpy.context.view_layer.update()
 for view in vs:
  target=Vector((0,-.24,.66) if name in ['closed','blink','large-mouth'] else (0,0,.50));cam=s.camera;cam.location=target+Vector(views[view]).normalized()*5;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=.44 if name in ['closed','blink','large-mouth'] else 1.16
  if '--coverage-only' in sys.argv and (E/'renders'/f'uv-{name}-{view}.png').exists():continue
  s.render.image_settings.file_format='PNG';s.render.filepath=str(E/'renders'/f'uv-{name}-{view}.png');bpy.ops.render.render(write_still=True)
print('UV_CHECKER_DONE')
