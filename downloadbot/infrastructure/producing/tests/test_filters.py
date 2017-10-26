# -*- coding: utf-8 -*-

from nose.tools import assert_is, assert_is_none

from .. import filters
from downloadbot.common import messaging


class TestDoublesBattle:

    def __init__(self):
        self.filter = None

    def setup(self):
        self.filter = filters.DoublesBattle()

    def test_doubles_battles_are_filtered(self):
        body = '/battle-foodoubles-0'
        input = messaging.messages.Message(id='',
                                           body=body,
                                           delivery_receipt='')
        output = self.filter.filter(message=input)
        assert_is_none(output)

    def test_non_double_battles_are_not_filtered(self):
        body = '/battle-foo-0'
        input = messaging.messages.Message(id='',
                                           body=body,
                                           delivery_receipt='')
        output = self.filter.filter(message=input)
        assert_is(output, input)
