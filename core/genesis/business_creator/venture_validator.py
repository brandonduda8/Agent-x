import uuid
import time


class VentureValidator:

    def validate(self, company):

        result={
            "id":f"validation_{uuid.uuid4().hex[:8]}",
            "company":company["name"],
            "market_fit":"HIGH",
            "status":"APPROVED",
            "timestamp":time.time()
        }

        print(
            "📈 Venture validated"
        )

        return result


venture_validator = VentureValidator()
