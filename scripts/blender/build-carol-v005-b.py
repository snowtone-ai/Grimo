"""Carol B experiment: deform the historical binary, retain its paint and UVs.
No zero-based geometry, remesh, rigging, texture repaint or production export.
"""
import bpy, numpy as np, math, json, hashlib, os
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/carol/evidence/hero-geometry-v005'
DEST=ROOT/'assets/grimo/production/carol/blender'
REVIEW=ROOT/'artifacts/carol-v005/ab'
bpy.ops.wm.read_factory_settings(use_empty=True)
SOURCE=ROOT/'assets/grimo/source/carol/historical/carol-15bfa8e-reference.glb'
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()=='0871f077abadedb716bdfad5cc57b28e36803da1c868ce23d61ded38a5d2fc21'
bpy.ops.import_scene.gltf(filepath=str(SOURCE));bpy.context.view_layer.update()
bpy.context.preferences.filepaths.save_version=0

# A continuous 2-D cage levels the old angled portrait. Values are source pixels
# and approved front pixels. Depth is authored separately, never inferred from UV.
pairs=[((314,8),(610,137)),((184,64),(337,262)),((96,181),(145,576)),
 ((116,306),(166,896)),((177,365),(326,1020)),((270,380),(453,1090)),
 ((416,376),(819,1090)),((521,334),(1080,973)),((537,267),(1100,802)),
 ((508,150),(1000,482)),((427,51),(848,211)),
 ((375,250),(503,737)),((474,216),(814,737)),
 ((431,242),(653,745)),((431,265),(654,824)),((430,302),(650,899)),
 ((337,264),(404,802)),((512,222),(914,778)),((403,182),(646,592)),
 ((304,246),(362,679)),((519,186),(966,682)),
 ((218,172),(356,458)),((361,137),(706,477)),((314,67),(624,296)),
 ((184,287),(194,621)),((443,322),(646,963)),((302,332),(312,922))]
src=np.array([[((u-337)*.007),(394-v)*.007] for (u,v),_ in pairs])
dst=np.array([[(u-645)/325,(1110-v)/325] for _,(u,v) in pairs])
def radial(r2): return r2*np.log(np.maximum(r2,1e-12))
K=radial(((src[:,None]-src[None,:])**2).sum(2)); P=np.c_[np.ones(len(src)),src]
L=np.block([[K+np.eye(len(src))*.08,P],[P.T,np.zeros((3,3))]])
W=np.linalg.solve(L,np.r_[dst,np.zeros((3,2))])
def cage(q):
    # Keep the actual painted face undistorted; blend its leveling transform into
    # the outer body. Dense landmark TPS produced a sheared face in trials 1/2.
    center=np.array([.607,1.127]); angle=math.radians(-18.96)
    rot=np.array([[math.cos(angle),-math.sin(angle)],[math.sin(angle),math.cos(angle)]])
    face=(q-center)@rot.T*1.306+np.array([.025,1.147])
    outer=np.c_[radial(((q[:,None]-src[None,:])**2).sum(2)),np.ones(len(q)),q]@W
    r=np.sqrt((((q-center)/np.array([.83,.63]))**2).sum(1))
    w=1-np.clip((r-.80)/.45,0,1);w=w*w*(3-2*w)
    return outer*(1-w[:,None])+face*w[:,None]
def uvhash(o):
    a=np.empty(len(o.data.uv_layers[0].data)*2,dtype=np.float32)
    o.data.uv_layers[0].data.foreach_get('uv',a)
    return hashlib.sha256(a.tobytes()).hexdigest()
report={'method':'historical vertex deformation; original topology, UVs, materials retained',
 'status':'B trial; not Human approved; neutral only; no production GLB',
 'source_sha256':'0871f077abadedb716bdfad5cc57b28e36803da1c868ce23d61ded38a5d2fc21',
 'iteration':4,'front_cage_pairs_source_and_approved_pixels':pairs,
 'field':'regularized thin-plate cage outside face, smooth affine leveling inside; piecewise shared depth; intact ear/motif transforms',
 'excluded':['Atmosphere00..10','ReferenceContour (retained hidden)'],
 'objects':[]}
for ob in list(bpy.context.scene.objects):
    if ob.type!='MESH':continue
    if ob.name.startswith('Atmosphere'):
        # Original remains intact in historical-import.blend and source binary.
        bpy.data.objects.remove(ob,do_unlink=True);continue
    if ob.name=='ReferenceContour':
        ob.hide_render=True;ob.hide_viewport=True;ob['B_excluded']='old silhouette outline intersects expanded side; source preserved';continue
    before=uvhash(ob); count=len(ob.data.vertices)
    M=ob.matrix_world.copy(); inv=M.inverted()
    base=np.array([M@v.co for v in ob.data.vertices]); lo=base.min(0);hi=base.max(0)
    def deform(v):
        a=np.array(v); q=cage(a[:,[0,2]]); out=np.c_[q[:,0],a[:,1],q[:,1]]
        n=ob.name
        if n in ['BodyWool','ReferenceContour']:
            t=np.clip((a[:,1]+.87)/1.13,0,1)
            out[:,1]=-1.30+t*3.30
            out[:,0]*=1-.15*t
            out[:,2]=.12+(out[:,2]-.12)*(1-.25*t)
        elif n=='HeadWool':out[:,1]=-1.93+(a[:,1]+1.2812)*.95
        elif n=='Face':out[:,1]=-2.06+(a[:,1]+1.265)*.9
        elif n.startswith('EarOuter'):
            left=n.endswith('L'); center=np.array([(-1.19 if left else 1.19),-1.50,1.20])
            # Preserve original ear UVs and bowl topology; level its painted pose.
            p=a-(lo+hi)/2; ang=math.radians(-18)
            xx=p[:,0]*math.cos(ang)-p[:,2]*math.sin(ang)
            zz=p[:,0]*math.sin(ang)+p[:,2]*math.cos(ang)
            out=np.c_[xx, p[:,1],zz]
            out[:,0]*=.90/(xx.max()-xx.min()); out[:,2]*=.49/(zz.max()-zz.min())
            out+=center
        elif n=='TailWool':
            out=(a-(lo+hi)/2)*np.array([1.2,2.1,1.35])+np.array([0,2.05,1.60])
        elif n in ['Moon','CrownStar','TopStar','WoolStar','ChestStar','LowerStar']:
            targets={'Moon':(356,458,.64,.71,-1.69),'CrownStar':(706,477,.35,.34,-1.99),
             'TopStar':(624,296,.37,.35,-1.57),'WoolStar':(194,621,.29,.32,-1.50),
             'ChestStar':(646,963,.26,.26,-1.63),'LowerStar':(312,922,.24,.25,-1.58)}
            u,v,w,h,y=targets[n]; out=a-(lo+hi)/2
            out*=np.array([w/(hi[0]-lo[0]),.7,h/(hi[2]-lo[2])]);out+=np.array([(u-645)/325,y,(1110-v)/325])
        part_out=out.copy()
        # Shared field preserves registration across layered original surfaces.
        # Original opaque paint has regions excluded from source-pigment transfer;
        # these are not established to be transparent alpha holes.
        out=np.c_[q[:,0],np.where(a[:,1]<=-.80,-1.65+(a[:,1]+.80)*.80,
                    -1.65+(a[:,1]+.80)*(3.60/1.0613)),q[:,1]]
        t=np.clip((out[:,1]+1.65)/3.6,0,1)
        out[:,0]*=1-.12*t
        out[:,2]=.10+(out[:,2]-.10)*(1-.20*t)
        if n=='TailWool':out=(a-(lo+hi)/2)*np.array([1.2,2.1,1.35])+np.array([0,2.08,1.60])
        if n.startswith('EarOuter') or n in ['Moon','CrownStar','TopStar','WoolStar','ChestStar','LowerStar']:out=part_out
        return out
    # Deform all shape-key coordinate sets consistently, leave expressions neutral.
    if ob.data.shape_keys:
        for key in ob.data.shape_keys.key_blocks:
            arr=np.array([M@p.co for p in key.data]); new=deform(arr)
            for p,co in zip(key.data,new):p.co=inv@Vector(co)
            key.value=0
    else:
        new=deform(base)
        for p,co in zip(ob.data.vertices,new):p.co=inv@Vector(co)
    ob.data.update();ob['construction']='B historical deformation; original UV/topology/paint'
    report['objects'].append({'name':ob.name,'vertices':count,'uv_before':before,'uv_after':uvhash(ob),'uv_preserved':before==uvhash(ob)})

SC=bpy.context.scene;SC['status']=report['status']
SC.render.engine='CYCLES';SC.cycles.samples=12;SC.cycles.use_denoising=True
SC.render.resolution_x=900;SC.render.resolution_y=900;SC.render.resolution_percentage=100
SC.render.image_settings.file_format='PNG';SC.render.image_settings.color_mode='RGBA';SC.render.film_transparent=True
SC.view_settings.view_transform='Standard';SC.world=bpy.data.worlds.new('B studio');SC.world.use_nodes=True
SC.world.node_tree.nodes['Background'].inputs[1].default_value=.5
for name,pos,power in [('Key',(-4,-5,7),600),('Fill',(4,-3,4),350)]:
    d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=5
    o=bpy.data.objects.new(name,d);SC.collection.objects.link(o);o.location=pos;o.rotation_euler=(Vector((0,0,1.5))-o.location).to_track_quat('-Z','Y').to_euler()
cams={}
for name,pos,target in [('front',(0,-12,1.5),(0,0,1.5)),('side',(12,0,1.5),(0,0,1.5)),('back',(0,12,1.5),(0,0,1.5)),('top',(0,0,14),(0,0,0)),('three-quarter',(-8,-10,6),(0,0,1.5))]:
    d=bpy.data.cameras.new('Review_'+name);o=bpy.data.objects.new('Review_'+name,d);SC.collection.objects.link(o);o.location=pos;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.type='ORTHO';d.ortho_scale=5.8;cams[name]=o
SC.camera=cams['front']
bpy.ops.wm.save_as_mainfile(filepath=str(DEST/'carol-b-v005.blend'))
bpy.ops.object.select_all(action='DESELECT')
for o in SC.objects:
    if o.type=='MESH' and not o.hide_render:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(REVIEW/'carol-b.preview.glb'),use_selection=True,export_animations=False,export_cameras=False,export_lights=False)
(OUT/'b-deformation-report.json').write_text(json.dumps(report,indent=2),encoding='utf8')
folder=OUT/'iterations/b-04';folder.mkdir(parents=True,exist_ok=True)
for view,cam in cams.items():
    SC.camera=cam;SC.render.filepath=str(folder/(view+'.png'));bpy.ops.render.render(write_still=True)
print('B COMPLETE, all UV unchanged:',all(x['uv_preserved'] for x in report['objects']))
