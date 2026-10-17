"""Local face/eye UV repair with deterministic retained-island packing.
No Smart UV, weld, remesh, shape/weight/material edit. Common atlas stays shared.
"""
import bpy,sys,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
TMP=ROOT/'artifacts/pino-pretexture-v005'
DEST=ROOT/'assets/grimo/production/pino/candidate-c/pretexture-reliability-v005'
OUT=ROOT/'docs/production/pino/evidence/pretexture-reliability-v005'
SRC=ROOT/'assets/grimo/production/pino/candidate-c/texture-handoff-v004/pino-c-texture-handoff-v004.blend'
NAMES=['PINO_C_BASE_RIG_V001','PinoSoftLids_L','PinoSoftLids_R','PinoOralLiner']
def main():
 bpy.ops.wm.open_mainfile(filepath=str(SRC));o=bpy.data.objects[NAMES[0]];m=o.data;V=np.array([p.co[:] for p in m.vertices]);L=np.load(ROOT/'docs/production/pino/evidence/rig-v001/reference-arrays.npz')['components']
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.context.tool_settings.mesh_select_mode=(False,False,True)
 bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='DESELECT');bpy.ops.object.mode_set(mode='OBJECT')
 selected=[]
 for p in m.polygons:
  c=V[list(p.vertices)].mean(0);p.select=bool(L[p.vertices[0]]==0 and c[2]>.50 and c[1]<-.205 and p.normal.y<-.20)
  if p.select:selected.append(p.index)
 # Boundary seams only for this front patch; the solver joins its old fragments.
 edge_faces={}
 for p in m.polygons:
  for ek in p.edge_keys:edge_faces.setdefault(tuple(sorted(ek)),[]).append(p.index)
 selected=set(selected)
 for e in m.edges:
  faces=edge_faces.get(tuple(sorted(e.vertices)),[])
  if any(i in selected for i in faces):e.use_seam=not all(i in selected for i in faces)
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 bpy.ops.object.mode_set(mode='EDIT');bpy.ops.uv.unwrap(method='ANGLE_BASED',margin=.001);bpy.ops.object.mode_set(mode='OBJECT')
 # Keep the low-distortion original eye charts; spherical eye trials overlapped.
 charts=[];facecounts={};selected_vertices={vi for j in selected for vi in m.polygons[j].vertices}
 for name in NAMES:
  ob=bpy.data.objects[name];me=ob.data;par=np.arange(len(me.polygons));edges={}
  def find(a):
   while par[a]!=a:par[a]=par[par[a]];a=par[a]
   return a
  for p in me.polygons:
   ids=list(p.loop_indices)
   for a,b in zip(ids,ids[1:]+ids[:1]):
    va,vb=me.loops[a].vertex_index,me.loops[b].vertex_index;qa,qb=me.uv_layers.active.data[a].uv[:],me.uv_layers.active.data[b].uv[:]
    if va>vb:va,vb=vb,va;qa,qb=qb,qa
    key=(va,vb,*np.round(qa,7),*np.round(qb,7))
    if key in edges:par[find(p.index)]=find(edges[key])
    else:edges[key]=p.index
  groups={}
  for p in me.polygons:groups.setdefault(find(p.index),[]).extend(p.loop_indices)
  for root,loops in groups.items():
   loops=np.array(loops);q=np.array([me.uv_layers.active.data[int(i)].uv[:] for i in loops]);lo=q.min(0);size=q.max(0)-lo
   # Existing planar fragments keep their shape. Scale only after chart formation.
   # The newly unwrapped face is normalized to density comparable to body, then
   # prioritized 2x; eyes use 3x body density instead of ~55 px across at 4K.
   xyz=np.array([me.vertices[me.loops[int(i)].vertex_index].co[:] for i in loops])
   # A chart with >100 formerly selected loops is part of the repaired face.
   faceset={int(me.loops[int(i)].vertex_index) for i in loops}
   isface=name==NAMES[0] and len(faceset&selected_vertices)>100
   iseye=name==NAMES[0] and all(L[i] in [8,9] for i in faceset)
   # UV face unwrap has arbitrary scale; match 0.128 UV/m source density.
   if isface:
    q=(q-lo)*(.128*2.0/max(np.ptp(xyz[:,0]),np.ptp(xyz[:,2]),1e-9))/max(size.max(),1e-9)*max(np.ptp(xyz[:,0]),np.ptp(xyz[:,2]))
   elif iseye:q=(q-lo)*3.0
   else:q=q-lo
   charts.append(dict(name=name,loops=loops,q=q,size=q.max(0),face=isface,eye=iseye))
  facecounts[name]=len(groups)
 # Deterministic shelves; constant >=12 px at 4K chart gap, 6 px border.
 charts.sort(key=lambda c:(-c['size'][1],-c['size'][0],c['name'],int(c['loops'][0])))
 margin=6/4096
 def pack(scale,write=False):
  x=y=margin;row=0;poses=[]
  for c in charts:
   w,h=c['size']*scale
   if x+w+margin>1:x=margin;y+=row+2*margin;row=0
   if y+h+margin>1:return False
   poses.append((x,y));x+=w+2*margin;row=max(row,h)
  if write:
   for c,pos in zip(charts,poses):
    uv=bpy.data.objects[c['name']].data.uv_layers.active
    for li,q in zip(c['loops'],c['q']*scale+pos):uv.data[int(li)].uv=q
  return True
 lo,hi=.01,8.
 for _ in range(30):
  mid=(lo+hi)/2
  if pack(mid):lo=mid
  else:hi=mid
 pack(lo,True)
 for name in NAMES:bpy.data.objects[name].data.uv_layers.active.name='PinoUV_v005'
 DEST.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
 bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(DEST/'pino-c-pretexture-v005.blend'),compress=True)
 (OUT/'uv-edit.json').write_text(json.dumps(dict(method='Angle-based unwrap selected front skin; original eye charts scaled 3x; remaining charts retain local shape; deterministic shared-atlas shelf packing',selected_front_skin_polygons=len(selected),charts=facecounts,prioritized_face_charts=sum(c['face'] for c in charts),prioritized_eye_charts=sum(c['eye'] for c in charts),scale=lo,margin_px_at_4k=6,smart_uv=False,geometry_edit=False,rejected='Projection and spherical eye trials overlapped; retained original eye charts. Correct face selection removes non-face selection propagation.'),indent=2), encoding='utf8', newline='\n')
if __name__=='__main__':main()
