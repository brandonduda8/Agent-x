import time
import uuid


class GenesisOpportunityAdapter:


    def __init__(
        self,
        name,
        category
    ):

        self.name = name
        self.category = category


    def create_opportunity(
        self,
        title,
        description,
        value,
        action
    ):

        return {

            "id":
            "opp_" + uuid.uuid4().hex[:8],

            "source":
            self.name,

            "category":
            self.category,

            "title":
            title,

            "description":
            description,

            "estimated_value":
            value,

            "next_action":
            action,

            "status":
            "NEW",

            "timestamp":
            time.time()

        }
