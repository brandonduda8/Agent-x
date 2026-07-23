import sqlite3
import time


class GenesisDatabase:


    def __init__(
        self,
        path="genesis_memory.db"
    ):

        self.connection = sqlite3.connect(
            path
        )

        self.create_tables()



    def create_tables(self):

        cursor = self.connection.cursor()


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS agents (

            id TEXT,
            name TEXT,
            type TEXT,
            skills TEXT,
            timestamp REAL

        )
        """)


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (

            id TEXT,
            business TEXT,
            offer TEXT,
            value REAL,
            stage TEXT,
            timestamp REAL

        )
        """)


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS missions (

            id TEXT,
            objective TEXT,
            status TEXT,
            value REAL,
            timestamp REAL

        )
        """)


        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (

            id TEXT,
            category TEXT,
            data TEXT,
            timestamp REAL

        )
        """)


        self.connection.commit()



    def insert(
        self,
        table,
        values
    ):

        cursor = self.connection.cursor()


        placeholders = ",".join(
            ["?"] * len(values)
        )


        cursor.execute(

            f"INSERT INTO {table} VALUES ({placeholders})",

            values

        )


        self.connection.commit()



    def query(
        self,
        table
    ):

        cursor = self.connection.cursor()

        cursor.execute(
            f"SELECT * FROM {table}"
        )

        return cursor.fetchall()
