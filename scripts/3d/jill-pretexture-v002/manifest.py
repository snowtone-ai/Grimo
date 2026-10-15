"""Hash this isolated delivery and its protected authority inputs."""
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
E = ROOT / 'docs/production/jill/rig-pretexture-v002'
A = ROOT / 'assets/grimo/production/jill/tripo/rig-pretexture-v002'

def describe(path):
    return {'path': str(path.resolve()), 'bytes': path.stat().st_size,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True, encoding='utf8').strip()

protected = [ROOT/'assets/grimo/production/jill/tripo/rig-other-v001'/n for n in ['jill-rig-other-v001.blend', 'jill-rig-other-v001.glb', 'source/jill-v002-authority-donor.blend']]
protected += [ROOT/'assets/grimo/source/jill/jill-Identity-canonical.png']
protected += [ROOT/f'assets/grimo/source/jill/tripo-generation-pose/jill_bodyonly_{v}.png' for v in ['front', 'left', 'right', 'back']]
records = [describe(p) for p in protected]
expected = {'jill-rig-other-v001.blend': '99ed802ad3a35a147d4b1a053b81db47e6d0d8ef24d1cfc93c28d014daae5694',
            'jill-v002-authority-donor.blend': '8c2ded49ec7108c420fead87d01b3ff26deb43e479d14479afc50e6aafd67a97'}
for record in records:
    name = Path(record['path']).name
    if name in expected:
        assert record['sha256'] == expected[name], f'Protected input changed: {name}'

scripts = sorted((ROOT/'scripts/blender').glob('*jill-pretexture*v002.py'))
scripts += [ROOT/'scripts/blender/jill_pretexture_face_v002.py', ROOT/'scripts/blender/compose-jill-pretexture-evidence.py']
files = list(A.rglob('*')) + list(E.rglob('*')) + list(Path(__file__).parent.glob('*')) + scripts
files += [ROOT/'docs/production/jill/HANDOFF.md', ROOT/'docs/production/jill/rig-other-v001/Plan.md']
files = sorted({p.resolve() for p in files if p.is_file() and p.name not in ['Manifest.json', 'RemoteReceipt.json'] and '__pycache__' not in p.parts})
result = {'created_utc': datetime.now(timezone.utc).isoformat(), 'status': 'IMPLEMENTED_REVIEW_HOLD', 'technical_go_candidate': False, 'human_final_go': False,
          'worktree': str(ROOT.resolve()), 'branch': git('branch', '--show-current'),
          'inherited_head': '379fe79ac2561b9a5796a4657c36d503d248cf04',
          'preimplementation_plan_commit': '202eae98ea92be431b4e8062330ab8b637891fa2',
          'authority_main': git('rev-parse', 'origin/main'),
          'hash_scope': 'Raw working-file bytes at the recorded absolute paths. Binary asset hashes survive Git/LFS roundtrip. Text hashes may differ on another checkout because this repository uses core.autocrlf=true.',
          'protected_inputs': records, 'files': [describe(p) for p in files],
          'exclusions': ['Manifest self-hash', 'RemoteReceipt records the already committed/pushed payload separately; no self-referential commit hash'],
          'uv_contract': 'Exact source UV retained in second layer; active UV .006+.88*source with documented local repair and appended face islands. Active UV change is unapproved.',
          'execution': 'No Tripo upload, payment, formal Texture generation, or full Motion production.'}
(E/'Manifest.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
print('MANIFEST_FILES', len(files), 'PROTECTED_INPUTS', len(records))
