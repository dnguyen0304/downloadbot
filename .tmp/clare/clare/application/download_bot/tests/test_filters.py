# -*- coding: utf-8 -*-

from nose.tools import assert_false, assert_is, assert_is_none

from .. import filters
from clare.common import messaging


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
