import json
import time
from pathlib import Path


class AgentHeartbeat:

    def __init__(self):

        self.file = Path(
            "memory/agent_health.json"
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
        model="unknown",
        capabilities=None
    ):

        data=self.load()

        data[agent]={

            "status":
                "ONLINE",

            "model":
                model,

            "capabilities":
                capabilities or [],

            "last_seen":
                time.time(),

            "tasks_completed":
                0,

            "errors":
                0

        }

        self.save(data)


    def heartbeat(
        self,
        agent
    ):

        data=self.load()

        if agent in data:

            data[agent]["last_seen"] = time.time()

            data[agent]["status"] = "ONLINE"

            self.save(data)

            return True

        return False


    def report(self):

        return self.load()



heartbeat = AgentHeartbeat()
