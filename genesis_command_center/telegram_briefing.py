import json
from datetime import datetime


def load_briefing():

    with open("executive_briefing.py") as f:
        pass


def format_briefing(data):

    message = f"""
🧬 GENESIS DAILY COMMAND BRIEF

Time:
{data['timestamp']}

SYSTEM STATUS
--------------
Core: {data['system_status']['core']}
Status: {data['system_status']['status']}

ACTIVE AGENTS
--------------
"""

    for agent in data["system_status"]["agents"]:
        message += f"🟢 {agent}\n"


    message += """

MISSION PRIORITIES
------------------

💰 INCOME
"""

    message += (
        data["missions"]["income"]["next_action"]
        + "\n\n"
    )

    message += """
🚀 REVENUE
"""

    message += (
        data["missions"]["revenue"]["next_action"]
        + "\n\n"
    )

    message += """
⚙️ TECHNOLOGY
"""

    message += (
        data["missions"]["technology"]["next_action"]
        + "\n\n"
    )


    message += """
APPROVAL CENTER
---------------
"""

    message += data["approval_center"]["instruction"]


    message += """

NEXT OPERATOR MOVES
-------------------
"""

    for move in data["operator_next_moves"]:
        message += f"➡️ {move}\n"


    return message



if __name__ == "__main__":

    from executive_briefing import generate_briefing

    briefing = generate_briefing()

    output = format_briefing(briefing)

    print(output)
