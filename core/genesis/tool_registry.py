import time
import uuid


class GenesisToolRegistry:

    def __init__(self):

        self.system = "GENESIS TOOL REGISTRY v1"

        self.tools = {}


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


        print(
            f"🔧 Tool registered: {name}"
        )


        return tool



    def verify_tool(self,name):

        if name in self.tools:

            self.tools[name]["status"] = "VERIFIED"
            self.tools[name]["health"] = "PASS"

            print(
                f"✅ Tool verified: {name}"
            )

            return True


        return False



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
