import os
import time
import requests

from dotenv import load_dotenv

from core.genesis.command_router import command_router


load_dotenv()


class GenesisTelegramAgent:

    def __init__(self):

        self.system = "GENESIS TELEGRAM AGENT v1"

        self.token = os.getenv(
            "TELEGRAM_BOT_TOKEN"
        )

        self.offset = 0

        self.messages = 0


    def send(self, chat_id, message):

        url = (
            f"https://api.telegram.org/"
            f"bot{self.token}/sendMessage"
        )

        response = requests.post(
            url,
            json={
                "chat_id": chat_id,
                "text": message
            }
        )

        return response.json()



    def listen_once(self):

        url = (
            f"https://api.telegram.org/"
            f"bot{self.token}/getUpdates"
        )


        response = requests.get(
            url,
            params={
                "offset": self.offset
            }
        )


        data = response.json()


        if not data.get("ok"):

            return data


        for update in data["result"]:

            self.offset = update["update_id"] + 1


            if "message" in update:

                message = update["message"]

                chat_id = message["chat"]["id"]

                text = message.get(
                    "text",
                    ""
                )


                self.messages += 1


                result = command_router.process(
                    text
                )


                self.send(
                    chat_id,
                    result["response"]
                )


                print(
                    "📲 Telegram command handled:",
                    text
                )


        return {
            "status": "LISTENING",
            "messages": self.messages,
            "timestamp": time.time()
        }



    def report(self):

        return {

            "system": self.system,

            "messages": self.messages,

            "timestamp": time.time()

        }



telegram_agent = GenesisTelegramAgent()
