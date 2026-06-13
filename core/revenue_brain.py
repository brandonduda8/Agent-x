class RevenueBrain:

    def __init__(self, revenue_engine):

        self.revenue = revenue_engine

    # -------------------------
    # TASK SCORE
    # -------------------------
    def score(self, task):

        base = 1

        revenue = self.revenue.total()

        revenue_boost = revenue * 0.01

        task_type = task.get("type", "unknown")

        # simple heuristic weights
        if task_type == "build":
            type_boost = 1.2
        elif task_type == "goal":
            type_boost = 0.8
        else:
            type_boost = 1.0

        score = base + revenue_boost + type_boost

        return round(score, 3)

    # -------------------------
    # RANK TASKS
    # -------------------------
    def rank(self, tasks):

        scored = []

        for t in tasks:

            scored.append((self.score(t), t))

        scored.sort(reverse=True, key=lambda x: x[0])

        return [x[1] for x in scored]
