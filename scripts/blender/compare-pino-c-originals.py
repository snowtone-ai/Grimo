"""Read-only FBX/GLB authority comparison, before selecting a Master."""
import bpy,json,importlib.util
from pathlib import Path
import numpy as np
spec=importlib.util.spec_from_file_location('pino_prove',Path(__file__).with_name('prove-pino-c-geometry.py'))
u=importlib.util.module_from_spec(spec);spec.loader.exec_module(u)
ROOT,ASSET,OUT=u.ROOT,u.ASSET,u.OUT

def material(m):
    nodes=[]
    for n in m.node_tree.nodes:
        if n.type=='BSDF_PRINCIPLED':
            nodes.append({s.name:list(s.default_value) if hasattr(s.default_value,'__iter__') else s.default_value for s in n.inputs if hasattr(s,'default_value') and s.name in ['Base Color','Metallic','Roughness','Alpha','IOR','Specular IOR Level','Transmission Weight','Coat Weight']})
    return dict(name=m.name,diffuse_color=list(m.diffuse_color),roughness=m.roughness,metallic=m.metallic,principled=nodes,image_nodes=[n.image.name for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image])

data={}
for ext in ['fbx','glb']:
    path=ASSET/'source'/f'cute blue creature 3d model.{ext}';o=u.u.load(path);cam=u.setup(o)
    data[ext]=dict(source_sha256=u.sha(path),materials=[material(m) for m in o.data.materials],uv_layers=len(o.data.uv_layers),custom_normals=o.data.has_custom_normals,
        transforms=[dict(name=p.name,type=p.type,matrix_world=[list(row) for row in p.matrix_world]) for p in bpy.context.scene.objects if p.type in ['MESH','EMPTY']],polygons=len(o.data.polygons),vertex_count=len(o.data.vertices))
    for view in u.VIEWS:u.render(cam,f'original-{ext}-{view}',view)
    bpy.context.preferences.filepaths.save_version=0;bpy.context.scene['role']='FROZEN ORIGINAL IMPORT / MASTER UNDECIDED / DO NOT EDIT'
    bpy.ops.wm.save_as_mainfile(filepath=str(ASSET/f'pino-c-original-{ext}-comparison.blend'))
f=np.load(OUT/'fbx-diagnostic-arrays.npz');g=np.load(OUT/'glb-diagnostic-arrays.npz');ft,gt=f['triangles'],g['triangles'];fv,gv=f['vertices'],g['vertices'];fs={tuple(sorted(map(int,t))) for t in ft};gs={tuple(sorted(map(int,t))) for t in gt}
data['differing_triangles']={tag:[dict(indices=t,center=v[list(t)].mean(axis=0).tolist(),component=int(g['components'][t[0]])) for t in sorted(a-b)] for tag,a,b,v in [('fbx',fs,gs,fv),('glb',gs,fs,gv)]}
data['master']='UNDECIDED / HUMAN DECISION REQUIRED: imported triangle surfaces differ'
u.write_json(OUT/'originals-comparison.json',data)
