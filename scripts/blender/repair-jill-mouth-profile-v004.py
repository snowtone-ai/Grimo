"""Fit the added mouth collar to the actual inherited facial envelope.

No topology, UV, weight, eye or skeleton edits. All output is a named derivative.
"""
import bpy,json,sys,math,hashlib
from pathlib import Path
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'assets/grimo/production/jill/tripo/rig-pretexture-technical-v003/jill-rig-texture-uv-v003.blend'
A=ROOT/'assets/grimo/production/jill/tripo/mouth-profile-v004';A.mkdir(exist_ok=True)
E=ROOT/'docs/production/jill/mouth-profile-v004';E.mkdir(exist_ok=True)
bpy.ops.wm.open_mainfile(filepath=str(SOURCE))
o=bpy.data.objects['Jill_Body'];r=bpy.data.objects['JILL_RIG'];m=o.data
contract=json.loads((ROOT/'docs/production/jill/rig-pretexture-v002/control-contract.json').read_text())
r.animation_data.action=None
for k in contract['authoring_properties']:r[k]=0.
r.update_tag();bpy.context.view_layer.update()
v=np.array([x.co[:] for x in m.vertices]);regions=np.load(ROOT/'docs/production/jill/rig-pretexture-v002/surface-contract.npz')['regions']
host=[list(p.vertices) for p in m.polygons if regions[p.index]=='original' and m.materials[p.material_index].get('paint_owner')=='body_skin']
bvh=BVHTree.FromPolygons([Vector(p) for p in v],host,all_triangles=False)
def ray(x,z):
    p,n,i,d=bvh.ray_cast(Vector((float(x),-1.,float(z))),Vector((0,1,0)),1.5)
    return p.y if p is not None else None
samples=[]
for z in np.linspace(.542,.644,70):
    for x in np.linspace(-.095,.095,81):
        # Exclude the opening, old oral recess and nose. Fit surrounding skin.
        if (x/.055)**2+((z-.606)/.034)**2<1.25**2 or (z>.626 and abs(x)<.043):continue
        y=ray(x,z)
        if y is not None and -.44<y<-.30:samples.append((x,y,z))
samples=np.array(samples)
def design(x,z):
    X=x/.07;Z=(z-.605)/.045
    return np.array([np.ones_like(X),Z,Z*Z,Z**3,X*X,X*X*Z,X*X*Z*Z,X**4]).T
coef=np.linalg.lstsq(design(samples[:,0],samples[:,2]),samples[:,1],rcond=None)[0]
def surface(x,z):return float(design(x,z)@coef)
probe={'samples':len(samples),'fit_rmse_m':float(np.sqrt(np.mean((design(samples[:,0],samples[:,2])@coef-samples[:,1])**2))),
       'profile':[{'x':x,'z':z,'actual_y':ray(x,z),'fit_y':surface(x,z)} for x in [0,.03,.06] for z in [.55,.56,.57,.58,.59,.60,.61,.62,.63,.64]],'coefficients':coef.tolist()}
(E/'host-fit.json').write_text(json.dumps(probe,indent=2)+'\n')
print(json.dumps(probe,indent=2),flush=True)
if '--probe' in sys.argv:sys.exit(0)

# A smooth depth field replaces the former shallow analytic muzzle plane.
# Unchanged x/z retain frontal contours. A bounded host Y fairing below handles
# the original muzzle's retreat; all other body regions stay untouched.
def old_surface(x,z):return -.408+2.3*x*x+2*(z-.625)**2
def depth_delta(x,z):return surface(x,z)-old_surface(x,z)
affected=set()
skin=set();adj={}
for p in m.polygons:
    if regions[p.index] in ['mouth-skin','mouth-inner','tongue','teeth']:affected.update(p.vertices)
    if regions[p.index]=='mouth-skin':
        skin.update(p.vertices)
        for j,i in enumerate(p.vertices):
            k=p.vertices[(j+1)%len(p.vertices)];adj.setdefault(i,set()).add(k);adj.setdefault(k,set()).add(i)
old_report=json.loads((ROOT/'docs/production/jill/rig-pretexture-v002/repair-report.json').read_text())
outer=next(x['boundary_vertices'] for x in old_report['local_changes'] if x.get('graft')=='mouth')
distance={i:0 for i in outer};front=list(outer)
while front:
    new=[]
    for i in front:
        for j in adj[i]:
            if j not in distance:distance[j]=distance[i]+1;new.append(j)
    front=new
assert set(distance)==skin and max(distance.values())==12
affected=sorted(affected)
before={k.name:np.array([x.co[:] for x in k.data]) for k in m.shape_keys.key_blocks}
# The inherited close key retracts some exposed lower muzzle by 35mm. That
# created the jagged edge when the old floating plate was fitted into the face.
# Fair only this small skin neighbourhood and retain the exposed cheek at close.
host_ids=set(i for p in host for i in p)
host_shift={};close_restored=[]
for i in host_ids:
    x,y,z=v[i]
    rho=math.sqrt((x/.067)**2+((z-.607)/.047)**2)
    if y>=-.375 or not .55<z<.634 or rho>=1.22:continue
    t=np.clip((rho-.82)/.40,0,1);w=1-t*t*(3-2*t)
    if z>.622 and abs(x)<.045:
        t=np.clip((z-.622)/.012,0,1);w*=1-t*t*(3-2*t)
    shift=(surface(x,z)-y)*w
    if abs(shift)>1e-8:host_shift[i]=float(shift)
    if abs(before['FACE_MouthClose'][i,1]-v[i,1]-.035)<1e-5:close_restored.append(i)
for key in m.shape_keys.key_blocks:
    coords=before[key.name].copy()
    for i,dy in host_shift.items():coords[i,1]+=dy
    if key.name=='FACE_MouthClose':
        for i in close_restored:coords[i,1]-=.035
    for i in affected:
        x,y,z=coords[i]
        if i in skin:
            t=distance[i]/12
            # Buried outer margin, tangent-continuous round skin, small lip rim.
            coords[i,1]=surface(x,z)+.0015*(1-t)**3-.0005*(1-(1-t)**3)
        elif key.name=='FACE_MouthClose':coords[i,1]+=depth_delta(x,z)-.0002
        else:
            old_lip=-.398+.004*(x/.045)**2-.10*(z-.605)
            coords[i,1]+=surface(x,z)-old_lip-.0005
    key.data.foreach_set('co',coords.astype(np.float32).ravel())
m.vertices.foreach_set('co',np.array([x.co[:] for x in m.shape_keys.key_blocks['Basis'].data],dtype=np.float32).ravel());m.update()
o['basis_contract']='v004: mouth skin/cavity depth fitted to head envelope; local original muzzle Y fairing and exposed-skin close retreat removed. All x/z, UVs/topology/weights preserved.'
o['texture_status']='Mouth profile v004 local derivative; unchanged Jill_Texture_UV0_v003 atlas. Human review pending.'
r['status']='MOUTH_PROFILE_V004 / HUMAN_VISUAL_REVIEW_PENDING'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(A/'jill-rig-mouth-profile-v004.blend'))
after={k.name:np.array([x.co[:] for x in k.data]) for k in m.shape_keys.key_blocks}
changed={k:{'changed_vertices':int(np.count_nonzero(np.linalg.norm(after[k]-before[k],axis=1)>1e-9)),
            'max_depth_change_m':float(np.max(abs(after[k][:,1]-before[k][:,1]))),
            'xz_exact':bool(np.array_equal(after[k][:,[0,2]],before[k][:,[0,2]])),
            'inherited_28050_exact':bool(np.array_equal(after[k][:28050],before[k][:28050]))} for k in before}
(E/'repair-report.json').write_text(json.dumps({'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'affected_vertices':affected,
    'method':'Y-only fitted host envelope for skin annulus, buried outer margin and 0.5mm lip rim. Connected cavity/tongue/teeth follows lip correction; bounded original muzzle Y fairing and exposed-skin close retreat removal.',
    'local_host_y_fairing':host_shift,'close_exposed_skin_retreat_removed':close_restored,
    'keys':changed,'geometry_topology_count_unchanged':True,'human_final_go':False},indent=2)+'\n')
