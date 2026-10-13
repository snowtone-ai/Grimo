"""Reopen the delivered files and inspect actual saved geometry/animation."""
import bpy,json,hashlib,struct,sys
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/shushu/evidence/geometry-v003'
ASSET=ROOT/'assets/grimo/production/shushu/blender/shushu-geometry-v003.blend'
PROOF=ASSET.with_name('shushu-geometry-v003-proof.blend')

def geometry(o):
    bpy.context.view_layer.update();ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=ev.to_mesh();m.calc_loop_triangles()
    v=[ev.matrix_world@p.co for p in m.vertices];f=[p.vertices[:] for p in m.loop_triangles];ev.to_mesh_clear();return v,f

def bvh(o):
    v,f=geometry(o);return BVHTree.FromPolygons(v,f,all_triangles=True)

def check_eye_parallax():
    """Check the inspected eye regions for rays falling through to the rear head."""
    objects=[bpy.data.objects[name] for name in ['Shushu_Head','Shushu_Eye.L','Shushu_Eye.R','Shushu_LidWall.L','Shushu_LidWall.R'] if name in bpy.data.objects]
    def key(name,value):
        for o in bpy.data.objects:
            if o.type=='MESH' and o.data.shape_keys and name in o.data.shape_keys.key_blocks:o.data.shape_keys.key_blocks[name].value=value
    def distance(trees,origin,direction):
        hits=[t.ray_cast(origin,direction)[3] for t in trees]
        return min((d for d in hits if d is not None),default=100.)
    checks={}
    cases=[('upright',(1,-1,0),(0,-.04,.65),.58,(240,400,320,416)),('rest',(1,-1,.12),(0,0,.49),1.15,(270,354,350,412))]
    for label,direction,target,scale,box in cases:
        key('Seat100',1 if label=='rest' else 0);key('HeadRest',1 if label=='rest' else 0)
        key('Blink.L',0);key('Blink.R',0);trees=[bvh(o) for o in objects]
        d=Vector(direction).normalized();q=(-d).to_track_quat('-Z','Y');center=Vector(target)+3*d
        origins=[center+q@Vector(((x/640-.5)*scale*640/720,(.5-y/720)*scale,0)) for y in range(box[2],box[3],3) for x in range(box[0],box[1],3)]
        origins=[p for p in origins if distance(trees,p,-d)<3.05]
        rows=[]
        for left,right in [(a,a) for a in [0,.25,.5,.7,.85,.95,1]]+[(.7,1),(1,.7)]:
            key('Blink.L',left);key('Blink.R',right);trees=[bvh(o) for o in objects]
            holes=sum(distance(trees,p,-d)>3.05 for p in origins)
            rows.append({'blink_left':left,'blink_right':right,'sample_rays':len(origins),'rear_head_or_missing_hits':holes})
        checks[label]=rows
    for name in ['Seat100','HeadRest','Blink.L','Blink.R']:key(name,0)
    assert all(row['rear_head_or_missing_hits']==0 for rows in checks.values() for row in rows),checks
    return checks

def main():
    result={'authority_main':'d655f9606b2785ac8be7484e5f22b84dbaee9f55','human_visual_gate':'PENDING','Tripo_Studio':'HOLD; no upload'}
    bpy.ops.wm.open_mainfile(filepath=str(ASSET))
    head=bvh(bpy.data.objects['Shushu_Head']);source=bvh(bpy.data.objects['Original_CandidateB_REFERENCE_ONLY']);profiles={}
    for label,x,z in [('nose',0,.64),('muzzle',.03,.63),('cheek_left',.23,.56),('cheek_right',-.23,.56),('forehead',0,.81)]:
        p=Vector((x,-1,z));d=Vector((0,1,0));a=source.ray_cast(p,d)[0];b=head.ray_cast(p,d)[0]
        profiles[label]={'donor_y':a.y,'v003_y':b.y,'difference':b.y-a.y}
    result['source_profile_samples']=profiles
    names=[o.name for o in bpy.data.objects if o.name.startswith('Shushu_')]
    baseline={name:geometry(bpy.data.objects[name])[0] for name in names}
    result['editable_asset']={'character_meshes':len(names),'armatures':sum(o.type=='ARMATURE' for o in bpy.data.objects),'total_shape_controls':sum(len(bpy.data.objects[name].data.shape_keys.key_blocks)-1 for name in names)}
    result['bounded_eye_parallax_checks']=check_eye_parallax()
    glb=ROOT/'assets/grimo/production/shushu/tripo/geometry-v003/shushu-geometry-v003-tripo.glb';data=glb.read_bytes();length,kind=struct.unpack_from('<II',data,12);doc=json.loads(data[20:20+length])
    result['glb_payload']={key:len(doc.get(key,[])) for key in ['meshes','materials','textures','images','skins','animations','cameras']}
    assert all(result['glb_payload'][k]==0 for k in ['materials','textures','images','skins','animations','cameras'])
    cameras=json.loads((OUT/'review-cameras.json').read_text())
    result['identical_review_camera_pairs']={view:cameras['donor-'+view]==cameras['neutral-'+view] for view in ['front','left','right','three-quarter','rear']}
    assert all(result['identical_review_camera_pairs'].values())
    roundtrip=json.loads((OUT/'static-roundtrip.json').read_text())
    for ext in ['fbx','glb']:
        assert hashlib.sha256(glb.with_suffix('.'+ext).read_bytes()).hexdigest()==roundtrip[ext]['sha256']
    bpy.ops.wm.open_mainfile(filepath=str(PROOF));s=bpy.context.scene
    result['proof']={'frame_start':s.frame_start,'frame_end':s.frame_end,'fps':s.render.fps,'markers':[{'frame':m.frame,'name':m.name} for m in s.timeline_markers]}
    resets={}
    for frame in [1,23,35,59,83,101,189,249,273,285]:
        s.frame_set(frame);error=max((a-b).length for name in names for a,b in zip(baseline[name],geometry(bpy.data.objects[name])[0]));resets[str(frame)]=error
        assert error<2e-6,(frame,error)
    result['proof']['neutral_return_max_errors']=resets
    prop=bpy.data.objects['Inspection_HeldProp'];s.frame_set(213);start=prop.location.copy();s.frame_set(237)
    result['proof']['release_prop_displacement']=(prop.location-start).length
    s.frame_set(249);result['proof']['prop_hidden_after_release']=bool(prop.hide_render)
    assert result['proof']['release_prop_displacement']>.10 and prop.hide_render
    manifest=json.loads((ROOT/'docs/production/shushu/evidence/candidate-b-8481/input-manifest.json').read_text())
    sources=[]
    for row in manifest['files'][:2]:
        # Original manifest paths are repository-relative.
        path=ROOT/row['path'];actual=hashlib.sha256(path.read_bytes()).hexdigest();assert actual==row['sha256'];sources.append({'path':row['path'],'sha256':actual})
    result['unchanged_original_donors']=sources
    result['delivered_files']=[{'path':str(p.relative_to(ROOT)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [ASSET,PROOF,glb,glb.with_suffix('.fbx')]]
    (OUT/'saved-artifact-checks.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('SAVED_ARTIFACT_CHECKS_COMPLETE',flush=True)
    if '--preview' in sys.argv:
        s.render.engine='CYCLES';s.cycles.samples=8;s.cycles.use_denoising=True;s.render.resolution_x=360;s.render.resolution_y=405;s.render.resolution_percentage=100
        c=s.camera;target=Vector((0,0,.49));d=Vector((1,-1,.12)).normalized();c.location=target+3*d;c.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=1.15
        dest=OUT/'preview-frames';dest.mkdir(exist_ok=True)
        for frame in range(101,190,4):
            s.frame_set(frame);s.render.filepath=str(dest/f'seat-{frame:03}.png');bpy.ops.render.render(write_still=True)
        target=Vector((0,-.04,.65));d=Vector((0,-1,0));c.location=target+3*d;c.rotation_euler=(-d).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=.50
        for frame in range(1,24,2):
            s.frame_set(frame);s.render.filepath=str(dest/f'blink-{frame:03}.png');bpy.ops.render.render(write_still=True)

if __name__=='__main__':main()
