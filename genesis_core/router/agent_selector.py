class GenesisAgentSelector:


    def select(
        self,
        skills,
        capability_map
    ):

        assignments = []


        for skill in skills:

            workers = capability_map.get(
                skill,
                []
            )


            for worker in workers:

                assignments.append({

                    "skill":
                    skill,

                    "agent":
                    worker

                })


        return assignments
