import time
import uuid


class GenesisApplicationEngine:

    def __init__(self):
        self.applications = []

    def create_application(self, opportunity, category="employment"):

        application = {
            "id": f"application_{uuid.uuid4().hex[:8]}",
            "category": category,
            "opportunity": opportunity,
            "status": "READY",
            "steps": [
                "review_match",
                "prepare_resume",
                "prepare_message",
                "submit",
                "follow_up"
            ],
            "timestamp": time.time()
        }

        self.applications.append(application)
        return application


    def submit_application(self, application_id):

        for app in self.applications:
            if app["id"] == application_id:
                app["status"] = "SUBMITTED"
                app["submitted_at"] = time.time()
                return app

        return {"status": "NOT_FOUND"}


    def status(self):

        return {
            "system": "GENESIS APPLICATION ENGINE v1",
            "status": "ONLINE",
            "applications": self.applications,
            "count": len(self.applications),
            "timestamp": time.time()
        }


application_engine = GenesisApplicationEngine()
