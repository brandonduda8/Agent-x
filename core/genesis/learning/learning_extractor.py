import time
import uuid


class GenesisLearningExtractor:

    def __init__(self):

        self.system = "GENESIS LEARNING EXTRACTOR v1"

        self.lessons = []


    def extract(
        self,
        mission,
        performance,
        result
    ):

        lesson = {

            "id":
                "lesson_" + uuid.uuid4().hex[:8],

            "mission":
                mission,

            "performance":
                performance,

            "result":
                result,

            "knowledge":
                self.generate_knowledge(
                    mission,
                    performance
                ),

            "created":
                time.time()
        }


        self.lessons.append(lesson)


        print(
            "🧠 Learning extracted"
        )


        return lesson



    def generate_knowledge(
        self,
        mission,
        performance
    ):

        if performance >= 0.8:

            return {

                "type":
                    "SUCCESS_PATTERN",

                "lesson":
                    "Current strategy should be scaled",

                "transferable":
                    True
            }


        return {

            "type":
                "IMPROVEMENT_PATTERN",

            "lesson":
                "Strategy requires optimization",

            "transferable":
                True
        }



    def report(self):

        return {

            "system":
                self.system,

            "lessons":
                len(self.lessons),

            "timestamp":
                time.time()
        }



learning_extractor = GenesisLearningExtractor()
