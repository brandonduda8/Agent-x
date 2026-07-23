import json
from pathlib import Path
from datetime import datetime


class CapabilityRegistry:

    def __init__(self):

        self.file = Path(
            "memory/capabilities.json"
        )

        self.file.parent.mkdir(
            exist_ok=True
        )

        if not self.file.exists():
            self.save({})


    def load(self):

        return json.loads(
            self.file.read_text()
        )


    def save(self,data):

        self.file.write_text(
            json.dumps(
                data,
                indent=2
            )
        )


    def register(
        self,
        agent,
        capabilities,
        model="unknown"
    ):

        data=self.load()

        data[agent]={

            "capabilities":
                capabilities,

            "model":
                model,

            "registered":
                datetime.utcnow().isoformat(),

            "status":
                "ONLINE"

        }

        self.save(data)


    def find_by_capability(
        self,
        capability
    ):

        data=self.load()

        matches=[]

        for agent,info in data.items():

            if capability in info.get(
                "capabilities",
                []
            ):

                matches.append(agent)

        return matches



capability_registry = CapabilityRegistry()
