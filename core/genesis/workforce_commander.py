import time
import uuid


class GenesisWorkforceCommander:

    def __init__(self):

        self.system = "GENESIS WORKFORCE COMMANDER v1.1"
        self.history = []


    def assign(
        self,
        objective,
        workers
    ):

        selected = []

        objective_lower = objective.lower()


        for worker in workers:

            if hasattr(worker, "name"):
                name = worker.name.lower()
                capability = getattr(
                    worker,
                    "capability",
                    ""
                ).lower()

            else:
                name = str(worker).lower()
                capability = name


            if (
                "coding" in objective_lower
                or "python" in objective_lower
                or "automation" in objective_lower
            ):

                if (
                    "coding" in name
                    or "coding" in capability
                    or "career" in name
                ):
                    selected.append(
                        name
                    )


            elif (
                "job" in objective_lower
                or "career" in objective_lower
            ):

                if (
                    "career" in name
                    or "job" in name
                ):
                    selected.append(
                        name
                    )


            elif (
                "money" in objective_lower
                or "client" in objective_lower
                or "revenue" in objective_lower
            ):

                if (
                    "revenue" in name
                    or "sales" in name
                ):
                    selected.append(
                        name
                    )


        mission = {

            "id":
                "workforce_"
                +
                uuid.uuid4().hex[:8],

            "objective":
                objective,

            "assigned":
                selected,

            "status":
                "READY",

            "created":
                time.time()

        }


        self.history.append(
            mission
        )


        print(
            "🧬 Workforce Mission Created"
        )

        print(
            "🤖 Assigned:",
            selected
        )


        return mission



    def report(
        self
    ):

        return {

            "system":
                self.system,

            "missions":
                len(self.history),

            "timestamp":
                time.time()

        }



workforce_commander = GenesisWorkforceCommander()
