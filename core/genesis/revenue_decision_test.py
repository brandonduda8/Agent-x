from core.genesis.opportunity_scanner import opportunity_scanner
from core.genesis.revenue_decision_engine import revenue_decision_engine


scan = opportunity_scanner.scan(
    "Find fastest path to first revenue"
)


print(
    revenue_decision_engine.evaluate(
        scan["opportunities"]
    )
)


print(
    revenue_decision_engine.report()
)
