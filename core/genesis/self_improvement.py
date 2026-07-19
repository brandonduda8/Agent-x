import os
import json
import time


class GenesisSelfImprovement:


    def __init__(self):

        self.name = "GENESIS SELF IMPROVEMENT ENGINE v1"

        self.file = "data/genesis_learning.json"

        os.makedirs(
            "data",
            exist_ok=True
        )

        self.initialize()



    def initialize(self):

        if not os.path.exists(self.file):

            with open(
                self.file,
                "w"
            ) as f:

                json.dump(
                    {
                        "failures": [],
                        "lessons": [],
                        "improvements": []
                    },
                    f,
                    indent=2
                )



    def load(self):

        with open(
            self.file,
            "r"
        ) as f:

            return json.load(f)



    def save(
        self,
        data
    ):

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                data,
                f,
                indent=2
            )



    def record_failure(
        self,
        system,
        error
    ):

        data = self.load()


        lesson = {

            "system":
                system,

            "error":
                error,

            "timestamp":
                time.time(),

            "recommendation":
                self.analyze_failure(error)

        }


        data["failures"].append(
            lesson
        )


        data["lessons"].append(
            lesson["recommendation"]
        )


        self.save(
            data
        )


        return lesson



    def analyze_failure(
        self,
        error
    ):

        error = str(error).lower()


        if "read-only" in error:

            return (
                "Use Genesis workspace manager "
                "instead of system directories."
            )


        if "json" in error:

            return (
                "Add JSON validation and repair "
                "before execution."
            )


        if "missing" in error:

            return (
                "Add dependency detection "
                "before mission execution."
            )


        return (
            "Monitor failure and create "
            "future improvement."
        )



    def suggest_upgrades(self):

        data = self.load()


        return {

            "engine":
                self.name,

            "failures":
                len(data["failures"]),

            "lessons":
                data["lessons"],

            "recommended_action":
                "Review failures and improve agents"

        }



self_improvement = GenesisSelfImprovement()
