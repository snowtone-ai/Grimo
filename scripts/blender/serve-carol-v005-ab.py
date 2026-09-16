"""Compatibility entry point: the retired A/B URL now serves v006 review."""
import runpy, sys
from pathlib import Path
if '--port' not in sys.argv:sys.argv.extend(['--port','3016'])
runpy.run_path(str(Path(__file__).with_name('serve-carol-v006-review.py')),run_name='__main__')
