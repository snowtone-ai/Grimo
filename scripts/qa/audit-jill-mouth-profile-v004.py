"""Rebind the exact v003 UV audit to the v004 changed triangulation."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
source=(ROOT/'scripts/qa/audit-jill-uv-v003.py').read_text(encoding='utf8').replace('rig-pretexture-technical-v003','mouth-profile-v004')
sys.argv=[__file__,'after']
exec(compile(source,str(ROOT/'scripts/qa/audit-jill-uv-v003.py'),'exec'),globals())
