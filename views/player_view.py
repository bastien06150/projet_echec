from datetime import datetime
import re


class PlayerView:
    @staticmethod
    def prompt_new_player():
        print("--- Nouveau joueur ---")
        last_name = input("Nom : ")
        first_name = input("Prénom : ")

        while True:
            birth_date = input("Date de naissance (DD-MM-YYYY) : ").strip()
            try:
                datetime.strptime(birth_date, "%d-%m-%Y")
                break
            except ValueError:
                print("Format invalide. Utilise le format DD-MM-YYYY (ex: 31-12-1990).")

        while True:
            national_id = input("ID national (ex : FR12345) : ").strip().upper()
            if re.fullmatch(r"[A-Z]{2}\d{5}", national_id):
                print("ID valide !")
                break
            else:
                print("ID invalide. Réessayer ")
        return {
            "last_name": last_name,
            "first_name": first_name,
            "birth_date": birth_date,
            "national_id": national_id,
        }

    @staticmethod
    def display_players(players):
        print("--- Liste des joueurs ---")
        if not players:
            print("Aucun joueur enregistré.")
            return

        for player in sorted(players, key=lambda player: player.last_name):
            print(f"{player.last_name}, {player.first_name} - ID: {player.national_id}")
