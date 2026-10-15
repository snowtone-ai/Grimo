"""Reframe existing low-rest samples to show the entire failed pose, not a crop."""
import bpy,json,hashlib,importlib.util,sys
from pathlib import Path
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('pino_exercise',Path(__file__).with_name('exercise-pino-c-geometry.py'));e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
d=json.loads((e.OUT/'four-tests.json').read_text(encoding='utf-8'));r=next(x for x in d['runs'] if x['name']=='low-rest')
for row in r['frames']:
    v=e.rest(row['strength']);assert hashlib.sha256(v.astype('<f8').tobytes()).hexdigest()==row['world_vertex_sha256']
    e.write_vertices(v)
    for view in ['front','threequarter','side']:e.render_frame('low-rest',row['frame'],view)
e.scene.render.engine='CYCLES';e.scene.cycles.samples=32;e.scene.view_settings.exposure=-.3;e.write_vertices(e.rest(1))
for view in ['front','threequarter','side']:e.render_frame('cycles-low-rest',0,view)
e.u.write_json(e.OUT/'rest-framing.json',dict(geometry_changed=False,sample_hashes_rechecked=25,orthographic_scale=1.8,target=[0,-.2,.38],reason='Original pose extremes exceeded tight framing. Re-render same actual samples with fixed larger framing for all rest frames/views. Failure remains visible; no pose correction adopted.'))
