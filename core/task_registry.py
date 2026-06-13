import json
from pathlib import Path

class TaskRegistry:

    def __init__(self, file_path="memory/tasks.json"):

        self.file = Path(file_path)

        self.file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        if not self.file.exists():
            self.file.write_text("[]")

    def load(self):

        return json.loads(
            self.file.read_text()
        )

    def save(self, tasks):

        self.file.write_text(
            json.dumps(tasks, indent=2)
        )

    def add(self, task):

        tasks = self.load()

        tasks.append(task)

        self.save(tasks)

    def list(self):

        return self.load()
