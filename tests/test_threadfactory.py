import pytest_mock
from slackoff import threadfactory
import threading

def test_thread_factory_threads():
    threadfactory.default_factory(None)
    assert len(threadfactory.threads) == 1

def test_default_thread_factory():
    assert type(threadfactory.default_factory(None)) == threading.Thread

def test_default_thread_factory_daemon():
    thread = threadfactory.default_factory(None)
    assert thread.daemon
    