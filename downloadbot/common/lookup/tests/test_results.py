# -*- coding: utf-8 -*-

from nose.tools import assert_is, assert_is_none, raises

from .. import exceptions
from .. import results


class TestFind(object):

    def setup(self):
        self.value = 'foo'
        self.zero_value = ''

    def test_or_none_returns_target_if_found(self):
        result = results.Find(value=self.value,
                              zero_value=self.zero_value)
        assert_is(result.or_none(), self.value)

    def test_or_none_returns_none_if_could_not_be_found(self):
        result = results.Find(value=self.zero_value,
                              zero_value=self.zero_value)
        assert_is_none(result.or_none())

    def test_or_none_returns_none_if_zero_value(self):
        result = results.Find(value=self.zero_value,
                              zero_value=self.zero_value)
        assert_is_none(result.or_none())

    def test_or_zero_value_returns_target_if_found(self):
        result = results.Find(value=self.value,
                              zero_value=self.zero_value)
        assert_is(result.or_zero_value(), self.value)

    def test_or_zero_value_returns_zero_value_if_could_not_be_found(self):
        result = results.Find(value=self.zero_value,
                              zero_value=self.zero_value)
        assert_is(result.or_zero_value(), self.zero_value)

    def test_or_error_returns_target_if_found(self):
        result = results.Find(value=self.value,
                              zero_value=self.zero_value)
        assert_is(result.or_raise(), self.value)

    @raises(exceptions.NoResultFound)
    def test_or_error_raises_no_result_found_if_could_not_be_found(self):
        result = results.Find(value=self.zero_value,
                              zero_value=self.zero_value)
        result.or_raise()
