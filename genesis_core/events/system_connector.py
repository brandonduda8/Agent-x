class GenesisSystemConnector:


    def __init__(
        self,
        bus
    ):

        self.bus = bus



    def opportunity_created(
        self,
        opportunity
    ):

        return self.bus.publish(

            "OPPORTUNITY_CREATED",

            opportunity

        )



    def mission_created(
        self,
        mission
    ):

        return self.bus.publish(

            "MISSION_CREATED",

            mission

        )



    def task_completed(
        self,
        result
    ):

        return self.bus.publish(

            "TASK_COMPLETED",

            result

        )



    def revenue_event(
        self,
        revenue
    ):

        return self.bus.publish(

            "REVENUE_EVENT",

            revenue

        )
