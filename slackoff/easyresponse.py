from slackoff import messagequeue
from slackoff.models.model import Message

def respond_to(text=""):
    """
    Subscribes the decorated function to Message that match the given text
    The function will be observed on its own thread.

    Example:
    @respond_to(str)

    Keyword arguments:
    text -- {str} [Optional] Filter the subscription to 
    to messages of the given text
    """
    def func_wrapper(func):
        messagequeue.queue.filter(lambda x:isinstance(x, Message) and x.text == text).observe_on(messagequeue.scheduler).subscribe(func)
        return func
    return func_wrapper
