"""Attribute-preserving application of the bounded crown reconstruction plan."""
import bpy,numpy as np
def apply(o,plan):
 old=o.data;old.calc_loop_triangles();tri=np.array([t.vertices[:] for t in old.loop_triangles]);assert np.array_equal(tri,plan['old_triangles'])
 keys=old.shape_keys;coordinates={k.name:np.array([v.co[:] for v in k.data]) for k in keys.key_blocks};keymeta={k.name:(k.slider_min,k.slider_max,k.value,k.relative_key.name) for k in keys.key_blocks};weights=[{g.group:g.weight for g in v.groups} for v in old.vertices];groupnames=[g.name for g in o.vertex_groups];drivers=[]
 for fc in keys.animation_data.drivers if keys.animation_data else []:
  drivers.append((fc.data_path,fc.array_index,fc.driver.type,fc.driver.expression,[(v.name,v.type,[(t.id,t.data_path,t.bone_target,t.transform_type,t.transform_space) for t in v.targets]) for v in fc.driver.variables]))
 ref=plan['new_reference'];bary=plan['new_barycentric'];offset=plan['new_offset'];newcoords={name:np.vstack([p,np.einsum('ni,nij->nj',bary,p[tri[ref]])+offset]) for name,p in coordinates.items()}
 # Original per-loop UVs remain exact on retained triangles. New corners use
 # the plan's barycentric source, including UV seams rather than a new texture.
 uv=old.uv_layers.active;uvtri=np.array([[uv.data[j].uv[:] for j in t.loops] for t in old.loop_triangles]);uvrefs=plan['uv_reference'];uvb=plan['uv_barycentric'];newuv=np.einsum('fci,fcij->fcj',uvb,uvtri[uvrefs])
 mesh=bpy.data.meshes.new(old.name+'_CrownLocalRebuild');mesh.from_pydata(newcoords['Basis'],[],plan['faces']);mesh.update()
 for material in old.materials:mesh.materials.append(material)
 layer=mesh.uv_layers.new(name=uv.name)
 for f,values in zip(mesh.polygons,newuv):
  f.use_smooth=True
  for i,value in zip(f.loop_indices,values):layer.data[i].uv=value
 o.data=mesh;o.vertex_groups.clear()
 for name in groupnames:o.vertex_groups.new(name=name)
 allweights=list(weights)
 for ids,b in zip(tri[ref],bary):
  result={}
  for i,t in zip(ids,b):
   for group,weight in weights[i].items():result[group]=result.get(group,0)+t*weight
  allweights.append(result)
 for i,w in enumerate(allweights):
  for group,value in w.items():
   if value>0:o.vertex_groups[group].add([i],value,'REPLACE')
 for name,p in newcoords.items():
  k=o.shape_key_add(name=name);k.data.foreach_set('co',p.astype(np.float32).ravel());k.slider_min,k.slider_max,k.value,_=keymeta[name]
 for name,(_,_,_,relative) in keymeta.items():mesh.shape_keys.key_blocks[name].relative_key=mesh.shape_keys.key_blocks[relative]
 for path,index,typ,expression,variables in drivers:
  fc=mesh.shape_keys.driver_add(path);fc.driver.type=typ;fc.driver.expression=expression
  for name,typ,targets in variables:
   v=fc.driver.variables.new();v.name=name;v.type=typ
   for t,(ident,dp,bone,tt,space) in zip(v.targets,targets):t.id=mesh.shape_keys if ident==keys else ident;t.data_path=dp;t.bone_target=bone;t.transform_type=tt;t.transform_space=space
 mesh.update()
 return {'vertices':len(mesh.vertices),'triangles':len(mesh.polygons),'retained_original_vertex_prefix':len(old.vertices),'shape_keys':len(mesh.shape_keys.key_blocks),'drivers':len(drivers),'packed_materials_retained':True}
