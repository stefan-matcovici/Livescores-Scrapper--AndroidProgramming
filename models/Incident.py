class Incident:
    def __init__(self, minute, home_player, away_player, score, home_event, away_event):
        self.minute = minute
        self.home_player = home_player
        self.away_player = away_player
        self.score = score
        self.home_event = home_event
        self.away_event = away_event

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)
