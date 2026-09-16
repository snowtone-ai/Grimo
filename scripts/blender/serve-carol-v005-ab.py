"""Local-only A/B diagnostic; routes are allowlisted, no app integration."""
import argparse,mimetypes,os
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote,urlparse
ROOT=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=3016);p.add_argument('--three',type=Path,default=ROOT.parent/'task-plant-carol3d/node_modules/three');args=p.parse_args()
evidence=ROOT/'docs/production/carol/evidence/hero-geometry-v005'
files={'/':Path(__file__).with_name('carol-v005-ab.html'),'/a.glb':ROOT/'artifacts/carol-v005/ab/carol-a.preview.glb','/b.glb':ROOT/'artifacts/carol-v005/ab/carol-b.preview.glb',
 '/original.glb':ROOT/'assets/grimo/source/carol/historical/carol-15bfa8e-reference.glb','/report':evidence/'README.md'}
for v,name in [('front','front-ortho'),('side','side-ortho'),('back','back-ortho'),('top','top-plan')]:files['/ref/'+v+'.png']=ROOT/'assets/grimo/source/carol/approved-3d'/('carol-'+name+'-transparent.png')
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  route=unquote(urlparse(self.path).path);path=files.get(route)
  if route.startswith('/three/'):
   candidate=(args.three/route[7:]).resolve()
   if candidate.is_relative_to(args.three.resolve()) and candidate.suffix=='.js':path=candidate
  if path is None or not path.is_file():self.send_error(404);return
  body=path.read_bytes();self.send_response(200);self.send_header('Content-Type','text/javascript' if path.suffix=='.js' else 'text/plain; charset=utf-8' if path.suffix=='.md' else mimetypes.guess_type(path.name)[0] or 'application/octet-stream');self.send_header('Content-Length',str(len(body)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(body)
print(f'Carol A/B http://127.0.0.1:{args.port}/',flush=True)
ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
