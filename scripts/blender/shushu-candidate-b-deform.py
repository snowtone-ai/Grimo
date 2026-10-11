"""Disposable anatomy rig, evaluated mesh tests and localized facial repair proof."""
import bpy, numpy as np, math, sys, json
from pathlib import Path
from collections import defaultdict
from mathutils import Vector, Matrix, Euler

sys.dont_write_bytecode = True
sys.path.insert(0,str(Path(__file__).resolve().parent))
import importlib
audit=importlib.import_module('shushu-candidate-b-audit')
ROOT,OUT,BLEND,RENDERS=audit.ROOT,audit.OUT,audit.BLEND,audit.RENDERS

def components(mesh):
    edges=defaultdict(list);p=list(range(len(mesh.polygons)))
    def find(a):
        while p[a]!=a:p[a]=p[p[a]];a=p[a]
        return a
    for poly in mesh.polygons:
        for e in poly.edge_keys:edges[tuple(sorted(e))].append(poly.index)
    for inc in edges.values():
        for b in inc[1:]:p[find(b)]=find(inc[0])
    result=defaultdict(list)
    for i in range(len(p)):result[find(i)].append(i)
    return sorted(result.values(),key=len,reverse=True)

def evaluated(obj):
    bpy.context.view_layer.update();dep=bpy.context.evaluated_depsgraph_get();ev=obj.evaluated_get(dep);m=ev.to_mesh()
    m.calc_loop_triangles();v=np.array([list(ev.matrix_world@p.co) for p in m.vertices]);t=np.array([list(p.vertices) for p in m.loop_triangles])
    ev.to_mesh_clear();return v,t

def semantic(center):
    x,y,z=center
    if z>.84 and abs(x)>.13:return 'Ear.L' if x>0 else 'Ear.R'
    if z>.57:return 'Head'
    if .28<z<.53 and abs(x)>.23:return 'Paw.L' if x>0 else 'Paw.R'
    if z<.24 and abs(x)>.07:return 'Leg.L' if x>0 else 'Leg.R'
    return 'Torso'

def clone(raw,name,clean=False):
    obj=raw.copy();obj.data=raw.data.copy();bpy.context.scene.collection.objects.link(obj);obj.name=name
    groups=components(obj.data)
    if clean:
        keep=groups[:8];ids=sorted(set(i for g in keep for face in g for i in obj.data.polygons[face].vertices));mapping={a:i for i,a in enumerate(ids)}
        verts=[obj.data.vertices[i].co[:] for i in ids];faces=[[mapping[i] for i in obj.data.polygons[f].vertices] for g in keep for f in g]
        mesh=bpy.data.meshes.new(name+'_Mesh');mesh.from_pydata(verts,[],faces);mesh.update();obj.data=mesh
    return obj

def smoothstep(a,b,x):
    t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)

def build_rig(obj):
    ad=bpy.data.armatures.new(obj.name+'_Rig');rig=bpy.data.objects.new(obj.name+'_Rig',ad);bpy.context.scene.collection.objects.link(rig)
    bpy.ops.object.select_all(action='DESELECT');rig.select_set(True);bpy.context.view_layer.objects.active=rig;bpy.ops.object.mode_set(mode='EDIT')
    def bone(name,head,tail,parent=None):
        b=ad.edit_bones.new(name);b.head=head;b.tail=tail
        if parent:b.parent=ad.edit_bones[parent]
    bone('Pelvis',(0,0,.20),(0,0,.40));bone('Head',(0,0,.47),(0,0,.75),'Pelvis')
    for side,sign in [('L',1),('R',-1)]:
        bone('Paw.'+side,(sign*.17,0,.485),(sign*.33,-.02,.34),'Pelvis')
        bone('Ear.'+side,(sign*.19,.05,.845),(sign*.28,.05,.95),'Head')
        bone('Thigh.'+side,(sign*.14,0,.20),(sign*.14,0,.11),'Pelvis')
        bone('Shin.'+side,(sign*.14,0,.11),(sign*.14,0,.04),'Thigh.'+side)
        bone('Foot.'+side,(sign*.14,0,.04),(sign*.14,-.09,.04),'Shin.'+side)
    bpy.ops.object.mode_set(mode='OBJECT')
    for name in ad.bones.keys():obj.vertex_groups.new(name=name)
    classifications={};membership={}
    for group in components(obj.data):
        ids=sorted(set(i for f in group for i in obj.data.polygons[f].vertices));center=np.mean([obj.data.vertices[i].co[:] for i in ids],axis=0)
        part=semantic(center);classifications.setdefault(part,[]).append({'faces':len(group),'vertices':len(ids),'center':center.tolist()})
        for i in ids:membership.setdefault(i,part)
    for v in obj.data.vertices:
        x,y,z=v.co;part=membership[v.index];weights={}
        if part=='Head':
            h=smoothstep(.45,.58,z);weights={'Head':h,'Pelvis':1-h}
        elif part.startswith('Ear'):
            h=smoothstep(.83,.89,z);weights={part:h,'Head':1-h}
        elif part.startswith('Paw'):
            w=smoothstep(.145,.235,abs(x));weights={part:w,'Pelvis':1-w}
        elif part.startswith('Leg'):
            side=part[-1]
            foot=1-smoothstep(.065,.10,z);thigh=smoothstep(.10,.17,z)
            weights={'Foot.'+side:foot,'Thigh.'+side:(1-foot)*thigh,'Shin.'+side:(1-foot)*(1-thigh)}
        else:
            h=.35*smoothstep(.38,.515,z);weights={'Head':h,'Pelvis':1-h}
        for name,w in weights.items():
            if w>0:obj.vertex_groups[name].add([v.index],w,'REPLACE')
    mod=obj.modifiers.new('Temporary anatomical skinning','ARMATURE');mod.object=rig;mod.use_deform_preserve_volume=True
    rig.show_in_front=True;obj['role']='Disposable controlled test geometry; not production approved'
    return rig,classifications

def reset(rig,obj):
    for b in rig.pose.bones:b.matrix_basis=Matrix.Identity(4)
    if obj.data.shape_keys:
        for key in obj.data.shape_keys.key_blocks:key.value=0
    bpy.context.view_layer.update()

def point_bone(rig,name,start,end):
    direction=Vector(end)-Vector(start)
    rest=rig.data.bones[name]
    rotation=(rest.tail_local-rest.head_local).rotation_difference(direction)
    rig.pose.bones[name].matrix=Matrix.Translation(Vector(start))@rotation.to_matrix().to_4x4()@rest.matrix_local.to_3x3().to_4x4()
    bpy.context.view_layer.update()

def support_pose(rig,depth,shift=0):
    rig.pose.bones['Pelvis'].location=(shift,-depth,0) # bone local Y is world Z
    bpy.context.view_layer.update()
    for side,sign in [('L',1),('R',-1)]:
        hip=Vector((sign*.14+shift,0,.20-depth));ankle=Vector((sign*.14,0,.04));delta=ankle-hip;d=delta.length
        l1=.09;l2=.07;a=(l1*l1-l2*l2+d*d)/(2*d);h=math.sqrt(max(0,l1*l1-a*a));axis=delta.normalized()
        perpendicular=Vector((0,-1,0));knee=hip+axis*a+perpendicular*h
        point_bone(rig,'Thigh.'+side,hip,knee);point_bone(rig,'Shin.'+side,knee,ankle)
        point_bone(rig,'Foot.'+side,ankle,ankle+Vector((0,-.09,0)))

def paw_target(rig,side,target):
    name='Paw.'+side;rest=rig.data.bones[name]
    point_bone(rig,name,rest.head_local,Vector(rest.head_local)+(Vector(target)-rest.head_local).normalized()*rest.length)

def shape(obj,name,fn):
    if obj.data.shape_keys is None:obj.shape_key_add(name='Basis')
    k=obj.shape_key_add(name=name,from_mix=False)
    for p in k.data:p.co=fn(p.co.copy())
    return k

def add_shapes(obj):
    def compression(center,radii,axis,amplitude):
        def fn(p):
            q=(np.array(p)-center)/radii;weight=math.exp(-float(q@q)*2)
            if float(q@q)>4:weight=0
            p[axis]+=amplitude*weight;return p
        return fn
    shape(obj,'CheekPressure.L',compression(np.array([.21,-.23,.59]),np.array([.095,.075,.085]),1,.025))
    shape(obj,'BellyPressure',compression(np.array([0,-.235,.32]),np.array([.13,.07,.13]),1,.027))
    shape(obj,'SupportCompression',compression(np.array([0,-.02,.18]),np.array([.17,.18,.045]),2,.018))
    def smile(p):
        x,y,z=p;q=(x/.1)**2+((y+.27)/.08)**2+((z-.59)/.045)**2
        p.z+=.012*math.exp(-q*2)*min(1,abs(x)/.04);return p
    shape(obj,'SmileSmall',smile)
    def mouth(p):
        x,y,z=p;q=(x/.055)**2+((y+.277)/.055)**2+((z-.585)/.028)**2
        p.z-=.012*math.exp(-q*2);p.y-=.002*math.exp(-q*2);return p
    shape(obj,'MouthOpenRaw',mouth)
    # Move only upper orbital skin downward: deliberately keeps underlying eye cap.
    # This is an actual failed-lid probe, never a whole-eye scale PASS.
    for side,sign in [('L',1),('R',-1)]:
        def blink(p,sign=sign):
            x,y,z=p;q=((x-sign*.139)/.065)**2+((y+.225)/.075)**2
            w=math.exp(-q*1.5)*smoothstep(.655,.69,z)*(1-smoothstep(.72,.76,z))
            p.z-=.053*w;p.y-=.012*w;return p
        shape(obj,'RawUpperLidProbe.'+side,blink)

def proxy(name,location,radius):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=radius,location=location)
    o=bpy.context.object;o.name=name;o.color=(.8,.3,.15,1);return o

def metrics(v,t,basis,base_t):
    q=v[t];b=basis[base_t]
    area=np.linalg.norm(np.cross(q[:,1]-q[:,0],q[:,2]-q[:,0]),axis=1)/2
    ba=np.linalg.norm(np.cross(b[:,1]-b[:,0],b[:,2]-b[:,0]),axis=1)/2
    lengths=np.linalg.norm(q[:,[1,2,0]]-q[:,[0,1,2]],axis=2)
    bl=np.linalg.norm(b[:,[1,2,0]]-b[:,[0,1,2]],axis=2)
    ratio=lengths/np.maximum(bl,1e-12);disp=np.linalg.norm(v-basis,axis=1)
    soles={}
    for side,sign in [('L',1),('R',-1)]:
        mask=(basis[:,2]<.012)&(basis[:,0]*sign>.04)
        soles[side]={'vertices':int(mask.sum()),'max_displacement':float(disp[mask].max()),'minimum_z':float(v[mask,2].min()),'maximum_z':float(v[mask,2].max())}
    return {'finite':bool(np.isfinite(v).all()),'changed_vertices_gt1e-6':int((disp>1e-6).sum()),'max_displacement':float(disp.max()),
            'area_ratio_min':float((area/np.maximum(ba,1e-12)).min()),'area_ratio_max':float((area/np.maximum(ba,1e-12)).max()),
            'edge_length_ratio_p01_p99':np.percentile(ratio,[1,99]).tolist(),'edge_length_ratio_min_max':[float(ratio.min()),float(ratio.max())],
            'sole_samples':soles,'minimum_z':float(v[:,2].min()),'bounds':[v.min(0).tolist(),v.max(0).tolist()]}

def main():
    bpy.ops.wm.open_mainfile(filepath=str(BLEND));raw=bpy.data.objects['CandidateB_RawFBX_Copy'];cam=bpy.context.scene.camera
    for o in list(bpy.data.objects):
        if o.name.startswith(('CandidateB_ScratchCore','CandidateB_RawSkinningProbe','TEMP_','FacialRepair_')):
            bpy.data.objects.remove(o,do_unlink=True)
    raw.hide_render=True;raw.hide_set(True)
    obj=clone(raw,'CandidateB_ScratchCore',True);obj.hide_set(False);obj.hide_render=False
    for p in obj.data.polygons:p.use_smooth=True
    rig,parts=build_rig(obj);add_shapes(obj)
    rawtest=clone(raw,'CandidateB_RawSkinningProbe');rawtest.hide_set(False);rawtest.hide_render=True
    rawrig,rawparts=build_rig(rawtest);add_shapes(rawtest)
    reset(rig,obj);reset(rawrig,rawtest)
    basis,t=evaluated(obj);rb,rt=evaluated(rawtest)
    original=np.array([v.co[:] for v in obj.data.shape_keys.key_blocks['Basis'].data])
    assert np.linalg.norm(basis-original,axis=1).max()<1e-5, 'Rest evaluation changed copied geometry'
    record={'temporary_setup':'8 largest edge-connected components retained on core scratch; all source components retained on raw control; anatomy weights are diagnostic, not final',
            'core_vertices':len(basis),'core_triangles':len(t),'parts':parts,'raw_parts':rawparts,'poses':{}}
    # Same neutral camera conditions as source audit.
    tests=[('neutral',{}),('head-yaw-left',{'head':(0,0,20)}),('head-yaw-right',{'head':(0,0,-20)}),
           ('head-down',{'head':(15,0,0)}),('head-roll',{'head':(0,12,0)}),
           ('paw-left-offer',{'pawL':(-32,0,-12)}),('paw-right-offer',{'pawR':(-32,0,12)}),
           ('both-paws-hold',{'targetL':(.095,-.205,.365),'targetR':(-.095,-.205,.365)}),
           ('weight-shift',{'depth':.012,'shift':.012}),('low-squat',{'depth':.035}),('toward-sitting',{'depth':.095}),
           ('cheek-pressure',{'shape':{'CheekPressure.L':1}}),('belly-pressure',{'shape':{'BellyPressure':1}}),
           ('support-compression',{'depth':.035,'shape':{'SupportCompression':1}}),
           ('ear-left',{'earL':(0,0,10)}),('ear-right',{'earR':(0,0,-10)}),
           ('small-smile',{'shape':{'SmileSmall':1}}),('mouth-open-raw',{'shape':{'MouthOpenRaw':1}}),
           ('raw-lid-left-half',{'shape':{'RawUpperLidProbe.L':.5}}),('raw-lid-left-closed',{'shape':{'RawUpperLidProbe.L':1}}),
           ('raw-lid-right-closed',{'shape':{'RawUpperLidProbe.R':1}}),
           ('occupied-paw-head-touch',{'pawL':(-30,0,-16),'head':(10,0,12),'shape':{'CheekPressure.L':1}}),
           ('food-approach',{'head':(7,0,0),'shape':{'MouthOpenRaw':.7}}),
           ('gift-low-offer',{'targetL':(.095,-.22,.375),'targetR':(-.095,-.22,.375)})]
    keymap={'head':'Head','pawL':'Paw.L','pawR':'Paw.R','earL':'Ear.L','earR':'Ear.R'}
    proxies=[]
    for label,spec in tests:
        reset(rig,obj);reset(rawrig,rawtest)
        for target,mesh in [(rig,obj),(rawrig,rawtest)]:
            if 'depth' in spec:support_pose(target,spec['depth'],spec.get('shift',0))
            for key,bone in keymap.items():
                if key in spec:
                    b=target.pose.bones[bone];b.rotation_mode='QUATERNION'
                    rest=target.data.bones[bone].matrix_local.to_3x3()
                    world=Euler([math.radians(n) for n in spec[key]],'XYZ').to_matrix()
                    b.rotation_quaternion=(rest.inverted()@world@rest).to_quaternion()
            for key,value in spec.get('shape',{}).items():mesh.data.shape_keys.key_blocks[key].value=value
            for side in ['L','R']:
                if 'target'+side in spec:paw_target(target,side,spec['target'+side])
        v,_=evaluated(obj);rv,_=evaluated(rawtest)
        record['poses'][label]={'parameters':spec,'core':metrics(v,t,basis,t),'raw':metrics(rv,rt,rb,rt)}
        if label in ['neutral','head-down','head-yaw-left','paw-left-offer','both-paws-hold','toward-sitting','low-squat']:
            record['poses'][label]['core']['self_intersections']=audit.intersection_pairs(v,t)
        for o in proxies:bpy.data.objects.remove(o,do_unlink=True)
        proxies=[]
        if label in ['both-paws-hold','gift-low-offer','occupied-paw-head-touch']:
            # Bounded prop below face, measured against actual evaluated surface.
            loc=(0,-.265,.35) if label!='occupied-paw-head-touch' else (.28,-.12,.38)
            radius=.078 if label!='occupied-paw-head-touch' else .025
            proxies=[proxy('TEMP_HeldObject',loc,radius)]
            nearest={}
            for side,sign in [('L',1),('R',-1)]:
                mask=(basis[:,0]*sign>.27)&(basis[:,2]>.27)&(basis[:,2]<.43)
                distance=np.linalg.norm(v[mask]-np.array(loc),axis=1)-radius
                nearest[side]={'nearest_sphere_surface_absolute_distance':float(np.abs(distance).min()),'minimum_sphere_signed_distance':float(distance.min())}
            torso=(np.abs(basis[:,0])<.18)&(basis[:,2]>.25)&(basis[:,2]<.43)
            record['poses'][label]['proxy']={'center':loc,'radius':radius,'paws':nearest,'minimum_torso_vertex_distance_minus_radius':float((np.linalg.norm(v[torso]-np.array(loc),axis=1)-radius).min()),'limitation':'vertex-to-sphere samples, not complete triangle collision or product holding semantics'}
        if label=='food-approach':proxies=[proxy('TEMP_Food',(0,-.335,.585),.018)]
        if label in ['ear-left','ear-right','head-roll']:
            headmatrix=rig.pose.bones['Head'].matrix@rig.data.bones['Head'].matrix_local.inverted()
            crown=proxy('TEMP_CrownEnvelope',headmatrix@Vector((0,-.01,.955)),.052);crown.scale=(2,1,.35);proxies=[crown]
        for direction,suffix in [((0,-1,0),'front'),((1,-1,.12),'threequarter')]:
            audit.render(cam,'pose-'+label+'-'+suffix,direction)
        if label in ['head-down','toward-sitting','low-squat','paw-left-offer','food-approach']:
            audit.render(cam,'pose-'+label+'-side',(1,0,0))
        if label.startswith('raw-lid') or label in ['mouth-open-raw','small-smile']:
            obj.hide_render=True;rawtest.hide_render=False
            audit.render(cam,'detail-'+label,(0,-1,0),target=(0,-.16,.66),scale=.44)
            rawtest.hide_render=True;obj.hide_render=False
        # Corresponding original topology poses expose any artifacts removed by core cleanup.
        if label in ['head-down','paw-left-offer','toward-sitting','raw-lid-left-closed']:
            obj.hide_render=True;rawtest.hide_render=False
            audit.render(cam,'raw-pose-'+label,(1,-1,.12))
            rawtest.hide_render=True;obj.hide_render=False
    for o in proxies:bpy.data.objects.remove(o,do_unlink=True)
    reset(rig,obj);reset(rawrig,rawtest)
    returned,_=evaluated(obj);record['neutral_return_max_vertex_error']=float(np.linalg.norm(returned-basis,axis=1).max())
    audit.write('deformation-measurements.json',record)
    # Baked keyframes for representative head/paw/settle and exported morph proof.
    for frame,depth in [(1,0),(12,.035),(24,0)]:
        reset(rig,obj);support_pose(rig,depth)
        for name,angles in [('Head',(0,0,15 if frame==12 else 0)),('Paw.L',(-25 if frame==12 else 0,0,0))]:
            rest=rig.data.bones[name].matrix_local.to_3x3();b=rig.pose.bones[name];b.rotation_mode='QUATERNION'
            b.rotation_quaternion=(rest.inverted()@Euler([math.radians(a) for a in angles],'XYZ').to_matrix()@rest).to_quaternion()
        for b in rig.pose.bones:
            b.keyframe_insert('location',frame=frame);b.keyframe_insert('rotation_quaternion' if b.rotation_mode=='QUATERNION' else 'rotation_euler',frame=frame);b.keyframe_insert('scale',frame=frame)
        k=obj.data.shape_keys.key_blocks['BellyPressure'];k.value=1 if frame==12 else 0;k.keyframe_insert('value',frame=frame)
    bpy.context.scene.frame_start=1;bpy.context.scene.frame_end=24;bpy.context.scene.frame_set(1)
    rawtest.hide_set(True);rig.select_set(True);obj.select_set(True);bpy.context.view_layer.objects.active=obj
    bpy.ops.wm.save_as_mainfile(filepath=str(BLEND))
    print('DEFORMATION_COMPLETE',len(tests),'poses',len(basis),'core vertices')

if __name__=='__main__':main()
