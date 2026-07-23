import time
import uuid
import json
import os


class GenesisLifeExecutiveBridge:

    def __init__(self):

        self.system = (
            "GENESIS LIFE EXECUTIVE BRIDGE v1"
        )


    def load(self, path):

        try:

            with open(path, "r") as f:
                return json.load(f)

        except:

            return {}


    def executive_check(self):

        emergency = self.load(
            "data/genesis_emergency_command.json"
        )

        revenue = self.load(
            "data/genesis_revenue_cycles.json"
        )

        heartbeat = self.load(
            "data/genesis_life_operations_heartbeat.json"
        )


        actions = []


        if revenue.get("cycles"):

            actions.append(
                "Contact highest probability revenue prospects"
            )

        else:

            actions.append(
                "Create first revenue mission"
            )


        if emergency:

            actions.append(
                "Complete emergency stabilization tasks"
            )

        else:

            actions.append(
                "Activate emergency life command plan"
            )


        actions.append(
            "Improve Genesis system capability"
        )


        return {

            "id":
                "life_exec_" +
                uuid.uuid4().hex[:8],


            "system":
                self.system,


            "priority_order": [

                {
                    "priority": 1,
                    "mission": actions[0]
                },

                {
                    "priority": 2,
                    "mission": actions[1]
                },

                {
                    "priority": 3,
                    "mission": actions[2]
                }

            ],


            "genesis_status": {

                "revenue_connected":
                    bool(
                        revenue.get("cycles")
                    ),

                "emergency_connected":
                    bool(
                        emergency
                    ),

                "heartbeat_connected":
                    bool(
                        heartbeat
                    )

            },


            "timestamp":
                time.time()

        }


    def report(self):

        return {

            "system":
                self.system,

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }


genesis_life_executive_bridge = (
    GenesisLifeExecutiveBridge()
)
