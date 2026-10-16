"""Read-only authored control witnesses for the standalone runtime controller."""
import bpy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];D=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v003';B=R/'assets/grimo/production/shushu/tripo/geometry-v003/rigging'
p=B/'shushu-v004-motion-gate-v003-proof.blend';bpy.ops.wm.open_mainfile(filepath=str(p));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE')
keys=['Seat']+[mode+'.'+side for mode in ['Hold','SelfContact','Offer','Wrist'] for side in ['L','R']];rows=[]
for f in [1,477,493,501,*range(505,542,3),549,1041,1053,1065,1089,1095,1101,1113,1149]:
 bpy.context.scene.frame_set(f);bpy.context.view_layer.update();rows.append({'frame':f,'controls':{k:float(rig[k]) for k in keys}})
timeline=[]
for f in range(1,1150):
 bpy.context.scene.frame_set(f);timeline.append([float(rig[k]) for k in keys])
(D/'paw-control-timeline.json').write_text(json.dumps({'keys':keys,'fps':24,'frames':timeline}))
(D/'paw-control-witnesses.json').write_text(json.dumps({'proof_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256((B/'shushu-v004-motion-gate-v003.glb').read_bytes()).hexdigest(),'rows':rows},indent=2));print('CONTROL_WITNESSES',len(rows))
