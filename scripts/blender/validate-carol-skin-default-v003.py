"""Product focused checks on the reopened v003 Skin and its v004 source."""
import importlib.util
import json
import math
import sys
from pathlib import Path

import bpy

sys.dont_write_bytecode = True
from mathutils import Vector
from mathutils.bvhtree import BVHTree

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('builder', HERE/'build-carol-skin-default-v003.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
spec2 = importlib.util.spec_from_file_location('ear_util', HERE/'build-carol-ear-production-v002.py')
util = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(util)


def skin_snapshot():
    return {n:builder.snapshot(bpy.data.objects[n]) for n in
            (builder.SKIN_MESHES | builder.SKIN_CURVES | builder.SKIN_EMPTIES)-{'EAR_L','EAR_R'}}


def material_state():
    used={m for n in builder.SKIN_MESHES-{'EAR_L','EAR_R'}
          for m in bpy.data.objects[n].data.materials if m}
    result={}
    for material in used:
        nodes=[]
        if material.use_nodes:
            for node in material.node_tree.nodes:
                sockets=[]
                for index,socket in enumerate(node.inputs):
                    if hasattr(socket,'default_value'):
                        value=socket.default_value
                        if hasattr(value,'__iter__') and not isinstance(value,str):
                            value=tuple(round(float(x),8) for x in value)
                        elif isinstance(value,(int,float)):
                            value=round(float(value),8)
                        else:
                            value=str(value)
                        sockets.append((index,socket.name,value))
                nodes.append((node.name,node.type,tuple(sockets)))
            links=sorted((l.from_node.name,l.from_socket.name,l.to_node.name,l.to_socket.name)
                         for l in material.node_tree.links)
        else:
            links=[]
        result[material.name]=(sorted(nodes),links)
    return result


def root_check(name):
    ob = bpy.data.objects[name]
    tree = BVHTree.FromObject(bpy.data.objects['CENTRAL_CHASSIS'], bpy.context.evaluated_depsgraph_get())
    ring = ob.data.vertices[:24]
    center = sum((ob.matrix_world@v.co for v in ring),Vector())/len(ring)
    hit,normal,_,distance = tree.find_nearest(center)
    return {'inside_head': (center-hit).dot(normal)<0, 'surface_distance_H':distance}


def main():
    report_path=builder.EVIDENCE/'composition.json'
    composition=json.loads(report_path.read_text(encoding='utf8'))
    bpy.ops.wm.open_mainfile(filepath=str(builder.V004))
    source=skin_snapshot()
    source_materials=material_state()
    bpy.ops.wm.open_mainfile(filepath=str(builder.OUTPUT))
    target=skin_snapshot()
    assert source==target
    assert source_materials==material_state()
    report={'asset':builder.OUTPUT.relative_to(builder.ROOT).as_posix(),
            'saved_reopened':True,'non_ear_skin_objects_identical_to_v004':len(source),
            'non_ear_differences':[],
            'non_ear_material_node_trees_identical_to_v004':True,
            'ear_checks':{n:util.mesh_check(bpy.data.objects[n]) for n in ['EAR_L','EAR_R']},
            'root_checks':{n:root_check(n) for n in ['EAR_L','EAR_R']}}
    left,right=(bpy.data.objects[n] for n in ['EAR_L','EAR_R'])
    report['bilateral_max_mirror_error_H']=max((Vector((a.co.x,-a.co.y,a.co.z))-b.co).length
                                            for a,b in zip(left.data.vertices,right.data.vertices))
    report['finite_skin_geometry']=all(math.isfinite(c) for n in builder.SKIN_MESHES
                                       for v in bpy.data.objects[n].data.vertices for c in v.co)
    visible={o.name for o in bpy.context.scene.objects if o.type in {'MESH','CURVE'}}
    report['visible_geometry_exact_skin_subset']=visible==builder.SKIN_MESHES|builder.SKIN_CURVES
    report['source_sha256_unchanged']={
        'v004':builder.sha(builder.V004)==composition['sources']['v004']['sha256'],
        'ear_v001':builder.sha(builder.EAR)==composition['sources']['ear_v001']['sha256'],
        'skin_v002':builder.sha(builder.ASSETS/'carol-skin-final-v002.blend')==composition['sources']['skin_v002']['sha256']}
    assert report['finite_skin_geometry'] and report['visible_geometry_exact_skin_subset']
    assert all(report['source_sha256_unchanged'].values())
    assert report['bilateral_max_mirror_error_H'] < 1e-6
    assert all(v['inside_head'] for v in report['root_checks'].values())
    print('EAR_CHECKS',json.dumps(report['ear_checks']))
    assert all(c['finite'] and c['nonmanifold_edges']==0 and c['outward_normals'] and
               c['nonadjacent_triangle_intersections']==0 for c in report['ear_checks'].values())
    report['technical_checks_pass']=True
    (builder.EVIDENCE/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print('SKIN_DEFAULT_VALIDATED',json.dumps({'non_ear':len(source),
          'mirror_error':report['bilateral_max_mirror_error_H'],'roots':report['root_checks']}))


if __name__=='__main__':main()
