import uuid
import time


from core.genesis.business_creator.opportunity_scanner import (
    opportunity_scanner
)

from core.genesis.business_creator.business_designer import (
    business_designer
)

from core.genesis.business_creator.company_builder import (
    company_builder
)

from core.genesis.business_creator.workforce_launcher import (
    workforce_launcher
)

from core.genesis.business_creator.venture_validator import (
    venture_validator
)


class CreatorBrain:

    def __init__(self):
        self.cycles=[]


    def create(self):

        print(
            "🧬 Creator Brain activated"
        )

        opportunity = opportunity_scanner.scan()

        business = business_designer.design(
            opportunity
        )

        company = company_builder.build(
            business
        )

        workforce = workforce_launcher.deploy()

        validation = venture_validator.validate(
            company
        )


        cycle={
            "id":
            f"creator_{uuid.uuid4().hex[:8]}",
            "opportunity":opportunity,
            "business":business,
            "company":company,
            "workforce":workforce,
            "validation":validation,
            "status":"LAUNCHED",
            "timestamp":time.time()
        }


        self.cycles.append(cycle)


        print(
            "🚀 Autonomous business launched"
        )


        return cycle


creator_brain = CreatorBrain()
