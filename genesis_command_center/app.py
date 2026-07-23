import json
import http.server
import socketserver
from datetime import datetime

PORT = 8080

PROFILE = {
    "mission": [
        "secure income",
        "housing stability",
        "career transition",
        "technology growth",
        "financial independence"
    ],
    "skills": [
        "customer service",
        "communication",
        "problem solving",
        "learning technology"
    ],
    "targets": [
        "remote technical support",
        "help desk",
        "AI automation assistant",
        "software development pathway"
    ]
}

MISSIONS = [
    {
        "agent": "Opportunity Discovery Agent",
        "mission": "Find 25 matching job opportunities",
        "status": "VERIFIED"
    },
    {
        "agent": "Revenue Agent",
        "mission": "Find 50 business leads",
        "status": "VERIFIED"
    },
    {
        "agent": "Stability Agent",
        "mission": "Find housing resources",
        "status": "VERIFIED"
    }
]


class Dashboard(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        page = f"""
        <html>
        <head>
        <title>Genesis Command Center</title>
        <style>
        body {{
            font-family: Arial;
            background:#111;
            color:#eee;
            padding:30px;
        }}
        .card {{
            background:#222;
            padding:20px;
            margin:15px;
            border-radius:10px;
        }}
        </style>
        </head>

        <body>

        <h1>GENESIS COMMAND CENTER v1</h1>

        <div class="card">
        <h2>Operator Profile</h2>
        <pre>{json.dumps(PROFILE,indent=2)}</pre>
        </div>

        <div class="card">
        <h2>Agent Missions</h2>
        <pre>{json.dumps(MISSIONS,indent=2)}</pre>
        </div>

        <div class="card">
        Last Update:
        {datetime.now()}
        </div>

        </body>
        </html>
        """

        self.send_response(200)
        self.send_header(
            "Content-type",
            "text/html"
        )
        self.end_headers()
        self.wfile.write(page.encode())


print("GENESIS COMMAND CENTER ONLINE")
print(f"Open browser: http://localhost:{PORT}")

server = socketserver.TCPServer(
    ("", PORT),
    Dashboard
)

server.serve_forever()
