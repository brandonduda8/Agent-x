import os
import json
import time


class GenesisAgentFactory:

    def __init__(self):

        self.name = "GENESIS AGENT FACTORY v1"

        self.agent_dir = "agents/generated"

        os.makedirs(
            self.agent_dir,
            exist_ok=True
        )


    def create_agent(
        self,
        name,
        purpose,
        tools=None
    ):

        filename = (
            name.lower()
            .replace(" ","_")
            + ".py"
        )

        path = os.path.join(
            self.agent_dir,
            filename
        )


        template = f'''
class {name.replace(" ","")}:

    def __init__(self):

        self.name = "{name}"

        self.purpose = "{purpose}"

        self.tools = {tools or []}


    async def run(self, mission):

        print(
            "[{name}] Executing:",
            mission
        )

        return {{
            "agent":
                self.name,

            "mission":
                mission,

            "status":
                "COMPLETE"
        }}


{name.replace(" ","").lower()}
= {name.replace(" ","")}()
'''


        with open(
            path,
            "w"
        ) as f:

            f.write(template)


        return {

            "created": True,

            "agent": name,

            "file": path,

            "timestamp": time.time()

        }



    def list_generated(self):

        return os.listdir(
            self.agent_dir
        )



agent_factory = GenesisAgentFactory()
