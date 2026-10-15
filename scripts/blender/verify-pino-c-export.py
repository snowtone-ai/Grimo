"""Reimport and nine-view comparison of FBX-derived GLB to formal original GLB."""
import bpy,json,hashlib,importlib.util,sys
from pathlib import Path
import numpy as np
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('pino_prove',Path(__file__).with_name('prove-pino-c-geometry.py'));u=importlib.util.module_from_spec(spec);spec.loader.exec_module(u)
ROOT,ASSET,OUT=u.ROOT,u.ASSET,u.OUT
def snapshot(o):
    m=o.data;m.calc_loop_triangles()
    return dict(vertices=np.array([tuple(v.co) for v in m.vertices]),triangles=np.array([tuple(t.vertices) for t in m.loop_triangles]),normals=np.array([tuple(n.vector) for n in m.corner_normals]),matrix=np.array(o.matrix_world))
a=snapshot(u.u.load(ASSET/'source/cute blue creature 3d model.glb'))
o=u.u.load(ASSET/'delivery/pino-c-master-derived-neutral.glb');b=snapshot(o)
checks={k:bool(np.array_equal(a[k],b[k])) for k in a};assert all(checks.values()),checks
cam=u.setup(o)
for view in u.VIEWS:u.render(cam,f'master-derived-{view}',view)
u.write_json(OUT/'export-reimport.json',dict(source_reference='source/cute blue creature 3d model.glb',output='delivery/pino-c-master-derived-neutral.glb',exact_reimport_checks=checks,render_settings='Same setup and nine cameras as original-glb-*; pixel verification in report script',master_export=u.sha(ASSET/'delivery/pino-c-master-derived-neutral.glb'),human_geometry_gate='PENDING'))
print(checks)
