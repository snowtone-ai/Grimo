"""Use gate_capture's camera/material definitions without repeating numerical tests."""
from pathlib import Path
p=Path(__file__).with_name('gate_capture.py')
source=p.read_text(encoding='utf8')
setup=source[:source.index('report={')]
captures=source[source.index('a.setup_render(s)'):]
exec(compile(setup+captures,str(p),'exec'),{'__file__':str(p),'__name__':'__main__'})
