import os
import json
from datetime import datetime

from dotenv import load_dotenv


load_dotenv()


BOT_TOKEN = os.getenv(
    "TELEGRAM_BOT_TOKEN"
)

CHAT_ID = os.getenv(
    "TELEGRAM_CHAT_ID"
)


status = {

    "system":
    "HERMES TELEGRAM CONNECTOR",

    "timestamp":
    str(datetime.now()),

    "telegram": {

        "token_loaded":
        bool(BOT_TOKEN),

        "chat_id_loaded":
        bool(CHAT_ID)

    },

    "capabilities": [

        "Send daily briefings",

        "Send approval requests",

        "Send system alerts",

        "Receive operator commands"

    ],

    "status":
    "READY_FOR_API_CONNECTION"

}


print(
    json.dumps(
        status,
        indent=4
    )
)
