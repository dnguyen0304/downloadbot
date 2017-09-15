# -*- coding: utf-8 -*-

from nose.tools import assert_equal, raises

from .. import PlayerRecord


class TestPlayerRecord(object):

    def test_from_message(self):
        message = '|player|p1|foo|0'
        record = PlayerRecord.from_message(message)
        assert_equal(record.position, 1)
        assert_equal(record.name, 'foo')

    @raises(ValueError)
    def test_from_message_unmatched_pattern(self):
        message = '|foo'
        PlayerRecord.from_message(message)
