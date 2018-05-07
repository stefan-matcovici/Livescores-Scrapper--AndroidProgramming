#!flask/bin/python

from flask import Flask, request, jsonify, json

from models.Event import Event
from models.Header import Header
from scrapper import Scrapper

app = Flask(__name__)

scrapper = Scrapper()


@app.route('/<sport>/live_events', methods=['GET'])
def liveEvents(sport):
    return jsonify([x.to_dict() for x in scrapper.get_live_events(sport)])


@app.route('/fake/<sport>/live_events', methods=['GET'])
def fakeLiveEvents(sport):
    events = []
    event1 = Event("id-1-2747587", "real madrid", "away team", "1", "0", "link",
                   Header("La liga", "link", "stage", "stage_link", "date"))
    event2 = Event("id-2-276543", "real madrid2", "away team2", "2", "0", "link",
                   Header("La liga2", "link2", "stage2", "stage_link2", "date"))
    events.append(event1)
    events.append(event2)
    return jsonify([x.to_dict() for x in events])


@app.route('/commentaries', methods=['POST'])
def commentaries():
    return json.dumps([x.__dict__ for x in scrapper.get_event_commentaries(request.get_json(force=True)["link"])])+"\n"


@app.route('/<sport>/international_competitions', methods=['GET'])
def international_competitions(sport):
    return jsonify([x.__dict__ for x in scrapper.get_international_competitions(sport)])


@app.route('/international_events', methods=['POST'])
def events():
    return jsonify([x.to_dict() for x in scrapper.get_competition_events(request.get_json(force=True)["link"])])


@app.route('/stop', methods=['POST'])
def stop(sport):
    return ""


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=80)
