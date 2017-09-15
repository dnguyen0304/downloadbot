# -*- coding: utf-8 -*-

from nose.tools import assert_equal, assert_true, raises

from .. import HitPointsChangedRecord


class TestHitPointsChangedRecord(object):

    def test_from_message(self):
        message = '|-damage|p1a: eggs|10\/100'
        record = HitPointsChangedRecord.from_message(message)
        assert_equal(record.targeted_position, 1)
        assert_equal(record.targeted_pokemon_name, 'eggs')
        assert_equal(record.remaining_hit_points, 10)

    def test_from_message_status_condition(self):
        message = '|-damage|p1a: eggs|10\/100 par'
        record = HitPointsChangedRecord.from_message(message)
        assert_equal(record.targeted_position, 1)
        assert_equal(record.targeted_pokemon_name, 'eggs')
        assert_equal(record.remaining_hit_points, 10)

    def test_from_message_faint_status_condition(self):
        message = '|-damage|p1a: eggs|0 fnt'
        record = HitPointsChangedRecord.from_message(message)
        assert_equal(record.targeted_position, 1)
        assert_equal(record.targeted_pokemon_name, 'eggs')
        assert_equal(record.remaining_hit_points, 0)

    def test_from_message_indirect_cause(self):
        message = '|-damage|p1a: eggs|10\/100|[from] Stealth Rock'
        record = HitPointsChangedRecord.from_message(message)
        assert_equal(record.targeted_position, 1)
        assert_equal(record.targeted_pokemon_name, 'eggs')
        assert_equal(record.remaining_hit_points, 10)
        assert_true(record.indirectly_caused_by)

    def test_from_message_wish(self):
        message = '|-heal|p1a: eggs|10\/100|[from] move: Wish|[wisher] ham'
        record = HitPointsChangedRecord.from_message(message)
        assert_equal(record.targeted_position, 1)
        assert_equal(record.targeted_pokemon_name, 'eggs')
        assert_equal(record.remaining_hit_points, 10)
        assert_true(record.indirectly_caused_by)

    @raises(ValueError)
    def test_from_message_incorrect_format(self):
        message = '|foo'
        HitPointsChangedRecord.from_message(message)
