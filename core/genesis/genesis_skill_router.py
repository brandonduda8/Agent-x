import time


class GenesisSkillRouter:

    def __init__(self):

        self.system = "GENESIS UNIVERSAL SKILL ROUTER v3"

        self.skills = {

            "debugging": {
                "agent": "OpenHands",
                "priority": 1,
                "keywords": [
                    "debug",
                    "bug",
                    "error",
                    "exception",
                    "fix",
                    "broken"
                ]
            },

            "coding": {
                "agent": "Computer Science Meta Agent",
                "priority": 2,
                "keywords": [
                    "coding",
                    "code",
                    "programming",
                    "python",
                    "javascript",
                    "software"
                ]
            },

            "revenue": {
                "agent": "Revenue Agent",
                "priority": 1,
                "keywords": [
                    "money",
                    "revenue",
                    "sales",
                    "business",
                    "clients"
                ]
            },

            "jobs": {
                "agent": "Opportunity Discovery Agent",
                "priority": 1,
                "keywords": [
                    "job",
                    "employment",
                    "work",
                    "career"
                ]
            },

            "housing": {
                "agent": "Stability Agent",
                "priority": 1,
                "keywords": [
                    "housing",
                    "rent",
                    "shelter",
                    "stability"
                ]
            },

            "strategy": {
                "agent": "Zane Hart Agent",
                "priority": 5,
                "keywords": [
                    "strategy",
                    "plan",
                    "roadmap"
                ]
            },

            "reasoning": {
                "agent": "Hermes Agent Connector v1",
                "priority": 3,
                "keywords": [
                    "reason",
                    "evaluate",
                    "analyze"
                ]
            },

            "execution": {
                "agent": "Agent-X",
                "priority": 2,
                "keywords": [
                    "execute",
                    "run",
                    "automation"
                ]
            }
        }


    def route(self, task):

        task_lower = task.lower()

        matches = []

        for skill, data in self.skills.items():

            for keyword in data["keywords"]:

                if keyword in task_lower:

                    matches.append(
                        (
                            data["priority"],
                            skill,
                            data["agent"]
                        )
                    )


        if matches:

            matches.sort(key=lambda x: x[0])

            priority, skill, agent = matches[0]

            return {
                "task": task,
                "assigned_agent": agent,
                "skill": skill,
                "status": "ROUTED",
                "priority": priority
            }


        return {
            "task": task,
            "assigned_agent": "Zane Hart Agent",
            "skill": "strategy",
            "status": "DEFAULT_ROUTING"
        }


    def status(self):

        return {
            "system": self.system,
            "status": "ONLINE",
            "timestamp": time.time()
        }


skill_router = GenesisSkillRouter()
