import time

from core.genesis.agent_factory import agent_factory
from core.genesis.agent_registry import agent_registry


class GenesisSTEMIntelligenceFactory:

    def __init__(self):

        self.system = "GENESIS STEM INTELLIGENCE FACTORY v1"

        self.created = []


    def build_stem_division(self):

        specialists = [

            (
                "Computer Science Architect",
                [
                    "algorithms",
                    "data structures",
                    "system architecture",
                    "optimization"
                ]
            ),

            (
                "Software Engineer",
                [
                    "Python",
                    "APIs",
                    "automation",
                    "debugging",
                    "testing"
                ]
            ),

            (
                "AI Engineer",
                [
                    "AI",
                    "LLM",
                    "agents",
                    "MCP",
                    "model routing"
                ]
            ),

            (
                "QA Scientist",
                [
                    "testing",
                    "validation",
                    "quality",
                    "security"
                ]
            ),

            (
                "Knowledge Engineer",
                [
                    "documentation",
                    "codebase mapping",
                    "memory",
                    "knowledge systems"
                ]
            )

        ]


        for role, skills in specialists:

            factory_agent = agent_factory.create_agent(
                role,
                skills
            )


            registry_agent = agent_registry.register(
                factory_agent["name"],
                role,
                skills,
                "GENESIS_STEM"
            )


            self.created.append(
                registry_agent
            )


        return {

            "status":
                "STEM DIVISION CREATED",

            "agents":
                self.created,

            "timestamp":
                time.time()

        }


    def report(self):

        return {

            "system":
                self.system,

            "agents_created":
                len(
                    self.created
                ),

            "timestamp":
                time.time()

        }


genesis_stem_intelligence_factory = GenesisSTEMIntelligenceFactory()
