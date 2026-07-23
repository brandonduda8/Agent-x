import json
import os
from datetime import datetime


class CapabilityRegistry:

    def __init__(
        self,
        file_path="core/genesis/data/capabilities.json"
    ):

        self.file_path = file_path

        os.makedirs(
            os.path.dirname(file_path),
            exist_ok=True
        )

        if not os.path.exists(file_path):
            self.save({})


    def load(self):

        with open(
            self.file_path,
            "r"
        ) as f:
            return json.load(f)


    def save(self, data):

        with open(
            self.file_path,
            "w"
        ) as f:
            json.dump(
                data,
                f,
                indent=2
            )


    def register(
        self,
        agent_name,
        capabilities,
        model="general"
    ):

        registry = self.load()

        registry[agent_name] = {

            "agent": agent_name,

            "capabilities":
                capabilities,

            "model":
                model,

            "status":
                "ONLINE",

            "tasks_completed":
                0,

            "errors":
                0,

            "created":
                datetime.utcnow()
                .isoformat()
        }


        self.save(registry)


    def get(self, agent_name):

        return self.load().get(
            agent_name
        )


    def all_agents(self):

        return self.load()


    def update_stats(
        self,
        agent_name,
        completed=False,
        error=False
    ):

        registry = self.load()

        if agent_name in registry:

            if completed:
                registry[agent_name][
                    "tasks_completed"
                ] += 1

            if error:
                registry[agent_name][
                    "errors"
                ] += 1


        self.save(registry)



capability_registry = CapabilityRegistry()
