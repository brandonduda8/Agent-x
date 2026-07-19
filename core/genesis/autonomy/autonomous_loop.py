import time
import uuid


from core.genesis.autonomy.goal_manager import (
    goal_manager
)

from core.genesis.autonomy.mission_scheduler import (
    mission_scheduler
)

from core.genesis.autonomy.execution_monitor import (
    execution_monitor
)


from core.genesis.company.company_operator import (
    company_operator
)


from core.genesis.swarm.swarm_commander import (
    swarm_commander
)



class GenesisAutonomousLoop:


    def __init__(self):

        self.system = "GENESIS AUTONOMOUS LOOP v1"
        self.cycles = []



    def run(
        self,
        objective,
        company_name,
        market
    ):


        print(
            "♻️ Genesis autonomous cycle started"
        )


        goal = goal_manager.create_goal(
            objective
        )


        mission = mission_scheduler.schedule(
            goal
        )


        swarm = swarm_commander.create_swarm(
            objective
        )


        company = company_operator.create_company(
            company_name,
            market,
            objective
        )


        execution = execution_monitor.monitor(
            mission
        )


        cycle = {

            "id":
            "autonomous_cycle_" +
            uuid.uuid4().hex[:8],

            "objective":
            objective,

            "goal":
            goal,

            "mission":
            mission,

            "swarm":
            swarm,

            "company":
            company,

            "execution":
            execution,

            "status":
            "COMPLETE",

            "timestamp":
            time.time()

        }


        self.cycles.append(cycle)


        print(
            "🚀 Genesis autonomous cycle complete"
        )


        return cycle



    def report(self):

        return {

            "system":
            self.system,

            "cycles":
            len(self.cycles),

            "timestamp":
            time.time()

        }



autonomous_loop = GenesisAutonomousLoop()
