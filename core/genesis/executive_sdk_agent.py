import time
import uuid

from core.genesis.llm_connector import llm_connector

from core.genesis.persistent_memory_core import (
    genesis_persistent_memory_core
)


class GenesisExecutiveSDKAgent:

    def __init__(self):

        self.system = "GENESIS EXECUTIVE SDK AGENT v1"
        self.executions = []


    def detect_capability(self, mission):

        text = mission.lower()

        if any(word in text for word in [
            "python",
            "code",
            "api",
            "connector",
            "automation"
        ]):
            return "coding"

        if any(word in text for word in [
            "research",
            "find",
            "analyze"
        ]):
            return "research"

        if any(word in text for word in [
            "money",
            "revenue",
            "sales",
            "client"
        ]):
            return "revenue"

        return "general"


    def choose_tools(self, capability):

        tools = {

            "coding": [
                "code_executor",
                "file_manager",
                "api_builder"
            ],

            "research": [
                "web_research",
                "source_validator"
            ],

            "revenue": [
                "opportunity_hunter",
                "outreach_engine"
            ],

            "general": [
                "memory",
                "planner"
            ]
        }

        return tools.get(
            capability,
            tools["general"]
        )


    def execute(self, mission, agent):

        capability = self.detect_capability(
            mission
        )

        tools = self.choose_tools(
            capability
        )

        brain = llm_connector.run(
            capability,
            mission
        )

        memory = genesis_persistent_memory_core.remember(
            "executive_missions",
            {
                "mission": mission,
                "agent": agent,
                "capability": capability
            }
        )

        execution = {

            "id":
            "executive_" + uuid.uuid4().hex[:8],

            "mission":
            mission,

            "agent":
            agent,

            "capability":
            capability,

            "tools":
            tools,

            "brain":
            brain,

            "memory":
            memory,

            "status":
            "READY",

            "created":
            time.time()
        }

        self.executions.append(
            execution
        )

        print(
            "👑 Executive SDK Agent activated"
        )

        print(
            "Mission:",
            mission
        )

        print(
            "Capability:",
            capability
        )

        return execution


    def report(self):

        return {

            "system":
            self.system,

            "executions":
            len(self.executions),

            "timestamp":
            time.time()
        }


genesis_executive_sdk_agent = GenesisExecutiveSDKAgent()
