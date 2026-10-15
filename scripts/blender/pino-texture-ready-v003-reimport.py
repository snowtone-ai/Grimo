"""Reopen the delivered master, import GLB, compare by stable provenance IDs."""
import bpy,sys,importlib.util,json,math
from pathlib import Path
import numpy as np
from mathutils import Matrix
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2];sp=importlib.util.spec_from_file_location('v3',ROOT/'scripts/blender/pino-texture-ready-v003.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
sp=importlib.util.spec_from_file_location('glb',ROOT/'scripts/3d/package-pino-texture-ready-v003.py');gl=importlib.util.module_from_spec(sp);sp.loader.exec_module(gl)

def bind_normals(objects):
    """Recreate the Blender preview using only normals embedded in the GLB."""
    g,blob=gl.read(v.DEST/'pino-c-texture-ready-v003-HOLD.glb')
    for name,ob in objects.items():
        node=next(n for n in g['nodes'] if n.get('name')==name);mesh=g['meshes'][node['mesh']];keys=mesh['extras']['targetNames'];size=max(int(gl.accessor(g,blob,p['attributes']['_PINO_CORNER_ID']).max()) for p in mesh['primitives'])+1
        base=np.zeros((size,3));bank={k:np.zeros((size,3)) for k in keys}
        for p in mesh['primitives']:
            ids=gl.accessor(g,blob,p['attributes']['_PINO_CORNER_ID']).ravel().round().astype(int)
            def convert(a):return np.c_[a[:,0],-a[:,2],a[:,1]]
            base[ids]=convert(gl.accessor(g,blob,p['attributes']['NORMAL']))
            for k,t in zip(keys,p['targets']):bank[k][ids]=convert(gl.accessor(g,blob,t['NORMAL']))
        ids=np.array([a.value for a in ob.data.attributes['_PINO_CORNER_ID'].data]).round().astype(int);loops=ids[np.array([l.vertex_index for l in ob.data.loops])]
        v.normal_controller(ob,base[loops],{k:a[loops] for k,a in bank.items()})

def run():
    bpy.ops.wm.open_mainfile(filepath=str(v.DEST/'pino-c-texture-ready-v003-HOLD.blend'))
    o=bpy.data.objects['PINO_C_BASE_RIG_V001'];lids=[bpy.data.objects['PinoSoftLids_'+s] for s in ['L','R']]
    names=[o.name,*[x.name for x in lids],'PinoOralLiner'];states=[('Basis',(0,0,0,0)),('closed',(1,0,0,0)),('half',(0,0,.5,.5)),('combined',(0,1,1,1)),('wink',(1,0,1,0)),('head-probe',(.4,0,.5,1))]
    states.insert(-1,('three-quarter',(0,0,.75,.75)))
    states.insert(-1,('settling',(0,0,.925,.925)))
    states.insert(-1,('near-closed',(0,0,.95,.95)))
    def head_probe():
        rig=next(ob for ob in bpy.context.scene.objects if ob.type=='ARMATURE');head=rig.pose.bones['mixamorig:Head'];pivot=head.matrix.translation.copy()
        head.matrix=Matrix.Translation(pivot)@Matrix.Rotation(math.radians(6),4,'Z')@Matrix.Translation(-pivot)@head.matrix
        bpy.context.view_layer.update()
    bank={};normals={};uv={};colors={}
    for name,args in states:
        v.state(o,lids,*args)
        if name=='head-probe':head_probe()
        for obname in names:
            ob=bpy.data.objects[obname];bank[(name,obname)]=v.f.evaluated(ob);ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());normals[(name,obname)]=np.array([n.vector[:] for n in ev.data.corner_normals]);uv[obname]=np.array([u.uv[:] for u in ob.data.uv_layers.active.data])
            for mat in ob.data.materials:colors[mat.name]=mat.diffuse_color[:]
        if name in ['Basis','closed','combined','wink']:
            v.f.display(bpy.context.scene,360)
            for view in ['front','3q']:
                v.f.view(bpy.context.scene,view);v.f.render(bpy.context.scene,v.TMP/f'roundtrip-master-{name}-{view}.png')
    for ob in list(bpy.context.scene.objects):
        if ob.type in ['MESH','ARMATURE']:bpy.data.objects.remove(ob,do_unlink=True)
    bpy.ops.import_scene.gltf(filepath=str(v.DEST/'pino-c-texture-ready-v003-HOLD.glb'))
    objects={name:bpy.data.objects.get(name) for name in names};audit=[]
    for name,ob in objects.items():
        audit.append({'object':name,'found':ob is not None,'vertices':len(ob.data.vertices) if ob else None,'attributes':list(ob.data.attributes.keys()) if ob else []})
    o=objects[names[0]];lids=[objects['PinoSoftLids_'+s] for s in ['L','R']];comparisons=[]
    # Match Workbench display swatches for this proof. Shader colors untouched.
    for ob in objects.values():
        for mat in ob.data.materials:
            if mat.name.split('.')[0] in colors:mat.diffuse_color=colors[mat.name.split('.')[0]]
    v.state(o,lids,1);v.f.display(bpy.context.scene,360);v.f.view(bpy.context.scene,'front');v.f.render(bpy.context.scene,v.TMP/'roundtrip-native-closed.png')
    bind_normals(objects)
    for name,args in states:
        v.state(o,lids,*args)
        if name=='head-probe':head_probe()
        for obname,ob in objects.items():
            attr=ob.data.attributes.get('_PINO_VERTEX_ID')
            if not attr:comparisons.append({'state':name,'object':obname,'status':'UNKNOWN provenance attribute absent'});continue
            ids=np.array([a.value for a in attr.data]).round().astype(int);actual=v.f.evaluated(ob);expect=bank[(name,obname)][ids]
            cornerids=np.array([a.value for a in ob.data.attributes['_PINO_CORNER_ID'].data]).round().astype(int);loopids=cornerids[np.array([l.vertex_index for l in ob.data.loops])]
            ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());nn=np.array([n.vector[:] for n in ev.data.corner_normals]);en=normals[(name,obname)][loopids];valid=np.linalg.norm(en,axis=1)>.5
            comparisons.append({'state':name,'object':obname,'max_position_error':float(np.linalg.norm(actual-expect,axis=1).max()),'max_normal_vector_error':float(np.linalg.norm(nn[valid]-en[valid],axis=1).max(initial=0)),'max_uv_error':float(np.linalg.norm(np.array([u.uv[:] for u in ob.data.uv_layers.active.data])-uv[obname][loopids],axis=1).max())})
        if name in ['Basis','closed','combined','wink']:
            v.f.display(bpy.context.scene,360)
            for view in ['front','3q']:
                v.f.view(bpy.context.scene,view);v.f.render(bpy.context.scene,v.TMP/f'reimport-{name}-{view}.png')
    (v.OUT/'reimport-audit.json').write_text(json.dumps({'objects':audit,'comparisons':comparisons,'normal_note':'Native Blender import does not bind GLB morph normals. bind_normals() reconstructs the preview from the GLB alone. Proof display swatches normalized; shader colors untouched.'},indent=2)+'\n',encoding='utf8')

if __name__=='__main__':run()
