# -*- coding: utf-8 -*-

import time


class Attempt(object):

    def __init__(self,
                 number,
                 was_successful,
                 result,
                 exception,
                 first_attempt_start_time):

        self.number = number
        self.was_successful = was_successful
        self.result = result
        self.exception = exception
        self.first_attempt_start_time = first_attempt_start_time

    @classmethod
    def first(cls, _get_now_in_seconds=time.time):

        """
        Parameters
        ----------
        _get_now_in_seconds : collections.Callable
            Used internally. Defaults to time.time.
        """

        attempt = cls(number=0,
                      was_successful=None,
                      result=None,
                      exception=None,
                      first_attempt_start_time=_get_now_in_seconds())
        return attempt

    def next(self):
        attempt = self.__class__(
            number=self.number + 1,
            was_successful=None,
            result=None,
            exception=None,
            first_attempt_start_time=self.first_attempt_start_time)
        return attempt

    def __repr__(self):
        repr_ = ('{}('
                 'number={}, '
                 'was_successful={}, '
                 'result={}, '
                 'exception={}, '
                 'first_attempt_start_time={})')
        return repr_.format(self.__class__.__name__,
                            self.number,
                            self.was_successful,
                            self.result,
                            self.exception,
                            self.first_attempt_start_time)
