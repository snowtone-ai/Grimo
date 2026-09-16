"""Canonical-derived v004 geometry study. Blender 5.2, no rig or GLB export.

Preserves v003 chassis/supports/hooves/tuft and review cameras. Rebuilds its
visible shell as one closed radial volume with source-authored relief fields.
Historical paint is never projected onto the new geometry.
"""
import argparse
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
import bpy
import bmesh
import numpy as np
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'assets/grimo/production/carol/blender/carol-blockout-v003.blend'
DATA=json.loads(Path(__file__).with_name('carol-v004-reference-data.json').read_text())
spec=importlib.util.spec_from_file_location('old',Path(__file__).with_name('build-carol-blockout.py'))
old=importlib.util.module_from_spec(spec); spec.loader.exec_module(old)
spec3=importlib.util.spec_from_file_location('v3',Path(__file__).with_name('build-carol-v003.py'))
v3=importlib.util.module_from_spec(spec3); spec3.loader.exec_module(v3)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def mapped(x,y): return ((x-324)*.0072,.37+(380-y)*.007)
def trace(points,steps=8):
    pts=np.array(points,float); out=[]
    for i,p1 in enumerate(pts):
        p0,p2,p3=pts[(i-1)%len(pts)],pts[(i+1)%len(pts)],pts[(i+2)%len(pts)]
        for j in range(steps):
            t=j/steps
            out.append(.5*(2*p1+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t))
    return np.array(out)

def radial_trace(points,center,segments):
    pts=trace(points); a=pts-np.array(center); b=np.roll(pts,-1,axis=0)-pts
    radii=[]
    for i in range(segments):
        d=np.array([math.cos(i*math.tau/segments), math.sin(i*math.tau/segments)])
        denom=d[0]*b[:,1]-d[1]*b[:,0]
        safe=np.where(abs(denom)>1e-9,denom,1e-9)
        t=(a[:,0]*b[:,1]-a[:,1]*b[:,0])/safe
        u=(a[:,0]*d[1]-a[:,1]*d[0])/safe
        hits=t[(t>0)&(u>=0)&(u<=1)]
        assert len(hits),'Contour is not star-shaped about its documented center'
        radii.append(float(max(hits)))
    return np.array(radii)

def closed_volume(name,outline,center,depth_fn,mat,segments=192,rings=80,fade=False):
    radii=radial_trace(outline,center,segments)
    verts=[]; coords=[]; faces=[]
    # Unique front/rear pole avoids degenerate rings.
    for j in range(rings+1):
        th=math.pi*j/rings; r=math.sin(th); c=math.cos(th)
        for i in range(1 if j in (0,rings) else segments):
            a=i*math.tau/segments
            radius=radii[i]
            if fade:
                rx=(radii[0]+radii[segments//2])/2
                ry=(radii[segments//4]+radii[3*segments//4])/2
                ellipse=1/math.sqrt((math.cos(a)/rx)**2+(math.sin(a)/ry)**2)
                radius=ellipse+(radius-ellipse)*r**10
            sx=center[0]+radius*r*math.cos(a)
            sy=center[1]+radius*r*math.sin(a)
            x,z=mapped(sx,sy)
            verts.append((x,depth_fn(sx,sy,r,c,a),z)); coords.append((sx,sy,r,c,a))
    for i in range(segments): faces.append((0,1+i,1+(i+1)%segments))
    for j in range(rings-2):
        for i in range(segments):
            a=1+j*segments+i; b=1+j*segments+(i+1)%segments
            faces.append((a,a+segments,b+segments,b))
    end=len(verts)-1; start=1+(rings-2)*segments
    for i in range(segments): faces.append((start+i,end,start+(i+1)%segments))
    mesh=bpy.data.meshes.new(name); mesh.from_pydata(verts,[],faces); mesh.update()
    bm=bmesh.new(); bm.from_mesh(mesh); bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces)); bm.to_mesh(mesh); bm.free()
    obj=bpy.data.objects.new(name,mesh); bpy.context.collection.objects.link(obj)
    obj.parent=bpy.data.objects['Carol_Model']; obj.data.materials.append(mat); old.smooth(obj)
    return obj,np.array(coords)

def locks(sx,sy,controls):
    vals=[d*math.exp(-2*(((sx-x)/rx)**2+((sy-y)/ry)**2)) for x,y,rx,ry,d in controls]
    return sum(v**5 for v in vals)**.2

def preserve():
    result={}
    for o in bpy.data.objects:
        if o.type=='MESH' and o.name.startswith(('Carol_Chassis','Carol_Support_','Carol_Hoof_','Carol_Rear_Tuft')):
            result[o.name]={'mesh':hashlib.sha256(np.array([v.co[:] for v in o.data.vertices],np.float32).tobytes()).hexdigest(),'matrix':[list(r) for r in o.matrix_world]}
    return result

def shell(pass_number,mat):
    def depth(x,y,r,c,a):
        # Full 3D: front-to-back depth remains ~3 BU, with no shallow reverse.
        if c>=0:
            controls=DATA['BODY_LOCKS']+DATA['HEAD_LOCKS']
            if pass_number>=3: controls=[(cx,cy,rx*1.12,ry*1.08,d*.72) for cx,cy,rx,ry,d in controls]
            relief=locks(x,y,controls)
            recess=.18*math.exp(-(((x-426)/70)**4+((y-242)/58)**4))
            return .10-1.26*c**.70-(1.0 if pass_number==1 else 1.25)*relief*c**.35+recess*c
        return .10+1.43*(-c)**.85
    obj,coords=closed_volume('Carol_Fleece_Continuous',DATA['BODY_OUTLINE'],(324,206),depth,mat,256,144,pass_number>=2)
    pos=np.array([v.co[:] for v in obj.data.vertices]); center=np.array([0,.12,1.55])
    dirs=(pos-center)/np.array([1.55,1.4,1.35]); dirs/=np.linalg.norm(dirs,axis=1)[:,None]
    # Flow on both flanks and rear; deliberately unequal oblique banks.
    banks=[(-178,38,.36,.17,.18,.6),(-175,0,.40,.19,.23,-.5),(-170,-34,.32,.16,.18,.4),
           (-2,40,.36,.17,.22,-.6),(5,3,.44,.19,.21,.55),(12,-33,.35,.18,.20,-.5),
           (138,38,.41,.22,.25,.6),(70,45,.34,.20,.19,-.5),(103,12,.44,.19,.23,.6),
           (146,-8,.35,.19,.20,-.4),(48,-8,.36,.17,.24,.5),(112,-36,.40,.17,.22,-.4)]
    small=[(170,20,.19,.13,.10,.3),(22,24,.21,.12,.11,-.3),(174,-18,.23,.12,.12,-.5),
           (26,-23,.20,.13,.10,.4),(123,56,.24,.14,.11,.5),(76,-31,.23,.13,.11,-.4)]
    if pass_number>=3:
        banks += [(91,30,.31,.16,.27,-.55),(83,-6,.34,.15,.23,.45),
                  (121,-31,.30,.15,.20,-.4),(173,19,.30,.16,.24,-.5),
                  (178,-16,.31,.16,.22,.4),(0,20,.32,.16,.25,.5),
                  (3,-16,.30,.15,.21,-.4)]
    amp=1 if pass_number==1 else 1.65
    relief=amp*v3.field(dirs,banks)+v3.field(dirs,small)
    # Envelope displacement fades on the source-registered front hemisphere.
    influence=np.clip((dirs[:,1]+.45)/.75,0,1)
    radial=pos-center; radial/=np.linalg.norm(radial,axis=1)[:,None]
    pos+=radial*(relief*influence)[:,None]
    obj.data.vertices.foreach_set('co',pos.astype(np.float32).ravel()); obj.data.update()
    if pass_number>=2:
        def head_depth(x,y,r,c,a):
            if c>=0:
                recess=(.25 if pass_number>=3 else .13)*math.exp(-(((x-426)/70)**4+((y-242)/58)**4))
                if pass_number>=3:
                    return -1.20-.21*c-.80*locks(x,y,DATA['HEAD_LOCKS'])*c**.3+recess*c
                return -.96-.30*c-1.10*locks(x,y,DATA['HEAD_LOCKS'])*c**.3+recess*c
            return -.96-.75*c
        head,_=closed_volume('V004_Temporary_HeadEnvelope',DATA['HEAD'],(398,214),head_depth,mat,192,96,True)
        # Lower cover is actual volume around the preserved support roots.
        lower=old.uv('V004_Temporary_LowerCover',(0,.15,.59 if pass_number>=3 else .64),
                     (1.28 if pass_number>=3 else 1.20,1.40 if pass_number>=3 else 1.33,.34),mat)
        obj=old.fuse('Carol_Fleece_Continuous',[obj,head,lower],mat,bpy.data.objects['Carol_Model'],voxel=.018,iterations=2)
    obj['construction']='One closed Full-3D envelope; exact source BODY outline; fifth-norm BODY/HEAD relief; authored circumferential banks'
    obj['historical_data']='carol-v004-reference-data.json'
    return obj

def crescent(shell,mat,root):
    # Closed strip preserves the concavity without tessellating a thin ngon.
    verts=[]; faces=[]; n=61
    for i in range(n):
        t=i/(n-1); a=math.radians(-66-240*t); b=math.radians(-104-157*t)
        outer=mapped(218+45*math.cos(a),172+48*math.sin(a))
        inner=mapped(235+30*math.cos(b),158+33*math.sin(b))
        if i in (0,n-1): inner=(outer[0]+.001,outer[1]-.001)
        for x,z in (outer,inner):
            hit,p,_,_=shell.ray_cast(Vector((x,-5,z)),Vector((0,1,0))); assert hit
            verts.append([x,p.y-.045,z])
    # Smooth only attachment depth along each contour; keep traced X/Z fixed.
    for _ in range(12):
        old_y=[p[1] for p in verts]
        for i in range(2,len(verts)-2): verts[i][1]=.5*old_y[i]+.25*(old_y[i-2]+old_y[i+2])
    # A common cross-strip depth prevents a corrugated ribbon over cloud ridges.
    for i in range(n):
        y=min(verts[2*i][1],verts[2*i+1][1]);verts[2*i][1]=verts[2*i+1][1]=y
    verts += [[x,y+.045,z] for x,y,z in verts.copy()]
    offset=2*n
    for i in range(n-1):
        j=2*i;faces += [(j,j+2,j+3,j+1),(j+offset+1,j+offset+3,j+offset+2,j+offset),
                       (j,j+offset,j+offset+2,j+2),(j+1,j+3,j+offset+3,j+offset+1)]
    faces += [(0,1,offset+1,offset),(offset-2,2*offset-2,2*offset-1,offset-1)]
    mesh=bpy.data.meshes.new('Carol_Moon_Attached');mesh.from_pydata(verts,[],faces)
    bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free()
    obj=bpy.data.objects.new('Carol_Moon_Attached',mesh);bpy.context.collection.objects.link(obj);obj.parent=root;mesh.materials.append(mat);old.smooth(obj)

def features(pass_number):
    root=bpy.data.objects['Carol_Model']
    cream=old.material('V004_Diagnostic_Cream',(1,.84,.68))
    brown=old.material('V004_Diagnostic_Cocoa',(.18,.085,.065))
    pink=old.material('V004_Diagnostic_InnerEar',(.84,.35,.29))
    dark=old.material('V004_Diagnostic_Eye',(.037,.019,.029))
    iris=old.material('V004_Diagnostic_Iris',(.43,.21,.085))
    gold=old.material('V004_Diagnostic_Honey',(.98,.62,.19))
    shine=old.material('V004_Diagnostic_Highlight',(1,.95,.83))
    coral=old.material('V004_Diagnostic_Mouth',(.58,.13,.11))
    tongue=old.material('V004_Diagnostic_Tongue',(.98,.36,.28))
    # Shallow convex custom contour, continuous back extending into fleece.
    face,_=closed_volume('Carol_Face',DATA['FACE'],(424,242),
        lambda x,y,r,c,a:-1.28-(.20 if c>=0 else .26)*c,cream,192,72)
    face['construction']='Canonical FACE trace, full closed cheek/jaw volume; no circular mask'
    x,z=mapped(424,242); old.empty('Carol_Face_Center',(x,-1.52,z),root)
    for i,side in enumerate(('L','R')):
        center=DATA['features']['earCenters'][i]; outer=DATA['EAR_'+side]
        d= -1.44 if side=='L' else -1.19
        obj,_=closed_volume('Carol_Ear_'+side,outer,center,
            lambda x,y,r,c,a,d=d:d-.105*c,brown,128,42)
        obj['construction']='Independent canonical trace with thickness; inner region manually traced from canonical'
        inn=DATA['features']['innerEarTraces'][i]; ic=tuple(np.mean(inn,axis=0))
        closed_volume('Carol_InnerEar_'+side,inn,ic,
            lambda x,y,r,c,a,d=d:d-.095-.018*c,pink,96,24)
        rx,rz=mapped(*DATA['features']['earRoots'][i]); old.empty('Carol_Ear_Root_'+side,(rx,d,rz),root)
    # Visible eye radii are measured artwork approximations, not warp radii.
    for i,(ex,ey) in enumerate(DATA['eye_centers']):
        side='L' if i==0 else 'R'; x,z=mapped(ex,ey)
        # Slightly curved face: source-relative feature depth evaluated by ray.
        hit,p,_,_=face.ray_cast(Vector((x,-5,z)),Vector((0,1,0)))
        assert hit
        y=p.y-.019
        eye=old.uv('Carol_Eye_'+side,(x,y,z),(.130,.068,.174),dark,root)
        eye.rotation_euler.y=math.radians(-19)
        old.uv('Carol_Iris_'+side,(x+.024,y-.058,z-.052),(.102,.019,.092),iris,root).rotation_euler.y=math.radians(-19)
        old.uv('Carol_EyeHoney_'+side,(x+.040,y-.078,z-.088),(.059,.011,.055),gold,root)
        old.uv('Carol_EyeGlint_'+side,(x-.033,y-.073,z+.076),(.042,.016,.046),shine,root)
        old.uv('Carol_EyeGlintSmall_'+side,(x+.060,y-.074,z+.015),(.017,.012,.022),shine,root)
    x,z=mapped(431,242)
    old.uv('Carol_Nose',(x,-1.51,z),(.041,.020,.023),brown,root).rotation_euler.y=math.radians(-19)
    mouth=DATA['features']['mouthTrace']; mc=tuple(np.mean(mouth,axis=0))
    closed_volume('Carol_Mouth',mouth,mc,lambda x,y,r,c,a:-1.462-.032*c,coral,96,28)
    x,z=mapped(432,266); old.uv('Carol_Tongue',(x,-1.501,z),(.046,.009,.040),tongue,root)
    # Small cream cheek volume follows the muzzle-free facial center; no snout.
    for i,(sx,sy) in enumerate(((420,250),(441,243))):
        x,z=mapped(sx,sy)
        old.uv('Carol_CreamCheek_'+str(i),(x,-1.465,z),(.064,.019,.035),cream,root)
    return face

def export_diagnostic(path):
    """Temporary mesh JSON for browser comparison, not a production asset."""
    result=[]; dg=bpy.context.evaluated_depsgraph_get()
    for obj in bpy.context.scene.objects:
        if obj.type!='MESH': continue
        evaluated=obj.evaluated_get(dg); mesh=evaluated.to_mesh(); mesh.calc_loop_triangles()
        coords=[list(obj.matrix_world@v.co) for v in mesh.vertices]
        mats=[list(m.diffuse_color) for m in mesh.materials]
        for mi,mat in enumerate(mats):
            tris=[list(t.vertices) for t in mesh.loop_triangles if t.material_index==mi]
            if tris: result.append({'name':obj.name,'positions':coords,'triangles':tris,'color':mat})
        evaluated.to_mesh_clear()
    path.write_text(json.dumps(result,separators=(',',':')),encoding='utf-8')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--pass-number',type=int,default=1)
    ap.add_argument('--output',type=Path,required=True); ap.add_argument('--width',type=int,default=1100)
    ap.add_argument('--blend-path',type=Path); args=ap.parse_args(sys.argv[sys.argv.index('--')+1:])
    out=args.output.resolve(); out.mkdir(parents=True,exist_ok=True)
    protected=[BASE,*list((ROOT/'assets/grimo/source').rglob('*.png')),*list((ROOT/'docs/production/carol/evidence/blockout-v003').glob('*'))]
    hashes={str(p.relative_to(ROOT)):sha(p) for p in protected if p.is_file()}
    bpy.ops.wm.open_mainfile(filepath=str(BASE)); before=preserve()
    if args.pass_number==1: export_diagnostic(out.parent/'v003-mesh.json')
    for obj in list(bpy.data.objects):
        if obj.name.startswith(('Carol_Fleece','Carol_Face','Carol_Eye','Carol_Ear','Carol_Nose','Carol_Mouth','Carol_Moon','Carol_Star','Carol_Review')):
            bpy.data.objects.remove(obj,do_unlink=True)
    fleece=old.material('V004_Diagnostic_Fleece',(.78,.81,.94))
    obj=shell(args.pass_number,fleece); features(args.pass_number)
    # Map source motifs with the same transform, attaching to actual surface.
    mat=bpy.data.materials['Diagnostic_Motifs']; root=bpy.data.objects['Carol_Model']
    for name,x,y,r in DATA['features']['stars']:
        pts=[mapped(x+math.sin(i*math.pi/5)*r*(1 if i%2==0 else .49),y-math.cos(i*math.pi/5)*r*(1 if i%2==0 else .49)) for i in range(10)]
        old.attached_polygon('Carol_Star_'+name,pts,obj,mat,root)
    pts=[]
    for i in range(61):
        a=math.radians(-66-240*i/60); pts.append(mapped(218+45*math.cos(a),172+48*math.sin(a)))
    for i in range(59,0,-1):
        a=math.radians(-104-157*i/60); pts.append(mapped(235+30*math.cos(a),158+33*math.sin(a)))
    if args.pass_number>=3: crescent(obj,mat,root)
    else: old.attached_polygon('Carol_Moon_Attached',pts,obj,mat,root)
    root['stage']='v004 canonical recovery / HUMAN Geometry Gate pending'
    bpy.context.view_layer.update(); assert preserve()==before
    export_diagnostic(out/'v004-mesh.json')
    old.render_evidence(out,args.width)
    for view in old.VIEWS: (out/f'carol-v002-{view}.png').replace(out/f'carol-v004-{view}.png')
    checks=old.validate()
    assert all(math.isfinite(c) for o in bpy.data.objects if o.type=='MESH' for v in o.data.vertices for c in v.co)
    checks['finiteGeometry']=True; checks['v003ProtectedStructureUnchanged']=True
    blend=(args.blend_path or out/'carol-blockout-v004.blend').resolve()
    assert blend!=BASE.resolve(); blend.parent.mkdir(parents=True,exist_ok=True)
    bpy.ops.object.select_all(action='DESELECT'); obj.select_set(True); bpy.context.view_layer.objects.active=obj
    bpy.context.preferences.filepaths.save_version=0; bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    bpy.ops.wm.open_mainfile(filepath=str(blend)); old.validate(); assert preserve()==before
    assert all(sha(ROOT/p)==h for p,h in hashes.items())
    checks['savedBlendReopened']=True
    (out/'validation.json').write_text(json.dumps({'version':4,'pass':args.pass_number,'baselineCommit':'d2b5ddc5a3e225469a432360ad202ca3cade62bb',
        'checks':checks,'preservedHashes':hashes,'protectedStructure':before,'blendSha256':sha(blend),
        'generatorSha256':sha(Path(__file__)),'dataSha256':sha(Path(__file__).with_name('carol-v004-reference-data.json')),
        'status':'HUMAN Geometry Gate pending'},indent=2)+'\n',encoding='utf-8')
    print('V004 saved, reopened, validated',blend)

if __name__=='__main__': main()
