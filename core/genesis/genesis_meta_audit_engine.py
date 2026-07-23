import os
import time
import uuid
import json
import ast


class GenesisMetaAuditEngine:

    def __init__(self):
        self.system = "GENESIS META AUDIT ENGINE v1"
        self.report_file = "data/genesis_meta_audit_report.json"

        os.makedirs("data", exist_ok=True)

        self.audit_history = []


    def scan_directory(self, path):

        results = {
            "path": path,
            "exists": False,
            "files": [],
            "errors": []
        }

        if not os.path.exists(path):
            return results

        results["exists"] = True

        for root, dirs, files in os.walk(path):

            for file in files:

                if file.endswith(".py"):

                    full_path = os.path.join(
                        root,
                        file
                    )

                    results["files"].append(
                        full_path
                    )

        return results


    def check_python_files(self, files):

        broken = []

        for file in files:

            try:

                with open(file, "r") as f:
                    code = f.read()

                ast.parse(code)


            except Exception as e:

                broken.append(
                    {
                        "file": file,
                        "error": str(e)
                    }
                )

        return broken


    def audit_environment(self):

        return {

            "termux_detected":
                "com.termux" in os.getcwd(),

            "python_version":
                os.sys.version,

            "working_directory":
                os.getcwd(),

            "env_keys_found":
                list(
                    os.environ.keys()
                )
        }


    def audit_adapters(self):

        adapters = [

            "core",
            "agents",
            "openclaw",
            "agent-x",
            "hermes",
            "adapters",
            "deployment"

        ]

        results = {}

        for adapter in adapters:

            results[adapter] = {
                "exists":
                    os.path.exists(adapter)
            }

        return results


    def run_audit(self):

        print(
            "🧬 Genesis Meta Audit Started"
        )


        core_scan = self.scan_directory(
            "core/genesis"
        )


        all_python = (
            core_scan["files"]
        )


        broken_files = (
            self.check_python_files(
                all_python
            )
        )


        report = {

            "id":
                "audit_" + uuid.uuid4().hex[:8],

            "system":
                self.system,

            "timestamp":
                time.time(),

            "core_scan":
                core_scan,

            "broken_python_files":
                broken_files,

            "environment":
                self.audit_environment(),

            "adapters":
                self.audit_adapters(),

            "status":
                "COMPLETE"

        }


        self.audit_history.append(
            report
        )


        with open(
            self.report_file,
            "w"
        ) as f:

            json.dump(
                report,
                f,
                indent=2
            )


        print(
            "✅ Genesis Meta Audit Complete"
        )


        return report



    def report(self):

        return {

            "system":
                self.system,

            "audits_completed":
                len(self.audit_history),

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_meta_audit_engine = (
    GenesisMetaAuditEngine()
)
