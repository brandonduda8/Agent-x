#!/bin/bash
echo "🧠 Upgrading AGENT-X with Real Intelligence..."

# 1. Add web search capability to requirements
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
duckduckgo-search
EOF

# 2. Create LLM Configuration
mkdir -p config
cat << 'EOF' > config/settings.yaml
# LLM Configuration
# Option A: Local Termux (Requires 'pkg install ollama' and 'ollama run qwen2.5-coder:1.5b')
# Option B: Cloud API (e.g., Groq, OpenRouter, OpenAI)
llm:
  provider: "ollama" # Change to "openai" if using an API key
  model: "qwen2.5-coder:1.5b" # Use a small, fast model for Termux
  base_url: "http://localhost:11434"
  api_key: "none" # Put your API key here if using cloud
EOF

# 3. Create the Unified LLM Client
mkdir -p core
cat << 'EOF' > core/llm_client.py
import httpx
import yaml
import json
import os

class LLMClient:
    def __init__(self):
        config_path = os.path.join(os.path.dirname(__file__), '../config/settings.yaml')
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)['llm']
            
        self.provider = self.config['provider']
        self.model = self.config['model']
        self.base_url = self.config['base_url']
        self.api_key = self.config['api_key']

    async def generate(self, prompt: str, system_prompt: str = "You are an expert AI agent.") -> str:
        print(f"🧠 [LLM] Thinking with {self.model}...")
        
        if self.provider == "ollama":
            return await self._call_ollama(prompt, system_prompt)
        else:
            return await self._call_openai_compatible(prompt, system_prompt)

    async def _call_ollama(self, prompt: str, system_prompt: str) -> str:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(f"{self.base_url}/api/chat", json={
                "model": self.model,
                "stream": False,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            })
            return response.json()['message']['content']

    async def _call_openai_compatible(self, prompt: str, system_prompt: str) -> str:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(f"{self.base_url}/v1/chat/completions", 
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ]
                })
            return response.json()['choices'][0]['message']['content']

llm = LLMClient()
EOF

# 4. Upgrade the Master Builder Agent
cat << 'EOF' > agents/builder/builder_agent.py
import asyncio
import json
from core.event_bus import bus
from core.llm_client import llm
from tools.code_tools import write_file, run_terminal_command

class BuilderAgent:
    def __init__(self, name="Master-Builder"):
        self.name = name
        bus.subscribe("task", self.on_task_received)

    async def on_task_received(self, event: dict):
        if event['target'] != 'builder':
            return
            
        objective = event['payload']['objective']
        print(f"🛠️ [{self.name}] Received objective: {objective}")
        
        # 1. Ask the LLM to generate a coding plan in strict JSON
        system_prompt = """You are an expert Python/HTML developer. 
        You must output ONLY a valid JSON array of actions to achieve the user's goal.
        Format: [{"action": "write", "path": "filename.ext", "content": "code here"}, {"action": "execute", "command": "bash command"}]
        Do not include markdown formatting or explanations. Just the raw JSON array."""
        
        try:
            raw_response = await llm.generate(f"Goal: {objective}", system_prompt)
            # Clean up response in case LLM adds markdown ticks
            clean_json = raw_response.replace('```json', '').replace('```', '').strip()
            plan = json.loads(clean_json)
        except Exception as e:
            print(f"❌ [{self.name}] LLM failed to generate valid JSON: {e}")
            await bus.publish({"id": f"fail_{event['id']}", "source": "builder", "target": "hub", "type": "failure", "payload": {"task_id": event['id']}})
            return

        # 2. Execute the AI-generated plan
        for step in plan:
            await asyncio.sleep(0.5) # Keep UI smooth
            if step.get('action') == 'write':
                write_file(step['path'], step['content'])
            elif step.get('action') == 'execute':
                output = run_terminal_command(step['command'])
                print(f"📟 [EXEC] {output[:100]}...")
                
        # 3. Report success
        await bus.publish({
            "id": f"res_{event['id']}",
            "source": "builder",
            "target": "hub",
            "type": "result",
            "payload": {"task_id": event['id'], "status": "success", "artifacts": [s['path'] for s in plan if s.get('action') == 'write']}
        })

builder = BuilderAgent()
EOF

# 5. Create the Research Agent (Web Search)
mkdir -p agents/researcher
cat << 'EOF' > agents/researcher/researcher_agent.py
import asyncio
from core.event_bus import bus
from core.llm_client import llm
from duckduckgo_search import DDGS

class ResearcherAgent:
    def __init__(self, name="Researcher"):
        self.name = name
        bus.subscribe("task", self.on_task_received)

    async def on_task_received(self, event: dict):
        if event['target'] != 'researcher':
            return
            
        query = event['payload']['objective']
        print(f"🔍 [{self.name}] Researching: {query}")
        
        # 1. Perform real web search
        try:
            with DDGS() as ddgs:
                results = [r for r in ddgs.text(query, max_results=3)]
                context = "\n".join([f"- {r['title']}: {r['body']}" for r in results])
        except Exception as e:
            context = "Web search failed. Relying on internal knowledge."

        # 2. Synthesize findings
        system_prompt = "You are a market researcher. Summarize the findings into a concise 3-point strategy for building a product."
        summary = await llm.generate(f"Search results:\n{context}\n\nQuery: {query}", system_prompt)
        print(f"📊 [{self.name}] Synthesized Strategy: {summary[:100]}...")

        # 3. Hand off to Builder
        await bus.publish({
            "id": f"build_{event['id']}",
            "source": "researcher",
            "target": "builder",
            "type": "task",
            "payload": {"objective": f"Build a prototype based on this strategy: {summary}"}
        })

researcher = ResearcherAgent()
EOF

# 6. Update the main run.py to trigger the full loop
cat << 'EOF' > run.py
import asyncio
from rich.console import Console
from rich.live import Live
from rich.table import Table
from core.event_bus import bus
from core.hub_bridge import bridge
from agents.builder.builder_agent import builder
from agents.researcher.researcher_agent import researcher

console = Console()

def generate_table() -> Table:
    table = Table(title="🚀 AGENT-X AUTOPILOT CONTROL CENTER (LIVE AI)")
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
    console.print("[bold green]Initializing AGENT-X Autopilot with Real AI...[/bold green]")
    
    # Trigger the full Revenue Loop: User -> Researcher -> Builder -> Hub
    await bus.publish({
        "id": "goal_001",
        "source": "user",
        "target": "researcher",
        "type": "task",
        "payload": {"objective": "Find 3 trending micro-SaaS ideas for AI automation that can be built in a weekend"}
    })

    # Live UI loop
    with Live(generate_table(), refresh_per_second=2, console=console) as live:
        for _ in range(30): # Give it 30 seconds to think and build
            await asyncio.sleep(1)
            live.update(generate_table())
            
    console.print("[bold green]✅ Cycle complete. Check your workspace for AI-generated code![/bold green]")

if __name__ == "__main__":
    asyncio.run(main())
EOF

echo "✅ Upgrades applied! Installing new dependencies..."
pip install -r requirements.txt
echo "🎉 Ready! Run 'python run.py' to watch the AI build your project."
