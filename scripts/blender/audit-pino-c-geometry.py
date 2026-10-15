"""Pino C: read-only source audit. Run in a factory-startup background Blender.

No operators touch the source files. Diagnostic mesh edits affect duplicates only.
"""
import bpy,bmesh,json,hashlib,math,sys
from pathlib import Path
from collections import Counter,defaultdict
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
ASSET=ROOT/'assets/grimo/production/pino/candidate-c'
OUT=ROOT/'docs/production/pino/evidence/geometry-c-v001'
OUT.mkdir(parents=True,exist_ok=True)

def load(path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if path.suffix=='.glb':bpy.ops.import_scene.gltf(filepath=str(path))
    else:bpy.ops.import_scene.fbx(filepath=str(path))
    return [o for o in bpy.context.scene.objects if o.type=='MESH'][0]

def topology(o):
    me=o.data;me.calc_loop_triangles()
    vs=np.array([tuple(o.matrix_world@v.co) for v in me.vertices])
    tris=np.array([tuple(t.vertices) for t in me.loop_triangles],dtype=int)
    parent=list(range(len(vs)))
    def find(a):
        while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
        return a
    def union(a,b):
        a,b=find(a),find(b)
        if a!=b:parent[b]=a
    edges=defaultdict(list)
    for i,t in enumerate(tris):
        for a,b in zip(t,np.roll(t,-1)):
            union(int(a),int(b));edges[tuple(sorted((int(a),int(b))))].append(i)
    groups=defaultdict(list)
    for i in range(len(vs)):groups[find(i)].append(i)
    comps=sorted(groups.values(),key=len,reverse=True)
    labels=np.zeros(len(vs),dtype=int)
    records=[]
    for k,ids in enumerate(comps):
        labels[ids]=k;p=vs[ids];faces=[i for i,t in enumerate(tris) if find(int(t[0]))==find(ids[0])]
        records.append(dict(id=k,vertices=len(ids),triangles=len(faces),bounds=[p.min(axis=0).tolist(),p.max(axis=0).tolist()],center=p.mean(axis=0).tolist()))
    canon=[tuple(sorted(tuple(np.round(vs[v],7)) for v in t)) for t in tris]
    counts=Counter(canon)
    ar=np.linalg.norm(np.cross(vs[tris[:,1]]-vs[tris[:,0]],vs[tris[:,2]]-vs[tris[:,0]]),axis=1)/2
    tree=BVHTree.FromPolygons([Vector(v) for v in vs],tris.tolist(),all_triangles=True,epsilon=0)
    overlaps=[]
    for a,b in tree.overlap(tree):
        if a<b and set(tris[a]).isdisjoint(tris[b]) and canon[a]!=canon[b]:overlaps.append((a,b))
    bycomp=Counter(tuple(sorted((int(labels[tris[a,0]]),int(labels[tris[b,0]])))) for a,b in overlaps)
    bm=bmesh.new();bm.from_mesh(me)
    report=dict(vertices=len(vs),polygons=len(me.polygons),triangles=len(tris),bounds=[vs.min(axis=0).tolist(),vs.max(axis=0).tolist()],components=records,
        boundary_edges=sum(e.is_boundary for e in bm.edges),nonmanifold_edges=sum(not e.is_manifold for e in bm.edges),inconsistent_winding_edges=sum(e.is_manifold and not e.is_contiguous for e in bm.edges),
        degenerate_triangles=int(np.sum(ar<1e-12)),duplicate_triangle_excess=sum(n-1 for n in counts.values()),
        disjoint_triangle_intersection_pairs=len(overlaps),intersection_component_pairs={str(k):n for k,n in bycomp.items()},
        intersection_sample_centers=[vs[tris[a]].mean(axis=0).tolist() for a,b in overlaps[:100]],
        uv_layers=len(me.uv_layers),shape_keys=len(me.shape_keys.key_blocks) if me.shape_keys else 0,vertex_groups=len(o.vertex_groups),custom_normals=me.has_custom_normals,
        materials=[dict(name=m.name,use_nodes=m.use_nodes) for m in me.materials],armature=o.find_armature() is not None)
    bm.free()
    return report,vs,tris,labels

def main():
    report={};arrays={}
    for ext in ['fbx','glb']:
        o=load(ASSET/'source'/f'cute blue creature 3d model.{ext}')
        r,v,t,l=topology(o);report[ext]=r;arrays[ext]=(v,t,l)
        np.savez_compressed(OUT/f'{ext}-diagnostic-arrays.npz',vertices=v,triangles=t,components=l)
    (OUT/'initial-audit.json').write_text(json.dumps(report,indent=2)+'\n')
    print('AUDIT_SUMMARY',json.dumps(report))

if __name__=='__main__':main()
