import time


class GenesisCapabilityMatcher:


    def __init__(self):

        self.system = (
            "GENESIS CAPABILITY MATCHER v1"
        )


    def match(
        self,
        agents,
        required
    ):


        matches = []


        for agent in agents:

            skills = agent["capabilities"]

            if any(
                skill in required
                for skill in skills
            ):

                matches.append(agent)


        return {

            "required":
                required,

            "matches":
                matches,

            "timestamp":
                time.time()

        }
