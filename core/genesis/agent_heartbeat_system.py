import time
import uuid


class GenesisAgentHeartbeatSystem:

    def __init__(self):

        self.system = "GENESIS AGENT HEARTBEAT SYSTEM v1"

        self.agents = {}

        self.heartbeats = []


    def register_agent(
        self,
        name,
        role,
        skills
    ):

        agent = {

            "id":
                "agent_" + uuid.uuid4().hex[:8],

            "name":
                name,

            "role":
                role,

            "skills":
                skills,

            "status":
                "ONLINE",

            "current_mission":
                None,

            "current_task":
                None,

            "health":
                100,

            "created":
                time.time(),

            "last_heartbeat":
                time.time()

        }


        self.agents[name] = agent


        print(
            f"❤️ Agent heartbeat registered: {name}"
        )


        return agent



    def heartbeat(
        self,
        name,
        mission=None,
        task=None
    ):

        if name not in self.agents:

            return {
                "status":
                    "AGENT_NOT_FOUND"
            }


        agent = self.agents[name]


        agent["last_heartbeat"] = time.time()

        agent["status"] = "ACTIVE"

        if mission:
            agent["current_mission"] = mission

        if task:
            agent["current_task"] = task


        heartbeat = {

            "id":
                "heartbeat_" + uuid.uuid4().hex[:8],

            "agent":
                name,

            "status":
                agent["status"],

            "timestamp":
                time.time()

        }


        self.heartbeats.append(
            heartbeat
        )


        print(
            f"💓 Heartbeat received: {name}"
        )


        return heartbeat



    def update_health(
        self,
        name,
        health
    ):

        if name in self.agents:

            self.agents[name]["health"] = health

            return self.agents[name]


        return {
            "status":
                "NOT_FOUND"
        }



    def workforce_status(self):

        return {

            "system":
                self.system,

            "agents":
                self.agents,

            "heartbeats":
                len(self.heartbeats),

            "timestamp":
                time.time()

        }



agent_heartbeat_system = GenesisAgentHeartbeatSystem()
