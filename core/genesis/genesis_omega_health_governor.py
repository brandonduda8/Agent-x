import os
import time
import uuid
import json


class GenesisOmegaHealthGovernor:

    def __init__(self):
        self.system = "GENESIS OMEGA HEALTH GOVERNOR v1"
        self.history = []
        self.report_file = "data/genesis_omega_health_report.json"

        os.makedirs("data", exist_ok=True)


    def check_component(self, path):

        return {
            "component": path,
            "online": os.path.exists(path)
        }


    def check_environment(self):

        return {
            "termux": "com.termux" in os.getcwd(),
            "openai_connected": bool(
                os.getenv("OPENAI_API_KEY")
            ),
            "openrouter_connected": bool(
                os.getenv("OPENROUTER_API_KEY")
            ),
            "working_directory": os.getcwd()
        }


    def check_genesis_core(self):

        components = [
            "core/genesis",
            "core/genesis/genesis_unified_command_center.py",
            "core/genesis/genesis_emergency_life_operations_center.py",
            "core/genesis/genesis_intelligence_adapter_manager.py",
            "core/genesis/agent_registry.py",
            "core/genesis/memory_engine.py"
        ]

        results = []

        for component in components:
            results.append(
                self.check_component(component)
            )

        return results


    def calculate_health(self, report):

        failures = []

        for component in report["components"]:
            if not component["online"]:
                failures.append(
                    component["component"]
                )


        environment = report["environment"]

        warnings = []

        if not environment["openai_connected"]:
            warnings.append(
                "OpenAI adapter unavailable"
            )

        if not environment["openrouter_connected"]:
            warnings.append(
                "OpenRouter adapter unavailable"
            )


        if failures:
            return "BLOCKED", failures + warnings


        if warnings:
            return "WARNING", warnings


        return "READY", []


    def run_check(self):

        print(
            "🧬 Genesis Omega Health Governor Started"
        )

        report = {
            "id":
                "health_" + uuid.uuid4().hex[:8],

            "system":
                self.system,

            "timestamp":
                time.time(),

            "environment":
                self.check_environment(),

            "components":
                self.check_genesis_core()
        }


        status, issues = self.calculate_health(report)


        report["health_status"] = status
        report["issues"] = issues
        report["status"] = "COMPLETE"


        self.history.append(report)


        with open(self.report_file, "w") as f:
            json.dump(
                report,
                f,
                indent=2
            )


        print(
            "✅ Genesis Omega Health Check Complete"
        )

        return report


    def report(self):

        return {
            "system": self.system,
            "checks_completed": len(self.history),
            "status": "ONLINE",
            "timestamp": time.time()
        }



genesis_omega_health_governor = (
    GenesisOmegaHealthGovernor()
)
