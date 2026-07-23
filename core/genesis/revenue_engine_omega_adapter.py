from core.genesis.revenue_execution_engine import (
    revenue_execution_engine
)

from core.genesis.revenue_execution_engine_report_patch import (
    attach_revenue_report
)


revenue_engine_omega_adapter = (
    attach_revenue_report(
        revenue_execution_engine
    )
)
