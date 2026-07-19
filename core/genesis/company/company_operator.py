import time
import uuid

from core.genesis.company.operations_manager import (
    operations_manager
)

from core.genesis.company.customer_engine import (
    customer_engine
)

from core.genesis.company.finance_engine import (
    finance_engine
)

from core.genesis.company.performance_dashboard import (
    performance_dashboard
)


class GenesisCompanyOperator:

    def __init__(self):

        self.system = "GENESIS COMPANY OPERATOR v1"
        self.companies = []


    def create_company(
        self,
        name,
        market,
        objective
    ):

        print(
            "🏢 Creating autonomous company:",
            name
        )


        operations = (
            operations_manager.create_plan(
                objective
            )
        )


        pipeline = (
            customer_engine.create_pipeline(
                market
            )
        )


        customer_engine.add_prospects(
            pipeline,
            25
        )


        finance = (
            finance_engine.record_revenue(
                name,
                0
            )
        )


        dashboard = (
            performance_dashboard.analyze(
                name,
                0,
                25
            )
        )


        company = {

            "id":
            "company_" + uuid.uuid4().hex[:8],

            "name":
            name,

            "market":
            market,

            "operations":
            operations,

            "pipeline":
            pipeline,

            "finance":
            finance,

            "dashboard":
            dashboard,

            "status":
            "ACTIVE",

            "timestamp":
            time.time()

        }


        self.companies.append(company)

        print(
            "🚀 Autonomous company active"
        )

        return company



    def report(self):

        return {

            "system":
            self.system,

            "companies":
            len(self.companies),

            "timestamp":
            time.time()

        }



company_operator = GenesisCompanyOperator()
