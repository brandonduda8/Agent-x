from genesis_core.governance.meta_council import GenesisMetaGovernanceCouncil


council = GenesisMetaGovernanceCouncil()


council.register_agent(
    "Genesis CEO Agent",
    "strategy",
    [
        "planning",
        "reasoning",
        "priority"
    ]
)


council.register_agent(
    "STEM Meta Agents",
    "science",
    [
        "research",
        "engineering",
        "analysis"
    ]
)


council.register_agent(
    "Agent-X Coding Agent",
    "engineering",
    [
        "coding",
        "deployment",
        "debugging"
    ]
)


council.register_agent(
    "Hermes Research Agent",
    "intelligence",
    [
        "research",
        "analysis",
        "tools"
    ]
)


mission = {

    "objective":
    "Improve Genesis system capability",

    "required_skill":
    "engineering"

}


print(
    council.assign(mission)
)


print(
    council.council_status()
)
