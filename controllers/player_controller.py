import os
import json
from models.player import Player
from views.player_view import PlayerView


class PlayerController:
    def __init__(self):
        self.players = []
        self.data_file = "data/players.json"
        self.load_players()

    def load_players(self):
        """Charge les joueurs existants depuis le JSON."""
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.players = [Player.creation_joueur_from_dict(p) for p in data]

    def save_players(self):
        """Sauvegarde les joueurs dans un JSON."""
        os.makedirs("data", exist_ok=True)
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump([p.to_dict() for p in self.players], f, indent=4)

    def add_player(self):
        """Ajoute un nouveau joueur via la vue."""
        data = PlayerView.prompt_new_player()
        new_player = Player(**data)

        # Évite les doublons par ID
        if any(p.national_id == new_player.national_id for p in self.players):
            print("Ce joueur existe déjà.")
        else:
            self.players.append(new_player)
            self.save_players()
            print("Joueur ajouté avec succès.")

    def list_players(self):
        """Affiche tous les joueurs."""
        PlayerView.display_players(self.players)
