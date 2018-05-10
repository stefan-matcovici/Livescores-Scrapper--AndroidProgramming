class InternationalCompetition:
    def __init__(self, name, link):
        self.name = name
        self.link = link

    def __repr__(self):
        return "InternationalCompetition{name = " + self.name + ", link = " + self.link + "}"
