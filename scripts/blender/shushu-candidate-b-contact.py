"""Search bounded low paw contact with actual evaluated mesh, no limb extension."""
import bpy,sys,math,numpy as np
from pathlib import Path
from mathutils import Vector,Euler
from mathutils.bvhtree import BVHTree
import importlib
sys.dont_write_bytecode = True
sys.path.insert(0,str(Path(__file__).resolve().parent))
audit=importlib.import_module('shushu-candidate-b-audit');deform=importlib.import_module('shushu-candidate-b-deform')

def main():
    bpy.ops.wm.open_mainfile(filepath=str(audit.BLEND))
    o=bpy.data.objects['CandidateB_ScratchCore'];rig=bpy.data.objects['CandidateB_ScratchCore_Rig'];cam=bpy.context.scene.camera
    rig.animation_data_clear();o.data.shape_keys.animation_data_clear();deform.reset(rig,o)
    for obj in bpy.data.objects:
        if obj.name.startswith('FacialRepair_') and obj.data and hasattr(obj.data,'shape_keys') and obj.data.shape_keys:obj.data.shape_keys.animation_data_clear()
    basis,t=deform.evaluated(o)
    sets={}
    for group in deform.components(o.data):
        ids=set(i for face in group for i in o.data.polygons[face].vertices)
        center=np.mean([o.data.vertices[i].co[:] for i in ids],axis=0)
        sets[deform.semantic(center)]=ids
    masks={name:np.array([set(map(int,tri))<=ids for tri in t]) for name,ids in sets.items()}
    trials=[];best=None
    for z in [.395,.420,.445]:
        for reach in [.22,.27,.32]:
            for x in [.08,.11,.14]:
                deform.reset(rig,o)
                for side,sign in [('L',1),('R',-1)]:deform.paw_target(rig,side,(sign*x,-reach,z))
                v,_=deform.evaluated(o);trees={name:BVHTree.FromPolygons([Vector(p) for p in v],t[mask].tolist(),all_triangles=True) for name,mask in masks.items() if name in ['Torso','Head','Paw.L','Paw.R']}
                for cy in [-.26,-.29,-.32]:
                    point=Vector((0,cy,z));dl=trees['Paw.L'].find_nearest(point)[3];dr=trees['Paw.R'].find_nearest(point)[3]
                    radius=(dl+dr)/2;body=trees['Torso'].find_nearest(point)[3]-radius;head=trees['Head'].find_nearest(point)[3]-radius
                    trial={'target_x':x,'target_y':-reach,'target_z':z,'proxy_center':list(point),'proxy_radius':radius,
                           'L_R_contact_radius_difference':abs(dl-dr),'torso_surface_clearance':body,'head_surface_clearance':head}
                    trials.append(trial)
                    if .025<=radius<=.08 and abs(dl-dr)<.003 and body>.003 and head>.015:
                        score=body+head*.1
                        if best is None or score>best[0]:best=(score,trial)
    report={'method':'81 bounded pose/prop combinations; nearest actual triangle surface from per-part BVH; radius is tangent to the two paws; not solid collision, grasp physics or final prop fit',
            'combination_count':len(trials),'feasible_count':sum(.025<=r['proxy_radius']<=.08 and r['L_R_contact_radius_difference']<.003 and r['torso_surface_clearance']>.003 and r['head_surface_clearance']>.015 for r in trials)}
    if best:
        r=best[1];report['best']=r
        deform.reset(rig,o)
        for side,sign in [('L',1),('R',-1)]:deform.paw_target(rig,side,(sign*r['target_x'],r['target_y'],r['target_z']))
        prop=deform.proxy('TEMP_ReachableGiftContact',r['proxy_center'],r['proxy_radius'])
        audit.render(cam,'contact-repaired-both-hold-front',(0,-1,0));audit.render(cam,'contact-repaired-both-hold-threequarter',(1,-1,.12));audit.render(cam,'contact-repaired-both-hold-side',(1,0,0))
        before,_=deform.evaluated(o);report['best']['deformation']=deform.metrics(before,t,basis,t)
        rest=rig.data.bones['Head'].matrix_local.to_3x3();b=rig.pose.bones['Head'];b.rotation_mode='QUATERNION'
        b.rotation_quaternion=(rest.inverted()@Euler((math.radians(10),0,math.radians(12)),'XYZ').to_matrix()@rest).to_quaternion()
        v,_=deform.evaluated(o);tree=BVHTree.FromPolygons([Vector(p) for p in v],t[masks['Head']].tolist(),all_triangles=True)
        clearance=tree.find_nearest(Vector(r['proxy_center']))[3]-r['proxy_radius']
        report['head_touch_while_holding']={'head_angles_world_degrees':[10,0,12],'head_surface_clearance':clearance,
                                          'paw_max_displacement_from_held_pose':float(np.linalg.norm(v[list(sets['Paw.L']|sets['Paw.R'])]-before[list(sets['Paw.L']|sets['Paw.R'])],axis=1).max())}
        audit.render(cam,'contact-hold-plus-head-touch',(1,-1,.12))
        bpy.data.objects.remove(prop,do_unlink=True);deform.reset(rig,o)
        after,_=deform.evaluated(o);report['neutral_return_max_error']=float(np.linalg.norm(after-basis,axis=1).max())
        report['verdict']='CONDITIONAL: bounded geometric contact exists; shoulder repair, real prop fit and natural grasp still required'
    else:report['verdict']='FAIL for searched low target range; no supported bounded sphere grip'
    # Verify neighboring anatomy during localized pressure on untouched-topology control.
    raw=bpy.data.objects['CandidateB_RawSkinningProbe'];rawrig=bpy.data.objects['CandidateB_RawSkinningProbe_Rig']
    deform.reset(rawrig,raw);rv,rt=deform.evaluated(raw);local={}
    for name in ['CheekPressure.L','BellyPressure','SupportCompression']:
        deform.reset(rawrig,raw);raw.data.shape_keys.key_blocks[name].value=1
        current,_=deform.evaluated(raw);delta=np.linalg.norm(current-rv,axis=1)
        masks_local={'eyes':(np.abs(np.abs(rv[:,0])-.139)<.065)&(rv[:,1]<-.16)&(rv[:,2]>.61)&(rv[:,2]<.735),
                     'distal_paws':(np.abs(rv[:,0])>.28)&(rv[:,2]>.27)&(rv[:,2]<.43),
                     'opposite_cheek':(rv[:,0]<-.18)&(rv[:,1]<-.15)&(rv[:,2]>.52)&(rv[:,2]<.63)}
        local[name]={'max_displacement':float(delta.max()),'neighbor_displacements':{k:float(delta[mask].max()) for k,mask in masks_local.items()}}
    deform.reset(rawrig,raw);local['release_max_error']=float(np.linalg.norm(deform.evaluated(raw)[0]-rv,axis=1).max());report['local_pressure_isolation']=local
    audit.write('contact-feasibility.json',report)
    print('CONTACT_COMPLETE',report)

if __name__=='__main__':main()
