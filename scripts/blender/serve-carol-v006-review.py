"""Local-only static server for the Carol v006 Human Review page.

The route table intentionally has no B/alternate-model route. Evidence can be
partially generated: missing images and metrics remain visible as PENDING.
"""
import argparse, mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[2]
PAGE = Path(__file__).with_name("carol-v006-review.html")
EVIDENCE = ROOT / "docs/production/carol/evidence/reconstruction-v006"
OLD = ROOT / "docs/production/carol/evidence/blockout-v004"
VIEWS = ("front", "side", "back", "top", "3q-left", "3q-right")
REF_FILES = {
    "front": "carol-front-ortho-transparent.png", "side": "carol-side-ortho-transparent.png",
    "back": "carol-back-ortho-transparent.png", "top": "carol-top-plan-transparent.png",
    "3q-left": "carol-front-3q-left.png", "3q-right": "carol-front-3q-right.png",
}

FILES = {"/": PAGE, "/metrics.json": EVIDENCE / "metrics.json", "/evidence/old-front.png": EVIDENCE / "old-front.png"}
for view in VIEWS:
    FILES[f"/evidence/{view}-reference.png"] = EVIDENCE / f"{view}-reference.png"
    for suffix in ("render", "clay", "overlay", "difference", "silhouette", "old"):
        FILES[f"/evidence/{view}-{suffix}.png"] = EVIDENCE / f"{view}-{suffix}.png"

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return
    def do_GET(self):
        route = unquote(urlparse(self.path).path)
        path = FILES.get(route)
        if path is None or not path.is_file():
            self.send_error(404)
            return
        body = path.read_bytes()
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=3017)
args = parser.parse_args()
print(f"Carol v006 Human Review http://127.0.0.1:{args.port}/", flush=True)
ThreadingHTTPServer(("127.0.0.1", args.port), Handler).serve_forever()
