import uuid
import time


class ExpenseManager:

    def track(self, company, expenses):

        result = {
            "id": f"expense_{uuid.uuid4().hex[:8]}",
            "company": company,
            "expenses": expenses,
            "timestamp": time.time()
        }

        print(f"💸 Expenses tracked: ${expenses}")

        return result


expense_manager = ExpenseManager()
