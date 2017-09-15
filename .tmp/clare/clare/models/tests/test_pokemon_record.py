# -*- coding: utf-8 -*-

from nose.tools import assert_equal, raises

from .. import PokemonRecord


class TestPokemonRecord(object):

    def test_from_message_no_details(self):
        message = '|poke|p1|eggs-spam|item'
        record = PokemonRecord.from_message(message)
        assert_equal(record.position, 1)
        assert_equal(record.full_name, 'eggs-spam')

    def test_from_message_one_detail(self):
        message = '|poke|p1|eggs-spam, F|item'
        record = PokemonRecord.from_message(message)
        assert_equal(record.position, 1)
        assert_equal(record.full_name, 'eggs-spam')

    def test_from_message_multiple_details(self):
        message = '|poke|p1|eggs-spam, F, shiny|item'
        record = PokemonRecord.from_message(message)
        assert_equal(record.position, 1)
        assert_equal(record.full_name, 'eggs-spam')

    @raises(ValueError)
    def test_from_message_incorrect_format(self):
        message = '|foo'
        PokemonRecord.from_message(message)
