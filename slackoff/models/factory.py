import logging
from slackoff.models import model

def handle_unknown_type(data):
    """
    Log the unknown type and return None
    """
    logging.error("Unknown Type")
    logging.error(data)
    return None

def create_from(data, bot_info=None, client=None):
    """
    Create a model from the given data
    """
    if isinstance(data, list):
        return create_from_dict(data[0], bot_info, client)
    if isinstance(data, dict):
        return create_from_dict(data, bot_info, client)

    handle_unknown_type(data)

def get_model_from_type(data, bot_info=None, client=None):
    """
    get a model based on its type
    """
    model_type = data['type']

    if model_type == 'message':
        if 'subtype' in data:
            if data['subtype'] == 'bot_message':
                return model.BotMessage(data, bot_info, client)
        return model.Message(data, bot_info, client)

    if model_type == 'file_shared':
        return model.FileShared(data, bot_info, client)

    if model_type == 'presence_change':
        return model.PresenceChange(data, bot_info, client)

    if model_type == 'user_typing':
        return model.UserTyping(data, bot_info, client)

    if model_type == 'reconnect_url':
        return model.ReconnectUrl(data, bot_info, client)

    if model_type == 'hello':
        return None

    handle_unknown_type(data)

def create_from_dict(data, bot_info=None, client=None):
    """
    create a model from the given dict
    """
    if 'type' in data:
        return get_model_from_type(data, bot_info, client)

    if 'reply_to' in data and 'ok' in data:
        return None

    if 'user_id' in data and 'user' in data:
        return model.BotInfo(data, bot_info, client)

    handle_unknown_type(data)
