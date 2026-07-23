import time

from genesis_core.router.skill_analyzer import GenesisSkillAnalyzer
from genesis_core.router.agent_selector import GenesisAgentSelector



class GenesisMetaMissionRouter:


    def __init__(
        self,
        capability_map
    ):

        self.capability_map = capability_map

        self.analyzer = GenesisSkillAnalyzer()

        self.selector = GenesisAgentSelector()



    def route(
        self,
        mission
    ):

        required_skills = self.analyzer.analyze(
            mission
        )


        agents = self.selector.select(

            required_skills,

            self.capability_map

        )


        return {

            "system":
            "GENESIS META MISSION ROUTER v1",

            "mission":
            mission,

            "required_skills":
            required_skills,

            "assigned_agents":
            agents,

            "status":
            "READY",

            "timestamp":
            time.time()

        }
