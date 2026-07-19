from core.genesis.company.os.company_brain import (
    company_brain
)

from core.genesis.company.os.financial_controller import (
    financial_controller
)

from core.genesis.company.os.operations_manager import (
    operations_manager
)

from core.genesis.company.os.company_dashboard import (
    dashboard
)


class GenesisCompanyOS:


    def run(
        self,
        company,
        market,
        objective
    ):


        print(
            "🏢 Genesis Company OS activated"
        )


        operations = operations_manager.create_plan(
            company,
            objective
        )


        finance = financial_controller.record(
            company,
            0
        )


        decision = company_brain.analyze(
            company,
            0,
            0
        )


        report = dashboard.generate(
            company,
            0,
            0,
            6
        )


        return {

            "company":
            company,

            "market":
            market,

            "operations":
            operations,

            "finance":
            finance,

            "decision":
            decision,

            "dashboard":
            report

        }



company_os = GenesisCompanyOS()
