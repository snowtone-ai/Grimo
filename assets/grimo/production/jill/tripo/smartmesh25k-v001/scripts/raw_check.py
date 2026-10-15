import sys,struct,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from audit_common import *
b=(ASSET/'input/cute dragon 3d model (1).glb').read_bytes()
n=struct.unpack_from('<I',b,12)[0]; j=json.loads(b[20:20+n]); blob=b[28+n:]
tri=np.frombuffer(blob,dtype='<u4',offset=673200,count=163119).reshape(-1,3)
pos=np.frombuffer(blob,dtype='<f4',offset=0,count=84150).reshape(-1,3)
mesh=bpy.data.meshes.new('RawGLBIndices'); mesh.from_pydata([(x,-z,y) for x,y,z in pos],[],tri.tolist())
o=bpy.data.objects.new('RAW_EXACT_TRIANGLES',mesh); bpy.context.scene.collection.objects.link(o)
a=audit(o); write_json('raw-glb-audit.json',a)
out={}
rt={tuple(sorted(t)) for t in tri.tolist()}
for obj in bpy.data.objects:
    if obj.type=='MESH' and obj.name.startswith('Original'):
        out[obj.name]={'matching_raw_triangle_sets':sum(tuple(sorted(p.vertices)) in rt for p in obj.data.polygons),
                      'first_12_faces':[list(p.vertices) for p in list(obj.data.polygons)[:12]]}
write_json('raw-import-comparison.json',out)
print(json.dumps({'comparisons':out,'raw_first_12':tri[:12].tolist(),'small_components':[c for c in a['components'] if c['faces']<15]}))
for obj in bpy.context.scene.objects:
    if obj.type=='MESH': obj.hide_render=obj!=o
o.color=(.58,.68,.55,1)
render(bpy.context.scene,'raw-original-front',(0,-1,0),(0,0,.5),1.16)
bpy.ops.wm.save_as_mainfile(filepath=str(ASSET/'jill-raw-inspection.blend'))
