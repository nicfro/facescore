import os
import json


class UserData:
    def __init__(self):
        with open(
            os.path.join(os.path.dirname(__file__), "data.json"), encoding="utf-8"
        ) as f:
            self.data = json.load(f)

        self.users = [x for x in self.data]
