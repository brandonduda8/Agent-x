import os
import json
from tools.code_tools import write_file, run_terminal_command
from core.llm_client import llm

class SelfCorrectingBuilder:
    def __init__(self):
        self.max_iterations = 3

    async def run(self, objective: str) -> dict:
        state = {
            "objective": objective,
            "plan": [],
            "code_written": [],
            "execution_output": "",
            "error_message": "",
            "iteration_count": 0
        }

        while state["iteration_count"] < self.max_iterations:
            state["iteration_count"] += 1
            print(f"🔄 [PureGraph] Iteration {state['iteration_count']} of {self.max_iterations}")

            state = await self.planner_node(state)
            if state.get("error_message") and not state.get("plan"):
                break

            state = await self.executor_node(state)
            action = self.reviewer_node(state)
            
            if action == "success":
                print("✅ [PureGraph] Build successful!")
                return state
            else:
                print("⚠️ [PureGraph] Execution error detected. Looping back to planner to fix it...")
                state["objective"] = f"Original goal: {objective}. \n\nPREVIOUS ATTEMPT FAILED WITH THIS ERROR:\n{state['error_message']}\n\nPlease output the raw HTML code array."

        print("❌ [PureGraph] Max iterations reached. Build failed.")
        return state

    async def planner_node(self, state: dict) -> dict:
        print("🧠 [PureGraph] Planning Barebones MVP...")
        # Overwhelmingly strict prompt to ignore distractions
        system_prompt = """You are an expert web developer. Your ONLY job is to output a valid JSON array of actions to build a web page.
IGNORE any mentions of "no-code", "Figma", or "AI generators" in the user's prompt. You must write raw HTML/CSS/JS code.

You MUST output EXACTLY this JSON array format, nothing else:
[
  {"action": "write", "path": "index.html", "content": "<html><body><h1>Test</h1></body></html>"},
  {"action": "execute", "command": "git init && git add . && git commit -m 'init'"}
]

CRITICAL RULES:
1. The output MUST start with `[` and end with `]`.
2. Do NOT output a JSON object `{}`. Output an array `[]`.
3. Keep the "content" string extremely short (under 10 lines).
4. Escape all inner quotes with backslashes (e.g., \\" or \\').
5. Do NOT include markdown formatting (no ```json) or conversational text."""
        
        json_retries = 0
        raw_response = ""
        
        while json_retries < 2:
            try:
                raw_response = await llm.generate(state["objective"], system_prompt, max_tokens=2000)
                clean = raw_response.strip()
                
                # Strip markdown if present
                if "```" in clean:
                    parts = clean.split("```")
                    if len(parts) >= 3:
                        clean = parts[1].strip()
                        if clean.lower().startswith("json"):
                            clean = clean.split("\n", 1)[1].strip() if "\n" in clean else clean[4:].strip()
                
                start = clean.find('[')
                end = clean.rfind(']')
                
                if start != -1 and end != -1 and end > start:
                    json_str = clean[start:end+1]
                    state["plan"] = json.loads(json_str)
                    print("✅ [PureGraph] JSON parsed successfully!")
                    return state
                else:
                    raise ValueError(f"No JSON array found. start={start}, end={end}")
                    
            except json.JSONDecodeError as e:
                json_retries += 1
                print(f"⚠️ [PureGraph] Invalid JSON. Asking LLM to fix it ({json_retries}/2)...")
                system_prompt = f"You output invalid JSON: {e}\nBroken: {raw_response}\nOutput ONLY a valid JSON array starting with [ and ending with ]."
            except Exception as e:
                print(f"🚨 [PureGraph] DEBUG: Raw LLM Response failed:\n...{raw_response[-200:]}\n")
                state["error_message"] = f"JSON Parse Error: {e}"
                state["plan"] = []
                return state
                
        state["error_message"] = "Failed to generate valid JSON after 2 retries."
        state["plan"] = []
        return state

    async def executor_node(self, state: dict) -> dict:
        print(f"⚙️ [PureGraph] Executing {len(state['plan'])} steps...")
        artifacts = []
        last_output = ""
        
        import time
        project_dir = f"project_{int(time.time())}"
        os.makedirs(project_dir, exist_ok=True)
        
        for step in state['plan']:
            if step.get('action') == 'write':
                filepath = os.path.join(project_dir, step['path'])
                write_file(filepath, step['content'])
                artifacts.append(filepath)
            elif step.get('action') == 'execute':
                original_dir = os.getcwd()
                os.chdir(project_dir)
                last_output = run_terminal_command(step['command'])
                os.chdir(original_dir)
                
        state['code_written'] = artifacts
        state['execution_output'] = last_output
        state['project_dir'] = project_dir
        return state

    def reviewer_node(self, state: dict) -> str:
        print("🔍 [PureGraph] Reviewing execution output...")
        output = state.get('execution_output', '')
        
        if any(err in output.lower() for err in ['error', 'traceback', 'failed', 'no such file', 'command not found']) and 'nothing to commit' not in output.lower():
            state['error_message'] = f"Execution failed with: {output[:300]}"
            return "retry"
        
        return "success"

self_correcting_builder = SelfCorrectingBuilder()
