"""Audit the authored candidate and actual head cross-sections, no visual PASS."""
import bpy,bmesh,json,math,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[2]
out=root/'docs/production/carol/evidence/reconstruction-v006'
deps=bpy.context.evaluated_depsgraph_get();rows=[];hashes={};duplicates=[]
for ob in bpy.data.objects:
    if ob.type!='MESH':continue
    evaluated=ob.evaluated_get(deps);mesh=evaluated.to_mesh()
    bm=bmesh.new();bm.from_mesh(mesh)
    digest=hashlib.sha256(str([(tuple(v.co)) for v in mesh.vertices]).encode()).hexdigest()
    if digest in hashes:duplicates.append([hashes[digest],ob.name])
    hashes[digest]=ob.name
    rows.append({'name':ob.name,'vertices':len(mesh.vertices),'triangles':sum(len(f.vertices)-2 for f in mesh.polygons),'non_manifold_edges':sum(not e.is_manifold for e in bm.edges),'non_finite_vertices':sum(not all(math.isfinite(c) for c in v.co) for v in mesh.vertices),'hidden_render':ob.hide_render,'scale':list(ob.scale),'modifiers':[m.type for m in ob.modifiers]})
    bm.free();evaluated.to_mesh_clear()
head=bpy.data.objects['Head_Volumetric_Cheeks_Jaw'];mesh=head.data;sections=[]
for label,z in [('chin',.65),('lower_cheek',.85),('mouth',1.0),('eye_line',1.145),('upper_cheek',1.45),('forehead',1.65)]:
    points=[]
    for edge in mesh.edges:
        a,b=[mesh.vertices[i].co for i in edge.vertices]
        if (a.z-z)*(b.z-z)<0:
            q=a+(b-a)*((z-a.z)/(b.z-a.z));points.append(list(q))
    sections.append({'name':label,'z':z,'intersection_count':len(points),'width':max(p[0] for p in points)-min(p[0] for p in points) if points else None,'front_back_depth':max(p[1] for p in points)-min(p[1] for p in points) if points else None,'points':points})
result={'visual_acceptance':'NOT_ACCEPTED','checks':'Evaluated per-object topology, finite coordinates, exact vertex duplicate detection, actual final head edge-plane intersections.','not_checked':['Inter-object collision/interpenetration; cloud overlaps are present.','Production retopology, rig deformation and runtime GLB.'],'mesh_count':len(rows),'triangles':sum(r['triangles'] for r in rows),'non_manifold_edges':sum(r['non_manifold_edges'] for r in rows),'non_finite_vertices':sum(r['non_finite_vertices'] for r in rows),'duplicate_vertex_arrays':duplicates,'objects':rows,'actual_head_cross_sections':sections}
(out/'geometry-audit.json').write_text(json.dumps(result,indent=2));print({k:result[k] for k in ['mesh_count','triangles','non_manifold_edges','non_finite_vertices']})
