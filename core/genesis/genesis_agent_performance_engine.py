import time
import uuid


class GenesisAgentPerformanceEngine:

    def __init__(self):
        self.agents = {}
        self.events = []

    def record_result(
        self,
        agent,
        task,
        success,
        value=0
    ):

        if agent not in self.agents:
            self.agents[agent] = {
                "tasks": 0,
                "successes": 0,
                "revenue_value": 0,
                "score": 0
            }

        profile = self.agents[agent]

        profile["tasks"] += 1

        if success:
            profile["successes"] += 1

        profile["revenue_value"] += value

        profile["score"] = round(
            profile["successes"] /
            profile["tasks"],
            2
        )

        event = {
            "id": f"performance_{uuid.uuid4().hex[:8]}",
            "agent": agent,
            "task": task,
            "success": success,
            "value": value,
            "timestamp": time.time()
        }

        self.events.append(event)

        return {
            "event": event,
            "agent_profile": profile
        }


    def rank_agents(self):

        ranking = sorted(
            self.agents.items(),
            key=lambda x: (
                x[1]["score"],
                x[1]["revenue_value"]
            ),
            reverse=True
        )

        return {
            "id":
                f"ranking_{uuid.uuid4().hex[:8]}",
            "ranking": [
                {
                    "agent": name,
                    "score": data["score"],
                    "tasks": data["tasks"],
                    "revenue_value":
                        data["revenue_value"]
                }
                for name, data in ranking
            ],
            "timestamp":
                time.time()
        }


    def recommend_agent(
        self,
        task_type
    ):

        if not self.agents:
            return {
                "recommendation":
                    "No performance data available"
            }

        best = max(
            self.agents.items(),
            key=lambda x: x[1]["score"]
        )

        return {
            "task":
                task_type,
            "recommended_agent":
                best[0],
            "confidence":
                best[1]["score"],
            "timestamp":
                time.time()
        }


    def report(self):

        return {
            "system":
                "GENESIS AGENT PERFORMANCE ENGINE v1",
            "agents":
                len(self.agents),
            "events":
                len(self.events),
            "status":
                "ONLINE",
            "timestamp":
                time.time()
        }


genesis_agent_performance_engine = GenesisAgentPerformanceEngine()
