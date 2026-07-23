import time
import uuid


class GenesisBusinessLoop:


    def __init__(
        self,
        world=None,
        orchestrator=None,
        memory=None,
        patterns=None
    ):

        self.world = world
        self.orchestrator = orchestrator
        self.memory = memory
        self.patterns = patterns

        self.cycles = []



    def run_cycle(self):

        cycle = {

            "id":
            "business_cycle_" +
            uuid.uuid4().hex[:8],

            "steps": [],

            "timestamp":
            time.time()

        }


        # Discover

        opportunities = []


        if self.world:

            opportunities = (
                self.world.opportunities
            )


        cycle["steps"].append({

            "discover":

            len(opportunities)

        })



        if opportunities:

            # prioritize highest value

            opportunity = max(

                opportunities,

                key=lambda x:

                x.get(
                    "value",
                    0
                )

            )


            cycle["steps"].append({

                "selected":

                opportunity["name"]

            })


            # execute through orchestrator

            if self.orchestrator:

                result = self.orchestrator.run(
                    opportunity
                )


                cycle["steps"].append({

                    "execution":

                    result["cycle"]

                })



            # store learning

            if self.memory:

                self.memory.store(

                    "business_cycle",

                    "Genesis Business Loop",

                    {

                    "opportunity":

                    opportunity["name"],

                    "value":

                    opportunity.get(
                        "value",
                        0
                    )

                    }

                )



        self.cycles.append(
            cycle
        )


        return cycle



    def status(self):

        return {

            "system":

            "GENESIS AUTONOMOUS BUSINESS LOOP v1",

            "cycles":

            len(self.cycles),

            "status":

            "ONLINE",

            "timestamp":

            time.time()

        }
