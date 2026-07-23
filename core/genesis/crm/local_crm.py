import sqlite3
import uuid
import time
import os


class GenesisLocalCRM:

    def __init__(self):

        self.system = "GENESIS LOCAL CRM v1"

        self.db_path = os.path.expanduser(
            "genesis_crm.db"
        )

        self.connection = sqlite3.connect(
            self.db_path
        )

        self.initialize()


    def initialize(self):

        cursor = self.connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts(
            id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            company TEXT,
            status TEXT,
            created REAL
        )
        """)


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS deals(
            id TEXT PRIMARY KEY,
            contact_id TEXT,
            title TEXT,
            value REAL,
            stage TEXT,
            created REAL
        )
        """)


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS activities(
            id TEXT PRIMARY KEY,
            type TEXT,
            description TEXT,
            created REAL
        )
        """)


        self.connection.commit()



    def create_contact(
        self,
        name,
        email="",
        company=""
    ):

        contact_id = (
            "contact_"
            +
            uuid.uuid4().hex[:8]
        )


        self.connection.execute(
            """
            INSERT INTO contacts
            VALUES(?,?,?,?,?,?)
            """,
            (
                contact_id,
                name,
                email,
                company,
                "NEW",
                time.time()
            )
        )


        self.connection.commit()


        print(
            f"👤 CRM Contact Created: {contact_id}"
        )


        return contact_id



    def create_deal(
        self,
        contact_id,
        title,
        value
    ):

        deal_id = (
            "deal_"
            +
            uuid.uuid4().hex[:8]
        )


        self.connection.execute(
            """
            INSERT INTO deals
            VALUES(?,?,?,?,?,?)
            """,
            (
                deal_id,
                contact_id,
                title,
                value,
                "OPEN",
                time.time()
            )
        )


        self.connection.commit()


        print(
            f"💰 CRM Deal Created: {deal_id}"
        )


        return deal_id



    def add_activity(
        self,
        activity_type,
        description
    ):

        activity_id = (
            "activity_"
            +
            uuid.uuid4().hex[:8]
        )


        self.connection.execute(
            """
            INSERT INTO activities
            VALUES(?,?,?,?)
            """,
            (
                activity_id,
                activity_type,
                description,
                time.time()
            )
        )


        self.connection.commit()


        return activity_id



    def report(self):

        cursor = self.connection.cursor()


        contacts = cursor.execute(
            "SELECT COUNT(*) FROM contacts"
        ).fetchone()[0]


        deals = cursor.execute(
            "SELECT COUNT(*) FROM deals"
        ).fetchone()[0]


        activities = cursor.execute(
            "SELECT COUNT(*) FROM activities"
        ).fetchone()[0]


        return {

            "system": self.system,

            "database": self.db_path,

            "contacts": contacts,

            "deals": deals,

            "activities": activities,

            "status": "ONLINE",

            "timestamp": time.time()

        }



local_crm = GenesisLocalCRM()
