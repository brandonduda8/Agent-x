import time
import uuid


class GenesisAgentHealthMonitor:

    def __init__(self):

        self.system = "GENESIS AGENT HEALTH MONITOR v1"

        self.agents = {}
        self.performance = []


    def register_agent(self, name, skills):

        agent = {

            "id":
                "agent_health_" + uuid.uuid4().hex[:8],

            "name":
                name,

            "skills":
                skills,

            "status":
                "ONLINE",

            "health":
                100,

            "tasks_completed":
                0,

            "successes":
                0,

            "failures":
                0,

            "created":
                time.time(),

            "last_seen":
                time.time()
        }

        self.agents[name] = agent

        print(
            f"❤️ Agent health registered: {name}"
        )

        return agent



    def heartbeat(self, name):

        agent = self.agents.get(name)

        if not agent:
            return None

        agent["status"] = "ONLINE"
        agent["last_seen"] = time.time()

        print(
            f"💓 Heartbeat: {name}"
        )

        return agent



    def record_task(
        self,
        name,
        success=True,
        revenue=0
    ):

        agent = self.agents.get(name)

        if not agent:
            return None


        agent["tasks_completed"] += 1


        if success:

            agent["successes"] += 1

        else:

            agent["failures"] += 1


        result = {

            "id":
                "performance_" + uuid.uuid4().hex[:8],

            "agent":
                name,

            "success":
                success,

            "revenue":
                revenue,

            "timestamp":
                time.time()
        }


        self.performance.append(result)


        print(
            f"📈 Performance recorded: {name}"
        )

        return result



    def analyze_agent(self, name):

        agent = self.agents.get(name)

        if not agent:
            return None


        total = agent["tasks_completed"]

        rate = 0

        if total:

            rate = agent["successes"] / total


        analysis = {

            "agent":
                name,

            "success_rate":
                rate,

            "tasks":
                total,

            "recommendation":
                (
                    "EVOLVE"
                    if rate < 0.5
                    else
                    "CONTINUE"
                ),

            "timestamp":
                time.time()
        }


        print(
            f"🧠 Agent analyzed: {name}"
        )

        return analysis



    def report(self):

        return {

            "system":
                self.system,

            "agents":
                len(self.agents),

            "performance_events":
                len(self.performance),

            "timestamp":
                time.time()
        }



agent_health_monitor = GenesisAgentHealthMonitor()
