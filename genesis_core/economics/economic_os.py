import time
import uuid


class GenesisEconomicOS:


    def __init__(self):

        self.opportunities = []

        self.missions = []

        self.revenue_events = []



    def add_opportunity(
        self,
        name,
        category,
        value
    ):

        opportunity = {

            "id":
            "opp_" + uuid.uuid4().hex[:8],

            "name":
            name,

            "category":
            category,

            "value":
            value,

            "status":
            "NEW",

            "timestamp":
            time.time()

        }


        self.opportunities.append(
            opportunity
        )

        return opportunity



    def add_mission(
        self,
        mission,
        value
    ):

        item = {

            "id":
            "economic_mission_" +
            uuid.uuid4().hex[:8],

            "mission":
            mission,

            "value":
            value,

            "status":
            "ACTIVE",

            "timestamp":
            time.time()

        }


        self.missions.append(
            item
        )

        return item



    def record_revenue(
        self,
        source,
        amount
    ):

        event = {

            "id":
            "revenue_" +
            uuid.uuid4().hex[:8],

            "source":
            source,

            "amount":
            amount,

            "timestamp":
            time.time()

        }


        self.revenue_events.append(
            event
        )

        return event



    def dashboard(self):

        pipeline = sum(

            x["value"]

            for x in self.opportunities

        )


        revenue = sum(

            x["amount"]

            for x in self.revenue_events

        )


        return {

            "system":
            "GENESIS ECONOMIC OPERATING SYSTEM v1",

            "pipeline_value":
            pipeline,

            "active_missions":
            len(self.missions),

            "revenue":
            revenue,

            "timestamp":
            time.time()

        }
