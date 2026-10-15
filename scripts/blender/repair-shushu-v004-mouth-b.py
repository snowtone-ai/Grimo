"""Separate mouth-only candidate. Geometry first; local texture is a later stage.

No writes to approved v004. New closed Basis and actual opening share its existing
mouth boundary. Oral wall, back and tongue are head-owned editable geometry.
"""
import bpy,sys,json,math,importlib.util,hashlib
from pathlib import Path
import numpy as np
from mathutils import Vector
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/production-rig-v004-mouth-b'
BASE=ROOT/'assets/grimo/production/shushu/tripo/geometry-v003/rigging'
SOURCE=BASE/'shushu-v006-production-rig-v004.blend'
ASSET=BASE/'shushu-v004-mouth-b-v001.blend'
GLB=BASE/'shushu-v004-mouth-b-v001.glb'
def module(name,path):
    s=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
b=module('base001','scripts/blender/build-shushu-production-rig-v001.py')
def write(name,data):
    (OUT/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def coords(k):return np.array([v.co for v in k.data])
def smooth(a,c,x):
    t=np.clip((x-a)/(c-a),0,1);return t*t*(3-2*t)
def boundary(p,tri):
    u,ix=np.unique(np.round(p,6),axis=0,return_inverse=True)
    edges=np.sort(np.concatenate([ix[tri[:,[0,1]]],ix[tri[:,[1,2]]],ix[tri[:,[2,0]]]]),axis=1)
    edges,n=np.unique(edges,axis=0,return_counts=True);edges=edges[n==1]
    a=u[edges].mean(1);edges=edges[(abs(a[:,0])<.04)&(a[:,2]>.595)&(a[:,2]<.615)&(a[:,1]<-.23)]
    adj={}
    for a,c in edges:
        adj.setdefault(int(a),[]).append(int(c));adj.setdefault(int(c),[]).append(int(a))
    assert all(len(v)==2 for v in adj.values()),'Mouth boundary must be one loop'
    loop=[min(adj,key=lambda i:u[i,0])];previous=None
    while True:
        nxt=next(v for v in adj[loop[-1]] if v!=previous)
        if nxt==loop[0]:break
        previous=loop[-1];loop.append(nxt)
        assert len(loop)<=len(adj)
    assert len(loop)==len(adj)
    ring=u[loop];right=np.argmax(ring[:,0]);a=ring[:right+1];c=np.concatenate([ring[right:],ring[:1]])[::-1]
    if np.mean(a[:,2])<np.mean(c[:,2]):a,c=c,a
    return ring,a,c
def seam(u):
    # Exact W lip contact; rounded philtrum and corners, modest plush thickness.
    return .616-.010*np.maximum(0,np.sin(np.pi*np.abs(u)))**.9
def opening(x,lower,t):
    u=np.clip(x/.043,-1,1);z=seam(u)
    if lower:z=z*(1-t)+(.614-.043*np.maximum(0,1-u*u)**.65)*t
    else:z+=.0008*t*(1-u*u)
    # Rounded chin retreats as it opens. Upper muzzle stays attached to nose.
    y=-.268+3.1*x*x+.34*(.616-z)+3.2*(.616-z)**2
    if lower:y+=.003*t*(1-u*u)
    return np.c_[x,y,z]
def head_shapes(o,rig):
    m=o.data;m.calc_loop_triangles();p=np.array([v.co for v in m.vertices]);tri=np.array([list(t.vertices) for t in m.loop_triangles]);ring,upper,lower=boundary(p,tri)
    w=max(abs(ring[:,0]));x,y,z=p.T
    # Existing x order stretches smoothly, then returns exactly to old cheek.
    xx=np.sign(x)*np.where(abs(x)<=w,abs(x)*.043/w,.043+(abs(x)-w)*(.080-.043)/(.080-w))
    uz=np.interp(x,upper[:,0],upper[:,2]);lz=np.interp(x,lower[:,0],lower[:,2]);mid=(uz+lz)/2
    islower=z<mid
    oldedge=np.where(islower,lz,uz)
    fadez=np.where(islower,1-smooth(.0,.058,np.maximum(0,oldedge-z)),1-smooth(.0,np.maximum(.001,.624-oldedge),np.maximum(0,z-oldedge)))
    mask=(1-smooth(w,.065,abs(x)))*smooth(.20,.24,-y)*fadez
    # Preserve nose (.624+) and every unrelated facial vertex/shape coordinate.
    mask[z>=.624]=0
    old_y=np.where(islower,np.interp(x,lower[:,0],lower[:,1]),np.interp(x,upper[:,0],upper[:,1]))
    def state(t):
        targets=np.zeros_like(p)
        for lo in [False,True]:
            mm=islower==lo;targets[mm]=opening(np.clip(xx[mm],-.043,.043),lo,t)
        delta=targets-np.c_[x,old_y,oldedge]
        delta[:,0]=xx-x
        result=p+delta*mask[:,None]
        surface_y=-.268+3.1*result[:,0]**2+.34*(.616-result[:,2])+3.2*(.616-result[:,2])**2
        if t:surface_y+=np.where(islower,.003*t*np.maximum(0,1-(np.clip(xx,-.043,.043)/.043)**2),0)
        result[:,1]=p[:,1]*(1-mask)+surface_y*mask
        return result
    closed=state(0);opened=state(1);ks=o.data.shape_keys
    old={k.name:coords(k) for k in ks.key_blocks}
    for k in ks.key_blocks:
        if k.name=='Basis':a=closed
        elif k.name=='MouthOpen':a=opened+(old[k.name]-p)*(1-mask[:,None])
        elif k.name in ['MouthClose','Corrective.MouthCavity']:a=closed+(old[k.name]-p)*(1-mask[:,None])
        else:
            delta=old[k.name]-p
            if k.name in ['Smile','Surprise']:delta*=1-mask[:,None]
            a=closed+delta
        k.data.foreach_set('co',a.astype(np.float32).ravel())
    for fc in ks.animation_data.drivers:
        if fc.data_path=='key_blocks["MouthOpen"].value':
            fc.driver.expression='max(o,t*.55,s*.18,j*.24,u*.65)*(1-c)'
            while fc.driver.variables:fc.driver.variables.remove(fc.driver.variables[0])
            for n,prop in {'o':'MouthOpen','t':'Tongue','s':'Smile','j':'Joy','u':'Surprise','c':'MouthClose'}.items():
                v=fc.driver.variables.new();v.name=n;v.type='SINGLE_PROP';v.targets[0].id=rig;v.targets[0].data_path='["'+prop+'"]'
    # Exact duplicated seam coordinates avoid independent UV seam drift.
    rid=[]
    for q in ring:rid.append(int(np.argmin(np.linalg.norm(p-q,axis=1))))
    data={'ring_source_indices':rid,'closed':closed[rid].tolist(),'open':opened[rid].tolist(),'lower':islower[rid].tolist(),'changed_vertices':int((mask>0).sum()),'changed_bounds':[p[mask>0].min(0).tolist(),p[mask>0].max(0).tolist()],'max_closed_delta':float(np.linalg.norm(closed-p,axis=1).max()),'max_open_delta':float(np.linalg.norm(opened-p,axis=1).max()),'outside_mask_all_keys_exact':all(np.array_equal(coords(k)[mask==0],old[k.name][mask==0]) for k in ks.key_blocks)}
    np.savez_compressed(OUT/'head-edit-mask.npz',mask=mask,original=p,closed=closed,opened=opened,ring_indices=rid)
    write('geometry-authoring.json',data)
    assert data['outside_mask_all_keys_exact']
    return closed[rid],opened[rid],islower[rid]
def material(name,color,rough=.75):
    m=bpy.data.materials.new(name);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=rough;return m
def replace_oral(name,p,polys,mat,rig,opened):
    o=bpy.data.objects['ShushuStatic_'+name]
    if o.data.shape_keys:o.shape_key_clear()
    mesh=bpy.data.meshes.new(o.data.name+'_MouthB');mesh.from_pydata(p,[],polys);mesh.update();o.data=mesh;o.location=(0,0,0);o.rotation_euler=(0,0,0);o.scale=(1,1,1)
    o.vertex_groups.clear();g=o.vertex_groups.new(name='mixamorig:Head');g.add(list(range(len(p))),1,'REPLACE')
    o.data.materials.clear();o.data.materials.append(mat)
    for face in mesh.polygons:face.use_smooth=True
    o.shape_key_add(name='Basis');k=o.shape_key_add(name='MouthOpen');k.data.foreach_set('co',np.asarray(opened,dtype=np.float32).ravel())
    b.driver(k,'value',rig,'max(o,t*.55,s*.18,j*.24,u*.65)*(1-c)',{'o':'MouthOpen','t':'Tongue','s':'Smile','j':'Joy','u':'Surprise','c':'MouthClose'})
    return o
def oral(rig,c,a,lo):
    n=len(c);layers=9
    def wall(ring):
        rows=[]
        for j in range(layers):
            t=j/(layers-1);q=ring.copy();q[:,0]*=1-.18*t;q[:,1]+=.00012+.032*t;q[:,2]=q[:,2]*(1-.12*t)+.600*.12*t;rows.extend(q)
        return np.array(rows)
    faces=[(j*n+i,j*n+(i+1)%n,(j+1)*n+(i+1)%n,(j+1)*n+i) for j in range(layers-1) for i in range(n)]
    # Reverse winding toward the oral air space; glTF uses double-sided interior.
    wallmat=material('MouthB lip to oral wall',(.28,.035,.049));wallmat.use_backface_culling=False
    replace_oral('MouthInterior',wall(c),faces,wallmat,rig,wall(a))
    def back(ring):
        inner=wall(ring)[-n:];center=inner.mean(0);center[1]+=.009
        return np.vstack([inner,center])
    replace_oral('OralBowl',back(c),[(i,(i+1)%n,n) for i in range(n)],material('MouthB rounded oral back',(.19,.024,.034)),rig,back(a))
    # Low rounded tongue remains behind the real lower lip; never a painted oval.
    verts=[];opened=[];segs=40;rings=20
    unit=[np.array([0,0,1])]
    for j in range(1,rings):
        phi=math.pi*j/rings
        for i in range(segs):
            theta=2*math.pi*i/segs
            unit.append(np.array([math.sin(phi)*math.cos(theta),math.sin(phi)*math.sin(theta),math.cos(phi)]))
    unit.append(np.array([0,0,-1]));verts=np.array([0,-.234,.604])+np.array(unit)*[.014,.009,.003];opened=np.array([0,-.240,.581])+np.array(unit)*[.018,.012,.005]
    faces=[(0,1+i,1+(i+1)%segs) for i in range(segs)]
    faces += [(1+j*segs+i,1+(j+1)*segs+i,1+(j+1)*segs+(i+1)%segs,1+j*segs+(i+1)%segs) for j in range(rings-2) for i in range(segs)]
    last=1+(rings-2)*segs;faces += [(len(verts)-1,last+(i+1)%segs,last+i) for i in range(segs)]
    replace_oral('Tongue',verts,faces,material('MouthB soft tongue',(.72,.19,.25),.6),rig,opened)
def load():
    bpy.ops.wm.open_mainfile(filepath=str(ASSET));return next(o for o in bpy.data.objects if o.type=='ARMATURE')
def texture():
    rig=load();o=bpy.data.objects['ShushuStatic_Head'];before=hashlib.sha256(b''.join(coords(k).tobytes() for k in o.data.shape_keys.key_blocks)).hexdigest()
    img=bpy.data.images.load(str(OUT/'Head-mouth-b-local.png'),check_existing=False);img.name='Shushu Head mouth B local';img.pack()
    nodes=[n for m in o.data.materials for n in m.node_tree.nodes if n.type=='TEX_IMAGE'];assert len(nodes)==1
    nodes[0].image=img
    # Modest stylized indirect tissue colour. Actual oral geometry remains lit.
    for role in ['MouthInterior','OralBowl']:
        bs=bpy.data.objects['ShushuStatic_'+role].data.materials[0].node_tree.nodes.get('Principled BSDF')
        bs.inputs['Emission Color'].default_value=(.055,.006,.009,1);bs.inputs['Emission Strength'].default_value=.35
    after=hashlib.sha256(b''.join(coords(k).tobytes() for k in o.data.shape_keys.key_blocks)).hexdigest();assert before==after
    write('texture-stage-geometry-invariance.json',{'before':before,'after':after,'equal':before==after})
    bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(ASSET))
def build():
    bpy.ops.wm.open_mainfile(filepath=str(SOURCE));rig=next(o for o in bpy.data.objects if o.type=='ARMATURE');b.reset(rig)
    c,a,lo=head_shapes(bpy.data.objects['ShushuStatic_Head'],rig);oral(rig,c,a,lo);b.reset(rig)
    rig['Mouth B status']='Candidate v001; closed model image first, geometry stage. Human PENDING. Original v004 protected.'
    bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(ASSET))
    print('MOUTH_B_GEOMETRY_SAVED',flush=True)
VIEWS={'front':(0,-3,.615),'side':(-3,0,.615),'3q':(-2,-2.5,.65)}
STATES={'closed':{},'small':{'MouthOpen':.2},'medium':{'MouthOpen':.55},'large':{'MouthOpen':1}}
def render():
    rig=load();scene,cam=b.setup_review(640,24);cam.data.type='ORTHO';cam.data.ortho_scale=.56
    clay='--clay' in sys.argv
    if clay:
        bpy.data.objects['ShushuStatic_Head'].data.materials.clear();bpy.data.objects['ShushuStatic_Head'].data.materials.append(material('Geometry review cream',(.78,.75,.71)))
    folder=OUT/('geometry-clay' if clay else 'author');folder.mkdir(exist_ok=True)
    names=sys.argv[sys.argv.index('--names')+1].split(',') if '--names' in sys.argv else list(STATES)
    for name in names:
        b.state(rig,STATES[name])
        for view,loc in VIEWS.items():
            cam.location=loc;cam.rotation_euler=(Vector((0,-.02,.69))-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(folder/f'{name}-{view}.png');bpy.ops.render.render(write_still=True)
        print('MOUTH_RENDER',name,flush=True)
if __name__=='__main__':
    if '--build' in sys.argv:build()
    elif '--render' in sys.argv:render()
    elif '--texture' in sys.argv:texture()
