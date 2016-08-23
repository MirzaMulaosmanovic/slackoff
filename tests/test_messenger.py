import pytest_mock
from slackoff import messagequeue
from rx.subjects import Subject
from rx.concurrency import NewThreadScheduler

def test_messenger_stream():
    assert type(messagequeue.queue) == Subject

def test_messenger_scheduler():
    assert type(messagequeue.scheduler) == NewThreadScheduler

def test_on_next(mocker):
    mocker = pytest_mock.MockFixture()
    mocker.spy(messagequeue.queue, 'on_next')
    messagequeue.send_message("test message")
    assert messagequeue.queue.on_next.call_count == 1
