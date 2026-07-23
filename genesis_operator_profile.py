import time

from genesis_contact_vault import contact_vault


class GenesisOperatorProfile:

    def __init__(self):

        self.profile = {
            "goals": [
                "secure_income",
                "build_revenue",
                "housing_stability",
                "long_term_growth"
            ],
            "skills": [],
            "job_targets": [],
            "preferred_work": [],
            "availability": None
        }


    def update(self, category, value):

        self.profile[category] = value

        return {
            "status": "UPDATED",
            "category": category,
            "timestamp": time.time()
        }


    def combined_status(self):

        return {
            "system": "GENESIS OPERATOR PROFILE ENGINE v1",
            "status": "ONLINE",
            "contact_vault": contact_vault.status(),
            "profile": self.profile,
            "timestamp": time.time()
        }


operator_profile = GenesisOperatorProfile()
