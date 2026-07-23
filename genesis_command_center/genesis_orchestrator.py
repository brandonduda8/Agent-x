import json
import datetime
from pathlib import Path


class GenesisOrchestrator:

    def __init__(self):
        self.memory_file = Path("memory.json")

    def load_memory(self):
        if self.memory_file.exists():
            return json.loads(self.memory_file.read_text())

        return {
            "missions": [],
            "agents": {},
            "approvals": []
        }


    def dispatch(self, agent, objective):

        mission = {
            "agent": agent,
            "objective": objective,
            "status": "DISPATCHED",
            "timestamp": str(datetime.datetime.now())
        }

        memory = self.load_memory()

        memory["missions"].append(mission)

        self.memory_file.write_text(
            json.dumps(memory, indent=4)
        )

        return mission


    def daily_power_move(self):

        return {
            "type": "DAILY_POWER_BRIEF",

            "priority_order": [

                {
                    "mission":
                    "Secure income",
                    "actions":
                    [
                        "Review matching jobs",
                        "Submit applications",
                        "Track responses"
                    ]
                },

                {
                    "mission":
                    "Build revenue pipeline",
                    "actions":
                    [
                        "Review leads",
                        "Approve outreach",
                        "Follow up"
                    ]
                },

                {
                    "mission":
                    "Technology growth",
                    "actions":
                    [
                        "Improve Genesis",
                        "Add automation",
                        "Document systems"
                    ]
                }
            ],

            "timestamp":
            str(datetime.datetime.now())
        }



if __name__ == "__main__":

    genesis = GenesisOrchestrator()

    print(
        genesis.dispatch(
            "Genesis Core",
            "Coordinate all connected agents"
        )
    )

    print(
        json.dumps(
            genesis.daily_power_move(),
            indent=4
        )
    )
