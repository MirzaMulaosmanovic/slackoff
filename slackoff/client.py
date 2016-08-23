import time
import logging
from slackclient import SlackClient
from slackoff import messagequeue
from slackoff import threadfactory
from slackoff import settings
from .models import factory
from .plugins import loader

class SlackOff(object):
    def __init__(self, token):
        self.client = SlackClient(token)

    def run(self, as_daemon=False):
        """
        Start SlackOff on a new thread.
        
        Example:
        run(True)
        run(False)
        run()

        Keyword arguments:
        as_daemon -- {bool} [Optional] Start SlackOff on a daemon thread
        """
        loader.load_plugins(settings)

        t = threadfactory.default_factory(target=self.__run_slack_client, name="SlackOff", as_daemon=as_daemon)
        t.setDaemon(as_daemon)
        t.start()

    def send_message(self, channel, text="", attachments=None):
        self.client.api_call("chat.postMessage", parse="full", as_user=True, channel=channel, text=text, attachments=attachments)

    def __run_slack_client(self):
        """
        Runs the SlackClient and adds each item from the RTM to the messagequeue
        """

        logging.debug("Starting SlackOff")

        # Get some info about the bot and add it to the messagequeue in the case
        # that any plugin needs some more info about the bot
        botInfo=factory.create_from(self.client.api_call("auth.test"), self.client)
        messagequeue.send_message(botInfo)

        if self.client.rtm_connect():
            while True:
                data = self.client.rtm_read()
                if data:
                    logging.debug(data)
                    model = factory.create_from(data, bot_info=botInfo, client=self)
                    if model is not None:
                        messagequeue.send_message(model)
                    else:
                        messagequeue.send_message(data)
                time.sleep(1)
        else:
            logging.error("Connection Failed, invalid token?")
