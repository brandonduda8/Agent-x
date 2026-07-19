import time
import uuid

from core.genesis.execution.tool_registry import (
    tool_registry
)


class GenesisAgentExecutor:


    def execute_tool(
        self,
        agent,
        tool,
        *args
    ):

        print(
            f"🤖 {agent} executing {tool}"
        )

        result = tool_registry.execute(
            tool,
            *args
        )

        return {
            "id":
            "agent_execution_" +
            uuid.uuid4().hex[:8],

            "agent": agent,

            "tool": tool,

            "result": result,

            "timestamp": time.time()
        }


agent_executor = GenesisAgentExecutor()
