"""One saved-blend contract snapshot, including reversible UV provenance."""
import bpy,json,numpy as np
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];A=ROOT/'assets/grimo/production/jill/tripo/rig-pretexture-v002';E=ROOT/'docs/production/jill/rig-pretexture-v002'
def write(n,x):(E/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
bpy.ops.wm.open_mainfile(filepath=str(A/'jill-rig-pretexture-v002.blend'));r=bpy.data.objects['JILL_RIG'];b=bpy.data.objects['Jill_Body'];m=b.data;src=np.load(E/'intake.npz');N=len(src['v'])
lookup=defaultdict(list)
for i,p in zip(src['loopvert'],src['uv']):lookup[int(i)].append(p)
repair=json.loads((E/'repair-report.json').read_text());exceptions={i for x in repair.get('local_uv_repairs',[]) for i in x['loops']}
errors=[];affine=[];corners=0
for p in m.polygons:
 if all(i<N for i in p.vertices):
  for li,i in zip(p.loop_indices,p.vertices):
   q=np.array(m.uv_layers[1].data[li].uv);errors.append(min(float(np.linalg.norm(q-x)) for x in lookup[i]));corners+=1
   if li not in exceptions:affine.append(float(np.linalg.norm(np.array(m.uv_layers[0].data[li].uv)-(.006+.88*q))))
weights=[[(b.vertex_groups[g.group].name,g.weight) for g in v.groups if g.weight>1e-7] for v in m.vertices]
write('inheritance-validation.json',{'bones':len(r.data.bones),'semantic_channels':len(json.loads((E/'control-contract.json').read_text())['authoring_properties']),'morphs':len(m.shape_keys.key_blocks)-1,'anchors':len([o for o in bpy.context.scene.objects if o.name.startswith('ANCHOR_')]),'inherited_vertices':N,'basis_max_delta':float(np.linalg.norm(np.array([tuple(v.co) for v in m.shape_keys.key_blocks['Basis'].data[:N]])-src['v'],axis=1).max()),'retained_source_uv_corners':corners,'source_uv_max_delta':max(errors),'active_affine_max_delta_excluding_documented_repair':max(affine),'uv_repair_loops':sorted(exceptions),'max_weight_influences':max(map(len,weights)),'weight_sum_max_delta':max(abs(sum(w for _,w in x)-1) for x in weights),'human_visual':'HOLD / numeric inheritance is not approval'})
drivers=[]
for block,label in [(r,'JILL_RIG'),(m.shape_keys,'Jill_Body.shape_keys')]:
 for f in block.animation_data.drivers:
  drivers.append({'owner':label,'path':f.data_path,'index':f.array_index,'expression':f.driver.expression,'variables':[{'name':v.name,'type':v.type,'targets':[{'id':t.id.name if t.id else None,'path':t.data_path} for t in v.targets]} for v in f.driver.variables]})
write('runtime-mapping.json',{'basis':'Blender local Z-up, glTF exported Y-up','drivers':drivers,'bone_rest_matrices':{x.name:[list(row) for row in x.matrix_local] for x in r.data.bones},'constraint_mapping_inherited':'../rig-other-v001/runtime-mapping.json','portable_boundary':'Drivers and IK are Blender authoring logic. Exported sampled proof is runtime-playable; arbitrary semantic solver not implemented. New eyelids are body morphs, eye recession is in blink morphs, eye bone location drivers zero.'})
c=json.loads((E/'control-contract.json').read_text());c['status']='IMPLEMENTED REVIEW / HOLD, Human PENDING';c['artifact_status']=c['status'];c['morph_names']=[k.name for k in m.shape_keys.key_blocks][1:];c['morph_consolidation']='20 body morphs; physical lids and eye recession in FACE_Blink.L/R. No separate lid objects.';c['runtime_mapping_file']='runtime-mapping.json';c['limitations']=[x for x in c['limitations'] if 'No PlayCanvas/phone' not in x];c['limitations']+=['Local PlayCanvas 2.22.2 sampled proof only; phone and arbitrary semantic solver unverified','Facial collar/socket/muzzle continuity remains HOLD','Fold limited to 0.30 rad root sweep, not full wing storage'];c['limitations']=list(dict.fromkeys(c['limitations']))
# Metadata follows the delivered half-strength inherited deltas. Always derive
# from the immutable v001 contract, so repeated snapshots cannot halve twice.
old=json.loads((ROOT/'docs/production/jill/rig-other-v001/control-contract.json').read_text())
old_correctives={x['name']:x for x in old['correctives']}
for correction in c['correctives']:
 if correction['name'].startswith(('COR_WingOpen.','COR_WingFold.')):
  original=old_correctives[correction['name']]
  correction['max_rest_delta']=original['max_rest_delta']*.5
  correction['method']=original['method']+' v002: delta scaled 0.5 after root weighting change, not a new DQ solve.'
write('control-contract.json',c)
print('CONTRACT_SNAPSHOT_COMPLETE')
