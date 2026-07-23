import time


class GenesisCRMLeadScoring:


    def __init__(self):

        self.system = "GENESIS CRM LEAD SCORING v1"



    def score(self, lead):

        score = 0
        matched = []


        text = (
            str(lead)
            .lower()
        )


        keywords = {

            "automation":20,
            "ai":20,
            "business":15,
            "company":10,
            "software":15,
            "agency":15,
            "enterprise":20,
            "budget":15

        }


        for key,value in keywords.items():

            if key in text:

                score += value

                matched.append(key)



        if score >= 70:

            priority = "HOT"

        elif score >= 40:

            priority = "WARM"

        else:

            priority = "COLD"



        return {

            "lead": lead,

            "score": score,

            "priority": priority,

            "matched_signals": matched,

            "recommended_action":
                "OUTREACH_NOW"
                if priority == "HOT"
                else "NURTURE",

            "timestamp": time.time()

        }



crm_lead_scoring = GenesisCRMLeadScoring()
