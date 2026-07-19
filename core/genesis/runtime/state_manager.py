import os
import json
import time
import tempfile


class GenesisStateManager:

    def __init__(self):

        self.system = "GENESIS STATE MANAGER v2"

        self.file = "data/genesis_runtime_state.json"

        os.makedirs(
            "data",
            exist_ok=True
        )


        if not os.path.exists(self.file):

            self.save(
                self.default_state()
            )


    def default_state(self):

        return {

            "runtime": "OFFLINE",

            "cycles": 0,

            "last_cycle": None,

            "events": []

        }


    def load(self):

        try:

            with open(self.file, "r") as f:

                content = f.read().strip()


            if not content:

                data = self.default_state()

                self.save(data)

                return data


            return json.loads(content)


        except Exception as e:

            print(
                "⚠️ State recovery:",
                e
            )


            data = self.default_state()

            self.save(data)

            return data



    def save(self, data):

        directory = os.path.dirname(self.file)


        fd, temp_path = tempfile.mkstemp(
            dir=directory
        )


        try:

            with os.fdopen(fd, "w") as f:

                json.dump(
                    data,
                    f,
                    indent=2
                )


            os.replace(
                temp_path,
                self.file
            )


        except Exception:

            if os.path.exists(temp_path):

                os.remove(temp_path)

            raise



    def update(
        self,
        key,
        value
    ):

        data = self.load()

        data[key] = value

        self.save(data)

        return data



    def record_event(
        self,
        event
    ):

        data = self.load()


        data["events"].append(

            {
                "event": event,
                "timestamp": time.time()
            }

        )


        self.save(data)



state_manager = GenesisStateManager()
