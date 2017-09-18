# -*- coding: utf-8 -*-

from nose.tools import assert_false, assert_true

from .. import utility


class MockGetNowInSeconds(object):

    def __init__(self, start_time, next_time):

        """
        Parameters
        -------
        start_time : float
        next_time : float
        """

        self._start_time = start_time
        self._next_time = next_time

        self._call_count = 0

    @classmethod
    def greater_than(cls, duration, start_time):
        next_time = (duration * 2) + start_time
        get_now_in_seconds = cls(start_time=start_time, next_time=next_time)
        return get_now_in_seconds

    @classmethod
    def equal_to(cls, duration, start_time):
        next_time = (duration * 1) + start_time
        get_now_in_seconds = cls(start_time=start_time, next_time=next_time)
        return get_now_in_seconds

    @classmethod
    def less_than(cls, duration, start_time):
        next_time = (duration * 0) + start_time
        get_now_in_seconds = cls(start_time=start_time, next_time=next_time)
        return get_now_in_seconds

    def __call__(self):
        if self._call_count == 0:
            now = self._start_time
        else:
            now = self._next_time
        self._call_count += 1
        return now

    def __repr__(self):
        repr_ = '{}(start_time={}, next_time={})'
        return repr_.format(self.__class__.__name__,
                            self._start_time,
                            self._next_time)


class TestCountdownTimer(object):

    def __init__(self):
        self.duration = None
        self.start_time = None

    def setup(self):
        self.duration = 1.0
        self.start_time = 0.0

    def test_state_before_starting(self):
        timer = utility.CountdownTimer(duration=self.duration)
        assert_false(timer.is_running)

    def test_state_after_starting_and_before_resetting(self):
        timer = utility.CountdownTimer(duration=self.duration)
        timer.start()
        assert_true(timer.is_running)

    def test_state_after_resetting(self):
        timer = utility.CountdownTimer(duration=self.duration)
        timer.start()
        timer.reset()
        assert_false(timer.is_running)

    def test_has_positive_time_remaining(self):
        get_now_in_seconds = MockGetNowInSeconds.less_than(
            duration=self.duration,
            start_time=self.start_time)
        timer = utility.CountdownTimer(duration=self.duration,
                                       get_now_in_seconds=get_now_in_seconds)
        timer.start()
        has_time_remaining = timer.has_time_remaining
        assert_true(has_time_remaining)

    def test_has_no_time_remaining(self):
        get_now_in_seconds = MockGetNowInSeconds.equal_to(
            duration=self.duration,
            start_time=self.start_time)
        timer = utility.CountdownTimer(duration=self.duration,
                                       get_now_in_seconds=get_now_in_seconds)
        timer.start()
        has_time_remaining = timer.has_time_remaining
        assert_false(has_time_remaining)

    def test_has_negative_time_remaining(self):
        get_now_in_seconds = MockGetNowInSeconds.greater_than(
            duration=self.duration,
            start_time=self.start_time)
        timer = utility.CountdownTimer(duration=self.duration,
                                       get_now_in_seconds=get_now_in_seconds)
        timer.start()
        has_time_remaining = timer.has_time_remaining
        assert_false(has_time_remaining)
