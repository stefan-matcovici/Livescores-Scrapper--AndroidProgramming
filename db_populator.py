import copy

import pyrebase
import logging
import sys

log = logging.getLogger(__name__)
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
out_hdlr.setLevel(logging.INFO)
log.addHandler(out_hdlr)
log.setLevel(logging.INFO)

from scrapper import Scrapper

config = {
    "apiKey": "AIzaSyAmetdoF4mAKT9FzpjMcK58D2gA7mKgUGw",
    "authDomain": "tppa-sport-scores.firebaseapp.com",
    "databaseURL": "https://tppa-sport-scores.firebaseio.com",
    "projectId": "tppa-sport-scores",
    "storageBucket": "tppa-sport-scores.appspot.com",
    "messagingSenderId": "177465540548"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
scrapper = Scrapper()


def get_competition_events(competition_name):
    competitions = db.child("competitions").get()
    for competition in competitions.each():
        if competition.key() == competition_name:
            print(competition)


def add_events_to_competition(competition, ref):

    events = scrapper.get_competition_events(competition.link)
    log.info("{} events to push further".format(len(events)))

    if len(events) == 0:
        ref.remove()
    else:
        for event in events[:2]:
            log.info("{} vs {}".format(event.homeTeam, event.awayTeam))
            base_ref = copy.deepcopy(ref)
            base_ref.child("events").push(event.to_dict())
            # if not event.scoreLink:
            #     log.info("No commentaries")
            # else:
            #     commentaries = scrapper.get_event_commentaries(event.scoreLink)
            #     log.info("{} commentaries to push further".format(len(commentaries)))
            #     if len(commentaries) == 0:
            #         log.info("No commentaries")
            #     else:
            #         for commentary in commentaries:
            #             base_ref = copy.deepcopy(ref)
            #             base_ref.child(competition_id).child("events").child(event_id).child("commentaries").push(
            #                 commentary.__dict__)


def add_competitions(sport):
    # clear
    db.child("competitions").child(sport).remove()

    # update
    competitions = scrapper.get_international_competitions(sport)

    for competition in competitions:
        log.info("Starting pushing " + competition.name)
        competition_id = db.child("competitions").child(sport).push(competition.__dict__)

        events = scrapper.get_competition_events(competition.link)
        log.info("{} events to push further".format(len(events)))

        if len(events) == 0:
            db.child("competitions").child(sport).child(competition_id["name"]).remove()
        else:
            for event in events:
                log.info("{} vs {}".format(event.homeTeam, event.awayTeam))
                db.child("competitions").child(sport).child(competition_id["name"]).child("events").push(event.to_dict())


if __name__ == "__main__":
    try:
        add_competitions("soccer")
        # add_competitions("basketball")
        # add_competitions("tennis")
    except Exception as e:
        print(e)
    finally:
        scrapper.close()
    # get_competition_events("Champions League")
