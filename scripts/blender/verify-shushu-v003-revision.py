"""Focused checks of the saved local v003 revision, including full-open combinations."""
import bpy,json,math,importlib.util
from pathlib import Path
import numpy as np
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('revision',Path(__file__).with_name('revise-shushu-geometry-v003.py'));r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
def projected(points,direction):
    q=(-Vector(direction).normalized()).to_track_quat('-Z','Y').inverted();a=np.array([q@Vector(p) for p in points])
    return {'bounds':[a.min(0)[:2].tolist(),a.max(0)[:2].tolist()],'width_height':np.ptp(a,axis=0)[:2].tolist()}
def fields():
    h=r.v3.parts['Head'];basis=h.data.shape_keys.key_blocks['Basis'];out={}
    for side in ['L','R']:
        g=h.vertex_groups['Local eyelid thickness.'+side];ws={v.index:next((a.weight for a in v.groups if a.group==g.index),0) for v in h.data.vertices}
        lid=[basis.data[i].co for i,w in ws.items() if w>.99];orbital=[basis.data[i].co for i,w in ws.items() if w>0]
        eye=bpy.data.objects['Shushu_Eye.'+side];cap=[v.co for v in eye.data.shape_keys.key_blocks['Basis'].data][:513]
        out[side]={v:{'front_eye_cap':projected(cap,d),'aperture_lid_inner_edge':projected(lid,d),'orbital_edit_region':projected(orbital,d)} for v,d in r.VIEWS.items()}
        out[side]['wall_thickness']=h.modifiers['Inner eyelid wall.'+side].thickness
    # The diagnostic pink mask can be projected independently, without calling it an eye.
    pink=[b.co for b in basis.data if ((abs(b.co.x)-.134)/.071)**2+((b.co.z-.648)/.084)**2<1.08 and b.co.y<-.135]
    out['pink_diagnostic_only']={v:projected(pink,d) for v,d in r.VIEWS.items()}
    out['pink_donor_measurement']=None
    out['pink_limit']='Original donor FBX/GLB has no encoded pink pattern. Diagnostic mask is separately projected and never counted as eyeball; final texture extent remains UNKNOWN.'
    return out
def controls(o):
    return {'keys':[k.name for k in o.data.shape_keys.key_blocks], 'drivers':{f.data_path:f.driver.expression for f in o.data.shape_keys.animation_data.drivers} if o.data.shape_keys.animation_data else {}}
def main():
    report={'Human_Geometry_Gate':'PENDING','measurement_units':'Donor normalised to approximately 1 unit tall; projection dimensions are scene units','scope':'Local eye, mouth and proximal-thigh checks; no final rig/runtime claim'}
    r.load(r.BACK/r.v3.ASSET.name);old_fields=fields();old_shapes={o.name:controls(o) for o in r.v3.character};old_basis={o.name:np.array([v.co for v in o.data.shape_keys.key_blocks['Basis'].data]) for o in r.v3.character}
    old_seat={}
    for side in ['L','R']:
        o=r.v3.parts['Leg.'+side];old_seat[side]=np.array([v.co for v in o.data.shape_keys.key_blocks['Seat100'].data])
    r.load(r.v3.ASSET);report['separated_projected_regions']={'before':old_fields,'after':fields()}
    continuity={}
    for o in r.v3.character:
        new=controls(o);old=old_shapes[o.name]
        assert all(k in new['keys'] for k in old['keys']);assert all(new['drivers'].get(k)==v for k,v in old['drivers'].items())
        a=np.array([v.co for v in o.data.shape_keys.key_blocks['Basis'].data]);diff=np.linalg.norm(a-old_basis[o.name],axis=1)
        continuity[o.name]={'existing_keys_retained':True,'existing_driver_expressions_retained':True,'basis_changed_vertices':int(sum(diff>1e-7)),'basis_max_displacement':float(diff.max()),'added_keys':[k for k in new['keys'] if k not in old['keys']]}
        if o.get('part') in ['Leg.L','Leg.R','Torso','Paw.L','Paw.R','Ear.L','Ear.R']:assert diff.max()==0
    report['control_and_standing_continuity']=continuity
    report['local_thigh']={}
    for side in ['L','R']:
        o=r.v3.parts['Leg.'+side];basis=o.data.shape_keys.key_blocks['Basis'];a=np.array([v.co for v in o.data.shape_keys.key_blocks['Seat100'].data]);diff=np.linalg.norm(a-old_seat[side],axis=1)
        distal=[i for i,b in enumerate(basis.data) if b.co.z<=.095]
        report['local_thigh'][side]={'changed_vertices':int(sum(diff>1e-7)),'max_displacement':float(diff.max()),'distal_foot_max_displacement':float(diff[distal].max())};assert diff[distal].max()==0
    mouth=bpy.data.objects['Shushu_MouthInterior'];head=r.v3.parts['Head'];mouth_checks=[]
    for label,small,full,smile in [('neutral',0,0,0),('small',1,0,0),('full',0,1,0),('smile',0,.65,1)]:
        r.v3.reset();r.v3.key('MouthOpen',small);r.v3.key('MouthDonorOpen',full);r.v3.key('GentleSmile',smile)
        v,_=r.v3.evaluated(mouth);rim=v[1:];mouth_checks.append({'state':label,'rim_bounds':[rim.min(0).tolist(),rim.max(0).tolist()],'rim_width_height':[float(np.ptp(rim[:,0])),float(np.ptp(rim[:,2]))]})
    report['mouth_apertures']=mouth_checks
    # Focused full-mouth sweep, upright and tilted/seated, with blink + smile.
    sweep=[]
    for seat,tilt,mode in [(0,0,'neutral-to-full'),(1,.7,'neutral-to-full'),(0,0,'small-to-full'),(1,.7,'small-to-full')]:
        for full in np.linspace(0,1,9):
            r.v3.reset();r.v3.sit(seat);r.v3.key('HeadTilt.L',tilt);r.v3.key('MouthDonorOpen',float(full));r.v3.key('MouthOpen',1-float(full) if mode=='small-to-full' else 0);r.v3.key('GentleSmile',.5);r.v3.key('Blink.L',.5);r.v3.key('Blink.R',.25)
            hv,ht=r.v3.evaluated(head);mv,mt=r.v3.evaluated(mouth);trees=[r.v3.tree(head),r.v3.tree(mouth)]
            assert np.isfinite(hv).all() and np.isfinite(mv).all()
            # Rays to interior barycentric bowl points must hit local head/bowl
            # before passing to the back of the head. This probes actual 3D opening.
            points=[Vector(mv[0])*.35+Vector(mv[i])*.325+Vector(mv[1+(i%64)])*.325 for i in range(1,65,2)]
            gaps=0
            for view,d in r.VIEWS.items():
                direction=Vector(d).normalized()
                for p in points:
                    ds=[tr.ray_cast(p+direction*.3,-direction)[3] for tr in trees];nearest=min((a for a in ds if a is not None),default=10)
                    gaps+=nearest>.301
            assert gaps==0,(seat,full,gaps)
            sweep.append({'transition':mode,'seat':seat,'head_tilt':tilt,'full_open':float(full),'mouth_surface_rays':len(points)*3,'rear_or_missing_hits':gaps})
    report['full_mouth_combination_sweep']=sweep;r.v3.reset()
    # The original prop geometry and release timeline remain byte-level control evidence.
    r.load(r.v3.PROOF);report['proof_continuity']={'frame_range':[bpy.context.scene.frame_start,bpy.context.scene.frame_end],'markers':[(m.name,m.frame) for m in bpy.context.scene.timeline_markers]}
    original=json.loads((r.v3.OUT/'source-integrity.json').read_text())
    assert all(r.sha(ROOT/row['path'])==row['sha256'] for row in original)
    report['original_donor_and_visual_authority_hashes_rechecked']=original
    r.write('focused-revision-checks.json',report);print('FOCUSED_REVISION_CHECKS_COMPLETE',flush=True)
if __name__=='__main__':main()
