import os
from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from views.menu_view import MainMenuView
from models.tournament import Tournament
from views.tournament_view import TournamentView


class MainController:
    def __init__(self):
        self.player_ctrl = PlayerController()
        self.tournament_ctrl = TournamentController()
        self.current_tournament = None

    def run(self):
        """affiche le menu principal et redirige vers les actions choisies"""

        while True:
            choix = MainMenuView.display_main_menu()

            if choix == "1":
                self._menu_joueurs()

            elif choix == "2":
                self.tournament_ctrl.create_tournament()

            elif choix == "3":
                self.tournament_ctrl.load_tournament()

            elif choix == "4":
                self.tournament_ctrl.afficher_tous_les_tournois()

            elif choix == "5":
                self._lancer_round()

            elif choix == "6":
                MainMenuView.show_exit_message()
                break

    def _menu_joueurs(self):
        while True:
            action = MainMenuView.display_player_menu()
            if action == "1":
                self.player_ctrl.add_player()
            elif action == "2":
                self.player_ctrl.list_players()
            elif action == "3":
                break
            else:
                MainMenuView.show_invalid_choice()

    def _lancer_round(self):
        name = TournamentView.prompt_tournament_name()
        filename = f"data/tournoi_{name.replace(' ', '_').lower()}.json"

        if not os.path.exists(filename):
            TournamentView.show_message("Fichier introuvable.")
            return

        self.current_tournament = Tournament.load_from_file(filename)
        self.tournament_ctrl.jouer_round_suivant(self.current_tournament)
