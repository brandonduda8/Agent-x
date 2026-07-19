import uuid
import time


from core.genesis.command_center.system_monitor import (
    system_monitor
)

from core.genesis.command_center.intelligence_aggregator import (
    intelligence_aggregator
)

from core.genesis.command_center.decision_engine import (
    decision_engine
)

from core.genesis.command_center.resource_governor import (
    resource_governor
)

from core.genesis.command_center.execution_dispatcher import (
    execution_dispatcher
)


class CommandBrain:

    def __init__(self):
        self.cycles=[]


    def execute(self):

        print(
            "👑 Command Center activated"
        )

        systems = system_monitor.scan()

        intelligence = intelligence_aggregator.analyze(
            systems
        )

        decision = decision_engine.decide(
            intelligence
        )

        resources = resource_governor.allocate(
            decision
        )

        execution = execution_dispatcher.dispatch(
            decision
        )


        cycle = {
            "id":
            f"command_{uuid.uuid4().hex[:8]}",
            "systems":systems,
            "intelligence":intelligence,
            "decision":decision,
            "resources":resources,
            "execution":execution,
            "status":"COMPLETE",
            "timestamp":time.time()
        }


        self.cycles.append(cycle)


        print(
            "👑 Strategic command cycle complete"
        )

        return cycle


command_brain = CommandBrain()
