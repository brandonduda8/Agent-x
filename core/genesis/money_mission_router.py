import time
import uuid


class GenesisMoneyMissionRouter:

    """
    GENESIS MONEY MISSION ROUTER v1

    Executive revenue decision layer.

    Decides:
    - execute personally
    - create sales partner mission
    - create learning mission
    - prioritize cash opportunities
    """

    def __init__(self):

        self.system = (
            "GENESIS MONEY MISSION ROUTER v1"
        )

        self.missions = []


    def evaluate(self, opportunity):

        category = opportunity.get(
            "category",
            "UNKNOWN"
        )

        value = opportunity.get(
            "estimated_value",
            0
        )

        skills = opportunity.get(
            "skills",
            []
        )


        if category in [
            "JOB",
            "FREELANCE"
        ]:

            action = (
                "EXECUTE_APPLICATION"
            )

            reason = (
                "Genesis can prepare application package"
            )


        elif category in [
            "CLIENT",
            "DEAL"
        ]:

            action = (
                "FIND_CLOSER"
            )

            reason = (
                "High value deal requires sales execution"
            )


        else:

            action = (
                "RESEARCH"
            )

            reason = (
                "Opportunity requires analysis"
            )


        score = 0


        if value >= 5000:

            score += 50

        elif value >= 1000:

            score += 30

        else:

            score += 10


        if "ai" in [
            x.lower()
            for x in skills
        ]:

            score += 20


        if "automation" in [
            x.lower()
            for x in skills
        ]:

            score += 20


        mission = {

            "id":
                "money_"
                +
                uuid.uuid4().hex[:8],

            "opportunity":
                opportunity,

            "action":
                action,

            "reason":
                reason,

            "priority_score":
                score,

            "status":
                "READY",

            "created":
                time.time()

        }


        self.missions.append(
            mission
        )


        print(
            "💰 Money Mission Created:"
        )

        print(
            opportunity.get(
                "title"
            )
        )


        return mission



    def scan(
        self,
        opportunities
    ):

        results = []


        for opportunity in opportunities:

            results.append(
                self.evaluate(
                    opportunity
                )
            )


        results.sort(
            key=lambda x:
            x["priority_score"],
            reverse=True
        )


        return {

            "mission":
                "MAKE MONEY",

            "priority_targets":
                results,

            "timestamp":
                time.time()

        }



    def report(self):

        return {

            "system":
                self.system,

            "missions":
                len(
                    self.missions
                ),

            "timestamp":
                time.time()

        }



money_mission_router = GenesisMoneyMissionRouter()
