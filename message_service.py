from twilio.rest import Client
from decouple import config

SSID = config("TWILO_SSID")
AUTH = config("TWILO_AUTH_TOKEN")
FROM_NUMBER = config("TWILO_PHONE_NUMBER")
TO_NUMBER = config("DEST_PHONE_NUMBER")

client = Client(SSID, AUTH)

def sendMessage(message_body: str):
    '''Allows you to send messages to a particular phone number'''
    message = client.messages.create(from_=FROM_NUMBER, body=message_body, to=TO_NUMBER)
    return message.sid


# if __name__ == "__main__":
    sendMessage("Python Message Service Test:\n\n Service is up!")