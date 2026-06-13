import json
from pathlib import Path

class StateManager:

    def __init__(self, file_path="memory/state.json"):

        self.file = Path(file_path)

        self.file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.file.exists():
            self.file.write_text("{}")

    def get_state(self):

        return json.loads(
            self.file.read_text()
        )

    def save_state(self, state):

        self.file.write_text(
            json.dumps(state, indent=2)
        )

    def update(self, key, value):

        state = self.get_state()

        state[key] = value

        self.save_state(state)
