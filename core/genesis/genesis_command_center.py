import time
import json
import os
import uuid


from core.genesis.genesis_autonomous_heartbeat_engine import (
    genesis_autonomous_heartbeat_engine
)

from core.genesis.genesis_revenue_autonomous_operator import (
    genesis_revenue_autonomous_operator
)



class GenesisCommandCenter:


    def __init__(self):

        self.system = (
            "GENESIS COMMAND CENTER v1"
        )

        self.file = (
            "data/genesis_command_center_memory.json"
        )

        self.commands = []

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.load()



    def load(self):

        if os.path.exists(
            self.file
        ):

            try:

                with open(
                    self.file,
                    "r"
                ) as f:

                    data = json.load(f)

                    self.commands = (
                        data.get(
                            "commands",
                            []
                        )
                    )

            except Exception:

                self.commands = []



    def save(self):

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                {
                    "system": self.system,
                    "commands": self.commands,
                    "updated": time.time()
                },
                f,
                indent=2
            )



    def execute(
        self,
        objective
    ):

        print(
            "👑 GENESIS COMMAND CENTER ACTIVE"
        )


        heartbeat = (
            genesis_autonomous_heartbeat_engine
            .heartbeat(
                objective
            )
        )


        operation = (
            genesis_revenue_autonomous_operator
            .report()
        )


        command = {

            "id":
                "command_"
                +
                uuid.uuid4().hex[:8],

            "objective":
                objective,

            "heartbeat_status":
                heartbeat.get(
                    "status"
                ),

            "operator":
                operation,

            "status":
                "COMPLETE",

            "created":
                time.time()

        }


        self.commands.append(
            command
        )


        self.save()


        print(
            "👑 GENESIS COMMAND COMPLETE"
        )


        return command



    def report(self):

        return {

            "system":
                self.system,

            "commands":
                len(
                    self.commands
                ),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_command_center = (
    GenesisCommandCenter()
)
