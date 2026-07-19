import time

from core.genesis.memory_engine import memory_engine


class GenesisLearningEngine:


    def __init__(self):

        self.name = "GENESIS LEARNING ENGINE v1"



    def analyze_success(
        self,
        agent,
        mission,
        result
    ):

        lesson = (
            f"{agent} successfully completed "
            f"{mission}"
        )

        memory_engine.remember_lesson(
            lesson,
            source=agent
        )


        memory_engine.record_performance(
            agent,
            True
        )


        memory_engine.remember_knowledge(
            "successful_strategy",
            result,
            confidence=0.7
        )


        return {

            "status":
                "LEARNED",

            "lesson":
                lesson

        }



    def analyze_failure(
        self,
        agent,
        mission,
        error
    ):

        lesson = (
            f"Avoid failure pattern: {error}"
        )


        memory_engine.remember_lesson(
            lesson,
            source=agent
        )


        memory_engine.record_performance(
            agent,
            False
        )


        return {

            "status":
                "LEARNED_FROM_FAILURE",

            "lesson":
                lesson

        }



    def report(self):

        return {

            "engine":
                self.name,

            "memory":
                memory_engine.report(),

            "timestamp":
                time.time()

        }



learning_engine = GenesisLearningEngine()
