#!flask/bin/python

from flask import Flask, request, jsonify
from flask_request_params import bind_request_params
from scrapper import Scrapper

app = Flask(__name__)
app.before_request(bind_request_params)

scrapper = Scrapper()

@app.route('/<sport>/live_events', methods=['GET'])
def liveEvents(sport):
    return jsonify([x.__dict__ for x in scrapper.get_live_events(sport)])


@app.route('/commentaries', methods=['POST'])
def commentaries():
    return jsonify([x.__dict__ for x in scrapper.get_event_commentaries(request.json)])


@app.route('/<sport>/international_competitions', methods=['GET'])
def international_competitions(sport):
    return jsonify([x.__dict__ for x in scrapper.get_international_competitions(sport)])


@app.route('/international_events', methods=['POST'])
def events():
    print(request.get_json()) 
    return jsonify([x.__dict__ for x in scrapper.get_international_competition_events(request.get_json(force=True)["link"])])

@app.route('/stop', methods=['POST'])
def stop(sport):
    return ""
if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=80)
