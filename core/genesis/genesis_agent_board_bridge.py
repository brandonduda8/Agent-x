import time


class GenesisAgentBoardBridge:

    def __init__(self):

        self.system = "GENESIS AGENT BOARD BRIDGE v1"

        self.routes = {
            "Opportunity Discovery Agent": "income",
            "Revenue Agent": "revenue",
            "Stability Agent": "housing",
            "Mission Execution Agent": "execution",
            "Outreach Agent": "execution"
        }

        self.entries = {
            "income": [],
            "revenue": [],
            "housing": [],
            "execution": []
        }


    def add(self, agent, item):

        board = self.routes.get(agent)

        if not board:
            return {
                "status": "UNKNOWN_AGENT",
                "agent": agent
            }

        self.entries[board].append({
            "agent": agent,
            "item": item,
            "timestamp": time.time()
        })

        return {
            "status": "RECORDED",
            "board": board,
            "agent": agent,
            "item": item
        }


    def status(self):

        return {
            "system": self.system,
            "status": "ONLINE",
            "boards": self.entries,
            "timestamp": time.time()
        }


agent_board_bridge = GenesisAgentBoardBridge()
