"""Fit oblique camera pose from measured landmarks; geometry stays immutable.

Least-squares uniform scale/translation registration. Searches orthographic and
finite-distance perspective families; results are evidence, not invented lens
metadata for illustrations. Uses only explicitly visible point correspondence.
"""
import argparse,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
ALIASES={'eye_L_center':'eye_center_L','eye_R_center':'eye_center_R','ear_L_root':'ear_root_L','ear_R_root':'ear_root_R','ear_L_tip':'ear_tip_L','ear_R_tip':'ear_tip_R','nose_center':'nose_center','mouth_corner_L':'mouth_corner_L','mouth_corner_R':'mouth_corner_R','hoof_FL_center':'hoof_front_L','hoof_FR_center':'hoof_front_R','hoof_RL_center':'hoof_rear_L','hoof_RR_center':'hoof_rear_R'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--geometry',required=True);a=p.parse_args()
    source=Path(a.geometry);source=source if source.is_absolute() else ROOT/source
    geo=json.loads(source.read_text(encoding='utf8'))
    refs=json.loads((ROOT/'docs/production/carol/carol-reference-measurements.json').read_text(encoding='utf8'))
    output={'method':'Grid camera pose search, uniform registration, no mesh change','views':{}}
    for view,sign in [('3q-left',-1),('3q-right',1)]:
        ref=refs['views'].get(view,refs['views'].get(view.replace('3q-','three_quarter_'),{}))
        pairs=[]
        for key,name in ALIASES.items():
            row=ref.get('landmarks',{}).get(key)
            if row and name in geo['landmarks_3d'] and isinstance(row.get('pixel'),list):pairs.append((key,geo['landmarks_3d'][name],row['pixel']))
        if len(pairs)<5:
            output['views'][view]={'status':'INSUFFICIENT_CORRESPONDENCE','count':len(pairs)};continue
        xyz=np.array([r[1] for r in pairs]);target=np.array([r[2] for r in pairs]);tc=target-target.mean(0)
        results=[]
        for az in np.arange(18,65.1,1):
            ar=math.radians(sign*az)
            for el in np.arange(0,36.1,1):
                er=math.radians(el);right=np.array([math.cos(ar),math.sin(ar),0]);up=np.array([-math.sin(er)*math.sin(ar),math.sin(er)*math.cos(ar),math.cos(er)])
                toward=np.array([math.cos(er)*math.sin(ar),-math.cos(er)*math.cos(ar),math.sin(er)])
                centered=xyz-np.array([0,0,1.5]);q=np.stack([centered@right,-centered@up],axis=1)
                for distance in [None,8,12,20,40]:
                    screen=q if distance is None else q/(distance-centered@toward)[:,None]*distance
                    pc=screen-screen.mean(0)
                    dot=float((pc*tc).sum());cross=float((pc[:,0]*tc[:,1]-pc[:,1]*tc[:,0]).sum())
                    roll=float(np.clip(math.atan2(cross,dot),math.radians(-18),math.radians(18)))
                    rotation=np.array([[math.cos(roll),-math.sin(roll)],[math.sin(roll),math.cos(roll)]])
                    screen=screen@rotation.T;pc=screen-screen.mean(0)
                    scale=float((pc*tc).sum()/(pc*pc).sum());offset=target.mean(0)-scale*screen.mean(0)
                    residual=screen*scale+offset-target;rmse=float(np.sqrt((residual**2).sum(1).mean()))
                    results.append({'roll_degrees':math.degrees(roll),'azimuth':round(sign*az,3),'elevation':round(float(el),3),'projection':'ORTHO' if distance is None else 'PERSP','distance':distance,'uniform_pixel_scale':scale,'offset_px':offset.tolist(),'rmse_px':rmse,'correspondence_count':len(pairs),'residuals':{r[0]:residual[i].tolist() for i,r in enumerate(pairs)}})
        results.sort(key=lambda r:r['rmse_px']);best=dict(results[0]);best['status']='FIT_CANDIDATE_NOT_ACCEPTANCE';best['best_orthographic']=dict(min((r for r in results if r['projection']=='ORTHO'),key=lambda r:r['rmse_px']))
        output['views'][view]=best
    dest=source.parent/'camera-fit.json';dest.write_text(json.dumps(output,indent=2),encoding='utf8');print(json.dumps(output,indent=2))
if __name__=='__main__':main()
