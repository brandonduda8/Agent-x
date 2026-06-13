import os
import sys

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from core.task_registry import TaskRegistry
from core.supervisor import Supervisor
from core.state_manager import StateManager

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

tasks = TaskRegistry()
supervisor = Supervisor()
state = StateManager()

PORT = int(os.getenv("PORT", 3001))


# -----------------------------
# STATIC UI
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# API (fallback support)
# -----------------------------
@app.route("/api/tasks")
def get_tasks():
    return jsonify(tasks.list())


@app.route("/api/status")
def status():
    return jsonify({
        "supervisor": supervisor.stats,
        "state": state.get_state()
    })


# -----------------------------
# REAL-TIME STREAMING ENGINE
# -----------------------------
def emit_event(event_type, data):

    socketio.emit("event", {
        "type": event_type,
        "data": data
    })


# Hook into supervisor updates
def push_supervisor_update():

    emit_event("supervisor_update", supervisor.stats)


# Hook into task updates
def push_task_update():

    emit_event("task_update", tasks.list())


# -----------------------------
# SOCKET CONNECTION
# -----------------------------
@socketio.on("connect")
def handle_connect():

    print("[DASHBOARD] Client connected")

    emit_event("system", {
        "status": "connected"
    })


# -----------------------------
# MAIN RUN
# -----------------------------
if __name__ == "__main__":

    print("[AGENT-X v2.1 REAL-TIME DASHBOARD]")

    socketio.run(
        app,
        host="0.0.0.0",
        port=PORT,
        debug=True
    )
