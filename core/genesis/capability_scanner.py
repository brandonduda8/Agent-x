import os
import shutil
import platform
import subprocess


class CapabilityScanner:

    def __init__(self):

        self.name = "GENESIS CAPABILITY SCANNER v1"


    def check_command(self, command):

        return shutil.which(command) is not None


    def scan(self):

        capabilities = []


        tools = {

            "python":
                "python",

            "node":
                "node",

            "git":
                "git",

            "camera":
                "termux-camera-photo",

            "battery":
                "termux-battery-status",

            "location":
                "termux-location",

            "sensor":
                "termux-sensor",

            "notifications":
                "termux-notification",

            "clipboard":
                "termux-clipboard-get"

        }


        for name, command in tools.items():

            if self.check_command(command):

                capabilities.append(name)


        return {

            "genesis":

                self.name,


            "device":

                platform.platform(),


            "architecture":

                platform.machine(),


            "python":

                platform.python_version(),


            "capabilities":

                capabilities,


            "status":

                "SCANNED"

        }



capability_scanner = CapabilityScanner()
