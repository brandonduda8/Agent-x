import json
import datetime
import os


STATE_FILE = "genesis_state.json"


class GenesisStateEngine:

    def __init__(self):
        self.state = self.load()


    def load(self):

        if os.path.exists(STATE_FILE):

            with open(STATE_FILE, "r") as f:
                return json.load(f)

        return {

            "income": {

                "applications_sent":0,
                "responses":0

            },

            "revenue": {

                "leads_found":0,
                "outreach_sent":0

            },

            "housing": {

                "resources_found":0

            },

            "technology": {

                "systems_built":0

            },

            "approvals_pending":0,

            "last_update":None

        }


    def update(self, category, metric, value):

        self.state[category][metric] = value

        self.state["last_update"] = str(datetime.datetime.now())

        self.save()

        return self.state


    def save(self):

        with open(STATE_FILE,"w") as f:

            json.dump(self.state,f,indent=4)



if __name__ == "__main__":

    engine = GenesisStateEngine()

    print(
        engine.update(
            "revenue",
            "leads_found",
            50
        )
    )
