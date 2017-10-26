# -*- coding: utf-8 -*-

from nose.tools import assert_false, assert_is, assert_is_none

from .. import filters
from clare.common import messaging


class TestExceptGenerationSevenMetagameFilter(object):

    def __init__(self):
        self.filter = None

    def setup(self):
        self.filter = filters.ExceptGenerationSevenMetagameFilter()

    def test_does_not_filter_generation_seven_metagame_battle(self):
        value = '/battle-gen7foo-0'
        input = messaging.records.Record(timestamp=None, value=value)
        output = self.filter.filter(message=input)
        assert_is(output, input)

    def test_does_filter_non_generation_seven_metagame_battle(self):
        value = '/battle-gen0foo-0'
        record = messaging.records.Record(timestamp=None, value=value)
        record = self.filter.filter(message=record)
        assert_is_none(record)


class TestExceptOverusedMetagameFilter(object):

    def __init__(self):
        self.filter = None

    def setup(self):
        self.filter = filters.ExceptOverusedMetagameFilter()

    def test_does_not_filter_overused_metagame_battle(self):
        value = '/battle-fooou-0'
        input = messaging.records.Record(timestamp=None, value=value)
        output = self.filter.filter(message=input)
        assert_is(output, input)

    def test_does_filter_non_overused_metagame_battle(self):
        value = '/battle-foobar-0'
        record = messaging.records.Record(timestamp=None, value=value)
        record = self.filter.filter(message=record)
        assert_is_none(record)
