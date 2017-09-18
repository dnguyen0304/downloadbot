# -*- coding: utf-8 -*-

from nose.tools import assert_false, assert_true, raises

from .. import continue_strategies
from ..attempt import Attempt


def test_after_result_should_continue():
    continue_strategy = continue_strategies.AfterResult(
        predicate=lambda x: x == 'foo')
    attempt = Attempt(number=None,
                      was_successful=None,
                      result='foo',
                      exception=None,
                      first_attempt_start_time=None)
    assert_true(continue_strategy.should_continue(attempt=attempt))


def test_after_result_should_not_continue():
    continue_strategy = continue_strategies.AfterResult(
        predicate=lambda x: x == 'foo')
    attempt = Attempt(number=None,
                      was_successful=None,
                      result='bar',
                      exception=None,
                      first_attempt_start_time=None)
    assert_false(continue_strategy.should_continue(attempt=attempt))


@raises(TypeError)
def test_after_result_predicate_accepts_one_argument():
    continue_strategy = continue_strategies.AfterResult(
        predicate=lambda: None)
    attempt = Attempt(number=None,
                      was_successful=None,
                      result=None,
                      exception=None,
                      first_attempt_start_time=None)
    continue_strategy.should_continue(attempt=attempt)
