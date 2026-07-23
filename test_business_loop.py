
from genesis_core.business_loop.business_loop import GenesisBusinessLoop


class MockWorld:

    opportunities = [

        {

        "name":
        "Dental AI Reception Automation",

        "value":
        999

        },

        {

        "name":
        "AI Automation Assistant",

        "value":
        1000

        }

    ]



class MockOrchestrator:

    def run(
        self,
        opportunity
    ):

        return {

        "cycle":
        "executed_" + opportunity["name"]

        }



class MockMemory:

    def store(
        self,
        *args
    ):

        return True



loop = GenesisBusinessLoop(

    MockWorld(),

    MockOrchestrator(),

    MockMemory()

)


print(
loop.run_cycle()
)


print(
loop.status()
)

