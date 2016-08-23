import importlib
import logging 
from slackoff import settings

def load_plugins(settings=None):
    """load the plugins from the given settings
    """
    if settings is not None:
        for plugin in settings.plugins:
            try:
                importlib.import_module(".plugins." + plugin, "slackoff")
            except Exception as ex:
                logging.debug("Error loading plugin " + plugin +" "+ str(ex))