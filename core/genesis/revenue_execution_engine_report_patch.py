import time


def attach_revenue_report(engine):

    def report():

        return {
            "system":
                "GENESIS REVENUE EXECUTION ENGINE",

            "status":
                "ONLINE",

            "executions":
                len(engine.executions),

            "active_ids":
                list(engine.executions.keys())
                if isinstance(engine.executions, dict)
                else [],

            "timestamp":
                time.time()
        }


    engine.report = report

    return engine
