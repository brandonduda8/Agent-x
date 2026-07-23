import platform
import time


class GenesisAndroidDeviceAdapter:


    def __init__(self):

        self.system = (
            "GENESIS ANDROID DEVICE ADAPTER v1"
        )


    def status(self):

        return {

            "platform":
                platform.platform(),

            "python":
                platform.python_version(),

            "capabilities":
                [
                    "device",
                    "storage",
                    "automation"
                ],

            "timestamp":
                time.time()

        }
