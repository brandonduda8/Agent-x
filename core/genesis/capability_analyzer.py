import time
import uuid


class CapabilityAnalyzer:

    def __init__(self):

        self.system = "GENESIS CAPABILITY ANALYZER v1"
        self.decisions = []


    def analyze(self, text):

        value = str(text).lower()


        coding_words = [
            "code",
            "python",
            "api",
            "connector",
            "database",
            "testing",
            "debug",
            "bug",
            "architecture",
            "framework",
            "deployment",
            "sdk",
            "integration",
            "upgrade",
            "system"
        ]


        research_words = [
            "research",
            "discover",
            "market",
            "source",
            "jobs",
            "opportunities",
            "ai tools",
            "competitors",
            "trends"
        ]


        revenue_words = [
            "revenue",
            "sales",
            "client",
            "offer",
            "pricing",
            "lead",
            "customer",
            "money"
        ]


        planning_words = [
            "strategy",
            "roadmap",
            "executive",
            "ceo",
            "mission",
            "planning",
            "operations"
        ]


        score = {
            "coding": 0,
            "research": 0,
            "revenue": 0,
            "planning": 0
        }


        for word in coding_words:
            if word in value:
                score["coding"] += 1


        for word in research_words:
            if word in value:
                score["research"] += 1


        for word in revenue_words:
            if word in value:
                score["revenue"] += 1


        for word in planning_words:
            if word in value:
                score["planning"] += 1



        capability = max(
            score,
            key=score.get
        )


        if score[capability] == 0:
            capability = "general"


        decision = {

            "id":
            "capability_"
            +
            uuid.uuid4().hex[:8],

            "input":
            text,

            "scores":
            score,

            "capability":
            capability,

            "timestamp":
            time.time()

        }


        self.decisions.append(
            decision
        )


        print(
            "🧠 Capability:",
            capability
        )


        return decision



    def report(self):

        return {

            "system":
            self.system,

            "decisions":
            len(self.decisions),

            "timestamp":
            time.time()

        }



genesis_capability_analyzer = CapabilityAnalyzer()
