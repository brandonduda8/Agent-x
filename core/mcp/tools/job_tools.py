import time


def hunt_jobs(payload=None):

    from core.genesis.job_hunter_engine import (
        job_hunter_engine
    )

    payload = payload or {}

    return job_hunter_engine.hunt(
        payload.get(
            "candidate_profile",
            {
                "skills":
                [
                    "Python",
                    "AI agents",
                    "automation",
                    "APIs",
                    "sales automation"
                ]
            }
        )
    )



def create_application(payload=None):

    from core.genesis.application_agent import (
        application_agent
    )

    payload = payload or {}

    return application_agent.create_application(
        payload["job"],
        payload.get(
            "candidate_profile",
            {
                "skills":
                [
                    "AI agents",
                    "automation",
                    "Python"
                ]
            }
        )
    )



def application_report(payload=None):

    from core.genesis.application_agent import (
        application_agent
    )

    return application_agent.report()



def job_match_report(payload=None):

    from core.genesis.skill_match_engine import (
        skill_match_engine
    )

    return skill_match_engine.report()



def register_job_tools():

    from core.mcp.genesis_mcp_server import (
        genesis_mcp_server
    )


    tools = {

        "hunt_jobs":
            hunt_jobs,

        "create_application":
            create_application,

        "application_report":
            application_report,

        "job_match_report":
            job_match_report

    }


    for name, tool in tools.items():

        genesis_mcp_server.register_tool(
            name,
            tool
        )


    return {

        "status":
        "JOB MCP ONLINE",

        "tools":
        list(tools.keys()),

        "timestamp":
        time.time()

    }
