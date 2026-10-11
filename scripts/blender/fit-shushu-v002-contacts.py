"""Fit reachable tangent self-contact with the actual rigid short paw, no stretching."""
import bpy,sys,importlib,json
from pathlib import Path
from mathutils import Vector
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).parent))
c=importlib.import_module('check-shushu-geometry-v002');b=c.b
c.init(b.ASSET)
bone=b.rig.data.bones['Paw.L'];direction=(bone.tail_local-bone.head_local).normalized()
ids=[v.index for v in b.parts['Paw.L'].data.vertices if (v.co-bone.head_local).dot(direction)>.135]
results={}
for mode,part,zs in [('groom','Head',[.36,.40,.42,.44,.46]),('chest-groom','Torso',[.36,.40,.44,.48])]:
 b.state(mode);target_tree=c.tree(b.parts[part]);best=None;tested=0;best_negative=None
 for x in ([.42,.50,.60,.75] if mode=='groom' else [.26,.30,.34,.38,.42,.46]):
  for y in [-.14,-.18,-.22,-.26,-.30]:
   for z in zs:
    tested+=1;b.paw_pose('L',(x,y,z));v,_=b.evaluated(b.parts['Paw.L']);ds=[];points=[]
    for i in ids:
     p,n,_,d=target_tree.find_nearest(Vector(v[i]));ds.append(d if (Vector(v[i])-p).dot(n)>=0 else -d);points.append(p)
    minimum=min(ds);idx=ds.index(minimum)
    if best_negative is None or minimum>best_negative['distal_signed_min']:
     best_negative={'target':[x,y,z],'distal_signed_min':minimum,'contact_point':list(points[idx])}
    if minimum>=-.00005 and (best is None or minimum<best['distal_signed_min']):
     best={'target':[x,y,z],'distal_signed_min':minimum,'contact_point':list(points[idx])}
 assert best is not None,(mode,best_negative)
 # Refine the chosen rotation direction, staying in the original reach sphere.
 for step in [.010,.003,.001,.0003]:
  center=best['target'][:]
  for axis in range(3):
   for delta in [-step,step]:
    candidate=center[:];candidate[axis]+=delta;b.paw_pose('L',candidate);v,_=b.evaluated(b.parts['Paw.L']);ds=[];points=[]
    for i in ids:
     p,n,_,d=target_tree.find_nearest(Vector(v[i]));ds.append(d if (Vector(v[i])-p).dot(n)>=0 else -d);points.append(p)
    minimum=min(ds);idx=ds.index(minimum)
    if minimum>=-.00005 and minimum<best['distal_signed_min']:
     best={'target':candidate,'distal_signed_min':minimum,'contact_point':list(points[idx])}
 best['grid_trials']=tested;best['method']='Rigid short-paw orientation only. Distal projection > .135 from original shoulder. Shoulder overlap excluded.'
 results[mode]=best;print(mode,best,flush=True)
(b.OUT/'contact-targets.json').write_text(json.dumps(results,indent=2)+'\n')
