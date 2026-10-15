"""Positive-area UV triangle overlap; shared borders are not intersections."""
import numpy as np

def overlaps(triangles,tolerance=1e-8):
    t=np.asarray(triangles,dtype=np.float64);n=len(t)
    area=np.abs(np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]))/2
    valid=area>1e-12;lo=t.min(1);hi=t.max(1);cells={};resolution=64
    # Work on atlas space. Validation callers reject out-of-bounds separately.
    for i in np.flatnonzero(valid):
        a=np.floor(lo[i]*resolution).astype(int);b=np.floor(hi[i]*resolution).astype(int)
        for x in range(a[0],b[0]+1):
            for y in range(a[1],b[1]+1):cells.setdefault((x,y),[]).append(i)
    keys=[]
    for ids in cells.values():
        if len(ids)<2:continue
        ids=np.array(ids,dtype=np.int64);ii,jj=np.triu_indices(len(ids),1);keys.append(ids[ii]*n+ids[jj])
    if not keys:return np.empty((0,2),dtype=int),np.flatnonzero(~valid)
    keys=np.unique(np.concatenate(keys));result=[]
    for start in range(0,len(keys),20000):
        k=keys[start:start+20000];ia=k//n;ib=k%n
        bbox=np.all(np.minimum(hi[ia],hi[ib])-np.maximum(lo[ia],lo[ib])>tolerance,axis=1);ia=ia[bbox];ib=ib[bbox]
        if not len(ia):continue
        a=t[ia];b=t[ib];keep=np.ones(len(a),dtype=bool)
        for shape in [a,b]:
            for j in range(3):
                edge=shape[:,(j+1)%3]-shape[:,j];axis=np.stack([-edge[:,1],edge[:,0]],axis=1)
                pa=np.einsum('nij,nj->ni',a,axis);pb=np.einsum('nij,nj->ni',b,axis);eps=tolerance*np.linalg.norm(axis,axis=1)
                keep&=np.minimum(pa.max(1),pb.max(1))-np.maximum(pa.min(1),pb.min(1))>eps
        if keep.any():result.append(np.c_[ia[keep],ib[keep]])
    return np.concatenate(result) if result else np.empty((0,2),dtype=int),np.flatnonzero(~valid)
