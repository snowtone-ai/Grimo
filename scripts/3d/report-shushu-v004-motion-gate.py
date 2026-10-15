"""Measured comparisons and preservation; no inferred Human PASS."""
from pathlib import Path
import hashlib,json,numpy as np
from scipy.spatial import cKDTree
R=Path(__file__).resolve().parents[2];D=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready'
def write(name,data):(D/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
rows=[]
for f in [1,477,493,509,517,533,549]:
 author=np.load(D/'author-normals'/f'f{f}.npz')
 before=json.loads((D/'desktop-source-normals'/f'exported-normal-{f}.json').read_text())
 after=json.loads((D/'desktop'/f'surface-{f}.json').read_text())
 for mesh in after['meshes']:
  name=mesh['name'];p=np.asarray(mesh['position']).reshape(-1,3);n=np.asarray(mesh['normal']).reshape(-1,3);a=author[name+'-p'];an=author[name+'-n'];a=a[:,[0,2,1]]*np.array([1,1,-1]);an=an[:,[0,2,1]]*np.array([1,1,-1]);err,ids=cKDTree(a).query(p)
  old=next(x for x in before['meshes'] if x['name']==name);oldn=np.asarray(old['normal'])
  def stats(n):
   n=n/np.linalg.norm(n,axis=1)[:,None];angle=np.degrees(np.arccos(np.clip((n*an[ids]).sum(1),-1,1)))
   return {'median':float(np.median(angle)),'p95':float(np.quantile(angle,.95)),'max':float(angle.max()),'over20deg':int((angle>20).sum())}
  rows.append({'frame':f,'mesh':name,'max_position_error':float(err.max()),'exported_normal_deg':stats(oldn),'corrected_normal_deg':stats(n)})
write('paw-normal-comparison.json',{'mapping':'Nearest posed vertex per sample; coincident vertices can be ambiguous. Geometric normals and authored split normals differ at some seam/degenerate vertices; this is not exact-normal proof.','rows':rows})
protected=json.loads((D/'protected-inputs.json').read_text(encoding='utf8'));changes=[];missing=[]
for p,h in protected.items():
 path=R/p
 if not path.exists():missing.append(p);continue
 actual=hashlib.sha256(path.read_bytes()).hexdigest()
 if actual!=h:changes.append({'path':p,'before':h,'after':actual})
write('protected-inputs-check.json',{'count':len(protected),'changes':changes,'missing':missing,'allowed_state_doc':['docs/production/Handoff.md'],'original_not_replaced':not any(x['path'].startswith('assets/') for x in changes)})
