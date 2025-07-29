class PlayerView:
    @staticmethod
    def prompt_new_player():
        print("--- Nouveau joueur ---")
        last_name = input("Nom : ")
        first_name = input("Prénom : ")
        birth_date = input("Date de naissance (DD-MM-YYYY) : ")
        national_id = input("ID national (ex : FR12345) : ")
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
