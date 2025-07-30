class MainMenuView:

    @staticmethod
    def display_main_menu():
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
