import logging
import time
from datetime import date
from slackoff.messagequeue import subscribe_to
from slackoff.client import SlackOff
from slackoff.easyresponse import respond_to
from slackoff.models.model import Message, UserTyping, PresenceChange

logging.basicConfig(level=logging.DEBUG, format='%(threadName)-10s%(message)s')

# Create and run the SlackOff client
s = SlackOff('token goes here')
s.run()

# to respond to specific messages you can use the respond_to decorator
@respond_to("hello")
def say_hello(message):
    client = message.get_client()
    client.send_message(message.channel, text="Hello!")

# long running response do not block other subscriptions because
# each subscription (decorator) is executed on its own thread
@respond_to("hello")
def respond_slowly(message):
    time.sleep(5)
    client = message.get_client()
    client.send_message(message.channel, text="slowwww response")    

# sCalled when recieving a message
@subscribe_to(Message)
def subscribe_to_every_message(message):
    if "date" in message.text:
        client = message.get_client()
        client.send_message(message.channel, text=str(date.today()))

# called when a user is typing  
@subscribe_to(UserTyping)
def subscribe_to_every_user_typing(user_typing):
    client = user_typing.get_client()
    client.send_message(user_typing.channel, text="I see you typing")

# called when a users presence changes
@subscribe_to(PresenceChange)
def subscribe_to_every_presence_change(presence_change):
    if presence_change.presence == "active":
        client = presence_change.get_client()
        client.send_message(presence_change.user, text="Welcome Back!")