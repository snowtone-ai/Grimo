"""Representative temporary frames for two compact GIFs; no texture work."""
import bpy,bmesh,sys,importlib.util,json,hashlib
from pathlib import Path
import numpy as np
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2];sp=importlib.util.spec_from_file_location('v3',ROOT/'scripts/blender/pino-texture-ready-v003.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)

def proof():
    bpy.ops.wm.open_mainfile(filepath=str(v.DEST/'pino-c-texture-ready-v003-HOLD.blend'))
    o=bpy.data.objects['PINO_C_BASE_RIG_V001'];lids=[bpy.data.objects['PinoSoftLids_'+s] for s in ['L','R']];sc=bpy.context.scene
    # Diagnostic colors only; never save these back to the editing master.
    for name,col in [('Pino_Eye_L',(.025,.10,.20,1)),('Pino_Eye_R',(.025,.10,.20,1)),('Pino_OralInterior',(.03,.018,.018,1))]:bpy.data.materials[name].diffuse_color=col
    v.f.display(sc,360)
    frames=[('closed',(1,0,0,0)),('small',(.75,0,0,0)),('medium',(.4,0,0,0)),('Basis',(0,0,0,0)),('large',(0,1,0,0)),('medium',(.4,0,0,0)),('small',(.75,0,0,0)),('near closed',(.92,0,0,0)),('closed',(1,0,0,0)),('half L',(0,0,.5,0)),('wink L',(0,0,1,0)),('half L',(0,0,.5,0)),('open',(0,0,0,0)),('half R',(0,0,0,.5)),('wink R',(0,0,0,1)),('half both',(0,0,.5,.5)),('three quarter both',(0,0,.75,.75)),('near closed both',(0,0,.95,.95)),('closed both',(0,0,1,1)),('combined',(1,0,.5,1)),('combined large',(0,1,1,1)),('Basis',(0,0,0,0))]
    frames.insert(17,('settling both',(0,0,.925,.925)))
    if '--audit-only' in sys.argv:frames=[]
    manifest=[]
    for i,(name,args) in enumerate(frames):
        v.state(o,lids,*args);manifest.append({'index':i,'label':name,'controls':args})
        for view in ['front','side','3q']:
            v.f.view(sc,view);v.f.render(sc,v.TMP/f'proof-{i:02d}-{view}.png')
    if manifest:(v.TMP/'proof-frames.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
    if frames:
        v.state(o,lids,1);bpy.data.objects['PinoOralLiner'].hide_render=True
        for view in ['front','side','3q']:
            v.f.view(sc,view);v.f.render(sc,v.TMP/f'closed-liner-hidden-{view}.png')
    # Reopen the saved master and check the source invariants, UV, and weights.
    bpy.ops.wm.open_mainfile(filepath=str(v.DEST/'pino-c-texture-ready-v003-HOLD.blend'))
    o=bpy.data.objects['PINO_C_BASE_RIG_V001'];src=np.load(v.TMP/'source.npz')
    audit={'basis_vertex_max_delta':float(np.linalg.norm(v.coords(o)-src['v'],axis=1).max()),'triangles_equal':bool(np.array_equal(np.array([p.vertices[:] for p in o.data.polygons]),src['t'])),'canonical_corner_normal_max_delta':float(np.linalg.norm(np.array([n.vector[:] for n in o.data.corner_normals])-src['corner'],axis=1).max()),'objects':[]}
    uvbank={};meshobs=[x for x in bpy.context.scene.objects if x.type=='MESH' and x.data.shape_keys]
    for idx,ob in enumerate(meshobs):
        me=ob.data;ww=[sum(g.weight for g in p.groups) for p in me.vertices]
        audit['objects'].append({'name':ob.name,'vertices':len(me.vertices),'max_influences':max(len(p.groups) for p in me.vertices),'weight_sum_max_error':max(abs(w-1) for w in ww),'uv_loops':len(me.uv_layers.active.data) if me.uv_layers.active else 0,'morphs':[k.name for k in me.shape_keys.key_blocks]})
        uvbank[f'{idx}_uv']=np.array([l.uv[:] for l in me.uv_layers.active.data]);uvbank[f'{idx}_starts']=np.array([p.loop_start for p in me.polygons]);uvbank[f'{idx}_counts']=np.array([p.loop_total for p in me.polygons]);uvbank[f'{idx}_material']=np.array([p.material_index for p in me.polygons])
    np.savez_compressed(v.TMP/'uv-layout.npz',**uvbank)
    bpy.ops.object.select_all(action='DESELECT')
    for ob in meshobs:ob.select_set(True)
    bpy.context.view_layer.objects.active=o;bpy.ops.object.mode_set(mode='EDIT');bpy.context.scene.tool_settings.use_uv_select_sync=False
    bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.select_all(action='DESELECT')
    try:
        bpy.ops.uv.select_overlap(extend=False);overlaps={}
        for ob in meshobs:
            bm=bmesh.from_edit_mesh(ob.data)
            overlaps[ob.name]=sum(any(l.uv_select_vert for l in p.loops) for p in bm.faces)
        audit['uv_overlap_selection']=overlaps
    except Exception as ex:
        audit['uv_overlap_status']='UNKNOWN '+str(ex);audit['uv_api']=dir(o.data.uv_layers.active)
    if o.mode=='EDIT':bpy.ops.object.mode_set(mode='OBJECT')
    (v.OUT/'saved-master-audit.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf8')

if __name__=='__main__':proof()
