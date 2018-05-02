from pyfcm import FCMNotification
import pyrebase

from RepeatedTimer import RepeatedTimer
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


def do_something():
    print("Doing stuff...")


if __name__ == "__main__":
    # push_service = FCMNotification(api_key="AAAAKVHFP8Q:APA91bHUbwf_vT3Pa99DlONXqsEBtIGmiSqbpaX4vwUCkrQdBgwF_yK6Bn6Q2QEOEvQGTg0i-np5yy-rykHVXKnkIxAykUZErs-huNy2VP7IAF0SepoFhSVzafu-QI9BEe8It-bp4boM")
    #
    # message_title = "Uber update"
    # message_body = "Hi john, your customized news for today is ready"
    #
    #
    # result = push_service.notify_topic_subscribers(topic_name="news", message_body=message_body)
    # print(result)

    scrapper = Scrapper()
    match_id = "1-2747587"
    incidents = scrapper.get_event_info(
        "http://www.livescore.com/soccer/champions-league/semi-finals/real-madrid-vs-bayern-munich/1-2747587/")

    for incident in incidents:
        db.child(match_id).child(incident.minute).set(incident.__dict__)

    scrapper.close()

    # repeated_timer = RepeatedTimer(1, do_something)
