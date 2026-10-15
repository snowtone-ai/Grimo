"""Local diagnostic viewer. Uses an existing PlayCanvas build; installs nothing."""
import argparse,http.server,functools
from pathlib import Path
from urllib.parse import unquote,urlsplit

ROOT=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--engine-root',type=Path,default=ROOT/'node_modules/playcanvas/build')
parser.add_argument('--port',type=int,default=8793)

def main():
    args=parser.parse_args();engine=args.engine_root.resolve()
    if not (engine/'playcanvas.mjs').is_file():parser.error('--engine-root must contain playcanvas.mjs')
    class Handler(http.server.SimpleHTTPRequestHandler):
        def translate_path(self,path):
            uri=unquote(urlsplit(path).path)
            if uri.startswith('/_engine/'):
                target=(engine/uri.removeprefix('/_engine/')).resolve()
                return str(target if target.is_relative_to(engine) else engine/'__invalid__')
            return super().translate_path(path)
    print(f'http://127.0.0.1:{args.port}/scripts/3d/pino-texture-ready-v003-runtime.html',flush=True)
    http.server.ThreadingHTTPServer(('127.0.0.1',args.port),functools.partial(Handler,directory=str(ROOT))).serve_forever()

if __name__=='__main__':main()
