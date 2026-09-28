"""Final packet provenance verification; explicitly does not grant visual acceptance."""
from pathlib import Path
import hashlib,json,math,ast
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/carol/evidence/normal-fleece-v003'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
asset=ROOT/'assets/grimo/production/carol/blender/carol-normal-fleece-v003.blend'
audit=json.loads((OUT/'asset-audit.json').read_text());manifest=json.loads((OUT/'render-manifest.json').read_text())
assert sha(asset)==audit['sha256']==manifest['asset_sha256']
assert audit['phase1_state']=='NORMAL_FLEECE_V003_GEOMETRY_FAILED'
assert audit['accepted_skin_unchanged'] and audit['non_finite_vertices']==0
assert all(a['matches_manifest'] for a in audit['authorities'])
assert len(audit['anchors'])==4
assert set(manifest['views'])=={'front','side','3q','rear','top','opposite_side'}
checks={}
for view,item in manifest['views'].items():
    p=OUT/item['file'];assert sha(p)==item['sha256'];im=Image.open(p)
    assert list(im.size)==item['resolution']==[1000,1000]
    assert item['samples']==48 and item['appearance_pass']==0 and item['geometry_attempt']==3
    assert all(math.isfinite(v) for r in item['camera_matrix'] for v in r)
    checks[view]={'sha256':sha(p),'resolution':list(im.size),'samples':item['samples']}
for name in ['01-authority-comparison.jpg','02-geometry-overlay.jpg','03-spatial-review.jpg','04-surface-review.jpg','05-small-scale-review.jpg','authority-contract.json','geometry-measurements.json','semantic-measurements.json','README.md']:
    assert (OUT/name).is_file(),name
for p in (ROOT/'scripts/blender').glob('*carol-normal-fleece-v003.py'):ast.parse(p.read_text(encoding='utf-8'))
result={'technical_packet_verified':True,'visual_production_success':False,'state':audit['phase1_state'],
        'asset_sha256':sha(asset),'accepted_skin_sha256':audit['accepted_skin_sha256'],
        'geometry_attempts':3,'appearance_passes':0,'final_native_views':checks,
        'audit_sha256':sha(OUT/'asset-audit.json'),'manifest_sha256':sha(OUT/'render-manifest.json'),
        'artifact_hashes':{p.name:sha(p) for p in OUT.iterdir() if p.is_file() and p.name!='packet-verification.json'},
        'limitations':['The final geometry failed internal visual review.','Iteration images belong to their historical saved attempts, not the final asset.','No Human, motion, deformation, runtime or device PASS. Phase 2 not started.','Git cleanliness and local/remote equality are checked after commit, outside this self-referential packet.']}
(OUT/'packet-verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'technical_packet_verified':True,'visual_production_success':False,'asset_sha256':sha(asset)},indent=2))
