class Header:
    def __init__(self, competition, competition_link, stage, stage_link, date):
        self.competition = competition
        self.competitionLink = competition_link
        self.stage = stage
        self.stageLink = stage_link
        self.date = date

    def set_date(self, date):
        self.date = date

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)
