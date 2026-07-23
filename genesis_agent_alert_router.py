import time

from genesis_notification_bridge import notification_bridge


class AgentAlertRouter:


    def route(self, agent, category, result):

        priority = "HIGH"

        if category == "income":
            priority = "CRITICAL"

        if category == "housing":
            priority = "CRITICAL"


        return notification_bridge.notify(
            category,
            f"{agent}: {result}",
            priority
        )


alert_router = AgentAlertRouter()
