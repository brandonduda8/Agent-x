import time
import os
import threading
import requests

from dotenv import load_dotenv

from core.genesis.telegram.telegram_command_center import (
    telegram_command_center
)

from core.genesis.runtime.genesis_runtime import (
    genesis_runtime
)


load_dotenv(".env")


class GenesisTelegramDaemon:


    def __init__(self):

        self.system = "GENESIS TELEGRAM DAEMON v2"

        self.token = os.getenv(
            "TELEGRAM_BOT_TOKEN"
        )

        self.offset = 0

        self.running = False

        self.messages = 0

        self.thread = None



    def send(
        self,
        chat_id,
        message
    ):

        if not self.token:

            return {
                "status":
                "NO_TOKEN"
            }


        url = (
            f"https://api.telegram.org/"
            f"bot{self.token}/sendMessage"
        )


        response = requests.post(

            url,

            json={

                "chat_id":
                chat_id,

                "text":
                message

            },

            timeout=10

        )


        return response.json()



    def start(self):

        if self.running:

            return {
                "status":
                "ALREADY_RUNNING"
            }


        genesis_runtime.start()


        self.running = True


        self.thread = threading.Thread(

            target=self.listen_loop,

            daemon=True

        )


        self.thread.start()


        print(
            "📲 Genesis Telegram Daemon Online"
        )


        return {

            "system":
            self.system,

            "status":
            "ONLINE"

        }



    def listen_loop(self):

        print(
            "👂 Genesis Telegram Listener Active"
        )


        while self.running:


            try:

                self.listen_once()


            except Exception as e:

                print(
                    "Telegram listener error:",
                    e
                )


            time.sleep(2)



    def listen_once(self):

        if not self.token:

            return



        url = (

            f"https://api.telegram.org/"
            f"bot{self.token}/getUpdates"

        )


        response = requests.get(

            url,

            params={

                "offset":
                self.offset

            },

            timeout=10

        )


        data = response.json()


        if not data.get("ok"):

            return data



        for update in data["result"]:


            self.offset = (

                update["update_id"]
                + 1

            )


            if "message" not in update:

                continue



            message = update["message"]


            chat_id = message["chat"]["id"]


            text = message.get(
                "text",
                ""
            )


            print(
                "📲 Telegram command:",
                text
            )


            result = telegram_command_center.process(
                text
            )


            self.send(

                chat_id,

                result

            )


            self.messages += 1



        return {

            "status":
            "LISTENING",

            "messages":
            self.messages

        }



telegram_daemon = GenesisTelegramDaemon()
