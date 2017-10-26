# -*- coding: utf-8 -*-

from nose.tools import assert_false, assert_is, assert_is_none

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


class TestEveryFirstN:

    def __init__(self):
        self.n = None
        self.filter = None
        self.message = None

    def setup(self):
        self.n = len('foo')
        self.filter = filters.EveryFirstN(n=self.n)
        self.message = messaging.messages.Message(id='',
                                                  body='',
                                                  delivery_receipt='')

    def test_first_n_are_filtered(self):
        results = (self.filter.filter(message=self.message)
                   for i
                   in range(self.n))
        assert_false(any(results))

    def test_every_first_n_are_filtered(self):
        for i in range(2):
            self.test_first_n_are_filtered()
            output = self.filter.filter(message=self.message)
            assert_is(output, self.message)

    def test_after_first_n_is_not_filtered(self):
        for i in range(self.n + 1):
            output = self.filter.filter(message=self.message)
        assert_is(output, self.message)
