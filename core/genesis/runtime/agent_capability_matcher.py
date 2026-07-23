import time


class GenesisAgentCapabilityMatcher:


    def __init__(self):

        self.system = (
            "GENESIS AGENT CAPABILITY MATCHER v1"
        )


        self.agents = {

            "Genesis Research Agent": [
                "research"
            ],

            "Genesis Revenue Agent": [
                "sales",
                "leads"
            ],

            "Genesis Automation Agent": [
                "automation",
                "workflow"
            ],

            "Genesis AI Engineer Agent": [
                "reasoning",
                "ai",
                "architecture"
            ]

        }



    def match(self, capabilities):

        matches = {}


        for capability in capabilities:

            matches[capability] = []


            for agent, skills in self.agents.items():

                if capability in skills:

                    matches[capability].append(
                        agent
                    )


        return {

            "matches": matches,

            "timestamp": time.time()

        }
