import time
import uuid


class GenesisOmegaDecisionGate:

    """
    GENESIS OMEGA DECISION GATE v1

    Determines whether an action can execute
    automatically or requires human approval.
    """

    def __init__(
        self,
        approval_system=None
    ):

        self.system = (
            "GENESIS OMEGA DECISION GATE v1"
        )

        self.approval_system = approval_system
        self.decisions = []


    def evaluate(
        self,
        action,
        worker,
        data=None
    ):

        data = data or {}

        risk_keywords = [

            "send",
            "email",
            "publish",
            "purchase",
            "payment",
            "account",
            "delete",
            "external"

        ]


        requires_approval = any(

            word in action.lower()

            for word in risk_keywords

        )


        decision = {

            "id":
                "decision_"
                + uuid.uuid4().hex[:8],

            "action":
                action,

            "worker":
                worker,

            "risk":
                "HIGH"
                if requires_approval
                else "LOW",

            "status":
                None,

            "created":
                time.time()

        }


        if requires_approval:

            decision["status"] = (
                "WAITING_APPROVAL"
            )


            if self.approval_system:

                decision["approval"] = (
                    self.approval_system.request_approval(
                        action,
                        worker,
                        data
                    )
                )


        else:

            decision["status"] = (
                "AUTO_APPROVED"
            )


        self.decisions.append(
            decision
        )


        print(
            "🧠 Decision:",
            decision["status"],
            decision["id"]
        )


        return decision



    def report(self):

        return {

            "system":
                self.system,

            "decisions":
                len(self.decisions),

            "status":
                "ONLINE",

            "timestamp":
                time.time()
        }



genesis_decision_gate = (
    GenesisOmegaDecisionGate()
)
