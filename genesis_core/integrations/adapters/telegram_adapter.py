import os


class TelegramAdapter:


    def check(self):

        token = os.getenv(
            "TELEGRAM_BOT_TOKEN"
        )


        if token:

            return {

                "name":
                "Telegram",

                "status":
                "CONFIGURED"

            }


        return {

            "name":
            "Telegram",

            "status":
            "MISSING_TOKEN"

        }
