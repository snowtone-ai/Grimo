"""Check the saved fleece for finite coordinates, winding and intersections."""
import json
import sys
from pathlib import Path
import bpy
import bmesh
import numpy as np
from mathutils.bvhtree import BVHTree

obj = bpy.data.objects['Carol_Fleece_Continuous']
bm = bmesh.new()
bm.from_mesh(obj.data)
assert all(e.is_manifold for e in bm.edges)
assert all(np.isfinite(tuple(v.co)).all() for v in bm.verts)
volume = bm.calc_volume(signed=True)
assert volume > 0
bmesh.ops.triangulate(bm,faces=list(bm.faces))
bm.faces.ensure_lookup_table()
tree = BVHTree.FromBMesh(bm,epsilon=0)
intersections = [(a,b) for a,b in tree.overlap(tree) if a<b and
                 not set(bm.faces[a].verts).intersection(bm.faces[b].verts)]
result = {'fleeceSignedVolume':volume,'triangles':len(bm.faces),
          'nonAdjacentTriangleIntersections':len(intersections),'finiteCoordinates':True}
print(json.dumps(result))
Path(sys.argv[sys.argv.index('--')+1]).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
bm.free()
assert not intersections,'Fleece has self intersections'
