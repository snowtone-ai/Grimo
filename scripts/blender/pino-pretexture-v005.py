"""Pino v005 saved-master protection and actual diagnostic texture renders.
Run --inspect before atlas.py; then --proof. Never opens a live Blender session.
"""
import bpy, sys, json, hashlib, importlib.util
from pathlib import Path
import numpy as np
from mathutils import Vector
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
TMP=ROOT/'artifacts/pino-pretexture-v005'
OUT=ROOT/'docs/production/pino/evidence/pretexture-reliability-v005'
DEST=ROOT/'assets/grimo/production/pino/candidate-c/pretexture-reliability-v005'
SRC=ROOT/'assets/grimo/production/pino/candidate-c/texture-handoff-v004/pino-c-texture-handoff-v004.blend'
NAMES=['PINO_C_BASE_RIG_V001','PinoSoftLids_L','PinoSoftLids_R','PinoOralLiner']
for d in [TMP,OUT,DEST]:d.mkdir(parents=True,exist_ok=True)
def module(n,p):
 s=importlib.util.spec_from_file_location(n,ROOT/p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
v=module('pino_v4','scripts/blender/pino-texture-handoff-v004.py')
def dump(n,d):(OUT/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8', newline='\n')
def sha(a):return hashlib.sha256(np.asarray(a).tobytes()).hexdigest()
def fingerprint():
 rows={}
 for name in NAMES:
  o=bpy.data.objects[name];m=o.data
  rows[name]=dict(basis=sha(np.array([x.co[:] for x in m.vertices],'<f4')),corner=sha(np.array([x.vertex_index for x in m.loops],'<u4')),poly=sha(np.array([x.loop_total for x in m.polygons],'<u4')),uv=sha(np.array([x.uv[:] for x in m.uv_layers.active.data],'<f4')),ownership=sha(np.array([x.material_index for x in m.polygons],'<u4')),slots=[x.name for x in m.materials],groups=[g.name for g in o.vertex_groups],weights=sha(np.array([(i,g.group,g.weight) for i,x in enumerate(m.vertices) for g in x.groups],'<f8')),shapes={k.name:sha(np.array([x.co[:] for x in k.data],'<f4')) for k in m.shape_keys.key_blocks},normal_fields={a.name:sha(np.array([x.vector[:] for x in a.data],'<f4')) for a in m.attributes if a.data_type=='FLOAT_VECTOR' and (a.name.startswith('PinoDN_') or a.name=='PinoCanonicalCornerNormal')},matrix=np.array(o.matrix_world).tolist(),modifiers=[(a.name,a.type) for a in o.modifiers])
 r=bpy.data.objects['PINO_C_TRIPO_PLUS_CONTROLS_V001'];rows['rig']={b.name:dict(parent=b.parent.name if b.parent else None,rest=np.array(b.matrix_local).tolist()) for b in r.data.bones}
 return rows
def inspect():
 path=DEST/'pino-c-pretexture-v005.blend' if '--candidate' in sys.argv else SRC
 bpy.ops.wm.open_mainfile(filepath=str(path));rows=[];bank={}
 for i,o in enumerate(x for x in bpy.data.objects if x.type=='MESH'):
  m=o.data;m.calc_loop_triangles();p=np.array([x.co[:] for x in m.vertices]);t=np.array([x.vertices[:] for x in m.loop_triangles]);li=np.array([x.loops[:] for x in m.loop_triangles]);uv=np.array([x.uv[:] for x in m.uv_layers.active.data])
  bank.update({f'{i}_p':p,f'{i}_t':t,f'{i}_li':li,f'{i}_uv':uv,f'{i}_mat':np.array([m.polygons[x.polygon_index].material_index for x in m.loop_triangles])})
  rows.append(dict(i=i,name=o.name))
 np.savez_compressed(TMP/'mesh-data.npz',**bank);(TMP/'inspect.json').write_text(json.dumps(rows), encoding='utf8', newline='\n')
def attach(image):
 for name in ['Pino_Skin','Pino_Eye_L','Pino_Eye_R','Pino_LidSkin','Pino_OralInterior']:
  m=bpy.data.materials[name];m.use_nodes=True;n=m.node_tree.nodes;lk=m.node_tree.links
  tex=n.get('V005_DIAGNOSTIC_IMAGE') or n.new('ShaderNodeTexImage');tex.name='V005_DIAGNOSTIC_IMAGE';tex.image=image;tex.interpolation='Linear';tex.extension='EXTEND'
  bs=next(x for x in n if x.type=='BSDF_PRINCIPLED');lk.new(tex.outputs['Color'],bs.inputs['Base Color']);bs.inputs['Roughness'].default_value=.85
  bs.inputs['Metallic'].default_value=0
def stage(sc):
 sc.render.engine='CYCLES';sc.cycles.samples=12;sc.cycles.use_denoising=True
 sc.render.resolution_x=600;sc.render.resolution_y=600;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.film_transparent=False
 sc.view_settings.view_transform='Standard';sc.view_settings.look='None'
 sc.world.use_nodes=True;sc.world.node_tree.nodes.get('Background').inputs[0].default_value=(.22,.25,.30,1);sc.world.node_tree.nodes.get('Background').inputs[1].default_value=.5
 for o in sc.objects:
  if o.type=='LIGHT':o.hide_render=True
 for name,loc,power,size in [('Key',(1.7,-2,2.4),70,2.5),('Fill',(-1.7,-1,1.1),40,2),('Rim',(0,1.8,2),60,2)]:
  d=bpy.data.lights.new('V005_'+name,'AREA');d.energy=power;d.shape='DISK';d.size=size;o=bpy.data.objects.new(d.name,d);sc.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,.5))-o.location).to_track_quat('-Z','Y').to_euler()
def render(sc,label,view,face=False):
 v.v3.f.view(sc,view,target=(0,-.16,.65) if face else (0,.015,.48),scale=.57 if face else 1.3)
 sc.render.filepath=str(TMP/(label+'-'+view+'.png'));bpy.ops.render.render(write_still=True)
def proof():
 bpy.ops.wm.open_mainfile(filepath=str(SRC));before=fingerprint()
 bpy.ops.wm.open_mainfile(filepath=str(DEST/'pino-c-pretexture-v005.blend'))
 uv_before={name:before[name].pop('uv') for name in NAMES}
 candidate_contract=fingerprint()
 for name in NAMES:candidate_contract[name].pop('uv')
 assert before==candidate_contract,'UV repair changed a protected non-UV field'
 r=bpy.data.objects['PINO_C_TRIPO_PLUS_CONTROLS_V001'];o=bpy.data.objects[NAMES[0]];sc=bpy.context.scene
 for name in NAMES:
  bpy.data.objects[name]['v005_texture_gate']='PENDING; diagnostics only; PinoUV_v005'
  bpy.data.objects[name]['UV_contract']='PinoUV_v005; synchronized input/review/map'
 bpy.context.preferences.filepaths.save_version=0
 master=DEST/'pino-c-pretexture-v005.blend';bpy.ops.wm.save_as_mainfile(filepath=str(master),compress=True)
 bpy.ops.wm.open_mainfile(filepath=str(master));after=fingerprint()
 for name in NAMES:after[name].pop('uv')
 assert before==after
 assert all(bpy.data.objects[n].data.uv_layers.active.name=='PinoUV_v005' for n in NAMES)
 assert all(abs(k.value)<1e-7 for n in NAMES for k in bpy.data.objects[n].data.shape_keys.key_blocks)
 master_sha=hashlib.sha256(master.read_bytes()).hexdigest()
 dump('master-preservation.json',dict(all_protected_non_uv_fields_exact=True,source=str(SRC.relative_to(ROOT)),saved=str(master.relative_to(ROOT)),original_uv_sha=uv_before,fields=after))
 o=bpy.data.objects[NAMES[0]];r=bpy.data.objects['PINO_C_TRIPO_PLUS_CONTROLS_V001'];sc=bpy.context.scene;stage(sc)
 color=bpy.data.images.load(str(TMP/'diagnostic-color-4k.png'),check_existing=True)
 check=bpy.data.images.load(str(TMP/'checker-4k.png'),check_existing=True)
 states=[('neutral','neutral',0,0,0,0,0),('blink-half','neutral',0,0,0,.5,.5),('closed','neutral',0,1,0,1,1),('wink','neutral',0,.4,0,1,0),('mouth-small','neutral',0,.65,0,0,0),('mouth-open','neutral',0,0,1,0,0),('contact-mid','contact',.5,0,0,0,0),('contact','contact',1,0,0,0,0),('rest-mid','rest',.5,0,0,0,0),('rest','rest',1,0,0,0,0),('tail-L','tail',1,0,0,0,0),('tail-R','tail',-1,0,0,0,0),('mouth-closed','neutral',0,1,0,0,0)]
 for mode,img in ([('color',color)] if '--recolor' in sys.argv else [('color',color),('checker',check)]):
  attach(img)
  for label,kind,s,c,l,bl,br in states:
   if mode=='checker' and label in ['wink','mouth-small','tail-R','mouth-closed']:continue
   v.body_state(o,r,kind,s,c,l,bl,br)
   face=label in ['blink-half','closed','wink','mouth-small','mouth-open','mouth-closed']
   views=['front','side','3q'] if label=='neutral' else (['front','side'] if face else ['3q','side'])
   for view in views:render(sc,mode+'-'+label,view,face)
   if label=='neutral':
    for view in ['front','side']:render(sc,mode+'-neutral-face',view,True)
 if '--recolor' in sys.argv:
  attach(check);v.body_state(o,r)
  for view in ['front','side']:render(sc,'checker-neutral-face',view,True)
 # Same output images, attached to this existing rig only.
 returned=bpy.data.images.load(str(TMP/'returned-changed-4k.png'),check_existing=True)
 attach(returned)
 for label,kind,s,c,l,bl,br in [states[0],states[3],states[5],states[7],states[9],states[10]]:
  v.body_state(o,r,kind,s,c,l,bl,br)
  render(sc,'returned-'+label,'3q',label in ['wink','mouth-open'])
 v.body_state(o,r);attach(color)
 for im in [color,check,returned]:im.use_fake_user=True;im.pack()
 proof_path=DEST/'pino-c-v005-diagnostic-proof.blend'
 bpy.ops.wm.save_as_mainfile(filepath=str(proof_path),compress=True)
 bpy.ops.wm.open_mainfile(filepath=str(proof_path));packed=[]
 for basename in ['diagnostic-color-4k.png','checker-4k.png','returned-changed-4k.png']:
  im=bpy.data.images[basename];assert im.packed_file and im.use_fake_user
  digest=hashlib.sha256(im.packed_file.data).hexdigest()
  assert digest==hashlib.sha256((TMP/basename).read_bytes()).hexdigest()
  packed.append(dict(image=basename,packed=True,retained_after_reopen=True,sha256=digest))
 assert hashlib.sha256(master.read_bytes()).hexdigest()==master_sha
 report=json.loads((OUT/'master-preservation.json').read_text(encoding='utf8'))
 report['diagnostic_packed_images']=packed;report['master_neutral_uv_and_nonmutation_rechecked']=True
 dump('master-preservation.json',report)
 dump('render-scope.json',dict(states=[dict(name=a,kind=b,strength=c,face=[d,e,f,g]) for a,b,c,d,e,f,g in states],engine='Cycles 12 samples + denoise',diagnostic_only=True,production_texture=False,production_motion=False))
if __name__=='__main__':
 if '--inspect' in sys.argv:inspect()
 if '--proof' in sys.argv:proof()
