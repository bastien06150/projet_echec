import os
from models.tournament import Tournament
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from views.menu_view import MainMenuView


player_ctrl = PlayerController()
tournament_controller = TournamentController()
current_tournament = None

while True:
    choix = MainMenuView.display_main_menu()

    if choix == "1":
        # Sous-menu pour les joueurs
        print("\n1. Ajouter un joueur")
        print("2. Liste des joueurs")
        action = input("Votre choix : ")

        if action == "1":
            player_ctrl.add_player()
        elif action == "2":
            player_ctrl.list_players()
        else:
            print("Choix invalide.")

    elif choix == "2":
        tournament_controller.create_tournament()

    elif choix == "3":
        tournament_controller.load_tournament()

    elif choix == "4":
        if current_tournament:
            tournament_controller.jouer_round_suivant(current_tournament)
        else:
            path = input("Chemin du tournoi existant : ").strip()
            if not os.path.exists(path):
                print("Fichier introuvable.")
            else:
                current_tournament = Tournament.load_from_file(path)
                tournament_controller.jouer_round_suivant(current_tournament)

    elif choix == "5":
        print(" Fin du programme.")
        break
