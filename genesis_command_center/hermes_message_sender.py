import os
import json
import requests

from datetime import datetime
from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN"
)

CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID"
)


def send_message(message):

    url = (
        "https://api.telegram.org/bot"
        + BOT_TOKEN
        + "/sendMessage"
    )

    payload = {

        "chat_id": CHAT_ID,

        "text": message

    }


    response = requests.post(
        url,
        json=payload
    )


    return response.json()



brief = """
🧬 GENESIS DAILY BRIEF

System:
ONLINE

Agents:
SYNCHRONIZED

Adapters:
CONNECTED

Priority:

1. Secure income
2. Build revenue pipeline
3. Improve automation

Approval Center:
READY

Operator:
Brandon Duda
"""


result = {

    "system":
    "HERMES MESSAGE SENDER",

    "timestamp":
    str(datetime.now()),

    "telegram_result":
    send_message(brief)

}


print(
    json.dumps(
        result,
        indent=4
    )
)
