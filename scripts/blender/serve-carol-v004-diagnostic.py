"""Loopback-only allowlisted diagnostic viewer; no production runtime integration."""
import argparse
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import mimetypes
from urllib.parse import urlparse,unquote

ROOT=Path(__file__).resolve().parents[2]
ap=argparse.ArgumentParser();ap.add_argument('--historical',type=Path,required=True)
ap.add_argument('--three',type=Path,required=True);ap.add_argument('--candidate',type=Path,required=True)
ap.add_argument('--port',type=int,default=3015);args=ap.parse_args()
files={'/':Path(__file__).with_name('carol-v004-diagnostic.html'),
       '/legacy.glb':args.historical/'public/grimo/carol-3d/carol.glb',
       '/canonical.png':ROOT/'assets/grimo/source/carol/carol-Identity-canonical.png',
       '/v003-mesh.json':ROOT/'artifacts/carol-v004/v003-mesh.json',
       '/v004-mesh.json':args.candidate/'v004-mesh.json'}
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        route=unquote(urlparse(self.path).path);path=files.get(route)
        if route.startswith('/three/'):
            candidate=(args.three/route[len('/three/'):]).resolve()
            if candidate.is_relative_to(args.three.resolve()) and candidate.suffix=='.js':path=candidate
        if route.startswith('/evidence/'):
            candidate=(ROOT/'docs/production/carol/evidence/blockout-v004'/route[len('/evidence/'):]).resolve()
            if candidate.is_relative_to((ROOT/'docs/production/carol/evidence/blockout-v004').resolve()) and candidate.suffix=='.png':path=candidate
        if path is None or not path.is_file():self.send_error(404);return
        body=path.read_bytes();self.send_response(200)
        self.send_header('Content-Type','text/javascript' if path.suffix=='.js' else mimetypes.guess_type(path.name)[0] or 'application/octet-stream')
        self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
print(f'Carol diagnostic: http://127.0.0.1:{args.port}/',flush=True)
ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
