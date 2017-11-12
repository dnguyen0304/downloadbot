# -*- coding: utf-8 -*-

import abc
import collections
import json
import sys
import time

import six

from . import exceptions
from .attempt import Attempt
from downloadbot.common import io
from downloadbot.common import utility


class Topic(utility.AutomatedEnum):
    ATTEMPT_STARTED = ()
    ATTEMPT_COMPLETED = ()


class BaseAttemptEvent(io.JsonSerializable, metaclass=abc.ABCMeta):

    @staticmethod
    def do_to_json(data):

        """
        Parameters
        ----------
        data : typing.Mapping
        """

        serialized = json.dumps(data, default=repr)
        return serialized


class AttemptStartedEvent(BaseAttemptEvent):

    topic = Topic.ATTEMPT_STARTED

    def __init__(self, attempt_number):

        """
        Parameters
        ----------
        attempt_number : int
        """

        self.arguments = collections.OrderedDict()
        self.arguments['attempt_number'] = attempt_number

    def to_json(self):
        data = collections.OrderedDict()
        data['topic_name'] = self.topic.name
        data['arguments'] = self.arguments

        serialized = self.do_to_json(data=data)
        return serialized

    def __repr__(self):
        repr_ = '{}(attempt_number={})'
        return repr_.format(self.__class__.__name__,
                            self.arguments['attempt_number'])


class AttemptCompletedEvent(BaseAttemptEvent):

    topic = Topic.ATTEMPT_COMPLETED

    def __init__(self,
                 result,
                 exception,
                 next_wait_time,
                 was_successful,
                 should_continue,
                 should_stop,
                 should_wait):

        """
        Parameters
        ----------
        result : typing.Any
        exception : Exception
        next_wait_time : float
        was_successful : bool
        should_continue : bool
        should_stop : bool
        should_wait : bool
        """

        self.arguments = collections.OrderedDict()
        self.arguments['result'] = result
        self.arguments['exception'] = exception
        self.arguments['next_wait_time'] = next_wait_time
        self.arguments['was_successful'] = was_successful
        self.arguments['should_continue'] = should_continue
        self.arguments['should_stop'] = should_stop
        self.arguments['should_wait'] = should_wait

    def to_json(self):
        data = collections.OrderedDict()
        data['topic_name'] = self.topic.name
        data['arguments'] = self.arguments

        serialized = self.do_to_json(data=data)
        return serialized

    def __repr__(self):
        repr_ = ('{}('
                 'result={}, '
                 'exception={}, '
                 'next_wait_time={}, '
                 'was_successful={}, '
                 'should_continue={}, '
                 'should_stop={}, '
                 'should_wait={})')
        return repr_.format(self.__class__.__name__,
                            self.arguments['result'],
                            self.arguments['exception'],
                            self.arguments['next_wait_time'],
                            self.arguments['was_successful'],
                            self.arguments['should_continue'],
                            self.arguments['should_stop'],
                            self.arguments['should_wait'])


class Policy(object):

    def __init__(self,
                 stop_strategies,
                 wait_strategy,
                 continue_strategies,
                 handled_exceptions,
                 messaging_broker):
        self._stop_strategies = stop_strategies
        self._wait_strategy = wait_strategy
        self._continue_strategies = continue_strategies
        self._handled_exceptions = handled_exceptions
        self._messaging_broker = messaging_broker

    def execute(self, callable, _sleep=time.sleep):

        """
        Parameters
        ----------
        callable : collections.Callable
        _sleep : collections.Callable
            Used internally. Defaults to time.sleep.
        """

        attempt = Attempt.first()

        while True:
            attempt = six.next(attempt)

            self._publish_attempt_started(attempt_number=attempt.number)

            try:
                attempt.result = callable()
            except self._handled_exceptions as handled_exception:
                attempt.was_successful = False
                attempt.exception = handled_exception
            else:
                attempt.was_successful = True

            should_continue = any(
                continue_strategy.should_continue(attempt=attempt)
                for continue_strategy
                in self._continue_strategies)

            for stop_strategy in self._stop_strategies:
                try:
                    stop_strategy.should_stop(attempt=attempt)
                except exceptions.MaximumRetry:
                    e = sys.exc_info()
                    e[1].message = 'There are no more allowable retries.'
                    should_stop = True
                    break
            else:
                should_stop = False

            should_wait = not attempt.was_successful and not should_stop
            wait_time = self._wait_strategy.compute_wait_time(attempt=attempt)

            self._publish_attempt_completed(result=attempt.result,
                                            exception=attempt.exception,
                                            next_wait_time=wait_time,
                                            was_successful=attempt.was_successful,
                                            should_continue=should_continue,
                                            should_stop=should_stop,
                                            should_wait=should_wait)

            if attempt.was_successful and not should_continue:
                break
            elif should_stop:
                raise six.reraise(*e)
            else:
                _sleep(wait_time)

        if attempt.was_successful:
            return attempt.result

    def _publish_attempt_started(self, attempt_number):
        if self._messaging_broker is not None:
            event = AttemptStartedEvent(attempt_number=attempt_number)
            self._messaging_broker.publish(event=event.to_json(),
                                           topic_name=event.topic.name)

    def _publish_attempt_completed(self,
                                   result,
                                   exception,
                                   next_wait_time,
                                   was_successful,
                                   should_continue,
                                   should_stop,
                                   should_wait):
        if self._messaging_broker is not None:
            event = AttemptCompletedEvent(result=result,
                                          exception=exception,
                                          next_wait_time=next_wait_time,
                                          was_successful=was_successful,
                                          should_continue=should_continue,
                                          should_stop=should_stop,
                                          should_wait=should_wait)
            self._messaging_broker.publish(event=event.to_json(),
                                           topic_name=event.topic.name)

    def __repr__(self):
        repr_ = ('{}('
                 'stop_strategies={}, '
                 'wait_strategy={}, '
                 'continue_strategies={}, '
                 'handled_exceptions={}, '
                 'messaging_broker={})')
        return repr_.format(self.__class__.__name__,
                            self._stop_strategies,
                            self._wait_strategy,
                            self._continue_strategies,
                            self._handled_exceptions,
                            self._messaging_broker)
