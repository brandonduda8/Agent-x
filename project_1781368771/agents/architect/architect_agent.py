import os
import json
from core.event_bus import bus
from core.llm_client import llm
from tools.code_tools import write_file, run_terminal_command

class ArchitectAgent:
    def __init__(self, name="Architect-Toolsmith"):
        self.name = name
        bus.subscribe("tool_request", self.on_tool_request)
        print(f"🏗️ [{self.name}] Online and ready to build system tools.")

    async def on_tool_request(self, event: dict):
        if event.get('target') != 'architect':
            return
            
        tool_desc = event['payload']['description']
        print(f"🏗️ [{self.name}] Received request to build: {tool_desc}")
        
        system_prompt = """You are an expert Python developer. Output ONLY a valid JSON object.
Format: {"filename": "new_tool.py", "content": "def my_function():\\n    return 'hello'"}
CRITICAL: 
1. The code must be fully functional and include any necessary imports.
2. Escape ALL quotes inside the "content" string with a backslash (e.g., \\" or \\').
3. Do NOT include markdown formatting (no ```json) or conversational text. Just the raw JSON object."""
        
        try:
            raw = await llm.generate(f"Build a Python tool that does the following: {tool_desc}", system_prompt, max_tokens=2000)
            clean = raw.strip()
            
            # Strip markdown if the LLM adds it
            if "```" in clean:
                parts = clean.split("```")
                if len(parts) >= 3:
                    clean = parts[1].strip()
                    if clean.lower().startswith("json"):
                        clean = clean.split("\n", 1)[1].strip() if "\n" in clean else clean[4:].strip()
            
            start = clean.find('{')
            end = clean.rfind('}')
            if start != -1 and end != -1:
                json_str = clean[start:end+1]
                tool_data = json.loads(json_str)
                
                filename = tool_data['filename']
                content = tool_data['content']
                filepath = f"tools/{filename}"
                
                # 1. Write the tool to the filesystem
                write_file(filepath, content)
                print(f"✅ [{self.name}] Successfully built and saved {filepath}!")
                
                # 2. Test the tool to ensure it has no syntax errors
                print(f"🧪 [{self.name}] Testing the new tool...")
                test_output = run_terminal_command(f"python -m py_compile {filepath}")
                
                if test_output.strip() == "":
                    print(f"🎉 [{self.name}] Tool {filename} is fully operational and added to the empire!")
                    await bus.publish({
                        "id": f"tool_built_{event['id']}",
                        "source": "architect",
                        "target": "hub",
                        "type": "result",
                        "payload": {"tool_name": filename, "status": "success"}
                    })
                else:
                    print(f"⚠️ [{self.name}] Tool built but failed syntax test: {test_output}")
            else:
                raise ValueError("No JSON object found")
                
        except Exception as e:
            print(f"❌ [{self.name}] Failed to build tool: {e}")

architect = ArchitectAgent()
