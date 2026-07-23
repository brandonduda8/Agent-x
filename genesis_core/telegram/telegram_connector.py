import os
import asyncio

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

from genesis_core.telegram.command_router import GenesisCommandRouter


class GenesisTelegramConnector:


    def __init__(
        self,
        state
    ):

        self.router = GenesisCommandRouter(
            state
        )

        self.token = os.getenv(
            "TELEGRAM_BOT_TOKEN"
        )


    async def handle_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ):

        command = update.message.text

        response = self.router.route(
            command
        )


        await update.message.reply_text(
            str(response)
        )



    def start(self):

        if not self.token:

            raise Exception(
                "Missing TELEGRAM_BOT_TOKEN"
            )


        app = Application.builder().token(
            self.token
        ).build()


        commands = [

            "status",
            "opportunities",
            "missions",
            "today",
            "help"

        ]


        for command in commands:

            app.add_handler(

                CommandHandler(

                    command,

                    self.handle_command

                )

            )


        print(
            "GENESIS TELEGRAM CONNECTOR ONLINE"
        )


        app.run_polling()
