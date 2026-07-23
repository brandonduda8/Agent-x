import time


class GenesisBusinessNetworkEngine:


    def __init__(
        self,
        entities,
        graph,
        revenue
    ):

        self.entities = entities
        self.graph = graph
        self.revenue = revenue

        self.system = (
            "GENESIS GLOBAL BUSINESS NETWORK v1"
        )


    def create_business_system(
        self,
        business,
        offer,
        worker
    ):


        company = self.entities.create(

            "business",

            business,

            {}

        )


        service = self.entities.create(

            "offer",

            offer,

            {}

        )


        person = self.entities.create(

            "worker",

            worker,

            {}

        )


        self.graph.connect(

            company["id"],

            "needs",

            service["id"]

        )


        self.graph.connect(

            service["id"],

            "assigned_to",

            person["id"]

        )


        return {


            "system":
                self.system,

            "business":
                company,

            "offer":
                service,

            "worker":
                person,

            "status":
                "NETWORK_CREATED",

            "timestamp":
                time.time()

        }
