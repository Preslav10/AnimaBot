import json
import os

class Memory:
    def __init__(self, file="memory.json"):
        self.file = file
        self.data = self.load()

    def load(self):
        if not os.path.exists(self.file):
            return {}
        with open(self.file, "r") as f:
            return json.load(f)

    def save(self, key, value):
        self.data[key] = value
        with open(self.file, "w") as f:
            json.dump(self.data, f, indent=4)

    def exists(self, key):
        return key in self.data