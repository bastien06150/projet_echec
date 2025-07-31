import json
from models.round import Round
from models.player import Player


class Tournament:
    def __init__(
        self, name, location, start_date, end_date, description="", number_of_rounds=4
    ):
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.number_of_round = number_of_rounds
        self.current_round_number = 0
        self.players = []
        self.rounds = []
        self.match_history = set()  # évite les rematchs

    def add_player(self, player: Player):
        if any(p.national_id == player.national_id for p in self.players):
            print(
                f"Joueur déjà inscrit : {player.first_name} {player.last_name} {player.national_id}"
            )
        else:
            self.players.append(player)
            print(
                f"Joueur ajouté au tournoi : {player.first_name} {player.last_name} ({player.national_id})"
            )
            print(f"Nombre total de joueurs dans le tournoi : {len(self.players)}")

    def get_player_by_id(self, national_id):
        for player in self.players:
            if player.national_id == national_id:
                return player
        return None

    def to_dict(self):
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "description": self.description,
            "number_of_round": self.number_of_round,
            "current_round_number": self.current_round_number,
            "players": [player.to_dict() for player in self.players],
            "rounds": [round.to_dict() for round in self.rounds],
        }

    @classmethod
    def creation_tournament_from_dict(cls, data):
        tournament = cls(
            data["name"],
            data["location"],
            data["start_date"],
            data["end_date"],
            data.get("description", ""),
            data.get("number_of_round", 4),
        )

        tournament.current_round_number = data.get("current_round_number", 0)
        tournament.players = [
            Player.creation_joueur_from_dict(player) for player in data["players"]
        ]
        tournament.rounds = [
            Round.creation_round_from_dict(round) for round in data["rounds"]
        ]
        return tournament

    def save_to_file(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=4)

    @staticmethod
    def load_from_file(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Tournament.creation_tournament_from_dict(data)
