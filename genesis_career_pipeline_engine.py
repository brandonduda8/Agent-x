import time
import uuid


class GenesisCareerPipeline:

    def __init__(self):
        self.records = []


    def create_record(self, opportunity):

        record = {
            "id": f"career_{uuid.uuid4().hex[:8]}",
            "opportunity": opportunity,
            "status": "APPLIED",
            "stages": [
                "APPLIED",
                "RESPONSE_RECEIVED",
                "INTERVIEW",
                "OFFER",
                "DECISION"
            ],
            "current_stage": "APPLIED",
            "notes": [],
            "timestamp": time.time()
        }

        self.records.append(record)
        return record


    def advance(self, record_id, stage, note=None):

        for record in self.records:
            if record["id"] == record_id:
                record["current_stage"] = stage

                if note:
                    record["notes"].append(note)

                return record

        return {"status": "NOT_FOUND"}


    def status(self):

        return {
            "system": "GENESIS CAREER PIPELINE ENGINE v1",
            "status": "ONLINE",
            "records": self.records,
            "timestamp": time.time()
        }


career_pipeline = GenesisCareerPipeline()
