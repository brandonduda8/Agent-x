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
from agents.architect.architect_agent import architect # THE NEW MASTER AGENT

console = Console()

def generate_table() -> Table:
    table = Table(title="🚀 AGENT-X EMPIRE CONTROL CENTER")
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
    console.print("[bold green]🚀 Initializing AGENT-X Empire with Master Agents...[/bold green]")
    
    # 1. SUMMON THE ARCHITECT
    console.print("[bold cyan]🏗️ Asking Architect to build a new tool...[/bold cyan]")
    await bus.publish({
        "id": "tool_req_001",
        "source": "user",
        "target": "architect",
        "type": "tool_request",
        "payload": {"description": "A tool named 'seo_analyzer.py' that contains a function 'analyze_seo(html_content)' which counts the number of <h1> tags and returns a dictionary like {'h1_count': X, 'status': 'good'}."}
    })

    # Wait for the Architect to finish building
    console.print("[yellow]Waiting for Architect to finish building...[/yellow]")
    for _ in range(30):
        await asyncio.sleep(1)
        if any(e.get('type') == 'result' and e.get('source') == 'architect' for e in bus.event_log):
            break

    # 2. TEST THE NEWLY BUILT TOOL
    console.print("[bold green]🧪 Testing the newly built tool...[/bold green]")
    try:
        # Dynamically import the tool the AI just wrote!
        import tools.seo_analyzer
        score = tools.seo_analyzer.analyze_seo("<html><body><h1>Test</h1><h1>Test2</h1></body></html>")
        console.print(f"[bold green]✅ SEO Tool Output: {score}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]❌ Tool import failed: {e}[/bold red]")
        
    # 3. START THE NORMAL AUTOPILOT LOOP
    console.print("\n[bold cyan]🎯 Starting normal Autopilot loop...[/bold cyan]")
    await bus.publish({
        "id": f"auto_{int(asyncio.get_event_loop().time())}",
        "source": "user",
        "target": "researcher",
        "type": "task",
        "payload": {"objective": "Build a landing page for a 'Dog Walking SaaS' with a booking form."}
    })

    # Live UI loop
    with Live(generate_table(), refresh_per_second=2, console=console) as live:
        for _ in range(90): 
            await asyncio.sleep(1)
            live.update(generate_table())
            # Break if the builder finishes
            if bus.event_log and bus.event_log[-1]['source'] == 'builder' and bus.event_log[-1]['type'] in ['result', 'failure']:
                break
            
    console.print("\n[bold green]✅ Empire cycle complete![/bold green]")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[bold red]🛑 Empire manually stopped.[/bold red]")
