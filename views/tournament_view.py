from datetime import datetime


class TournamentView:
    @staticmethod
    def prompt_new_tournament():
        """Demande les informations pour créer un nouveau tournoi"""

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
        """Affiche la liste des tournois enregistrés"""

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
        """Affiche les détails d'un tournoi"""

        print(f"\n Tournoi : {tournament.name}")
        print(f" Lieu : {tournament.location}")
        print(f" Du {tournament.start_date} au {tournament.end_date}")
        print(f" Description : {tournament.description}")
        print(f" Joueurs inscrits : {len(tournament.players)}")
        print(
            f" Tours effectués : {tournament.current_round_number}/{tournament.number_of_round}"
        )

    @staticmethod
    def show_match_count(n):
        print(f"{n} match(s) généré(s).")

    @staticmethod
    def display_existing_players(players):
        print("\n--- Joueurs existants ---")
        for player in players:
            print(f"- {player.first_name} {player.last_name} ({player.national_id})")

    def prompt_player_addition_choice():
        print("\n--- Ajout de joueurs ---")
        print("1. Ajouter un nouveau joueur")
        print("2. Terminer l'ajout de joueurs")
        return input("Votre choix : ").strip()

    @staticmethod
    def prompt_tournament_name():
        return input("Nom du tournoi à charger : ").strip()

    def show_message(message):
        print(message)

    @staticmethod
    def show_round_header(round_name):
        print(f"\n{round_name} — Saisie des résultats :")

    @staticmethod
    def display_match_list(matches, tournament):
        """Affiche tous les matchs d'un round"""

        print("\n--- Matchs du round ---")
        for match in matches:
            joueur1 = tournament.get_player_by_id(match.player1_id)
            joueur2 = tournament.get_player_by_id(match.player2_id)
            print(
                f"{joueur1.first_name} {joueur1.last_name} vs {joueur2.first_name} {joueur2.last_name}"
            )

    @staticmethod
    def display_match(joueur1, joueur2):
        print(
            f"\nMatch : {joueur1.first_name} {joueur1.last_name} vs {joueur2.first_name} {joueur2.last_name}"
        )

    @staticmethod
    def prompt_match_result(joueur1, joueur2):
        """Demande d'entrer le score pour chaque joueur d'un match"""

        while True:
            try:
                s1 = float(input(f"Score de {joueur1.last_name} : "))
                s2 = float(input(f"Score de {joueur2.last_name} : "))
                if (s1, s2) not in [(1.0, 0.0), (0.0, 1.0), (0.5, 0.5)]:
                    raise ValueError("Format non valide (1-0, 0-1 ou 0.5-0.5)")
                return s1, s2
            except ValueError as e:
                print(e)

    @staticmethod
    def show_round_end(round_name):
        print(f"\n{round_name} terminé et sauvegardé.")

    @staticmethod
    def display_scores(players):
        print("\nScores des joueurs :")
        for joueur in sorted(players, key=lambda j: j.score, reverse=True):
            print(
                f"{joueur.first_name} {joueur.last_name} ({joueur.national_id}) : {joueur.score} points"
            )

    @staticmethod
    def display_winner(winner):
        print("\nLe tournoi est terminé !")
        print(
            f"\nFélicitations à {winner.first_name} {winner.last_name}, le grand gagnant !"
        )

    @staticmethod
    def show_all_rounds_played(current, total):
        print("Tous les rounds ont déjà été joués.")
        print(f"⏳ Round actuel : {current}, Rounds prévus : {total}")

    @staticmethod
    def show_no_matches():
        print("Aucun match généré — impossible de lancer un nouveau round.")

    @staticmethod
    def show_min_players_required(current_count):
        print(
            f"Vous devez inscrire au moins 4 joueurs (actuellement : {current_count})."
        )

    @staticmethod
    def show_invalid_choice():
        print("Choix invalide.")
