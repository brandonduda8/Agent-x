import time
import uuid


class ExperimentAgent:

    def __init__(self):
        self.system = "GENESIS EXPERIMENT AGENT v1"
        self.experiments = []

    def create(self, strategy):

        experiment = {
            "id": "experiment_" + uuid.uuid4().hex[:8],
            "strategy": strategy,
            "test": "Optimize execution variables",
            "status": "READY",
            "timestamp": time.time()
        }

        self.experiments.append(experiment)

        print("🔬 Experiment created")

        return experiment


experiment_agent = ExperimentAgent()
