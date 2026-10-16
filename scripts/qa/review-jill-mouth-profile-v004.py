"""Local shape-sensitive UV metrics and before/after render contact sheets."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2];E=ROOT/'docs/production/jill/mouth-profile-v004';OLD=ROOT/'docs/production/jill/rig-pretexture-technical-v003';R=E/'renders'
d=np.load(E/'after.npz');prior=np.load(OLD/'after.npz')
assert np.array_equal(d['uv'],prior['uv'])
xyz=d['xyz'][d['tris']];uv=d['uv'][d['loops']];regions=np.load(ROOT/'docs/production/jill/rig-pretexture-v002/surface-contract.npz')['regions'][d['polygons']]
aa=uv[:,1]-uv[:,0];bb=uv[:,2]-uv[:,0];ua=abs(aa[:,0]*bb[:,1]-aa[:,1]*bb[:,0])/2;ga=np.linalg.norm(np.cross(xyz[:,1]-xyz[:,0],xyz[:,2]-xyz[:,0]),axis=1)/2
e1=xyz[:,1]-xyz[:,0];e2=xyz[:,2]-xyz[:,0];length=np.linalg.norm(e1,axis=1);G=np.zeros((len(xyz),2,2));G[:,0,0]=length;G[:,0,1]=np.sum(e1*e2,axis=1)/np.maximum(length,1e-20);G[:,1,1]=2*ga/np.maximum(length,1e-20)
valid=(ga>1e-14)&(ua>1e-14);U=np.stack([uv[:,1]-uv[:,0],uv[:,2]-uv[:,0]],axis=2);sing=np.linalg.svd(U[valid]@np.linalg.inv(G[valid]),compute_uv=False);stretch=np.full(len(xyz),np.inf);stretch[valid]=sing[:,0]/sing[:,1];density=np.sqrt(ua/np.maximum(ga,1e-20))
groups={}
for name in np.unique(regions):
    mask=regions==name;s=stretch[mask];s=s[np.isfinite(s)]
    groups[str(name)]={'triangles':int(sum(mask)),'anisotropy_p50_p95_max':np.percentile(s,[50,95,100]).tolist(),'density_px_per_m_p05_median_p95':{str(n):(np.percentile(density[mask],[5,50,95])*n).tolist() for n in [1024,2048,4096,8192]}}
old=json.loads((E/'after-uv-audit.json').read_text());report={'uv_and_polygon_contract_exact':True,'automatic_triangle_diagonal_changes':int(sum(np.any(d['tris']!=prior['tris'],axis=1))),'overlap_padding_evidence':'after-uv-audit.json; recomputed because Blender automatic polygon diagonals changed with the local depth correction','positive_overlap_pairs':old['positive_overlap_pairs'],'intentional_shared_pairs':old['intentional_shared_pairs'],'minimum_island_gap_uv':old['minimum_island_gap_uv'],'tile_edge_gap_uv':old['tile_edge_gap_uv'],'degenerate_uv_triangles':int(sum(ua<1e-12)),'degenerate_geometry_triangles':int(sum(ga<1e-14)),'groups':groups,'method':'Same principal-stretch/rest-area method as v003; new evaluated polygon triangulation audited exactly, despite identical polygon and loop UV contracts.'}
(E/'uv-geometry-audit.json').write_text(json.dumps(report,indent=2)+'\n')
# The newly retained closed-mouth host skin must not receive a printed mouth.
# Its existing body owner/UV stays unchanged; this is a local paint-fill mask.
repair=json.loads((E/'repair-report.json').read_text());host=set(map(int,repair['local_host_y_fairing']))
owners=json.loads((OLD/'material-ownership.json').read_text())['polygon_owners']
mask=Image.new('L',(4096,4096));draw=ImageDraw.Draw(mask);selected=set()
triangles=d['tris'];polygon_indices=d['polygons']
for ti,verts in enumerate(triangles):
    pi=int(polygon_indices[ti]);centroid=xyz[ti].mean(0)
    if owners[pi]!='body_skin' or not host.intersection(map(int,verts)) or centroid[2]>.626:continue
    draw.polygon([(float(u*4095),float((1-v)*4095)) for u,v in uv[ti]],fill=255);selected.add(pi)
mask.save(E/'mouth-host-fill-mask.png')
(E/'mouth-host-fill-mask.json').write_text(json.dumps({'resolution':4096,'polygons':sorted(selected),'pixels':int(np.count_nonzero(np.array(mask))),'purpose':'Local body-owner mouth neighbourhood, explicit same approved skin fill at closed-mouth return. No UV/material changes; nose excluded by centroid Z<=.626.'},indent=2)+'\n')
def oldfile(state,view):return (R if view.startswith('left') else OLD/'renders')/f'v003-{state}-{view}.png'
def newfile(state,view):return R/f'v004-{state}-{view}.png'
states=['neutral','close-mid','closed','open','blink-mid','blink']
def board(name,rows,width=320):
    canvas=Image.new('RGB',(len(rows[0])*width,len(rows)*(width+28)),(234,237,230));draw=ImageDraw.Draw(canvas)
    for j,row in enumerate(rows):
        for i,(file,label) in enumerate(row):
            canvas.paste(Image.open(file).convert('RGB').resize((width,width),Image.Resampling.LANCZOS),(i*width,j*(width+28)));draw.text((i*width+7,j*(width+28)+width+6),label,fill=(25,35,30))
    canvas.save(E/name,quality=94)
board('face-review.jpg',[[(newfile(s,v),f'v004 {s} {v}') for v in ['front','side','3q']] for s in states])
board('side-before-after.jpg',[[(oldfile(s,'side'),f'v003 {s} side'),(newfile(s,'side'),f'v004 {s} side')] for s in states])
board('side-key-poses.jpg',[[(oldfile(s,'side'),f'v003 {s} side'),(newfile(s,'side'),f'v004 {s} side')] for s in ['neutral','closed','open']])
board('front-3q-before-after.jpg',[[(oldfile(s,'front'),f'v003 {s} front'),(newfile(s,'front'),f'v004 {s} front'),(oldfile(s,'3q'),f'v003 {s} 3q'),(newfile(s,'3q'),f'v004 {s} 3q')] for s in states[:4]])
board('opposite-side-before-after.jpg',[[(oldfile(s,'left-side'),f'v003 {s} left'),(newfile(s,'left-side'),f'v004 {s} left'),(oldfile(s,'left-3q'),f'v003 {s} left 3q'),(newfile(s,'left-3q'),f'v004 {s} left 3q')] for s in states[:4]])
comparisons=[]
for state in states:
    for view in ['front','side','3q']:
        a=np.array(Image.open(oldfile(state,view)).convert('RGB')).astype(int);b=np.array(Image.open(newfile(state,view)).convert('RGB')).astype(int);delta=abs(a-b).max(2);yy,xx=np.where(delta>8)
        comparisons.append({'state':state,'view':view,'changed_pixels_above_8':int(len(xx)),'bbox_above_8':None if not len(xx) else [int(xx.min()),int(yy.min()),int(xx.max()),int(yy.max())]})
recovery={v:bool(np.array_equal(np.array(Image.open(newfile('neutral',v))),np.array(Image.open(newfile('recovery',v))))) for v in ['front','side','3q']}
(E/'render-review.json').write_text(json.dumps({'comparisons':comparisons,'neutral_recovery_pixel_exact':recovery,'human_final_go':False,'note':'Intentional local mouth appearance changes. Pixel differences do not confer Human visual approval.'},indent=2)+'\n');assert all(recovery.values())
print(json.dumps({'groups':groups,'recovery_pixel_exact':recovery},indent=2))
