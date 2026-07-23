import time
from datetime import datetime


class AgentHeartbeat:

    def __init__(self, registry):

        self.registry = registry
        self.last_check = {}


    def pulse(self, agent_name):

        now = time.time()

        self.last_check[agent_name] = now

        agent = self.registry.get(agent_name)

        if agent:

            agent["last_seen"] = now
            agent["heartbeat"] = "ACTIVE"

            print(
                f"💓 HEARTBEAT | {agent_name} | ONLINE"
            )

            return True


        print(
            f"⚠️ UNKNOWN AGENT | {agent_name}"
        )

        return False



    def check_all(self):

        agents = self.registry.all_agents()

        report = {}

        for name in agents:

            self.pulse(name)

            report[name] = {
                "status": "ONLINE",
                "last_seen":
                    datetime.utcnow()
                    .isoformat()
            }


        return report



heartbeat = None
