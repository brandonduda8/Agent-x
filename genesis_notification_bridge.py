import time
import uuid


class GenesisNotificationBridge:

    def __init__(self):
        self.channels = {
            "sms": {
                "status": "READY",
                "purpose": "urgent_notifications"
            },
            "telegram": {
                "status": "READY",
                "purpose": "agent_reports_commands"
            },
            "genesis_mobile": {
                "status": "READY",
                "purpose": "dashboard_notifications"
            }
        }

        self.queue = []


    def notify(self, category, message, priority="NORMAL"):

        event = {
            "id": "notify_" + uuid.uuid4().hex[:8],
            "category": category,
            "message": message,
            "priority": priority,
            "channels": list(self.channels.keys()),
            "status": "QUEUED",
            "timestamp": time.time()
        }

        self.queue.append(event)

        print(event)

        return event


    def status(self):

        return {
            "system": "GENESIS MULTI CHANNEL NOTIFICATION BRIDGE v1",
            "status": "ONLINE",
            "channels": self.channels,
            "queue": self.queue,
            "timestamp": time.time()
        }


notification_bridge = GenesisNotificationBridge()
