import os
import json
import time
import re

from tools.code_tools import write_file, run_terminal_command
from core.llm_client import llm


class SelfCorrectingBuilder:

    def __init__(self):
        self.max_iterations = 3


    async def run(self, objective):

        state = {
            "objective": objective,
            "plan": [],
            "code_written": [],
            "project_dir": "",
            "iteration_count": 0,
            "error_message": ""
        }


        print("🔄 [PureGraph] Starting autonomous build system")


        for attempt in range(1, self.max_iterations + 1):

            state["iteration_count"] = attempt

            print(
                f"🔁 [PureGraph] Build attempt {attempt}/{self.max_iterations}"
            )


            try:

                state = await self.planner_node(state)


                if not state["plan"]:
                    raise Exception(
                        "Planner produced no valid actions"
                    )


                state = await self.executor_node(state)


                if state["code_written"]:
                    await self.deploy_node(state)

                    print(
                        "✅ [PureGraph] Build completed"
                    )

                    return state


            except Exception as e:

                state["error_message"] = str(e)

                print(
                    f"⚠️ Build attempt failed: {e}"
                )


        return state



    async def planner_node(self,state):


        print(
            "🧠 [PureGraph] Creating build plan..."
        )


        prompt=f"""
Create a website project.

Objective:
{state['objective']}


Return ONLY JSON.

Format:

[
 {{
 "action":"write",
 "path":"index.html",
 "content":"FULL HTML HERE"
 }}
]

Rules:
- no markdown
- no explanations
- valid JSON only
- escape quotes correctly
- include complete HTML
"""


        raw = await llm.generate(
            prompt,
            "You are a senior software architect.",
            max_tokens=5000
        )


        raw = raw.strip()


        raw = re.sub(
            r"```json|```",
            "",
            raw
        ).strip()


        start = raw.find("[")

        end = raw.rfind("]")


        if start == -1 or end == -1:

            raise Exception(
                "No JSON array found"
            )


        clean = raw[start:end+1]


        plan=json.loads(clean)


        state["plan"]=plan


        return state



    async def executor_node(self,state):


        project_dir = (
            f"project_{int(time.time())}"
        )


        os.makedirs(
            project_dir,
            exist_ok=True
        )


        files=[]


        for item in state["plan"]:


            if item.get("action")=="write":


                path=os.path.join(
                    project_dir,
                    item["path"]
                )


                write_file(
                    path,
                    item["content"]
                )


                files.append(path)


        state["code_written"]=files

        state["project_dir"]=project_dir


        return state



    async def deploy_node(self,state):


        print(
            "🚀 [PureGraph] Preparing deployment"
        )


        return state



self_correcting_builder = SelfCorrectingBuilder()
