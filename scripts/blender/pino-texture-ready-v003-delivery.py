"""Package the isolated v003 candidate; never alters any source revision.

Run with Blender from repo root after pino-texture-ready-v003.py --build --fill-mouth.
The status stays HOLD until the visual and portability gates pass.
"""
import bpy,bmesh,sys,importlib.util,json,hashlib,struct,math
from pathlib import Path
import numpy as np
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
sp=importlib.util.spec_from_file_location('v3',ROOT/'scripts/blender/pino-texture-ready-v003.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
sp=importlib.util.spec_from_file_location('uvcheck',ROOT/'scripts/3d/pino-uv-overlap.py');uvcheck=importlib.util.module_from_spec(sp);sp.loader.exec_module(uvcheck)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def repair_uv_charts(meshes):
    repaired={ob.name:set() for ob in meshes}
    while True:
        triangles=[];owners=[]
        for oi,ob in enumerate(meshes):
            bm=bmesh.from_edit_mesh(ob.data);bm.faces.index_update();bm.normal_update();layer=bm.loops.layers.uv.active
            for p in bm.faces:
                q=np.array([l[layer].uv[:] for l in p.loops])
                for i in range(1,len(q)-1):triangles.append(q[[0,i,i+1]]);owners.append((oi,p.index))
        pairs,zero=uvcheck.overlaps(triangles);owners=np.array(owners);badowners=owners[np.unique(pairs)]
        print('UV positive-area overlap pairs',len(pairs),flush=True)
        if not len(pairs):break
        for oi,ob in enumerate(meshes):
            bm=bmesh.from_edit_mesh(ob.data);layer=bm.loops.layers.uv.active
            badids=set(badowners[badowners[:,0]==oi,1]);bad=[p for p in bm.faces if p.index in badids]
            area3=sum(p.calc_area() for p in bm.faces)
            def area2(p):
                q=[l[layer].uv[:] for l in p.loops]
                return abs(sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(q,q[1:]+q[:1])))/2
            scale=math.sqrt(sum(area2(p) for p in bm.faces)/max(area3,1e-12))
            for p in bad:
                repaired[ob.name].add(p.index)
                origin=p.loops[0].vert.co;edge=p.loops[1].vert.co-origin
                offset=(2+(p.index%256)*.03,(p.index//256)*.03)
                if edge.length>1e-9 and p.calc_area()>1e-12:
                    x=edge.normalized();y=p.normal.cross(x).normalized()
                    for l in p.loops:
                        rel=l.vert.co-origin;l[layer].uv=(offset[0]+rel.dot(x)*scale,offset[1]+rel.dot(y)*scale)
                else:
                    for i,l in enumerate(p.loops):l[layer].uv=(offset[0]+.0001*math.cos(2*math.pi*i/len(p.loops)),offset[1]+.0001*math.sin(2*math.pi*i/len(p.loops)))
            bmesh.update_edit_mesh(ob.data,loop_triangles=False,destructive=False)
        bpy.ops.uv.select_all(action='SELECT');bpy.ops.uv.pack_islands(udim_source='ACTIVE_UDIM',rotate=False,shape_method='CONVEX',margin_method='ADD',margin=.002)
    return {name:sorted(ids) for name,ids in repaired.items()}

def package():
    bpy.ops.wm.open_mainfile(filepath=str(v.TMP/'candidate.blend'))
    o=bpy.data.objects['PINO_C_BASE_RIG_V001'];r=bpy.data.objects['PINO_C_TRIPO_PLUS_CONTROLS_V001'];sc=bpy.context.scene
    lids=[bpy.data.objects['PinoSoftLids_'+s] for s in ['L','R']];seal=bpy.data.objects['PinoOralLiner'];meshes=[o,*lids,seal]
    v.state(o,lids);labels=np.load(v.TMP/'source.npz')['labels'];pts=v.coords(o)
    source=o.data.materials[0];mats={}
    for name in ['Pino_Skin','Pino_OralInterior','Pino_Eye_L','Pino_Eye_R','Pino_LidSkin','Pino_MuzzleSkin']:
        mat=source.copy();mat.name=name;mats[name]=mat
    o.data.materials.clear()
    for name in ['Pino_Skin','Pino_OralInterior','Pino_Eye_L','Pino_Eye_R']:o.data.materials.append(mats[name])
    oral=[]
    for p in o.data.polygons:
        c=pts[list(p.vertices)].mean(0);label=labels[p.vertices[0]]
        p.material_index=2 if label==9 else 3 if label==8 else 0
        # The head owns skin only. The independent retracting liner owns oral color.
    for ob in lids+[seal]:
        ob.data.materials.clear();ob.data.materials.append(mats['Pino_LidSkin' if ob in lids else 'Pino_OralInterior'])
    weights=[]
    for ob in meshes:
        original=[]
        for vert in ob.data.vertices:
            ww=sorted([(g.group,g.weight) for g in vert.groups],key=lambda t:t[1],reverse=True);original.append(ww)
            keep=ww[:4];total=sum(w for g,w in keep)
            for g,w in ww:
                if (g,w) in keep:ob.vertex_groups[g].add([vert.index],w/total,'REPLACE')
                else:ob.vertex_groups[g].remove([vert.index])
        weights.append({'object':ob.name,'max_source_influences':max(map(len,original)),'trimmed_vertices':sum(len(w)>4 for w in original)})
        for mod in ob.modifiers:
            if mod.type=='ARMATURE':mod.use_deform_preserve_volume=False
        attr=ob.data.attributes.new('_PINO_VERTEX_ID','FLOAT','POINT');attr.data.foreach_set('value',np.arange(len(ob.data.vertices),dtype=np.float32))
        attr=ob.data.attributes.new('_PINO_CORNER_ID','FLOAT','CORNER');attr.data.foreach_set('value',np.arange(len(ob.data.loops),dtype=np.float32))
        ob['Texture_GO']='NO — Human Pre-Texture Gate PENDING';ob['Technical_status']='HOLD';ob['UV_contract']='PinoUV_v003; no topology/UV edits downstream'
    bpy.ops.object.select_all(action='DESELECT')
    for ob in meshes:ob.select_set(True)
    bpy.context.view_layer.objects.active=o
    bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(35),island_margin=.008,area_weight=0,correct_aspect=True,scale_to_bounds=False)
    bpy.ops.uv.seams_from_islands()
    bpy.ops.uv.unwrap(method='ANGLE_BASED',margin=.006,fill_holes=True,correct_aspect=True)
    bpy.ops.object.mode_set(mode='OBJECT')
    for ob in lids:
        uv=ob.data.uv_layers.active
        for loop in ob.data.loops:
            vi=loop.vertex_index;half=vi//1625;idx=vi%1625
            uv.data[loop.index].uv=((idx%65)/64*.08+half*.09,(idx//65)/24*.04)
    bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.uv.select_all(action='SELECT')
    bpy.ops.uv.pack_islands(rotate=False,margin=.006)
    uvrepairs=repair_uv_charts(meshes)
    bpy.ops.object.mode_set(mode='OBJECT')
    topology={}
    normal_bank={};normal_meta=[]
    for ob in meshes:
        me=ob.data;me.uv_layers.active.name='PinoUV_v003'
        uv=np.array([u.uv[:] for u in me.uv_layers.active.data],dtype='<f4');faces=np.array([l.vertex_index for l in me.loops],dtype='<u4')
        topology[ob.name]={'vertices':len(me.vertices),'polygons':len(me.polygons),'loops':len(me.loops),'uv_sha256':hashlib.sha256(uv.tobytes()).hexdigest(),'corner_vertex_sha256':hashlib.sha256(faces.tobytes()).hexdigest(),'uv_min':uv.min(0).tolist(),'uv_max':uv.max(0).tolist(),'shape_keys':[k.name for k in me.shape_keys.key_blocks],'materials':[m.name for m in me.materials]}
        idx=len(normal_meta);base=np.array([n.vector[:] for n in me.corner_normals]);normal_bank[f'{idx}_base']=base;normal_bank[f'{idx}_vid']=faces
        keys=list(me.shape_keys.key_blocks)[1:];normal_meta.append({'mesh':me.name,'object':ob.name,'keys':[k.name for k in keys]})
        for ki,key in enumerate(keys):
            attr=me.attributes.get('PinoDN_'+key.name)
            if attr:dn=np.array([a.vector[:] for a in attr.data])
            else:
                temp=bpy.data.meshes.new('Morph normal scratch');temp.from_pydata([p.co[:] for p in key.data],[],[p.vertices[:] for p in me.polygons]);temp.update()
                for p in temp.polygons:p.use_smooth=True
                dn=np.array([n.vector[:] for n in temp.corner_normals])-base;bpy.data.meshes.remove(temp)
            normal_bank[f'{idx}_target{ki}']=dn
    np.savez_compressed(v.TMP/'delivery-normal-bank.npz',**normal_bank)
    (v.TMP/'delivery-normal-meta.json').write_text(json.dumps(normal_meta),encoding='utf8')
    v.state(o,lids);v.f.display(sc,480);v.f.view(sc,'3q')
    bpy.context.preferences.filepaths.save_version=0
    master=v.DEST/'pino-c-texture-ready-v003-HOLD.blend';bpy.ops.wm.save_as_mainfile(filepath=str(master),compress=True)
    # Disable the preview normal modifier for export. Morph normals are patched
    # explicitly from the saved corner-normal bank after standard skin export.
    for ob in meshes:
        for mod in ob.modifiers:
            if mod.type=='NODES':mod.show_render=False;mod.show_viewport=False
    bpy.ops.object.select_all(action='DESELECT')
    for ob in [r,*meshes]:ob.select_set(True)
    bpy.context.view_layer.objects.active=o
    glb=v.DEST/'pino-c-texture-ready-v003-HOLD.glb'
    bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',use_selection=True,export_animations=False,export_apply=False,export_normals=True,export_morph=True,export_morph_normal=False,export_skins=True,export_all_influences=False,export_attributes=True,export_extras=True,export_materials='EXPORT')
    report={'status':'HOLD','Human_Pre_Texture_Gate':'PENDING','Texture_GO':False,'master':master.name,'glb':glb.name,'topology':topology,'weights':weights,'uv_local_chart_repairs':uvrepairs,'oral_face_ids':oral,'notes':['All slots retain neutral source placeholder color. No texture generated.','Portable editing master uses LBS and four influences. Source DQ remains untouched in Rig v001.','UV is a candidate atlas, not released for texture production until gates clear.']}
    (v.OUT/'delivery-contract.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')

if __name__=='__main__':package()
