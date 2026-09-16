"""Close the two converted curve ends; same correction is in the generator."""
from pathlib import Path
import bpy,bmesh
root=Path(__file__).resolve().parents[2]
for name in ['Smile_lip','Philtrum']:
    ob=bpy.data.objects[name];bm=bmesh.new();bm.from_mesh(ob.data)
    bmesh.ops.holes_fill(bm,edges=[e for e in bm.edges if e.is_boundary],sides=0)
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free()
    for f in ob.data.polygons:f.use_smooth=True
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(root/'assets/grimo/production/carol/blender/carol-a-v006.blend'))
folder=root/'docs/production/carol/evidence/reconstruction-v006/iterations/pass-05-iteration-09'
scene=bpy.context.scene
for view,label in [('front','FRONT'),('side','SIDE'),('back','BACK'),('top','TOP'),('3q-left','3Q_LEFT'),('3q-right','3Q_RIGHT')]:
    scene.camera=bpy.data.objects['CAM_CAROL_'+label];scene.render.filepath=str(folder/f'{view}-clay.png');bpy.ops.render.render(write_still=True)
# A cap is an occluder, so refresh surface-ID masks with the identical cameras.
scene.display.shading.light='FLAT';scene.display.shading.color_type='OBJECT';scene.display.shading.show_shadows=False;scene.display.shading.show_cavity=False
for view,label in [('front','FRONT'),('side','SIDE'),('back','BACK'),('top','TOP'),('3q-left','3Q_LEFT'),('3q-right','3Q_RIGHT')]:
    scene.camera=bpy.data.objects['CAM_CAROL_'+label];scene.render.filepath=str(folder/f'{view}-face-mask.png');bpy.ops.render.render(write_still=True)
