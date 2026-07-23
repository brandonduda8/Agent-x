import time
import uuid


class GenesisApplicationCampaignManager:

    def __init__(self):
        self.campaigns = []


    def create_campaign(self, opportunity, category="employment"):

        campaign = {
            "id": "campaign_" + str(uuid.uuid4())[:8],
            "category": category,
            "opportunity": opportunity,
            "status": "READY",
            "steps": [
                "profile_match",
                "resume_prepare",
                "message_prepare",
                "approval_required",
                "submit",
                "follow_up",
                "track_result"
            ],
            "created": time.time()
        }

        self.campaigns.append(campaign)
        return campaign


    def status(self):

        return {
            "system": "GENESIS APPLICATION CAMPAIGN MANAGER v1",
            "status": "ONLINE",
            "campaign_count": len(self.campaigns),
            "campaigns": self.campaigns,
            "timestamp": time.time()
        }


campaign_manager = GenesisApplicationCampaignManager()
