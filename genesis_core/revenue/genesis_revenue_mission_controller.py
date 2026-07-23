import time
import uuid


class GenesisRevenueMissionController:


    def __init__(
        self,
        economic_os,
        revenue_engine,
        crm,
        event_bus=None
    ):

        self.system = (
            "GENESIS REVENUE MISSION CONTROLLER v1"
        )

        self.economic = economic_os
        self.revenue = revenue_engine
        self.crm = crm
        self.event_bus = event_bus

        self.missions = []


    def create_revenue_mission(
        self,
        business,
        industry,
        problem,
        offer,
        value
    ):

        mission = {

            "id":
                "revenue_mission_" +
                uuid.uuid4().hex[:8],

            "business":
                business,

            "industry":
                industry,

            "problem":
                problem,

            "offer":
                offer,

            "value":
                value,

            "status":
                "ACTIVE",

            "created":
                time.time()
        }


        opportunity = (
            self.economic.add_opportunity(
                offer,
                industry,
                value
            )
        )


        lead = (
            self.crm.create_lead(
                business,
                industry,
                problem,
                value
            )
        )


        revenue_lead = (
            self.revenue.create_lead(
                {
                    "title": offer,
                    "estimated_value": value
                }
            )
        )


        mission["opportunity"] = opportunity
        mission["crm_lead"] = lead
        mission["revenue_lead"] = revenue_lead


        self.missions.append(
            mission
        )


        if self.event_bus:

            self.event_bus.publish(
                "REVENUE_MISSION_CREATED",
                mission
            )


        return mission



    def report(self):

        return {

            "system":
                self.system,

            "missions":
                len(self.missions),

            "status":
                "ONLINE",

            "timestamp":
                time.time()
        }
