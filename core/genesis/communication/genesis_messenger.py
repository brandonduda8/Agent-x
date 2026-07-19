import os
import requests
import time

from dotenv import load_dotenv


load_dotenv(".env")


class GenesisMessenger:


    def __init__(self):

        self.system = "GENESIS MESSENGER v1"

        self.token = os.getenv(
            "TELEGRAM_BOT_TOKEN"
        )

        self.chat_id = os.getenv(
            "GENESIS_CHAT_ID"
        )



    def send(self, message):

        if not self.token or not self.chat_id:

            return {
                "status":
                "NO_CHAT_CONFIG"
            }


        url = (
            f"https://api.telegram.org/"
            f"bot{self.token}/sendMessage"
        )


        response = requests.post(

            url,

            json={

                "chat_id":
                self.chat_id,

                "text":
                message

            },

            timeout=10

        )


        return response.json()



    def startup_report(self):

        return self.send(

            """🧬 GENESIS ONLINE

Runtime initialized.

Supervisor:
ACTIVE

Communication:
ONLINE

Mission:
AUTONOMOUS OPERATIONS STARTED

"""

        )



    def system_report(self, data):

        return self.send(

            "🧬 GENESIS REPORT\n\n"
            + str(data)

        )



genesis_messenger = GenesisMessenger()
