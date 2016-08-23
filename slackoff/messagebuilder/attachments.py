import json
import random

class Attachments(object):
    """Attachments object use to build the attachments attribute of a Slack message
    """
    def __init__(self):
        self.attachment_list = []

    def add_attachment(self, attachment):
        """
        Add the given attachment
        """
        self.attachment_list.append(attachment.__dict__)

    def get_json(self):
        """
        get the attachments json
        """
        return self.__str__()

    def __str__(self):
        return json.dumps(self.attachment_list)

class Attachment(object):
    """Represents a single attachment used to build the Attachments
    attribute of a Slack message
    """
    def __init__(self):
        self.title = ''
        self.title_link = ''
        self.color = ''
        self.ts = ''
        self.thumb_url = ''

    def __str__(self):
        return json.dumps(self.__dict__)

    def use_random_color(self):
        """
        use a random color for the attachment
        """
        color = ''.join([random.choice('0123456789ABCDEF') for x in range(6)])

        self.color = '#' + color
