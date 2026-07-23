import json
from pathlib import Path
from datetime import datetime


class RepositoryScanner:

    IGNORE_DIRS = {
        ".git",
        "node_modules",
        "__pycache__",
        "venv",
        ".venv",
        "env",
        "dist",
        "build",
        ".cache",
        ".pytest_cache",
    }

    IMPORTANT_DIRS = {
        "core",
        "agents",
        "config",
        "data",
        "deployment",
        "integrations",
        "memory",
        "tools",
        "scripts",
    }


    def __init__(self, root="."):

        self.root = Path(root)

        self.output_dir = Path(
            "memory/meta_audit"
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )


    def should_ignore(self, path):

        for part in path.parts:

            if part in self.IGNORE_DIRS:
                return True

        return False


    def scan(self):

        report = {

            "timestamp":
                datetime.utcnow().isoformat(),

            "system":
                "CLAW-OS / GENESIS",

            "files": [],

            "directories": [],

            "python_files": [],

            "javascript_files": [],

            "config_files": [],

            "agent_files": [],

            "core_files": [],

            "genesis_files": [],

            "important_paths": []

        }


        for path in self.root.rglob("*"):


            if self.should_ignore(path):
                continue


            if path.name.startswith("."):
                continue


            relative = str(path)


            if path.is_dir():

                report["directories"].append(
                    relative
                )

                if path.name in self.IMPORTANT_DIRS:
                    report["important_paths"].append(
                        relative
                    )

                continue



            report["files"].append(
                relative
            )


            if relative.endswith(".py"):

                report["python_files"].append(
                    relative
                )


            if relative.endswith(".js"):

                report["javascript_files"].append(
                    relative
                )


            if (
                relative.endswith(".yaml")
                or relative.endswith(".yml")
                or relative.endswith(".json")
            ):

                report["config_files"].append(
                    relative
                )


            if "agent" in relative.lower():

                report["agent_files"].append(
                    relative
                )


            if "/core/" in relative:

                report["core_files"].append(
                    relative
                )


            if "genesis" in relative.lower():

                report["genesis_files"].append(
                    relative
                )



        report["statistics"] = {

            "total_files":
                len(report["files"]),

            "python_files":
                len(report["python_files"]),

            "javascript_files":
                len(report["javascript_files"]),

            "agents":
                len(report["agent_files"]),

            "core_modules":
                len(report["core_files"]),

            "genesis_related":
                len(report["genesis_files"])

        }


        output = (
            self.output_dir /
            "repository.json"
        )


        output.write_text(
            json.dumps(
                report,
                indent=2
            )
        )


        return report
