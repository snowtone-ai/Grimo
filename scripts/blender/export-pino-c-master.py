"""FBX-only geometry source; immutable GLB supplies appearance/triangulation policy.

No repair is adopted. Never copy modified GLB geometry back into the Master.
The output is a retained-geometry candidate, not a Tripo-ready approval.
"""
import bpy,json,struct,hashlib,importlib.util,sys
from pathlib import Path
from collections import defaultdict,Counter
import numpy as np
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2];ASSET=ROOT/'assets/grimo/production/pino/candidate-c';OUT=ROOT/'docs/production/pino/evidence/geometry-c-v001'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
decision=json.loads((OUT/'master-decision.json').read_text(encoding='utf-8'))
assert decision['status']=='HUMAN_SELECTED' and decision['source'].endswith('.fbx')
master=ROOT/decision['source'];reference=ASSET/'source/cute blue creature 3d model.glb'
assert sha(master)==decision['sha256']
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.ops.import_scene.fbx(filepath=str(master))
o=next(x for x in bpy.context.scene.objects if x.type=='MESH');me=o.data
native=np.array([tuple(v.co) for v in me.vertices],dtype='<f4')
raw=reference.read_bytes();n=struct.unpack_from('<I',raw,12)[0];j=json.loads(raw[20:20+n]);bn=struct.unpack_from('<I',raw,20+n)[0];blob=bytearray(raw[28+n:28+n+bn]);p=j['meshes'][0]['primitives'][0]
def accessor(k):
    a=j['accessors'][k];b=j['bufferViews'][a['bufferView']];offset=b.get('byteOffset',0)+a.get('byteOffset',0)
    assert 'byteStride' not in b
    dtype={5126:'<f4',5125:'<u4'}[a['componentType']];width={'SCALAR':1,'VEC3':3}[a['type']]
    return np.frombuffer(blob,dtype=dtype,count=a['count']*width,offset=offset).reshape(a['count'],width),offset
expected,pos_offset=accessor(p['attributes']['POSITION']);tri,_=accessor(p['indices']);tri=tri.reshape(-1,3)
assert np.array_equal(native,expected), 'Cannot use reference topology without exact native FBX vertex correspondence'
# Every export triangle must be contained in an FBX face; no geometry donor.
polys=[set(f.vertices) for f in me.polygons];byvert=defaultdict(set)
for i,f in enumerate(polys):
    for v in f:byvert[v].add(i)
unmatched=[];candidate_counts=Counter()
for i,t in enumerate(tri):
    candidates=set.intersection(*(byvert[int(v)] for v in t))
    candidate_counts[len(candidates)]+=1
    if not candidates:unmatched.append(i)
report=dict(master=decision,appearance_reference_sha256=sha(reference),native_fbx_positions_exact_to_glb_reference=True,
    export_triangle_count=len(tri),export_triangles_not_contained_in_fbx_faces=unmatched,
    candidate_face_count_histogram=dict(candidate_counts),
    policy='FBX native vertex coordinates are sole exported position source. Original GLB supplies export tessellation, split-normal bytes and material values solely to preserve its formal Neutral appearance. No independent GLB repair or vertex edit.',
    repair='NONE ADOPTED; overlapping tails/root and global topology remain BLOCKED',human_geometry_gate='PENDING')
if unmatched:
    report['status']='BLOCKED: original GLB tessellation cannot be verified against FBX polygons'
else:
    # Explicitly write every exported position from the FBX, retaining exact units/axis.
    blob[pos_offset:pos_offset+native.nbytes]=native.tobytes()
    j.setdefault('asset',{}).setdefault('extras',{})['pinoGeometryProvenance']={'masterSHA256':sha(master),'appearanceReferenceSHA256':sha(reference),'repair':'none','gate':'PENDING'}
    jb=json.dumps(j,separators=(',',':'),ensure_ascii=False).encode();jb+=b' '*((-len(jb))%4);blob.extend(b'\0'*((-len(blob))%4))
    payload=struct.pack('<III',0x46546c67,2,12+8+len(jb)+8+len(blob))+struct.pack('<II',len(jb),0x4e4f534a)+jb+struct.pack('<II',len(blob),0x004e4942)+blob
    output=ASSET/'delivery/pino-c-master-derived-neutral.glb';output.write_bytes(payload)
    report.update(status='EXPORTED / RETAINED GEOMETRY / APPEARANCE VERIFICATION REQUIRED',output=output.relative_to(ROOT).as_posix(),output_sha256=sha(output),active_binary_payload_byte_exact_to_reference=bytes(blob)==raw[28+n:28+n+bn],materials_exact_to_reference=True)
# Save a faithful editable import of the FBX, without applying import-axis rotation.
bpy.context.scene['sole_geometry_master']=decision['source'];bpy.context.scene['appearance_reference']=str(reference.relative_to(ROOT));bpy.context.scene['geometry_gate']='PENDING';bpy.context.scene['repairs_adopted']='NONE'
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(ASSET/'pino-c-master-retained.blend'))
report.update(master_source_sha256_after=sha(master),reference_sha256_after=sha(reference))
(OUT/'master-export.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
