import time
import uuid


class GenesisMCPServer:

    """
    GENESIS MCP SERVER v1

    Universal tool gateway for Genesis agents.
    """

    def __init__(self):

        self.system = "GENESIS MCP SERVER v1"

        self.tools = {}

        self.calls = []


    def register_tool(
        self,
        name,
        function
    ):

        self.tools[name] = function

        return {
            "tool": name,
            "status": "REGISTERED"
        }


    def call(
        self,
        tool,
        payload=None
    ):

        request = {

            "id":
                "mcp_" +
                uuid.uuid4().hex[:8],

            "tool":
                tool,

            "payload":
                payload or {},

            "timestamp":
                time.time()

        }


        self.calls.append(request)


        if tool not in self.tools:

            return {

                "status":
                    "ERROR",

                "message":
                    f"Unknown MCP tool: {tool}"

            }


        try:

            result = self.tools[tool](
                payload or {}
            )


            return {

                "status":
                    "SUCCESS",

                "tool":
                    tool,

                "result":
                    result,

                "timestamp":
                    time.time()

            }


        except Exception as e:

            return {

                "status":
                    "FAILED",

                "tool":
                    tool,

                "error":
                    str(e)

            }


    def report(self):

        return {

            "system":
                self.system,

            "tools":
                list(
                    self.tools.keys()
                ),

            "calls":
                len(self.calls),

            "timestamp":
                time.time()

        }



genesis_mcp_server = GenesisMCPServer()
