import time

class RealWorldVerification:

    def verify(self, action, evidence=None):

        if evidence:
            status = "VERIFIED"
        else:
            status = "WAITING_FOR_EVIDENCE"

        return {
            "system": "GENESIS REAL WORLD VERIFICATION v1",
            "action": action,
            "status": status,
            "evidence": evidence,
            "timestamp": time.time()
        }


verification = RealWorldVerification()
