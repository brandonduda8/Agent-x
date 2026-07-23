
from genesis_core.agent_factory.agent_factory import GenesisAgentFactory
from genesis_core.deployment.deployment_engine import GenesisDeploymentEngine


factory = GenesisAgentFactory()

deployment = GenesisDeploymentEngine()


blueprint = factory.create_blueprint(

"marketing",

"Acquire AI automation clients"

)


agent = deployment.deploy(
    blueprint
)


print(agent)


print(
deployment.status()
)

