import os
import sys
import json

ROOT = os.path.abspath(
    os.path.dirname(__file__)
)

if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


from core.genesis.genesis_control_center import genesis_control_center
from core.genesis.genesis_kernel import genesis_kernel
from core.genesis.agent_manager import agent_manager
from core.genesis.agent_x_bridge import agent_x_bridge
from core.genesis.runtime.agent_harness import genesis_agent_harness

from genesis_core.fusion.revenue_fusion_adapter import (
    genesis_revenue_fusion_adapter
)

from genesis_core.opportunities.autonomous_opportunity_hunter import (
    genesis_opportunity_hunter
)

from genesis_core.fusion.genesis_omega_mission_bridge import (
    genesis_omega_mission_bridge
)

from genesis_core.fusion.genesis_ceo_mission_commander import (
    genesis_ceo_mission_commander
)

from genesis_core.fusion.genesis_execution_fusion_bridge import (
    genesis_execution_fusion_bridge
)

from core.genesis.revenue_operator_bridge import (
    genesis_revenue_operator_bridge
)


genesis_control_center.connect(
    "Kernel",
    genesis_kernel
)

genesis_control_center.connect(
    "Agent Manager",
    agent_manager
)

genesis_control_center.connect(
    "Agent-X",
    agent_x_bridge
)

genesis_control_center.connect(
    "Agent Harness",
    genesis_agent_harness
)

genesis_control_center.connect(
    "Revenue System",
    genesis_revenue_fusion_adapter
)

genesis_control_center.connect(
    "Opportunity Hunter",
    genesis_opportunity_hunter
)


genesis_omega_mission_bridge.revenue = (
    genesis_revenue_fusion_adapter
)


genesis_control_center.connect(
    "Omega Mission Bridge",
    genesis_omega_mission_bridge
)


omega_cycle = (
    genesis_omega_mission_bridge.dispatch()
)


genesis_ceo_mission_commander.mission_bridge = (
    genesis_omega_mission_bridge
)


ceo_cycle = (
    genesis_ceo_mission_commander.command_cycle()
)


genesis_control_center.connect(
    "CEO Mission Commander",
    genesis_ceo_mission_commander
)


genesis_execution_fusion_bridge.commander = (
    genesis_ceo_mission_commander
)


execution_cycle = (
    genesis_execution_fusion_bridge.execute_cycle()
)


genesis_control_center.connect(
    "Execution System",
    genesis_execution_fusion_bridge
)


# ==========================================
# GENESIS REVENUE OPERATOR ACTIVATION
# ==========================================

revenue_operator_cycle = (
    genesis_revenue_operator_bridge.activate(
        execution_cycle.get(
            "tasks",
            []
        )
    )
)


genesis_control_center.connect(
    "Revenue Operator",
    genesis_revenue_operator_bridge
)


dashboard = (
    genesis_control_center.collect()
)


dashboard["omega_cycle"] = omega_cycle

dashboard["ceo_cycle"] = ceo_cycle

dashboard["execution_cycle"] = execution_cycle

dashboard["revenue_operator_cycle"] = (
    revenue_operator_cycle
)


print(
    json.dumps(
        dashboard,
        indent=4,
        default=str
    )
)
