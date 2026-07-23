import time
import uuid


class GenesisExecutionFeedbackEngine:

    def __init__(self):
        self.system = "GENESIS EXECUTION FEEDBACK ENGINE v1"
        self.executions = []
        self.agent_scores = {}
        self.lessons = []

    def record_execution(
        self,
        execution_id,
        action,
        result,
        agents=None,
        revenue_value=0
    ):

        event = {
            "id": "feedback_" + uuid.uuid4().hex[:8],
            "execution_id": execution_id,
            "action": action,
            "result": result,
            "agents": agents or [],
            "revenue_value": revenue_value,
            "timestamp": time.time()
        }

        self.executions.append(event)

        self._score_agents(
            agents or [],
            result
        )

        self._create_lesson(event)

        print("🧠 Execution feedback recorded")

        return event


    def _score_agents(self, agents, result):

        success = 1 if result == "SUCCESS" else 0

        for agent in agents:

            if agent not in self.agent_scores:
                self.agent_scores[agent] = {
                    "tasks":0,
                    "successes":0,
                    "score":0
                }

            data = self.agent_scores[agent]

            data["tasks"] += 1
            data["successes"] += success

            data["score"] = round(
                data["successes"] /
                data["tasks"],
                2
            )


    def _create_lesson(self, event):

        lesson = {
            "id":"lesson_" + uuid.uuid4().hex[:8],
            "action":event["action"],
            "result":event["result"],
            "learning":
                "Improve future execution decisions",
            "timestamp":time.time()
        }

        self.lessons.append(lesson)


    def improve_signal(self):

        return {
            "system":
                self.system,

            "executions":
                len(self.executions),

            "agents":
                self.agent_scores,

            "lessons":
                len(self.lessons),

            "status":
                "LEARNING",

            "timestamp":
                time.time()
        }


    def report(self):

        return {
            "system":
                self.system,

            "executions":
                len(self.executions),

            "agent_scores":
                self.agent_scores,

            "lessons":
                len(self.lessons),

            "status":
                "ONLINE",

            "timestamp":
                time.time()
        }


genesis_execution_feedback_engine = (
    GenesisExecutionFeedbackEngine()
)
