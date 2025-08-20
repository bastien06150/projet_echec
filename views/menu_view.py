class MainMenuView:

    @staticmethod
    def display_main_menu():
        """Affiche le menu principal"""

        while True:
            print("\n==== MENU PRINCIPAL ====")
            print("1. Gérer les joueurs")
            print("2. Gérer les tournois")
            print("3. Afficher les rapports")
            print("4. Lancement du round")
            print("5. Quitter")

            choice = input("Votre choix : ").strip()
            if choice in {"1", "2", "3", "4", "5"}:
                return choice

            print("Entrée invalide. Veuillez choisir 1, 2, 3, 4 ou 5 ")

    @staticmethod
    def display_player_menu():
        """Affiche le sous-menu pour gérer les joueurs"""

        print("\n--- Menu Joueurs ---")
        print("1. Ajouter un joueur")
        print("2. Liste des joueurs")
        print("3. Retour")
        return input("Votre choix : ").strip()

    @staticmethod
    def prompt_tournament_path():
        return input("Chemin du tournoi existant : ").strip()

    @staticmethod
    def show_file_not_found():
        print("Fichier introuvable.")

    @staticmethod
    def show_exit_message():
        print("Fin du programme.")

    @staticmethod
    def show_invalid_choice():
        print("Choix invalide.")
