import time


class GenesisRevenuePipeline:


    def __init__(self):

        self.pipeline = []


    def add(
        self,
        opportunity
    ):

        record = {

            "opportunity":
                opportunity,

            "stage":
                "DISCOVERED",

            "timestamp":
                time.time()

        }


        self.pipeline.append(record)


        return record


    def update(
        self,
        opportunity,
        stage
    ):


        for item in self.pipeline:

            if item["opportunity"] == opportunity:

                item["stage"] = stage


        return self.pipeline
