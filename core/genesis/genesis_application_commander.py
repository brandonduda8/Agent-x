import time
import uuid


class GenesisApplicationCommander:

    def __init__(self):
        self.applications = []


    def submit_application(
        self,
        company,
        position,
        resume,
        source
    ):

        application = {
            "id": f"application_{uuid.uuid4().hex[:8]}",
            "company": company,
            "position": position,
            "resume": resume,
            "source": source,
            "status": "SUBMITTED",
            "follow_up": "48 hours",
            "timestamp": time.time()
        }

        self.applications.append(application)

        return application


    def update_status(
        self,
        application_id,
        status
    ):

        for app in self.applications:

            if app["id"] == application_id:

                app["status"] = status

                return {
                    "id": f"update_{uuid.uuid4().hex[:8]}",
                    "application": application_id,
                    "status": status,
                    "timestamp": time.time()
                }


        return {
            "error": "Application not found"
        }


    def create_followup_queue(self):

        return {
            "queue": [
                {
                    "company": app["company"],
                    "action": "Contact recruiter",
                    "when": app["follow_up"]
                }
                for app in self.applications
            ],
            "status": "READY",
            "timestamp": time.time()
        }


    def report(self):

        return {
            "system": "GENESIS APPLICATION COMMANDER v1",
            "applications": len(self.applications),
            "status": "ONLINE",
            "timestamp": time.time()
        }


genesis_application_commander = GenesisApplicationCommander()
