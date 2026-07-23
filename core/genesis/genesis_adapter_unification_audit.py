import os
import sys
import time
import json
import subprocess


class GenesisAdapterUnificationAudit:

    def __init__(self):

        self.system = (
            "GENESIS ADAPTER UNIFICATION AUDIT v1"
        )

        self.file = (
            "data/genesis_adapter_audit.json"
        )

        os.makedirs(
            "data",
            exist_ok=True
        )


    def check_command(self, command):

        try:

            result = subprocess.check_output(
                command,
                shell=True,
                stderr=subprocess.STDOUT
            )

            return result.decode().strip()

        except:

            return "NOT_AVAILABLE"


    def scan(self):

        audit = {

            "system":
                self.system,

            "android": {

                "termux":
                    "DETECTED"
                    if "com.termux" in sys.prefix
                    or os.path.exists(
                        "/data/data/com.termux"
                    )
                    else "UNKNOWN",

                "storage":
                    os.path.exists(
                        "/sdcard"
                    )

            },


            "runtime": {

                "python":
                    sys.version,

                "node":
                    self.check_command(
                        "node --version"
                    )

            },


            "environment": {

                "openrouter":
                    bool(
                        os.getenv(
                            "OPENROUTER_API_KEY"
                        )
                    ),

                "openai":
                    bool(
                        os.getenv(
                            "OPENAI_API_KEY"
                        )
                    )

            },


            "genesis": {

                "core":
                    os.path.exists(
                        "core/genesis"
                    ),

                "memory":
                    os.path.exists(
                        "data"
                    )

            },


            "timestamp":
                time.time()

        }


        with open(
            self.file,
            "w"
        ) as f:

            json.dump(
                audit,
                f,
                indent=2
            )


        return audit



    def report(self):

        return {

            "system":
                self.system,

            "status":
                "ONLINE",

            "timestamp":
                time.time()

        }



genesis_adapter_unification_audit = (
    GenesisAdapterUnificationAudit()
)
