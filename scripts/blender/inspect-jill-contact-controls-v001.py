"""Small, reversible IK target and anchor measurement after saved-blend reopen."""
import bpy,json
from pathlib import Path
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[2];E=R/'docs/production/jill/rig-other-v001'
bpy.ops.wm.open_mainfile(filepath=str(R/'assets/grimo/production/jill/tripo/rig-other-v001/jill-rig-other-v001.blend'))
rig=bpy.data.objects['JILL_RIG'];body=bpy.data.objects['Jill_Body'];rig.animation_data.action=None
channels=json.loads((E/'control-contract.json').read_text())['authoring_properties']
def update():rig.update_tag();bpy.context.view_layer.update()
def reset():
    for c in channels:rig[c]=0.
    rig.pose.bones['DEF_pelvis'].location=(0,0,0);update()
def head(name):return rig.matrix_world@rig.pose.bones[name].head
reset();rows=[]
for limb,tip in [('paw','paw'),('foot','foot')]:
    for side,other in [('L','R'),('R','L')]:
        reset();target=bpy.data.objects[f'CTRL_{limb}_IK.{side}'];matrix=target.matrix_world.copy()
        stationary=head(f'DEF_{tip}.{other}').copy();rig[f'{limb}_ik.{side}']=1.
        target.location+=Vector((.008 if side=='L' else -.008,-.010,.006 if limb=='paw' else 0));update()
        rows.append({'limb':limb,'side':side,'target_displacement':[.008 if side=='L' else -.008,-.010,.006 if limb=='paw' else 0],
          'effector_to_target':float((head(f'DEF_{tip}.{side}')-target.matrix_world.translation).length),
          'opposite_effector_displacement':float((head(f'DEF_{tip}.{other}')-stationary).length),
          'scale_max_delta':max(abs(float(v)-1) for b in rig.pose.bones for v in b.scale)})
        target.matrix_world=matrix
reset();dg=bpy.context.evaluated_depsgraph_get();ev=body.evaluated_get(dg);mesh=ev.to_mesh()
bvh=BVHTree.FromPolygons([body.matrix_world@v.co for v in mesh.vertices],[tuple(p.vertices) for p in mesh.polygons],all_triangles=False)
anchors=[]
for ob in bpy.data.objects:
    if ob.name.startswith('ANCHOR_'):
        point,normal,index,dist=bvh.find_nearest(ob.matrix_world.translation)
        anchors.append({'name':ob.name,'semantic_owner':ob.get('semantic_owner'),'neutral_nearest_surface_distance':dist,'position':list(ob.matrix_world.translation)})
ev.to_mesh_clear()
(E/'contact-control-validation.json').write_text(json.dumps({'ik_target_probes':rows,'anchors':anchors,
 'scope':'Small independent target offsets only. No reach extremes, prop fit, semantic contact surface projection or physical balance certification. Anchor nodes retain bone ownership; offsets are explicit.',
 'human_visual':'PENDING'},indent=2)+'\n',encoding='utf8')
print('CONTACT_CONTROL_COMPLETE',json.dumps(rows))
