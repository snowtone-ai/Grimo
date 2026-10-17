"""Bounded runtime data integrity; never grants appearance PASS."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
source=(ROOT/'scripts/qa/verify-jill-runtime-v005.py').read_text(encoding='utf8')
source=source.replace("E = ROOT / 'docs/production/jill/texture-return-v005'","E = ROOT / 'docs/production/jill/texture-return-v005/upper-w-local'").replace('jill-textured-review-bounded-v005.glb','jill-upper-w-review-bounded-v005.glb')
exec(compile(source,'<upper W bounded runtime>','exec'),globals())
