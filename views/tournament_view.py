from datetime import datetime


class TournamentView:
    @staticmethod
    def prompt_new_tournament():
        print("\n--- Créer un nouveau tournoi ---")
        while True:
            name = input("Nom du tournoi : ").strip()
            if not name:
                print("Le nom peut pas etre vide.")
                continue

            location = input("Lieu : ")
            if not location:
                print("le lieu ne peut pas etre vide")
            break

        while True:
            start_date = input("Date de début (DD-MM-YYYY) : ").strip()
            try:
                datetime.strptime(start_date, "%d-%m-%Y")
                break
            except ValueError:
                print("Format de date invalide. Attendu : .DD-MM-YYYY")

        while True:
            end_date = input("Date de fin (DD-MM-YYYY) : ").strip()
            try:
                datetime.strptime(end_date, "%d-%m-%Y")
                break
            except ValueError:
                print("Format de date invalide. Attendu : .DD-MM-YYYY")

        description = input("Description : ")
        return {
            "name": name,
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "description": description,
        }

    @staticmethod
    def display_tournaments(tournaments):
        print("\n--- Tournois enregistrés ---")
        if not tournaments:
            print("Aucun tournoi disponible.")
            return

        for i, tournament in enumerate(tournaments):
            print(
                f"{i + 1}. {tournament.name} - {tournament.location} ({tournament.start_date} → {tournament.end_date})"
            )

    @staticmethod
    def display_tournament_detail(tournament):
        print(f"\n Tournoi : {tournament.name}")
        print(f" Lieu : {tournament.location}")
        print(f" Du {tournament.start_date} au {tournament.end_date}")
        print(f" Description : {tournament.description}")
        print(f" Joueurs inscrits : {len(tournament.players)}")
        print(
            f" Tours effectués : {tournament.current_round_number}/{tournament.number_of_round}"
        )
