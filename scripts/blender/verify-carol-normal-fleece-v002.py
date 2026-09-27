"""Verify the final review packet's provenance, never its aesthetic acceptance."""
from pathlib import Path
import hashlib,json
from PIL import Image

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/production/carol/evidence/normal-fleece-v002'
ASSET=ROOT/'assets/grimo/production/carol/blender/carol-normal-fleece-v002.blend'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

audit=json.loads((OUT/'asset-audit.json').read_text())
manifest=json.loads((OUT/'render-manifest.json').read_text())
assert audit['sha256']==manifest['asset_sha256']==sha(ASSET)
assert audit['phase1_state']=='NORMAL_FLEECE_V002_AWAITING_HUMAN_REVIEW'
assert audit['non_finite_vertices']==0
assert all(abs(v)<1e-8 for obj in audit['neutral_fleece_values'].values() for v in obj.values())
assert set(manifest['views'])=={'front','side','3q','rear','top','opposite_side'}
for view,record in manifest['views'].items():
    path=OUT/record['file']
    assert record['sha256']==sha(path), f'Stale render: {view}'
    assert record['resolution']==[1000,1000] and record['samples']==48
    with Image.open(path) as im:assert im.size==(1000,1000) and im.mode=='RGBA'
files=[p for p in OUT.iterdir() if p.suffix in {'.png','.jpg'}]
assert all((OUT/name).is_file() for name in ['01-authority-comparison.jpg','02-spatial-review.jpg','03-surface-review.jpg'])
sources=[ROOT/'scripts/blender'/name for name in [
    'build-carol-normal-fleece-v001.py','build-carol-normal-fleece-v002.py',
    'audit-carol-normal-fleece-v002.py','measure-carol-normal-fleece-v002.py',
    'compose-carol-normal-fleece-v002.py','verify-carol-normal-fleece-v002.py']]
sources += [ROOT/'assets/grimo/source/carol/approved-3d'/name for name in ['carol_front.png','carol_side.png']]
sources += [ROOT/'assets/grimo/source/carol/third-party/savino-star/star.obj']
report={'result':'PASS_TECHNICAL_PACKET_ONLY','asset_sha256':sha(ASSET),
        'human_review':'PENDING','motion_deformation_runtime_device':'NOT_PERFORMED',
        'evidence_sha256':{p.name:sha(p) for p in files},
        'source_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in sources}}
(OUT/'packet-verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({'result':report['result'],'asset_sha256':report['asset_sha256'],'verified_views':len(manifest['views'])}))
