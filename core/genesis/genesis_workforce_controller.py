import time
import uuid


from core.genesis.agent_registry import agent_registry
from core.genesis.agent_matching_engine import agent_matching_engine
from core.genesis.worker_registry import worker_registry



class GenesisWorkforceController:
    """
    GENESIS WORKFORCE CONTROLLER v2

    Unified execution workforce layer.

    Responsibilities:

    - Connect agent registry
    - Connect matching engine
    - Assign missions
    - Activate workers
    - Track assignments

    Authority:

    Command Center
          |
          v
    Workforce Controller
          |
          v
    Agents
    """



    def __init__(self):

        self.system = (
            "GENESIS WORKFORCE CONTROLLER v2"
        )


        self.agent_registry = agent_registry

        self.agent_matching_engine = (
            agent_matching_engine
        )


        self.worker_registry = (
            worker_registry
        )


        self.assignments = []



        self.sync()



    def sync(self):

        synced = 0


        for name, agent in self.agent_registry.agents.items():

            self.agent_matching_engine.register_agent(
                name,
                agent.get(
                    "skills",
                    []
                )
            )

            synced += 1


        return synced



    def find_agents(self, mission):

        required = mission.get(
            "required_capabilities",
            []
        )


        result = self.agent_matching_engine.match(
            mission
        )


        return result.get(
            "team",
            []
        )



    def assign_mission(self, mission):


        team = self.find_agents(
            mission
        )


        assignment = {


            "id":
            "workforce_" + uuid.uuid4().hex[:8],


            "mission":
            mission.get(
                "id"
            ),


            "objective":
            mission.get(
                "objective",
                ""
            ),


            "agents":
            team,


            "status":
            "ASSIGNED",


            "timestamp":
            time.time()

        }


        self.assignments.append(
            assignment
        )


        return assignment



    def activate_workers(self, assignment):


        workers = []


        for agent in assignment.get(
            "agents",
            []
        ):


            worker = {


                "id":
                "worker_" + uuid.uuid4().hex[:8],


                "agent":
                agent.get(
                    "agent"
                ),


                "status":
                "READY",


                "mission":
                assignment.get(
                    "mission"
                )


            }


            workers.append(
                worker
            )


        assignment["workers"] = workers


        return workers



    def monitor(self):

        return {


            "system":
            self.system,


            "assignments":
            len(
                self.assignments
            ),


            "connected_agents":
            len(
                self.agent_matching_engine.agents
            ),


            "status":
            "ONLINE",


            "timestamp":
            time.time()

        }



    def report(self):

        return {


            "system":
            self.system,


            "assignments":
            len(
                self.assignments
            ),


            "agents_connected":
            len(
                self.agent_matching_engine.agents
            ),


            "status":
            "ONLINE",


            "timestamp":
            time.time()

        }



genesis_workforce_controller = GenesisWorkforceController()
