import uuid
import time


class ResourceAllocator:

    def allocate(self, capital):

        allocation = [
            {
                "department": "Sales Agents",
                "investment": int(capital * 0.5)
            },
            {
                "department": "Automation",
                "investment": int(capital * 0.3)
            },
            {
                "department": "Research",
                "investment": int(capital * 0.2)
            }
        ]

        result = {
            "id": f"allocation_{uuid.uuid4().hex[:8]}",
            "allocation": allocation,
            "timestamp": time.time()
        }

        print(
            "📊 Resources allocated"
        )

        return result


resource_allocator = ResourceAllocator()
