"""Focused mouth-profile renders, reusing existing v003 reference images."""
import bpy,json,sys
from pathlib import Path
import numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];E=ROOT/'docs/production/jill/mouth-profile-v004';R=E/'renders';R.mkdir(exist_ok=True)
if '--saved-returns' in sys.argv:
    source=(ROOT/'scripts/blender/review-jill-texture-v003.py').read_text(encoding='utf8').replace('rig-pretexture-technical-v003','mouth-profile-v004')
    exec(compile(source,str(ROOT/'scripts/blender/review-jill-texture-v003.py'),'exec'),globals())
    sys.exit(0)
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'assets/grimo/production/jill/tripo/mouth-profile-v004/jill-rig-mouth-profile-v004.blend'))
o=bpy.data.objects['Jill_Body'];r=bpy.data.objects['JILL_RIG'];s=bpy.context.scene
channels=json.loads((ROOT/'docs/production/jill/rig-pretexture-v002/control-contract.json').read_text())['authoring_properties']
r.animation_data.action=None
states=[('neutral',{}),('close-mid',{'mouth_close':.5}),('closed',{'mouth_close':1}),('open',{'mouth_open':1}),('blink-mid',{'blink.L':.5,'blink.R':.5}),('blink',{'blink.L':1,'blink.R':1}),('recovery',{})]
views={'front':(0,-1,0),'side':(1,0,0),'3q':(1,-2,.12)}
neutral=None;rows=[]
for name,values in states:
    for k in channels:r[k]=float(values.get(k,0))
    r.update_tag();bpy.context.view_layer.update()
    ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh();xyz=np.array([v.co[:] for v in mesh.vertices]);ev.to_mesh_clear()
    if name=='neutral':neutral=xyz
    if name=='recovery':rows.append({'recovery_evaluated_max_m':float(np.linalg.norm(xyz-neutral,axis=1).max())})
    for view,direction in views.items():
        target=Vector((0,-.24,.68));cam=s.camera;cam.location=target+Vector(direction).normalized()*5;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=.44
        s.render.engine='BLENDER_WORKBENCH';s.display.shading.color_type='MATERIAL';s.display.shading.show_cavity=False;s.display.shading.show_shadows=True
        s.render.resolution_x=480;s.render.resolution_y=480;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.filepath=str(R/f'v004-{name}-{view}.png');bpy.ops.render.render(write_still=True)
    print('RENDERED',name,flush=True)
(E/'recovery-proof.json').write_text(json.dumps(rows,indent=2)+'\n')
