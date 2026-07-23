import time
import uuid


from core.genesis.omega.command_center.mission_database import (
    genesis_mission_database
)

from core.genesis.omega.command_center.approval_system import (
    genesis_approval_system
)

from core.genesis.omega.command_center.decision_gate import (
    genesis_decision_gate
)


try:
    from core.genesis.omega.command_center.event_bus import (
        genesis_event_bus
    )
except Exception:
    genesis_event_bus = None



class GenesisOmegaMissionExecutionLoop:


    def __init__(self):

        self.system = (
            "GENESIS OMEGA MISSION EXECUTION LOOP v3"
        )

        self.executions = []



    def run(self, mission_id=None):

        mission = self._get_mission(
            mission_id
        )


        if not mission:

            return {
                "status": "NO_MISSION"
            }


        execution = {

            "id":
                "execution_"
                + uuid.uuid4().hex[:8],

            "mission":
                mission["id"],

            "objective":
                mission["objective"],

            "status":
                "PLANNING",

            "created":
                time.time()

        }


        self.executions.append(
            execution
        )


        print(
            "🚀 Mission Execution Started:",
            execution["objective"]
        )


        return self.plan(
            execution
        )



    def plan(self, execution):


        tasks = [
            "discover_opportunities",
            "research_targets",
            "generate_solution",
            "prepare_execution",
            "create_outreach",
            "qualify_leads",
            "follow_up_prospects"
        ]

        execution["tasks"] = tasks


        try:

            decision = (
                genesis_decision_gate.evaluate(
                    execution["objective"],
                    "Genesis Mission Execution Loop"
                )
            )


        except Exception as e:

            decision = {

                "status":
                    "WAITING_APPROVAL",

                "reason":
                    str(e)

            }



        execution["decision"] = decision


        print(
            "🧠 Decision:",
            decision
        )


        if (
            isinstance(decision, dict)
            and decision.get("status")
            in [
                "WAITING_APPROVAL",
                "APPROVAL_REQUIRED"
            ]
        ):


            approval = (
                genesis_approval_system.request_approval(

                    action=
                    execution["objective"],

                    worker=
                    "Genesis Mission Execution Loop",

                    data={
                        "tasks": tasks
                    }

                )
            )


            execution["approval"] = approval


            print(
                "🔐 Approval Requested:",
                approval["id"]
            )


        else:

            execution["status"] = (
                "READY_FOR_EXECUTION"
            )


        return execution



    def approve_and_execute(
        self,
        approval_id
    ):


        approval = (
            genesis_approval_system.approve(
                approval_id
            )
        )


        if approval.get(
            "status"
        ) != "APPROVED":

            return approval


        return self.execute(
            approval
        )



    def execute(
        self,
        approval
    ):


        result = {

            "status":
                "EXECUTED",

            "approval":
                approval["id"],

            "timestamp":
                time.time()

        }


        print(
            "✅ Mission Execution Complete"
        )


        return result



    def _get_mission(
        self,
        mission_id=None
    ):

        missions = (
            genesis_mission_database.list_all()
        )


        if not missions:

            return None


        if mission_id:

            for mission in missions:

                if mission["id"] == mission_id:

                    return mission


        return missions[-1]



    def report(self):

        return {

            "system":
                self.system,

            "executions":
                len(self.executions),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_mission_execution_loop = (
    GenesisOmegaMissionExecutionLoop()
)
