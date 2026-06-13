import asyncio
import aiosqlite
from datetime import datetime
from rich.console import Console
from rich.live import Live
from rich.table import Table
from core.event_bus import bus
from core.hub_bridge import bridge
from agents.builder.builder_agent import builder
from agents.researcher.researcher_agent import researcher
from agents.revenue.revenue_agent import revenue_agent

console = Console()

IDEAS_QUEUE = [
    "Build a single-page landing page for an 'AI Resume Builder' SaaS with a waitlist form.",
    "Build a landing page for a 'Chrome Extension that summarizes YouTube videos' with pricing tiers.",
    "Build a landing page for a 'Freelance Invoice Generator' tool with an email capture."
]

def generate_table() -> Table:
    table = Table(title="🚀 AGENT-X CONTINUOUS AUTOPILOT (Multi-File + Revenue + Git)")
    table.add_column("Time", justify="right", style="cyan", no_wrap=True)
    table.add_column("Type", style="magenta")
    table.add_column("Source → Target", style="green")
    table.add_column("Payload Summary")

    for event in bus.event_log[-12:]:
        payload_str = str(event['payload'])
        table.add_row(
            event['timestamp'][11:19],
            event['type'].upper(),
            f"{event['source']} → {event['target']}",
            payload_str[:45] + ("..." if len(payload_str) > 45 else "")
        )
    return table

async def save_to_db(project_dir: str, idea: str):
    async with aiosqlite.connect("agent_x_projects.db") as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                idea TEXT,
                project_dir TEXT,
                status TEXT
            )
        """)
        await db.execute(
            "INSERT INTO projects (timestamp, idea, project_dir, status) VALUES (?, ?, ?, ?)",
            (datetime.now().isoformat(), idea, project_dir, "SUCCESS")
        )
        await db.commit()
    print(f"💾 [DATABASE] Saved project '{project_dir}' to agent_x_projects.db")

async def main():
    console.print("[bold green]🚀 Initializing AGENT-X Continuous Autopilot...[/bold green]")
    console.print("[bold yellow]Press CTRL+C to stop the loop.[/bold yellow]")
    
    for idea in IDEAS_QUEUE:
        console.print(f"\n[bold cyan]🎯 Starting new project: {idea[:60]}...[/bold cyan]")
        
        await bus.publish({
            "id": f"auto_{int(asyncio.get_event_loop().time())}",
            "source": "user",
            "target": "researcher",
            "type": "task",
            "payload": {"objective": idea}
        })

        max_wait = 120
        for _ in range(max_wait):
            await asyncio.sleep(1)
            if bus.event_log and bus.event_log[-1]['source'] == 'builder':
                last_event = bus.event_log[-1]
                if last_event['type'] in ['result', 'failure']:
                    if last_event['type'] == 'result' and 'project_dir' in last_event['payload']:
                        await save_to_db(last_event['payload'].get('project_dir', 'unknown'), idea)
                    break

    console.print("\n[bold green]✅ Autopilot queue completed! Check your directory for new 'project_XXXX' folders.[/bold green]")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[bold red]🛑 Autopilot manually stopped by user.[/bold red]")
