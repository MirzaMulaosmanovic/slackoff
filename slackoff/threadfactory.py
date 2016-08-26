import threading

def default_factory(target, name=None, as_daemon=True, args=None):
    """
    default thread factory, used to create threads as daemon
    """
    t = threading.Thread(target=target, name=name, args=args or [])
    t.setDaemon(as_daemon)
    return t
    