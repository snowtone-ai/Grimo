"""Temporary material separation on unchanged v001 geometry. No asset save."""
import bpy,sys,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[7];OLD=ROOT/'assets/grimo/production/jill/tripo/smartmesh25k-v001'
sys.path.insert(0,str(OLD/'scripts'))
import audit_common as a
E=ROOT/'docs/production/jill/evidence/smartmesh25k-v002';a.EVIDENCE=E
def jpeg_render(scene,name,direction,target=(0,0,0),scale=3):
    a.setup_camera(scene,direction,target,scale)
    scene.render.image_settings.file_format='JPEG';scene.render.image_settings.quality=96
    scene.render.filepath=str(E/'renders'/f'{name}.jpg');bpy.ops.render.render(write_still=True)
a.render=jpeg_render
o=bpy.data.objects['JILL_GEOMETRY_MASTER'];m=o.data;s=bpy.context.scene;s.frame_set(1)
xyz=np.array([tuple(o.matrix_world@v.co) for v in m.vertices]);parts=a.components(m)
def mat(name,col):
    x=bpy.data.materials.new('TEMP_DIAGNOSTIC_'+name);x.diffuse_color=(*col,1);m.materials.append(x);return len(m.materials)-1
skin=mat('skin',(.58,.68,.55));eye=mat('eye',(.025,.06,.025));mouth=mat('mouth',(.20,.025,.035));tongue=mat('tongue',(.8,.25,.28))
for p in m.polygons:p.material_index=skin
for c in [98,99]:
    for i in parts[c]['f']:m.polygons[i].material_index=eye
sel=[]
for p in m.polygons:
    q=xyz[list(p.vertices)].mean(0)
    if (q[0]/.044)**2+((q[2]-.605)/.037)**2<.85 and -.392<q[1]<-.33:
        p.material_index=mouth if q[2]>.588 else tongue;sel.append([p.index,*q])
s.display.shading.color_type='MATERIAL'
for name,d in [('front',(0,-1,0)),('left',(1,0,0)),('right',(-1,0,0)),('3q',(1,-2,.15))]:a.render(s,'face-material-v001-'+name,d,(0,-.20,.72),.60)
(E/'face-diagnostic-selection.json').write_text(json.dumps({'eye_components':[98,99],'mouth_polygons':sel,'temporary_only':True},indent=2),encoding='utf8')
