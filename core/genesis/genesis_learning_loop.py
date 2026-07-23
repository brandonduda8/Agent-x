import time
import uuid
import json
import os


class GenesisLearningLoop:

    def __init__(self):
        self.name = "GENESIS LEARNING LOOP v1"

        self.memory_path = (
            "core/genesis/data/genesis_memory.json"
        )


    def load_memories(self):

        if not os.path.exists(self.memory_path):
            return []

        try:
            with open(self.memory_path, "r") as f:
                data = json.load(f)

            if isinstance(data, list):
                return data

            if isinstance(data, dict):

                if "memories" in data:
                    return data["memories"]

                return [data]

            return []

        except Exception as e:

            print("Memory load error:", e)
            return []


    def normalize_memory(self, memory):

        if isinstance(memory, dict):

            return {
                "agent": memory.get(
                    "agent",
                    "Unknown Agent"
                ),
                "objective": memory.get(
                    "objective",
                    ""
                ),
                "result": memory.get(
                    "result",
                    ""
                ),
                "score": memory.get(
                    "score",
                    0
                )
            }


        if isinstance(memory, str):

            return {
                "agent": "Unknown Agent",
                "objective": "",
                "result": memory,
                "score": 0
            }


        return {
            "agent": "Unknown Agent",
            "objective": "",
            "result": str(memory),
            "score": 0
        }


    def analyze(self):

        memories = self.load_memories()

        if not memories:

            return {
                "system": self.name,
                "status": "NO_MEMORY",
                "message": "Genesis has no experiences to analyze",
                "timestamp": time.time()
            }


        normalized = []

        for memory in memories:

            normalized.append(
                self.normalize_memory(memory)
            )


        best = max(
            normalized,
            key=lambda x: x.get("score", 0)
        )


        lesson = {

            "id":
                "lesson_" + uuid.uuid4().hex[:8],

            "type":
                "genesis_improvement",

            "source_agent":
                best["agent"],

            "insight":
                best["result"],

            "score":
                best["score"],

            "timestamp":
                time.time()
        }


        return {

            "system":
                self.name,

            "status":
                "LEARNING_COMPLETE",

            "memories_analyzed":
                len(normalized),

            "best_agent":
                best["agent"],

            "best_strategy":
                best["result"],

            "improvement_lesson":
                lesson,

            "timestamp":
                time.time()
        }



genesis_learning_loop = GenesisLearningLoop()
