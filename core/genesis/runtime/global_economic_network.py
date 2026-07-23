import time


class GenesisGlobalEconomicNetwork:


    def __init__(
        self,
        graph,
        businesses,
        workers
    ):

        self.graph = graph
        self.businesses = businesses
        self.workers = workers

        self.system = (
            "GENESIS GLOBAL ECONOMIC NETWORK v1"
        )


    def create_network(self):


        business = self.businesses.register(

            "Smile Dental Clinic",

            "Dental",

            "Lost appointments and missed calls"

        )


        worker = self.workers.register(

            "AI Automation Builder",

            [

                "automation",

                "AI systems"

            ],

            "agent"

        )


        self.graph.add_node(business)

        self.graph.add_node(worker)


        self.graph.connect(

            business["id"],

            worker["id"],

            "solution_provider"

        )


        return {

            "system":
                self.system,

            "network":
                self.graph.view(),

            "status":
                "NETWORK_OPERATIONAL",

            "timestamp":
                time.time()

        }
