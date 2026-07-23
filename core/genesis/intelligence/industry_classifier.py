import time


class GenesisIndustryClassifier:


    def __init__(self):

        self.system = "GENESIS INDUSTRY CLASSIFIER v1"



        self.industries = {

            "real estate":
            [
                "property",
                "real estate",
                "agent",
                "broker"
            ],


            "healthcare":
            [
                "clinic",
                "medical",
                "health"
            ],


            "legal":
            [
                "law",
                "attorney",
                "legal"
            ],


            "ecommerce":
            [
                "shop",
                "store",
                " ecommerce",
                "product"
            ],


            "marketing":
            [
                "agency",
                "marketing",
                "ads"
            ]

        }



    def classify(self,text):


        text=text.lower()


        matches=[]


        for industry,words in self.industries.items():

            for word in words:

                if word in text:

                    matches.append(industry)



        return {


            "industry":
            matches[0]
            if matches
            else "unknown",


            "matches":
            matches,


            "timestamp":
            time.time()

        }



industry_classifier = GenesisIndustryClassifier()
