import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

ROOT = os.path.dirname(__file__)
PORT = 8090

class Dashboard(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path == "/":
            with open(os.path.join(ROOT, "dashboard.html")) as f:
                page = f.read()

            self.send_response(200)
            self.send_header("Content-type","text/html")
            self.end_headers()
            self.wfile.write(page.encode())
            return

        self.send_error(404)

print(f"GENESIS DASHBOARD ONLINE")
print(f"http://127.0.0.1:{PORT}")

HTTPServer(("0.0.0.0", PORT), Dashboard).serve_forever()
