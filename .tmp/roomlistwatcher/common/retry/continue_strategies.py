# -*- coding: utf-8 -*-

import abc


class ContinueStrategy(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def should_continue(self, attempt):

        """
        Parameters
        ----------
        attempt : roomlistwatcher.common.retry.attempt.Attempt

        Returns
        -------
        bool
            True if the client should continue and False otherwise.
        """

        pass


class AfterResult(ContinueStrategy):

    def __init__(self, predicate):

        """
        Parameters
        ----------
        predicate : collections.Callable
            The predicate must accept one argument and return a
            Boolean.
        """

        self._predicate = predicate

    def should_continue(self, attempt):
        result = self._predicate(attempt.result)
        return result

    def __repr__(self):
        repr_ = '{}(predicate={})'
        return repr_.format(self.__class__.__name__, self._predicate)
