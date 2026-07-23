
class GenesisSkillMatcher:


    def match(
        self,
        mission,
        agents
    ):


        required = self.required_skills(
            mission
        )


        matches = []


        for agent in agents:

            score = len(

                set(required)

                &

                set(agent["skills"])

            )


            if score > 0:

                matches.append(

                    {

                    "agent":
                    agent["name"],

                    "agent_id":
                    agent["id"],

                    "skills_matched":
                    score

                    }

                )


        return sorted(

            matches,

            key=lambda x:
            x["skills_matched"],

            reverse=True

        )



    def required_skills(
        self,
        mission
    ):

        objective = mission["objective"].lower()


        if "dental" in objective or "automation" in objective:

            return [

                "research",

                "sales",

                "coding"

            ]


        return [

            "research",

            "writing",

            "applications"

        ]
