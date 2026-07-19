import json
import os


class TelegramMemory:

    def __init__(self):

        self.file = "workspace/telegram_offset.json"

        self.offset = 0

        self.load()


    def load(self):

        if os.path.exists(self.file):

            with open(self.file) as f:

                data = json.load(f)

                self.offset = data.get(
                    "offset",
                    0
                )


    def save(self):

        os.makedirs(
            "workspace",
            exist_ok=True
        )

        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                {
                    "offset": self.offset
                },
                f,
                indent=2
            )


    def update(self, offset):

        self.offset = offset

        self.save()


telegram_memory = TelegramMemory()
