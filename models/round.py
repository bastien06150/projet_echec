from datetime import datetime
from models.match import Match


class Round:
    def __init__(self, name):
        self.name = name
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.end_time = None
        self.matches = []

    def end_round(self):
        self.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "name": self.name,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "matches": [match.to_list() for match in self.matches],
        }

    @classmethod
    def creation_round_from_dict(cls, data):
        round_obj = cls(data["name"])
        round_obj.start_time = data.get("start_time", "")
        round_obj.end_time = data.get("end_time", None)
        round_obj.matches = [Match.creation_match_from_list(m) for m in data["matches"]]
        return round_obj
