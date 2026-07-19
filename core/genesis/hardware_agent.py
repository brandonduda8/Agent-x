import os
import json
import time
import platform
import subprocess

from core.genesis.tool_manager import tool_manager


class GenesisHardwareAgent:

    def __init__(self):
        self.name = "GENESIS HARDWARE INTELLIGENCE AGENT v1"
        self.node = "android_primary"


    def run_command(self, command):

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )

            return {
                "command": command,
                "output": result.stdout.strip(),
                "error": result.stderr.strip(),
                "status": "SUCCESS"
            }

        except Exception as e:

            return {
                "command": command,
                "error": str(e),
                "status": "FAILED"
            }



    def identity(self):

        return {
            "node": self.node,
            "platform": platform.platform(),
            "architecture": platform.machine(),
            "python": platform.python_version()
        }



    def battery(self):

        return self.run_command(
            "termux-battery-status"
        )



    def storage(self):

        return self.run_command(
            "df -h /data"
        )



    def sensors(self):

        return self.run_command(
            "termux-sensor -l"
        )



    def capabilities(self):

        return tool_manager.report()



    def health_report(self):

        return {

            "genesis": self.name,

            "identity": self.identity(),

            "hardware": {

                "battery":
                    self.battery(),

                "storage":
                    self.storage(),

                "sensors":
                    self.sensors()

            },

            "capabilities":
                self.capabilities(),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



hardware_agent = GenesisHardwareAgent()
