import time
import uuid


class GenesisDevelopmentPipeline:

    def __init__(self):

        self.system = "GENESIS DEVELOPMENT PIPELINE v1"

        self.executions = []


    def start_build(
        self,
        project
    ):

        execution = {

            "id":
            "build_" + uuid.uuid4().hex[:8],

            "project":
            project["name"],

            "objective":
            project["objective"],

            "agents":[],

            "tasks":[],

            "status":
            "RUNNING",

            "timestamp":
            time.time()

        }


        for task in project["tasks"]:

            assignment = {

                "task":
                task["task"],

                "agent":
                task["agent"],

                "status":
                "QUEUED"

            }

            execution["tasks"].append(
                assignment
            )

            if task["agent"] not in execution["agents"]:

                execution["agents"].append(
                    task["agent"]
                )


        self.executions.append(
            execution
        )


        print(
            f"🚀 Build started: {project['name']}"
        )


        return execution



    def run_task(
        self,
        build_id,
        task_name
    ):


        for build in self.executions:

            if build["id"] == build_id:


                for task in build["tasks"]:

                    if task["task"] == task_name:

                        task["status"] = "COMPLETED"

                        task["completed"] = time.time()


                        print(
                            f"✅ Completed {task_name} by {task['agent']}"
                        )


                        return task


        return None



    def complete_build(
        self,
        build_id
    ):

        for build in self.executions:

            if build["id"] == build_id:

                build["status"] = "COMPLETED"

                return build


        return None



    def report(self):

        return {

            "system":
            self.system,

            "builds":
            len(self.executions),

            "timestamp":
            time.time()

        }



development_pipeline = GenesisDevelopmentPipeline()
