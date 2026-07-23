import time
import uuid
import json

from core.genesis.agent_registry import agent_registry
from core.genesis.llm_connector import llm_connector
from core.genesis.genesis_memory import GenesisMemory


class GenesisSTEMDivisionCommander:
    """
    GENESIS STEM DIVISION COMMANDER v2

    Responsibilities:

    - Coordinate STEM workforce
    - Assign engineering roles
    - Generate engineering plans
    - Route intelligence requests
    - Store historical knowledge
    - Prepare autonomous execution workflows
    """

    def __init__(self):

        self.system = "GENESIS STEM DIVISION COMMANDER v2"

        self.memory = GenesisMemory()

        self.executions = []


    def load_team(self):

        registry = agent_registry.report()

        return list(
            registry.get(
                "registry",
                {}
            ).values()
        )


    def build_team_context(self):

        team = self.load_team()

        if not team:
            return "No STEM agents currently registered."

        context = []

        for agent in team:

            context.append(
                {
                    "name":
                        agent.get(
                            "name"
                        ),

                    "role":
                        agent.get(
                            "role"
                        ),

                    "skills":
                        agent.get(
                            "skills",
                            []
                        )
                }
            )

        return json.dumps(
            context,
            indent=2
        )


    def request_engineering_plan(
        self,
        objective
    ):

        team_context = self.build_team_context()


        prompt = f"""

You are the Genesis STEM Division Commander.

You command this engineering workforce:

{team_context}


Engineering Objective:

{objective}


Create an engineering execution directive.

Return:

1. Architecture
2. Implementation plan
3. Agent assignments
4. Required modules
5. Testing strategy
6. Improvement loop
7. Execution workflow


The response should use the available Genesis agents effectively.

"""


        result = llm_connector.complete(
            "architecture",
            prompt
        )


        record = {

            "id":
                "stem_exec_"
                +
                uuid.uuid4().hex[:8],

            "objective":
                objective,

            "team":
                self.load_team(),

            "result":
                result,

            "timestamp":
                time.time()

        }


        self.executions.append(
            record
        )


        self.memory.store_mission(
            record
        )


        return record



    def report(self):

        return {

            "system":
                self.system,

            "executions":
                len(
                    self.executions
                ),

            "team_size":
                len(
                    self.load_team()
                ),

            "timestamp":
                time.time()

        }



stem_division_commander = GenesisSTEMDivisionCommander()
