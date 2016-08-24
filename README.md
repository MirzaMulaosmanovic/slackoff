This is a batteries included Slack bot that supports concurrent messages/responses.

#### Usage
Run the client
```python
from slackoff.client import SlackOff

# Create and run the SlackOff client
s = SlackOff('token goes here')
s.run()

```

Reply to specific messages
```python
from slackoff.easyresponse import respond_to

# to respond to specific messages you can use the respond_to decorator
@respond_to("hello")
def say_hello(message):
    client = message.get_client()
    client.send_message(message.channel, text="Hello!")
```

Subscribe to a specific message type
```python
from datetime import date
from slackoff.messagequeue import subscribe_to
from slackoff.models.model import Message, UserTyping, PresenceChange

# Called when recieving a message
@subscribe_to(Message)
def subscribe_to_every_message(message):
    if "date" in message.text:
        client = message.get_client()
        client.send_message(message.channel, text=str(date.today()))


# Called when a users presence changes
@subscribe_to(PresenceChange)
def subscribe_to_every_presence_change(presence_change):
    if presence_change.presence == "active":
        client = presence_change.get_client()
        client.send_message(presence_change.user, text="Welcome Back!")
```
