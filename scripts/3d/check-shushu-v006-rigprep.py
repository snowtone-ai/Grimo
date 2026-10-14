"""Independent saved GLB audit; source attributes, textures, surface and limb density."""
import json, struct, hashlib
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/tripo-rigprep-v006-lowpoly'
cfg=json.loads((OUT/'reduction.json').read_text())
def load(p):
 raw=p.read_bytes();assert raw[:4]==b'glTF' and struct.unpack_from('<I',raw,8)[0]==len(raw)
 length=struct.unpack_from('<I',raw,12)[0];j=json.loads(raw[20:20+length]);b=raw[28+length:]
 return raw,j,b
def a(j,b,i):
 ac=j['accessors'][i];v=j['bufferViews'][ac['bufferView']];n={'SCALAR':1,'VEC2':2,'VEC3':3}[ac['type']]
 return np.ndarray((ac['count'],n),dtype={5126:'<f4',5125:'<u4',5123:'<u2'}[ac['componentType']],buffer=b,offset=v.get('byteOffset',0)+ac.get('byteOffset',0)).copy()
def image_bytes(j,b):
 return [b[j['bufferViews'][im['bufferView']].get('byteOffset',0):j['bufferViews'][im['bufferView']].get('byteOffset',0)+j['bufferViews'][im['bufferView']]['byteLength']] for im in j['images']]
def topology(p,idx):
 _,remap=np.unique(p,axis=0,return_inverse=True);f=remap[idx]
 edges=np.sort(np.concatenate([f[:,[0,1]],f[:,[1,2]],f[:,[2,0]]]),axis=1)
 _,counts=np.unique(edges,axis=0,return_counts=True)
 return {'geometric_boundary_edges':int(sum(counts==1)),'geometric_nonmanifold_edges':int(sum(counts>2))}
sr,sj,sb=load(ROOT/cfg['source']);cr,cj,cb=load(ROOT/cfg['output'])
for key in ['nodes','materials','textures','samplers','scenes','scene','animations','skins']:
 assert sj.get(key)==cj.get(key),key
assert image_bytes(sj,sb)==image_bytes(cj,cb) and len(sj['images'])==12
rows=[]
for node in cj['nodes'][1:]:
 mi=node['mesh'];sp=sj['meshes'][mi]['primitives'][0];cp=cj['meshes'][mi]['primitives'][0]
 sattrs=[a(sj,sb,sp['attributes'][key]) for key in ['POSITION','NORMAL','TEXCOORD_0']]
 cattrs=[a(cj,cb,cp['attributes'][key]) for key in ['POSITION','NORMAL','TEXCOORD_0']]
 s=np.concatenate(sattrs,axis=1);c=np.concatenate(cattrs,axis=1)
 assert all(np.isfinite(v).all() for v in cattrs)
 source_rows={v.tobytes() for v in s};assert all(v.tobytes() in source_rows for v in c)
 p,n,uv=cattrs;idx=a(cj,cb,cp['indices']).reshape(-1,3)
 assert idx.max()<len(p)
 cross=np.cross(p[idx[:,1]]-p[idx[:,0]],p[idx[:,2]]-p[idx[:,0]])
 area=np.linalg.norm(cross,axis=1)/2;deg=int(sum(area<=1e-14))
 source_idx=a(sj,sb,sp['indices']).reshape(-1,3);source_p=sattrs[0]
 source_area=np.linalg.norm(np.cross(source_p[source_idx[:,1]]-source_p[source_idx[:,0]],source_p[source_idx[:,2]]-source_p[source_idx[:,0]]),axis=1)/2
 # Any pre-existing degeneracies must be reported, never concealed.
 assert deg==0,(node['name'],deg)
 lengths=np.linalg.norm(n,axis=1);assert np.max(abs(lengths-1))<.002
 topo=topology(p,idx);source_topo=topology(source_p,source_idx)
 assert topo==source_topo,(node['name'],source_topo,topo)
 q={'name':node['name'],'triangles':len(idx),'vertices':len(p),'source_attribute_rows_exact':True,'degenerate_faces':deg,'source_degenerate_faces':int(sum(source_area<=1e-14)),'minimum_area':float(area.min()),'normal_length_range':[float(lengths.min()),float(lengths.max())],'uv_bounds':[uv.min(0).tolist(),uv.max(0).tolist()],'bounds':[p.min(0).tolist(),p.max(0).tolist()],'topology':topo,'source_topology':source_topo}
 if not node['name'].endswith(('_Head','_Torso')):
  assert np.array_equal(s[source_idx],c[idx]);q['all_triangle_attribute_corners_identical']=True
 if node['name'].endswith('_Torso'):
  edges=np.concatenate([idx[:,[0,1]],idx[:,[1,2]],idx[:,[2,0]]]);edge_length=np.linalg.norm(p[edges[:,0]]-p[edges[:,1]],axis=1)
  centers=p[idx].mean(1);q['joint_bands']=[]
  for h in [.065,.13,.205,.265,.46,.505]:
   vs=abs(p[:,1]-h)<.0125;ts=abs(centers[:,1]-h)<.0125
   q['joint_bands'].append({'height':h,'vertices_in_025_band':int(sum(vs)),'triangles_in_025_band':int(sum(ts))})
  feet=p[p[:,1]<.13];q['lower_leg_horizontal_gap']=float(feet[feet[:,0]>0,0].min()-feet[feet[:,0]<0,0].max())
  q['edge_length_percentiles']=np.percentile(edge_length,[50,95,99,100]).tolist()
  q['forearm_torso_horizontal_gaps_at_height_0295_0325']={}
  band=p[(p[:,1]>.295)&(p[:,1]<.325)]
  for paw in ['ShushuStatic_Paw_L','ShushuStatic_Paw_R']:
   pn=next(n for n in cj['nodes'] if n.get('name')==paw);pp=cj['meshes'][pn['mesh']]['primitives'][0]
   pos=a(cj,cb,pp['attributes']['POSITION']);pos=pos[(pos[:,1]>.295)&(pos[:,1]<.325)]
   gap=pos[:,0].min()-band[:,0].max() if paw.endswith('_L') else band[:,0].min()-pos[:,0].max()
   q['forearm_torso_horizontal_gaps_at_height_0295_0325'][paw]=float(gap)
 rows.append(q)
protected=json.loads((OUT/'protected-inputs.json').read_text(encoding='utf-8'));changed=[p for p,h in protected.items() if hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
assert not changed,changed
result={'source_sha256':hashlib.sha256(sr).hexdigest(),'candidate_sha256':hashlib.sha256(cr).hexdigest(),'triangles':sum(r['triangles'] for r in rows),'all_12_image_bytes_identical':True,'materials_nodes_textures_samplers_identical':True,'source_vertex_position_normal_uv_rows_retained_exactly':True,'protected_inputs':len(protected),'protected_changes':changed,'meshes':rows,'rig_animation_skin_counts':[len(cj.get(k,[])) for k in ['skins','animations']],'gltf_y_up_front_positive_z':True,'pose':'source standing A-like pose preserved; not a T pose; future Auto Rig acceptance UNKNOWN'}
(OUT/'saved-glb-checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k!='meshes'}))
