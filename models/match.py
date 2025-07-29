class Match:
    def __init__(self, player1_id, player2_id, score1=0.0, score2=0.0):
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.score1 = score1
        self.score2 = score2

    def to_list(self):
        return [[self.player1_id, self.score1], [self.player2_id, self.score2]]

    @classmethod
    def creation_match_from_list(cls, data):
        player1_data, player2_data = data
        return cls(
            player1_id=player1_data[0],
            score1=player1_data[1],
            player2_id=player2_data[0],
            score2=player2_data[1],
        )
