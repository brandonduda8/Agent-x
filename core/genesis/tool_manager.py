import os
import json
import time
import shutil
import subprocess


class GenesisToolManager:
    """
    GENESIS TOOL MANAGER v1

    Purpose:
    - Track available tools
    - Let agents discover capabilities
    - Execute approved tools
    - Prepare for self-expanding tool ecosystem
    """

    def __init__(self):
        self.name = "GENESIS TOOL MANAGER v1"
        self.registry_file = "data/genesis_tools.json"
        self.tools = {}

        self.default_tools = {
            "python": {
                "command": "python",
                "category": "development"
            },
            "node": {
                "command": "node",
                "category": "development"
            },
            "git": {
                "command": "git",
                "category": "deployment"
            },
            "camera": {
                "command": "termux-camera-photo",
                "category": "hardware"
            },
            "battery": {
                "command": "termux-battery-status",
                "category": "hardware"
            },
            "location": {
                "command": "termux-location",
                "category": "hardware"
            },
            "sensor": {
                "command": "termux-sensor",
                "category": "hardware"
            },
            "notification": {
                "command": "termux-notification",
                "category": "hardware"
            },
            "clipboard": {
                "command": "termux-clipboard-get",
                "category": "hardware"
            }
        }

        self.load()


    def command_exists(self, command):
        return shutil.which(command) is not None


    def scan(self):

        results = {}

        for name, info in self.default_tools.items():

            installed = self.command_exists(
                info["command"]
            )

            results[name] = {
                "command": info["command"],
                "category": info["category"],
                "installed": installed
            }


        self.tools = results
        self.save()

        return results



    def register_tool(
        self,
        name,
        command,
        category="custom"
    ):

        self.tools[name] = {
            "command": command,
            "category": category,
            "installed": self.command_exists(command),
            "registered": time.time()
        }

        self.save()

        return self.tools[name]



    def execute(
        self,
        tool,
        args=None
    ):

        if tool not in self.tools:
            return {
                "error": "Tool not registered"
            }


        command = self.tools[tool]["command"]

        if args is None:
            args = []


        try:

            result = subprocess.run(
                [command] + args,
                capture_output=True,
                text=True,
                timeout=30
            )


            return {
                "tool": tool,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "code": result.returncode
            }


        except Exception as e:

            return {
                "tool": tool,
                "error": str(e)
            }



    def save(self):

        os.makedirs(
            "data",
            exist_ok=True
        )

        with open(
            self.registry_file,
            "w"
        ) as f:

            json.dump(
                self.tools,
                f,
                indent=2
            )



    def load(self):

        if os.path.exists(
            self.registry_file
        ):

            try:

                with open(
                    self.registry_file
                ) as f:

                    self.tools = json.load(f)

            except:

                self.tools = {}



    def report(self):

        return {
            "system": self.name,
            "tools": self.tools,
            "count": len(self.tools),
            "timestamp": time.time()
        }



tool_manager = GenesisToolManager()
