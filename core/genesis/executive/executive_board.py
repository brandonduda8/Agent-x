import time
import uuid

from core.genesis.executive.ceo_agent import ceo_agent
from core.genesis.executive.cfo_agent import cfo_agent
from core.genesis.executive.cto_agent import cto_agent
from core.genesis.executive.coo_agent import coo_agent
from core.genesis.executive.cro_agent import cro_agent


class ExecutiveBoard:

    def __init__(self):

        self.system = "GENESIS EXECUTIVE BOARD v1"
        self.cycles = []


    def evaluate(self, opportunity):

        print(
            "👑 Genesis Executive Board activated"
        )

        board = {
            "id": "board_" + uuid.uuid4().hex[:8],

            "ceo":
                ceo_agent.decide(opportunity),

            "cfo":
                cfo_agent.analyze(opportunity),

            "cto":
                cto_agent.plan(opportunity),

            "coo":
                coo_agent.design(opportunity),

            "cro":
                cro_agent.growth(opportunity),

            "status": "APPROVED",

            "timestamp": time.time()
        }


        self.cycles.append(board)

        print(
            "🚀 Executive decision complete"
        )

        return board


executive_board = ExecutiveBoard()
