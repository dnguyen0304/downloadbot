# -*- coding: utf-8 -*-

from . import continue_strategies
from .policy import Policy
from .. import event


class HookAdapter(event.notifiables.Notifyable):

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
        """

        self._stop_strategies = stop_strategies or list()
        self._wait_strategy = wait_strategy
        self._continue_strategies = continue_strategies or list()
        self._handled_exceptions = handled_exceptions or tuple()
        self._messaging_broker = messaging_broker

    def with_stop_strategy(self, stop_strategy):

        """
        Parameters
        ----------
        stop_strategy : clare.common.retry.stop_strategies.IStopStrategy
        """

        self._stop_strategies.append(stop_strategy)
        return self

    def with_wait_strategy(self, wait_strategy):

        """
        Parameters
        ----------
        wait_strategy : clare.common.retry.wait_strategies.IWaitStrategy
        """

        self._wait_strategy = wait_strategy
        return self

    def _with_continue_strategy(self, continue_strategy):

        """
        Parameters
        ----------
        continue_strategy : clare.common.retry.continue_strategies.ContinueStrategy
        """

        self._continue_strategies.append(continue_strategy)
        return self

    def continue_on_exception(self, exception):

        """
        When the algorithm would normally stop due to an exception
        being thrown within the callable, continuing overrides that
        behavior.
        """

        self._handled_exceptions += (exception,)
        return self

    def continue_if_result(self, predicate):

        """
        When the algorithm would normally stop due to a successful
        attempt, continuing overrides that behavior.

        A "successful" attempt is understood as one where an exception
        was not thrown within the callable.

        Parameters
        ---------
        predicate : collections.Callable
            The predicate must accept one argument and return a Boolean.
        """

        continue_strategy = continue_strategies.AfterResult(predicate=predicate)
        return self._with_continue_strategy(continue_strategy)

    def with_messaging_broker(self, messaging_broker):

        """
        Parameters
        ----------
        messaging_broker : clare.common.event_driven.messaging.Broker
        """

        self._messaging_broker = messaging_broker
        return self

    def with_hook(self, predicate, topic):

        """
        You must provide a messaging broker before creating a hook.

        For the Attempt Started event, the hook will be executed
        before each attempt.

        For the Attempt Completed event, the hook will be executed
        after each attempt.

        Hooks receive a serialized object containing runtime metadata.
        They are also read-only and therefore cannot affect the runtime
        behavior of the Policy.

        Parameters
        ----------
        predicate : collections.Callable
            The predicate must accept one argument of type str and
            return a Boolean.
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
