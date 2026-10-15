"""Reuse original compressed-image restoration for the separate combined gate."""
from pathlib import Path
import importlib.util,sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2]
s=importlib.util.spec_from_file_location('repack',ROOT/'scripts/3d/repack-shushu-v004-mouth-b.py')
p=importlib.util.module_from_spec(s);s.loader.exec_module(p)
p.OUT=ROOT/'docs/production/shushu/evidence/production-rig-v004-motion-ready'
p.TARGET=p.BASE/'shushu-v004-motion-gate-v001.glb'
if '--v002' in sys.argv:
 p.OUT=p.OUT/'final-v002';p.TARGET=p.BASE/'shushu-v004-motion-gate-v002.glb'
# Keep the established per-evidence texture filename for the shared repacker.
p.main()
