"""Necessary conditions for matching the plates with one rigid orthographic body."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[2]
data=json.loads((root/'docs/production/carol/carol-reference-measurements.json').read_text())
rows=[]
for key in ['eye_R_center','nose_center','ear_R_root','ear_R_tip','hoof_FR_center']:
    values=[]
    for view in ['front','side']:
        r=data['views'][view];b=r['segmentation']['visible_bbox'];p=r['landmarks'][key]
        values.append({'view':view,'normalized_height_from_bottom':(b['y1']+1-p['pixel'][1])/b['height'],'annotation_uncertainty':p['uncertainty_px']/b['height']})
    delta=abs(values[0]['normalized_height_from_bottom']-values[1]['normalized_height_from_bottom'])
    target=.01 if key.startswith(('eye','nose')) else .015
    budget=2*target+sum(v['annotation_uncertainty'] for v in values)
    rows.append({'landmark':key,'values':values,'difference':delta,'two_view_error_plus_annotation_budget':budget,'incompatible_under_assumptions':delta>budget})
result={'status':'REFERENCE_CORRESPONDENCE_CONFLICT','assumptions':['Same anatomical landmark, same pose, opaque full-body silhouette.','Front and Side are horizontal orthographic views; identical world vertical axis.','Independent uniform bbox-height normalization; no vertical stretching.','Manual annotation uncertainty is nominal, not statistically validated.'], 'proof':'A horizontal orthographic camera rotation preserves every world Z coordinate and the whole-body min/max Z. Consequently normalized landmark height is invariant. A model cannot lie within both error intervals when those intervals do not overlap.','conclusion':'Eye and nose annotations require source/correspondence or projection/pose reconciliation before simultaneous strict acceptance can be certified. This does not excuse separate model shape failures.','landmarks':rows}
out=root/'docs/production/carol/evidence/reconstruction-v006/reference-vertical-consistency.json';out.write_text(json.dumps(result,indent=2))
print([(r['landmark'],round(r['difference'],4),r['incompatible_under_assumptions']) for r in rows])
