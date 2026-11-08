"""Local-only browser interface: python web_app.py. Never expose publicly unauthenticated."""
import json
import os
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from src.ai_launchguard.assistant import ReleaseAssistant,QuestionError
from src.ai_launchguard.tools import _load
HTML=(Path(__file__).parent/"static"/"index.html").read_bytes()
class Handler(BaseHTTPRequestHandler):
    def send_json(self,status,obj):
        data=json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Content-Length",str(len(data)))
        self.send_header("Cache-Control","no-store")
        self.end_headers();self.wfile.write(data)
    def do_GET(self):
        if self.path=="/":
            self.send_response(200);self.send_header("Content-Type","text/html; charset=utf-8")
            self.send_header("Content-Length",str(len(HTML)));self.end_headers();self.wfile.write(HTML)
        elif self.path=="/api/health":
            self.send_json(200,{"status":"ok","features":list(_load("features.json"))})
        else:self.send_json(404,{"error":"Not found"})
    def do_POST(self):
        if self.path!="/api/ask":return self.send_json(404,{"error":"Not found"})
        try:
            n=int(self.headers.get("Content-Length","0"))
            if not 0<n<=4096:return self.send_json(413,{"error":"Question too large"})
            body=json.loads(self.rfile.read(n))
            result=ReleaseAssistant().ask(body.get("question",""))
            self.send_json(200,result)
        except (QuestionError,ValueError,TypeError) as exc:
            self.send_json(400,{"error":str(exc)})
        except Exception:
            self.send_json(500,{"error":"Assessment failed"})
if __name__=="__main__":
    port=int(os.getenv("PORT","8765"))
    print(f"Local-only demo: http://127.0.0.1:{port}")
    ThreadingHTTPServer(("127.0.0.1",port),Handler).serve_forever()
