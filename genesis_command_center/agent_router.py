from genesis_bus import dispatch

AGENTS = {
    "income": "Opportunity Discovery Agent",
    "revenue": "Revenue Agent",
    "housing": "Stability Agent",
    "development": "Development Agent"
}

def run_agent(category, mission):
    agent = AGENTS.get(category)

    if not agent:
        return {
            "status":"ERROR",
            "message":"Unknown agent"
        }

    return dispatch(
        agent,
        mission
    )


if __name__ == "__main__":

    print(run_agent(
        "income",
        "Search and prioritize income opportunities"
    ))

    print(run_agent(
        "revenue",
        "Prepare outreach pipeline"
    ))

    print(run_agent(
        "housing",
        "Update stability resources"
    ))
