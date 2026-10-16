"""Restore compressed texture bytes/materials after the v003 GLB export."""
from pathlib import Path
import importlib.util,sys
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parents[2];sp=importlib.util.spec_from_file_location('repack',R/'scripts/3d/repack-shushu-v004-mouth-b.py');p=importlib.util.module_from_spec(sp);sp.loader.exec_module(p)
p.OUT=R/'docs/production/shushu/evidence/production-rig-v004-motion-ready/final-v003';p.TARGET=p.BASE/'shushu-v004-motion-gate-v003.glb'
(p.OUT/'Head-mouth-b-local.png').write_bytes((p.OUT.parent/'Head-mouth-gate-retopo.png').read_bytes());p.main()
