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


def notify_about_event(event):
    match_id = event.id
    incidents = scrapper.get_event_info(event.scoreLink)

    subscriptions = db.child("subscriptions").get()

    for subscription in subscriptions.each():
        user_id = subscription.key()
        match_minute = subscription.val()
        for user_sub_match_id in match_minute.keys():
            minute = match_minute[user_sub_match_id]
            current_minute = minute
            if user_sub_match_id == match_id:
                incidents_to_push = list(filter(lambda incident: int(incident.minute[:-1]) > int(minute), incidents))
                print(incidents_to_push)
                for incident in incidents_to_push:
                    message_title = "Something happened at " + incident.minute
                    message_body = incident.home_event + " " + incident.home_player + " : " + incident.away_event + incident.away_player

                    result = push_service.notify_single_device(user_id, message_title=message_title,
                                                               message_body=message_body)
                    current_minute = int(incident.minute[:-1])
            db.child("subscriptions").child(user_id).child(user_sub_match_id).set(current_minute)


if __name__ == "__main__":
    push_service = FCMNotification(
        api_key="AAAAKVHFP8Q:APA91bHUbwf_vT3Pa99DlONXqsEBtIGmiSqbpaX4vwUCkrQdBgwF_yK6Bn6Q2QEOEvQGTg0i-np5yy-rykHVXKnkIxAykUZErs-huNy2VP7IAF0SepoFhSVzafu-QI9BEe8It-bp4boM")

    scrapper = Scrapper()

    live_events = scrapper.get_live_events()

    scrapper.close()

    # repeated_timer = RepeatedTimer(1, do_something)
