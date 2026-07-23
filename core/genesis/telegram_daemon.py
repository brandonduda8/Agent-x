import os
import time
import requests

from dotenv import load_dotenv

from core.genesis.telegram_command_center import (
    telegram_command_center
)


load_dotenv(".env")


class GenesisTelegramDaemon:

    def __init__(self):
        self.system = "GENESIS TELEGRAM DAEMON v1"
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.offset = 0
        self.running = False
        self.messages = 0

    def send(self, chat_id, text):

        url = (
            f"https://api.telegram.org/"
            f"bot{self.token}/sendMessage"
        )

        requests.post(
            url,
            json={
                "chat_id": chat_id,
                "text": text
            },
            timeout=10
        )

    def poll_once(self):

        url = (
            f"https://api.telegram.org/"
            f"bot{self.token}/getUpdates"
        )

        response = requests.get(
            url,
            params={
                "offset": self.offset,
                "timeout": 20
            },
            timeout=30
        )

        data = response.json()

        if not data.get("ok"):
            return data

        for update in data.get("result", []):

            self.offset = update["update_id"] + 1

            if "message" not in update:
                continue

            message = update["message"]

            chat_id = message["chat"]["id"]

            text = message.get(
                "text",
                ""
            )

            self.messages += 1

            reply = telegram_command_center.process(
                text
            )

            self.send(
                chat_id,
                reply
            )

            print(
                "📲 Telegram:",
                text
            )

        return {
            "status": "POLLING",
            "messages": self.messages,
            "timestamp": time.time()
        }


    def start(self):

        if not self.token:
            return {
                "status": "ERROR",
                "message": "Missing TELEGRAM_BOT_TOKEN"
            }

        self.running = True

        print("=" * 60)
        print("🧬 GENESIS TELEGRAM DAEMON ONLINE")
        print("=" * 60)

        while self.running:
            try:
                self.poll_once()

            except Exception as e:
                print(
                    "Telegram error:",
                    e
                )

            time.sleep(2)


    def report(self):

        return {
            "system": self.system,
            "running": self.running,
            "messages": self.messages,
            "timestamp": time.time()
        }


telegram_daemon = GenesisTelegramDaemon()


if __name__ == "__main__":
    telegram_daemon.start()
