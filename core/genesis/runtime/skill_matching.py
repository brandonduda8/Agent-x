import time


class GenesisSkillMatcher:


    def __init__(
        self,
        registry
    ):

        self.registry = registry


    def match(
        self,
        required_skill
    ):

        matches = []


        for worker in self.registry.workers.values():

            if required_skill in worker["skills"]:

                matches.append(worker)


        return {

            "skill":
                required_skill,

            "matches":
                matches,

            "timestamp":
                time.time()

        }
