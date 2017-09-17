# -*- coding: utf-8 -*-

from nose.tools import assert_is, assert_is_none, raises

from .. import exceptions
from .. import results


class TestWebElementResult(object):

    def setup(self):
        self.web_element = 'foo'
        self.result = results.WebElement()

    def test_or_none_returns_web_element_if_found(self):
        self.result.web_element = self.web_element
        assert_is(self.result.or_none(), self.web_element)

    def test_or_none_returns_none_if_could_not_be_found(self):
        assert_is_none(self.result.or_none())

    def test_or_error_returns_web_element_if_found(self):
        self.result.web_element = self.web_element
        assert_is(self.result.or_error(), self.web_element)

    @raises(exceptions.NoResultFound)
    def test_or_error_raises_no_result_found_if_could_not_be_found(self):
        self.result.or_error()
