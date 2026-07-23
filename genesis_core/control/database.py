import sqlite3
import time
import json


class GenesisDatabase:


    def __init__(
        self,
        path="genesis_memory.db"
    ):

        self.connection = sqlite3.connect(
            path
        )

        self.create_tables()



    def create_tables(
        self
    ):

        cursor = self.connection.cursor()


        cursor.execute("""

        CREATE TABLE IF NOT EXISTS memories (

            id TEXT PRIMARY KEY,

            type TEXT,

            data TEXT,

            timestamp REAL

        )

        """)



        cursor.execute("""

        CREATE TABLE IF NOT EXISTS missions (

            id TEXT PRIMARY KEY,

            objective TEXT,

            priority TEXT,

            value REAL,

            status TEXT,

            timestamp REAL

        )

        """)



        cursor.execute("""

        CREATE TABLE IF NOT EXISTS opportunities (

            id TEXT PRIMARY KEY,

            title TEXT,

            category TEXT,

            value REAL,

            status TEXT,

            timestamp REAL

        )

        """)


        self.connection.commit()



    def save(
        self,
        table,
        record
    ):

        cursor = self.connection.cursor()


        if table == "memories":

            cursor.execute(

            """
            INSERT INTO memories
            VALUES (?,?,?,?)
            """,

            (

            record["id"],

            record["type"],

            json.dumps(record["data"]),

            record["timestamp"]

            )

            )


        self.connection.commit()



    def count(
        self,
        table
    ):

        cursor = self.connection.cursor()

        result = cursor.execute(

            f"SELECT COUNT(*) FROM {table}"

        ).fetchone()


        return result[0]
