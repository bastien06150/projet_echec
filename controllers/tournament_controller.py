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
        data = TournamentView.prompt_new_tournament()
        tournament = Tournament(**data)

        player_controller = PlayerController()

        print("\n--- Joueurs existants ---")
        for player in player_controller.players:
            print(f"- {player.first_name} {player.last_name} ({player.national_id})")

        for player in player_controller.players:
            tournament.add_player(player)

        while True:
            """print("\n1. Ajouter un joueur existant")"""
            print("2. Ajouter un nouveau joueur")
            print("3. Terminer l'ajout de joueurs")
            choix = input("Votre choix : ").strip()

            if choix == "1":
                national_id = input(
                    "Entrez l'ID national du joueur à ajouter : "
                ).strip()
                existing = next(
                    (
                        p
                        for p in player_controller.players
                        if p.national_id == national_id
                    ),
                    None,
                )
                if not existing:
                    print("Aucun joueur trouvé avec cet ID.")
                elif any(p.national_id == national_id for p in tournament.players):
                    print("Ce joueur est déjà dans le tournoi.")
                else:
                    tournament.add_player(existing)
                    print(
                        f"{existing.first_name} {existing.last_name} ajouté au tournoi."
                    )

            if choix == "2":
                player_data = PlayerView.prompt_new_player()
                new_player = Player(**player_data)

                if any(
                    p.national_id == new_player.national_id
                    for p in player_controller.players
                ):
                    print("Ce joueur est déjà enregistré.")
                else:
                    player_controller.players.append(new_player)
                    player_controller.save_players()
                    tournament.add_player(new_player)
                    print(
                        f"Joueur {new_player.first_name} {new_player.last_name} ajouté."
                    )

            elif choix == "3":
                if len(tournament.players) < 4:
                    print(
                        f"Vous devez inscrire au moins 4 joueurs (actuellement : {len(tournament.players)})."
                    )
                else:
                    break
            else:
                print("Choix invalide.")

        os.makedirs("data", exist_ok=True)
        tournament.save_to_file("data/tournoi_auto.json")
        print("Tournoi sauvegardé avec succès !")

        self.jouer_round_suivant(tournament)

    def load_tournament(self):
        path = input("Chemin du fichier tournoi (ex: data/tournoi_auto.json) : ")
        if not os.path.exists(path):
            print(" Fichier introuvable.")
            return
        tournament = Tournament.load_from_file(path)
        TournamentView.display_tournament_detail(tournament)

    def generer_paires(self, joueurs, match_history):

        joueurs_tries = sorted(joueurs, key=lambda j: j.score, reverse=True)
        matchs = []
        i = 0
        if len(match_history) == 0:
            while i < len(joueurs_tries) - 1:
                j1 = joueurs_tries[i]
                j2 = joueurs_tries[i + 1]
                key = tuple(sorted([j1.national_id, j2.national_id]))
                if key not in match_history:
                    matchs.append(Match(j1.national_id, j2.national_id))
                    match_history.add(key)
                i += 2
        else:
            players_with_match = []
            while i < len(joueurs_tries) - 1:
                j1 = joueurs_tries[i]
                j2 = None
                if j1.national_id not in players_with_match:
                    for j in range(i + 1, len(joueurs_tries) - 1):
                        j_potentiel = joueurs_tries[j]
                        key = tuple(sorted([j1.national_id, j_potentiel.national_id]))
                        if key not in match_history:
                            j2 = j_potentiel
                            break
                    if not j2:
                        """prendre le premier ou dernier qui n est pas dans  player with match"""
                        for j in joueurs_tries:
                            if (
                                j.national_id != j1.national_id
                                and j.national_id not in players_with_match
                            ):
                                j2 = j
                                key = tuple(
                                    sorted([j1.national_id, j_potentiel.national_id])
                                )
                                break

                    matchs.append(Match(j1.national_id, j2.national_id))
                    match_history.add(key)
                    players_with_match.append(j1.national_id)
                    players_with_match.append(j2.national_id)
        return matchs

    def jouer_round_suivant(self, tournament):
        if tournament.current_round_number >= tournament.number_of_round:
            print(" Tous les rounds ont déjà été joués.")
            return

        round_name = f"Round {tournament.current_round_number + 1}"
        nouveau_round = Round(round_name)
        nouveau_round.matches = self.generer_paires(
            tournament.players, tournament.match_history
        )

        print(f"\n {round_name} — Saisie des résultats :")

        for match in nouveau_round.matches:
            joueur1 = tournament.get_player_by_id(match.player1_id)
            joueur2 = tournament.get_player_by_id(match.player2_id)

            print(
                f"\nMatch : {joueur1.first_name} {joueur1.last_name} vs {joueur2.first_name} {joueur2.last_name}"
            )

            # Saisie et validation des scores
            while True:
                try:
                    s1 = float(input(f"Score de {joueur1.last_name} : "))
                    s2 = float(input(f"Score de {joueur2.last_name} : "))
                    if (s1, s2) not in [(1.0, 0.0), (0.0, 1.0), (0.5, 0.5)]:
                        raise ValueError(
                            "Format non valide (accepte seulement 1-0, 0-1 ou 0.5-0.5)"
                        )
                    break
                except ValueError as e:
                    print(e)

            match.score1 = s1
            match.score2 = s2
            joueur1.score += s1
            joueur2.score += s2

        nouveau_round.end_round()
        tournament.rounds.append(nouveau_round)
        tournament.current_round_number += 1

        tournament.save_to_file("data/tournoi_auto.json")

        print(f"\n {round_name} terminé et sauvegardé.")
        print("\n Scores des joueurs :")
        for joueur in tournament.players:
            print(
                f"{joueur.first_name} {joueur.last_name} ({joueur.national_id}) : {joueur.score} points"
            )

        if tournament.current_round_number >= tournament.number_of_round:
            print("\n Le tournoi est terminé !")

            # Trie les joueurs par score décroissant
            joueurs_tries = sorted(
                tournament.players, key=lambda j: j.score, reverse=True
            )
            gagnant = joueurs_tries[0]

            print(
                f"\n Félicitations à {gagnant.first_name} {gagnant.last_name}  le grand gagnant  !"
            )
