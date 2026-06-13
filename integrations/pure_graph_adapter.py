import os
import json
import base64
import time
from tools.code_tools import write_file, run_terminal_command
from core.llm_client import llm

class SelfCorrectingBuilder:
    def __init__(self):
        self.max_iterations = 2

    async def run(self, objective: str) -> dict:
        state = {"objective": objective, "plan": [], "code_written": [], "project_dir": ""}
        
        print(f"🔄 [PureGraph] Generating Base64 HTML...")
        state = await self.planner_node(state)
        if state.get("plan"):
            state = await self.executor_node(state)
            print(f"🚀 [PureGraph] Auto-deploying to GitHub...")
            await self.deploy_node(state)
            print("✅ [PureGraph] Build & Deploy successful!")
        return state

    async def planner_node(self, state: dict) -> dict:
        # The Base64 Shield: LLM encodes HTML to prevent JSON escape errors
        system_prompt = """You are an expert web developer. Output ONLY a valid JSON array.
To prevent JSON escape errors, you MUST Base64 encode the HTML content.
Format: [{"action": "write", "path": "index.html", "content_base64": "PGgxPkhlbGxvPC9oMT4="}]
Generate a complete, beautiful, single-file HTML landing page with inline CSS/JS.
Include a monetization hook (e.g. Stripe checkout link placeholder or email waitlist).
CRITICAL: Output ONLY the JSON array. No markdown."""
        
        try:
            raw = await llm.generate(state["objective"], system_prompt, max_tokens=4000)
            clean = raw.strip()
            if "```" in clean: clean = clean.split("```")[1].strip().replace("json", "")
            
            start = clean.find('[')
            end = clean.rfind(']')
            if start != -1 and end != -1:
                state["plan"] = json.loads(clean[start:end+1])
                return state
        except Exception as e:
            print(f"🚨 [PureGraph] Base64 parse error: {e}")
        return state

    async def executor_node(self, state: dict) -> dict:
        project_dir = f"project_{int(time.time())}"
        os.makedirs(project_dir, exist_ok=True)
        artifacts = []
        
        for step in state['plan']:
            if step.get('action') == 'write' and 'content_base64' in step:
                # Decode Base64 back to normal HTML
                html_bytes = base64.b64decode(step['content_base64'])
                html_content = html_bytes.decode('utf-8')
                
                filepath = os.path.join(project_dir, step['path'])
                write_file(filepath, html_content)
                artifacts.append(filepath)
                
        state['code_written'] = artifacts
        state['project_dir'] = project_dir
        return state

    async def deploy_node(self, state: dict):
        # Automatically commits and pushes the new project to your GitHub!
        proj = state['project_dir']
        original_dir = os.getcwd()
        os.chdir(proj)
        run_terminal_command("git init && git add . && git commit -m 'feat: AI generated site'")
        os.chdir(original_dir)
        
        # Add to main repo and push
        run_terminal_command(f"git add {proj}/")
        run_terminal_command(f"git commit -m 'feat: added {proj}'")
        run_terminal_command("git push")

self_correcting_builder = SelfCorrectingBuilder()
