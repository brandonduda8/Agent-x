import uuid
import time


class ProfitAnalyzer:

    def analyze(self, revenue, expenses):

        profit = revenue - expenses

        margin = 0

        if revenue:
            margin = round((profit / revenue) * 100, 2)

        result = {
            "id": f"profit_{uuid.uuid4().hex[:8]}",
            "revenue": revenue,
            "expenses": expenses,
            "profit": profit,
            "margin": margin,
            "timestamp": time.time()
        }

        print(
            f"📊 Profit analyzed: ${profit}"
        )

        return result


profit_analyzer = ProfitAnalyzer()
