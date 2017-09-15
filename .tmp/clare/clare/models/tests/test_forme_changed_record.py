# -*- coding: utf-8 -*-

from nose.tools import assert_equal, raises

from .. import FormeChangedRecord


class TestFormeChangedRecord(object):

    def test_from_message(self):
        message = '|detailschange|p1a: eggs|eggs-Mega'
        record = FormeChangedRecord.from_message(message)
        assert_equal(record.position, 1)
        assert_equal(record.pokemon_name, 'eggs')
        assert_equal(record.forme_name, 'eggs-Mega')

    def test_from_message_with_details(self):
        message = '|detailschange|p1a: eggs|eggs-Mega, F'
        record = FormeChangedRecord.from_message(message)
        assert_equal(record.position, 1)
        assert_equal(record.pokemon_name, 'eggs')
        assert_equal(record.forme_name, 'eggs-Mega')

    @raises(ValueError)
    def test_from_message_unmatched_pattern(self):
        message = '|foo'
        FormeChangedRecord.from_message(message)
