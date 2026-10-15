"""Record immutable inputs and scoped output hashes; no geometry changes."""
from pathlib import Path
import hashlib,json,subprocess,sys,re
ROOT=Path(__file__).resolve().parents[7]
A=ROOT/'assets/grimo/production/jill/tripo/smartmesh25k-v001'
E=ROOT/'docs/production/jill/evidence/smartmesh25k-v001'
SOURCE=Path(sys.argv[1]).resolve()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT).decode('utf-8').strip()
expected={'cute dragon 3d model (1).fbx':'5e9339437af5ad209c01597997006e96bd90d5489a08c28531ab5faa2b3f31db',
          'cute dragon 3d model (1).glb':'fb960ddb3a6a346508b77e0850c57ce9c6f4cdc7e8aaab035ff31ce03feafad1'}
for name,digest in expected.items():assert sha(SOURCE/name)==sha(A/'input'/name)==digest,name
subprocess.run(['git','merge-base','--is-ancestor','2abea76fad578281f74b9fa628987a80b56ad6dc','HEAD'],cwd=ROOT,check=True)
for name in ['fbx-glb-equivalence.json','raw-import-comparison.json']:
    p=E/name;data=json.loads(p.read_text())
    data['_interpretation']='INTERIM ONLY: FBX quad polygon sets were directly compared with GLB triangle sets. FBX count is not a valid shape mismatch metric. Superseded by editing-source-selection.json; raw GLB import comparison remains valid.'
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
for base in [ROOT/'assets/grimo/production/jill',ROOT/'docs/production/jill']:
    for p in base.rglob('*'):
        if p.is_file() and (p.suffix in ['.py','.md','.json'] or p.name=='.gitattributes'):
            p.write_bytes(p.read_bytes().replace(b'\r\n',b'\n'))
authority=[ROOT/'AGENTS.md',ROOT/'docs/grimo/knowledge/Goal√map.md',ROOT/'docs/production/Handoff.md',
           ROOT/'assets/grimo/source/jill/jill-Identity-canonical.png']
authority.extend((ROOT/'assets/grimo/source/jill/tripo-generation-pose').glob('jill_bodyonly_*.png'))
record={'date':'2026-10-15','gate':'HUMAN_PENDING_HOLD','branch':git('branch','--show-current'),
        'initial_head':'93a8d2480c44e90a9c6a6d693c0fd34f9f4487cb',
        'integrated_production_head':'2abea76fad578281f74b9fa628987a80b56ad6dc',
        'motion_contract_main_revision':'940fc5ee3d9c2d155031a0c3030034d4999dea16',
        'inputs_sha256':expected,'original_upload_and_copy_hashes_equal':True,
        'single_editing_source':'input/cute dragon 3d model (1).fbx',
        'editable_master':'jill-geometry-master.blend','master_sha256':sha(A/'jill-geometry-master.blend'),
        'derived_glb_sha256':sha(A/'jill-repaired-neutral.glb'),
        'authority_sha256':{p.relative_to(ROOT).as_posix():sha(p) for p in authority},
        'visual_review':'Boards 00-09 including 03b reviewed: neutral before/after, transition midpoint, peak front/side/3Q, contacts. Missing approved pose refs and unresolved roots/face => HOLD.',
        'original_workspace_note':'Separate worktree used; original production branch and dirty/untracked work left in place. Concurrent Shushu work progressed independently.',
        'prohibited_operations_performed':[]}
(E/'provenance.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
files=sorted(p for base in [ROOT/'assets/grimo/production/jill',ROOT/'docs/production/jill'] for p in base.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='artifact-manifest.json')
manifest={'scope':'Only Jill deliverables; manifest excludes itself and Python bytecode',
          'files':[{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in files]}
(E/'artifact-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8',newline='\n')
# Check local Markdown targets and image decodability, not unrelated application tests.
for p in files:
    if p.suffix=='.md':
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            if '://' not in link and not link.startswith('#'):assert (p.parent/link.split('#')[0]).exists(),(p,link)
from PIL import Image
for p in files:
    if p.suffix.lower() in ['.png','.jpg','.gif']:
        with Image.open(p) as im:
            im.verify()
print(json.dumps({'verified_files':len(files),'bytes':sum(p.stat().st_size for p in files),'input_hashes_unchanged':True,'links_and_image_files_valid':True}))
