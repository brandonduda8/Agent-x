import time
import uuid


class GenesisLearningFeedbackLoop:


    def __init__(
        self,
        analyzer,
        memory
    ):

        self.analyzer = analyzer

        self.memory = memory

        self.system = (
            "GENESIS LEARNING FEEDBACK LOOP v2"
        )


    def learn(self, execution):


        insight = (
            self.analyzer.analyze(
                execution
            )
        )


        stored = (
            self.memory.store(
                insight
            )
        )


        return {

            "id":
                "learning_" +
                uuid.uuid4().hex[:8],

            "system":
                self.system,

            "insight":
                insight,

            "memory":
                stored,

            "status":
                "LEARNING_COMPLETE",

            "timestamp":
                time.time()

        }
