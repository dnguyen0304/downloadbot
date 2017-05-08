# -*- coding: utf-8 -*-

from . import continue_strategies
from .policy import Policy
from clare import event_driven


class HookAdapter(event_driven.interfaces.INotifyable):

    def __init__(self, predicate):
        self._predicate = predicate

    def notify(self, event):
        self._predicate(event)

    def __repr__(self):
        repr_ = '{}(predicate={})'
        return repr_.format(self.__class__.__name__, self._predicate)


class PolicyBuilder(object):

    def __init__(self,
                 stop_strategies=None,
                 wait_strategy=None,
                 continue_strategies=None,
                 handled_exceptions=None,
                 messaging_broker=None):

        """
        Policies must have the following:
          - exactly 1 wait strategy
        Policies should have the following:
          - at least 1 stop strategy
        Policies may have the following:
          - 0 or more exceptions on which to continue
          - 0 or more results on which to continue
          - 0 or more hooks
          - at most 1 messaging brokers

        A "successful" attempt is understood as one where an exception
        was not thrown within the callable.

        Parameters
        ----------
        stop_strategies : iterable of IStopStrategy
            Defaults to an empty list.
        wait_strategy : IWaitStrategy
            Defaults to None.
        continue_strategies : iterable of IContinueStrategy
            Continuing takes precedence over stopping after successful
            attempts. In other words, it "overrides" those cases.
            Defaults to an empty list.
        handled_exceptions : iterable of Exception
            Defaults to an empty tuple.
        messaging_broker : clare.event_driven.messaging.Broker
            See the method docstring for more details. Defaults to None.
        """

        self._stop_strategies = stop_strategies or list()
        self._wait_strategy = wait_strategy
        self._continue_strategies = continue_strategies or list()
        self._handled_exceptions = handled_exceptions or tuple()
        self._messaging_broker = messaging_broker

    def with_stop_strategy(self, stop_strategy):
        self._stop_strategies.append(stop_strategy)
        return self

    def with_wait_strategy(self, wait_strategy):
        self._wait_strategy = wait_strategy
        return self

    def _with_continue_strategy(self, continue_strategy):
        self._continue_strategies.append(continue_strategy)
        return self

    def continue_on_exception(self, exception):
        self._handled_exceptions += (exception,)
        return self

    def continue_if_result(self, predicate):
        continue_strategy = continue_strategies.AfterResult(predicate=predicate)
        return self._with_continue_strategy(continue_strategy)

    def with_messaging_broker(self, messaging_broker):
        self._messaging_broker = messaging_broker
        return self

    def with_hook(self, predicate, topic):

        """
        You must provide a messaging broker before creating a hook.

        For the Attempt Started event, the hook will be executed
        before each attempt. It receives a serialized object
        containing metadata about the current attempt number
        ("attempt_number").

        For the Attempt Completed event, the hook will be executed
        after each attempt. It receives a serialized object
        containing metadata about the returned result ("result"), the
        thrown exception ("exception"), and the next wait time
        ("next_wait_time").

        These hooks are read-only and therefore cannot affect the
        runtime behavior of the Policy.

        Parameters
        ----------
        predicate : collections.Callable
            The predicate must accept one argument of type str.
        topic : enum.Enum
        """

        # TODO (duy): Creating a hook without first providing a
        # messaging broker should not be possible.
        hook_adapter = HookAdapter(predicate=predicate)
        self._messaging_broker.subscribe(subscriber=hook_adapter,
                                         topic_name=topic.name)
        return self

    def build(self):
        retry_policy = Policy(stop_strategies=self._stop_strategies,
                              wait_strategy=self._wait_strategy,
                              continue_strategies=self._continue_strategies,
                              handled_exceptions=self._handled_exceptions,
                              messaging_broker=self._messaging_broker)
        return retry_policy
