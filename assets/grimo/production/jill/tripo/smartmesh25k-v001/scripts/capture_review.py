import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from audit_common import *
o=bpy.data.objects['JILL_GEOMETRY_MASTER'];m=o.data;scene=bpy.context.scene
proof=json.loads((EVIDENCE/'deformation-validation.json').read_text())
collisions=json.loads((EVIDENCE/'collision-screen.json').read_text())
for ci,c in enumerate(proof['cases']):
    scene.frame_set(1+24*ci+6)
    for view,d in [('front',(0,-1,0)),('rear',(1,2,.35))]:render(scene,'half-'+c['name']+'-'+view,d,(0,0,.5),1.16)
scene.frame_set(1)
render(scene,'proof-neutral-rear',(1,2,.35),(0,0,.5),1.16)
original_slots=list(m.materials);original_indices=[p.material_index for p in m.polygons]
for color,name in [((.58,.68,.55,1),'ScreenNeutral'),((.95,.03,.16,1),'NewSurfaceCrossingCandidate')]:
    mat=bpy.data.materials.new(name);mat.diffuse_color=color;m.materials.append(mat)
scene.display.shading.color_type='MATERIAL';offset=len(original_slots)
m.calc_loop_triangles();tri_polys=[t.polygon_index for t in m.loop_triangles]
for ci,c in enumerate(collisions['cases'][:8]):
    ids=set(i for pair in c['samples'][-1]['new_triangle_pairs'] for i in pair)
    pol=set(tri_polys[i] for i in ids)
    for p in m.polygons:p.material_index=offset+int(p.index in pol)
    scene.frame_set(1+24*ci+12)
    name=c['name'];side=-1 if name.startswith(('WingR','ArmR')) else 1
    if name.startswith('Wing'):d=(side,1,.2);target=(.18*side,.06,.52);scale=.48
    elif name.startswith('Tail'):d=(1,1,.15);target=(0,.19,.29);scale=.64
    else:d=(side,-2,.25);target=(.16*side,-.12,.42);scale=.50
    render(scene,'contact-screen-'+name,d,target,scale)
    scene.frame_set(1)
    render(scene,'contact-neutral-'+name,d,target,scale)
print('REVIEW_CAPTURES_COMPLETE; master not modified or resaved')
