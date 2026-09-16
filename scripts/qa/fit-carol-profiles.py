"""Derive bounded, view-independent cross-section sculpt guides from orthos."""
from pathlib import Path
import json,argparse
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--folder',required=True);a=p.parse_args()
folder=ROOT/a.folder;source=ROOT/'assets/grimo/source/carol/approved-3d'
def mask(path):return np.asarray(Image.open(path).convert('RGBA'))[:,:,3]>127
def box(m):
 y,x=np.where(m);return x.min(),y.min(),x.max()+1,y.max()+1
def smooth(a):return np.convolve(np.pad(a,(2,2),mode='edge'),[1,2,3,2,1],mode='valid')/9
m=mask(folder/'top-clay.png');r=mask(source/'carol-top-plan-transparent.png');mb=box(m);rb=box(r)
rows=[]
for s in np.linspace(0,1,61):
 my=min(mb[3]-1,round(mb[1]+s*(mb[3]-mb[1]-1)));ry=min(rb[3]-1,round(rb[1]+s*(rb[3]-rb[1]-1)))
 mx=np.where(m[my])[0];rx=np.where(r[ry])[0]
 ratio=(len(rx) and (rx[-1]-rx[0]+1)/(rb[3]-rb[1])*(mb[3]-mb[1])/max(1,mx[-1]-mx[0]+1)) if len(mx) else 1
 rows.append([(my+.5-m.shape[0]/2)*5.6/m.shape[0],float(np.clip(ratio,.82,1.15)) if .08<s<.96 else 1])
ratios=smooth(np.array(rows)[:,1]);top=[[row[0],float(ratios[i])] for i,row in enumerate(rows)]
m=mask(folder/'side-clay.png');r=mask(source/'carol-side-ortho-transparent.png');mb=box(m);rb=box(r);rows=[]
for s in np.linspace(0,1,61):
 mx=min(mb[2]-1,round(mb[0]+s*(mb[2]-mb[0]-1)));rx=min(rb[2]-1,round(rb[0]+s*(rb[2]-rb[0]-1)))
 my=np.where(m[:,mx])[0];ry=np.where(r[:,rx])[0]
 dz=((my[0]-mb[1])/(mb[3]-mb[1])-(ry[0]-rb[1])/(rb[3]-rb[1]))*(mb[3]-mb[1])*5.6/m.shape[0] if len(my) and len(ry) else 0
 rows.append([(mx+.5-m.shape[1]/2)*5.6/m.shape[1],float(np.clip(dz,-.20,.20)) if .1<s<.88 else 0])
offsets=smooth(np.array(rows)[:,1]);side=[[row[0],float(offsets[i])] for i,row in enumerate(rows)]
output={'source_iteration':a.folder,'method':'Bounded smooth world-Y cross-section deformation. Same vertices for all cameras; no camera-conditioned geometry. Validate all six views after applying.','top_x_scale_by_world_y':top,'side_crown_z_offset_by_world_y':side}
(folder/'profile-fit.json').write_text(json.dumps(output,indent=2))
print('Wrote profile-fit.json; X scale range',float(ratios.min()),float(ratios.max()),'; crown offset range',float(offsets.min()),float(offsets.max()))
