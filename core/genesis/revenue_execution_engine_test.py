from core.genesis.revenue_execution_engine import GenesisRevenueExecutionEngine

from core.genesis.lead_generation_engine import lead_generation_engine
from core.genesis.crm_agent import crm_agent
from core.genesis.business_automation_engine import business_automation_engine


engine = GenesisRevenueExecutionEngine(

    lead_engine=lead_generation_engine,

    crm=crm_agent,

    business_engine=business_automation_engine

)


mission = engine.create_revenue_mission(
    "Find first AI automation customer"
)


print(mission)


result = engine.execute_test_pipeline()


print(result)


print(
    engine.status()
)
