import json
import os
import time


class GenesisSkillRegistry:

    def __init__(self):

        self.name = "GENESIS SKILL REGISTRY v1"

        self.file = "data/genesis_skills.json"

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.initialize()


    def initialize(self):

        if not os.path.exists(self.file):

            skills = {

                "coding": {

                    "description":
                    "Software development and programming",

                    "tools":
                    [
                        "python",
                        "node",
                        "git"
                    ]

                },

                "research": {

                    "description":
                    "Internet research and analysis",

                    "tools":
                    [
                        "httpx",
                        "beautifulsoup4"
                    ]

                },

                "hardware_control": {

                    "description":
                    "Android device intelligence",

                    "tools":
                    [
                        "camera",
                        "sensor",
                        "battery",
                        "notification"
                    ]

                },

                "security": {

                    "description":
                    "Protect Genesis system",

                    "tools":
                    [
                        "sensors",
                        "notifications"
                    ]

                },

                "business": {

                    "description":
                    "Revenue generation and SaaS planning",

                    "tools":
                    [
                        "research",
                        "coding"
                    ]

                }

            }


            with open(
                self.file,
                "w"
            ) as f:

                json.dump(
                    skills,
                    f,
                    indent=2
                )



    def list_skills(self):

        with open(
            self.file,
            "r"
        ) as f:

            return json.load(f)



    def find_skill(self, name):

        skills = self.list_skills()

        return skills.get(
            name,
            None
        )



    def register_skill(
        self,
        name,
        description,
        tools
    ):

        skills = self.list_skills()


        skills[name] = {

            "description":
                description,

            "tools":
                tools,

            "created":
                time.time()

        }


        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                skills,
                f,
                indent=2
            )


        return {
            "created":True,
            "skill":name
        }



skill_registry = GenesisSkillRegistry()
