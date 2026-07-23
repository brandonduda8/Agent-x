import os
import json
import time
import uuid


class GenesisToolRegistry:
    """
    GENESIS TOOL REGISTRY v2

    Persistent capability storage.

    Stores:
    - MCP tools
    - agent tools
    - automation tools
    - execution capabilities
    """

    def __init__(self):

        self.system = "GENESIS TOOL REGISTRY v2"

        self.file = (
            "core/genesis/genesis_tool_registry.json"
        )

        self.tools = {}

        self.load()



    def load(self):

        if os.path.exists(self.file):

            try:

                with open(
                    self.file,
                    "r"
                ) as f:

                    self.tools = json.load(f)


            except Exception:

                self.tools = {}



    def save(self):

        os.makedirs(
            os.path.dirname(self.file),
            exist_ok=True
        )

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                self.tools,
                f,
                indent=4
            )



    def register_tool(
        self,
        name,
        category,
        purpose,
        agents
    ):


        tool = {

            "id":
            "tool_" + uuid.uuid4().hex[:8],

            "name":
            name,

            "category":
            category,

            "purpose":
            purpose,

            "agents":
            agents,

            "status":
            "REGISTERED",

            "health":
            "UNKNOWN",

            "created":
            time.time()

        }


        self.tools[name] = tool


        self.save()


        print(
            f"🔧 Tool registered: {name}"
        )


        return tool



    def verify_tool(
        self,
        name
    ):

        return (
            name in self.tools
        )



    def list_tools(self):

        return list(
            self.tools.values()
        )



    def report(self):

        return {

            "system":
            self.system,

            "tools":
            len(self.tools),

            "registry":
            self.tools,

            "timestamp":
            time.time()

        }



tool_registry = GenesisToolRegistry()
