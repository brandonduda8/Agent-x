import time

from core.genesis.skill_registry import skill_registry
from core.genesis.agent_manager import agent_manager


class GenesisBrainPlanner:


    def __init__(self):

        self.name = "GENESIS BRAIN PLANNER v1"



    def analyze_objective(self, objective):

        objective_lower = objective.lower()


        required_skills = []


        if any(word in objective_lower for word in [
            "business",
            "money",
            "revenue",
            "saas",
            "startup"
        ]):

            required_skills.append(
                "business"
            )


        if any(word in objective_lower for word in [
            "build",
            "app",
            "software",
            "website",
            "code"
        ]):

            required_skills.append(
                "coding"
            )


        if any(word in objective_lower for word in [
            "research",
            "market",
            "competitor"
        ]):

            required_skills.append(
                "research"
            )


        if any(word in objective_lower for word in [
            "protect",
            "security",
            "safe"
        ]):

            required_skills.append(
                "security"
            )


        if "phone" in objective_lower or "android" in objective_lower:

            required_skills.append(
                "hardware_control"
            )


        agents = []


        mapping = {

            "coding":
                "builder",

            "research":
                "researcher",

            "business":
                "revenue",

            "security":
                "security_guardian"

        }


        for skill in required_skills:

            if skill in mapping:

                agents.append(
                    mapping[skill]
                )


        return {

            "planner":
                self.name,

            "objective":
                objective,

            "required_skills":
                required_skills,

            "assigned_agents":
                list(set(agents)),

            "steps":[

                "Analyze objective",

                "Gather required skills",

                "Assign agents",

                "Execute mission",

                "Evaluate results",

                "Improve system"

            ],

            "timestamp":
                time.time()

        }



brain_planner = GenesisBrainPlanner()
