from genesis_meta_agent import GenesisMetaAgent
from genesis_state_engine import GenesisStateEngine
import datetime
import json


class DailyCommandCenter:

    def __init__(self):

        self.meta = GenesisMetaAgent()

        self.state = GenesisStateEngine()


    def generate_brief(self):

        strategy = self.meta.analyze({

            "income":"CRITICAL",

            "entrepreneurship":"HIGH",

            "technology_growth":"HIGH"

        })


        return {

            "system":
            "GENESIS DAILY COMMAND CENTER",

            "date":
            str(datetime.datetime.now()),

            "system_state":
            self.state.state,

            "strategy":
            strategy["daily_strategy"],

            "next_actions":[

                "Review income opportunities",

                "Approve revenue outreach",

                "Check system improvements"

            ]

        }



if __name__ == "__main__":

    center = DailyCommandCenter()

    print(
        json.dumps(
            center.generate_brief(),
            indent=4
        )
    )
