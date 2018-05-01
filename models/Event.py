import json
import re

class Event:
    def __init__(self, id, homeTeam, awayTeam, homeScore, awayScore, score_link):
        self.id = id[id.index('-')+1:]
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.homeScore = homeScore
        self.awayScore = awayScore
        self.scoreLink = score_link

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)
