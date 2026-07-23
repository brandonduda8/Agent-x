from datetime import datetime
import traceback

from core.genesis.capability_registry import capability_registry
from core.llm_client import llm


class UnifiedAgentRuntime:

    def __init__(self):

        self.registry = capability_registry
        self.llm = llm
        self.execution_history = []


    async def execute(
        self,
        agent_name,
        task,
        capability="general"
    ):

        started = datetime.utcnow().isoformat()

        agent = self.registry.get(agent_name)


        if not agent:

            return {
                "status": "ERROR",
                "message":
                    f"Agent {agent_name} not registered"
            }


        model_type = agent.get(
            "model",
            capability
        )


        execution = {

            "agent": agent_name,
            "task": task,
            "model": model_type,
            "started": started
        }


        try:

            result = await self.llm.generate(

                prompt=task,

                system_prompt=f"""
You are {agent_name}.

Your capabilities:
{agent['capabilities']}

Complete the assigned mission.
Return actionable results.
""",

                task_type=model_type
            )


            self.registry.update_stats(
                agent_name,
                completed=True
            )


            execution["status"] = "COMPLETED"
            execution["result"] = result


        except Exception as error:


            self.registry.update_stats(
                agent_name,
                error=True
            )


            execution["status"] = "FAILED"
            execution["error"] = str(error)

            execution["trace"] = (
                traceback.format_exc()
            )


        self.execution_history.append(
            execution
        )


        return execution



runtime = UnifiedAgentRuntime()
