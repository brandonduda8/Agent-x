import os
import json
from pathlib import Path


class GenesisMetaAuditor:

    def __init__(self):
        self.name = "GENESIS META AUDITOR"
        self.report_file = Path(
            "memory/genesis_audit.json"
        )

        self.report_file.parent.mkdir(
            exist_ok=True
        )


    def scan_files(self):

        results = []

        for root, dirs, files in os.walk("."):

            if "node_modules" in root:
                continue

            for file in files:

                if file.endswith(
                    (".py",".js",".yaml",".json")
                ):
                    results.append(
                        os.path.join(
                            root,
                            file
                        )
                    )

        return results


    def audit(self):

        files = self.scan_files()

        report = {

            "system":
                "GENESIS",

            "files_detected":
                len(files),

            "agents": [],

            "missing_connections": [],

            "recommendations": []

        }


        for f in files:

            if "agent" in f.lower():

                report["agents"].append(f)


        if not Path(
            "memory"
        ).exists():

            report["recommendations"].append(
                "Create persistent memory layer"
            )


        if not Path(
            "core/event_bus.py"
        ).exists():

            report["missing_connections"].append(
                "Event bus missing"
            )


        report["recommendations"].extend([

            "Connect every agent to LLM Council",

            "Create unified agent heartbeat",

            "Create capability registry",

            "Create autonomous upgrade loop",

            "Create revenue execution pipeline"

        ])


        self.report_file.write_text(
            json.dumps(
                report,
                indent=2
            )
        )


        return report



meta_auditor = GenesisMetaAuditor()
