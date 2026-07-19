import time

from core.genesis.mobile_agent import mobile_agent
from core.genesis.conversation_memory import conversation_memory

from core.genesis.ceo_intelligence import GenesisCEOIntelligence
from core.genesis.mission_orchestrator import GenesisMissionOrchestrator
from core.genesis.event_stream import event_stream


class GenesisCommandRouter:

    def __init__(self):

        self.system = "GENESIS COMMAND ROUTER v2"

        self.commands = []

        self.ceo = GenesisCEOIntelligence(
            event_stream=event_stream
        )

        self.orchestrator = GenesisMissionOrchestrator(
            event_stream=event_stream
        )


    def process(self, message):

        print(
            f"🧬 Processing command: {message}"
        )


        mobile_agent.receive_command(
            message
        )


        response = self.think(
            message
        )


        conversation_memory.remember(
            "USER",
            message,
            response
        )


        result = {

            "command":
                message,

            "response":
                response,

            "timestamp":
                time.time()

        }


        self.commands.append(result)


        return result



    def think(self, message):

        text = message.lower()


        # Genesis status

        if "status" in text:

            return (
                "🧬 Genesis Online\n"
                "CEO Engine: ACTIVE\n"
                "Mission System: ACTIVE\n"
                "Telegram Bridge: CONNECTED"
            )


        # Business missions

        if any(word in text for word in [
            "money",
            "revenue",
            "customer",
            "lead",
            "business"
        ]):


            decision = self.ceo.analyze_objective(
                message
            )


            mission = self.orchestrator.create_mission(
                decision
            )


            return (

                "🧬 Genesis Mission Created\n\n"

                f"Objective:\n"
                f"{mission['objective']}\n\n"

                "Agents Assigned:\n"

                + "\n".join(
                    "- " + a
                    for a in mission["agents"]
                )

            )


        # Building requests

        if "build" in text:

            decision = self.ceo.analyze_objective(
                message
            )


            mission = self.orchestrator.create_mission(
                decision
            )


            return (

                "🏗 Build Mission Created\n\n"

                f"{mission['objective']}\n\n"

                "Assigned:\n"

                + "\n".join(
                    "- " + a
                    for a in mission["agents"]
                )

            )


        return (
            "Genesis received your request.\n"
            "Planning next action."
        )



    def report(self):

        return {

            "system":
                self.system,

            "commands":
                len(self.commands),

            "timestamp":
                time.time()
        }


command_router = GenesisCommandRouter()
