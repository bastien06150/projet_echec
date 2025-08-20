from controllers.player_controller import PlayerController
from models.tournament import Tournament
from models.round import Round
from models.match import Match
from models.player import Player
from views.tournament_view import TournamentView
from views.player_view import PlayerView
import os


class TournamentController:

    def create_tournament(self):
        """Crée un nouveau tournoi"""

        tournament = self._init_tournament()
        player_controller = PlayerController()

        self._print_existing_players(player_controller)
        self._add_existing_players_to_tournament(tournament, player_controller)
        self._handle_player_addition_loop(tournament, player_controller)

        self._save_tournament(tournament)
        self.jouer_round_suivant(tournament)

    def _init_tournament(self):
        data = TournamentView.prompt_new_tournament()
        return Tournament(**data)

    def _print_existing_players(self, player_controller):
        TournamentView.display_existing_players(player_controller.players)

    def _add_existing_players_to_tournament(self, tournament, player_controller):
        for player in player_controller.players:
            tournament.add_player(player)

    def _handle_player_addition_loop(self, tournament, player_controller):
        """ajout des joueurs au tournoi jusqu’à ce qu’il y en ait au moins 4"""

        while True:
            choix = TournamentView.prompt_player_addition_choice()

            if choix == "1":
                self._ajouter_nouveau_joueur(tournament, player_controller)

            elif choix == "2":
                if len(tournament.players) < 4:
                    TournamentView.show_min_players_required(len(tournament.players))
                else:
                    break
            else:
                TournamentView.show_invalid_choice()

    def _ajouter_nouveau_joueur(self, tournament, player_controller):
        player_data = PlayerView.prompt_new_player()
        new_player = Player(**player_data)

        if any(
            p.national_id == new_player.national_id for p in player_controller.players
        ):
            TournamentView.show_message("Ce joueur est déjà enregistré.")
        else:
            player_controller.players.append(new_player)
            player_controller.save_players()
            tournament.add_player(new_player)
            TournamentView.show_message(
                f"Joueur {new_player.first_name} {new_player.last_name} ajouté."
            )

    def _save_tournament(self, tournament):
        os.makedirs("data", exist_ok=True)
        filename = f"data/tournoi_{tournament.name.replace(' ', '_').lower()}.json"
        tournament.save_to_file(filename)

        self.jouer_round_suivant(tournament)

    def load_tournament(self):
        path = TournamentView.prompt_tournament_file_path()
        if not os.path.exists(path):
            TournamentView.show_message("Fichier inexistant! ")
            return
        tournament = Tournament.load_from_file(path)
        TournamentView.display_tournament_detail(tournament)

    def generer_paires(self, joueurs, match_history):
        """Génère des paires de joueurs pour un round, en évitant les rematchs si possible"""

        joueurs_tries = sorted(joueurs, key=lambda j: j.score, reverse=True)
        matchs = []
        players_with_match = set()
        i = 0

        while i < len(joueurs_tries) - 1:
            j1 = joueurs_tries[i]
            if j1.national_id in players_with_match:
                i += 1
                continue

            j2 = None
            for j in range(i + 1, len(joueurs_tries)):
                j_potentiel = joueurs_tries[j]
                key = tuple(sorted([j1.national_id, j_potentiel.national_id]))
                if (
                    j_potentiel.national_id not in players_with_match
                    and key not in match_history
                ):
                    j2 = j_potentiel
                    break

            # Si aucun joueur inédit, on prend le premier dispo même si déjà affronté
            if not j2:
                for j in range(i + 1, len(joueurs_tries)):
                    j_potentiel = joueurs_tries[j]
                    if j_potentiel.national_id not in players_with_match:
                        j2 = j_potentiel
                        break

            if j2:
                key = tuple(sorted([j1.national_id, j2.national_id]))
                matchs.append(Match(j1.national_id, j2.national_id))
                match_history.add(key)
                players_with_match.update([j1.national_id, j2.national_id])
            i += 1

        TournamentView.show_match_count(len(matchs))
        return matchs

    def jouer_round_suivant(self, tournament):
        """Lance le round suivant du tournoi"""

        if tournament.current_round_number >= tournament.number_of_round:
            TournamentView.show_all_rounds_played(
                tournament.current_round_number, tournament.number_of_round
            )
            return

        round_name = f"Round {tournament.current_round_number + 1}"
        nouveau_round = Round(round_name)
        nouveau_round.matches = self.generer_paires(
            tournament.players, tournament.match_history
        )

        if not nouveau_round.matches:
            TournamentView.show_no_matches()
            return

        TournamentView.show_round_header(round_name)

        TournamentView.display_match_list(nouveau_round.matches, tournament)

        for match in nouveau_round.matches:
            joueur1 = tournament.get_player_by_id(match.player1_id)
            joueur2 = tournament.get_player_by_id(match.player2_id)

            # Saisie et validation des scores
            TournamentView.display_match(joueur1, joueur2)
            s1, s2 = TournamentView.prompt_match_result(joueur1, joueur2)

            match.score1 = s1
            match.score2 = s2
            joueur1.score += s1
            joueur2.score += s2

        nouveau_round.end_round()
        tournament.rounds.append(nouveau_round)
        tournament.current_round_number += 1
        filename = f"data/tournoi_{tournament.name.replace(' ', '_').lower()}.json"
        tournament.save_to_file(filename)

        TournamentView.show_round_end(round_name)
        TournamentView.display_scores(tournament.players)

        if tournament.current_round_number >= tournament.number_of_round:
            joueurs_tries = sorted(
                tournament.players, key=lambda j: j.score, reverse=True
            )
            gagnant = joueurs_tries[0]
            TournamentView.display_winner(gagnant)
