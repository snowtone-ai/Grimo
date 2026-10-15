"""Four actual deformation trials, solely from a Human-selected original Master.

Diagnostics only: no final rig, product motion, UV, texture or source rewrite.
An explicit recorded Master decision is required before executing this script.
"""
import bpy,json,math,hashlib,importlib.util,sys
sys.dont_write_bytecode=True
from pathlib import Path
from collections import defaultdict
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
from mathutils.geometry import convex_hull_2d
import numpy as np
spec=importlib.util.spec_from_file_location('pino_prove',Path(__file__).with_name('prove-pino-c-geometry.py'));u=importlib.util.module_from_spec(spec);spec.loader.exec_module(u)
ROOT,ASSET,OUT=u.ROOT,u.ASSET,u.OUT
MOTION=OUT/'motion';MOTION.mkdir(exist_ok=True)
decision=json.loads((OUT/'master-decision.json').read_text(encoding='utf-8'))
assert decision['status']=='HUMAN_SELECTED', 'Master must be decided by Human after discrepancy review'
MASTER=ROOT/decision['source'];assert u.sha(MASTER)==decision['sha256']
o=u.u.load(MASTER);o.data=o.data.copy();o.name='PINO_C_DIAGNOSTIC_DUPLICATE_ONLY'
me=o.data;me.calc_loop_triangles();V=np.array([tuple(o.matrix_world@v.co) for v in me.vertices]);T=np.array([list(t.vertices) for t in me.loop_triangles]);L=u.L.copy();u.V=V;u.T=T
BASE_LOCAL=np.array([tuple(v.co) for v in me.vertices]);INV=o.matrix_world.inverted()
NORMAL_START=np.array([tuple(n.vector) for n in me.corner_normals]);MATERIAL_START=[m.name for m in me.materials]
N=len(V);cam=u.setup(o);scene=bpy.context.scene
scene.render.engine='BLENDER_WORKBENCH';scene.render.resolution_x=400;scene.render.resolution_y=400
scene.render.film_transparent=False;scene.display.shading.light='STUDIO';scene.display.shading.studiolight_rotate_z=.25
scene.display.shading.color_type='MATERIAL';scene.display.shading.show_shadows=True;scene.display.shading.show_cavity=False;scene.display.shading.show_specular_highlight=True
scene.display.shading.background_type='WORLD';scene.world.color=(.12,.14,.17);scene.view_settings.exposure=0

def rot_x(p,pivot,angle):
    q=p-pivot;c,s=math.cos(angle),math.sin(angle);out=q.copy();out[:,1]=c*q[:,1]-s*q[:,2];out[:,2]=s*q[:,1]+c*q[:,2];return out+pivot

def arm_pose(sides,strength,inward=0):
    if strength==0:return V.copy()
    v=V.copy()
    for side in sides:
        x=side*V[:,0];w=u.smooth(.17,.245,x)*u.smooth(.16,.28,V[:,2])*(1-u.smooth(.43,.52,V[:,2]))*(L==0)
        q=V-np.array([side*.19,-.12,.45]);ang=-side*math.radians(inward)*strength*w;c,s=np.cos(ang),np.sin(ang);r=q.copy();r[:,0]=c*q[:,0]-s*q[:,1];r[:,1]=s*q[:,0]+c*q[:,1]
        ang=math.radians(-30)*strength*w;c,s=np.cos(ang),np.sin(ang);z=r[:,2].copy();y=r[:,1].copy();r[:,1]=c*y-s*z;r[:,2]=s*y+c*z
        mask=w>0;v[mask]=r[mask]+np.array([side*.19,-.12,.45])
    return v

bodytree=BVHTree.FromPolygons([Vector(p) for p in V],T[L[T[:,0]]==0].tolist(),all_triangles=True)
eye_targets={}
for comp in [8,9]:
    ids=np.where(L==comp)[0];p=V[ids];center=(p.min(axis=0)+p.max(axis=0))/2;xn=(p[:,0]-center[0])/(np.ptp(p[:,0])/2);line=center[2]+.010*(1-xn*xn)
    target=p.copy();target[:,2]=line+.035*(p[:,2]-center[2])
    for i,pt in enumerate(target):
        hit=bodytree.ray_cast(Vector((pt[0],-.8,pt[2])),Vector((0,1,0)))
        if hit[0] is not None:target[i,1]=hit[0].y-.0015-.0025*(1-xn[i]*xn[i])
    eye_targets[comp]=(ids,target)

def eyes(left,right):
    v=V.copy()
    for comp,amount in [(9,left),(8,right)]:
        ids,target=eye_targets[comp];v[ids]=(1-amount)*V[ids]+amount*target
    return v

def rest(strength):
    if strength==0:return V.copy()
    angle=math.radians(60)*strength;pivot=np.array([0,-.02,.16]);v=rot_x(V,pivot,angle)
    # Hind soles stay at their original coordinates; the transition is smooth.
    w=u.smooth(.055,.19,V[:,2]);v=V+(v-V)*w[:,None]
    # Head counter-rotation maintains an observable face; no shape reconstruction.
    neck=np.array([0,-.12,.48]);neck_new=rot_x(neck[None,:],pivot,angle)[0]
    h=u.smooth(.44,.54,V[:,2]);counter=rot_x(v,neck_new,math.radians(-40)*strength);v+=(counter-v)*h[:,None]
    tail=np.isin(L,[2,5]);v[tail]=rot_x(V[tail],pivot,math.radians(15)*strength)
    return v

def signed_volume(v,fs):
    p=v[fs];return float(np.einsum('ij,ij->i',p[:,0],np.cross(p[:,1],p[:,2])).sum()/6)

def tail_shell_ids():
    ids=np.where(L[T[:,0]]==2)[0];fs=T[ids];edges=defaultdict(list)
    for i,t in enumerate(fs):
        for a,b in zip(t,np.roll(t,-1)):edges[tuple(sorted((int(a),int(b))))].append(i)
    parent=list(range(len(fs)))
    def find(a):
        while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
        return a
    for a in edges.values():
        if len(a)==2:parent[find(a[0])]=find(a[1])
    groups=defaultdict(list)
    for i in range(len(fs)):groups[find(i)].append(i)
    return [fs[g] for g in groups.values()]+[T[L[T[:,0]]==5]]

SHELLS=tail_shell_ids();BASEVOLS=[signed_volume(V,f) for f in SHELLS]
FOOTMASK=(L==0)&(V[:,2]<.045)
PAWS=[np.where((L==0)&(s*V[:,0]>.265)&(V[:,2]>.24)&(V[:,2]<.38))[0] for s in [1,-1]]

def section_area(v,fs,origin,normal,axis1,axis2):
    points=[]
    for p in v[fs]:
        d=(p-origin)@normal
        for a,b in [(0,1),(1,2),(2,0)]:
            if d[a]*d[b]<0:
                q=p[a]+(p[b]-p[a])*(-d[a])/(d[b]-d[a]);points.append([float((q-origin)@axis1),float((q-origin)@axis2)])
    if len(points)<3:return None
    points=np.unique(np.round(points,10),axis=0);ids=convex_hull_2d([Vector(p) for p in points]);p=points[ids]
    return float(abs(np.sum(p[:,0]*np.roll(p[:,1],-1)-p[:,1]*np.roll(p[:,0],-1)))/2)

BASE_AREAS=[section_area(V,SHELLS[0],np.array([0,y,0]),np.array([0,1,0]),np.array([1,0,0]),np.array([0,0,1])) for y in [.05,.20,.35]]
def tail_sections(v,strength):
    k=math.radians(20)*strength/.415;areas=[]
    for y,base in zip([.05,.20,.35],BASE_AREAS):
        dy=y-.015;a=k*dy;c,s=math.cos(a),math.sin(a);org=np.array([(1-c)/k if abs(k)>1e-12 else 0,.015+s/k if abs(k)>1e-12 else y,0]);normal=np.array([s,c,0]);ax=np.array([c,-s,0])
        area=section_area(v,SHELLS[0],org,normal,ax,np.array([0,0,1]));areas.append(None if area is None else area/base)
    return areas

def metrics(v,kind,strength):
    r=u.surface_stats(v);r.update(foot_vertex_max_displacement=float(np.linalg.norm(v[FOOTMASK]-V[FOOTMASK],axis=1).max()),
        tail_signed_volume_ratio=[signed_volume(v,f)/b for f,b in zip(SHELLS,BASEVOLS)],tail_body_shared_vertices=0,
        world_vertex_sha256=hashlib.sha256(v.astype('<f8').tobytes()).hexdigest())
    r['distal_paw_vertex_min_gap']=float(np.linalg.norm(v[PAWS[0]][:,None,:]-v[PAWS[1]][None,:,:],axis=-1).min())
    r['floor_contact_vertices']={name:int(np.sum(np.abs(v[mask,2])<=.001)) for name,mask in [('hindfeet',FOOTMASK),('belly',(L==0)&(np.abs(V[:,0])<.16)&(V[:,2]>.16)&(V[:,2]<.43)),('tail',np.isin(L,[2,5]))]}
    if kind=='tail':r['tail_material_section_area_ratio']=tail_sections(v,strength)
    return r

def write_vertices(v):
    if np.array_equal(v,V):
        for i,p in enumerate(BASE_LOCAL):me.vertices[i].co=p
    else:
        for i,p in enumerate(v):me.vertices[i].co=INV@Vector(p)
    me.update();bpy.context.view_layer.update()

def render_frame(name,index,view):
    d=Vector({'front':(0,-1,.08),'threequarter':(1,-1,.14),'side':(1,0,.04)}[view]).normalized();target=Vector((0,-.20,.38) if 'low-rest' in name else (0,-.05,.46));cam.location=target+d*3;cam.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=1.80 if 'low-rest' in name else 1.24
    bpy.context.view_layer.update()
    scene.render.filepath=str(MOTION/f'{name}-{index:03d}-{view}.png');bpy.ops.render.render(write_still=True)

fixture=None
def create_fixture(kind,full):
    global fixture
    if fixture:bpy.data.objects.remove(fixture,do_unlink=True);fixture=None
    if kind not in ['high-five-L','both-contact','food-hold','gift-present']:return None
    # A bounded diagnostic fixture fitted to the selected endpoint, not a product item.
    anchor_ids=[]
    for side in ([1] if kind in ['high-five-L','food-hold'] else [1,-1]):
        ids=np.where((L==0)&(side*V[:,0]>.265)&(V[:,2]>.24)&(V[:,2]<.38))[0]
        center=full[ids].mean(axis=0);i=ids[np.argmin(full[ids,1])];anchor_ids.append(int(i))
    pts=full[anchor_ids]
    if len(pts)==1:
        radius=.018 if kind=='high-five-L' else .055;center=pts[0]+np.array([0,-radius,0]);bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,radius=radius,location=center);fixture=bpy.context.object
        meta=dict(type='sphere',radius=radius,center=center.tolist(),anchors=anchor_ids)
    else:
        center=pts.mean(axis=0);size=np.array([abs(pts[0,0]-pts[1,0]),.055,.075]);center[1]-=size[1]/2;bpy.ops.mesh.primitive_cube_add(size=1,location=center);fixture=bpy.context.object;fixture.scale=size
        meta=dict(type='box',center=center.tolist(),size=size.tolist(),anchors=anchor_ids)
    fixture.name='DIAGNOSTIC_FIXTURE_NOT_PRODUCT';m=bpy.data.materials.new('Fixture terracotta');m.diffuse_color=(.55,.18,.11,1);fixture.data.materials.append(m)
    return meta

def fixture_metrics(v,meta):
    if not meta:return None
    p=v[meta['anchors']];center=np.array(meta['center'])
    if meta['type']=='sphere':gap=np.abs(np.linalg.norm(p-center,axis=1)-meta['radius'])
    else:
        q=np.abs(p-center)-np.array(meta['size'])/2;gap=np.linalg.norm(np.maximum(q,0),axis=1)+np.minimum(np.max(q,axis=1),0)
    body=BVHTree.FromPolygons([Vector(p) for p in v],T.tolist(),all_triangles=True);fixture.data.calc_loop_triangles();fv=[fixture.matrix_world@vv.co for vv in fixture.data.vertices];ft=[list(t.vertices) for t in fixture.data.loop_triangles];tree=BVHTree.FromPolygons(fv,ft,all_triangles=True)
    return dict(anchor_surface_gap=np.abs(gap).tolist(),triangle_intersections=len(body.overlap(tree)),fit='endpoint-fitted diagnostic fixture; not arbitrary Food/Gift reach validation')

def pulse(n):return [math.sin(math.pi*i/(n-1))**2 for i in range(n)]
def main():
    runs=[];bank={}
    tests=[('tail','tail',list(np.sin(np.linspace(0,2*math.pi,25)))),
        ('eyes-L-blink','eyes-L',pulse(9)),('eyes-R-blink','eyes-R',pulse(9)),('eyes-L-wink','eyes-L',[0,.5,1,1,1,1,.5,0,0]),('eyes-R-wink','eyes-R',[0,.5,1,1,1,1,.5,0,0]),
        ('eyes-half','eyes-both',[0,.25,.5,.5,.5,.5,.25,0,0]),('eyes-full-close','eyes-both',[0,.5,1,1,1,1,.5,0,0]),
        ('raise-L','raise-L',pulse(13)),('raise-R','raise-R',pulse(13)),('high-five-L','raise-L',pulse(13)),('both-contact','both',pulse(13)),('food-hold','food',pulse(13)),('gift-present','both',pulse(13)),('low-rest','rest',pulse(25))]
    for name,kind,values in tests:
        def calculate(s):
            if kind=='tail':return u.deform('tail',s)
            if kind=='eyes-L':return eyes(s,0)
            if kind=='eyes-R':return eyes(0,s)
            if kind=='eyes-both':return eyes(s,s)
            if kind=='raise-L':return arm_pose([1],s)
            if kind=='raise-R':return arm_pose([-1],s)
            if kind=='both':return arm_pose([1,-1],s,75)
            if kind=='food':return arm_pose([1],s,30)
            return rest(s)
        full=calculate(.5 if name=='eyes-half' else 1);bank[name]=full.copy();meta=create_fixture(name,full);rows=[]
        for i,strength in enumerate(values):
            if i==len(values)-1:strength=0 # exact reset, not floating sin residue
            v=calculate(float(strength));write_vertices(v);r=metrics(v,'tail' if kind=='tail' else kind,float(strength));r.update(frame=i,strength=float(strength),fixture=fixture_metrics(v,meta));rows.append(r)
            for view in ['front','threequarter','side']:render_frame(name,i,view)
        runs.append(dict(name=name,kind=kind,frames=rows,fixture=meta,neutral_return_exact=np.array_equal(calculate(0),V)))
        u.write_json(OUT/'four-tests-progress.json',dict(master=decision,runs=runs))
    if fixture:bpy.data.objects.remove(fixture,do_unlink=True)
    write_vertices(V)
    # Exact local restoration avoids inverse-transform roundoff in saved Neutral.
    for i,p in enumerate(BASE_LOCAL):me.vertices[i].co=p
    me.update();bpy.context.view_layer.update()
    neutral_local=np.array([tuple(v.co) for v in me.vertices]);neutral_normals=np.array([tuple(n.vector) for n in me.corner_normals])
    exact=dict(local_vertices=np.array_equal(neutral_local,BASE_LOCAL),corner_normals=np.array_equal(neutral_normals,NORMAL_START),materials=[m.name for m in me.materials]==MATERIAL_START)
    assert all(exact.values()),exact
    # Material-faithful Cycles endpoints supplement the actual Workbench transitions.
    scene.render.engine='CYCLES';scene.cycles.samples=32;scene.view_settings.exposure=-.3
    for name in ['Neutral',*bank]:
        write_vertices(V if name=='Neutral' else bank[name])
        for view in ['front','threequarter','side']:render_frame('cycles-'+name,0,view)
    write_vertices(V)
    basis=o.shape_key_add(name='Basis')
    for name,world in bank.items():
        key=o.shape_key_add(name=name)
        for i,p in enumerate(world):key.data[i].co=INV@Vector(p)
        key.value=0
    scene['purpose']='FOUR ACTUAL DIAGNOSTIC TESTS ONLY / no production rig / originals immutable';scene['master_source']=decision['source'];scene['human_geometry_gate']='PENDING';scene['neutral_restoration']=json.dumps(exact)
    bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(ASSET/'pino-c-master-derived-four-tests.blend'))
    u.write_json(OUT/'four-tests.json',dict(master=decision,runs=runs,neutral_restoration_exact=exact,source_sha256_after=u.sha(MASTER),
        support='Floor contacts and mesh intersections measured per actual deformed frame. Physical COM/density and stable dynamics UNKNOWN due nonmanifold overlapping body; no tail-as-prop support assumed.',
        eye_method='Attempted eye-patch closure into existing head surface on duplicate only; no eyelid topology was invented. Assess crease/volume visually; geometry closure is not naturalness PASS.',
        limits='Bounds are diagnostic choices, not approved joint ranges. Fitted fixtures are not shipped Food/Gift. Custom source normals are retained on diagnostic mesh; no production normal/skin solution is certified. All deformation capabilities require Human review.',
        appearance_lock=dict(upstream_commit='2abea76fad578281f74b9fa628987a80b56ad6dc',integrated_main='8e4996c63c6d8fbb41954a2aa5cb5d892e45f01b',actual_views=['front','threequarter','side'],neutral_equality_does_not_imply_posed_quality=True)))

if __name__=='__main__':main()
