"""Read-only donor comparison: same cameras for current-axis assets, head-fit for legacy a-v006."""
import bpy,importlib.util,json,tempfile,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('ear',ROOT/'scripts/blender/build-carol-ear-production-v001.py');ear=importlib.util.module_from_spec(spec);spec.loader.exec_module(ear)
ear.TMP=Path(tempfile.gettempdir())/'carol-ear-v002';ear.TMP.mkdir(exist_ok=True)
names=['carol-ear-production-v001','carol-hero-modules-v003','carol-hero-modules-v002','carol-v011','carol-v012','carol-v013','carol-hero-experience-probe-v001','carol-a-v006']
report={}
import sys
for name in (names if '--legacy-only' not in sys.argv else ['carol-a-v006']):
 path=ROOT/'assets/grimo/production/carol/blender'/f'{name}.blend'
 if not path.exists():report[name]={'present':False};continue
 bpy.ops.wm.open_mainfile(filepath=str(path));scene=bpy.context.scene;scene.frame_set(1)
 scene.render.use_compositing=False;scene.render.use_sequencer=False
 scene.render.engine='CYCLES';scene.cycles.samples=16;scene.cycles.use_denoising=True
 if name=='carol-a-v006':
  visible={o.name for o in bpy.data.objects if any(k in o.name.lower() for k in ['head','eye','nose','mouth','philtrum','tongue'])}
  head=bpy.data.objects['Head_Volumetric_Cheeks_Jaw']; bounds=[head.matrix_world@Vector(v) for v in head.bound_box];center=sum(bounds,Vector())/8
  target=center;scale=1.7
  scene.world=bpy.data.worlds.new('TEMP audit world');scene.world.use_nodes=True;scene.world.node_tree.nodes.get('Background').inputs[0].default_value=(.65,.65,.65,1)
  ld=bpy.data.lights.new('TEMP audit key','AREA');ld.energy=450;ld.shape='DISK';ld.size=4
  lo=bpy.data.objects.new('TEMP audit key',ld);scene.collection.objects.link(lo);lo.location=center+Vector((2,-4,4));lo.rotation_euler=(center-lo.location).to_track_quat('-Z','Y').to_euler()
  directions=[('side',(4,0,0)),('front',(0,-4,0))]
 else:
  visible={'CENTRAL_CHASSIS','EYE_L','EYE_R','EYELID_L','EYELID_R','NOSE','MOUTH_closed','PHILTRUM'}
  target=(.28,0,.47);scale=.66;directions=[('side',(0,-4,0)),('front',(-4,0,0))]
 report[name]={'present':True,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'face_objects':{o.name:ear.snapshot(o) for o in bpy.data.objects if o.name in visible}}
 for view,d in directions:ear.render('audit-'+name+'-'+view,d,target,scale,visible,size=(420,420))
if '--legacy-only' in sys.argv:
 old=json.loads((ear.TMP/'audit.json').read_text());old.update(report);report=old
(ear.TMP/'audit.json').write_text(json.dumps(report,indent=2))
