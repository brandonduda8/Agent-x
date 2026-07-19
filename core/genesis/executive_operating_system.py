import time
import uuid

from core.genesis.event_stream import event_stream
from core.genesis.agent_registry import agent_registry
from core.genesis.tool_registry import tool_registry
from core.genesis.business_automation_engine import business_automation_engine
from core.genesis.lead_generation_engine import lead_generation_engine
from core.genesis.crm_agent import crm_agent


class GenesisExecutiveOperatingSystem:

    def __init__(self):
        self.system = "GENESIS EXECUTIVE OPERATING SYSTEM v1"
        self.running = False
        self.decisions = []
        self.missions = []
        self.reports = []


    def start(self):

        self.running = True

        event_stream.emit(
            "EXECUTIVE_OS_STARTED",
            self.system
        )

        print("""
================================
🧬 GENESIS EXECUTIVE OS ONLINE
================================
""")

        return self.status()


    def create_ceo_decision(self, objective):

        decision = {

            "id":
                "decision_" + uuid.uuid4().hex[:8],

            "objective":
                objective,

            "agents":
                list(agent_registry.agents.keys()),

            "tools":
                list(tool_registry.tools.keys()),

            "timestamp":
                time.time()
        }


        self.decisions.append(decision)


        event_stream.emit(
            "CEO_DECISION_CREATED",
            decision
        )


        return decision



    def create_mission(self, objective):

        mission = {

            "id":
                "mission_" + uuid.uuid4().hex[:8],

            "objective":
                objective,

            "status":
                "READY",

            "created":
                time.time()
        }


        self.missions.append(mission)


        event_stream.emit(
            "EXECUTIVE_MISSION_CREATED",
            mission
        )


        return mission



    def revenue_report(self):

        return {

            "leads":
                lead_generation_engine.status(),

            "crm":
                crm_agent.status(),

            "business":
                business_automation_engine.status()

        }



    def status(self):

        return {

            "system":
                self.system,

            "running":
                self.running,

            "decisions":
                len(self.decisions),

            "missions":
                len(self.missions),

            "timestamp":
                time.time()

        }



executive_os = GenesisExecutiveOperatingSystem()
