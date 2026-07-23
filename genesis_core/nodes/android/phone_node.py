import time
import platform


class GenesisAndroidNode:


    def __init__(self):

        self.name = "Android Edge Node"



    def heartbeat(self):

        return {

            "node":
            self.name,

            "status":
            "ONLINE",

            "device":
            platform.system(),

            "capabilities":

            [

            "notifications",

            "mobile_execution",

            "device_monitoring"

            ],

            "timestamp":
            time.time()

        }
