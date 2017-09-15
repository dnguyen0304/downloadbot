# -*- coding: utf-8 -*-

from nose.tools import assert_false, assert_is, assert_is_none

from .. import filters
from clare.common import messaging


class TestDoublesBattleFilter(object):

    def __init__(self):
        self.filter = None

    def setup(self):
        self.filter = filters.DoublesBattleFilter()

    def test_doubles_battles_are_filtered(self):
        value = '/battle-foodoubles-0'
        record = messaging.records.Record(timestamp=None, value=value)
        output = self.filter.filter(record=record)
        assert_is_none(output)

    def test_non_double_battles_are_not_filtered(self):
        value = '/battle-foo-0'
        input = messaging.records.Record(timestamp=None, value=value)
        output = self.filter.filter(record=input)
        assert_is(output, input)


class TestEveryFirstNFilter(object):

    def __init__(self):
        self.n = None
        self.filter = None
        self.record = None

    def setup(self):
        self.n = len('foo')
        self.filter = filters.EveryFirstNFilter(n=self.n)
        self.record = messaging.records.Record(timestamp=None, value=None)

    def test_does_filter_first_n(self):
        results = (self.filter.filter(record=self.record)
                   for i
                   in xrange(self.n))
        assert_false(any(results))

    def test_does_filter_every_first_n(self):
        for i in xrange(2):
            self.test_does_filter_first_n()
            output = self.filter.filter(record=self.record)
            assert_is(output, self.record)

    def test_does_not_filter_after_first_n(self):
        for i in xrange(self.n + 1):
            output = self.filter.filter(record=self.record)
        assert_is(output, self.record)


class TestExceptGenerationSevenMetagameFilter(object):

    def __init__(self):
        self.filter = None

    def setup(self):
        self.filter = filters.ExceptGenerationSevenMetagameFilter()

    def test_does_not_filter_generation_seven_metagame_battle(self):
        value = '/battle-gen7foo-0'
        input = messaging.records.Record(timestamp=None, value=value)
        output = self.filter.filter(record=input)
        assert_is(output, input)

    def test_does_filter_non_generation_seven_metagame_battle(self):
        value = '/battle-gen0foo-0'
        record = messaging.records.Record(timestamp=None, value=value)
        record = self.filter.filter(record=record)
        assert_is_none(record)


class TestExceptOverusedMetagameFilter(object):

    def __init__(self):
        self.filter = None

    def setup(self):
        self.filter = filters.ExceptOverusedMetagameFilter()

    def test_does_not_filter_overused_metagame_battle(self):
        value = '/battle-fooou-0'
        input = messaging.records.Record(timestamp=None, value=value)
        output = self.filter.filter(record=input)
        assert_is(output, input)

    def test_does_filter_non_overused_metagame_battle(self):
        value = '/battle-foobar-0'
        record = messaging.records.Record(timestamp=None, value=value)
        record = self.filter.filter(record=record)
        assert_is_none(record)
