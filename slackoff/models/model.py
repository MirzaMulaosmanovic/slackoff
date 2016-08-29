
class BaseSlackModel(object):
    """
    Base class for all SlackModel classes
    """
    def __init__(self, data, bot_info, client):
        self.data = data
        self.bot_info = bot_info
        self.client = client

    def get_bot_id(self):
        """
        get the user_id of the bot that we are using
        """
        if 'user_id' in self.bot_info:
            return self.bot_info['user_id']

    def get_bot_username(self):
        """
        get the username of the bot that we are using
        """
        if 'user' in self.bot_info:
            return self.bot_info['user']

    def get_client(self):
        """
        get the SlackClient from which the model originated
        """
        return self.client

    def __str__(self):
        return str(self.data)

class FileShared(BaseSlackModel):
    def __init__(self, data, bot_info, client):
        super(Message, self).__init__(data, bot_info=bot_info, client=client)

class Message(BaseSlackModel):
    def __init__(self, data, bot_info, client):
        self.text = data['text']
        if 'user' in data:
            self.user = data['user']
        self.channel = data['channel']
        if 'team' in data:
            self.team = data['team']
        super(Message, self).__init__(data, bot_info=bot_info, client=client)

    def __str__(self):
        return self.text

class BotMessage(Message):
    def __init__(self, data, bot_info, client):
        self.username = data['username']
        self.channel = data['channel']
        if 'team' in data:
            self.team = data['team']
        self.user_team = data['user_team']
        self.bot_id = data['bot_id']
        super(BotMessage, self).__init__(data, bot_info=bot_info, client=client)

class UserTyping(BaseSlackModel):
    def __init__(self, data, bot_info, client):
        self.user = data['user']
        self.channel = data['channel']
        super(UserTyping, self).__init__(data, bot_info=bot_info, client=client)

class PresenceChange(BaseSlackModel):
    def __init__(self, data, bot_info, client):
        self.user = data['user']
        self.presence = data['presence']
        super(PresenceChange, self).__init__(data, bot_info=bot_info, client=client)

class ReconnectUrl(BaseSlackModel):
    def __init__(self, data, bot_info, client):
        self.url = data['url']
        super(ReconnectUrl, self).__init__(data, bot_info=bot_info, client=client)

class BotInfo(BaseSlackModel):
    def __init__(self, data, bot_info, client):
        self.url = data['url']
        self.team = data['team']
        self.user = data['user']
        self.team_id = data['team_id']
        self.user_id = data['user_id']
        super(BotInfo, self).__init__(data, bot_info=bot_info, client=client)
