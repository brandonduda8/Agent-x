import time
import uuid


class GenesisMissionLearningEngine:
    """
    GENESIS MISSION LEARNING ENGINE v1.2

    Learns from:
    - completed agents
    - capabilities
    - mission outcomes
    - success scores
    """

    def __init__(self):

        self.system = "GENESIS MISSION LEARNING ENGINE v1.2"

        self.lessons = []

        self.agent_scores = {}

        self.capability_scores = {}


    def learn(self, outcome):

        print(
            "🧠 Genesis learning from mission outcome"
        )


        mission = outcome.get(
            "mission"
        )

        objective = outcome.get(
            "objective"
        )

        success_score = outcome.get(
            "success_score",
            0
        )


        agents = outcome.get(
            "agents",
            []
        )


        capabilities = outcome.get(
            "capabilities",
            []
        )


        # fallback extraction
        if not agents:

            for item in outcome.get(
                "agent_results",
                []
            ):

                agent = item.get(
                    "agent"
                )

                if agent:
                    agents.append(
                        agent
                    )


        if not capabilities:

            for item in outcome.get(
                "agent_results",
                []
            ):

                for result in item.get(
                    "results",
                    []
                ):

                    skill = result.get(
                        "skill"
                    )

                    if skill:
                        capabilities.append(
                            skill
                        )


        for agent in agents:

            if agent not in self.agent_scores:

                self.agent_scores[agent] = 0

            self.agent_scores[agent] += success_score



        for capability in capabilities:

            if capability not in self.capability_scores:

                self.capability_scores[capability] = 0

            self.capability_scores[capability] += success_score



        lesson = {

            "id":
                "lesson_" + uuid.uuid4().hex[:8],

            "mission":
                mission,

            "objective":
                objective,

            "success_score":
                success_score,

            "agents":
                agents,

            "capabilities":
                capabilities,

            "timestamp":
                time.time()

        }


        self.lessons.append(
            lesson
        )


        print(
            "🧠 Genesis learned successfully"
        )


        return lesson



    def report(self):

        return {

            "system":
                self.system,

            "lessons":
                len(
                    self.lessons
                ),

            "agent_scores":
                self.agent_scores,

            "capability_scores":
                self.capability_scores,

            "timestamp":
                time.time()

        }



mission_learning_engine = GenesisMissionLearningEngine()
