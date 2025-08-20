class Player:

    def __init__(self, last_name, first_name, birth_date, national_id, score=0.0):
        """Initialise un joueur avec ses informations"""

        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.national_id = national_id
        self.score = score

    def to_dict(self):
        """Convertit le joueur en dictionnaire pour le sauvegarder dans un fichier JSON"""

        return {
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "national_id": self.national_id,
            "score": self.score,
        }

    @classmethod
    def creation_joueur_from_dict(cls, data):
        """Crée un objet Player à partir d'un dictionnaire"""

        player = cls(
            data["last_name"],
            data["first_name"],
            data["birth_date"],
            data["national_id"],
        )

        player.score = data.get("score", 0.0)
        return player
