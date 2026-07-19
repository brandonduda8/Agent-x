import time


class PipelineManager:

    stages = [
        "PROSPECT",
        "RESEARCHED",
        "CONTACTED",
        "REPLIED",
        "MEETING",
        "PROPOSAL",
        "CUSTOMER",
        "DELIVERED"
    ]


    def move_stage(self, opportunity, stage):

        opportunity["stage"] = stage
        opportunity["updated"] = time.time()

        print(
            f"📈 Pipeline moved: {stage}"
        )

        return opportunity


pipeline_manager = PipelineManager()
