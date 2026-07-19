import time
import uuid


class ContactManager:

    def __init__(self):
        self.contacts = []


    def create_contact(self, company, industry, role):
        contact = {
            "id": f"contact_{uuid.uuid4().hex[:8]}",
            "company": company,
            "industry": industry,
            "role": role,
            "pain_points": [],
            "score": 0,
            "created": time.time()
        }

        self.contacts.append(contact)

        print(f"👤 Contact created: {company}")

        return contact


contact_manager = ContactManager()
