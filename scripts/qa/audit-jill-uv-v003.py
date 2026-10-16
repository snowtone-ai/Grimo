"""Exact positive triangle intersections and island clearance; no raster overlap proxy.

Requires numpy, shapely 2, scipy, Pillow. python this.py before|after
All lengths in normalized atlas units, density uses metre geometry.
"""
from pathlib import Path
import sys,json
import numpy as np
import shapely as sh
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];E=ROOT/'docs/production/jill/rig-pretexture-technical-v003'
label=sys.argv[1];d=np.load(E/(label+'.npz'));uv=d['uv'][d['loops']];xyz=d['xyz'][d['tris']]
regions=np.load(ROOT/'docs/production/jill/rig-pretexture-v002/surface-contract.npz')['regions'][d['polygons']]
comp=np.load(ROOT/'docs/production/jill/rig-other-v001/authority-parts.npz')['component']
parts=np.full(len(d['xyz']),-1);parts[:len(comp)]=comp
tri_parts=parts[d['tris'][:,0]]
cross=lambda q:q[:,0,0]*q[:,1,1]-q[:,0,1]*q[:,1,0]
uarea=abs(cross(uv[:,1:]-uv[:,:1]))/2
garea=np.linalg.norm(np.cross(xyz[:,1]-xyz[:,0],xyz[:,2]-xyz[:,0]),axis=1)/2
polys=sh.polygons(uv);tree=sh.STRtree(polys);ij=tree.query(polys,predicate='intersects');ij=ij[:,ij[0]<ij[1]]
areas=sh.area(sh.intersection(polys[ij[0]],polys[ij[1]]));hit=ij[:,areas>1e-12];ha=areas[areas>1e-12]
# A UV island is topologically connected through an identical position+UV edge.
edges={};rows=[];cols=[]
for ti,(v,q) in enumerate(zip(d['tris'],uv)):
    for a,b in [(0,1),(1,2),(2,0)]:
        key=tuple(sorted([(int(v[a]),*np.round(q[a],7)),(int(v[b]),*np.round(q[b],7))]))
        if key in edges:rows.append(ti);cols.append(edges[key])
        else:edges[key]=ti
n,islands=connected_components(coo_matrix((np.ones(len(rows)),(rows,cols)),shape=(len(uv),len(uv))),directed=False)
ip=[sh.union_all(polys[islands==i]) for i in range(n)]
it=sh.STRtree(ip);pairs=it.query(sh.buffer(ip,32/1024),predicate='intersects');pairs=pairs[:,pairs[0]<pairs[1]]
gaps=sh.distance(np.array(ip,dtype=object)[pairs[0]],np.array(ip,dtype=object)[pairs[1]])
minimum=float(gaps.min()) if len(gaps) else None
# Principal stretches from tangent-plane metric; scale-independent anisotropy.
e1=xyz[:,1]-xyz[:,0];e2=xyz[:,2]-xyz[:,0];l=np.linalg.norm(e1,axis=1)
x=np.sum(e1*e2,axis=1)/np.maximum(l,1e-20);y=2*garea/np.maximum(l,1e-20)
G=np.zeros((len(uv),2,2));G[:,0,0]=l;G[:,0,1]=x;G[:,1,1]=y
valid=(garea>1e-14)&(uarea>1e-14)
U=np.stack([uv[:,1]-uv[:,0],uv[:,2]-uv[:,0]],axis=2)
sing=np.linalg.svd(U[valid]@np.linalg.inv(G[valid]),compute_uv=False)
stretch=np.full(len(uv),np.inf);stretch[valid]=sing[:,0]/sing[:,1]
density=np.sqrt(uarea/np.maximum(garea,1e-20))
def stats(ids):
    z=stretch[ids];z=z[np.isfinite(z)];de=density[ids]
    return {'triangles':int(sum(ids)),'uv_area':float(sum(uarea[ids])),'surface_m2':float(sum(garea[ids])),
        'density_uv_per_m_p05_median_p95':np.percentile(de,[5,50,95]).tolist(),
        'anisotropy_p50_p95_max':np.percentile(z,[50,95,100]).tolist() if len(z) else [],
        'area_weighted_anisotropy_gt4':float(sum(garea[ids&(stretch>4)])/max(sum(garea[ids]),1e-20))}
groups={str(k):stats(regions==k) for k in np.unique(regions)}
for name,ids in [('eye-L',tri_parts==99),('eye-R',tri_parts==98),('wing-L',np.isin(tri_parts,[2,4])),('wing-R',tri_parts==1),('body-L',(tri_parts==0)&(xyz.mean(1)[:,0]>.03)),('body-R',(tri_parts==0)&(xyz.mean(1)[:,0]<-.03))]:groups[name]=stats(ids)
shared=[];other=[]
for a,b in hit.T:
    row={'triangles':[int(a),int(b)],'polygons':d['polygons'][[a,b]].tolist(),'regions':regions[[a,b]].tolist(),'components':tri_parts[[a,b]].tolist()}
    # No intentional sharing is authorized for this atlas. Geometric coincidence is evidence, not intent.
    other.append(row)
report={'label':label,'triangles':len(uv),'islands':n,'positive_overlap_pairs':len(other),'intentional_shared_pairs':shared,
    'overlap_area_pair_sum_uv2':float(sum(ha)),'overlap_examples':other,
    'degenerate_uv_triangles':int(sum(uarea<1e-12)),'degenerate_geometry_triangles':int(sum(garea<1e-14)),
    'minimum_island_gap_uv':minimum,'tile_edge_gap_uv':float(min(uv.min(),1-uv.max())),
    'coverage_union':float(sh.area(sh.union_all(polys))),'groups':groups,
    'resolutions':{str(res):{'minimum_island_gap_px':minimum*res if minimum is not None else None,
        'tile_edge_px':float(min(uv.min(),1-uv.max()))*res,
        'pairs_below_8px':int(sum(gaps*res<8-1e-4)),
        'density_px_per_m_p05_median_p95':(np.percentile(density,[5,50,95])*res).tolist()} for res in [1024,2048,4096,8192]},
    'method':'Shapely exact triangle intersections >1e-12 UV². Edge-connected position+UV islands. Exact polygon distance within 32/1024. No overlap inferred intentional. Density/anisotropy per triangle, rest pose; stretch=principal stretch ratio.'}
(E/(label+'-uv-audit.json')).write_text(json.dumps(report,indent=2)+'\n')
im=Image.new('RGB',(1536,1536),'#181e23');dr=ImageDraw.Draw(im)
for q,i in zip(uv,islands):dr.polygon([(float(u*1535),float((1-v)*1535)) for u,v in q],fill=((int(i)*53)%170+65,(int(i)*97)%170+65,(int(i)*31)%170+65))
im.save(E/(label+'-atlas.png'))
np.savez_compressed(E/(label+'-islands.npz'),islands=islands,stretch=stretch,density=density)
print(json.dumps({k:v for k,v in report.items() if k not in ['groups','overlap_examples']},indent=2))
