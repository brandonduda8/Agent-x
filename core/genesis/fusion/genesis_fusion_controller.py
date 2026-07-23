import os
import json
import time


class GenesisFusionController:

    def __init__(self):

        self.system = "GENESIS FUSION CONTROLLER v1"

        self.root = "core/genesis"

        self.report = {
            "system": self.system,
            "timestamp": time.time(),
            "agents": [],
            "engines": [],
            "controllers": [],
            "brains": [],
            "tests": 0,
            "python_files": 0,
            "folders": 0,
            "recommendations": []
        }


    def scan(self):

        for folder, dirs, files in os.walk(self.root):

            self.report["folders"] += 1

            for file in files:

                if file.endswith(".py"):

                    self.report["python_files"] += 1

                    path = os.path.join(folder, file)

                    if "test" in file.lower():
                        self.report["tests"] += 1


                    try:

                        text = open(
                            path,
                            errors="ignore"
                        ).read()


                        for line in text.splitlines():

                            clean = line.strip()


                            if clean.startswith("class "):

                                name = clean.replace(
                                    "class ",
                                    ""
                                ).split("(")[0].replace(":","")


                                lower = name.lower()


                                item = {
                                    "name": name,
                                    "file": path
                                }


                                if "agent" in lower:
                                    self.report["agents"].append(item)

                                elif "engine" in lower:
                                    self.report["engines"].append(item)

                                elif "controller" in lower:
                                    self.report["controllers"].append(item)

                                elif "brain" in lower:
                                    self.report["brains"].append(item)


                    except Exception:
                        pass


        self.generate_recommendations()

        return self.report



    def generate_recommendations(self):

        if len(self.report["controllers"]) > 10:

            self.report["recommendations"].append(
                "Consolidate controller hierarchy"
            )


        if len(self.report["engines"]) > 50:

            self.report["recommendations"].append(
                "Create engine capability registry"
            )


        if len(self.report["agents"]) > 20:

            self.report["recommendations"].append(
                "Create workforce orchestration layer"
            )


        self.report["recommendations"].append(
            "Connect tool registry with real adapters"
        )

        self.report["recommendations"].append(
            "Activate runtime kernel governance"
        )



    def save(self):

        os.makedirs(
            "core/genesis/data",
            exist_ok=True
        )


        with open(
            "core/genesis/data/genesis_fusion_report.json",
            "w"
        ) as f:

            json.dump(
                self.report,
                f,
                indent=2
            )


        return "Fusion report saved"



genesis_fusion_controller = GenesisFusionController()
