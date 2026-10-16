"""Focused representative probes; no production Motion or texture generation."""
import bpy,sys,importlib.util,json,math
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from pathlib import Path
import numpy as np
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
sp=importlib.util.spec_from_file_location('v4',ROOT/'scripts/blender/pino-texture-handoff-v004.py');v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
STATES=[('neutral','neutral',0,0,0,0,0),('contact-mid','contact',.5,0,0,0,0),('contact','contact',1,0,0,0,0),('rest-mid','rest',.5,0,0,0,0),('rest','rest',1,0,0,0,0),('tail-L','tail',1,0,0,0,0),('tail-R','tail',-1,0,0,0,0),('half','neutral',0,0,0,.5,.5),('near','neutral',0,0,0,.97,.97),('closed','neutral',0,1,0,1,1),('wink','neutral',0,.4,0,1,0),('combined','contact',.5,0,1,.5,1)]
def normals(ob,r):
 me=ob.data;N=np.array([a.vector[:] for a in me.attributes['PinoCanonicalCornerNormal'].data])
 for k in list(me.shape_keys.key_blocks)[1:]:
  if k.value:N+=k.value*np.array([a.vector[:] for a in me.attributes['PinoDN_'+k.name].data])
 loops=np.array([l.vertex_index for l in me.loops]);M=v.skin_matrices(ob,r);n=np.einsum('nij,nj->ni',M[loops,:3,:3],N);n/=np.maximum(np.linalg.norm(n,axis=1),1e-20)[:,None];return n

def main():
 o,r,sc=v.load();v.reset(r);v.render(sc,'source-neutral')
 o,r,sc=v.load(True);V=v.coords(o);L=v.labels();edges=np.array([e.vertices[:] for e in o.data.edges]);baseedge=np.linalg.norm(V[edges[:,0]]-V[edges[:,1]],axis=1);valid=baseedge>1e-6;o.data.calc_loop_triangles();T=np.array([t.vertices[:] for t in o.data.loop_triangles]);TT=T[np.isin(L[T[:,0]],[2,5])]
 def volume(P):
  q=P[TT];return float(np.einsum('ij,ij->i',q[:,0],np.cross(q[:,1],q[:,2])).sum()/6)
 vol0=volume(V);paws=[np.where((L==0)&(sg*V[:,0]>.265)&(V[:,2]>.24)&(V[:,2]<.38))[0] for sg in [1,-1]]
 masks={'feet':(L==0)&(V[:,2]<.055),'rump':(L==0)&(V[:,2]>.075)&(V[:,2]<.25)&(V[:,1]>-.1),'tail':np.isin(L,[2,5])}
 pawsets=[set(ids) for ids in paws];pawpolys=[[p.vertices[:] for p in o.data.polygons if all(j in ids for j in p.vertices)] for ids in pawsets]
 rows=[]
 for kind in ['contact','rest','tail']:
  for s in ([0,.125,.25,.375,.5,.625,.75,.875,1,.75,.5,.25,0] if kind!='tail' else [0,.25,.5,.75,1,.5,0,-.5,-1,-.5,0]):
   v.body_state(o,r,kind,s,preview=False);P=v.evaluated(o);pa=[P[ids] for ids in paws];ratio=np.linalg.norm(P[edges[:,0]]-P[edges[:,1]],axis=1)[valid]/baseedge[valid]
   trees=[BVHTree.FromPolygons([Vector(p) for p in P],pol,all_triangles=True) for pol in pawpolys] if kind=='contact' else None
   intersections=len(trees[0].overlap(trees[1])) if trees else None
   surface_gap=min(trees[1].find_nearest(Vector(p))[3] for p in pa[0]) if trees else None
   rows.append(dict(paw_triangle_intersections=intersections,paw_vertex_to_surface_gap=surface_gap,kind=kind,s=s,min_z=float(P[:,2].min()),below_floor_1mm=int((P[:,2]<-.001).sum()),region={n:dict(min_z=float(P[m,2].min()),floor_3mm=int((abs(P[m,2])<.003).sum())) for n,m in masks.items()},paw_surface_distance=float(np.linalg.norm(pa[0][:,None]-pa[1][None,:],axis=2).min()),paw_signed_x_gap=float(pa[0][:,0].min()-pa[1][:,0].max()),edge_ratio_p99=float(np.percentile(ratio,99)),edge_ratio_max=float(ratio.max()),tail_volume_ratio=volume(P)/vol0,neutral_max_delta=float(np.linalg.norm(P-V,axis=1).max()) if s==0 else None))
 v.dump('body-probes.json',dict(note='Meters. Rump selection is posterior body surface, not feet. Contact must be judged in renders as well. Tail volume includes original three shells.',samples=rows))
 names=[o.name,'PinoSoftLids_L','PinoSoftLids_R','PinoOralLiner'];expected={};pose=[]
 for label,kind,s,c,l,bl,br in STATES:
  v.body_state(o,r,kind,s,c,l,bl,br,preview=False)
  pose.append(dict(name=label,kind=kind,strength=s,face=[c,l,bl,br],skin_delta={p.name:np.array(r.matrix_world@p.matrix@p.bone.matrix_local.inverted()@r.matrix_world.inverted()).tolist() for p in r.pose.bones},morphs={name:{k.name:float(k.value) for k in list(bpy.data.objects[name].data.shape_keys.key_blocks)[1:]} for name in names}))
  for i,name in enumerate(names):
   ob=bpy.data.objects[name];expected[f'{label}_{i}_position']=v.evaluated(ob);expected[f'{label}_{i}_normal']=normals(ob,r)
  if label in ['neutral','contact-mid','contact','rest-mid','rest','tail-L','tail-R']:
   v.refresh_preview_normals(o,r);v.render(sc,'final-'+label)
 np.savez_compressed(v.TMP/'expected.npz',**expected);v.dump('probe-controls.json',pose)
 # Swatches test semantic visibility; these colors are not saved in the master.
 for name,col in [('Pino_Eye_L',(.025,.10,.20,1)),('Pino_Eye_R',(.025,.10,.20,1)),('Pino_OralInterior',(.03,.018,.018,1))]:bpy.data.materials[name].diffuse_color=col
 for b in [0,.25,.5,.75,.9,.97,1]:
  v.body_state(o,r,bL=b,bR=b);v.render(sc,'final-eye-'+str(b),True)
 for label,kind,s,c,l,bl,br in [STATES[-2],STATES[-1],STATES[-3]]:
  v.body_state(o,r,kind,s,c,l,bl,br);v.render(sc,'final-face-'+label,True)
 for c in [0,.35,.7,1]:
  v.body_state(o,r,c=c);v.render(sc,'final-mouth-'+str(c),True)
if __name__=='__main__':main()
