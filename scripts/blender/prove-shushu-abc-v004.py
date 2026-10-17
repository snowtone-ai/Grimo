"""Export/reload the isolated candidate with existing diagnostic motion only."""
import bpy,sys,importlib.util,json
from pathlib import Path
R=Path(__file__).resolve().parents[2];sys.dont_write_bytecode=True
sp=importlib.util.spec_from_file_location('gate',R/'scripts/blender/shushu-v004-motion-gate.py');g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
g.OUT=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v004';g.ASSET=g.BASE/'shushu-v004-motion-gate-v004.blend';g.PROOF=g.ASSET.with_name(g.ASSET.stem+'-proof.blend');g.GLB=g.ASSET.with_suffix('.glb')
EXTRA={1005:{'Hold.L':1,'Hold.R':1,'MouthOpen':.55},1017:{'Hold.L':1,'Hold.R':1,'MouthOpen':1,'Blink.L':.35},1029:{'Hold.L':1,'SelfContact.R':1,'MouthOpen':.2,'Blink.R':.7,'CheekPressure.R':.6},1041:{'Offer.L':.5,'Offer.R':.5,'MouthOpen':.55},1053:{'Offer.L':1,'Offer.R':1,'Wrist.L':1,'Wrist.R':-1},1065:{'SelfContact.L':.5,'SelfContact.R':.5},1077:{'SelfContact.L':1,'SelfContact.R':1},1089:{'Seat':.5,'Hold.L':.5,'Hold.R':.5,'MouthOpen':.55},1101:{'Seat':1,'Hold.L':1,'Hold.R':1,'MouthOpen':1},1113:{'Seat':1,'Hold.L':1,'SelfContact.R':1,'MouthClose':1,'Blink.R':.7},1125:{'Seat':1,'Hold.L':1,'Hold.R':1,'Tongue':1},1137:{'Seat':.5},1149:{}}
def timeline():
 bpy.ops.wm.open_mainfile(filepath=str(g.PROOF));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');keys=['Seat','Hold.L','Hold.R','SelfContact.L','SelfContact.R','Offer.L','Offer.R','Wrist.L','Wrist.R'];curves={fc.data_path:fc for l in rig.animation_data.action.layers for s in l.strips for bag in s.channelbags for fc in bag.fcurves};frames=[[float(curves['["'+k+'"]'].evaluate(f)) if '["'+k+'"]' in curves else 0 for k in keys] for f in range(1,1150)];(g.OUT/'paw-control-timeline.json').write_text(json.dumps({'keys':keys,'frames':frames,'fps':24,'first_frame':1,'first_time':1/24},separators=(',',':')))
if '--export' in sys.argv:g.proof(EXTRA);timeline()
elif '--verify' in sys.argv:g.verify()
elif '--timeline' in sys.argv:timeline()
