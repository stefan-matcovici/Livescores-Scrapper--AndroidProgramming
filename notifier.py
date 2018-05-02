from pyfcm import FCMNotification

if __name__ == "__main__":

    push_service = FCMNotification(api_key="AAAAKVHFP8Q:APA91bHUbwf_vT3Pa99DlONXqsEBtIGmiSqbpaX4vwUCkrQdBgwF_yK6Bn6Q2QEOEvQGTg0i-np5yy-rykHVXKnkIxAykUZErs-huNy2VP7IAF0SepoFhSVzafu-QI9BEe8It-bp4boM")

    message_title = "Uber update"
    message_body = "Hi john, your customized news for today is ready"

    result = push_service.notify_topic_subscribers(topic_name="news", message_body=message_body)
    print(result)
