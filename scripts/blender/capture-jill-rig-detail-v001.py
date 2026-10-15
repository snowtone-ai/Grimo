"""Bounded reverse-side and root-detail captures of the saved proof. No file save."""
import bpy,json
from pathlib import Path
import numpy as np
from mathutils import Vector
R=Path(__file__).resolve().parents[2];E=R/'docs/production/jill/rig-other-v001'
bpy.ops.wm.open_mainfile(filepath=str(R/'assets/grimo/production/jill/tripo/rig-other-v001/jill-rig-other-v001.blend'))
s=bpy.context.scene;body=bpy.data.objects['Jill_Body'];rig=bpy.data.objects['JILL_RIG']
parts=np.load(E/'authority-parts.npz')['component'];base=np.load(E/'rig-bind-data.npz')['basis']
def mat(name,c):
    m=bpy.data.materials.new('CAPTURE_ONLY_'+name);m.diffuse_color=(*c,1);return m
skin=mat('skin',(.59,.69,.53));eye=mat('eye',(.035,.065,.04));mouth=mat('mouth',(.20,.055,.065))
body.data.materials.clear()
for m in [skin,eye,mouth]:body.data.materials.append(m)
for p in body.data.polygons:
    p.material_index=1 if parts[p.vertices[0]] in [98,99] else 0
    q=base[list(p.vertices)].mean(0)
    if (q[0]/.044)**2+((q[2]-.605)/.037)**2<.85 and -.392<q[1]<-.33:p.material_index=2
for side in ['L','R']:bpy.data.objects['Jill_Lids.'+side].data.materials.append(skin)
frames={c['name']:c['peak'] for c in json.loads((E/'proof-schedule.json').read_text())}
cam=s.camera
for name,frame,d,target,scale in [
 ('detail-neutral-back',1,(1,2,.35),(0,.04,.43),.68),
 ('detail-fold-back',frames['both-wings-fold'],(1,2,.35),(0,.04,.43),.68),
 ('detail-offer-shoulder',frames['paw-L-offer'],(1,-.45,.2),(.14,-.16,.52),.4),
 ('detail-combined-back',frames['combined-left'],(1,2,.35),(0,.04,.43),.68),
 ('detail-tail-root',frames['tail-left'],(1,1,.25),(0,.15,.27),.5),
 ('neutral-left-side',1,(-1,0,0),(0,0,.50),1.18),
 ('fold-left-side',frames['both-wings-fold'],(-1,0,0),(0,0,.50),1.18),
 ('combined-right-left-side',frames['combined-right'],(-1,0,0),(0,0,.50),1.18)]:
    s.frame_set(frame);rig.update_tag();bpy.context.view_layer.update()
    t=Vector(target);cam.location=t+Vector(d).normalized()*5;cam.rotation_euler=(t-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale
    s.render.image_settings.file_format='PNG';s.render.filepath=str(E/'renders'/f'{name}.png');bpy.ops.render.render(write_still=True)
print('DETAIL_CAPTURE_COMPLETE')
