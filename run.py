import asyncio
from rich.console import Console
from rich.live import Live
from rich.table import Table
from core.event_bus import bus
from core.hub_bridge import bridge
from core.llm_client import llm
from agents.builder.builder_agent import builder
from agents.researcher.researcher_agent import researcher
from agents.revenue.revenue_agent import revenue_agent

console = Console()

async def ceo_brainstorm() -> str:
    """The CEO asks the LLM for a highly profitable, trending idea."""
    print("👑 [CEO] Brainstorming next highly profitable micro-SaaS target...")
    prompt = "Give me ONE highly profitable, trending, and unique micro-SaaS idea for a landing page. Just the name and a 1-sentence description."
    idea = await llm.generate(prompt, "You are a billionaire startup CEO.", max_tokens=100)
    return idea.strip().replace('"', '')

def generate_table() -> Table:
    table = Table(title="👑 AGENT-X EMPIRE: 24/7 CEO MODE")
    table.add_column("Time", style="cyan")
    table.add_column("Agent", style="magenta")
    table.add_column("Action", style="green")

    for event in bus.event_log[-8:]:
        table.add_row(
            event['timestamp'][11:19],
            event['source'].upper(),
            str(event['payload'])[:40] + "..."
        )
    return table

async def main():
    console.print("[bold green]👑 Initializing CEO Agent - 24/7 Infinite Empire Loop...[/bold green]")
    console.print("[yellow]Press CTRL+C to stop the empire.[/yellow]\n")
    
    cycle = 1
    while True:
        console.print(f"\n[bold cyan]--- EMPIRE CYCLE #{cycle} ---[/bold cyan]")
        
        # 1. CEO invents an idea
        idea = await ceo_brainstorm()
        console.print(f"🎯 [CEO] Target Acquired: {idea}")
        
        # 2. Dispatch to the Empire
        await bus.publish({
            "id": f"empire_{cycle}",
            "source": "ceo",
            "target": "researcher",
            "type": "task",
            "payload": {"objective": f"Research and build a high-converting landing page for: {idea}"}
        })

        # 3. Watch the empire work
        with Live(generate_table(), refresh_per_second=2, console=console) as live:
            for _ in range(120): # Wait up to 2 mins for the build
                await asyncio.sleep(1)
                live.update(generate_table())
                if bus.event_log and bus.event_log[-1]['source'] == 'builder' and bus.event_log[-1]['type'] == 'result':
                    break
                    
        console.print(f"🏁 [CEO] Cycle #{cycle} complete. Deployed to GitHub. Sleeping 30s...")
        await asyncio.sleep(30)
        cycle += 1

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        console.print("\n[bold red]🛑 CEO halted.[/bold red]")
