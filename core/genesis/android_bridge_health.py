import time
import os


class AndroidBridgeHealth:

    def __init__(self):

        self.components = {
            "Shizuku_API": os.path.exists("Shizuku-API"),
            "Android_MCP_Server": os.path.exists(
                "core/genesis/android_mcp_server.py"
            ),
            "Mobile_Bridge": os.path.exists(
                "core/genesis/mcp_mobile_bridge.py"
            ),
            "Genesis_Mobile_App": os.path.exists(
                "genesis_mobile"
            )
        }


    def check(self):

        connected = [
            name for name, exists in self.components.items()
            if exists
        ]

        missing = [
            name for name, exists in self.components.items()
            if not exists
        ]

        return {
            "system": "GENESIS ANDROID CONTROL BRIDGE HEALTH v1",
            "status": "ONLINE",
            "available_components": connected,
            "missing_components": missing,
            "bridge_ready": len(missing) == 0,
            "timestamp": time.time()
        }


android_bridge_health = AndroidBridgeHealth()
