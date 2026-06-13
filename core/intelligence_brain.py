import json
from pathlib import Path


class IntelligenceBrain:

    def __init__(self, memory_file="memory/brain.json"):

        self.file = Path(memory_file)
        self.file.parent.mkdir(parents=True, exist_ok=True)

        if not self.file.exists():
            self.file.write_text(json.dumps({
                "success_patterns": {},
                "failure_patterns": {},
                "revenue_weights": {}
            }))

    # -------------------------
    # LOAD MEMORY
    # -------------------------
    def load(self):

        return json.loads(self.file.read_text())

    # -------------------------
    # SAVE MEMORY
    # -------------------------
    def save(self, data):

        self.file.write_text(json.dumps(data, indent=2))

    # -------------------------
    # TASK SCORING ENGINE
    # -------------------------
    def score_task(self, task, revenue_total=0):

        data = self.load()

        base = 1

        task_type = task.get("type", "unknown")

        # Revenue weighting
        revenue_boost = revenue_total * 0.01 if revenue_total > 0 else 0

        # Learned success boost
        success_boost = data["success_patterns"].get(task_type, 0)

        # Failure penalty
        failure_penalty = data["failure_patterns"].get(task_type, 0)

        score = base + revenue_boost + success_boost - failure_penalty

        return round(score, 3)

    # -------------------------
    # LEARN SUCCESS
    # -------------------------
    def record_success(self, task_type):

        data = self.load()

        data["success_patterns"][task_type] = \
            data["success_patterns"].get(task_type, 0) + 0.1

        self.save(data)

    # -------------------------
    # LEARN FAILURE
    # -------------------------
    def record_failure(self, task_type):

        data = self.load()

        data["failure_patterns"][task_type] = \
            data["failure_patterns"].get(task_type, 0) + 0.1

        self.save(data)

    # -------------------------
    # PRIORITIZE TASKS
    # -------------------------
    def rank_tasks(self, tasks, revenue_total=0):

        scored = []

        for task in tasks:

            score = self.score_task(task, revenue_total)

            scored.append((score, task))

        scored.sort(reverse=True, key=lambda x: x[0])

        return [t[1] for t in scored]
