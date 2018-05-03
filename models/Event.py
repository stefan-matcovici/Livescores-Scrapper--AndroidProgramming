import json
import re


class Event:
    def __init__(self, id, homeTeam, awayTeam, homeScore, awayScore, score_link, header):
        self.id = id[id.index('-') + 1:]
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.homeScore = homeScore
        self.awayScore = awayScore
        self.scoreLink = score_link
        self.header = header

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)

    def __dict__(self):
        return {
            "id": self.id,
            "homeTeam": self.homeTeam,
            "awayTeam": self.awayTeam,
            "homeScore": self.homeScore,
            "awayScore": self.awayScore,
            "scoreLink": self.scoreLink,
            "header": self.header.__dict__
        }
