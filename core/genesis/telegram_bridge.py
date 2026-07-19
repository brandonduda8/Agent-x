import os
import time
import requests

from dotenv import load_dotenv

load_dotenv()


class GenesisTelegramBridge:

    def __init__(self):

        self.name = "GENESIS TELEGRAM BRIDGE v1"

        self.token = os.getenv(
            "TELEGRAM_BOT_TOKEN"
        )

        self.chat_id = os.getenv(
            "TELEGRAM_CHAT_ID"
        )

        self.messages = []



    def connected(self):

        return bool(
            self.token
            and self.chat_id
        )



    def send(self, message):

        if not self.connected():

            return {
                "status": "NOT_CONNECTED",
                "message": "Missing Telegram credentials"
            }


        url = (
            f"https://api.telegram.org/"
            f"bot{self.token}/sendMessage"
        )


        payload = {

            "chat_id":
                self.chat_id,

            "text":
                message

        }


        response = requests.post(
            url,
            json=payload,
            timeout=10
        )


        result = {

            "status":
                "SENT",

            "response":
                response.json(),

            "timestamp":
                time.time()

        }


        self.messages.append(
            result
        )


        return result



    def report(self):

        return {

            "system":
                self.name,

            "connected":
                self.connected(),

            "messages":
                len(self.messages),

            "timestamp":
                time.time()

        }



telegram_bridge = GenesisTelegramBridge()
