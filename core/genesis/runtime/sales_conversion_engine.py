import time
import uuid


class GenesisSalesConversionEngine:


    def __init__(
        self,
        scorer,
        follow_up,
        pipeline
    ):

        self.scorer = scorer

        self.follow_up = follow_up

        self.pipeline = pipeline

        self.system = (
            "GENESIS SALES CONVERSION ENGINE v1"
        )


    def process(
        self,
        business,
        problems
    ):


        lead = self.scorer.score(

            business,

            problems

        )


        follow = self.follow_up.create_sequence(

            business

        )


        pipeline = self.pipeline.add(

            lead

        )


        return {

            "id":
                "sales_" +
                uuid.uuid4().hex[:8],

            "system":
                self.system,

            "lead":
                lead,

            "follow_up":
                follow,

            "pipeline":
                pipeline,

            "status":
                "ACTIVE",

            "timestamp":
                time.time()

        }
