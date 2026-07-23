import os
import time
import json
import uuid


class GenesisOmegaConnectorAudit:

    def __init__(self):
        self.system = "GENESIS OMEGA CONNECTOR AUDIT ENGINE v1"
        self.history = []
        self.report_file = "data/genesis_omega_connector_audit.json"

        os.makedirs("data", exist_ok=True)


    def check_path(self, path):
        return {
            "path": path,
            "exists": os.path.exists(path)
        }


    def check_environment(self):

        return {
            "python": os.sys.version,
            "working_directory": os.getcwd(),
            "openai_key": bool(os.getenv("OPENAI_API_KEY")),
            "openrouter_key": bool(os.getenv("OPENROUTER_API_KEY")),
            "termux": "com.termux" in os.getcwd()
        }


    def check_genesis_components(self):

        components = [
            "core/genesis",
            "data",
            "core/genesis/agent_registry.py",
            "core/genesis/memory_engine.py",
            "core/genesis/genesis_unified_command_center.py",
            "core/genesis/genesis_emergency_life_operations_center.py",
            "core/genesis/android_mcp_adapter.py",
            "core/genesis/genesis_intelligence_adapter_manager.py"
        ]

        results = {}

        for component in components:
            results[component] = os.path.exists(component)

        return results


    def generate_recommendations(self, report):

        recommendations = []

        if not report["environment"]["openai_key"]:
            recommendations.append(
                "Connect OpenAI adapter or alternative intelligence provider"
            )

        if not report["environment"]["openrouter_key"]:
            recommendations.append(
                "Connect OpenRouter adapter for multi-model routing"
            )

        if not report["components"].get(
            "core/genesis/android_mcp_adapter.py",
            False
        ):
            recommendations.append(
                "Repair Android adapter bridge"
            )

        if not report["components"].get(
            "core/genesis/genesis_emergency_life_operations_center.py",
            False
        ):
            recommendations.append(
                "Reconnect emergency life operations"
            )

        if not recommendations:
            recommendations.append(
                "All primary connectors operational"
            )

        return recommendations


    def run(self):

        print("🧬 Genesis Omega Connector Audit Started")

        report = {
            "id": "omega_audit_" + uuid.uuid4().hex[:8],
            "system": self.system,
            "timestamp": time.time(),
            "environment": self.check_environment(),
            "components": self.check_genesis_components()
        }

        report["recommendations"] = self.generate_recommendations(report)

        report["status"] = "COMPLETE"

        self.history.append(report)

        with open(self.report_file, "w") as f:
            json.dump(report, f, indent=2)


        print("✅ Genesis Omega Connector Audit Complete")

        return report


    def report(self):

        return {
            "system": self.system,
            "audits_completed": len(self.history),
            "status": "ONLINE",
            "timestamp": time.time()
        }



genesis_omega_connector_audit = GenesisOmegaConnectorAudit()
