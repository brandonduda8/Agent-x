import uuid
import time


class ResourceGovernor:

    def allocate(self, decision):

        result = {
            "id":f"resource_{uuid.uuid4().hex[:8]}",
            "allocation":[
                {
                    "resource":"Sales Agents",
                    "priority":"HIGH"
                },
                {
                    "resource":"Automation Agents",
                    "priority":"HIGH"
                }
            ],
            "timestamp":time.time()
        }

        print(
            "💰 Resources allocated"
        )

        return result


resource_governor = ResourceGovernor()
