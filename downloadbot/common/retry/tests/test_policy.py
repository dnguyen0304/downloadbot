# -*- coding: utf-8 -*-

import json

import mock
from nose.tools import (assert_equal,
                        assert_false,
                        assert_greater,
                        assert_in,
                        assert_true,
                        raises)

from .. import (PolicyBuilder,
                Topic,
                exceptions,
                stop_strategies,
                wait_strategies)
from .. import policy
from downloadbot import common


def test_BaseAttemptEvent_do_to_json_default_serializer():

    class Foo(object):
        pass
    data = {'foo': Foo()}
    policy.BaseAttemptEvent.do_to_json(data=data)


def test_attempt_started_event_to_json_names():

    event = policy.AttemptStartedEvent(attempt_number=None)
    assert_in('topic_name', json.loads(event.to_json()))
    assert_in('arguments', json.loads(event.to_json()))


def test_attempt_started_event_to_json_arguments_names():

    event = policy.AttemptStartedEvent(attempt_number=None)
    assert_in('attempt_number', json.loads(event.to_json())['arguments'])


def test_attempt_completed_event_to_json_names():

    event = policy.AttemptStartedEvent(attempt_number=None)
    assert_in('topic_name', event.to_json())
    assert_in('arguments', json.loads(event.to_json()))


def test_attempt_completed_event_to_json_arguments_names():

    event = policy.AttemptCompletedEvent(result=None,
                                         exception=None,
                                         next_wait_time=None,
                                         was_successful=None,
                                         should_continue=None,
                                         should_stop=None,
                                         should_wait=None)
    assert_in('result', json.loads(event.to_json())['arguments'])
    assert_in('exception', json.loads(event.to_json())['arguments'])
    assert_in('next_wait_time', json.loads(event.to_json())['arguments'])
    assert_in('was_successful', json.loads(event.to_json())['arguments'])
    assert_in('should_continue', json.loads(event.to_json())['arguments'])
    assert_in('should_stop', json.loads(event.to_json())['arguments'])
    assert_in('should_wait', json.loads(event.to_json())['arguments'])


class MockException(Exception):
    pass


class MockService(object):

    def __init__(self):
        self.call_count = 0

    def call(self):
        self.call_count += 1

    def call_and_raise(self):
        self.call_count += 1
        if self.call_count == 1:
            raise MockException

    def call_and_return(self):
        self.call_count += 1
        return 'foo'


class TestPolicy(object):

    def __init__(self):
        self.service = None
        self.messaging_broker = None

    def setup(self):
        self.service = MockService()
        self.messaging_broker = common.event.messaging.Broker(
            observable_class=common.event.notifiables.Observable)
        self.messaging_broker.create_topic(name=Topic.ATTEMPT_STARTED.name)
        self.messaging_broker.create_topic(name=Topic.ATTEMPT_COMPLETED.name)

    def test_execute_successful_attempt_stops(self):
        policy = PolicyBuilder() \
            .with_stop_strategy(stop_strategies.AfterNever()) \
            .with_wait_strategy(wait_strategies.Fixed(wait_time=0)) \
            .build()
        policy.execute(callable=self.service.call)
        assert_equal(self.service.call_count, 1)

    def test_execute_successful_attempt_does_not_wait(self):
        _sleep = mock.Mock()
        policy = PolicyBuilder() \
            .with_stop_strategy(stop_strategies.AfterNever()) \
            .with_wait_strategy(wait_strategies.Fixed(wait_time=None)) \
            .build()
        policy.execute(callable=self.service.call, _sleep=_sleep)
        assert_false(_sleep.called)

    def test_execute_successful_attempt_returns_result(self):
        policy = PolicyBuilder() \
            .with_stop_strategy(stop_strategies.AfterNever()) \
            .with_wait_strategy(wait_strategies.Fixed(wait_time=0)) \
            .build()
        result = policy.execute(callable=self.service.call_and_return)
        assert_equal(result, 'foo')

    @raises(MockException)
    def test_execute_failed_attempt_raises_exception(self):
        policy = PolicyBuilder() \
            .with_stop_strategy(stop_strategies.AfterNever()) \
            .with_wait_strategy(wait_strategies.Fixed(wait_time=0)) \
            .build()
        policy.execute(callable=self.service.call_and_raise)

    def test_execute_failed_attempt_waits(self):
        _sleep = mock.Mock()
        policy = PolicyBuilder() \
            .with_stop_strategy(stop_strategies.AfterAttempt(maximum_attempt=2)) \
            .with_wait_strategy(wait_strategies.Fixed(wait_time=0)) \
            .continue_on_exception(MockException) \
            .build()
        policy.execute(callable=self.service.call_and_raise, _sleep=_sleep)
        assert_true(_sleep.called)

    def test_execute_continue_on_exception(self):
        policy = PolicyBuilder() \
            .with_stop_strategy(stop_strategies.AfterAttempt(maximum_attempt=2)) \
            .with_wait_strategy(wait_strategies.Fixed(wait_time=0)) \
            .continue_on_exception(MockException) \
            .build()
        policy.execute(callable=self.service.call_and_raise)
        assert_greater(self.service.call_count, 1)

    def test_execute_continue_if_result(self):
        policy = PolicyBuilder() \
            .with_stop_strategy(stop_strategies.AfterAttempt(maximum_attempt=2)) \
            .with_wait_strategy(wait_strategies.Fixed(wait_time=0)) \
            .continue_if_result(predicate=lambda x: x == 'foo') \
            .build()
        try:
            policy.execute(callable=self.service.call_and_return)
        except exceptions.MaximumRetry:
            assert_greater(self.service.call_count, 1)

    def test_execute_with_attempt_started_hook(self):
        predicate = mock.Mock()
        policy = PolicyBuilder() \
            .with_stop_strategy(stop_strategies.AfterNever()) \
            .with_wait_strategy(wait_strategies.Fixed(wait_time=0)) \
            .with_messaging_broker(self.messaging_broker) \
            .with_hook(predicate=predicate, topic=Topic.ATTEMPT_STARTED) \
            .build()
        policy.execute(callable=self.service.call_and_return)
        assert_equal(predicate.call_count, 1)

    def test_execute_with_attempt_completed_hook(self):
        predicate = mock.Mock()
        policy = PolicyBuilder() \
            .with_stop_strategy(stop_strategies.AfterNever()) \
            .with_wait_strategy(wait_strategies.Fixed(wait_time=0)) \
            .with_messaging_broker(self.messaging_broker) \
            .with_hook(predicate=predicate, topic=Topic.ATTEMPT_COMPLETED) \
            .build()
        policy.execute(callable=self.service.call_and_return)
        assert_equal(predicate.call_count, 1)
