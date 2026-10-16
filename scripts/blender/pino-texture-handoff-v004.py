"""Pino pre-texture structure probes and reversible v004 authoring.

Never writes v001-v003. Run in background Blender 5.2 from any directory.
"""
import bpy, sys, json, math, hashlib, importlib.util
from pathlib import Path
import numpy as np
from mathutils import Vector, Matrix, Quaternion
from mathutils.bvhtree import BVHTree
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
AS = ROOT/'assets/grimo/production/pino/candidate-c'
OUT = ROOT/'docs/production/pino/evidence/texture-handoff-v004'
DEST = AS/'texture-handoff-v004'
TMP = ROOT/'artifacts/pino-texture-v004'
for p in (OUT, DEST, TMP): p.mkdir(parents=True, exist_ok=True)
def module(name, path):
    sp=importlib.util.spec_from_file_location(name,ROOT/path)
    m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
v3=module('v3','scripts/blender/pino-texture-ready-v003.py')
def dump(name, data):
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def coords(o): return np.array([v.co[:] for v in o.data.vertices])
def load(candidate=False):
    path=DEST/'pino-c-texture-handoff-v004.blend' if candidate else AS/'texture-ready-v003/pino-c-texture-ready-v003-HOLD.blend'
    bpy.ops.wm.open_mainfile(filepath=str(path))
    return bpy.data.objects['PINO_C_BASE_RIG_V001'],bpy.data.objects['PINO_C_TRIPO_PLUS_CONTROLS_V001'],bpy.context.scene
def labels(): return np.load(ROOT/'docs/production/pino/evidence/rig-v001/reference-arrays.npz')['components']
def reset(r):
    for p in r.pose.bones:
        p.matrix_basis=Matrix.Identity(4)
        for c in p.constraints: c.influence=0
    for o in bpy.context.scene.objects:
        if o.type=='MESH' and o.data.shape_keys:
            for k in o.data.shape_keys.key_blocks:k.value=0
    bpy.context.view_layer.update()
def rot(r,name,axis,degrees):
    p=r.pose.bones[name];p.rotation_mode='QUATERNION';rest=p.bone.matrix_local.to_quaternion()
    p.rotation_quaternion=rest.inverted()@Quaternion(Vector(axis),math.radians(degrees))@rest
def move(r,name,delta):
    p=r.pose.bones[name];p.location=p.bone.matrix_local.to_3x3().inverted()@Vector(delta)
def weights_replace(o, ids, bank):
    ids=list(map(int,ids))
    for g in o.vertex_groups:g.remove(ids)
    for i,ww in zip(ids,bank):
        ww=sorted([(n,w) for n,w in ww.items() if w>1e-8],key=lambda a:-a[1])[:4]
        total=sum(w for n,w in ww)
        for n,w in ww:
            g=o.vertex_groups.get(n) or o.vertex_groups.new(name=n);g.add([i],float(w/total),'REPLACE')
def body_weights(o):
    V=coords(o);L=labels();x,y,z=V.T;ids=np.where((L==0)&(z<.5))[0];bank=[]
    for i in ids:
        side='Left' if x[i]>=0 else 'Right'
        # The torso stays torso-owned. The proximal sleeve uses Arm rather than
        # the distal Hand, preventing distal IK from pulling a sheet of chest.
        wa=float(v3.f.smooth(.202,.285,abs(x[i]))*v3.f.smooth(.20,.27,z[i])*(1-v3.f.smooth(.414,.48,z[i])))
        a=np.array((.17,-.146,.392));d=np.array((.16,-.074,-.079));p=np.array((abs(x[i]),y[i],z[i]));t=np.clip((p-a)@d/(d@d),0,1)
        radius=float(np.linalg.norm(p-a-t*d))
        wa*=float(1-v3.f.smooth(.052,.082,radius))
        wh=float(v3.f.smooth(.43,.5,z[i]));wf=float((1-v3.f.smooth(.055,.165,z[i]))*v3.f.smooth(.055,.105,abs(x[i])));ws=float(v3.f.smooth(.19,.40,z[i]))
        wl=0.;shank=0.
        ww={'mixamorig:Head':wh,'mixamorig:Hips':(1-wh)*(1-wf-wl)*(1-ws),
            'mixamorig:Spine2':(1-wh)*(1-wf-wl)*ws,f'mixamorig:{side}Foot':(1-wh)*wf,
            f'mixamorig:{side}UpLeg':(1-wh)*wl*(1-shank),f'mixamorig:{side}Leg':(1-wh)*wl*shank}
        ww={n:w*(1-wa) for n,w in ww.items()}
        ww[f'mixamorig:{side}Arm']=wa
        bank.append(ww)
    weights_replace(o,ids,bank)
    # A smooth three-bone field replaces the old piecewise two-bone tail field.
    ids=np.where(np.isin(L,[2,5]))[0];bank=[]
    for i in ids:
        t=np.clip((V[i,1]-.075)/.09,0,4);cent=int(round(t));lo=max(0,min(2,cent-1));js=np.arange(lo,lo+3)
        w=np.exp(-((t-js)/.72)**2);w/=sum(w);a=float(v3.f.smooth(-.015,.075,V[i,1]))
        ww={f'PinoTail{j+1:02d}':a*val for j,val in zip(js,w)};ww['mixamorig:Hips']=1-a;bank.append(ww)
    weights_replace(o,ids,bank)
def setup_support_bones(r):
    bpy.context.view_layer.objects.active=r;r.select_set(True);bpy.ops.object.mode_set(mode='EDIT')
    for side,sg in [('Left',1),('Right',-1)]:
        up=r.data.edit_bones['mixamorig:'+side+'UpLeg'];leg=r.data.edit_bones['mixamorig:'+side+'Leg']
        up.head=(sg*.115,-.090,.205);up.tail=(sg*.138,-.105,.12);leg.head=up.tail
    bpy.ops.object.mode_set(mode='OBJECT')

def evaluated(o):return v3.f.evaluated(o)
def body_pose(o,r,kind,s):
    reset(r);V=coords(o);L=labels()
    if kind=='contact':
        for side,sg in [('Left',1),('Right',-1)]:
            move(r,'mixamorig:'+side+'Shoulder',(-sg*.051955395507812495*s,-.073*s,0))
            rot(r,'mixamorig:'+side+'Arm',(0,0,1),-sg*95*s)
    elif kind=='rest':
        rot(r,'mixamorig:Hips',(1,0,0),-14*s);move(r,'mixamorig:Hips',(0,.025*s,-.0765*s))
        rot(r,'mixamorig:Neck',(1,0,0),10*s)
        bpy.context.view_layer.update()
        for side in ['Left','Right']:
            foot=r.data.bones['mixamorig:'+side+'Foot'];ankle=foot.head_local+Vector((0,-.040*s,0))
            up=r.pose.bones['mixamorig:'+side+'UpLeg'];leg=r.pose.bones['mixamorig:'+side+'Leg'];hip=up.head.copy()
            d=ankle-hip;dist=d.length;direction=d.normalized();l1=up.bone.length;l2=leg.bone.length
            assert abs(l1-l2)<dist<l1+l2,(side,dist,l1,l2)
            along=(l1*l1-l2*l2+dist*dist)/(2*dist);height=math.sqrt(max(0,l1*l1-along*along))
            pole=Vector((0,-1,0));pole=(pole-direction*pole.dot(direction)).normalized();knee=hip+direction*along+pole*height
            for p,a,b in [(up,hip,knee),(leg,knee,ankle)]:
                q=(p.bone.tail_local-p.bone.head_local).rotation_difference(b-a)
                m=(q.to_matrix()@p.bone.matrix_local.to_3x3()).to_4x4();m.translation=a;p.matrix=m;bpy.context.view_layer.update()
            m=foot.matrix_local.copy();m.translation=ankle;r.pose.bones[foot.name].matrix=m;bpy.context.view_layer.update()
        rot(r,'PinoTail01',(1,0,0),30*s);move(r,'PinoTail01',(0,0,.056*s))
    elif kind=='tail':
        for j in range(5):rot(r,f'PinoTail{j+1:02d}',(0,0,1),9*s)
    bpy.context.view_layer.update()
def render(sc,label,face=False):
    v3.f.display(sc,400)
    for view in ['front','side','3q']:
        v3.f.view(sc,view,target=(0,-.16,.64) if face else (0,-.015,.47),scale=.55 if face else 1.32)
        v3.f.render(sc,TMP/(label+'-'+view+'.png'))
def facial_state(o,c=0,l=0,bL=0,bR=0):
    """Stylized continuous squint; legacy rolling lid shapes remain unused.

    Neutral eye geometry is untouched. The closed state is a narrow arched eye
    surface, not a disappearing eye followed by an external lid plate.
    """
    lids=[bpy.data.objects['PinoSoftLids_'+s] for s in ['L','R']]
    v3.state(o,lids,c,l,0,0)
    for side,b in zip(['L','R'],[bL,bR]):
        for k in list(bpy.data.objects['PinoSoftLids_'+side].data.shape_keys.key_blocks)[1:]:k.value=0
        o.data.shape_keys.key_blocks['PinoSquint_'+side].value=b
        o.data.shape_keys.key_blocks['PinoEyeRetract_'+side].value=0
        o.data.shape_keys.key_blocks['PinoSkinClose_'+side].value=0
    bpy.context.view_layer.update()

def renew_normals(ob):
    for m in list(ob.modifiers):
        if m.type=='NODES':ob.modifiers.remove(m)
    for a in list(ob.data.attributes):
        if a.name.startswith('PinoDN_') or a.name=='PinoCanonicalCornerNormal':ob.data.attributes.remove(a)
    v3.dynamic_normals(ob)
def eye_squint(o):
    V=coords(o);L=labels()
    for side,comp in [('L',9),('R',8)]:
        ep=V[L==comp];c=(ep.min(0)+ep.max(0))/2;out=np.array((.46 if side=='L' else -.46,-.888,0));out/=np.linalg.norm(out);tan=np.array((-out[1],out[0],0));u=(V-c)@tan
        ax=max(abs((ep-c)@tan));key=o.shape_key_add(name='PinoSquint_'+side,from_mix=False)
        for i in np.where(L==comp)[0]:key.data[int(i)].co.z=c[2]+.008*(1-(u[i]/ax)**2)+(V[i,2]-c[2])*.025
def skin_matrices(o,r):
    bpy.context.view_layer.update();N=len(o.data.vertices);m=np.zeros((N,4,4))
    transforms={g.index:np.array(o.matrix_world.inverted()@r.matrix_world@r.pose.bones[g.name].matrix@r.data.bones[g.name].matrix_local.inverted()@r.matrix_world.inverted()@o.matrix_world) for g in o.vertex_groups if g.name in r.pose.bones}
    for v in o.data.vertices:
        for g in v.groups:
            if g.group in transforms:m[v.index]+=transforms[g.group]*g.weight
    return m
def static_normals(o,points):
    temp=bpy.data.meshes.new('V4 normal scratch');temp.from_pydata(points.tolist(),[],[p.vertices[:] for p in o.data.polygons]);temp.update()
    for p in temp.polygons:p.use_smooth=True
    n=np.array([v.vector[:] for v in temp.corner_normals]);bpy.data.meshes.remove(temp);return n
BODY_KEYS=[('contact',.5),('contact',1),('rest',.25),('rest',.5),('rest',.75),('rest',1),('tail',-1),('tail',1)]
def body_key(kind,s):return f'V4_{kind}_{s:+.2f}'
def normal_correctives(o,r):
    V=coords(o);L=labels();me=o.data;loops=np.array([l.vertex_index for l in me.loops]);base=np.array([n.vector[:] for n in me.corner_normals]);records=[]
    for kind,s in BODY_KEYS:
        body_pose(o,r,kind,s);M=skin_matrices(o,r);actual=evaluated(o)
        modifier=next(m for m in o.modifiers if m.type=='ARMATURE');modifier.use_deform_preserve_volume=True
        target=evaluated(o);modifier.use_deform_preserve_volume=False
        if kind=='rest':
            # Pose-only compliant contact sculpt for the central posterior web.
            # Feet stay pinned. This reshapes compressed tissue, not the rest mesh.
            q=target[:,2].copy();w=(L==0)*(1-v3.f.smooth(.15,.24,V[:,2]))
            target[:,2]+=w*(.5*(q+np.sqrt(q*q+.002**2))-q)
        delta=np.linalg.solve(M[:,:3,:3],(target-actual)[:,:,None])[:,:,0]
        k=o.shape_key_add(name=body_key(kind,s),from_mix=False)
        for d,p in zip(k.data,V+delta):d.co=p
        # Correct normals from the actual posed surface, including weight-field
        # derivatives. Only displaced body/tail corners are replaced.
        desired=static_normals(o,target);pre=np.linalg.solve(M[loops,:3,:3],desired[:,:,None])[:,:,0]
        pre/=np.maximum(np.linalg.norm(pre,axis=1),1e-20)[:,None]
        active=(L==0)&(V[:,2]<.5)|np.isin(L,[2,5]);changed=(np.linalg.norm(target-V,axis=1)>1e-6)&active
        mask=np.repeat([any(changed[i] for i in p.vertices) for p in me.polygons],[p.loop_total for p in me.polygons])
        a=me.attributes.new('PinoDN_'+k.name,'FLOAT_VECTOR','CORNER');a.data.foreach_set('vector',((pre-base)*mask[:,None]).ravel())
        records.append(dict(kind=kind,s=s,max_volume_delta=float(np.linalg.norm(delta,axis=1).max()),normal_corners=int(mask.sum())))
    reset(r)
    # Rebuild the existing node controller using saved face fields plus the new
    # local body fields. Canonical rest normals remain byte-for-byte unchanged.
    bank={k.name:np.array([x.vector[:] for x in me.attributes['PinoDN_'+k.name].data]) for k in list(me.shape_keys.key_blocks)[1:]}
    for m in list(o.modifiers):
        if m.type=='NODES':o.modifiers.remove(m)
    for a in list(me.attributes):
        if a.name.startswith('PinoDN_') or a.name=='PinoCanonicalCornerNormal':me.attributes.remove(a)
    v3.normal_controller(o,base,bank);dump('corrective-authoring.json',records)
def refresh_preview_normals(o,r):
    """Blender FREE normals are static: preview the actual glTF skin-normal math.

    Call after direct pose/key edits. This does not modify portable target fields.
    PlayCanvas uses the embedded NORMAL morphs automatically, without this bridge.
    """
    for ob in bpy.context.scene.objects:
        if ob.type!='MESH' or not ob.data.shape_keys or 'PinoCanonicalCornerNormal' not in ob.data.attributes:continue
        me=ob.data;n=len(me.loops);base=np.empty(n*3);me.attributes['PinoCanonicalCornerNormal'].data.foreach_get('vector',base);base=base.reshape(-1,3)
        for k in list(me.shape_keys.key_blocks)[1:]:
            if k.value and 'PinoDN_'+k.name in me.attributes:
                dn=np.empty(n*3);me.attributes['PinoDN_'+k.name].data.foreach_get('vector',dn);base+=k.value*dn.reshape(-1,3)
        loops=np.array([l.vertex_index for l in me.loops]);M=skin_matrices(ob,r)
        actual=np.einsum('nij,nj->ni',M[loops,:3,:3],base);actual/=np.maximum(np.linalg.norm(actual,axis=1),1e-20)[:,None]
        attr=me.attributes.get('V4PreviewNormal') or me.attributes.new('V4PreviewNormal','FLOAT_VECTOR','CORNER');attr.data.foreach_set('vector',actual.ravel())
        for m in ob.modifiers:
            if m.type=='NODES' and m.name!='V4 glTF normal preview':m.show_viewport=False;m.show_render=False
        if not ob.modifiers.get('V4 glTF normal preview'):
            group=bpy.data.node_groups.new('V4 explicit glTF normal preview','GeometryNodeTree');group.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry');group.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry')
            nodes=group.nodes;links=group.links;inp=nodes.new('NodeGroupInput');out=nodes.new('NodeGroupOutput');setn=nodes.new('GeometryNodeSetMeshNormal');setn.mode='FREE';setn.domain='CORNER'
            get=nodes.new('GeometryNodeInputNamedAttribute');get.data_type='FLOAT_VECTOR';get.inputs['Name'].default_value='V4PreviewNormal'
            links.new(inp.outputs['Geometry'],setn.inputs['Mesh']);links.new(get.outputs['Attribute'],setn.inputs['Custom Normal']);links.new(setn.outputs['Mesh'],out.inputs['Geometry'])
            ob.modifiers.new('V4 glTF normal preview','NODES').node_group=group
        me.update()
    bpy.context.view_layer.update()
def body_state(o,r,kind='neutral',s=0,c=0,l=0,bL=0,bR=0,preview=True):
    body_pose(o,r,kind,s)
    facial_state(o,c,l,bL,bR)
    if kind=='tail':
        name=body_key(kind,1 if s>=0 else -1)
        if name in o.data.shape_keys.key_blocks:o.data.shape_keys.key_blocks[name].value=abs(s)
    elif kind in ['contact','rest']:
        for center in ([.25,.5,.75,1] if kind=='rest' else [.5,1]):
            name=body_key(kind,center)
            if name in o.data.shape_keys.key_blocks:o.data.shape_keys.key_blocks[name].value=max(0,1-abs(s-center)*(4 if kind=='rest' else 2))
    bpy.context.view_layer.update()
    if preview:refresh_preview_normals(o,r)
def build():
    o,r,sc=load();reset(r);body_weights(o);setup_support_bones(r);eye_squint(o);renew_normals(o);normal_correctives(o,r)
    for p in r.pose.bones:
        for c in list(p.constraints):p.constraints.remove(c)
    for ob in [o,*[bpy.data.objects['PinoSoftLids_'+s] for s in ['L','R']],bpy.data.objects['PinoOralLiner']]:
        ob['Texture_GO']='Human Pre-Texture Gate PENDING';ob['UV_contract']='PinoUV_v003 unchanged in v004';ob['v004_geometry_policy']='Basis/topology/UV/material ownership retained; pose-only repair'
    reset(r);refresh_preview_normals(o,r);bpy.context.preferences.filepaths.save_version=0
    bpy.ops.wm.save_as_mainfile(filepath=str(DEST/'pino-c-texture-handoff-v004.blend'),compress=True)
    for kind,s in [('contact',.5),('contact',1),('rest',.5),('rest',1),('tail',1),('tail',-1)]:
        body_state(o,r,kind,s);render(sc,f'candidate-{kind}-{s}')
if __name__=='__main__':
    if '--build' in sys.argv:build()
