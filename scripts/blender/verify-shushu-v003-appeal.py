"""Validate the saved appeal revision, including the visible continuous skin."""
import bpy,json,importlib.util,math,sys
from pathlib import Path
import numpy as np
from mathutils import Vector
spec=importlib.util.spec_from_file_location('appeal',Path(__file__).with_name('refine-shushu-v003-appeal.py'))
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
v=a.v;r=a.r
def controls(o):
    k=o.data.shape_keys
    return {'keys':[x.name for x in k.key_blocks],'drivers':{f.data_path:f.driver.expression for f in k.animation_data.drivers} if k.animation_data else {}}
def visible_eye(side):
    trees=[(v.tree(v.parts['Head']),False),(v.tree(bpy.data.objects['Shushu_Eye.'+side]),True)]
    name='Shushu_LidWall.'+side
    if name in bpy.data.objects:trees.append((v.tree(bpy.data.objects[name]),False))
    sign=1 if side=='L' else -1;xs=np.linspace(.035,.225,301)*sign;zs=np.linspace(.55,.77,341);hits=[]
    for x in xs:
        for z in zs:
            found=[]
            for tree,eye in trees:
                hit,normal,index,d=tree.ray_cast(Vector((x,-1,z)),Vector((0,1,0)))
                if hit is not None:found.append((d,eye))
            if found and min(found)[1]:hits.append((float(x),float(z)))
    points=np.array(hits)
    return {'width':float(np.ptp(points[:,0])),'height':float(np.ptp(points[:,1])),'method':'Nearest front hit including new physical lid sleeve, not pink mask'}
def main():
    report={'baseline':a.BASE,'Human':'PENDING','Tripo':'HOLD','scope':'Saved geometry and proof controls, not final rig or smartphone runtime'}
    a.load(a.BACK/v.ASSET.name)
    old={o.name:controls(o) for o in v.character};old_basis={o.name:np.array([p.co for p in o.data.shape_keys.key_blocks['Basis'].data]) for o in v.character}
    a.load(v.ASSET);continuity={}
    for o in v.character:
        if o.name not in old:
            continuity[o.name]={'added_aperture_sleeve':True,'all_head_control_names':controls(o)['keys']==controls(v.parts['Head'])['keys']}
            assert continuity[o.name]['all_head_control_names'];continue
        current=controls(o);assert current==old[o.name],(o.name,'control/driver changed')
        basis=np.array([p.co for p in o.data.shape_keys.key_blocks['Basis'].data])
        same=basis.shape==old_basis[o.name].shape and np.array_equal(basis,old_basis[o.name])
        if o.get('part')!='MouthInterior':assert same,(o.name,'unplanned neutral change')
        continuity[o.name]={'control_names_and_driver_expressions_identical':True,'source_basis_identical':same,'vertices':len(basis),'render_visible':not o.hide_render}
    report['continuity']=continuity
    report['visible_eyes']={s:visible_eye(s) for s in ['L','R']}
    former=json.loads((v.OUT/'human-gate-revision/eye-measurements-after.json').read_text())
    assert all(abs(report['visible_eyes'][s][d]-former[s][d])<1e-8 for s in ['L','R'] for d in ['width','height'])
    report['seat_skin']=[]
    for t in np.linspace(0,1,21):
        v.reset();v.sit(float(t));vv,tt=v.evaluated(v.parts['Torso'])
        assert np.isfinite(vv).all();minz=float(vv[:,2].min())
        row={'seat':float(t),'visible_skin_min_z':minz,'vertices':len(vv),'triangles':len(tt),'foot_min_z':{}}
        for side,sign in [('L',1),('R',-1)]:
            # Compare the evaluated skin with the retained plantar source frame.
            source,_=v.evaluated(v.parts['Leg.'+side]);low=source[source[:,2]<source[:,2].min()+.005]
            tree=v.tree(v.parts['Torso']);dist=max(tree.find_nearest(Vector(p))[3] for p in low)
            row['foot_min_z'][side]={'source_min_z':float(source[:,2].min()),'plantar_to_skin_max_distance':float(dist)}
            assert dist<.012,(t,side,dist)
        assert -.002<minz<.012,(t,minz)
        report['seat_skin'].append(row)
    v.reset();v.sit(1);vv,tt=v.evaluated(v.parts['Torso'])
    parent=list(range(len(vv)))
    def root(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    edgecounts={}
    for f in tt:
        for i,j in [(f[0],f[1]),(f[1],f[2]),(f[2],f[0])]:
            parent[root(int(i))]=root(int(j));edge=tuple(sorted([int(i),int(j)]));edgecounts[edge]=edgecounts.get(edge,0)+1
    components=len({root(i) for i in range(len(vv))});bad=sum(n!=2 for n in edgecounts.values())
    report['seated_visible_skin_topology']={'connected_components':components,'non_two_face_edges':bad}
    assert components==1 and bad==0
    mouth=bpy.data.objects['Shushu_MouthInterior'];head=v.parts['Head'];report['mouth_states']=[]
    for state in ['neutral','small','full','smile','happy-closed']:
        a.pose(state);vv,_=v.evaluated(mouth);rim=vv[193:257]
        report['mouth_states'].append({'state':state,'rim_width_height':[float(np.ptp(rim[:,0])),float(np.ptp(rim[:,2]))]})
    sweep=[]
    for mode in ['closed-full','small-full','full-smile']:
        for seat,tilt in [(0,0),(1,.7)]:
            for t in np.linspace(0,1,7):
                v.reset();v.sit(seat);v.key('HeadTilt.L',tilt)
                v.key('MouthOpen',1-float(t) if mode=='small-full' else 0)
                v.key('MouthDonorOpen',1-.2*float(t) if mode=='full-smile' else float(t))
                v.key('GentleSmile',float(t) if mode=='full-smile' else .3)
                v.key('Blink.L',.5);v.key('Blink.R',.25)
                vv,_=v.evaluated(mouth);assert np.isfinite(vv).all()
                trees=[v.tree(head),v.tree(mouth)];gaps=0
                for direction in r.VIEWS.values():
                    d=Vector(direction).normalized()
                    for i in range(1,193,4):
                        p=Vector(vv[i]);dist=[tr.ray_cast(p+d*.3,-d)[3] for tr in trees]
                        gaps+=min((x for x in dist if x is not None),default=10)>.301
                assert gaps==0,(mode,seat,t,gaps)
                sweep.append({'transition':mode,'seat':seat,'tilt':tilt,'t':float(t),'rays':144,'rear_or_missing_hits':gaps})
    report['mouth_combination_sweep']=sweep
    v.pose('hold');prop=bpy.data.objects['Inspection_HeldProp'];c=Vector(prop['hold_center']);rad=prop['radius']
    gaps=[v.tree(v.parts['Paw.'+s]).find_nearest(c)[3]-rad for s in ['L','R']];clearance=v.tree(v.parts['Torso']).find_nearest(c)[3]-rad
    assert max(abs(x) for x in gaps)<.0001 and clearance>.002
    report['hold_visible_skin']={'paw_gaps':gaps,'body_clearance':clearance}
    # Record contact/gaze/turn controls actually evaluated, not only their names.
    report['functional_states']={}
    for state in ['self-contact','offer','turn-tilt','rest']:
        v.pose(state);report['functional_states'][state]={o.name:len(v.evaluated(o)[0]) for o in v.character if not o.hide_render}
    for gaze in ['GazeLeft','GazeRight','GazeUp','GazeDown']:
        v.reset();v.key(gaze);assert all(np.isfinite(v.evaluated(bpy.data.objects['Shushu_Eye.'+s])[0]).all() for s in ['L','R'])
    original=json.loads((v.OUT/'source-integrity.json').read_text());assert all(r.sha(a.ROOT/row['path'])==row['sha256'] for row in original)
    protected=json.loads((a.OUT/'protected-inputs.json').read_text());assert all(r.sha(a.ROOT/p)==h for p,h in protected.items())
    report['authority_and_user_input_hashes_preserved']=True
    report['surface_limit']='The continuous torso/legs use evaluated remeshing. Editable original controls and proof retained; evaluated topology varies per pose, requiring final rig/retopology work before game runtime.'
    a.write('focused-checks.json',report);print('APPEAL_FOCUSED_CHECKS_COMPLETE',flush=True)
def happy_lids():
    spec=importlib.util.spec_from_file_location('saved',Path(__file__).with_name('verify-shushu-geometry-v003.py'))
    saved=importlib.util.module_from_spec(spec);spec.loader.exec_module(saved)
    a.load(v.ASSET);v.key('HappyLids',.45)
    checks=saved.check_eye_parallax()
    a.write('happy-lid-parallax.json',{'HappyLids':.45,'states':'upright/rest, symmetric and asymmetric blink','checks':checks,'Human':'PENDING'})
    print('HAPPY_LID_PARALLAX_COMPLETE',flush=True)
if __name__=='__main__':
    if '--happy-lids' in sys.argv:happy_lids()
    else:main()
