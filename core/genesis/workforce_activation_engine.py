import time


class GenesisWorkforceActivationEngine:


    def __init__(
        self,
        agent_manager,
        harness
    ):

        self.system = (
            "GENESIS WORKFORCE ACTIVATION ENGINE v1"
        )

        self.agent_manager = agent_manager
        self.harness = harness

        self.active_workers = []



    def activate(self):

        agents = (
            self.agent_manager.list_agents()
        )


        activated = []


        for agent_id, agent in agents.items():

            worker = GenesisWorker(
                agent["name"],
                agent["capabilities"]
            )


            self.harness.register(
                worker
            )


            self.active_workers.append(
                worker
            )


            activated.append(
                {
                    "id":
                    agent_id,

                    "name":
                    agent["name"],

                    "status":
                    "ONLINE",

                    "capabilities":
                    agent["capabilities"]
                }
            )


        return {

            "system":
            self.system,

            "workers":
            activated,

            "count":
            len(activated),

            "timestamp":
            time.time()

        }



    def report(self):

        return {

            "system":
            self.system,

            "active_workers":
            len(self.active_workers),

            "workers":
            [
                worker.name
                for worker in self.active_workers
            ],

            "timestamp":
            time.time()

        }



class GenesisWorker:


    def __init__(
        self,
        name,
        capabilities
    ):

        self.name = name

        self.capabilities = capabilities



    def execute(
        self,
        mission
    ):

        return {

            "agent":
            self.name,

            "mission":
            mission,

            "status":
            "COMPLETE",

            "timestamp":
            time.time()

        }
