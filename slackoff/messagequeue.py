from rx.subjects import Subject
from rx.concurrency import NewThreadScheduler
from slackoff import threadfactory

queue = Subject()
# Use a new thread scheduler, this will ensure that subscriptions are non blocking
scheduler = NewThreadScheduler(thread_factory=threadfactory.default_factory)

def subscribe():
    """
    Subscribes the decorated function to all messages from the messagequeue.

    Example:
    @subscribe()
    """
    def func_wrapper(func):
        queue.observe_on(scheduler).subscribe(func)
        return func
    return func_wrapper

def subscribe_to(type_to_subscribe_to=None):
    """
    Subscribes the decorated function to messages of the given type.
    The function will be observed on its own thread.

    Example:
    @subscribe_to(str)
    @subscribe_to(int)

    Keyword arguments:
    type_to_subscribe_to -- {Type} [Optional] Filter the subscription to 
    to messages of the given Type
    """
    def func_wrapper(func):
        queue.filter(lambda x:isinstance(x, type_to_subscribe_to) or type_to_subscribe_to == None).observe_on(scheduler).subscribe(func)
        return func
    return func_wrapper

def send_message(data):
    """
    Adds the given data to the queue. Any subscribers who are not filtering
    will recieve the message. Subscribers who are filtering on type will only
    see the message if it is of the type they are filtering on.

    Example:
    send_message("Hello World!")
    """
    if data is not None:
        queue.on_next(data)
