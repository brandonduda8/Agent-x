import time
import uuid


class GenesisSkillAdapter:

    def __init__(self):
        self.system = "GENESIS SKILL ADAPTER v2"
        self.upgrades = []


    def detect_gap(self, required, available):

        missing = []

        for skill in required:
            if skill not in available:
                missing.append(skill)

        return {
            "missing_skills": missing,
            "timestamp": time.time()
        }


    def add_skill_upgrade(self, agent, skill, reason):

        upgrade = {
            "id": "upgrade_" + uuid.uuid4().hex[:8],
            "agent": agent,
            "skill": skill,
            "reason": reason,
            "created": time.time()
        }

        self.upgrades.append(upgrade)

        print(
            f"🔧 Skill upgrade created: {agent} -> {skill}"
        )

        return upgrade


    def report(self):

        return {
            "system": self.system,
            "upgrades": len(self.upgrades),
            "timestamp": time.time()
        }


skill_adapter = GenesisSkillAdapter()
