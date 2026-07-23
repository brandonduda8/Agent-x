from core.genesis.omega.worker_fabric import (
    genesis_omega_worker_fabric
)

from core.genesis.omega.opportunity_worker_adapter import (
    GenesisOpportunityWorkerAdapter
)

from core.genesis.omega.execution_worker_adapter import (
    GenesisExecutionWorkerAdapter
)


def connect_genesis_workers():

    try:
        from core.genesis.genesis_revenue_operator import (
            genesis_revenue_operator
        )

        genesis_omega_worker_fabric.connect(
            "revenue",
            genesis_revenue_operator
        )

        print(
            "🔗 Omega Worker Adapted: revenue"
        )

    except Exception as e:
        print(
            "Revenue worker unavailable:",
            e
        )


    try:

        opportunity_worker = (
            GenesisOpportunityWorkerAdapter()
        )

        genesis_omega_worker_fabric.connect(
            "opportunity_discovery",
            opportunity_worker
        )

        print(
            "🔗 Omega Worker Adapted: opportunity_discovery"
        )


    except Exception as e:

        print(
            "Opportunity worker unavailable:",
            e
        )


    try:

        execution_worker = (
            GenesisExecutionWorkerAdapter()
        )

        genesis_omega_worker_fabric.connect(
            "mission_execution",
            execution_worker
        )

        print(
            "🔗 Omega Worker Adapted: mission_execution"
        )


    except Exception as e:

        print(
            "Execution worker unavailable:",
            e
        )


    try:

        from core.genesis.reality_action_engine import (
            genesis_reality_action_engine
        )

        genesis_omega_worker_fabric.connect(
            "real_world_execution",
            genesis_reality_action_engine
        )

        print(
            "🔗 Omega Worker Adapted: real_world_execution"
        )

    except Exception as e:

        print(
            "Reality worker unavailable:",
            e
        )


    try:
        from core.genesis.omega.workers.outreach_operator import (
            genesis_outreach_operator
        )

        genesis_omega_worker_fabric.connect(
            "outreach",
            genesis_outreach_operator
        )

        print(
            "🔗 Omega Worker Adapted: outreach"
        )

    except Exception as e:
        print(
            "Outreach worker unavailable:",
            e
        )


    return (
        genesis_omega_worker_fabric.report()
    )
