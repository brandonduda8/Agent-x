import time


class GenesisCapabilityAnalyzer:


    def __init__(self):

        self.system = (
            "GENESIS CAPABILITY ANALYZER v1"
        )


    def analyze(self, mission):

        capabilities = []


        text = mission.lower()


        if any(word in text for word in [
            "research",
            "find",
            "analyze",
            "market"
        ]):
            capabilities.append(
                "research"
            )


        if any(word in text for word in [
            "sell",
            "revenue",
            "customer",
            "lead"
        ]):
            capabilities.append(
                "sales"
            )


        if any(word in text for word in [
            "automation",
            "workflow",
            "system"
        ]):
            capabilities.append(
                "automation"
            )


        if any(word in text for word in [
            "ai",
            "model",
            "reason"
        ]):
            capabilities.append(
                "reasoning"
            )


        return {

            "mission": mission,

            "required_capabilities":
                list(set(capabilities)),

            "timestamp":
                time.time()

        }
