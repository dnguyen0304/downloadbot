# -*- coding: utf-8 -*-

from nose.tools import assert_equal

from ..attempt import Attempt


class TestAttempt(object):

    def __init__(self):
        self.attempt = None

    def setup(self):
        self.attempt = Attempt.first(_get_now_in_seconds=lambda: 0)

    def test_first(self):
        assert_equal(self.attempt.number, 0)
        assert_equal(self.attempt.first_attempt_start_time, 0)

    def test_next(self):
        next_attempt = next(self.attempt)
        assert_equal(next_attempt.number, self.attempt.number + 1)
        assert_equal(next_attempt.first_attempt_start_time,
                     self.attempt.first_attempt_start_time)
