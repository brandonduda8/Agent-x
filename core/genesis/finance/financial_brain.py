import uuid
import time


from core.genesis.finance.revenue_tracker import (
    revenue_tracker
)

from core.genesis.finance.expense_manager import (
    expense_manager
)

from core.genesis.finance.profit_analyzer import (
    profit_analyzer
)

from core.genesis.finance.growth_forecaster import (
    growth_forecaster
)


class FinancialBrain:

    def __init__(self):
        self.cycles = []


    def analyze(self, company):

        print("🏦 Financial Brain activated")

        revenue = revenue_tracker.record(
            company,
            5000
        )

        expenses = expense_manager.track(
            company,
            1000
        )

        profit = profit_analyzer.analyze(
            revenue["amount"],
            expenses["expenses"]
        )

        growth = growth_forecaster.forecast(
            profit["profit"]
        )


        cycle = {
            "id": f"finance_cycle_{uuid.uuid4().hex[:8]}",
            "company": company,
            "revenue": revenue,
            "expenses": expenses,
            "profit": profit,
            "growth": growth,
            "status": "COMPLETE",
            "timestamp": time.time()
        }


        self.cycles.append(cycle)


        print(
            "🚀 Financial analysis complete"
        )


        return cycle


financial_brain = FinancialBrain()
