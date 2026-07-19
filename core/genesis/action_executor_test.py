from core.genesis.opportunity_scanner import opportunity_scanner
from core.genesis.revenue_decision_engine import revenue_decision_engine
from core.genesis.action_executor import action_executor


scan = opportunity_scanner.scan(
    "Find fastest path to first revenue"
)


decision = revenue_decision_engine.evaluate(
    scan["opportunities"]
)


print(
    action_executor.execute(
        decision
    )
)


print(
    action_executor.report()
)
