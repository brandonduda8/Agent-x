import time
import uuid


class GenesisOutreachExecutionEngine:


    def __init__(
        self,
        personalizer,
        generator,
        pipeline
    ):

        self.personalizer = personalizer

        self.generator = generator

        self.pipeline = pipeline

        self.system = (
            "GENESIS OUTREACH EXECUTION ENGINE v1"
        )


    def execute(
        self,
        business,
        opportunity,
        offer
    ):


        analysis = self.personalizer.analyze(

            business,

            opportunity

        )


        outreach = self.generator.create(

            analysis,

            offer

        )


        lead = self.pipeline.add(
            outreach
        )


        return {

            "id":
                "outreach_" +
                uuid.uuid4().hex[:8],

            "system":
                self.system,

            "analysis":
                analysis,

            "outreach":
                outreach,

            "pipeline":
                lead,

            "status":
                "READY_FOR_CONTACT",

            "timestamp":
                time.time()

        }
