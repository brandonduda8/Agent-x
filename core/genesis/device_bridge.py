import time


class GenesisDeviceBridge:

    def __init__(self):

        self.system = "GENESIS DEVICE BRIDGE v1"

        self.actions = []


    def notify(self, message):

        action = {

            "type": "NOTIFICATION",

            "message": message,

            "status": "READY",

            "timestamp": time.time()

        }


        self.actions.append(action)

        print(
            f"📲 Device notification: {message}"
        )

        return action



    def execute_allowed_action(
        self,
        action
    ):

        allowed_actions = [

            "open_terminal",

            "check_status",

            "send_notification"

        ]


        if action in allowed_actions:

            result = {

                "action": action,

                "status": "AUTHORIZED",

                "timestamp": time.time()

            }

            self.actions.append(result)

            return result


        return {

            "action": action,

            "status": "DENIED",

            "timestamp": time.time()

        }



    def report(self):

        return {

            "system":
            self.system,

            "actions":
            len(self.actions),

            "timestamp":
            time.time()

        }



device_bridge = GenesisDeviceBridge()
