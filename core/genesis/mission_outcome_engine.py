import time
import uuid


class GenesisMissionOutcomeEngine:

    """
    GENESIS MISSION OUTCOME ENGINE v2

    Converts:

    Worker Execution Results
            |
            v
    Business Intelligence
            |
            v
    Learning + Next Actions
    """

    def __init__(self):

        self.system = (
            "GENESIS MISSION OUTCOME ENGINE v2"
        )

        self.outcomes = []


    def evaluate(
        self,
        mission,
        results
    ):

        print(
            "🧠 Evaluating mission outcome"
        )


        completed_agents = []

        capabilities = []

        discoveries = []

        intelligence = []


        for result in results:


            worker = result.get(
                "worker"
            )


            if worker:

                completed_agents.append(
                    worker
                )


            output = result.get(
                "output",
                {}
            )


            if not isinstance(output, dict):

                continue


            # Capture discoveries

            if "discoveries" in output:

                discoveries.extend(
                    output["discoveries"]
                )


                capabilities.append(
                    "market_research"
                )


            # Capture offers

            if "offer" in output:

                intelligence.append(
                    output["offer"]
                )


                capabilities.append(
                    "offer_creation"
                )


            # Capture workflows

            if "workflow" in output:

                intelligence.append(
                    output["workflow"]
                )


                capabilities.append(
                    "workflow_automation"
                )


            # Capture outreach

            if "outreach" in output:

                intelligence.append(
                    output["outreach"]
                )


                capabilities.append(
                    "client_acquisition"
                )


            # Generic mission capture

            if output.get("mission"):

                intelligence.append(
                    output["mission"]
                )


        success_score = 0


        if completed_agents:

            success_score += 25


        if capabilities:

            success_score += 25


        if discoveries or intelligence:

            success_score += 25


        if mission.get(
            "objective"
        ):

            success_score += 25



        next_actions = self.generate_next_actions(
            mission,
            discoveries,
            intelligence
        )


        outcome = {

            "id":
                "outcome_"
                + uuid.uuid4().hex[:8],


            "mission":
                mission.get(
                    "id"
                ),


            "objective":
                mission.get(
                    "objective"
                ),


            "completed_agents":
                completed_agents,


            "capabilities_used":
                list(
                    set(
                        capabilities
                    )
                ),


            "discoveries":
                discoveries,


            "business_intelligence":
                intelligence,


            "success_score":
                success_score,


            "next_actions":
                next_actions,


            "status":
                "COMPLETE",


            "timestamp":
                time.time()

        }


        self.outcomes.append(
            outcome
        )


        print(
            f"📊 Mission score: {success_score}/100"
        )


        return outcome



    def generate_next_actions(
        self,
        mission,
        discoveries,
        intelligence
    ):

        actions = []


        objective = mission.get(
            "objective",
            ""
        ).lower()



        if (
            "client" in objective
            or
            "customer" in objective
            or
            "revenue" in objective
            or
            "sales" in objective
        ):

            actions.extend(

                [

                    "Extract qualified prospects",

                    "Generate personalized outreach",

                    "Create sales pipeline entries",

                    "Track responses",

                    "Optimize offer"

                ]

            )


        if discoveries:

            actions.append(
                "Analyze market discoveries"
            )


        if intelligence:

            actions.append(
                "Store business intelligence"
            )


        if not actions:

            actions.append(
                "Continue mission optimization"
            )


        return actions



    def report(self):

        return {

            "system":
                self.system,

            "outcomes":
                len(
                    self.outcomes
                ),

            "timestamp":
                time.time()

        }



mission_outcome_engine = GenesisMissionOutcomeEngine()
