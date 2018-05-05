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

images = {
    "goal": "https://firebasestorage.googleapis.com/v0/b/tppa-sport-scores.appspot.com/o/football.png?alt=media&token=1ceb91e2-04fb-401d-a9e4-5dcbb20b50c2",
    "yellowcard": "https://firebasestorage.googleapis.com/v0/b/tppa-sport-scores.appspot.com/o/cards.png?alt=media&token=b23cb14e-b3d3-48d8-bc40-ac6a0f9030e9"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()


def do_something():
    print("started job")
    live_events = scrapper.get_live_events("football")

    for event in live_events:
        if event.scoreLink:
            notify_about_event(event)

    scrapper.close()


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
                for incident in incidents_to_push:
                    if "goal" in incident.away_event or "goal" in incident.home_event:
                        message_title = incident.minute + "' " + event.homeTeam + " " + event.homeTeam + " : " + event.awayScore + " " + event.awayTeam
                        if "goal" in incident.home_event:
                            if "-" in incident.home_event:
                                type_of_goal = incident.home_event.split("-")[1]
                                if type_of_goal == "pen":
                                    message_body = incident.home_player + " from " + event.homeTeam + " has just scored from penalty"
                                elif type_of_goal == "own":
                                    message_body = incident.home_player + " from " + event.homeTeam + " has just scored an own goal"
                            else:
                                message_body = incident.home_player + " from " + event.homeTeam + " has just scored"
                        if "goal" in incident.away_event:
                            if "-" in incident.away_event:
                                type_of_goal = incident.away_event.split("-")[1]
                                if type_of_goal == "pen":
                                    message_body = incident.away_player + " from " + event.awayTeam + " has just scored from penalty"
                                elif type_of_goal == "own":
                                    message_body = incident.away_player + " from " + event.awayTeam + " has just scored an own goal"
                            else:
                                message_body = incident.away_player + " from " + event.awayTeam + " has just scored"
                    elif "card" in incident.away_event or "card" in incident.home_event:
                        message_title = "Someone got booked"
                        if "card" in incident.home_event:
                            message_body = incident.home_player + " from " + event.homeTeam + " was just booked with " + \
                                           incident.home_event.split("card")[0] + " card"
                        if "card" in incident.away_event:
                            message_body = incident.away_event + " from " + event.awayTeam + " was just booked with " + \
                                           incident.away_event.split("card")[0] + " card"

                    result = push_service.notify_single_device(user_id, message_title=message_title,
                                                               message_body=message_body,
                                                               message_icon=images[
                                                                   incident.home_event if incident.home_event != "empty" else incident.away_event]
                                                               )
                    print(result)
                    current_minute = int(incident.minute[:-1])
            db.child("subscriptions").child(user_id).child(user_sub_match_id).set(current_minute)


if __name__ == "__main__":
    push_service = FCMNotification(
        api_key="AAAAKVHFP8Q:APA91bHUbwf_vT3Pa99DlONXqsEBtIGmiSqbpaX4vwUCkrQdBgwF_yK6Bn6Q2QEOEvQGTg0i-np5yy-rykHVXKnkIxAykUZErs-huNy2VP7IAF0SepoFhSVzafu-QI9BEe8It-bp4boM")

    scrapper = Scrapper()
    live_events = scrapper.get_live_events("football")

    for event in live_events:
        print(event)
        if event.scoreLink:
            notify_about_event(event)

    scrapper.close()

    # repeated_timer = RepeatedTimer(1, do_something)
