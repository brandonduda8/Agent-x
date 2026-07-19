import uuid
import time


class AppointmentAgent:

    def schedule(self, campaign):

        appointment = {
            "id": f"meeting_{uuid.uuid4().hex[:8]}",
            "campaign": campaign["id"],
            "meetings_target": campaign["targets"],
            "status": "ACTIVE",
            "timestamp": time.time()
        }

        print("📅 Appointment Agent activated")

        return appointment


appointment_agent = AppointmentAgent()
