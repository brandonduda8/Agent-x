import uuid
import time

from genesis_core.memory.database import GenesisDatabase



class GenesisMemoryManager:


    def __init__(self):

        self.db = GenesisDatabase()



    def remember(
        self,
        category,
        data
    ):

        self.db.insert(

            "memories",

            [

                "memory_" + uuid.uuid4().hex[:8],

                category,

                str(data),

                time.time()

            ]

        )


    def recall(
        self,
        category
    ):

        memories = self.db.query(
            "memories"
        )

        return [

            item

            for item in memories

            if item[1] == category

        ]
