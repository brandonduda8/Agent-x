
from genesis_core.agent_factory.agent_factory import GenesisAgentFactory


factory = GenesisAgentFactory()


agent = factory.create_blueprint(

"marketing",

"Acquire AI automation clients"

)


print(agent)


print(

factory.status()

)

