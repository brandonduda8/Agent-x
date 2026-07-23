import time


class GenesisSignalDetector:


    def __init__(self):

        self.system = "GENESIS SIGNAL DETECTOR v1"


        self.hot_signals = [

            "need ai",
            "looking for automation",
            "want automation",
            "scale",
            "growth",
            "reduce costs",
            "increase efficiency",
            "software",
            "automation"

        ]


        self.pain_signals = [

            "manual",
            "repetitive",
            "slow",
            "expensive",
            "wasted time",
            "data entry",
            "too many employees",
            "customer support"

        ]



    def analyze(self, text):

        text = text.lower()


        signals = []


        score = 0


        for signal in self.hot_signals:

            if signal in text:

                signals.append(signal)

                score += 15



        for signal in self.pain_signals:

            if signal in text:

                signals.append(signal)

                score += 10



        if score >= 70:

            priority = "HOT"


        elif score >= 35:

            priority = "WARM"


        else:

            priority = "COLD"



        return {


            "text":
            text,


            "score":
            score,


            "priority":
            priority,


            "signals":
            signals,


            "recommended_action":
            (
                "OUTREACH_NOW"
                if score >= 50
                else "NURTURE"
            ),


            "timestamp":
            time.time()

        }



signal_detector = GenesisSignalDetector()
