import os
import time
import uuid


class GenesisBuildValidator:

    def __init__(self):

        self.system = "GENESIS BUILD VALIDATOR v1"

        self.validations = []



    def validate_file(
        self,
        path
    ):

        result = {

            "file":
            path,

            "exists":
            os.path.exists(path),

            "readable":
            False,

            "status":
            "FAILED",

            "timestamp":
            time.time()

        }


        if result["exists"]:

            try:

                with open(
                    path,
                    "r"
                ) as file:

                    file.read()

                result["readable"] = True

                result["status"] = "PASS"


            except Exception as e:

                result["error"] = str(e)



        return result



    def validate_project(
        self,
        project_path
    ):

        required_files = [

            "lib/main.dart",

            "lib/services/genesis_api.dart",

            "lib/screens/dashboard.dart"

        ]


        results = []


        passed = 0


        for file in required_files:

            result = self.validate_file(

                os.path.join(
                    project_path,
                    file
                )

            )

            results.append(result)


            if result["status"] == "PASS":

                passed += 1



        report = {

            "id":
            "validation_" + uuid.uuid4().hex[:8],

            "project":
            project_path,

            "files_checked":
            len(required_files),

            "files_passed":
            passed,

            "results":
            results,

            "status":
            "PASS" if passed == len(required_files)
            else "FAILED",

            "timestamp":
            time.time()

        }


        self.validations.append(report)


        print(
            f"🧪 Build validation completed: {project_path}"
        )


        return report



    def report(self):

        return {

            "system":
            self.system,

            "validations":
            len(self.validations),

            "timestamp":
            time.time()

        }



build_validator = GenesisBuildValidator()
