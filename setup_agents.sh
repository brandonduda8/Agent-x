#!/bin/bash
echo "🚀 Initializing AGENT-X AUTOPILOT WORKSPACE..."

# Ensure we are in the right directory
mkdir -p ~/agent-x
cd ~/agent-x

# 1. Requirements
cat << 'EOF' > requirements.txt
langgraph
langchain-community
pip install sqlite-utils
aiosqlite
pyyaml
rich
textual
httpx
pydantic
EOF

# 2. Core Event Bus
mkdir -p core
cat << 'EOF' > core/event_bus.py
import asyncio
import json
from datetime import datetime
from typing import Callable, Dict, List

class EventBus:
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.event_log = []

    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    async def publish(self, event: dict):
        event["timestamp"] = datetime.utcnow().isoformat() + "Z"
        self.event_log.append(event)
        print(f"📡 [EVENT BUS] {event['type']} from {event['source']} -> {event['target']}")
        
        callbacks = self.subscribers.get(event['type'], [])
        callbacks.extend(self.subscribers.get('*', []))
        
        for callback in callbacks:
            if asyncio.iscoroutinefunction(callback):
                await callback(event)
            else:
                callback(event)

bus = EventBus()
EOF

# 3. Core Hub Bridge
cat << 'EOF' > core/hub_bridge.py
from .event_bus import bus

class HubBridge:
    def __init__(self):
        self.active_tasks = {}
        bus.subscribe("task", self.handle_task)
        bus.subscribe("result", self.handle_result)
        bus.subscribe("failure", self.handle_failure)

    async def handle_task(self, event: dict):
        target = event['target']
        print(f"🔀 [HUB] Routing task '{event['id']}' to {target} agent...")
        self.active_tasks[event['id']] = "processing"

    async def handle_result(self, event: dict):
        task_id = event['payload'].get('task_id')
        self.active_tasks[task_id] = "completed"
        print(f"✅ [HUB] Task {task_id} completed. Notifying Monitor & Revenue agents.")
        await bus.publish({
            "id": f"opt_{task_id}",
            "source": "hub",
            "target": "monitor",
            "type": "optimization_trigger",
            "payload": {"task_id": task_id, "result": event['payload']}
        })

    async def handle_failure(self, event: dict):
        print(f"⚠️ [HUB] Failure detected in {event['source']}. Triggering recovery.")
        await bus.publish({
            "id": f"retry_{event['id']}",
            "source": "hub",
            "target": "planner",
            "type": "task",
            "payload": {"objective": f"Recover failed task: {event['id']}", "priority": "high"}
        })

bridge = HubBridge()
EOF

# 4. Tools: Code Tools (Termux Safe)
mkdir -p tools
cat << 'EOF' > tools/code_tools.py
import os
import asyncio
import subprocess

def write_file(filepath: str, content: str):
    """Safely write content to a file in the workspace."""
    os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"💾 [CODE TOOL] Wrote {len(content)} bytes to {filepath}")

def run_terminal_command(command: str) -> str:
    """Execute a shell command safely and return output."""
    print(f"⚙️ [CODE TOOL] Executing: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr.strip()}"
    except Exception as e:
        return f"Exception: {str(e)}"
EOF

# 5. Agent: Planner
mkdir -p agents/planner
cat << 'EOF' > agents/planner/planner_agent.py
import asyncio
from core.event_bus import bus

class PlannerAgent:
    def __init__(self, name="Planner"):
        self.name = name
        bus.subscribe("task", self.on_task_received)

    async def on_task_received(self, event: dict):
        if event['target'] != 'planner':
            return
            
        print(f"🧠 [{self.name}] Analyzing objective: {event['payload']['objective']}")
        
        # Simulate breaking down the goal into subtasks
        subtasks = [
            {"id": f"task_{event['id']}_1", "target": "researcher", "objective": "Research market for AI automation micro-SaaS"},
            {"id": f"task_{event['id']}_2", "target": "builder", "objective": "Generate landing page code based on research"}
        ]
        
        for task in subtasks:
            await asyncio.sleep(1) # Simulate thinking time
            await bus.publish({
                "id": task["id"],
                "source": "planner",
                "target": task["target"],
                "type": "task",
                "payload": {"objective": task["objective"], "parent_id": event['id']}
            })

planner = PlannerAgent()
EOF

# 6. Agent: Builder
mkdir -p agents/builder
cat << 'EOF' > agents/builder/builder_agent.py
import asyncio
from core.event_bus import bus
from tools.code_tools import write_file, run_terminal_command

class BuilderAgent:
    def __init__(self, name="Builder"):
        self.name = name
        bus.subscribe("task", self.on_task_received)

    async def on_task_received(self, event: dict):
        if event['target'] != 'builder':
            return
            
        print(f"🛠️ [{self.name}] Received objective: {event['payload']['objective']}")
        
        # Simulate AI generating a plan and executing it
        plan = [
            {"action": "write", "path": "project/index.html", "content": "<!DOCTYPE html><html><body><h1>Agent-X AI Automation</h1><p>Coming Soon</p></body></html>"},
            {"action": "execute", "command": "ls -la project/"}
        ]
        
        for step in plan:
            await asyncio.sleep(1)
            if step['action'] == 'write':
                write_file(step['path'], step['content'])
            elif step['action'] == 'execute':
                run_terminal_command(step['command'])
                
        await bus.publish({
            "id": f"res_{event['id']}",
            "source": "builder",
            "target": "hub",
            "type": "result",
            "payload": {
                "task_id": event['id'],
                "status": "success",
                "artifacts": ["project/index.html"]
            }
        })

builder = BuilderAgent()
EOF

# 7. Main Run Script (Immersive Control Center)
cat << 'EOF' > run.py
import asyncio
from rich.console import Console
from rich.live import Live
from rich.table import Table
from core.event_bus import bus
from core.hub_bridge import bridge
from agents.builder.builder_agent import builder
from agents.planner.planner_agent import planner

console = Console()

def generate_table() -> Table:
    table = Table(title="🚀 AGENT-X AUTOPILOT CONTROL CENTER")
    table.add_column("Time", justify="right", style="cyan", no_wrap=True)
    table.add_column("Type", style="magenta")
    table.add_column("Source → Target", style="green")
    table.add_column("Payload Summary")

    for event in bus.event_log[-10:]:
        payload_str = str(event['payload'])
        table.add_row(
            event['timestamp'][11:19],
            event['type'].upper(),
            f"{event['source']} → {event['target']}",
            payload_str[:45] + ("..." if len(payload_str) > 45 else "")
        )
    return table

async def main():
    console.print("[bold green]Initializing AGENT-X Autopilot...[/bold green]")
    
    # Trigger the Revenue Workflow Loop
    await bus.publish({
        "id": "goal_001",
        "source": "user",
        "target": "planner",
        "type": "task",
        "payload": {"objective": "Research and build a micro-SaaS landing page for AI automation"}
    })

    # Start the immersive live UI
    with Live(generate_table(), refresh_per_second=2, console=console) as live:
        for _ in range(15): # Run loop for a short demo
            await asyncio.sleep(1)
            live.update(generate_table())
            
    console.print("[bold green]✅ Autopilot cycle complete. Check 'project/' directory for artifacts.[/bold green]")

if __name__ == "__main__":
    asyncio.run(main())
EOF

echo "✅ All files generated successfully!"
echo "📦 Installing dependencies (this may take a minute in Termux)..."
pip install -r requirements.txt
echo "🎉 Setup complete! Run 'python run.py' to start the Control Center."
