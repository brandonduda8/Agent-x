import time


class GenesisSkillMatcher:


    def match(
        self,
        job,
        workers
    ):

        matches = []


        for worker in workers.values():

            skills = worker["skills"]


            if all(

                skill in skills

                for skill in job["required_skills"]

            ):

                matches.append(worker)



        return {

            "job":
                job["id"],

            "matches":
                matches,

            "timestamp":
                time.time()

        }
