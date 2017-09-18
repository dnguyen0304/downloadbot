# -*- coding: utf-8 -*-

from nose.tools import assert_is, assert_is_none, raises

from .. import exceptions
from .. import results


class TestFind(object):

    def setup(self):
        self.data = 'foo'
        self.result = results.Find()

    def test_or_none_returns_target_if_found(self):
        self.result.data = self.data
        assert_is(self.result.or_none(), self.data)

    def test_or_none_returns_none_if_could_not_be_found(self):
        assert_is_none(self.result.or_none())

    def test_or_error_returns_target_if_found(self):
        self.result.data = self.data
        assert_is(self.result.or_error(), self.data)

    @raises(exceptions.NoResultFound)
    def test_or_error_raises_no_result_found_if_could_not_be_found(self):
        self.result.or_error()
